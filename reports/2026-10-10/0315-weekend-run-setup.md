# Weekend run: built and started

## Request

Divit's WEEKEND RUN prompt (2026-10-10), verbatim in `plan/weekend-run.md` ("Divit's prompt (verbatim, 2026-10-10)").

## Actions and results

- `ops/schedule/weekend_run.sh`: the loop. caffeinate -dimsu for its lifetime; headless Claude Code (`CLAUDE_CONFIG_DIR=~/.claude-b`, `fastMode` false) with the prompt "Continue the weekend run per plan/weekend-run.md". The Webflow MCP is not loaded (`--strict-mcp-config`, `ops/schedule/weekend.mcp.json` has DataForSEO only) and every Webflow tool is denied by name under the three server names, plus server-wide rules. Allowed: repo scripts, `ops/sync.sh`, read-only git, the AlsoAsked puller, WebSearch/WebFetch for writers' sources. Smoke test: the headless session saw no Webflow tool.
- Limits: on a session-limit exit it sleeps to the reset time in the message (+2 min, at most 5 h), else 20 min; stops for good on a weekly-limit message, any paid/extra-usage message, or 7 continuous hours limited. Parser tested on 6 message shapes.
- Stop: `touch ~/emergent-hubs/STOP` (after the current page); also stops when both queues are exhausted, after 6 failed iterations, 3 iterations without a commit, or about 3 hours of render waits.
- Locks and audits: waits while `ops/guards.py held` shows any lock; holds the `weekend` lock while a session runs; keeps 08:20-09:45 local free for the 09:00 live audit (stashes any stray edit, warns if no audit ran); pauses up to 45 min when the live "Last Published" stamp differs from the last audited one, so the publish watch's audit can run.
- `ops/weekend.py`: the state machine on top of `ops/ship.py` (autofix -> writer -> check -> images -> batch review -> one rework -> ready; a stage failed twice stops the page, `tick` parks it with the reason). Commands: init, next, add-new, aa (AlsoAsked with the 300-credit weekend cap and 2 per page), wait-render, commit (one page per push, under a git lock), tick (park, readiness board, position, a report every 10 finished pages), block-new/unblock-new.
- Rework batches (`plan/batches/wk-rework-*.txt`): written pages not live, held, parked or in Webflow: LP 13, Auto 4, SurveyQuiz 9, Form 132. New pages: canary of 3 per hub through review before more claims.
- First `next` run here: serial-comma autofix on 3 LP pages (punctuation only), 4 LP writer briefs. Loop started at 03:12 IST; iteration 1 running.

## Numbers

158 rework pages queued; new-page queues LP 92, Auto 64, SurveyQuiz 93, Form 71. AlsoAsked credits used this weekend: 0 of 300. DataForSEO budget 600 of 600 today.

## Decisions

- Built on `ops/ship.py` (DECISIONS 2026-10-08 combined pass; 2026-10-07 one review, one rework) rather than a new pipeline.
- Held pages left out by slug (DECISIONS 2026-10-09) and any spec with a Webflow item ID.
- Writers may run ad-hoc Python (FAQ embeds are built in Python, page-writer step 6); no Webflow credential exists in the environment and the Webflow MCP is not loaded.
- AlsoAsked only through `weekend.py aa` so the 300/2 caps are enforced in code.
- **The staging canary happens Monday before anything publishes.**

## Files changed and commits

ops/weekend.py, ops/schedule/weekend_run.sh, ops/schedule/weekend.mcp.json, plan/weekend-run.md, plan/batches/wk-rework-*.txt, status/weekend-run.json, RUNBOOK.md section 7. Commits 0feb2af, 23472f5, 2268182, 4c0709f, 24a698d.

## Webflow calls

None.

## Not done

- **New pages are held** (`block_new` in status/weekend-run.json): the DataForSEO MCP is not authenticated in `~/.claude-b`, and writers need the live SERP. The rework phase does not need it.

## Open questions for Divit

- To unlock new pages: run `CLAUDE_CONFIG_DIR=~/.claude-b claude` in ~/emergent-hubs, `/mcp`, authenticate dataforseo, then `.venv/bin/python3 ops/weekend.py unblock-new`. Default: rework only this weekend (158 pages likely use the remaining weekly usage anyway).
- Please confirm extra usage (paid credits) is off for this account; the loop stops if a message mentions it but cannot read the account setting.
