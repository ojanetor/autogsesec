"""Print the stored sessions and responses from the local SQLite database.

Development evidence tool. Usage: python scripts/inspect_db.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "autogsesec.db"


def main():
    if not DB_PATH.exists():
        print(f"No database yet at {DB_PATH}. Run the app and finish a scenario first.")
        return
    conn = sqlite3.connect(DB_PATH)
    sessions = conn.execute(
        "SELECT session_id, scenario_id, content_version, started_at, completed_at "
        "FROM sessions ORDER BY started_at"
    ).fetchall()
    responses = conn.execute(
        "SELECT session_id, decision_point_id, option_id, submitted_at "
        "FROM responses ORDER BY response_id"
    ).fetchall()
    conn.close()

    print(f"sessions: {len(sessions)}")
    for row in sessions:
        print("  ", row)
    print(f"responses: {len(responses)}")
    for row in responses:
        print("  ", row)


if __name__ == "__main__":
    main()