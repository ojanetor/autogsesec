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

## Project Status — v0.1.0 baseline

| Built | Planned |
|-------|---------|
| Scenario library, 3-step decision flow, session summary | Scoring engine and after-action report (Hard Stop 4) |
| Content loader with fail-closed validation | Database persistence (Sprint II) |
| sc01 GPS spoofing scenario (draft content) | sc02 and sc03 scenarios |
| 7 automated tests, run on every push | Public deployment on Render |

Known issues and risks: [docs/risk-issue-log.md](docs/risk-issue-log.md). Release history: [CHANGELOG.md](CHANGELOG.md).

---

## Tech Stack

- **Backend:** Python 3.11 + Flask 3.1
- **Frontend:** HTML, CSS, vanilla JavaScript
- **Content:** versioned JSON files in Git
- **Database:** SQLite via SQLAlchemy (planned)
- **Hosting:** Render.com free tier (planned)
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

Open `http://localhost:5000` in your browser.

### Run the tests

```bash
python -m pytest -v
```

Expected result: **7 passed**.

---

## Repository Structure

```
autogsesec/
├── .devcontainer/devcontainer.json   # reproducible Python 3.11 environment
├── .github/workflows/tests.yml       # runs tests on every push to main and every pull request
├── app.py                            # Flask entry point and routes
├── engine/
│   ├── content.py                    # loads and validates scenarios and mappings
│   ├── scoring.py                    # placeholder (Hard Stop 4)
│   └── report.py                     # placeholder (Hard Stop 4)
├── data/
│   ├── frameworks.json               # valid ATT&CK and NIST IDs with versions
│   ├── scenarios/                    # story content only
│   └── mappings/                     # ratings, controls, timelines
├── templates/                        # HTML pages
├── static/                           # CSS
├── tests/                            # functional and smoke tests
├── docs/                             # architecture, conventions, risk and issue log, charter
├── journal/engineering-log.md        # weekly engineering log
├── CHANGELOG.md
├── requirements.txt                  # runtime dependencies (pinned)
└── requirements-dev.txt              # runtime plus test dependencies
```

## Documentation

- [Architecture](docs/architecture.md)
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