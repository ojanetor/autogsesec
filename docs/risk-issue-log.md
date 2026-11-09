# Risk and Issue Log — AutoGSESec

Last reviewed: 2026-11-09 (Hard Stop 5). Reviewed at the end of every sprint and hard stop.

**Severity:** High = blocks the minimum viable artifact or invalidates results. Medium = degrades a requirement; a workaround exists. Low = minor or unlikely.
**Status:** Open, Monitoring, Mitigated, Closed.
**Owner:** O. Anetor (sole developer) for all items.

## Risks

| ID | Risk | Severity | Mitigation | Evidence for current rating | Status |
|----|------|----------|-----------|-----------------------------|--------|
| R-01 | Rubric mappings are wrong or unjustifiable | High | Startup validator; source citation for all 36 entries; independent check of at least 11 (30%) | Structural checks only; audit in progress | Open |
| R-02 | Render free tier deletes local files, wiping a SQLite database | Low (was Medium) | Render Postgres connected; production refuses to start without `DATABASE_URL` | `/health` on Render reports `postgresql`; configuration test | Mitigated |
| R-03 | Free-tier cold start breaks the 3-second requirement | Medium | Report warm and cold results separately; warm the service before demos and peer sessions | Warm: 20 of 20 under 3 s (median 0.16 s); cold runs in `evidence/benchmarks/` | Open |
| R-04 | ATT&CK or SP 800-82 revised mid-project | Medium | Version tags stored with every session; re-audit at each hard stop | SP 800-82 Rev. 4 draft published September 2026 | Monitoring |
| R-06 | Public deployment before CSRF protection | Low (was Medium) | CSRF on all forms; secure cookies | Live probe: form post without token returns 400 | Mitigated |
| R-07 | Peer reviewers unavailable | Medium (was High) | Three reviewers recruited verbally and asked to wait until the features are built; recorded demo as fallback | Testing dates not yet fixed | Open |
| R-08 | Codespaces free hours exhausted | Low | 2-core machine; stop when idle | — | Mitigated |
| R-09 | Scenario content misused (dual use) | Low | Conceptual content only, public MITRE and NIST sources | — | Mitigated |
| R-10 | sc02 and sc03 not ready in time for peer testing | High | First task of Week 9; peer testing moved to Week 10 | Both merged Nov 9 (v0.4.0), eight days after the Nov 1 checkpoint | Closed |
| R-11 | Tests pass on SQLite but fail on Postgres | Low | Every pull request runs all tests on both | Both CI jobs green since HS3 | Mitigated |
| R-12 | Free Render Postgres expires about 30 days after creation | Medium | Recreate before peer testing (runbook); export peer results to `evidence/` first | Render free-tier policy; exact date to confirm in the Render dashboard | Open |

## Known Issues

| ID | Issue | Severity | Action | Target | Status |
|----|-------|----------|--------|--------|--------|
| I-01 | All three mappings are drafts, not yet audited | Medium | Mapping audit | Nov 12 | Open |
| I-03 | Scoring engine and report were placeholders | High | Implemented and tested with known answers | HS4 | Closed |
| I-04 | No CSRF protection on forms | Medium | Flask-WTF CSRF added | HS4 | Closed |
| I-05 | Development SECRET_KEY fallback in code | Medium | Production refuses to start without it; confirmed on the first Render deploy | HS4 | Closed |
| I-09 | Timestamps shifted by the server's time-zone offset on Postgres | High | Time-zone-aware columns; regression test | HS3 | Closed |
| I-10 | No schema migrations | Medium | Deferred from HS5: no schema change has happened yet. The migration tool is added with the first schema change (understanding rating), before peer testing; until then a fresh database gets the full schema at startup | Nov 14–17 | Open |
| I-11 | Render Postgres not tested directly | Medium | Deployed, connected, and benchmarked | HS4 | Closed |
| I-12 | Abandoned sessions accumulate | Low | `scripts/purge_sessions.py --abandoned-hours`; 8 tests; run before peer testing | HS5 | Mitigated |
| I-13 | SQLite returns times without a zone marker | Low | All times written in UTC; Postgres stores the zone | — | Monitoring |
| I-14 | Python patch versions differ (old Codespace 3.11.16, CI and Render 3.11.17, new Codespace 3.11.18) | Low | Recorded in every evidence manifest; identical results on all three (v0.5.0 clean run) | — | Monitoring |
| I-16 | One gunicorn worker only, because startup table creation could race | Low | Remove the limit once migrations exist | HS5 | Open |
| I-17 | Benchmark runs leave test sessions in the production database | Low | `scripts/purge_sessions.py --started-before`; run on the live database before peer testing | HS5 | Mitigated |
| I-18 | Render silently ran on a temporary SQLite file because `DATABASE_URL` was missing; sessions were lost on each spin-down | High | Found by checking `/health` on the live site; variable set; production now refuses to start without it; test added | HS4 | Closed |
| I-19 | Benchmark script rejected by the HTTPS CSRF check because it sent no Referer header | Low | Script now sends Referer like a browser; real users unaffected (confirmed in browser) | HS4 | Closed |
| I-20 | Four content files saved with " copy" in their names; all tests still passed | Medium | Renamed; naming-convention test added | v0.4.0 | Closed |
| I-21 | `python app.py` started Flask's interactive debugger by default | Medium | Off unless `FLASK_DEBUG=1`; test added | HS5 | Closed |
| I-22 | Unknown pages and expired forms showed Flask's bare default error pages | Low | Friendly 404, expired-form, and 500 pages; tests added | HS5 | Closed |