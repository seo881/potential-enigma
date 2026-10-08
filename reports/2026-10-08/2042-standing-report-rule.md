# Standing work-report rule and three backfilled reports

## Request
> Read CLAUDE.md, DECISIONS.md (2026-10-08), docs/HANDOVER_2026-10-08.md, logs/form.md, plan/rework-2026-10-08.md, plan/template-edits-2026-10-08.md and audit/feedback-2026-10-08.md. No Webflow calls.
>
> PART 0: STANDING REPORT RULE
> Add this rule to CLAUDE.md and RUNBOOK.md section 6, plus a DECISIONS line under 2026-10-08:
> After every task Divit gives, write a work report to reports/YYYY-MM-DD/HHMM-<slug>.md with these sections:
> - Request: Divit's prompt, verbatim.
> - Actions and results: each command or change made, and its outcome.
> - Numbers: every count, total and measurement produced.
> - Decisions: each choice made, the option chosen, and the rule, file or source it follows (cite DECISIONS.md, HUB_RULES, a URL or a data file).
> - Files changed and commits (SHAs).
> - Webflow calls: type, item or element IDs, before and after values, rollback.
> - Not done: anything skipped and why.
> - Open questions for Divit.
> Add a line to reports/INDEX.md (newest first: date, slug, one-line summary, commit SHA).
> The repo is PUBLIC: never put keys, tokens, raw API responses, SERP or AlsoAsked question text, or anything from private/ or .cache/ in a report; reference file paths instead.
> Commit and push via ops/sync.sh, then reply in chat in under 15 lines: summary, report path, SHA.
>
> Backfill three reports from the commits and logs:
> 1. The rules pass (commit 9ea2d96).
> 2. The registration-form update payload: built, NOT sent (13 fields, ops/out/registration-form.update.payload.json).
> 3. Today's interrupted sessions: nothing was written; request ID req_011CfpwmUnep1U7FjsxFjw1K.
> Then STOP.

## Actions and results
- Read the seven files listed, plus RUNBOOK.md and `ops/sync.sh`.
- Added the rule to CLAUDE.md (non-negotiables), RUNBOOK.md (section 6, new subsection "Work report after every task") and DECISIONS.md (2026-10-08, first line). Pushed as 8bbe3f2.
- Gathered backfill facts read-only: `git show --stat 9ea2d96`, the commit's diffs of `qc/qc_hub.py`, `rules/style_rules.json`, `ops/hubctl.py`, `ops/table.py`; field names, target IDs and `isDraft` of the update payload (values not read into any report); `hubctl status` for registration-form (state `reviewed`); latest entry in each `logs/*.md`.
- Wrote three backfilled reports, this report and `reports/INDEX.md`.

## Numbers
- Files read: 9. Rule edits: 3 files. Reports written: 4. Index lines: 4.
- Backfill facts: see each report (rules pass: 199 files, +1,074/-334, 184 specs, 9 QC checks, 183-page rework plan; payload: 13 fields, 1 item).

## Decisions
- Report times use local time (IST) as the filename HHMM. Backfills are named for when the work happened: rules pass 1956 (commit time of 9ea2d96), payload 1954 (payload file time); the interrupted-sessions report has no known time, so it uses the time it was written (2042).
- INDEX SHA is the commit of the work described; the rule edits were committed first (8bbe3f2) so this report can cite them. The interrupted-sessions line has no SHA (no commit).
- Backfilled "Request" sections say the prompt was not recorded verbatim rather than reconstructing it (rule: Request is verbatim).
- Payload field names are listed (they are CMS slugs, already public in `config/collections.json`); field values are not (rule: no raw payloads in a public report).

## Files changed and commits
- 8bbe3f2: `CLAUDE.md`, `RUNBOOK.md`, `DECISIONS.md`.
- Report commit (SHA in `reports/INDEX.md` history and the chat reply): `reports/INDEX.md`, `reports/2026-10-08/1956-rules-pass.md`, `reports/2026-10-08/1954-registration-form-update-payload.md`, `reports/2026-10-08/2042-interrupted-sessions.md`, this file.

## Webflow calls
None.

## Not done
Nothing in the request was skipped. Stopped after the backfill, as asked.

## Open questions for Divit
None new; the backfilled reports carry the open questions from the rules pass and the payload.
