"""Database housekeeping: find and remove sessions that should not be kept.

Two kinds of session can be removed:
- abandoned: started but never finished, and older than a cut-off
  (use case UC-01 alternate path: a partial session is discarded, no report);
- test data: every session started before a given time, used once to clear
  benchmark and demo sessions before peer testing.

Responses are deleted together with their session. Nothing here identifies a
person; sessions are random identifiers (NFR-09).
"""
from datetime import timedelta

from models import ExerciseSession, db, utc_now


def find_sessions(abandoned_hours=None, started_before=None, now=None):
    """Return the sessions that match. Exactly one rule must be given."""
    if (abandoned_hours is None) == (started_before is None):
        raise ValueError("give exactly one of abandoned_hours or started_before")
    query = ExerciseSession.query
    if abandoned_hours is not None:
        if abandoned_hours < 1:
            raise ValueError("abandoned_hours must be at least 1")
        cutoff = (now or utc_now()) - timedelta(hours=abandoned_hours)
        query = query.filter(ExerciseSession.completed_at.is_(None),
                             ExerciseSession.started_at < cutoff)
    else:
        if started_before.tzinfo is None:
            raise ValueError("started_before must include a time zone (use UTC)")
        query = query.filter(ExerciseSession.started_at < started_before)
    return query.order_by(ExerciseSession.started_at).all()


def purge(sessions, apply=False):
    """Count the sessions and responses; delete them only when apply=True."""
    counts = {"sessions": len(sessions),
              "responses": sum(len(s.responses) for s in sessions),
              "deleted": False}
    if apply and sessions:
        for exercise in sessions:
            db.session.delete(exercise)  # responses go too (cascade)
        db.session.commit()
        counts["deleted"] = True
    return counts