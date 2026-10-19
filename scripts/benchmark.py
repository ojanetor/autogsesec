"""Latency benchmark for NFR-01 (score display in under 3 seconds).

Plays complete sc01 exercises against a running AutoGSESec server, exactly as
a browser would (cookies and CSRF tokens included), and times every request.
Uses only the Python standard library.

Usage:
    python scripts/benchmark.py --base-url http://127.0.0.1:5000 --runs 20 --label local
    python scripts/benchmark.py --base-url https://<app>.onrender.com --runs 20 --label render-warm
    python scripts/benchmark.py --base-url https://<app>.onrender.com --runs 1 --label render-cold --no-warmup

Results are written to evidence/benchmarks/<label>-<UTC timestamp>/ as
requests.csv (one row per request) and summary.json.
"""
import argparse
import csv
import http.cookiejar
import json
import re
import statistics
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANSWERS = ["d", "b", "c"]  # a fixed, mixed path: correct, correct, partial
NFR01_LIMIT_SECONDS = 3.0
TOKEN = re.compile(r'name="csrf_token" value="([^"]+)"')


def timed(opener, url, data=None):
    body = urllib.parse.urlencode(data).encode() if data else None
    start = time.perf_counter()
    with opener.open(url, data=body, timeout=120) as response:
        html = response.read().decode("utf-8", errors="replace")
        status = response.status
    return time.perf_counter() - start, status, html


def one_exercise(base_url, run_number):
    """Run one full exercise in a fresh browser-like session; return request rows."""
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    rows = []

    def record(step, url, data=None):
        seconds, status, html = timed(opener, url, data)
        rows.append({"run": run_number, "step": step, "status": status, "seconds": round(seconds, 4)})
        return html

    html = record("start + decision 1", f"{base_url}/scenario/sc01/start")
    for number, choice in enumerate(ANSWERS, start=1):
        match = TOKEN.search(html)
        if match is None:
            raise RuntimeError(f"run {run_number}: no CSRF token on decision {number} page")
        step = "submit decision 3 + score page" if number == len(ANSWERS) else f"submit decision {number}"
        html = record(step, f"{base_url}/scenario/sc01/decision/{number}",
                      {"option_id": choice, "csrf_token": match.group(1)})
    if "Readiness" not in html:
        raise RuntimeError(f"run {run_number}: score page did not show a readiness rating")
    record("after-action report", f"{base_url}/scenario/sc01/report")
    return rows


def summarize(rows):
    by_step = {}
    for row in rows:
        by_step.setdefault(row["step"], []).append(row["seconds"])
    summary = {}
    for step, values in by_step.items():
        ordered = sorted(values)
        p95_index = max(0, round(0.95 * len(ordered)) - 1)
        summary[step] = {
            "n": len(values),
            "min": round(ordered[0], 4),
            "median": round(statistics.median(ordered), 4),
            "p95": round(ordered[p95_index], 4),
            "max": round(ordered[-1], 4),
        }
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--runs", type=int, default=20)
    parser.add_argument("--label", required=True)
    parser.add_argument("--no-warmup", action="store_true",
                        help="skip the warm-up request (use when measuring a cold start)")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    if not args.no_warmup:
        opener = urllib.request.build_opener()
        seconds, _, _ = timed(opener, f"{base_url}/health")
        print(f"warm-up /health: {seconds:.3f}s (not counted)")

    rows = []
    for run in range(1, args.runs + 1):
        rows.extend(one_exercise(base_url, run))
        print(f"run {run}/{args.runs} done")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = ROOT / "evidence" / "benchmarks" / f"{args.label}-{stamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "requests.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run", "step", "status", "seconds"])
        writer.writeheader()
        writer.writerows(rows)

    summary = summarize(rows)
    score_times = [r["seconds"] for r in rows if r["step"] == "submit decision 3 + score page"]
    result = {
        "label": args.label,
        "base_url": base_url,
        "utc_time": stamp,
        "runs": args.runs,
        "answers": ANSWERS,
        "warm_up": not args.no_warmup,
        "nfr01_limit_seconds": NFR01_LIMIT_SECONDS,
        "nfr01_score_displays_under_limit": sum(t < NFR01_LIMIT_SECONDS for t in score_times),
        "nfr01_score_displays_total": len(score_times),
        "steps": summary,
    }
    (out_dir / "summary.json").write_text(json.dumps(result, indent=2))

    print(f"\nSaved to {out_dir.relative_to(ROOT)}")
    print(f"{'step':34} {'n':>3} {'median':>8} {'p95':>8} {'max':>8}")
    for step, s in summary.items():
        print(f"{step:34} {s['n']:>3} {s['median']:>8.3f} {s['p95']:>8.3f} {s['max']:>8.3f}")
    print(f"\nNFR-01: {result['nfr01_score_displays_under_limit']} of "
          f"{result['nfr01_score_displays_total']} score displays under {NFR01_LIMIT_SECONDS:.0f} s")


if __name__ == "__main__":
    main()