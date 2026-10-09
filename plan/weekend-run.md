# Weekend run (Divit, 2026-10-10)

Every headless session of the weekend run starts here (prompt: "Continue the weekend run per plan/weekend-run.md"). Read this file, `CLAUDE.md`, `LESSONS.md` and `DECISIONS.md` (2026-10-09 and 2026-10-10), then do the work below. Code decides what comes next (`ops/weekend.py`); you do the agent work. The loop that starts you is `ops/schedule/weekend_run.sh`.

## Current position

<!-- position:start (written by ops/weekend.py tick; do not edit by hand) -->
Updated 2026-10-09 22:48 UTC. Started 2026-10-09T21:40:27+00:00.

| Phase | Hub | Pages | Stages |
|---|---|---|---|
| rework | LP | 13 | ready 13 |
| rework | Auto | 4 | ready 2, rework 2 |
| rework | SurveyQuiz | 9 | autofix 5, check 4 |
| rework | Form | 132 | autofix 132 |

New pages claimed this weekend: none.
Holds: none.
AlsoAsked credits this weekend: 0 of 300. Reports written: 1.
Next step: run `.venv/bin/python3 ops/weekend.py next` and do what it prints.
<!-- position:end -->

## Hard limits (Divit's prompt; never relaxed by a later session)

- **No Webflow tools at all** (no CMS, no sites, nothing) and no publishing. Repo work only. The loop does not load the Webflow MCP and denies every `mcp__webflow__*` tool by name; if any Webflow tool is ever offered, do not call it.
- Never touch the 20 live pages, the held pages (consultation-form, checkout-form, conference-registration-form, summer-camp-registration-form, contact-form, the 4 originals) or parked pages. `weekend.py init` left them out of every batch; never add them.
- **AlsoAsked: at most 300 credits this weekend, 1-2 per page**, only through `ops/weekend.py aa <url>` (it enforces both caps and calls `ops/alsoasked_pull.py`, which logs to credits.log).
- Never fast mode, never paid usage credits. When the weekly limit is reached the loop stops for good.
- Every page passes the full pipeline: QC TOTAL 0, PAA gate 10/10 (PA14, PA15 included), D1, D2, F9 (2-3 moat lines), explore CTA at most 34 characters (D3), serial commas (H3 autofix, punctuation only), batch review (up to 4 pages per reviewer), one rework, images rendered. **A page that fails a stage twice is parked with a reason, never forced** (`ops/ship.py` stops it; `weekend.py tick` parks it).
- Rules are frozen: never edit `rules/`, `qc/`, `ops/` code, templates or shared files. New findings go to `plan/backlog.md` (one line each).
- Public repo: no question text, SERP or AlsoAsked content in commits outside `specs/`, in reports or in fail reasons. Nothing from `private/` or `.cache/`.

## Work order

1. **Rework** the written, non-live, non-parked pages to the 2026-10-09/10 rules (batches `plan/batches/wk-rework-<dir>.txt`), hub order LP, Automation, SurveyQuiz, then Form: code autofixes the serial commas (punctuation only); one writer pass replaces PA14/PA15 FAQ items, rewrites the hero and how-to descriptions (D1/D2), adds 2-3 FAQ moat lines (F9), shortens explore CTAs over 34 characters, fixes the remaining A5/A6/C4 flags and writes the 4 chip prompts; then QC 0, gate 10/10, images re-rendered when the brief changed, batch review, one rework.
2. **New pages** from the planned queues, same hub order (`plan/batches/wk-new-<dir>.txt`). **Canary per hub:** the first 3 new pages of a hub complete the full pipeline, review included, before more of that hub are claimed (`weekend.py next` enforces it; if 2 of the 3 park, the hub is held). **The staging canary happens Monday before anything publishes** (every report says so).

## One session = up to 3 units, then exit

