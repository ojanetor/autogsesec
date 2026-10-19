# Environment Notes — AutoGSESec

## Runtime

| Item | Value |
|------|-------|
| Python | 3.11 (`.python-version`; dev container `mcr.microsoft.com/devcontainers/python:3.11`) |
| Web framework | Flask 3.1.3, Flask-WTF 1.3.0 (CSRF protection) |
| Database layer | SQLAlchemy 2.1.4 via Flask-SQLAlchemy 3.1.1 |
| Postgres driver | psycopg 3.3.6 (binary build) |
| Production server | gunicorn 26.2.0 |
| Dependencies | `requirements.txt` (runtime), `requirements-dev.txt` (runtime + tests), all pinned |

`.python-version` holds the minor version only (`3.11`). Render and GitHub Actions read it and install the newest 3.11 patch; the Codespace image may run an older patch. The exact patch used for every evidence run is recorded in that run's `manifest.json` (issue I-14).

## Environment Variables

| Variable | Used by | Default if unset | Where it is set |
|----------|---------|------------------|-----------------|
| `DATABASE_URL` | `config.py` | `sqlite:///autogsesec.db` (file in `instance/`, not committed) | Render dashboard: the Postgres **Internal Database URL** |
| `SECRET_KEY` | `config.py` | Development placeholder. **In production the app refuses to start without it.** | Render dashboard (use "Generate") |
| `RENDER` | `config.py` | Unset | Set to `true` automatically by Render; switches on production rules |
| `APP_ENV` | `config.py` | Unset | Optional: `production` turns on production rules outside Render |
| `PORT` | gunicorn | 8000 | Set automatically by Render |
| `TEST_DATABASE_URL` | `tests/conftest.py` | `sqlite://` (in-memory) | GitHub Actions Postgres job |
| `PGTZ` | psycopg / libpq | Database server's time zone | GitHub Actions Postgres job (`America/New_York`) |

`config.py` converts `postgres://` and `postgresql://` URLs (the form Render provides) to `postgresql+psycopg://`, which SQLAlchemy needs to use the psycopg 3 driver.

## Production Rules (when `RENDER=true` or `APP_ENV=production`)

- `SECRET_KEY` must be set, or the app stops at startup.
- Session cookies are marked `Secure` (HTTPS only), `HttpOnly`, and `SameSite=Lax`.
- Every form post must carry a CSRF token (Flask-WTF); requests without one get HTTP 400.
- The Flask debugger is never used; gunicorn serves the app.

## Render Settings

| Setting | Value |
|---------|-------|
| Service type | Web Service, Free instance |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app --workers 1` |
| Health check path | `/health` |
| Database | Render Postgres, Free (expires 30 days after creation) |

One worker is used on purpose: tables are created at startup with `db.create_all()`, and two workers starting together could race to create them (issue I-16). Migrations (planned for Hard Stop 5) remove this limit.

## Databases Validated

| Database | Where | Evidence |
|----------|-------|----------|
| SQLite (file) | Codespaces, local runs | `/health` reports `database_engine: sqlite`; `scripts/inspect_db.py` |
| SQLite (in-memory) | Every test run | GitHub Actions `test-sqlite` job |
| Postgres 16 | GitHub Actions service container | GitHub Actions `test-postgres` job, all tests |
| Render Postgres | Deployed service | `evidence/benchmarks/` (from v0.3.0) |

## Time Zones

All timestamps are created in UTC (`models.utc_now`) and stored in time-zone-aware columns (`timestamp with time zone` on Postgres). See issue I-09 in `docs/risk-issue-log.md`.