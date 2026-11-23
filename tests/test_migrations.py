"""Migration tests: the migration scripts build exactly the schema in models.py.

Runs the same command the production start command runs, in a separate
process, against a brand-new database file.
"""
import os
import subprocess
import sys
from pathlib import Path

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, inspect

from models import db

ROOT = Path(__file__).resolve().parent.parent


def run_flask_db(command, url):
    env = {**os.environ, "APP_ENV": "production", "SECRET_KEY": "test-only", "DATABASE_URL": url}
    env.pop("RENDER", None)
    return subprocess.run([sys.executable, "-m", "flask", "--app", "app", "db", command],
                          cwd=ROOT, env=env, capture_output=True, text=True)


def test_migrations_build_the_same_schema_as_the_models(tmp_path):
    url = f"sqlite:///{tmp_path / 'migrated.db'}"
    result = run_flask_db("upgrade", url)
    assert result.returncode == 0, result.stderr

    engine = create_engine(url)
    with engine.connect() as connection:
        differences = compare_metadata(MigrationContext.configure(connection), db.metadata)
        tables = set(inspect(connection).get_table_names())
    engine.dispose()
    assert differences == []
    assert {"sessions", "responses", "alembic_version"} <= tables


def test_running_the_upgrade_twice_is_safe(tmp_path):
    """Render runs the upgrade on every start; a second run must change nothing."""
    url = f"sqlite:///{tmp_path / 'migrated.db'}"
    assert run_flask_db("upgrade", url).returncode == 0
    second = run_flask_db("upgrade", url)
    assert second.returncode == 0, second.stderr
    