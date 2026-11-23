import os
import sys
from importlib.metadata import version

from flask import Flask, Response as HttpResponse, abort, jsonify, redirect, render_template, request, session, url_for
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFError, CSRFProtect

from config import database_url, is_production, secret_key
from engine.content import load_all, load_control_names
from engine.report import build_report, report_as_text
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
migrate = Migrate(app, db)

# Production builds its schema with migrations (`flask --app app db upgrade`,
# run by the Render start command). Development and tests create it directly.
if not is_production():
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


RATING_SCALE = range(1, 6)  # 1 = very low, 5 = very high


def current_exercise(scenario_id):
    """Return this browser's exercise session for the scenario, or None.

    The browser cookie keeps one exercise per scenario, so finishing one
    scenario and starting another does not lose the first report.
    """
    exercise_id = session.get("exercises", {}).get(scenario_id)
    if exercise_id is None:
        return None
    exercise = db.session.get(ExerciseSession, exercise_id)
    if exercise is None or exercise.scenario_id != scenario_id:
        return None
    return exercise


def parse_rating(value):
    """Return an int 1-5 from a form value, None if blank; raise ValueError otherwise."""
    if value is None or value == "":
        return None
    rating = int(value)
    if rating not in RATING_SCALE:
        raise ValueError("rating out of range")
    return rating


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
    exercises = dict(session.get("exercises", {}))
    exercises[scenario_id] = exercise.session_id
    session["exercises"] = exercises
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

    if exercise.completed_at is not None:
        # Answers are locked once the exercise is scored.
        return redirect(url_for("summary", scenario_id=scenario_id))

    point = points[number - 1]

    if request.method == "POST":
        choice = request.form.get("option_id", "")
        allowed = {option["id"] for option in point["options"]}
        try:
            pre_rating = parse_rating(request.form.get("pre_understanding")) if number == 1 else None
        except ValueError:
            choice = None
        if choice not in allowed:
            return render_template(
                "decision.html", scenario=scenario, point=point,
                number=number, total=len(points),
                error="Please choose one of the listed options.",
            ), 400
        if pre_rating is not None:
            exercise.pre_understanding = pre_rating

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
        mark_complete(exercise)
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
    return render_template("summary.html", scenario=scenario, rows=rows, score=score,
                           exercise=exercise, error=None)


@app.route("/scenario/<scenario_id>/feedback", methods=["POST"])
def feedback(scenario_id):
    """Post-exercise questions (FR-10, NFR-05): understanding after, and usefulness."""
    scenario = get_scenario_or_404(scenario_id)
    exercise = current_exercise(scenario_id)
    if exercise is None or exercise.completed_at is None:
        return redirect(url_for("start", scenario_id=scenario_id))
    try:
        post_rating = parse_rating(request.form.get("post_understanding"))
        usefulness = parse_rating(request.form.get("usefulness"))
    except ValueError:
        post_rating = usefulness = None
    if post_rating is None or usefulness is None:
        abort(400)
    exercise.post_understanding = post_rating
    exercise.usefulness = usefulness
    db.session.commit()
    return redirect(url_for("summary", scenario_id=scenario["id"]))


def finished_report(scenario_id):
    """Return (scenario, exercise, report) for a finished exercise, or a response to send instead."""
    scenario = get_scenario_or_404(scenario_id)
    exercise = current_exercise(scenario_id)
    if exercise is None:
        return None, redirect(url_for("start", scenario_id=scenario_id))
    answers = complete_answers(scenario, exercise)
    if answers is None:
        return None, redirect(url_for("start", scenario_id=scenario_id))

    mark_complete(exercise)
    try:
        score = score_session(scenario, answers)
        aar = build_report(scenario, score, CONTROL_NAMES)
    except ScoringError:
        # UC-01 exception path: responses stay saved; nothing is scored incorrectly.
        app.logger.exception("Report failed for session %s", exercise.session_id)
        return None, (render_template("error.html"), 500)
    return (scenario, exercise, aar), None


@app.route("/scenario/<scenario_id>/report")
def report(scenario_id):
    """After-action report (FR-06 to FR-08), regenerated from stored responses."""
    found, other = finished_report(scenario_id)
    if other is not None:
        return other
    scenario, exercise, aar = found
    return render_template("report.html", scenario=scenario, report=aar, exercise=exercise)


@app.route("/scenario/<scenario_id>/report.txt")
def report_download(scenario_id):
    """The same report as a plain-text file the participant can keep (FR-12)."""
    found, other = finished_report(scenario_id)
    if other is not None:
        return other
    scenario, exercise, aar = found
    short_id = exercise.session_id[:8]
    return HttpResponse(
        report_as_text(aar, short_id),
        mimetype="text/plain",
        headers={"Content-Disposition":
                 f'attachment; filename="autogsesec-{scenario["id"]}-report-{short_id}.txt"'},
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        "error.html",
        heading="Page not found",
        message="That page or scenario does not exist. Choose a scenario from the library.",
    ), 404


@app.errorhandler(CSRFError)
def form_token_rejected(error):
    return render_template(
        "error.html",
        heading="This form has expired",
        message="The form's security token was missing or expired, so nothing was saved "
                "from this request. Start the scenario again from the library.",
    ), 400


@app.errorhandler(500)
def server_error(error):
    return render_template(
        "error.html",
        heading="Something went wrong",
        message="The server hit an unexpected error. Any answers already submitted are saved.",
    ), 500


if __name__ == "__main__":
    # The interactive debugger is off unless explicitly requested with FLASK_DEBUG=1.
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
