# DataForSEO retired, AlsoAsked for PAA; weekend run new-page phase released (2026-10-10 15:14 local)

## Request
> DECISION (Divit, 2026-10-10): DataForSEO is retired. AlsoAsked replaces it for People Also Ask; no live SERP pull is required anymore. Fast, the weekly window closes in about 2 hours.
>
> 1. Remove every DataForSEO dependency:
>    - QC F1 no longer requires a DataForSEO capture: a page passes F1 with an AlsoAsked pull (private/alsoasked/<slug>.json); top-10/intent context comes from the Semrush workbook and Wave 3 SERP data already in private/.
>    - Update qc/qc_hub.py and its golden tests, HUB_RULES (rule 5 and the FAQ section), RUNBOOK step 1b, the writer brief, and plan/weekend-run.md (delete step 0 and the DataForSEO writer step; keyword ideas come from the Semrush workbook).
>    - Remove mcp__dataforseo from .claude/settings.json.
>    - DECISIONS line. LESSONS line: "Before any unattended run, preflight every external dependency it needs (logins, tools, credits) and fail at start, not mid-run."
> 2. QC all written specs; report only the count of pages whose F1 result changed.
> 3. Restart the weekend run:
>    - .venv/bin/python3 ops/weekend.py unblock-new; rm -f STOP.
>    - If a weekend_run.sh process is still alive, do NOT start a second one. Otherwise start it with nohup bash ops/schedule/weekend_run.sh >/dev/null 2>&1 &.
>    - Within 5 minutes, confirm in the log that new LP, Automation and SurveyQuiz pages are being claimed (3-page canary per hub).
> 4. Report in 5 lines, then /exit.

## Actions and results
- QC F1 (`qc/qc_hub.py`): now P1 only when the page has no AlsoAsked pull. A DataForSEO capture is neither required nor sufficient.
- F2 without a capture: each FAQ source must be recorded. `paa`/`alsoasked` provenance is left to PAA gate PA1. `secondary`/`keyword` refs must be Semrush secondaries. `definition` must define the primary. `related` is rejected because there is no capture to check it against.
- Pages that have a legacy DataForSEO capture keep the existing F2/F3/F5 checks against it.
- F6 (data age) now reads the AlsoAsked pull's fetch date. The old version asked for a DataForSEO re-pull, which is no longer possible.
- `hubctl brief`: removed the "pull the live SERP (DataForSEO)" instruction. Wave 3 pages are pointed to the Wave 3 SERP data.
- Golden tests: new case kind `qc-f1` plus 4 guarded cases (f1-aa-only, f1-no-aa-legacy-serp, f1-no-sources, f1-both). Suite: 95 cases, 0 regressions. The 4 open misses were already open before this change.
- Docs: HUB_RULES rule 5 and the FAQ section, RUNBOOK step 1b (plus the budget row and the worktrees line), page-writer brief steps 0, 1 and 6, the hub-content skill, and `plan/weekend-run.md` (step 0 deleted; the new-page writer step now gets keyword ideas from the Semrush workbook).
- `.claude/settings.json`: removed `mcp__dataforseo` from the allow list and from the note.
- Weekend run: ran `weekend.py unblock-new` and `rm -f STOP`. weekend_run.sh was still alive (PID 15693), so no second loop was started.

## Numbers
- QC over all 192 specs, before and after: F1 result changed on **0 pages**. Every spec with an FAQ that QC checks already has an AlsoAsked pull.
- Running `weekend.py next` claimed the 3-page LP canary: ebook-landing-page, mobile-landing-page, video-landing-page.

## Decisions
- DataForSEO retired: DECISIONS 2026-10-10 (line added). HUB_RULES rule 5 and section 5 FAQ.
- Lesson on preflighting external dependencies: LESSONS section 5, 2026-10-10.
- One loop only: CLAUDE.md, and this request.

## Files changed and commits
- 150eec0: qc/qc_hub.py, tests/golden/run.py, tests/golden/cases.jsonl, ops/hubctl.py, rules/HUB_RULES.md, RUNBOOK.md, .claude/agents/page-writer.md, .claude/skills/hub-content/SKILL.md, plan/weekend-run.md, .claude/settings.json, DECISIONS.md, LESSONS.md.
- 5e4c5c6: new-page phase released (weekend.py). 4b4c433: claimed 3 new LP pages.

## Webflow calls
None.

## Not done
- `ops/schedule/weekend_run.sh` still lists `mcp__dataforseo` in its allowed tools and loads `ops/schedule/weekend.mcp.json` (DataForSEO only). Editing a bash script while it is running is unsafe, so neither was changed. Both are harmless: no step calls DataForSEO any more. Recommended: remove both the next time the loop is stopped.
- `plan/serp.py`, the `hubctl serp-*` commands and `dataforseo_daily_cap` stay in place for reading the legacy captures. Nothing calls DataForSEO.
- Automation and SurveyQuiz canaries: `weekend.py next` stops at the first hub that has work. Automation and SurveyQuiz get their 3 pages each once the LP writers move their pages past the writer stage, so they are not claimed yet.
- Stopping the loop's 20-minute render wait early was denied by the permission check. The loop picks up the LP pages when that wait ends.

## Open questions for Divit
- None. Default: strip DataForSEO from weekend_run.sh at the next restart.
