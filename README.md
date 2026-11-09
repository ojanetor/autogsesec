# AutoGSESec

![tests](https://github.com/ojanetor/autogsesec/actions/workflows/tests.yml/badge.svg)

**A cybersecurity tabletop exercise platform for teams that operate autonomous ground service equipment (GSE) on airfields.**

A participant works through a short incident scenario, makes three decisions, and gets a deterministic score, a readiness rating, and an after-action report that recommends NIST SP 800-82 Rev. 3 controls by implementation timeline.

**Live site:** https://autogsesec.onrender.com (free hosting: the first page can take about 30 seconds after the site has been idle)

> **Training tool only.** AutoGSESec supports discussion and practice. It is not a security assessment, certification, or operational guidance.

---

## Contents

1. [What it does](#what-it-does)
2. [Quick start (5 minutes)](#quick-start-5-minutes)
3. [Prerequisites](#prerequisites)
4. [Setup](#setup)
5. [Run the app](#run-the-app)
6. [Run the tests and expected output](#run-the-tests-and-expected-output)
7. [Reproduce the evidence](#reproduce-the-evidence)
8. [Configuration and secrets](#configuration-and-secrets)
9. [Data: where it comes from and what can be shared](#data-where-it-comes-from-and-what-can-be-shared)
10. [Troubleshooting](#troubleshooting)
11. [Repository layout](#repository-layout)
12. [Project status and known limitations](#project-status-and-known-limitations)
13. [Documentation](#documentation)

---

## What it does

| Scenario | ATT&CK for ICS tactic | Situation |
|---|---|---|
| Drifting Positions: GPS Spoofing on the Ramp (`sc01`) | Command and Control (TA0101) | Vehicles report positions that do not match where they are |
| The Helpful Caller: Social Engineering at the Fleet Console (`sc02`) | Initial Access (TA0108) | A fake vendor call and a former contractor's account that was never closed |
| Dark Screens: Loss of View Across the Fleet (`sc03`) | Impact (TA0105) | Fleet monitoring freezes while tractors keep moving near aircraft |

**How scoring works:** each answer is rated correct (2 points), partial (1), or incorrect (0) against a rubric in `data/mappings/`. Readiness is **Prepared** at 80% or more, **Developing** at 50% or more, **Unprepared** below 50%. Every non-correct answer names the NIST controls to strengthen and a timeline: Immediate (within 30 days), Short-term (30–90 days), or Long-term (over 90 days). Scoring is rule-based with no randomness: the same answers always give the same report.

---

## Quick start (5 minutes)

In a GitHub Codespace (nothing to install):

```bash
source .venv/bin/activate
python -m pytest -q          # expect: 89 passed
python app.py                # then open the forwarded port 5000
```

---

## Prerequisites

| Need | Version | Notes |
|---|---|---|
| Python | **3.11** (`.python-version`) | CI and Render use the newest 3.11 patch; evidence recorded on 3.11.16 and 3.11.17 |
| pip | any recent | comes with Python |
| Git | any recent | to clone the repository |
| Browser | any modern browser | cookies must be enabled (the exercise uses a session cookie) |
| Hardware | any laptop or a 2-core Codespace | no GPU or special hardware |
| Network | only for installing packages | the app calls no external services at runtime |

No paid service, API key, or account is needed to run locally.

---

## Setup

### Option A: GitHub Codespaces (recommended)

1. On the repository page, click **Code → Codespaces → Create codespace on main**.
2. Wait for the build to finish. The dev container (`.devcontainer/devcontainer.json`) installs Python 3.11, creates `.venv`, and installs `requirements-dev.txt`.
3. In the terminal: `source .venv/bin/activate`

### Option B: Your own machine

```bash
git clone https://github.com/ojanetor/autogsesec.git
cd autogsesec
python3.11 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

To reproduce a specific release exactly, check out its tag before installing, for example `git checkout v0.5.0`.

All dependencies are pinned to exact versions in `requirements.txt` (runtime) and `requirements-dev.txt` (runtime plus pytest).

---

## Run the app

```bash
python app.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: off
 * Running on http://127.0.0.1:5000
```

Open http://127.0.0.1:5000 (in Codespaces, open the forwarded port 5000). You should see the scenario library with three scenarios and the training-tool banner.

- On first start the app creates a local SQLite database at `instance/autogsesec.db` (not committed).
- Check the app is healthy: http://127.0.0.1:5000/health returns `"status": "ok"`, `"scenarios_loaded": 3`.
- See what was stored: `python scripts/inspect_db.py` (local SQLite only).
- The Flask debugger is off. Turn it on only on your own machine with `FLASK_DEBUG=1 python app.py`.

Production uses gunicorn instead: `gunicorn app:app --workers 1` (see [docs/runbook.md](docs/runbook.md)).

---

## Run the tests and expected output

```bash
python -m pytest -q
```

**Expected:** `89 passed` in about 1–3 seconds. The tests cover:

- **scoring correctness:** 21 hand-computed known-answer cases, 7 per scenario;
- **every possible answer path:** 192 (64 per scenario);
- **determinism:** 10 identical runs per scenario;
- **report content**;
- **security:** CSRF, production startup checks, cookies;
- **persistence, error pages, the content naming rules, and the session clean-up tool.**

To run the same tests against Postgres, set `TEST_DATABASE_URL` (see [docs/environment.md](docs/environment.md)). GitHub Actions runs every test on SQLite and on Postgres 16 for every pull request.

---

## Reproduce the evidence

Every claim in the project reports maps to a file in `evidence/`, listed in [docs/evidence-index.md](docs/evidence-index.md). To regenerate it:

| What | Command | Output | Expected |
|---|---|---|---|
| Tests, known answers, score distributions, environment manifest | `python scripts/collect_evidence.py --label my-run` | `evidence/runs/my-run/` | `tests.txt` shows 89 passed; `known_answers.md` shows 21 of 21 match |
| Score distribution for all 192 answer paths | `python scripts/score_distribution.py` | printed | Prepared on 6.2%, 7.8%, 6.2% of paths for sc01, sc02, sc03 |
| Response time, local | Start `python app.py`, then in a second terminal: `python scripts/benchmark.py --base-url http://127.0.0.1:5000 --runs 20 --label local` | `evidence/benchmarks/local-<UTC time>/` | 20 of 20 score pages under 3 s |
| Response time, live | `python scripts/benchmark.py --base-url https://autogsesec.onrender.com --runs 20 --label render-warm` | `evidence/benchmarks/render-warm-<UTC time>/` | 20 of 20 under 3 s once warm |
| Another scenario | add `--scenario sc02 --answers c,a,c` | same | — |

**Nothing is random**, so there are no seeds to set. The same commit, Python minor version, and pinned packages give the same scores and reports. Each evidence run records the exact commit, Python version, and package list in its `manifest.json`.

Benchmarks against the live site add sessions to its database. Clear them afterwards with `scripts/purge_sessions.py` (see the runbook).

---

## Configuration and secrets

**Local use needs no configuration.** Production settings come from environment variables only; nothing secret is stored in the repository. [`.env.example`](.env.example) lists every variable.

| Variable | Needed for | If unset |
|---|---|---|
| `SECRET_KEY` | production | **app refuses to start in production**; local uses a development placeholder |
| `DATABASE_URL` | production | **app refuses to start in production**; local uses SQLite in `instance/` |
| `RENDER` / `APP_ENV=production` | turning on production rules | development rules |
| `FLASK_DEBUG=1` | local debugging only | debugger off |
| `TEST_DATABASE_URL` | running tests on Postgres | tests use in-memory SQLite |

**External services:**
- **Render** hosts the live app and its Postgres database. Secrets are set in the Render dashboard, never in code.
- **GitHub Actions** runs the tests.

The app calls **no external APIs**, so there are no keys, quotas, rate limits, or per-call costs. Full details: [docs/environment.md](docs/environment.md).

---

## Data: where it comes from and what can be shared

| Data | Source | Can it be redistributed? |
|---|---|---|
| Scenario stories (`data/scenarios/`) | Written by the author from public MITRE ATT&CK for ICS and NIST guidance; conceptual only, with no attack instructions | Yes, under this repository's MIT license |
| Rubric mappings (`data/mappings/`) | Author's ratings and rationales, citing NIST SP 800-53 Rev. 5 control IDs as overlaid by NIST SP 800-82 Rev. 3 | Yes, MIT. **Status: draft, independent audit in progress** |
| Framework catalog (`data/frameworks.json`) | Tactic IDs and names from MITRE ATT&CK for ICS v19.2; control IDs and names from NIST SP 800-53 Rev. 5 | IDs and names only. NIST publications are U.S. Government works; ATT&CK is © The MITRE Corporation and used under its terms of use, which require attribution |
| Runtime data (database) | Created when people use the app: a random session id, scenario id, answer choices, timestamps | **No personal data is collected.** The production database is not distributed |
| Evidence (`evidence/`) | Generated by the scripts above | Yes |

**Not included, and must never be added:** proprietary or operational data from any GSE operator or vendor (including the author's employer), credentials, or exploitation details. No data preparation step is needed; the JSON files are loaded and checked at startup.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `RuntimeError: SECRET_KEY must be set in production` or `DATABASE_URL must be set in production` | `RENDER` or `APP_ENV=production` is set, which turns on production rules | Locally: `unset RENDER APP_ENV`. On Render: set both variables in the dashboard |
| App stops at startup with `ValueError` naming a scenario, option, or control | A content file is incomplete, or cites a control or tactic missing from `data/frameworks.json` | Fix the file named in the message; the startup check refuses incomplete rubrics on purpose |
| `ModuleNotFoundError: No module named 'flask'` | Virtual environment not active | `source .venv/bin/activate` |
| `python3.11: command not found` | Python 3.11 not installed | Install 3.11, or use a Codespace |
| Address already in use (port 5000) | Another app is using the port | Stop it, or run `flask --app app run --port 5001` |
| Live site takes ~30 seconds to load | Free hosting sleeps after ~15 minutes idle | Wait once; open the site a minute before a demo or session |
| "This form has expired" | The form's security token was missing or expired (cookies blocked, or a very old page) | Enable cookies and start the scenario again |
| A script gets HTTP 400 from the live site | HTTPS form check needs a `Referer` header and a CSRF token | Use `scripts/benchmark.py`, which sends both |
| Tests fail only on Postgres | Database differences (time zones, types) | Run with `TEST_DATABASE_URL`; check `docs/environment.md` |
| `/health` shows `"database_engine": "sqlite"` on Render | `DATABASE_URL` is not set on Render | Set the Internal Database URL in the Render dashboard |

Still stuck? Open an issue with the command you ran and its full output.

---

## Repository layout

```
autogsesec/
├── app.py                      # Flask routes, error pages, startup
├── config.py                   # environment variables and production rules
├── models.py                   # database tables: sessions, responses (no personal data)
├── maintenance.py              # find and remove abandoned sessions or test data
├── engine/
│   ├── content.py              # loads and validates scenarios and rubrics at startup
│   ├── scoring.py              # deterministic scoring and readiness rating
│   └── report.py               # after-action report and control recommendations
├── data/
│   ├── frameworks.json         # allowed ATT&CK tactics and NIST controls, with versions
│   ├── scenarios/              # scenario stories (sc01, sc02, sc03)
│   └── mappings/               # rubric: rating, controls, timeline, rationale per option
├── templates/, static/         # pages and styles
├── tests/                      # 89 tests; tests/data/ holds the hand-computed known answers
├── scripts/
│   ├── collect_evidence.py     # dated evidence record for the current commit
│   ├── benchmark.py            # response-time benchmark (any scenario)
│   ├── score_distribution.py   # score spread across every answer path
│   ├── purge_sessions.py       # clear abandoned sessions or test data (dry run by default)
│   └── inspect_db.py           # print the local SQLite data
├── evidence/                   # versioned evidence: runs/ and benchmarks/
├── docs/                       # runbook, reproducibility, architecture, environment, evidence index, logs
├── journal/engineering-log.md  # weekly engineering log
├── .devcontainer/              # Codespaces environment (Python 3.11)
├── .github/workflows/tests.yml # CI: all tests on SQLite and Postgres 16
├── .env.example                # every environment variable, with safe placeholders
├── .python-version             # 3.11
├── requirements.txt            # runtime dependencies, pinned
├── requirements-dev.txt        # runtime plus test dependencies, pinned
└── CHANGELOG.md
```

---

## Project status and known limitations

**v0.5.0 (Hard Stop 5).**

**Done:**
- three scenarios end to end, with deterministic scoring and after-action reports;
- 89 tests on SQLite and Postgres;
- live deployment on Render Postgres;
- clean-environment reproducibility pass ([docs/reproducibility.md](docs/reproducibility.md)).

**Not yet:**
- the rubric mapping audit is in progress, so the mappings are drafts;
- peer usability testing;
- the before-and-after understanding rating, facilitator view, and report download;
- schema migrations.

**Known limitations:**
- the live first page takes about 30 seconds after idle;
- the free database expires about 30 days after creation;
- benchmarks were run with one user at a time.

Full list: [docs/risk-issue-log.md](docs/risk-issue-log.md).

---

## Documentation

- [Runbook](docs/runbook.md): deploy, configure, warm up, clean data, release
- [Reproducibility pass and friction log](docs/reproducibility.md)
- [Architecture](docs/architecture.md)
- [Environment and configuration](docs/environment.md)
- [Evidence index](docs/evidence-index.md)
- [Risk and issue log](docs/risk-issue-log.md)
- [Engineering conventions](docs/conventions.md)
- [AI usage log](docs/ai-usage-log.md)
- [Changelog](CHANGELOG.md) · [Engineering log](journal/engineering-log.md)

---

## Project context

Applied project for CISC 699, Applied Project in Computer Information Sciences, Harrisburg University of Science and Technology, Fall 2026. Extends the GRAD 695 thesis *Securing the Airside: A Cybersecurity Risk and Threat-Modeling Framework for Autonomous Ground Service Equipment in U.S. Aviation Critical Infrastructure*.

## License

MIT. See [LICENSE](LICENSE).