import os
import sys
from importlib.metadata import version

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for

from engine.content import load_all
from models import ExerciseSession, Response, db, utc_now

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-before-deploying")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///autogsesec.db")

db.init_app(app)
with app.app_context():
    db.create_all()

SCENARIOS = load_all()


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

    answers = {r.decision_point_id: r.option_id for r in exercise.responses}
    rows = []
    for point in scenario["decision_points"]:
        chosen_id = answers.get(point["id"])
        if chosen_id is None:
            return redirect(url_for("start", scenario_id=scenario_id))
        option = next(o for o in point["options"] if o["id"] == chosen_id)
        entry = scenario["mapping"][point["id"]][chosen_id]
        rows.append({
            "prompt": point["prompt"],
            "choice": option["text"],
            "controls": entry["nist_controls"],
        })

    if exercise.completed_at is None:
        exercise.completed_at = utc_now()
        db.session.commit()

    return render_template("summary.html", scenario=scenario, rows=rows)


if __name__ == "__main__":
    app.run(debug=True)