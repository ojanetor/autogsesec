"""Scoring engine. Placeholder: built in Hard Stop 4 (task T7).

The interface is fixed now so routes and tests can be written against it.
Method: docs/architecture.md, "Computational method".
"""

POINTS = {"correct": 2, "partial": 1, "incorrect": 0}
READINESS_BANDS = [(80, "Prepared"), (50, "Developing"), (0, "Unprepared")]


def score_session(scenario, answers):
    """Score one completed session.

    scenario: a scenario dict returned by engine.content.load_all()
    answers:  {decision_point_id: option_id}
    returns:  {"percent": float, "readiness": str, "gaps": list}
    """
    raise NotImplementedError("Scoring engine is scheduled for Hard Stop 4 (task T7).")