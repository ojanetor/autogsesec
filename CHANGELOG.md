# Changelog

All notable changes to AutoGSESec are recorded here.
Format based on Keep a Changelog; versions follow `vMAJOR.MINOR.PATCH` (see docs/conventions.md).

## [Unreleased]

## [0.3.0] - 2026-10-25

Hard Stop 4 technical evidence release.

### Added
- Scoring engine: correct = 2, partial = 1, incorrect = 0; readiness bands Prepared (80%+), Developing (50–79%), Unprepared (below 50%); gaps ordered by timeline
- After-action report page: readiness rating, decision review with rationale, recommended NIST controls grouped by implementation timeline
- Error page when a session cannot be scored; saved responses are kept
- CSRF protection on all forms; secure, HttpOnly, SameSite session cookies in production
- Production refuses to start without `SECRET_KEY` or `DATABASE_URL`
- Render deployment (gunicorn, one worker) with Render Postgres
- Seven hand-computed known-answer cases; tests for the report, security, and configuration (52 tests)
- `scripts/benchmark.py` and `scripts/collect_evidence.py`; dated evidence in `evidence/`
- `docs/ai-usage-log.md` running AI usage log

### Fixed
- Render ran on a temporary SQLite file because `DATABASE_URL` was not set; the app now refuses to start without it in production
- The benchmark script did not send a Referer header, so the HTTPS CSRF check rejected it; real browsers were never affected

### Known issues
See docs/risk-issue-log.md.

## [0.2.0] - 2026-10-11

Hard Stop 3 early validation release.

### Added
- Database persistence for exercise sessions and responses (SQLAlchemy 2.1, Flask-SQLAlchemy 3.1) — task T3
- `config.py`: reads `DATABASE_URL`; converts Render-style Postgres URLs for the psycopg 3 driver — task T4
- Postgres 16 test job in GitHub Actions alongside SQLite; both run every test on every pull request
- `/health` now reports database status, database engine, and SQLAlchemy version
- `scripts/inspect_db.py` to print stored sessions and responses
- `docs/environment.md`: environment variables, databases validated, known gaps
- Tests: persistence (6), configuration (4); 17 tests in total

### Changed
- Session cookie now holds only a random session ID; answers live in the database
- Re-submitting a decision replaces the earlier answer (one answer per decision, enforced by a database constraint)

### Fixed
- Timestamps were stored without a time zone and shifted by the server's offset on Postgres (I-09)

### Known issues
See docs/risk-issue-log.md (I-01, I-03, I-04, I-05, I-10 to I-14).

## [0.1.0] - 2026-10-03

Implementation Sprint I baseline.

### Added
- Dev container (Python 3.11) that builds the virtual environment automatically
- Flask application: scenario library, three-step decision flow, session summary, `/health`
- Content loader with fail-closed validation (`engine/content.py`)
- sc01 GPS spoofing scenario and mapping (draft, pending NFR-07 audit)
- Placeholder interfaces for the scoring engine and after-action report (`engine/scoring.py`, `engine/report.py`)
- Tests: 3 functional and 4 smoke tests; GitHub Actions runs them on every push to main and every pull request
- Documentation: architecture, engineering conventions, risk and issue log, changelog

### Changed
- Scenario content and rubrics stored as versioned JSON instead of database tables (Hard Stop 2, decision D2)
- Third scenario module corrected to Impact (TA0105)
- Dependencies split into runtime (`requirements.txt`) and development (`requirements-dev.txt`)
- README setup instructions rewritten for Codespaces and local installs

### Known issues
See docs/risk-issue-log.md.