0. New pages need the live SERP from the `dataforseo` MCP. At session start, look for `mcp__dataforseo` tools (ToolSearch "dataforseo"). If there are none and `status/weekend-run.json` has no `block_new`, run `.venv/bin/python3 ops/weekend.py block-new "DataForSEO MCP not authenticated in ~/.claude-b"`; the rework phase continues, new pages wait. If the tools are there and `block_new` names DataForSEO, run `weekend.py unblock-new`. Never write a new page without its live SERP.
1. `git status`: if a previous session left uncommitted spec edits, read them; finish that page's step if the edit is complete, otherwise `git checkout -- <spec>` and let `next` hand the page out again.
2. Check the stop rules: if `~/emergent-hubs/STOP` exists, or the local time (`date`) is between 08:20 and 09:45 (the 09:00 live audit needs a clean tree and no lock), finish the page in hand, commit, tick, and exit.
3. `.venv/bin/python3 ops/weekend.py next` and do every line it prints (below). Then run `next` again, up to 3 units per session; then `weekend.py tick` and exit with a 3-line summary. Exit codes: 3 = both queues exhausted, 4 = STOP file: tick with `--final` and exit.

### What each line means

- `WRITER <batch> <url> brief <path>` (rework phase, first pass) and `WRITE-NEW <url>` (new page): one **page-writer** subagent per page, up to 4 in parallel, agent id `wk-w-<slug>` (rework) or `wk-n-<slug>` (new).
  - Rework writer prompt: follow the brief exactly (it is the one combined pass and lists the gate rejects, the allowed replacement sources, the open QC issues and the chip prompts); also fix the A5/A6/C4 flags that `hubctl qc <url>` reports; do not reword anything for serial commas (code did them); done when `hubctl ship-qc <url>` is TOTAL 0 and `hubctl paa <url> --spec` shows 10 items and no reject, then `hubctl state <url> qc_pass --by <id>`. If the brief offers fewer replacement questions than it needs and the page has no AlsoAsked pull this weekend, the writer may run `.venv/bin/python3 ops/weekend.py aa <url>` once.
  - New-page writer prompt: run `.venv/bin/python3 ops/weekend.py aa <url>` first (1 credit; `--fresh` once only if it returned no results), then the page-writer steps (DataForSEO SERP and keyword ideas, pack, plan, sources, copy, table, image brief, QC 0), with the 2026-10-09/10 rules (PA14, PA15, D1, D2, D3, F9), exactly 10 FAQ items gate-checked with `hubctl paa <url> --spec` (10 items, no reject), and `spec.chip_prompts` (exactly 4 strings, 60-220 characters, first person, one per chip in chip order); then `hubctl state <url> qc_pass --by <id>`.
  - Writers never commit, never edit rules or code, never quote FAQ questions in their summary. Each returns 3 lines: done or failed (reason in rule codes only), QC total, gate count.
  - After each writer returns: rework phase `hubctl ship-done <batch> <url> writer --by <id>` (or `--fail "<rule codes>"`); new page `weekend.py add-new <url> --by <id>` (or `--fail "<rule codes>"`). Then `hubctl usage-log <url> <tokens> --role writer --agent <id>`, `weekend.py commit <url> "writer pass"`, `weekend.py tick`.
- `REWORK <batch> <url> brief <path>`: the one rework, by a **different** page-writer (id `wk-rw-<slug>`), blocking findings only (the brief lists them); notes never trigger edits. Done at QC 0 and gate 10/10. Then `hubctl ship-done <batch> <url> rework --by <id>`, usage-log, commit, tick. `next` then re-checks, waits for the re-render and runs `hubctl ready`.
- `REVIEW <batch> <url> ...` (up to 4): one **page-reviewer** subagent for the group, id `wk-r-<n>` (n increasing; never an author of these pages). It reads each page cold (spec, `hubctl pack <url> --role reviewer`, the rendered SVGs in `images/<dir>/<slug>/`), severity from `rules/SEVERITY.md` only, and records each page with `hubctl review <url> <rubric.json> --by <id>` (add `--legacy` on a rework-phase page that already carries an earlier review: DECISIONS 2026-10-08, the batch review replaces it). Then per page `hubctl ship-done <batch> <url> review --by <id>`, `hubctl usage-log <url> <tokens/pages> --role reviewer --agent <id>`, commit, tick.
- `WAIT-RENDER <slugs>`: pages wait on the render Action (`.github/workflows/render.yml` renders on push and commits the images). Run `.venv/bin/python3 ops/weekend.py wait-render` (pulls every minute, up to 20 minutes; use a 10-minute Bash timeout and run it twice if needed), then `next` again. If still waiting, tick and exit.
- `EXHAUSTED` (exit 3): `weekend.py tick --final`, exit. `STOP` (exit 4): same.

