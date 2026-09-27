import os
import sys
from importlib.metadata import version

from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for

from engine.content import load_all

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-before-deploying")

SCENARIOS = load_all()


def get_scenario_or_404(scenario_id):
    scenario = SCENARIOS.get(scenario_id)
    if scenario is None:
        abort(404)
    return scenario


@app.route("/")
def home():
    return render_template("index.html", scenarios=SCENARIOS.values())


@app.route("/health")
def health():
    return jsonify(
        status="ok",
        python_version=sys.version.split()[0],
        flask_version=version("flask"),
        scenarios_loaded=len(SCENARIOS),
    )


@app.route("/scenario/<scenario_id>/start")
def start(scenario_id):
    get_scenario_or_404(scenario_id)
    session["scenario_id"] = scenario_id
    session["answers"] = {}
    return redirect(url_for("decision", scenario_id=scenario_id, number=1))


@app.route("/scenario/<scenario_id>/decision/<int:number>", methods=["GET", "POST"])
def decision(scenario_id, number):
    scenario = get_scenario_or_404(scenario_id)
    points = scenario["decision_points"]
    if number < 1 or number > len(points):
        abort(404)
    if session.get("scenario_id") != scenario_id:
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
        answers = session.get("answers", {})
        answers[point["id"]] = choice
        session["answers"] = answers
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
    answers = session.get("answers", {})
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
    return render_template("summary.html", scenario=scenario, rows=rows)


if __name__ == "__main__":
    app.run(debug=True)