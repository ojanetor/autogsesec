# Changelog

All notable changes to AutoGSESec are recorded here.
Format based on Keep a Changelog; versions follow `vMAJOR.MINOR.PATCH` (see docs/conventions.md).

## [Unreleased]

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