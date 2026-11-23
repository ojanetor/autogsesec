"""Export anonymous peer-testing results from the database to evidence/.

Writes one CSV row per exercise session started at or after --since, and a
summary with completion, understanding before and after, and usefulness
(FR-10, NFR-03, NFR-05). Sessions hold no personal data, so the export holds
none either.

Usage:
    python scripts/export_results.py --since 2026-11-24T00:00:00Z --label peer-testing
    DATABASE_URL='<External Database URL from Render>' python scripts/export_results.py --since 2026-11-24T00:00:00Z --label peer-testing

Output: evidence/peer-testing/<label>-<UTC time>/sessions.csv and summary.json
"""
import argparse
import csv
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FIELDS = ["session", "scenario_id", "started_utc", "completed", "pre_understanding",
          "post_understanding", "understanding_change", "usefulness",
          "earned", "possible", "percent", "readiness"]


def parse_utc(text):
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise argparse.ArgumentTypeError("include a time zone, e.g. 2026-11-24T00:00:00Z")
    return value


def as_utc(moment):
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def session_rows(sessions, scenarios):
    from app import complete_answers
    from engine.scoring import score_session

    rows = []
    for exercise in sessions:
        scenario = scenarios.get(exercise.scenario_id)
        answers = complete_answers(scenario, exercise) if scenario else None
        score = score_session(scenario, answers) if answers else None
        change = (exercise.post_understanding - exercise.pre_understanding
                  if exercise.pre_understanding and exercise.post_understanding else None)
        rows.append({
            "session": exercise.session_id[:8],
            "scenario_id": exercise.scenario_id,
            "started_utc": as_utc(exercise.started_at).isoformat(timespec="seconds"),
            "completed": exercise.completed_at is not None,
            "pre_understanding": exercise.pre_understanding,
            "post_understanding": exercise.post_understanding,
            "understanding_change": change,
            "usefulness": exercise.usefulness,
            "earned": score["earned"] if score else None,
            "possible": score["possible"] if score else None,
            "percent": score["percent"] if score else None,
            "readiness": score["readiness"] if score else None,
        })
    return rows


def summarize(rows):
    def mean(values):
        values = [v for v in values if v is not None]
        return round(statistics.mean(values), 2) if values else None

    completed = [r for r in rows if r["completed"]]
    usefulness = [r["usefulness"] for r in rows if r["usefulness"] is not None]
    return {
        "sessions_started": len(rows),
        "sessions_completed": len(completed),
        "completion_rate": round(len(completed) / len(rows), 3) if rows else None,
        "usefulness_responses": len(usefulness),
        "usefulness_mean": mean(usefulness),
        "usefulness_4_or_5": sum(u >= 4 for u in usefulness),
        "pre_understanding_mean": mean(r["pre_understanding"] for r in rows),
        "post_understanding_mean": mean(r["post_understanding"] for r in rows),
        "paired_change_responses": sum(r["understanding_change"] is not None for r in rows),
        "paired_change_mean": mean(r["understanding_change"] for r in rows),
        "readiness_counts": {band: sum(r["readiness"] == band for r in completed)
                             for band in ("Prepared", "Developing", "Unprepared")},
        "by_scenario": {sid: sum(r["scenario_id"] == sid for r in completed)
                        for sid in sorted({r["scenario_id"] for r in rows})},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--since", type=parse_utc, required=True,
                        help="start of the testing window, UTC (e.g. 2026-11-24T00:00:00Z)")
    parser.add_argument("--label", required=True)
    args = parser.parse_args()

    from app import SCENARIOS, app
    from models import ExerciseSession

    with app.app_context():
        sessions = (ExerciseSession.query
                    .filter(ExerciseSession.started_at >= args.since)
                    .order_by(ExerciseSession.started_at).all())
        rows = session_rows(sessions, SCENARIOS)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = ROOT / "evidence" / "peer-testing" / f"{args.label}-{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "sessions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    summary = {"since_utc": args.since.isoformat(), "exported_utc": stamp, **summarize(rows)}
    (out / "summary.json").write_text(json.dumps(summary, indent=2))

    print(f"Saved to {out.relative_to(ROOT)}")
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
    