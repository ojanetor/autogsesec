## Data Design (updated at Hard Stop 2)

The original draft stored scenarios and rubrics as database tables. As of
Hard Stop 2, scenario content and framework mappings live in versioned JSON
files in Git, and the database holds runtime data only. This keeps content
and control mappings independently updatable as MITRE ATT&CK and NIST
SP 800-82 are revised.

### Content (versioned JSON in Git)

| File | Holds |
|------|-------|
| `data/scenarios/<id>.json` | Story, prompts, and options only (no framework IDs) |
| `data/mappings/<id>.json` | Rating, NIST controls, timeline, and rationale per option; ATT&CK tactic; framework versions |
| `data/frameworks.json` | Valid ATT&CK for ICS tactic IDs and NIST control IDs, with version tags |

`engine/content.py` validates every mapping at startup and refuses to start
if any option is unmapped or references an unknown ID.

### Runtime database (SQLite via SQLAlchemy, built in Hard Stop 3)

**sessions**: session_id (random UUID), scenario_id, content_version, started_at, completed_at, pre_understanding, post_understanding

**responses**: response_id, session_id, decision_point_id, option_id, submitted_at

No field identifies a person (NFR-09). Scores are not stored: the
after-action report is regenerated from responses and mappings, which
deterministic scoring makes identical every time (NFR-06).







# OLD:  System Architecture — AutoGSESec

## Three-Tier Web Application

## Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Frontend | HTML, CSS, vanilla JavaScript | No framework overhead |
| Backend | Python 3.11 + Flask 3.x | Lightweight, beginner-accessible |
| Database | SQLite via SQLAlchemy | File-based, no server setup |
| Hosting | Render.com free tier | Auto-deploy from GitHub |
| Version Control | GitHub — ojanet/autogssec | Public repository |

## Database Schema (draft)

**scenarios** — id, tactic_code, title, description, decision_points
**responses** — id, session_id, scenario_id, decision_point, selected_option
**sessions** — id, started_at, completed_at, total_score
**rubrics** — id, scenario_id, decision_point, option, points, nist_control, timeline

## Computational Method

Rule-based deterministic scoring. Responses matched against predefined rubric. Points scored divided by points possible produces percentage readiness score. No machine learning — scoring must be fully explainable for a security training tool.
