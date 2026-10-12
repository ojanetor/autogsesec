# Risk and Issue Log — AutoGSESec

Last reviewed: 2026-10-11 (Hard Stop 3). Reviewed at the end of every sprint and hard stop.

**Severity:** High = blocks the minimum viable artifact or invalidates results. Medium = degrades a requirement; a workaround exists. Low = minor or unlikely.
**Status:** Open, Monitoring, Mitigated, Closed.
**Owner:** O. Anetor (sole developer) for all items.

## Risks

| ID | Risk | Severity | Mitigation | Status |
|----|------|----------|-----------|--------|
| R-01 | Rubric mappings are wrong or unjustifiable | High | Draft content labeled; startup validator; NFR-07 independent spot-check of at least 30% of entries, starting with sc02/sc03 (T5) | Open |
| R-02 | Render free tier deletes local files, wiping a SQLite database | Medium (was High) | Postgres path validated in CI on every pull request (HS3); `DATABASE_URL` accepts Render's URL format; Render Postgres itself still untested (I-11) | Mitigated |
| R-03 | Free-tier cold start (about one minute) breaks NFR-01 | Medium | Warm the service before timed tests; report cold starts separately | Open |
| R-04 | ATT&CK or SP 800-82 revised mid-project | Medium | Version tags; separated mappings; version tag stored with every session (HS3); re-audit at each hard stop | Monitoring |
| R-05 | Schedule slip: database persistence (T3) one week behind plan | Medium | T3 and T4 completed in Week 6 (HS3); slip recovered | Closed |
| R-06 | Public deployment before CSRF protection | Medium | Security hardening (T10) must finish before deployment (T11) | Open |
| R-07 | Peer reviewers unavailable in Week 9 | Medium | Recruit by Week 7; recorded local demo as fallback | Open |
| R-08 | Codespaces free hours exhausted | Low | 2-core machine only; stop when idle; delete unused codespaces | Mitigated |
| R-09 | Scenario content misused for attacks (dual use) | Low | Conceptual content only, from public MITRE and NIST sources | Mitigated |
| R-10 | Scenario content (T5) not ready for the midpoint demo; only sc01 exists | High | T5 is the next sprint's first task; scoring work paused until sc02 drafts exist | Open |
| R-11 | Tests pass on SQLite but fail on Postgres (database behavior differs) | Medium | Every pull request runs all tests on both databases (HS3) | Mitigated |

## Known Issues

| ID | Issue | Severity | Action | Target | Status |
|----|-------|----------|--------|--------|--------|
| I-01 | sc01 scenario and mapping are drafts, not yet audited | Medium | NFR-07 audit | HS4 | Open |
| I-02 | Answers held only in the session cookie; not saved (FR-03 partial) | Medium | Database persistence (T3) | Sprint II | Closed |
| I-03 | Scoring engine and report are placeholders | High | Implement T7 and T8 | HS4 | Open |
| I-04 | No CSRF protection on forms | Medium | Add in T10 | HS5 | Open |
| I-05 | Development SECRET_KEY fallback in code | Medium | Require environment variable in production | HS5 | Open |
| I-06 | Statistical treatment of usability and survey data not specified (HS2 feedback) | Low | Plan recorded: descriptive statistics only (see Sprint I reflection) | Sprint I | Closed |
| I-07 | Force push to main on 2026-09-27 overwrote remote history | Low | Repository verified complete against the HS2 package; no-force-push rule added to conventions | Sprint I | Closed |
| I-08 | docs/architecture.md contained a superseded schema | Low | Rewritten for v0.1.0 | Sprint I | Closed |
| I-09 | Timestamps stored without a time zone; on a Postgres server set to another zone, times were shifted by the server's offset | High | Found by the Postgres test run; columns changed to time-zone-aware; regression test added; CI runs Postgres in a non-UTC zone (`PGTZ`) | HS3 | Closed |
| I-10 | No schema migrations; `db.create_all()` creates missing tables but never changes existing ones | Medium | Workaround: delete local `instance/autogsesec.db` after a model change. Fix: add a migration tool before deployment | HS5 | Open |
| I-11 | Render Postgres not tested directly; only Postgres 16 in GitHub Actions | Medium | Test during first deployment (T11) | Week 8 | Open |
| I-12 | Abandoned sessions accumulate; every "Start" creates a row | Low | Purge rule for sessions with no completion time, before the testing window | HS5 | Open |
| I-13 | SQLite returns stored times without a time zone marker; correct only by the convention that all times are UTC | Low | Documented in docs/environment.md; Postgres stores the zone explicitly | HS3 | Monitoring |
| I-14 | Codespace runs Python 3.11.16; CI installs the latest 3.11 patch, so patch versions can differ | Low | Only the minor version (3.11) is pinned; acceptable. Pin the patch version if a difference ever appears | — | Monitoring |
