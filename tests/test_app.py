import pytest

from app import app, SCENARIOS


def test_every_option_has_a_mapping():
    for scenario in SCENARIOS.values():
        for point in scenario["decision_points"]:
            for option in point["options"]:
                assert option["id"] in scenario["mapping"][point["id"]]


def test_invalid_option_is_rejected():
    client = app.test_client()
    client.get("/scenario/sc01/start")
    response = client.post("/scenario/sc01/decision/1", data={"option_id": "zzz"})
    assert response.status_code == 400


def best_answers(scenario):
    """The first correct option at each decision, read from the mapping file."""
    return [
        next(opt for opt, entry in scenario["mapping"][point["id"]].items()
             if entry["rating"] == "correct")
        for point in scenario["decision_points"]
    ]


@pytest.mark.parametrize("scenario_id", sorted(SCENARIOS))
def test_full_walkthrough_reaches_summary_and_report(scenario_id):
    client = app.test_client()
    client.get(f"/scenario/{scenario_id}/start")
    for number, choice in enumerate(best_answers(SCENARIOS[scenario_id]), start=1):
        client.post(f"/scenario/{scenario_id}/decision/{number}", data={"option_id": choice})
    summary = client.get(f"/scenario/{scenario_id}/summary")
    assert summary.status_code == 200
    assert "6 of 6 points" in summary.get_data(as_text=True)
    report = client.get(f"/scenario/{scenario_id}/report")
    assert report.status_code == 200
    assert "Prepared" in report.get_data(as_text=True)


def test_library_lists_all_three_scenarios():
    page = app.test_client().get("/").get_data(as_text=True)
    for scenario in SCENARIOS.values():
        assert scenario["title"] in page
        