# Risk and Issue Log — AutoGSESec

Last reviewed: 2026-10-25 (Hard Stop 4). Reviewed at the end of every sprint and hard stop.

**Severity:** High = blocks the minimum viable artifact or invalidates results. Medium = degrades a requirement; a workaround exists. Low = minor or unlikely.
**Status:** Open, Monitoring, Mitigated, Closed.
**Owner:** O. Anetor (sole developer) for all items.

## Risks

| ID | Risk | Severity | Mitigation | Evidence for current rating | Status |
|----|------|----------|-----------|-----------------------------|--------|
| R-01 | Rubric mappings are wrong or unjustifiable | High | Startup validator; independent audit of at least 30% of entries with sc02/sc03 | Only structural checks exist; no content audit yet | Open |
| R-02 | Render free tier deletes local files, wiping a SQLite database | Low (was Medium) | Render Postgres connected; production refuses to start without `DATABASE_URL` | `/health` on Render reports `postgresql`; configuration test | Mitigated |
| R-03 | Free-tier cold start breaks the 3-second requirement | Medium | Report warm and cold results separately; warm the service before demos and peer sessions | Warm: 20 of 20 under 3 s (median 0.16 s); cold runs in `evidence/benchmarks/` | Open |
| R-04 | ATT&CK or SP 800-82 revised mid-project | Medium | Version tags stored with every session; re-audit at each hard stop | SP 800-82 Rev. 4 draft published September 2026 | Monitoring |
| R-06 | Public deployment before CSRF protection | Low (was Medium) | CSRF on all forms; secure cookies | Live probe: form post without token returns 400 | Mitigated |
| R-07 | Peer reviewers unavailable | High (was Medium) | Recruit three reviewers now for early November; recorded demo as fallback | No reviewers confirmed yet | Open |
| R-08 | Codespaces free hours exhausted | Low | 2-core machine; stop when idle | — | Mitigated |
| R-09 | Scenario content misused (dual use) | Low | Conceptual content only, public MITRE and NIST sources | — | Mitigated |
| R-10 | sc02 and sc03 not ready in time for peer testing | High | First task of Week 9; peer testing moved to Week 10 | Content task two weeks behind plan | Open |
| R-11 | Tests pass on SQLite but fail on Postgres | Low | Every pull request runs all tests on both | Both CI jobs green since HS3 | Mitigated |
| R-12 | Free Render Postgres expires about 30 days after creation | Medium | Recreate the database before the final demo; data is test data only | Render free-tier policy | Open |

## Known Issues

| ID | Issue | Severity | Action | Target | Status |
|----|-------|----------|--------|--------|--------|
| I-01 | sc01 scenario and mapping are drafts, not yet audited | Medium | Mapping audit | Week 9 | Open |
| I-03 | Scoring engine and report were placeholders | High | Implemented and tested with known answers | HS4 | Closed |
| I-04 | No CSRF protection on forms | Medium | Flask-WTF CSRF added | HS4 | Closed |
| I-05 | Development SECRET_KEY fallback in code | Medium | Production refuses to start without it; confirmed on the first Render deploy | HS4 | Closed |
| I-09 | Timestamps shifted by the server's time-zone offset on Postgres | High | Time-zone-aware columns; regression test | HS3 | Closed |
| I-10 | No schema migrations | Medium | Add a migration tool | HS5 | Open |
| I-11 | Render Postgres not tested directly | Medium | Deployed, connected, and benchmarked | HS4 | Closed |
| I-12 | Abandoned sessions accumulate | Low | Purge rule before peer testing | HS5 | Open |
| I-13 | SQLite returns times without a zone marker | Low | All times written in UTC; Postgres stores the zone | — | Monitoring |
| I-14 | Python patch versions differ (Codespace 3.11.16, Render and CI 3.11.17) | Low | Recorded in every evidence manifest | — | Monitoring |
| I-16 | One gunicorn worker only, because startup table creation could race | Low | Remove the limit once migrations exist | HS5 | Open |
| I-17 | Benchmark runs leave test sessions in the production database | Low | Purge before peer testing | HS5 | Open |
| I-18 | Render silently ran on a temporary SQLite file because `DATABASE_URL` was missing; sessions were lost on each spin-down | High | Found by checking `/health` on the live site; variable set; production now refuses to start without it; test added | HS4 | Closed |
| I-19 | Benchmark script rejected by the HTTPS CSRF check because it sent no Referer header | Low | Script now sends Referer like a browser; real users unaffected (confirmed in browser) | HS4 | Closed |
