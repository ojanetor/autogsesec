"""Remove abandoned sessions or old test data from the database.

Works on whatever database DATABASE_URL points to (local SQLite by default).
It is a dry run unless --apply is given: it first shows what would be removed.

Usage:
    python scripts/purge_sessions.py --abandoned-hours 24
    python scripts/purge_sessions.py --abandoned-hours 24 --apply
    python scripts/purge_sessions.py --started-before 2026-11-18T00:00:00Z
    python scripts/purge_sessions.py --started-before 2026-11-18T00:00:00Z --apply

To clean the live Render database, run it from your Codespace with
DATABASE_URL set to the Render Postgres *External* Database URL for that one
command (see docs/runbook.md). Never commit that URL.
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def parse_utc(text):
    value = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise argparse.ArgumentTypeError("include a time zone, e.g. 2026-11-18T00:00:00Z")
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    rule = parser.add_mutually_exclusive_group(required=True)
    rule.add_argument("--abandoned-hours", type=int,
                      help="unfinished sessions started more than this many hours ago")
    rule.add_argument("--started-before", type=parse_utc,
                      help="every session started before this UTC time (test data)")
    parser.add_argument("--apply", action="store_true", help="actually delete (default: dry run)")
    args = parser.parse_args()

    from app import app
    from maintenance import find_sessions, purge

    with app.app_context():
        try:
            sessions = find_sessions(abandoned_hours=args.abandoned_hours,
                                     started_before=args.started_before)
        except ValueError as problem:
            parser.error(str(problem))
        engine = app.extensions["sqlalchemy"].engine.name
        for exercise in sessions:
            state = "finished" if exercise.completed_at else "unfinished"
            print(f"  {exercise.started_at.isoformat()}  {exercise.scenario_id}  {state}  "
                  f"{len(exercise.responses)} responses")
        counts = purge(sessions, apply=args.apply)

    action = "Deleted" if counts["deleted"] else "Would delete (dry run)"
    print(f"{action}: {counts['sessions']} sessions, {counts['responses']} responses "
          f"[database: {engine}]")
    if not args.apply and counts["sessions"]:
        print("Run again with --apply to delete them.")


if __name__ == "__main__":
    main()
    