"""Scoring engine (task T7): deterministic, rule-based scoring.

Every point awarded comes from a rating in the scenario's mapping file, and
every rating names the NIST SP 800-82 controls behind it. There is no
randomness and no machine learning: the same answers always give the same
result (NFR-06).

Method: docs/architecture.md, "Computational method".
"""

POINTS = {"correct": 2, "partial": 1, "incorrect": 0}
MAX_POINTS = POINTS["correct"]
READINESS_BANDS = [(80, "Prepared"), (50, "Developing"), (0, "Unprepared")]
TIMELINE_ORDER = {"immediate": 0, "short_term": 1, "long_term": 2}


class ScoringError(Exception):
    """Raised when answers cannot be scored against the scenario's mapping."""


def readiness_for(earned, possible):
    """Return the readiness label for a score.

    Uses whole-number arithmetic (earned * 100 >= threshold * possible) so a
    score sitting exactly on a band boundary is never misjudged by rounding.
    """
    for threshold, label in READINESS_BANDS:
        if earned * 100 >= threshold * possible:
            return label
    raise ScoringError("score is below every readiness band")


def score_session(scenario, answers):
    """Score one completed session.

    scenario: a scenario dict returned by engine.content.load_all()
    answers:  {decision_point_id: option_id}
    returns:  {"earned", "possible", "percent", "readiness", "results", "gaps"}
    """
    earned = 0
    possible = 0
    results = []

    for point in scenario["decision_points"]:
        point_id = point["id"]
        option_id = answers.get(point_id)
        if option_id is None:
            raise ScoringError(f"no answer recorded for {point_id}")
        entry = scenario["mapping"].get(point_id, {}).get(option_id)
        if entry is None:
            raise ScoringError(f"{point_id} option {option_id} has no mapping entry")

        points = POINTS[entry["rating"]]
        earned += points
        possible += MAX_POINTS
        results.append({
            "decision_point_id": point_id,
            "option_id": option_id,
            "rating": entry["rating"],
            "points": points,
            "nist_controls": list(entry["nist_controls"]),
            "timeline": entry.get("timeline"),
            "rationale": entry["rationale"],
        })

    if possible == 0:
        raise ScoringError("scenario has no decision points")

    gaps = sorted(
        (r for r in results if r["rating"] != "correct"),
        key=lambda r: TIMELINE_ORDER[r["timeline"]],
    )

    return {
        "earned": earned,
        "possible": possible,
        "percent": round(earned * 100 / possible, 1),
        "readiness": readiness_for(earned, possible),
        "results": results,
        "gaps": gaps,
    }