### Commits and logs

- Every page step is committed and pushed by `weekend.py commit <url> "<step>"` (ops/sync.sh under a git lock), so a crash loses at most one page. Only the orchestrating session commits; subagents never do.
- `weekend.py tick` after every page: parks pages stopped twice (reason recorded), regenerates `status/readiness.md`, updates the position above, writes a report in `reports/` every 10 finished pages (done, parked with reasons, tokens per page, credits used) with its line in `reports/INDEX.md`.
- The loop logs to `~/Library/Logs/emergent-weekend-run.log`.

## Divit's prompt (verbatim, 2026-10-10)

> WEEKEND RUN. Use the remaining weekly usage until the weekly limit is hit, surviving 5-hour session limits. git pull first; read CLAUDE.md, LESSONS.md, DECISIONS.md (2026-10-09, 2026-10-10), RUNBOOK section 7 and plan/backlog.md.
>
> HARD LIMITS:
> - NO Webflow tools at all (no CMS, no sites, nothing). No publishing. Repo work only.
> - Do not touch the 20 live pages, the held pages or parked pages.
> - AlsoAsked: at most 300 credits this weekend, 1-2 per page, logged in credits.log.
> - Never use fast mode or paid usage credits; when the weekly limit is reached, stop for good.
> - Every page passes the full pipeline: QC TOTAL 0, PAA gate 10/10 (incl. PA14/PA15), D1, D2, F9 (2-3 moat lines), the explore_cta limit of 34 characters, serial commas (H3 autofix), batch review (4 pages per agent), one rework, images rendered. A page that fails twice is parked with a reason, never forced.
>
> WORK ORDER:
> 1. REWORK the written, non-live, non-parked pages to the 2026-10-09/10 rules: replace PA14/PA15 FAQ items, rewrite the hero and how-to descriptions (D1/D2), add 2-3 FAQ moat lines (F9), shorten CTAs over 34 characters, autofix the serial commas (punctuation only), and fix the remaining A5/A6/C4 flags. Then QC 0, gate, review, and re-render images if drawn text changed. Hub order: LP, Automation, SurveyQuiz, then Form.
> 2. NEW PAGES from the planned queues, same hub order. Canary per hub: the first 3 new pages of each hub complete the full pipeline, including review, before more than 3 more of that hub are claimed. Every report notes that the staging canary happens Monday before anything publishes.
>
> RESILIENCE (build it, then start it):
> - ops/schedule/weekend_run.sh:
>   - runs caffeinate -dimsu for its lifetime;
>   - loops headless Claude Code (CLAUDE_CONFIG_DIR=~/.claude-b, no fast mode) with the prompt "Continue the weekend run per plan/weekend-run.md". Allowed tools: the repo scripts, git via ops/sync.sh, and ops/alsoasked_pull.py. Disallowed: every mcp__webflow__* tool, explicitly.
> - Each iteration claims pages via hubctl, commits per page and pushes via ops/sync.sh, so a crash loses at most one page.
> - Limits:
>   - On a session-limit exit, sleep until the reset time if the message gives one; otherwise sleep 20 minutes and retry.
>   - If it is still limited after 7 continuous hours, or the message says the weekly limit is reached, stop for good.
> - Stop switches:
>   - touching ~/emergent-hubs/STOP stops it cleanly after the current page;
>   - it also stops when both queues are exhausted.
> - Respect ops/guards locks; if the 09:00 live audit or the publish watcher holds the lock, wait.
> - Write plan/weekend-run.md (rules, work order, current position) so every fresh session resumes exactly where the last one stopped.
> - Logging:
>   - ~/Library/Logs/emergent-weekend-run.log;
>   - a short report in reports/ every 10 pages (done, parked with reasons, tokens per page, credits used);
>   - status/readiness.md regenerated after each page.
>
> Start it with nohup so it survives this terminal closing. Confirm the script path, the PID, how to check progress (tail the log) and how to stop it (touch STOP). Then end this session.
