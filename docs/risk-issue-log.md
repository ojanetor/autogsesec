# Risk and Issue Log — AutoGSESec

Last reviewed: 2026-10-03 (Sprint I). Reviewed at the end of every sprint.

**Severity:** High = blocks the minimum viable artifact or invalidates results. Medium = degrades a requirement; a workaround exists. Low = minor or unlikely.
**Status:** Open, Monitoring, Mitigated, Closed.
**Owner:** O. Anetor (sole developer) for all items.

## Risks

| ID | Risk | Severity | Mitigation | Status |
|----|------|----------|-----------|--------|
| R-01 | Rubric mappings are wrong or unjustifiable | High | Draft content labeled; startup validator; NFR-07 independent spot-check of at least 30% of entries, starting with sc02/sc03 (T5) | Open |
| R-02 | Render free tier deletes local files, wiping a SQLite database | High | Use free Render Postgres for the Week 9 test window; SQLAlchemy keeps code database-independent; decide at T4 | Open |
| R-03 | Free-tier cold start (about one minute) breaks NFR-01 | Medium | Warm the service before timed tests; report cold starts separately | Open |
| R-04 | ATT&CK or SP 800-82 revised mid-project | Medium | Version tags; separated mappings; re-audit at each hard stop | Monitoring |
| R-05 | Schedule slip: database persistence (T3) one week behind plan | Medium | Moved to Sprint II alongside T4; scenario drafting (T5) runs in parallel | Open |
| R-06 | Public deployment before CSRF protection | Medium | Security hardening (T10) must finish before deployment (T11) | Open |
| R-07 | Peer reviewers unavailable in Week 9 | Medium | Recruit by Week 7; recorded local demo as fallback | Open |
| R-08 | Codespaces free hours exhausted | Low | 2-core machine only; stop when idle; delete unused codespaces | Mitigated |
| R-09 | Scenario content misused for attacks (dual use) | Low | Conceptual content only, from public MITRE and NIST sources | Mitigated |

## Known Issues

| ID | Issue | Severity | Action | Target | Status |
|----|-------|----------|--------|--------|--------|
| I-01 | sc01 scenario and mapping are drafts, not yet audited | Medium | NFR-07 audit | HS4 | Open |
| I-02 | Answers held only in the session cookie; not saved (FR-03 partial) | Medium | Database persistence (T3) | Sprint II | Open |
| I-03 | Scoring engine and report are placeholders | High | Implement T7 and T8 | HS4 | Open |
| I-04 | No CSRF protection on forms | Medium | Add in T10 | HS5 | Open |
| I-05 | Development SECRET_KEY fallback in code | Medium | Require environment variable in production | HS5 | Open |
| I-06 | Statistical treatment of usability and survey data not specified (HS2 feedback) | Low | Plan recorded: descriptive statistics only (see Sprint I reflection) | Sprint I | Closed |
| I-07 | Force push to main on 2026-09-27 overwrote remote history | Low | Repository verified complete against the HS2 package; no-force-push rule added to conventions | Sprint I | Closed |
| I-08 | docs/architecture.md contained a superseded schema | Low | Rewritten for v0.1.0 | Sprint I | Closed |