# Evidence Index — AutoGSESec v0.3.0

Every claim in the Hard Stop 4 package maps to a dated file in `evidence/`. Times are UTC.

| Criterion | Threshold | Evidence | Result |
|---|---|---|---|
| Scores and reports match hand-computed answers (FR-04, FR-07, FR-08) | 7 of 7 cases match | `evidence/runs/v0.3.0-codespace/known_answers.md` | PASS |
| Every possible sc01 answer path scores consistently (FR-04) | 64 of 64 paths | `evidence/runs/v0.3.0-codespace/tests.txt` (test_every_possible_answer_combination_scores_consistently) | PASS |
| Same input gives identical score and report (NFR-06) | 10 of 10 runs identical | `evidence/runs/v0.3.0-codespace/tests.txt` | PASS |
| Score page under 3 s, local (NFR-01) | 20 of 20 | `evidence/benchmarks/codespace-local-20261019T015148Z/summary.json` | PASS (median 0.022 s) |
| Score page under 3 s, live and warm (NFR-01) | 20 of 20 | `evidence/benchmarks/render-warm-20261026T013515Z/summary.json` | PASS (median 0.164 s, max 0.313 s) |
| Score page under 3 s, live after a cold start (NFR-01) | Score page under 3 s | `evidence/benchmarks/render-cold-20261026T023445Z/` and `evidence/benchmarks/[second cold run folder]/` | PASS for the score page (0.146 s); **first page took 32.4 s**, a limitation not covered by the requirement |
| Runs labeled "render-cold" that were not cold | — | `render-cold-20261026T021107Z` (site still awake), `render-cold-20261026T023602Z` (run one minute after a cold start) | Kept and labeled; excluded from cold-start analysis |
| Live site rejects bad requests (NFR-08) | 400, 404, 302 | `evidence/benchmarks/render-probes-20261026.txt` | PASS |
| Invalid input never stored; no personal data (NFR-08, NFR-09) | All tests pass | `evidence/runs/v0.3.0-codespace/tests.txt` | PASS |
| Production refuses to start without secret key or database | Startup stops with a clear error | Configuration and security tests; Render deploy log (first deploy) | PASS |
| Rubric validity (NFR-07) | 30% or more of entries independently audited | — | NOT YET (Week 9) |
| Usability, usefulness, availability (NFR-02, NFR-03, NFR-05) | Peer sessions | — | NOT YET (Week 10) |