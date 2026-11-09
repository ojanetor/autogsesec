"""Housekeeping tests: abandoned-session and test-data purge (UC-01 alternate path)."""
from datetime import datetime, timedelta, timezone

import pytest

from app import app
from maintenance import find_sessions, purge
from models import ExerciseSession, Response, db

NOW = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)


def add_session(hours_ago, finished, answers=1):
    exercise = ExerciseSession(scenario_id="sc01", content_version="test",
                               started_at=NOW - timedelta(hours=hours_ago))
    if finished:
        exercise.completed_at = exercise.started_at + timedelta(minutes=5)
    db.session.add(exercise)
    db.session.flush()
    for n in range(1, answers + 1):
        db.session.add(Response(session_id=exercise.session_id,
                                decision_point_id=f"dp{n}", option_id="a"))
    db.session.commit()
    return exercise.session_id


def test_only_old_unfinished_sessions_count_as_abandoned():
    with app.app_context():
        old_unfinished = add_session(48, finished=False)
        add_session(2, finished=False)             # recent, may still be in progress
        add_session(48, finished=True, answers=3)  # finished sessions are kept
        found = find_sessions(abandoned_hours=24, now=NOW)
        assert [s.session_id for s in found] == [old_unfinished]


def test_dry_run_deletes_nothing():
    with app.app_context():
        add_session(48, finished=False, answers=2)
        counts = purge(find_sessions(abandoned_hours=24, now=NOW), apply=False)
        assert counts == {"sessions": 1, "responses": 2, "deleted": False}
        assert ExerciseSession.query.count() == 1
        assert Response.query.count() == 2


def test_apply_deletes_sessions_and_their_responses():
    with app.app_context():
        add_session(48, finished=False, answers=2)
        keep = add_session(1, finished=True, answers=3)
        counts = purge(find_sessions(abandoned_hours=24, now=NOW), apply=True)
        assert counts == {"sessions": 1, "responses": 2, "deleted": True}
        assert [s.session_id for s in ExerciseSession.query.all()] == [keep]
        assert Response.query.count() == 3


def test_started_before_clears_all_test_data_before_a_time():
    with app.app_context():
        add_session(30, finished=True, answers=3)
        add_session(26, finished=False)
        recent = add_session(1, finished=True, answers=3)
        cutoff = NOW - timedelta(hours=24)
        counts = purge(find_sessions(started_before=cutoff), apply=True)
        assert counts["sessions"] == 2
        assert [s.session_id for s in ExerciseSession.query.all()] == [recent]


@pytest.mark.parametrize("kwargs", [
    {},                                                   # no rule
    {"abandoned_hours": 24, "started_before": NOW},       # two rules
    {"abandoned_hours": 0},                               # would remove sessions in progress
    {"started_before": datetime(2026, 11, 18)},           # no time zone
])
def test_unsafe_or_ambiguous_requests_are_refused(kwargs):
    with app.app_context():
        with pytest.raises(ValueError):
            find_sessions(**kwargs)

            