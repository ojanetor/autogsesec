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