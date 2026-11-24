# Defect Log — AutoGSESec

Severity: **Critical** = wrong score or report, data loss, or data exposure. **Major** = a feature or deployment does not work, or an unsafe default. **Minor** = inconvenience, tooling, or appearance.

Threshold (NFR-04): zero critical and at most three minor defects open at the end of testing.

| ID | Found | Defect | Severity | How found | Fix | Status | Risk log |
|---|---|---|---|---|---|---|---|
| D-01 | HS3 | Stored times shifted by the server's time-zone offset on Postgres | Major | Postgres test job | Time-zone-aware columns; UTC writes; CI runs Postgres in a non-UTC zone | Closed | I-09 |
| D-02 | HS4 | Live site ran on a temporary SQLite file; sessions lost on each spin-down | Critical | `/health` on the live site | `DATABASE_URL` set; production refuses to start without it; test | Closed | I-18 |
| D-03 | HS4 | Benchmark script rejected by the HTTPS form-security check | Minor | First live benchmark | Script sends browser-like headers | Closed | I-19 |
| D-04 | v0.4.0 | Four content files saved with " copy" in their names | Minor | Repository review | Renamed; naming test | Closed | I-20 |
| D-05 | HS5 | `python app.py` started the interactive debugger by default | Major | Code review | Off unless `FLASK_DEBUG=1`; test | Closed | I-21 |
| D-06 | HS5 | Unknown pages and expired forms showed bare default error pages | Minor | Manual check | Friendly 404, expired-form, and 500 pages; tests | Closed | I-22 |
| D-07 | Nov 23 | Deploy failed after database recreation: start command entered as the build command | Major | Render deploy log | Build and start commands corrected; deploy succeeded | Closed | — |

**Open at v0.6.0:** 0 critical, 0 major, 0 minor.

Defects found during peer testing (November 23–28) will be added from D-08, by tester ID only.
