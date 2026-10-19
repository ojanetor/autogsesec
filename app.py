import os
import sys
from importlib.metadata import version

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect

from config import database_url, is_production, secret_key
from engine.content import load_all, load_control_names
from engine.report import build_report
from engine.scoring import ScoringError, score_session
from models import ExerciseSession, Response, db, utc_now

app = Flask(__name__)
app.secret_key = secret_key()
app.config["SQLALCHEMY_DATABASE_URI"] = database_url()
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = is_production()

csrf = CSRFProtect(app)
db.init_app(app)
with app.app_context():
    db.create_all()

SCENARIOS = load_all()
CONTROL_NAMES = load_control_names()


def get_scenario_or_404(scenario_id):
    scenario = SCENARIOS.get(scenario_id)
    if scenario is None:
        abort(404)
    return scenario


def content_version_tag(scenario):
    versions = scenario["framework_versions"]
    return f"ATT&CK for ICS {versions['attack_ics']}; NIST SP 800-82 {versions['nist_sp800_82']}"


def current_exercise(scenario_id):
    """Return this browser's exercise session for the scenario, or None."""
    exercise_id = session.get("exercise_id")
    if exercise_id is None:
        return None
    exercise = db.session.get(ExerciseSession, exercise_id)
    if exercise is None or exercise.scenario_id != scenario_id:
        return None
    return exercise


def complete_answers(scenario, exercise):
    """Return {decision_point_id: option_id} if every decision is answered, else None."""
    answers = {r.decision_point_id: r.option_id for r in exercise.responses}
    if any(point["id"] not in answers for point in scenario["decision_points"]):
        return None
    return answers


def mark_complete(exercise):
    if exercise.completed_at is None:
        exercise.completed_at = utc_now()
        db.session.commit()


@app.route("/")
def home():
    return render_template("index.html", scenarios=SCENARIOS.values())


@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        database = "ok"
    except Exception:
        database = "unavailable"
    return jsonify(
        status="ok",
        python_version=sys.version.split()[0],
        flask_version=version("flask"),
        sqlalchemy_version=version("sqlalchemy"),
        database=database,
        database_engine=db.engine.dialect.name,
        scenarios_loaded=len(SCENARIOS),
    )


@app.route("/scenario/<scenario_id>/start")
def start(scenario_id):
    scenario = get_scenario_or_404(scenario_id)
    exercise = ExerciseSession(scenario_id=scenario_id, content_version=content_version_tag(scenario))
    db.session.add(exercise)
    db.session.commit()
    session["exercise_id"] = exercise.session_id
    return redirect(url_for("decision", scenario_id=scenario_id, number=1))


@app.route("/scenario/<scenario_id>/decision/<int:number>", methods=["GET", "POST"])
def decision(scenario_id, number):
    scenario = get_scenario_or_404(scenario_id)
    points = scenario["decision_points"]
    if number < 1 or number > len(points):
        abort(404)
    exercise = current_exercise(scenario_id)
    if exercise is None:
        return redirect(url_for("start", scenario_id=scenario_id))

    point = points[number - 1]

    if request.method == "POST":
        choice = request.form.get("option_id", "")
        allowed = {option["id"] for option in point["options"]}
        if choice not in allowed:
            return render_template(
                "decision.html", scenario=scenario, point=point,
                number=number, total=len(points),
                error="Please choose one of the listed options.",
            ), 400

        existing = Response.query.filter_by(
            session_id=exercise.session_id, decision_point_id=point["id"]
        ).first()
        if existing:
            existing.option_id = choice
            existing.submitted_at = utc_now()
        else:
            db.session.add(Response(
                session_id=exercise.session_id,
                decision_point_id=point["id"],
                option_id=choice,
            ))
        db.session.commit()

        if number < len(points):
            return redirect(url_for("decision", scenario_id=scenario_id, number=number + 1))
        return redirect(url_for("summary", scenario_id=scenario_id))

    return render_template(
        "decision.html", scenario=scenario, point=point,
        number=number, total=len(points), error=None,
    )


@app.route("/scenario/<scenario_id>/summary")
def summary(scenario_id):
    scenario = get_scenario_or_404(scenario_id)
    exercise = current_exercise(scenario_id)
    if exercise is None:
        return redirect(url_for("start", scenario_id=scenario_id))
    answers = complete_answers(scenario, exercise)
    if answers is None:
        return redirect(url_for("start", scenario_id=scenario_id))

    rows = []
    for point in scenario["decision_points"]:
        chosen_id = answers[point["id"]]
        option = next(o for o in point["options"] if o["id"] == chosen_id)
        entry = scenario["mapping"][point["id"]][chosen_id]
        rows.append({
            "prompt": point["prompt"],
            "choice": option["text"],
            "controls": entry["nist_controls"],
            "rating": entry["rating"],
        })

    mark_complete(exercise)
    try:
        score = score_session(scenario, answers)
    except ScoringError:
        app.logger.exception("Scoring failed for session %s", exercise.session_id)
        return render_template("error.html"), 500
    return render_template("summary.html", scenario=scenario, rows=rows, score=score)


@app.route("/scenario/<scenario_id>/report")
def report(scenario_id):
    """After-action report (FR-06 to FR-08), regenerated from stored responses."""
    scenario = get_scenario_or_404(scenario_id)
    exercise = current_exercise(scenario_id)
    if exercise is None:
        return redirect(url_for("start", scenario_id=scenario_id))
    answers = complete_answers(scenario, exercise)
    if answers is None:
        return redirect(url_for("start", scenario_id=scenario_id))

    mark_complete(exercise)
    try:
        score = score_session(scenario, answers)
        aar = build_report(scenario, score, CONTROL_NAMES)
    except ScoringError:
        # UC-01 exception path: responses stay saved; nothing is scored incorrectly.
        app.logger.exception("Report failed for session %s", exercise.session_id)
        return render_template("error.html"), 500
    return render_template("report.html", scenario=scenario, report=aar, exercise=exercise)


if __name__ == "__main__":
    app.run(debug=True)