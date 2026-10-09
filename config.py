"""Runtime configuration read from environment variables.

See docs/environment.md for every variable, its default, and where it is set.
"""
import os

DEFAULT_DATABASE_URL = "sqlite:///autogsesec.db"


def database_url():
    """Return the SQLAlchemy database URL.

    Local development falls back to a SQLite file. Hosting providers such as
    Render give Postgres URLs that start with "postgres://" or "postgresql://";
    SQLAlchemy needs "postgresql+psycopg://" to use the psycopg 3 driver.
    """
    url = os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url
