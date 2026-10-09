# Live audit built (Part 1): Layer A and B, auto-fix path, ledger, golden cases, daily job

## Request
Divit (2026-10-09), PART 1 of the live-audit prompt: "BUILD THE LIVE AUDIT exactly as docs/LIVE_AUDIT.md specifies", steps 1-8 (Layer A with screenshots and drift; hubctl live-audit with Layer A then Layer B; auto-fix for P0/P1 on child CMS items with the doc's 5 steps and --dry; ledger, day files, report with digest first, hubctl live-rollback; golden test cases; ops/github/live-audit.yml; the daily schedule on this Mac; a dry test against staging). Full prompt in the session; Parts 2 and 3 wait for "staging published" and "live".

## Actions and results
1. **Layer A.**
   - `ops/live_audit.mjs` reuses `ops/verify_launch.mjs`, refactored into exported `checkPage`/`checkHub`.
     - It adds the T1 check you asked for, that the older chip script does not overwrite the prompt: the box must still hold the chip text 1.2 s after the click.
     - It renders each page in Chromium (Playwright 1.48.2, pinned in `ops/package.json`) and records visible and full text, robots, links with HTTP status, images (loaded, size, alt) and JSON-LD.
     - It also measures the use-case SVG ratio and takes 1440 px and 390 px full-page screenshots into `.cache/live/DATE/`.
   - `ops/live_audit.py` turns that into findings, covering every check in the doc:
     - HTTP status, canonical, noindex and sitemap;
     - title and meta exact against the spec, with QC's limits;
     - every spec field rendered exactly once;
     - stray template text and empty sections;
     - character hygiene on visible text, alt, meta and JSON-LD;
     - links (internal 200, hub link in the FAQ exactly once, no non-live targets, external weekly);
     - images (format, WebP og:image, alt, 3:2);
     - scripts (T1, T2, T10, T5);
     - JSON-LD: it must parse, and the FAQPage must match the visible FAQ word for word.
   - **Drift:** a field not rendered as approved is classified with a CMS read (`live-audit drift`). It is drift (reported, never overwritten) only when the CMS differs from the spec while the spec equals our last verified write.
2. **`hubctl live-audit`** takes `--since-publish | --all | --urls | --set launch`, plus `--base`, `--dry`, `--external` and `--no-shots`.
   - Layer A runs first. Layer B pages are picked by the content hash at the last full read: the first audit after publish, any change since, or anything Layer A flagged.
   - It writes batches of 4 pages (`.cache/live/DATE/layerB-N.md`), each with the rules pack, rendered text and screenshots. `live-audit record` merges each reviewer's JSON.
3. **Auto-fix**, the doc's 5 steps:
   - **Code-computable fixes** (`live-fix apply`): zero-width and control characters, broken entities, double spaces, curly quotes, UK spellings, repeated words, links to non-live pages, image format.
   - **Writer fixes** (`live-fix brief`) cover the other auto-allowed fields.
   - **`live-fix prepare`** saves the before-value, then requires:
     - QC 0, gate 10/10 if the FAQ changed, and current images;
     - at most 10 fields;
     - never the slug or the primary keyword.
     It then builds the payload: update, item publish, read back.
   - **`live-fix verify`** checks the read-back, re-runs Layer A on that URL and, on failure, writes the rollback to send at once.
   - With `--dry`, nothing changes and would-fix items are listed.
4. **Ledger and reports:** `audits/live/LEDGER.md` (from `ledger.json`), per-page day files, and `reports/DATE/HHMM-live-audit.md` with the digest first. `hubctl live-rollback ISSUE [--done RESPONSE]` handles single rollbacks.
5. **Golden cases:** `tests/golden/cases.jsonl` and `tests/golden/run.py`.
   - Seeded with the 7 PA13 catches. They reference commit and question index, so no question text is copied into new files.
   - All 7 are "open" (the gate still misses them; the fixes are in the backlog under the rules freeze). The suite is green.
   - Every live-audit catch that QC passed is appended automatically.
6. **`ops/github/live-audit.yml`:** daily Layer A, GITHUB_TOKEN only, skipping a day the Mac already ran. Installed in Part 3.
7. **Schedule:** Claude Code's scheduler here is session-only (jobs end with the session), so I used launchd.
   - `~/Library/LaunchAgents/sh.emergent.live-audit.plist` runs daily at 09:00 (StartCalendarInterval) and is loaded with launchctl.
   - It calls `ops/schedule/live_audit_daily.sh`, which pulls, then skips if the tree is dirty or a lock is held (`ops/guards.py held`).
   - It then runs headless Claude Code under a session lock (`CLAUDE_CONFIG_DIR=~/.claude-b`, prompt `ops/schedule/live_audit_prompt.md`, `--permission-mode dontAsk`, allow-list in the script), logs to `~/Library/Logs/emergent-live-audit.log` and posts a macOS notification with the digest line.
   - RUNBOOK section 7 covers pause, resume and run now.
8. **Test:** a plumbing run on staging worked end to end, with 20 pages and 4 hubs. The pages 404 because staging isn't published yet, and that output was discarded.
   - It calibrated two rules: an empty Webflow paragraph is now P2, and the repeated-word check no longer crosses table cells.
   - **The full dry test is not run yet; it runs as soon as staging is published.**

## Decisions
- docs/LIVE_AUDIT.md and DECISIONS 2026-10-09 (live audit standing go); LESSONS rules 3 and 9.
- **Schedule:** launchd, because the native scheduler is session-only.
- **Allow-list width:** it includes Read/Glob/Grep/Agent, `Edit(specs/**)` and `Write(.cache/live/**)`, because Layer B reviewers and fix writers need them.
- **Webflow action limits:** `mcp__webflow__data_cms_tool` can only be allowed as a whole tool, so the action limits (list, update, item publish only) are enforced by the prompt and by hubctl writing only those payloads.

## Files changed and commits
- e37d24f: `ops/live_audit.mjs`, `ops/live_audit.py`, `rules/live_audit.json`, `ops/verify_launch.mjs`, `ops/hubctl.py`, `ops/guards.py`, `ops/schedule/*`, `ops/github/live-audit.yml`, `ops/package.json`/lock, `tests/golden/*`, RUNBOOK, docs/LIVE_AUDIT.md.

## Webflow calls
None.

## Not done
- **Step 8 dry test:** staging is not published yet (the launch URLs return 404 on emergent-sh.webflow.io).
- **Notification check:** not confirmed yet; it is part of the step 8 test.

## Open questions for Divit
None.
