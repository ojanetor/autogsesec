"""Tests for environment-variable configuration (T4)."""
from app import app
import config


def test_default_is_local_sqlite(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert config.database_url() == "sqlite:///autogsesec.db"


def test_render_style_postgres_url_is_converted(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pw@host:5432/db")
    assert config.database_url() == "postgresql+psycopg://user:pw@host:5432/db"


def test_postgresql_url_is_converted(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pw@host/db")
    assert config.database_url() == "postgresql+psycopg://user:pw@host/db"


def test_health_reports_database_engine():
    data = app.test_client().get("/health").get_json()
    assert data["database"] == "ok"
    assert data["database_engine"] in {"sqlite", "postgresql"}
