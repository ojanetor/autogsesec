"""Security configuration tests (T10 basics): CSRF, secret key, cookies."""
import re

import pytest

import config
from app import app


@pytest.fixture
def csrf_on():
    app.config["WTF_CSRF_ENABLED"] = True
    yield
    app.config["WTF_CSRF_ENABLED"] = False


def test_form_post_without_csrf_token_is_rejected(csrf_on):
    client = app.test_client()
    client.get("/scenario/sc01/start")
    response = client.post("/scenario/sc01/decision/1", data={"option_id": "d"})
    assert response.status_code == 400


def test_form_post_with_csrf_token_is_accepted(csrf_on):
    client = app.test_client()
    page = client.get("/scenario/sc01/start", follow_redirects=True).get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', page).group(1)
    response = client.post(
        "/scenario/sc01/decision/1", data={"option_id": "d", "csrf_token": token}
    )
    assert response.status_code == 302


def test_production_refuses_to_start_without_secret_key(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("RENDER", "true")
    with pytest.raises(RuntimeError):
        config.secret_key()


def test_development_uses_placeholder_key(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("RENDER", raising=False)
    monkeypatch.delenv("APP_ENV", raising=False)
    assert config.secret_key() == config.DEV_SECRET_KEY


def test_session_cookie_is_http_only_and_same_site():
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"