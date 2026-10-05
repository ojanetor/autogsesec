# Engineering Conventions — AutoGSESec

## Naming

| Item | Convention | Example |
|------|-----------|---------|
| Python files and functions | snake_case | `score_session()` in `engine/scoring.py` |
| Scenario IDs | `sc` + two digits | `sc01` |
| Scenario and mapping files | `<id>_<short_name>.json`, same name in both folders | `sc01_gps_spoofing.json` |
| Decision points | `dp` + number | `dp1` |
| Options | lowercase letter | `a` to `d` |
| Branches | `<type>/<short-description>` | `sprint-1/baseline`, `feature/persistence`, `fix/csrf` |
| Version tags | `vMAJOR.MINOR.PATCH` | `v0.1.0` |

## Branch Strategy

- `main` is the only long-lived branch. It must always run and pass all tests.
- All work happens on a short-lived branch and is merged into `main` through a pull request after the GitHub Actions check passes.
- No force-pushing to `main`.
- Branches are deleted after merging.

## Commit Messages

One line, imperative mood, describing the change. Examples: "Add smoke tests", "Fix typo in Impact scenario ID".

## Versioning and Tags

- Each sprint or hard stop ends with an annotated tag on `main`.
- MINOR increases for each milestone (v0.1.0 Sprint I, v0.2.0 Sprint II). PATCH is for fixes between milestones.
- v1.0.0 marks the minimum viable artifact: three scenarios, scoring, after-action reports, public deployment.
- Every tag has a matching CHANGELOG.md entry and a GitHub Release.

## Artifact Storage

| Artifact | Location |
|----------|----------|
| Scenario content | `data/scenarios/` |
| Framework mappings | `data/mappings/`, `data/frameworks.json` |
| Design and process documents | `docs/` |
| Weekly engineering notes | `journal/engineering-log.md` |
| Release notes | `CHANGELOG.md` and GitHub Releases |
| Dependencies | `requirements.txt` (runtime), `requirements-dev.txt` (tests) |
| Evidence screenshots | Course submissions, not the repository; any tagged version can regenerate its test output |
| Secrets | Never in the repository; environment variables only |

## Rules for Content Changes

Any change under `data/` must pass `python -m pytest` before merging; the loader rejects unmapped options and unknown framework IDs. When a framework version changes, update `data/frameworks.json` and the `framework_versions` field of each affected mapping in the same pull request.