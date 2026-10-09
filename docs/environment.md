# Environment Notes — AutoGSESec

## Runtime

| Item | Value |
|------|-------|
| Python | 3.11 (dev container `mcr.microsoft.com/devcontainers/python:3.11`) |
| Web framework | Flask 3.1.3 |
| Database layer | SQLAlchemy 2.1.4 via Flask-SQLAlchemy 3.1.1 |
| Postgres driver | psycopg 3.3.6 (binary build) |
| Dependencies | `requirements.txt` (runtime), `requirements-dev.txt` (runtime + tests), all pinned |

## Environment Variables

| Variable | Used by | Default if unset | Where it is set |
|----------|---------|------------------|-----------------|
| `DATABASE_URL` | `config.py` | `sqlite:///autogsesec.db` (file in `instance/`, not committed) | Render dashboard (production) |
| `SECRET_KEY` | `app.py` | Development-only placeholder | Render dashboard (production). Must be set before deployment (issue I-05). |
| `TEST_DATABASE_URL` | `tests/conftest.py` | `sqlite://` (in-memory) | GitHub Actions Postgres job |
| `PGTZ` | psycopg / libpq | Database server's time zone | GitHub Actions Postgres job (`America/New_York`) |

`config.py` converts `postgres://` and `postgresql://` URLs (the form Render provides) to `postgresql+psycopg://`, which SQLAlchemy needs to use the psycopg 3 driver.

## Databases Validated

| Database | Where | Evidence |
|----------|-------|----------|
| SQLite (file) | Codespaces, local runs | `/health` reports `database_engine: sqlite`; `scripts/inspect_db.py` |
| SQLite (in-memory) | Every test run | GitHub Actions `test-sqlite` job |
| Postgres 16 | GitHub Actions service container | GitHub Actions `test-postgres` job, all tests |

## Time Zones

All timestamps are created in UTC (`models.utc_now`) and stored in time-zone-aware columns (`timestamp with time zone` on Postgres). See issue I-09 in `docs/risk-issue-log.md`.

## Not Yet Validated

- Render Postgres itself (planned for the Week 8 deployment, task T11)
- Schema migrations (none yet; `db.create_all()` only creates missing tables — issue I-10)
