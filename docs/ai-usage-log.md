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
