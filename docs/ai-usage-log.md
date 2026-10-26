# AI Usage Log — AutoGSESec

Running record of every AI-assisted task in this project, kept in the
repository so it is versioned with the work it describes. Add an entry at the
end of every work session that used AI.

**Tool:** Claude (Anthropic), cited as Anthropic (2026). Other tools are named where used.
**Author:** O. Anetor. Every entry's "Decision" and "How I verified" columns are mine.

## How I decide whether to accept AI output

1. **Traceable:** the change serves a named requirement (FR or NFR) or a logged issue.
2. **Explainable:** I can explain what each changed line does before I commit it.
3. **Verified independently:** tests pass in my own Codespace *and* in both CI jobs (SQLite and Postgres); for scoring and mapping content, I check values by hand against the mapping file or the NIST and MITRE sources.
4. **Within constraints:** no paid services, no personal data, no proprietary AeroVect data, no exploitation detail.
5. **Honest in reporting:** AI-found results are labeled as such, and nothing is claimed as validated that I have not checked.

## How I work with AI

- I type or paste every change into the Codespace editor and commit it myself. I declined to give the AI push access to the repository.
- The AI reads the public repository to check its suggestions against the real files.
- I run every test, benchmark, and live check myself and give the output back for analysis.

---

## Hard Stop 4 (October 12–26, 2026)

Citation: Anthropic. (2026). *Claude* (October 26 version) [Large language model]. https://claude.ai

### Task log

| Date | Task | What the AI did | What was done and decided | How it was verified | Outcome |
|---|---|---|---|---|---|
| Oct 2026 | Scoring engine | Edited `engine/scoring.py` and its tests from my rules | Set the rules: correct 2, partial 1, incorrect 0; readiness bands at 80% and 50%; gaps ordered Immediate, Short-term, Long-term. Asked for whole-number comparison so boundary scores can't flip on rounding | Hand-computed 7 known-answer cases, including both boundaries; 64-path and 10-run tests; both CI jobs green | Accepted after review; pull request #5 (Oct 18) |
| Oct 2026 | After-action report | Edited `engine/report.py` and the report page | Chose to list each control once, at its earliest timeline, grouped by family | Known-answer cases compare gap order and recommended controls; report page test | Accepted; pull request #6 |
| Oct 2026 | Security and production settings | Edited CSRF protection, secure cookies, and the startup check that refuses to run without a secret key | Required that production fail closed rather than use a fallback key | Security tests; the first Render deploy stopped with "SECRET_KEY must be set in production", which showed the check works | Accepted; pull request #6 |
| Oct 2026 | Render deployment setup | Gave step-by-step setup for the Render service and gunicorn | Chose the free tier ($0 budget) and one worker | Site loaded; `/health` responded | Accepted, but see the temporary SQLite row |
| Oct 2026 | Benchmark and evidence scripts | Edited `scripts/benchmark.py` and `scripts/collect_evidence.py` | Required dated folders, a manifest with every package version, and a recorded label for every run | Ran both in my Codespace; compared output with test results | Accepted; benchmark later needed a fix (Oct 25) |
| Oct 2026 | Live site running on temporary SQLite | Explained why `/health` showed `sqlite`: no database address was set, so the app fell back silently. Drafted a startup check and a test as a corrective measure | Found the problem by checking `/health` on the live site. Set the Render database address. Decided production must refuse to start without it | `/health` now shows `postgresql`; new configuration test; both CI jobs green | Accepted; pull request #8. The silent fallback came from configuration code |
| Oct 2026 | Benchmark rejected with HTTP 400 on Render | Diagnosed the cause from my traceback: the HTTPS form check requires a Referer header, and the script sent none. Fixed the script | Confirmed that real users were safe by clicking through the live site in a browser to the report | Browser reached the report; fixed script got 20 of 20 under 3 s | Accepted |
| Oct 2026 | Warm and cold benchmarks | Suggested a run design for warm and cold; cold runs only after the site had been idle | Chose twenty warm runs and two cold runs instead of one; ran every benchmark | Two clean cold starts agree within 0.02 s (32.38 s and 32.39 s) | Accepted |
| Oct 2026 | Live probes | Suggested three probes | Ran probes on the live site: form without token, unknown scenario, report without a session | Got 400, 404, 302 as expected | Accepted |
| Oct 2026 | Evidence index, changelog, risk log, environment notes, README | Edited the text from the evidence files | Accepted corrections from edit; checked every number against `summary.json`, `known_answers.md`, and `tests.txt` | Numbers match the files | Accepted; tag `v0.3.0` and evidence record; published the GitHub Release |
| Oct 2026 | Hard Stop 4 package | Edited the package and compared content from the repo evidence and feedback | Kept full scope. Split open items across Assignments 9 and 10. Rechecked package against feedback and repo | Compared every number with the evidence files | Accepted with additional changes |

### AI suggestions I rejected or corrected

| AI suggestion or output | What I did | Why |
|---|---|---|
| Delivering code changes as a zip file | Rejected; switched to copy-and-paste into the editor | My laptop is at capacity, and I want to make each change myself |
| Editing files with terminal heredoc blocks | Rejected | They dropped edits; pasting into the editor is more reliable |
| Giving the AI push access to the repository | Declined | I make every change hands-on so I understand it |
| Referring to requirements and issues by ID codes in instructions | Corrected: asked for plain names | So I don't have to keep looking up earlier tables |
| First list of open items after Hard Stop 4 | Corrected: asked for re-verification against the repo, which found four missed items (three new controls, recruiting reviewers, clearing test data, recreating the database) | Accuracy |
| Package wording that reported open items only in Assignment 9 | Corrected to Assignments 9 and 10 | Matches my actual plan |
| Longer wording about the supervisor's response to my midpoint questions | Replaced with "Student chose to keep the full scope." | The decision was mine |
| Architecture rows saying "Not started" for planned features | Corrected to show the scheduled week | Conflicted with my no-cuts decision |
| Naming control PS-3 "Personnel Termination" | Correction pending: PS-3 is Personnel Screening and PS-4 is Personnel Termination; the correct control will be confirmed against the NIST catalog before the Initial Access scenario is written | Every control must be verifiable |

### Process slips (all caught before submission)

| What happened | How it was caught | Status |
|---|---|---|
| Configuration fell back silently to SQLite in production | Checked `/health` on the live site | Fixed; production refuses to start without the database address |
| Benchmark script sent no Referer header | HTTP 400 on the first live run | Fixed; real users never affected |
| Several pasted files were cut off partway (`report.py`, `collect_evidence.py`, this log); a missing function caused an ImportError | Line counts with `wc -l`; failing tests | Re-pasted; line count checked after every paste |
| Pull request #9 merged after one commit, before the rest of the work was in | Next commits needed a new pull request | Later work went into pull request #10; its redeploy is why one "cold" run was not cold |
| One commit's message does not match its contents (it holds the benchmark fix and warm data) | Review of history | Left as is, because rewriting published history is worse; recorded here |

### Statement

Every requirement, threshold, scoring rule, scope decision, and interpretation in Hard Stop 4 is mine. The AI drafted and edited code and text, diagnosed errors from output I gave it, and checked the repository for consistency. I verified each change by hand calculation, tests on two databases, live checks on the deployed site, or comparison with the evidence files. Where AI output has not yet been independently validated (rubric mappings, time estimates), the package says so.