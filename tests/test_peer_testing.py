"""Features added for peer testing: ratings (FR-10, NFR-05), report download (FR-12),
one exercise per scenario per browser, and answers locked once scored."""
import pytest

from app import app
from models import ExerciseSession, Response

BEST_SC01 = ["d", "b", "b"]


def finish(client, scenario_id, choices, pre=None):
    client.get(f"/scenario/{scenario_id}/start")
    for number, choice in enumerate(choices, start=1):
        data = {"option_id": choice}
        if number == 1 and pre is not None:
            data["pre_understanding"] = pre
        client.post(f"/scenario/{scenario_id}/decision/{number}", data=data)


def test_ratings_before_and_after_are_saved():
    client = app.test_client()
    finish(client, "sc01", BEST_SC01, pre="2")
    response = client.post("/scenario/sc01/feedback",
                           data={"post_understanding": "4", "usefulness": "5"})
    assert response.status_code == 302
    with app.app_context():
        exercise = ExerciseSession.query.one()
        assert (exercise.pre_understanding, exercise.post_understanding, exercise.usefulness) == (2, 4, 5)
    assert "Your answers were saved" in client.get("/scenario/sc01/summary").get_data(as_text=True)


def test_rating_is_optional_for_scripts_but_saved_when_given():
    client = app.test_client()
    finish(client, "sc01", BEST_SC01)
    with app.app_context():
        assert ExerciseSession.query.one().pre_understanding is None


@pytest.mark.parametrize("bad", ["0", "6", "abc", "3.5"])
def test_out_of_range_pre_rating_is_rejected_and_nothing_saved(bad):
    client = app.test_client()
    client.get("/scenario/sc01/start")
    response = client.post("/scenario/sc01/decision/1",
                           data={"option_id": "d", "pre_understanding": bad})
    assert response.status_code == 400
    with app.app_context():
        assert Response.query.count() == 0
        assert ExerciseSession.query.one().pre_understanding is None


@pytest.mark.parametrize("form", [
    {"post_understanding": "4"},                       # usefulness missing
    {"post_understanding": "9", "usefulness": "4"},    # out of range
    {"post_understanding": "4", "usefulness": "x"},    # not a number
])
def test_incomplete_or_invalid_feedback_is_rejected(form):
    client = app.test_client()
    finish(client, "sc01", BEST_SC01)
    assert client.post("/scenario/sc01/feedback", data=form).status_code == 400
    with app.app_context():
        assert ExerciseSession.query.one().usefulness is None


def test_feedback_before_finishing_is_not_accepted():
    client = app.test_client()
    finish(client, "sc01", ["d"])
    response = client.post("/scenario/sc01/feedback",
                           data={"post_understanding": "4", "usefulness": "4"})
    assert response.status_code == 302
    with app.app_context():
        assert ExerciseSession.query.one().usefulness is None


def test_answers_are_locked_once_scored():
    client = app.test_client()
    finish(client, "sc01", BEST_SC01)
    response = client.post("/scenario/sc01/decision/1", data={"option_id": "a"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/scenario/sc01/summary")
    with app.app_context():
        saved = {r.decision_point_id: r.option_id for r in Response.query.all()}
    assert saved == {"dp1": "d", "dp2": "b", "dp3": "b"}


def test_starting_a_second_scenario_keeps_the_first_report():
    client = app.test_client()
    finish(client, "sc01", BEST_SC01)
    finish(client, "sc02", ["c", "a", "b"])
    first = client.get("/scenario/sc01/report")
    second = client.get("/scenario/sc02/report")
    assert first.status_code == 200 and second.status_code == 200
    assert "Drifting Positions" in first.get_data(as_text=True)
    assert "The Helpful Caller" in second.get_data(as_text=True)


def test_report_downloads_as_a_text_file_matching_the_page():
    client = app.test_client()
    finish(client, "sc01", ["d", "b", "c"])
    response = client.get("/scenario/sc01/report.txt")
    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert response.headers["Content-Disposition"].startswith('attachment; filename="autogsesec-sc01-report-')
    text = response.get_data(as_text=True)
    assert "Readiness rating: Prepared" in text
    assert "Score: 5 of 6 points (83.3%)" in text
    assert "CP-10 System Recovery and Reconstitution" in text
    assert "not a security" in text


def test_download_requires_a_finished_exercise():
    client = app.test_client()
    finish(client, "sc01", ["d"])
    assert client.get("/scenario/sc01/report.txt").status_code == 302


def test_results_export_summarizes_sessions_without_personal_data():
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    from export_results import FIELDS, session_rows, summarize
    from app import SCENARIOS

    client = app.test_client()
    finish(client, "sc01", BEST_SC01, pre="2")
    client.post("/scenario/sc01/feedback", data={"post_understanding": "4", "usefulness": "5"})
    finish(client, "sc02", ["c"], pre="3")                      # abandoned after decision 1
    with app.app_context():
        rows = session_rows(ExerciseSession.query.order_by(ExerciseSession.started_at).all(),
                            SCENARIOS)
    summary = summarize(rows)
    assert summary["sessions_started"] == 2
    assert summary["sessions_completed"] == 1
    assert summary["usefulness_mean"] == 5
    assert summary["paired_change_mean"] == 2
    assert summary["readiness_counts"]["Prepared"] == 1
    assert set(rows[0]) == set(FIELDS)
    assert len(rows[0]["session"]) == 8                       # shortened random id only
    