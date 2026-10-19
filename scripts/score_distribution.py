"""Score every possible answer combination for each scenario and summarize.

Early analytics evidence for the scoring engine. Usage:
    python scripts/score_distribution.py
"""
import sys
from collections import Counter
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.content import load_all  # noqa: E402
from engine.scoring import score_session  # noqa: E402


def main():
    for scenario in load_all().values():
        point_ids = [p["id"] for p in scenario["decision_points"]]
        choices = [[o["id"] for o in p["options"]] for p in scenario["decision_points"]]
        results = [score_session(scenario, dict(zip(point_ids, c))) for c in product(*choices)]

        print(f"{scenario['id']}: {scenario['title']}")
        print(f"  answer combinations scored: {len(results)}")
        print("  score distribution:")
        for percent, count in sorted(Counter(r["percent"] for r in results).items()):
            print(f"    {percent:5.1f}%  {count:3d}  {'#' * count}")
        print("  readiness bands:")
        bands = Counter(r["readiness"] for r in results)
        for label in ("Prepared", "Developing", "Unprepared"):
            share = bands[label] / len(results) * 100
            print(f"    {label:<11} {bands[label]:3d}  ({share:.1f}%)")
        print()


if __name__ == "__main__":
    main()
