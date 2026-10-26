# autogsesec

![tests](https://github.com/ojanetor/autogsesec/actions/workflows/tests.yml/badge.svg)

Autonomous GSE Cybersecurity Tabletop Exercise Platform

A web-based security training platform for professionals responsible for securing autonomous ground service equipment operating on active airfields in U.S. aviation critical infrastructure.

---

## The Problem

Self-driving vehicles move cargo across active airfields at major U.S. airports today. A cyberattack on these systems does not produce a data breach — it produces a vehicle in motion near aircraft and people.

The frameworks that exist were built for IT networks and industrial control systems. Jiang et al. (2025) reviewed 417 publications on MITRE ATT&CK and confirmed documented gaps in cyber-physical and ICS coverage. Security teams working with autonomous airside systems have nothing purpose-built to train against.

AutoGSESec fills that gap.

---

## What It Does

| Component | Function |
|-----------|----------|
| **Scenario Library** | Interactive threat scenarios mapped to MITRE ATT&CK for ICS tactics |
| **Exercise Delivery Engine** | Decision prompts with session state management |
| **Scoring Engine** | Rule-based evaluation against NIST SP 800-82 controls |
| **After-Action Reports** | Gaps, recommended controls, and prioritized implementation timelines |

## Scenario Modules

1. **Initial Access (TA0108)** — insider threat and social engineering
2. **Command and Control (TA0101)** — GPS spoofing
3. **Impact (TA0105)** — physical consequence and response

---

## Project Status — v0.3.0 (Hard Stop 4)

**Live:** https://autogsesec.onrender.com

| Works now (tested) | Partial or not started |
|--------------------|------------------------|
| sc01 end to end: decisions, deterministic score, after-action report | sc02 and sc03 not yet written; sc01 mapping not yet audited |
| Responses stored in Render Postgres; data survives restarts | No schema migrations yet |
| CSRF protection; production refuses to start without its secret key or database | Before/after understanding rating not built |
| 52 automated tests on SQLite and Postgres 16; 7 of 7 known-answer cases match | Facilitator view and report export not built |
| Live site: 20 of 20 score pages under 3 seconds (warm) | Peer usability testing not yet run |

Known issues and risks: [docs/risk-issue-log.md](docs/risk-issue-log.md). Environment variables: [docs/environment.md](docs/environment.md). Release history: [CHANGELOG.md](CHANGELOG.md).

---

## Tech Stack

- **Backend:** Python 3.11 + Flask 3.1
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Content:** versioned JSON files in Git
- **Database:** SQLAlchemy 2.1 — SQLite for development, Postgres 16 validated in CI (psycopg 3)
- **Hosting:** Render.com free tier with Render Postgres (live)
- **Development:** GitHub Codespaces dev container; GitHub Actions for tests

---

## Setup

### Option A — GitHub Codespaces (recommended, nothing to install)

1. Click **Code → Codespaces → Create codespace on main**.
2. Wait for the build to finish. The dev container installs Python 3.11 and all dependencies automatically.
3. In the terminal:

```bash
   source .venv/bin/activate
   python app.py
```

4. Open the forwarded port 5000 when prompted.

### Option B — Local machine (Python 3.11 required)

```bash
git clone https://github.com/ojanetor/autogsesec.git
cd autogsesec
python3.11 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python app.py
```

Open `http://localhost:5000` in your browser. No environment variables are needed for local use; the app creates `instance/autogsesec.db` (SQLite) on first start.

### Run the tests

```bash
python -m pytest -v
```

Expected result: **52 passed**. To run the same tests against Postgres, set `TEST_DATABASE_URL` (see [docs/environment.md](docs/environment.md)).

### Inspect stored data

```bash
python scripts/inspect_db.py
```

Prints the sessions and responses saved in the local database.

---

## Repository Structure

```
autogsesec/
├── .devcontainer/devcontainer.json # reproducible Python 3.11 environment
├── .github/workflows/tests.yml # runs tests on every push to main and every pull request
├── app.py # Flask entry point and routes
├── config.py # reads DATABASE_URL and other settings
├── models.py # database tables: sessions, responses
├── engine/
│ ├── content.py # loads and validates scenarios and mappings
│ ├── scoring.py # deterministic scoring engine
│ └── report.py # after-action report generator
├── data/
│ ├── frameworks.json # valid ATT&CK and NIST IDs with versions
│ ├── scenarios/ # story content only
│ └── mappings/ # ratings, controls, timelines
├── templates/ # HTML pages
├── static/ # CSS
├── tests/ # functional, persistence, config and smoke tests
├── scripts/inspect_db.py # prints stored sessions and responses
├── docs/ # architecture, environment, conventions, risk and issue log, charter
├── journal/engineering-log.md # weekly engineering log
├── CHANGELOG.md
├── requirements.txt # runtime dependencies (pinned)
└── requirements-dev.txt # runtime plus test dependencies
```


## Documentation

- [Architecture](docs/architecture.md)
- [Environment notes](docs/environment.md) — variables, databases validated
- [Engineering conventions](docs/conventions.md) — naming, branches, tags, storage
- [Risk and issue log](docs/risk-issue-log.md)
- [Changelog](CHANGELOG.md)
- [Engineering log](journal/engineering-log.md)

---

## ⚠️ Disclaimer

AutoGSESec is an **educational and preparedness tool only**. It does not constitute a formal security assessment, compliance certification, or guarantee of protection. It should be used alongside qualified security professionals and regulatory compliance programs — never as a substitute for them.

All scenario content is derived from publicly available NIST and MITRE documentation. No proprietary operational data is used.

---

## Project Context

Applied project for CISC 699 — Applied Project in Computer Information Sciences
Harrisburg University of Science and Technology | Fall 2026

Extends thesis research completed in GRAD 695: *Securing the Airside — A Cybersecurity Risk and Threat-Modeling Framework for Autonomous Ground Service Equipment in U.S. Aviation Critical Infrastructure*

---

## License

MIT
