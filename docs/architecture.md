# System Architecture — AutoGSESec

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
