"""Scoring engine tests (T7): correctness, boundaries, determinism (NFR-06)."""
from itertools import product

import pytest

from app import SCENARIOS, app
from engine import content
from engine.scoring import POINTS, ScoringError, readiness_for, score_session

SC01 = SCENARIOS["sc01"]
POINT_IDS = [p["id"] for p in SC01["decision_points"]]


def all_answer_combinations(scenario):
    choices = [[o["id"] for o in p["options"]] for p in scenario["decision_points"]]
    for combo in product(*choices):
        yield dict(zip(POINT_IDS, combo))


def test_best_answers_score_100_percent():
    result = score_session(SC01, {"dp1": "d", "dp2": "b", "dp3": "b"})
    assert (result["earned"], result["possible"], result["percent"]) == (6, 6, 100.0)
    assert result["readiness"] == "Prepared"
    assert result["gaps"] == []


def test_worst_answers_score_zero_and_list_every_gap():
    result = score_session(SC01, {"dp1": "a", "dp2": "a", "dp3": "a"})
    assert result["earned"] == 0
    assert result["readiness"] == "Unprepared"
    assert len(result["gaps"]) == 3


def test_gaps_are_ordered_immediate_first():
    result = score_session(SC01, {"dp1": "b", "dp2": "a", "dp3": "c"})
    order = [g["timeline"] for g in result["gaps"]]
    assert order == ["immediate", "short_term", "long_term"]


@pytest.mark.parametrize("earned, label", [
    (6, "Prepared"), (5, "Prepared"), (4, "Developing"),
    (3, "Developing"), (2, "Unprepared"), (0, "Unprepared"),
])
def test_readiness_band_boundaries(earned, label):
    assert readiness_for(earned, 6) == label


def test_exact_boundary_is_not_lost_to_rounding():
    assert readiness_for(4, 5) == "Prepared"      # exactly 80%
    assert readiness_for(1, 2) == "Developing"    # exactly 50%


def test_every_possible_answer_combination_scores_consistently():
    """All 4 x 4 x 4 = 64 combinations: totals, gaps and bands agree with the rubric."""
    combinations = list(all_answer_combinations(SC01))
    assert len(combinations) == 64
    for answers in combinations:
        result = score_session(SC01, answers)
        ratings = [SC01["mapping"][pid][answers[pid]]["rating"] for pid in POINT_IDS]
        assert result["earned"] == sum(POINTS[r] for r in ratings)
        assert len(result["gaps"]) == sum(r != "correct" for r in ratings)
        assert result["readiness"] == readiness_for(result["earned"], result["possible"])
        for gap in result["gaps"]:
            assert gap["nist_controls"], "every gap must name a NIST control"


def test_same_answers_give_identical_results_ten_times():
    """NFR-06: identical input scored 10 times gives 100% identical output."""
    answers = {"dp1": "b", "dp2": "c", "dp3": "a"}
    results = [score_session(SC01, answers) for _ in range(10)]
    assert all(r == results[0] for r in results)


def test_missing_answer_is_refused():
    with pytest.raises(ScoringError):
        score_session(SC01, {"dp1": "d", "dp2": "b"})


def test_unmapped_option_is_refused():
    with pytest.raises(ScoringError):
        score_session(SC01, {"dp1": "z", "dp2": "b", "dp3": "b"})


def test_summary_page_shows_readiness():
    client = app.test_client()
    client.get("/scenario/sc01/start")
    for number, choice in [(1, "d"), (2, "b"), (3, "b")]:
        client.post(f"/scenario/sc01/decision/{number}", data={"option_id": choice})
    page = client.get("/scenario/sc01/summary").get_data(as_text=True)
    assert "Prepared" in page
    assert "6 of 6 points" in page


def _one_point_scenario(entries):
    scenario = {"id": "t", "decision_points": [
        {"id": "dp1", "options": [{"id": k} for k in entries]}]}
    mapping = {"scenario_id": "t", "attack_tactic": "TA0101",
               "decision_points": {"dp1": entries}}
    return scenario, mapping


def test_validator_requires_a_timeline_for_wrong_answers():
    scenario, mapping = _one_point_scenario({
        "a": {"rating": "correct", "nist_controls": ["IR-4"], "timeline": None},
        "b": {"rating": "incorrect", "nist_controls": ["IR-4"], "timeline": None},
    })
    with pytest.raises(ValueError, match="needs a timeline"):
        content._validate(scenario, mapping, {"TA0101"}, {"IR-4"})


def test_validator_requires_a_correct_option():
    scenario, mapping = _one_point_scenario({
        "a": {"rating": "partial", "nist_controls": ["IR-4"], "timeline": "immediate"},
    })
    with pytest.raises(ValueError, match="at least one correct option"):
        content._validate(scenario, mapping, {"TA0101"}, {"IR-4"})
