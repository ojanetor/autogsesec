# Engineering Log — AutoGSESec

## Week 2

**Completed:**
- Hard Stop 1 Proposal Approval Package submitted
- GitHub repository created at ojanet/autogssec
- Folder structure initialized
- Charter, architecture, and requirements documentation drafted

**Decisions Made:**
- Selected Option B (Tabletop Exercise Platform) over threat assessment tool and survey dashboard
- Minimum viable artifact set at 3 scenarios rather than 5 — realistic given Flask learning curve
- Rule-based scoring chosen over ML for explainability and feasibility

**Blockers:**
- Flask environment not yet configured
- No prior Flask experience — Week 2 dedicated to orientation

**Next Steps:**
- Install Python 3.11 and Flask
- Build first working Flask route
- Draft scenario content for 3 modules

## Week 3

**Completed:**
- Literature and Requirements Brief submitted: FR-01 to FR-12, NFR-01 to NFR-09, use cases

## Week 4

**Completed:**
- Moved development to GitHub Codespaces with a Python 3.11 dev container
- Built a navigable vertical slice of sc01 (GPS spoofing) with separated content and mappings
- Added startup validation and 3 automated tests
- Corrected the third module to Impact (TA0105); the earlier TA0106 label was wrong
- Hard Stop 2 Design Review Package submitted

**Decisions:** content as versioned JSON in Git; database for runtime data only

## Week 5 — Implementation Sprint I

**Completed:**
- Baseline documentation: conventions, risk and issue log, changelog, current architecture
- Placeholder interfaces for scoring and report modules
- Smoke tests and GitHub Actions; dependencies split into runtime and dev
- Branch strategy adopted; v0.1.0 baseline tagged

**Slipped:** database persistence (T3) moved to Sprint II

## Week 6 — Hard Stop 3

**Completed:**
- T3: sessions and responses saved with SQLAlchemy; data survives restarts
- T4: `DATABASE_URL` configuration; Postgres 16 test job added to GitHub Actions
- Found and fixed a time-zone defect (I-09) that only appeared on Postgres
- README, environment notes, risk and issue log updated; v0.2.0 tagged

**Recovered:** the one-week T3 slip from Sprint I

**Started, not finished:** scoring engine (T7), paused to prepare the Hard Stop 3 package

**Next:** sc02 and sc03 content (T5), then scoring (T7)

## Week 7 — Midpoint

**Completed:**
- Resumed the scoring engine after supervisor feedback separated technical correctness from assessment validity
- Built the after-action report, CSRF protection, production startup checks, and Render deployment
- Seven known-answer cases recomputed by hand; 51 tests passing
- Midpoint demo and adjustment memo submitted

**Found:** first Render deploy stopped because `SECRET_KEY` was missing (the startup check worked as designed)

## Week 8 — Hard Stop 4

**Completed:**
- Found on the live site that Render was running on a temporary SQLite file because `DATABASE_URL` was missing; connected Render Postgres and made production refuse to start without it
- Fixed the benchmark script, which the HTTPS form check rejected because it sent no Referer header; real users were unaffected
- Live benchmarks: warm 20 of 20 score pages under 3 s (median 0.16 s); two cold starts of 32.4 s for the first page
- Live probes, evidence index, v0.3.0 tag and evidence record

**Next:** sc02 and sc03 content and the mapping audit (Week 9), recruit three peer reviewers

