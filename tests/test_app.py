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


def test_full_walkthrough_reaches_summary():
    client = app.test_client()
    client.get("/scenario/sc01/start")
    for number, choice in [(1, "d"), (2, "b"), (3, "b")]:
        client.post(f"/scenario/sc01/decision/{number}", data={"option_id": choice})
    response = client.get("/scenario/sc01/summary")
    assert response.status_code == 200