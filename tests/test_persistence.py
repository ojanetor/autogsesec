"""Persistence tests for sessions and responses (FR-03, NFR-09)."""
from app import app
from models import ExerciseSession, Response, db


def walk_through(client, choices):
    client.get("/scenario/sc01/start")
    for number, choice in enumerate(choices, start=1):
        client.post(f"/scenario/sc01/decision/{number}", data={"option_id": choice})


def test_completed_walkthrough_is_saved():
    client = app.test_client()
    walk_through(client, ["d", "b", "b"])
    client.get("/scenario/sc01/summary")
    with app.app_context():
        exercise = ExerciseSession.query.one()
        saved = {r.decision_point_id: r.option_id for r in exercise.responses}
        assert saved == {"dp1": "d", "dp2": "b", "dp3": "b"}
        assert exercise.completed_at is not None
        assert "v19.2" in exercise.content_version


def test_resubmitting_a_decision_keeps_the_last_answer():
    client = app.test_client()
    walk_through(client, ["a"])
    client.post("/scenario/sc01/decision/1", data={"option_id": "d"})
    with app.app_context():
        rows = Response.query.all()
        assert len(rows) == 1
        assert rows[0].option_id == "d"


def test_invalid_option_is_not_saved():
    client = app.test_client()
    client.get("/scenario/sc01/start")
    client.post("/scenario/sc01/decision/1", data={"option_id": "zzz"})
    with app.app_context():
        assert Response.query.count() == 0


def test_abandoned_session_has_no_completion_time():
    client = app.test_client()
    walk_through(client, ["d"])
    with app.app_context():
        assert ExerciseSession.query.one().completed_at is None


def test_schema_has_no_personal_data_columns():
    expected_sessions = {
        "session_id", "scenario_id", "content_version", "started_at",
        "completed_at", "pre_understanding", "post_understanding",
    }
    expected_responses = {
        "response_id", "session_id", "decision_point_id", "option_id", "submitted_at",
    }
    with app.app_context():
        columns = {
            table.name: {column.name for column in table.columns}
            for table in db.metadata.sorted_tables
        }
    assert columns == {"sessions": expected_sessions, "responses": expected_responses}