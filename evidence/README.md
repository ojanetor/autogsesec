# Evidence

Dated, versioned evidence for AutoGSESec. Every folder here was produced by a
script in `scripts/`, so any result can be regenerated and compared.

| Folder | Produced by | Contents |
|--------|-------------|----------|
| `runs/<label>/` | `python scripts/collect_evidence.py --label <label>` | `manifest.json` (commit, tag, Python version, every package version, UTC time), `tests.txt` and `tests-junit.xml` (full test report), `score_distribution.txt` (all 64 sc01 answer paths), `known_answers.md` (expected vs actual for hand-computed cases) |
| `benchmarks/<label>-<UTC time>/` | `python scripts/benchmark.py --base-url <url> --runs <n> --label <label>` | `requests.csv` (every timed request), `summary.json` (median, 95th percentile, max per step; NFR-01 count) |

Labels name the release and the environment, for example `v0.3.0-codespace`,
`render-warm`, `render-cold`.

Screenshots for course submissions are not stored here; the text and CSV
records above are the source they are taken from.