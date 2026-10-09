"""Shared test setup: every test gets a fresh, empty in-memory database."""
import os

os.environ["DATABASE_URL"] = "sqlite://"

import pytest

from app import app
from models import db


@pytest.fixture(autouse=True)
def fresh_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield