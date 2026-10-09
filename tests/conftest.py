"""Shared test setup: every test gets a fresh, empty database.

By default tests use an in-memory SQLite database. Set TEST_DATABASE_URL to run
the same tests against another database (GitHub Actions uses Postgres).
"""
import os

os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "sqlite://")

import pytest

from app import app
from models import db


@pytest.fixture(autouse=True)
def fresh_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield
    with app.app_context():
        db.session.remove()
