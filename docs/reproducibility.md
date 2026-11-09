# Reproducibility Pass and Friction Log: AutoGSESec

**Question:** could another graduate student set up, run, test, and reproduce the evidence for AutoGSESec using only the README?

**Method:** follow the README from a brand-new environment, word for word, without using knowledge that is not written down. Record every command, its result, and every point of friction. Fix the documentation or code, then repeat until the pass is clean.

## Clean-environment runs

| Run | Date (UTC) | Environment | Commit / tag | Steps followed | Result | Record |
|---|---|---|---|---|---|---|
| 1. Pre-check | 2026-11-09 | Fresh `git clone` into an empty folder, new virtual environment, Python 3.11.18, Linux (run by the AI assistant in its own sandbox; see AI usage log) | HS5 working branch | README Option B: venv, `pip install -r requirements-dev.txt`, `python -m pytest -q`, `python app.py`, `/health` | 89 passed; `/health` ok with 3 scenarios | This table |
| 2. Clean Codespace (student) | 2026-11-09 | New GitHub Codespace created from `main`, never used before; Python 3.11.18 | `beccefc` (main after the Hard Stop 5 merge) | README Quick start and Setup Option A: activate `.venv`, `python app.py` (library loaded), `python -m pytest -q`, then "Reproduce the evidence": `collect_evidence.py` and the live benchmark | 89 passed in 0.62 s; 21 of 21 known-answer cases match; live benchmark 20 of 20 score pages under 3 s (median 0.177 s); no undocumented steps | `evidence/runs/v0.5.0-clean-codespace/`, `evidence/benchmarks/render-warm-20261109T222224Z/` |

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
| F14 | Server log shows `GET /favicon.ico 404` on the first page load | Clean Codespace run | Harmless, but looks like an error to a new user reading the log | Recorded; no site icon is defined. Cosmetic, left open | Server log |
| F15 | First live request took 32.2 s (benchmark warm-up) | Clean Codespace run | A new user may think the live site is down | No change needed: already explained in README (Live site, Troubleshooting) and the runbook; third cold-start measurement, consistent with 32.4 s at v0.3.0 | README, runbook |

## Conclusion

Following only the README, a brand-new Codespace reached 89 passing tests, 21 of 21 matching known-answer cases, and a complete evidence record on its first attempt, and the live site met the 3-second requirement on 20 of 20 runs. No step depended on knowledge outside the documentation. The two friction points found (a cosmetic favicon 404 and the documented cold start) did not block setup. Thirteen earlier friction points (F1–F13) were fixed before this run.
