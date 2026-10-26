"""Runtime configuration read from environment variables.

See docs/environment.md for every variable, its default, and where it is set.
"""
import os

DEFAULT_DATABASE_URL = "sqlite:///autogsesec.db"
DEV_SECRET_KEY = "dev-only-change-before-deploying"


def is_production():
    """True on Render (which always sets RENDER=true) or when APP_ENV=production."""
    return os.environ.get("RENDER") == "true" or os.environ.get("APP_ENV") == "production"


def database_url():
    """Return the SQLAlchemy database URL.

    Local development falls back to a SQLite file. Hosting providers such as
    Render give Postgres URLs that start with "postgres://" or "postgresql://";
    SQLAlchemy needs "postgresql+psycopg://" to use the psycopg 3 driver.
    """
    url = os.environ.get("DATABASE_URL")
    if not url:
        if is_production():
            raise RuntimeError("DATABASE_URL must be set in production")
        url = DEFAULT_DATABASE_URL
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


def secret_key():
    """Return the key that signs session cookies and CSRF tokens.

    In production a real SECRET_KEY must be set; the app refuses to start
    with the development placeholder, so a missing setting cannot go unnoticed.
    """
    key = os.environ.get("SECRET_KEY")
    if key:
        return key
    if is_production():
        raise RuntimeError("SECRET_KEY must be set in production")
    return DEV_SECRET_KEY