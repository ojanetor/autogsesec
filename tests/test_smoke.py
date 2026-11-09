"""Smoke tests: prove the baseline starts and its core paths respond."""
from app import app, SCENARIOS


def test_app_starts_and_loads_all_three_scenarios():
    assert sorted(SCENARIOS) == ["sc01", "sc02", "sc03"]


def test_each_module_name_matches_its_attack_tactic():
    """A scenario's module label must be the name of the ATT&CK for ICS tactic it maps to."""
    import json
    from engine.content import DATA_DIR
    tactics = json.loads((DATA_DIR / "frameworks.json").read_text())["attack_ics"]["tactics"]
    for scenario in SCENARIOS.values():
        assert scenario["module"] == tactics[scenario["attack_tactic"]]


def test_health_endpoint_reports_ok():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_home_page_shows_disclaimer():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert b"Training tool only" in response.data


def test_planned_modules_are_importable():
    from engine import report, scoring
    assert callable(scoring.score_session)
    assert callable(report.build_report)

def test_content_file_names_follow_the_naming_convention():
    """docs/conventions.md: <id>_<short_name>.json, same name in both folders, no spaces."""
    import re
    from engine.content import DATA_DIR
    scenario_files = sorted(p.name for p in (DATA_DIR / "scenarios").glob("*.json"))
    mapping_files = sorted(p.name for p in (DATA_DIR / "mappings").glob("*.json"))
    assert scenario_files == mapping_files
    for name in scenario_files:
        assert re.fullmatch(r"sc\d{2}_[a-z0-9_]+\.json", name), name

def test_unknown_page_shows_friendly_404():
    response = app.test_client().get("/scenario/zz99/start")
    assert response.status_code == 404
    assert "Page not found" in response.get_data(as_text=True)


def test_unexpected_error_shows_friendly_500(monkeypatch):
    import app as app_module

    def broken(*args, **kwargs):
        raise RuntimeError("simulated failure")

    monkeypatch.setattr(app_module, "current_exercise", broken)
    response = app.test_client().get("/scenario/sc01/summary")
    assert response.status_code == 500
    assert "Something went wrong" in response.get_data(as_text=True)        