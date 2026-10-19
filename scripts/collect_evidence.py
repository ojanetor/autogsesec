"""Collect a dated, inspectable evidence record for the current commit.

Runs the automated checks and saves their output, plus a manifest of the exact
environment, to evidence/runs/<label>/. Commit the folder so the evidence is
versioned with the code it describes.

Usage:
    python scripts/collect_evidence.py --label v0.3.0-codespace
"""
import argparse
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def git(*args):
    return run(["git", *args])[1].strip()


def known_answer_table():
    from engine.content import load_all, load_control_names
    from engine.report import build_report
    from engine.scoring import score_session

    scenarios = load_all()
    names = load_control_names()
    known = json.loads((ROOT / "tests" / "data" / "known_answers_sc01.json").read_text())
    scenario = scenarios[known["scenario_id"]]

    lines = [
        "| Case | Answers | Expected | Actual | Match |",
        "|---|---|---|---|---|",
    ]
    matches = 0
    for case in known["cases"]:
        exp = case["expected"]
        score = score_session(scenario, case["answers"])
        report = build_report(scenario, score, names)
        actual = {
            "earned": score["earned"],
            "percent": score["percent"],
            "readiness": report["readiness"],
            "gap_order": [g["decision_point_id"] for g in score["gaps"]],
            "recommended": {g["timeline"]: [c["id"] for c in g["controls"]]
                            for g in report["recommendations"]},
        }
        ok = all(actual[k] == exp[k] for k in exp)
        matches += ok
        answers = ", ".join(f"{k}={v}" for k, v in case["answers"].items())
        lines.append(
            f"| {case['id']} | {answers} | {exp['earned']}/6, {exp['percent']}%, {exp['readiness']} "
            f"| {actual['earned']}/6, {actual['percent']}%, {actual['readiness']} | {'yes' if ok else 'NO'} |"
        )
    lines.append("")
    lines.append(f"{matches} of {len(known['cases'])} known-answer cases match "
                 "(score, readiness, gap order and recommended controls compared).")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True, help="e.g. v0.3.0-codespace")
    args = parser.parse_args()

    out = ROOT / "evidence" / "runs" / args.label
    out.mkdir(parents=True, exist_ok=True)

    commands = {
        "tests.txt": [sys.executable, "-m", "pytest", "-v", "--durations=5",
                      f"--junitxml={out / 'tests-junit.xml'}"],
        "score_distribution.txt": [sys.executable, "scripts/score_distribution.py"],
    }
    results = {}
    for filename, command in commands.items():
        code, output = run(command)
        (out / filename).write_text(output)
        results[filename] = {"command": " ".join(Path(c).name if c == sys.executable else c
                                                 for c in command), "exit_code": code}

    (out / "known_answers.md").write_text(known_answer_table() + "\n")

    manifest = {
        "label": args.label,
        "collected_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": git("rev-parse", "HEAD"),
        "git_describe": git("describe", "--tags", "--always", "--dirty"),
        "git_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": run([sys.executable, "-m", "pip", "freeze"])[1].split(),
        "outputs": results,
        "files": sorted(p.name for p in out.iterdir()),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"Evidence saved to {out.relative_to(ROOT)}")
    for name, info in results.items():
        status = "ok" if info["exit_code"] == 0 else f"FAILED (exit {info['exit_code']})"
        print(f"  {name}: {status}")
    print("  known_answers.md, manifest.json")


if __name__ == "__main__":
    main()
    