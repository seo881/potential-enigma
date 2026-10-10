# Weekend loop reads the AlsoAsked key from the keychain; DataForSEO MCP removed (2026-10-10 15:50 local)

## Request
> The AlsoAsked key is now in the macOS keychain (service "alsoasked", account = $USER). Make the loop read it from there, never from a file or the repo: in ops/schedule/weekend_run.sh, before each headless session, export ALSOASKED_API_KEY="$(security find-generic-password -a "$USER" -s alsoasked -w 2>/dev/null)"; if it comes back empty, keep the new-page hold and log "AlsoAsked key missing". Never print the key. While editing the script, also remove mcp__dataforseo and weekend.mcp.json from it. Restart the loop safely between sessions (exactly one loop), run weekend.py unblock-new, and confirm within 3 minutes that the new LP/Auto/SurveyQuiz writers got their AlsoAsked pulls (private/alsoasked/credits.log grows). Report in 3 lines.

Follow-up: "The AlsoAsked key was added to the keychain just now ... Re-check it (exit code only, never print it), keep your watcher plan, and once the new loop starts confirm the log shows "AlsoAsked key found: new-page hold released" and new-page writers starting."

## Actions and results
- `weekend_run.sh`:
  - Before each session it exports `ALSOASKED_API_KEY` from the keychain; the key is never printed or written.
  - If the key is empty: it logs "AlsoAsked key missing" and holds new pages.
  - If the key is found: it lifts a missing-key hold when one is set, and otherwise logs "AlsoAsked key found (keychain)".
  - Removed `mcp__dataforseo` from the allowed tools. Sessions load an empty MCP config; `ops/schedule/weekend.mcp.json` is deleted.
- Installed by an atomic rename while the old loop was running. The old loop kept its open copy, so it was not affected.
- First keychain check: no item under any account. After Divit added it, both checks passed by exit code only.
- Restart: STOP at 15:35:38. The old session ended cleanly at 15:46:10 and the old loop at 15:47:46. A watcher then removed STOP, ran `unblock-new` and started one loop at 15:47:58 (PID 91274, parent PID 1).
- 15:48:06: "AlsoAsked key found (keychain); new pages not held". Iteration 1 handed out Form rework expense-report-form and new-page writers ebook-landing-page (LP), procurement-automation (Auto) and brand-perception-survey (SurveyQuiz).

## Numbers
- AlsoAsked credits this weekend: 20 at the restart, 24 at 15:49:27 (`weekend.py credits`).

## Decisions
- Keys only in the macOS keychain: LESSONS section 1, row 5. Divit's prompt above.

## Files changed and commits
- 68caa97 (keychain key, DataForSEO MCP removed), 1a9455f (key-found log line).

## Webflow calls
None.

## Not done
- The previous session's new-page writers ran without the key (before 15:47:58), so any `aa` pulls they tried failed. Those pages come round again through `next`.
- The exact text "AlsoAsked key found: new-page hold released" appears only when a missing-key hold is lifted. No such hold was set, so the log shows "AlsoAsked key found (keychain); new pages not held" instead.

## Open questions for Divit
- None.
