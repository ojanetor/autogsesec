# Evidence Index — AutoGSESec v0.5.0

Every claim in the project reports maps to a file in `evidence/`. Times are UTC. Each run folder has a `manifest.json` with the exact commit, Python version, and package list.

## Current release (v0.5.0, Hard Stop 5)

| Criterion | Threshold | Evidence | Result |
|---|---|---|---|
| Clean-environment reproducibility: README followed from a brand-new Codespace | All tests pass; known answers match; no undocumented steps | `evidence/runs/v0.5.0-clean-codespace/`; `docs/reproducibility.md` | PASS (Python 3.11.18, commit `beccefc`) |
| Scores and reports match hand-computed answers, all three scenarios (FR-04, FR-07, FR-08) | 21 of 21 | `evidence/runs/v0.5.0-clean-codespace/known_answers.md` | PASS (21 of 21) |
| Every answer path scores consistently (FR-04) | 192 of 192 (64 per scenario) | `evidence/runs/v0.5.0-clean-codespace/tests.txt` | PASS |
| Same input gives identical score and report (NFR-06) | 10 of 10, each scenario | same `tests.txt` | PASS |
| Hardening: friendly error pages, debugger off by default, session clean-up, file-naming check | Tests pass | same `tests.txt` (`test_smoke.py`, `test_security.py`, `test_maintenance.py`) | PASS (89 of 89 tests) |
| Score page under 3 s, live and warm, after v0.5.0 deploy (NFR-01) | 20 of 20 | `evidence/benchmarks/render-warm-20261109T222224Z/` | PASS: 20 of 20; median 0.177 s, p95 0.196 s, max 0.248 s |
| First request after idle (cold start), v0.5.0 | Reference | warm-up line of the same run (not counted in the 20) | 32.2 s, consistent with 32.4 s at v0.3.0 |

## v0.4.0 (three scenarios)

| Criterion | Threshold | Evidence | Result |
|---|---|---|---|
| Known answers, all three scenarios | 21 of 21 | `evidence/runs/v0.4.0/known_answers.md` | PASS |
| All tests (78) | All pass | `evidence/runs/v0.4.0/tests.txt` | PASS (Python 3.11.16) |
| Random-guessing baseline | Reference | `evidence/runs/v0.4.0/score_distribution.txt` | Prepared on 6.2%, 7.8%, 6.2% of paths |

## v0.3.0 (Hard Stop 4)

| Criterion | Threshold | Evidence | Result |
|---|---|---|---|
| Known answers, sc01 | 7 of 7 | `evidence/runs/v0.3.0/known_answers.md` | PASS |
| Score page under 3 s, local | 20 of 20 | `evidence/benchmarks/codespace-local-20261019T015148Z/` | PASS (median 0.022 s) |
| Score page under 3 s, live and warm | 20 of 20 | `evidence/benchmarks/render-warm-20261026T013515Z/` | PASS (median 0.164 s, max 0.313 s) |
| Score page under 3 s, live after a cold start | Score page under 3 s | `evidence/benchmarks/render-cold-20261026T023445Z/`, `render-cold-20261026T030137Z/` | PASS for the score page (0.146 s, 0.181 s); **first page 32.4 s** both times (limitation) |
| Runs labeled "render-cold" that were not cold | — | `render-cold-20261026T021107Z` (two minutes after a redeploy), `render-cold-20261026T023602Z` (one minute after a cold start) | Kept and labeled; excluded |
| Live site rejects bad requests (NFR-08) | 400, 404, 302 | `evidence/benchmarks/render-probes-20261026.txt` | PASS |
| Production refuses to start without secret key or database | Clear startup error | configuration and security tests; first Render deploy | PASS |

## Not yet demonstrated

| Criterion | Threshold | Status |
|---|---|---|
| Rubric validity (NFR-07) | All 36 entries cite a verifiable control; 30% or more independently checked | Audit in progress |
| Usability, usefulness, availability (NFR-02, NFR-03, NFR-05) | 80% unassisted completion; usefulness 4.0/5 or more; 95% uptime | Peer testing scheduled after the remaining features |