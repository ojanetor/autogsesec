"""Smoke tests: prove the baseline starts and its core paths respond."""
from app import app, SCENARIOS


def test_app_starts_and_loads_content():
    assert len(SCENARIOS) >= 1


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