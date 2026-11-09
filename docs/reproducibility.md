# Reproducibility Pass and Friction Log: AutoGSESec

**Question:** could another graduate student set up, run, test, and reproduce the evidence for AutoGSESec using only the README?

**Method:** follow the README from a brand-new environment, word for word, without using knowledge that is not written down. Record every command, its result, and every point of friction. Fix the documentation or code, then repeat until the pass is clean.

## Clean-environment runs

| Run | Date (UTC) | Environment | Commit / tag | Steps followed | Result | Record |
|---|---|---|---|---|---|---|
| 1. Pre-check | 2026-11-09 | Fresh `git clone` into an empty folder, new virtual environment, Python 3.11.18, Linux (run by the AI assistant in its own sandbox; see AI usage log) | HS5 working branch | README Option B: venv, `pip install -r requirements-dev.txt`, `python -m pytest -q`, `python app.py`, `/health` | 89 passed; `/health` ok with 3 scenarios | This table |
| 2. Clean Codespace (student) | [fill] | **New** GitHub Codespace created from `main`, never used before; Python [fill from manifest] | [fill: commit] | README Quick start and Setup Option A, then "Reproduce the evidence" | [fill: tests passed, known answers matched] | `evidence/runs/v0.5.0-clean-codespace/` |

## Friction log

| # | Friction point | Found by | Impact on a new user | Fix | Where |
|---|---|---|---|---|---|
| F1 | README said "52 passed"; the suite now has 89 tests | Repository audit | User thinks their run is wrong | Expected counts updated; README lists what the tests cover | README |
| F2 | README status said sc02 and sc03 were not written | Repository audit | Out-of-date picture of the artifact | Status section rewritten for v0.5.0 | README |
| F3 | `python app.py` started Flask's interactive debugger | Repository audit | Debugger can run code if exposed; unsafe default | Debugger off unless `FLASK_DEBUG=1`; test added | `app.py`, `tests/test_security.py` |
| F4 | No template listing environment variables | Repository audit | User must read `config.py` to find settings | `.env.example` with safe placeholders | `.env.example` |
| F5 | Benchmark could only run sc01 | Repository audit | Two scenarios could not be timed | `--scenario` and `--answers` options | `scripts/benchmark.py` |
| F6 | README had no expected outputs or troubleshooting | Repository audit | User cannot tell success from failure | "Expected output" for each step; troubleshooting table | README |
| F7 | README did not say where the data comes from or what may be shared | Repository audit | Licensing and confidentiality unclear | Data provenance and redistribution section | README |
| F8 | Four content files saved with " copy" in their names; every test still passed | Repository review, v0.4.0 | Files no longer match documented names | Renamed; naming test | `tests/test_smoke.py` |
| F9 | No way to clear abandoned sessions or benchmark data | Issue log (I-12, I-17) | Test data would mix with peer-testing data | `scripts/purge_sessions.py` (dry run by default); 8 tests | `maintenance.py`, `tests/test_maintenance.py` |
| F10 | Unknown pages and expired forms showed Flask's bare default pages | Repository audit | Confusing dead end for participants | Friendly 404, expired-form (CSRF), and 500 pages with a way back | `app.py`, `templates/error.html` |
| F11 | Evidence index described v0.3.0 only | Repository audit | Reviewer cannot find current evidence | Index rewritten for v0.5.0 | `docs/evidence-index.md` |
| F12 | `python3.11` is not installed on many machines | Pre-check | Option B fails at the first command | Troubleshooting row; Codespaces recommended | README |
| F13 | `scripts/inspect_db.py` reads local SQLite only | Pre-check | Confusing on Postgres | Documented in README | README |
| F14 | [fill: anything that slowed you down in run 2, or "None found"] | Clean Codespace run | | | |

## Conclusion

[fill after run 2: e.g. "Following only the README, a new Codespace reached 89 passing tests and 21 of 21 matching known-answer cases in about N minutes, with no undocumented steps."]
