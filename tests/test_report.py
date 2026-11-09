"""After-action report tests (T8): known answers, report page, error path."""
import json
from pathlib import Path

import pytest

import app as app_module
from app import CONTROL_NAMES, SCENARIOS, app
from engine.report import build_report
from engine.scoring import ScoringError, score_session
from models import Response

DATA_DIR = Path(__file__).parent / "data"
KNOWN_FILES = sorted(DATA_DIR.glob("known_answers_*.json"))
KNOWN_CASES = [
    (known["scenario_id"], case)
    for known in (json.loads(f.read_text()) for f in KNOWN_FILES)
    for case in known["cases"]
]
SC01 = SCENARIOS["sc01"]


def test_every_scenario_has_known_answer_cases():
    covered = {scenario_id for scenario_id, _ in KNOWN_CASES}
    assert covered == set(SCENARIOS)


@pytest.mark.parametrize("scenario_id, case", KNOWN_CASES,
                         ids=[f"{sid}-{c['id']}" for sid, c in KNOWN_CASES])
def test_known_answer_cases(scenario_id, case):
    """Engine output must equal the hand-computed expected values."""
    scenario = SCENARIOS[scenario_id]
    expected = case["expected"]
    score = score_session(scenario, case["answers"])
    report = build_report(scenario, score, CONTROL_NAMES)

    assert score["earned"] == expected["earned"]
    assert score["percent"] == expected["percent"]
    assert report["readiness"] == expected["readiness"]
    assert [g["decision_point_id"] for g in score["gaps"]] == expected["gap_order"]
    recommended = {
        group["timeline"]: [c["id"] for c in group["controls"]]
        for group in report["recommendations"]
    }
    assert recommended == expected["recommended"]


@pytest.mark.parametrize("scenario_id", sorted(SCENARIOS))
def test_every_mapped_control_has_a_name_and_family(scenario_id):
    """Every control any option can recommend has a catalog name and a known family."""
    from engine.report import CONTROL_FAMILIES
    for point_map in SCENARIOS[scenario_id]["mapping"].values():
        for entry in point_map.values():
            for control_id in entry["nist_controls"]:
                assert control_id in CONTROL_NAMES
                assert control_id.split("-")[0] in CONTROL_FAMILIES


def test_report_is_identical_across_ten_runs():
    answers = {"dp1": "c", "dp2": "b", "dp3": "d"}
    reports = [build_report(SC01, score_session(SC01, answers), CONTROL_NAMES) for _ in range(10)]
    assert all(r == reports[0] for r in reports)


def finish_scenario(client, choices):
    client.get("/scenario/sc01/start")
    for number, choice in enumerate(choices, start=1):
        client.post(f"/scenario/sc01/decision/{number}", data={"option_id": choice})


def test_report_page_shows_rating_controls_and_timelines():
    client = app.test_client()
    finish_scenario(client, ["d", "d", "d"])
    page = client.get("/scenario/sc01/report").get_data(as_text=True)
    assert "After-action report" in page
    assert "Unprepared" in page
    assert "Immediate (within 30 days)" in page
    assert "IR-6 Incident Reporting" in page
    assert "not a security assessment" in page


def test_report_requires_a_finished_session():
    client = app.test_client()
    client.get("/scenario/sc01/start")
    client.post("/scenario/sc01/decision/1", data={"option_id": "d"})
    response = client.get("/scenario/sc01/report")
    assert response.status_code == 302


def test_scoring_failure_shows_error_and_keeps_responses(monkeypatch):
    """UC-01 exception path: no wrong score is shown and saved answers survive."""
    client = app.test_client()
    finish_scenario(client, ["d", "b", "b"])

    def broken(*args, **kwargs):
        raise ScoringError("simulated rubric failure")

    monkeypatch.setattr(app_module, "score_session", broken)
    response = client.get("/scenario/sc01/report")
    assert response.status_code == 500
    assert "could not score this session" in response.get_data(as_text=True)
    with app.app_context():
        assert Response.query.count() == 3