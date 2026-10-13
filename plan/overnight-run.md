# Overnight run, 2026-10-13 to 2026-10-14 (Divit, ruling 17)

Account A alone; B is stopped. Nothing ships overnight: no Webflow calls at all. The headless loop is `ops/schedule/overnight_run.sh` (CLAUDE_CONFIG_DIR=~/.claude-b, account A's config dir).

## Override (recorded)
- `.hub` = `A:LP,Form,Auto,SurveyQuiz` from 2026-10-13 ~18:20 UTC (was `A:LP`). Temporary, for the canary and tonight's run only. Restore `A:LP` before B restarts (the previous value is in `.cache/hub.before`).
- B-held pages are never touched: hubctl refuses them, and the loop skips any page whose status entry carries a B hold.

## Gate: the canary first (ruling 15)
- 3 pages from different hubs: hipaa-release-form (Form, writer A-w-47), customer-service-automation (Auto, A-w-48), post-event-survey (SurveyQuiz, A-w-49).
- Full review by A-r agents that wrote none of them.
- Pass = QC 0 on the first run and 0 blocking findings, 3 of 3. Otherwise fix the causes and re-canary. **No scaling before 3/3.**

## Each iteration (headless session, account A)
You are the orchestrator for one iteration. Read CLAUDE.md, LESSONS.md (top), DECISIONS 2026-10-13 (rulings 12-17), docs/PREVENTION.md. Then:
1. `git pull --rebase`; `.venv/bin/python3 ops/overnight.py next`. It lists the work in plan order. Do the first non-empty groups, with at most **10 writer agents at once**.
2. **LP reworks** (A's 10): a page-writer agent `A-w-<n>` per page fixes the **blocking findings only** (legacy rework rules in its instructions; the page's review lock applies). Then `hubctl images <url> --by A-coord`, `hubctl ready <url> --by A-w-<n>`. No second review; notes ship.
3. **New pages, ruling 15 pipeline only:** `hubctl claim <HUB> 1 --by A-w-<n>` (from the top of plan/queue-ranked.txt; claim refuses held or infeasible pages), then `ops/skeleton.py build <url> --by A-w-<n> [--fresh]` (refusal = not writable: `hubctl release <url> --by A-coord --note "skeleton short"` and move on), `ops/skeleton.py pack <url>`, then spawn one `page-writer` agent `A-w-<n>` per page with: "Write <url> on the ruling 15 pipeline (spec pipeline r15). Pack: .cache/packs/<slug>.r15.md." The writer finishes at `state qc_pass`.
4. **Images:** `hubctl images <url> --by A-coord` for each qc_pass page (renders locally, 6 images + contact sheet). Read the contact sheet: one hero, readable text, numbers that add up, story matching the tab copy.
5. **Review:** spawn `page-reviewer` agents `A-r-<n>` (up to 4 pages each, never a page they or their writer id wrote). `hubctl review` records it. Blocking -> `rework`: one rework by a **different** `A-w-<n>` (blocking findings only), QC 0, `hubctl images`, `hubctl ready`. Nothing past `reviewed`.
6. Commit after every page stage: `bash ops/sync.sh "<stage>: <url> ..." <spec> <status file> <images dir>`. Log tokens with `hubctl usage-log`.
7. Never: any Webflow tool, a site or item publish, a page with a B hold (hubctl refuses), a rule or QC change, an AlsoAsked pull outside `weekend.py aa`, a Semrush call (results land from the separate fetch; `ops/semrush_questions.py derive` only).
8. End the iteration after about 3 hours of work or when `overnight.py next` is empty. Write one line to plan/backlog.md if anything blocked you.

Skipped on purpose: the tranche-1 pages that reach 10 (attendance-form, culture-survey, automated-loan-processing-system, content-approval-workflow, shipping-automation) are held by B as split writes. Ruling 17 says never touch B-held pages, so they wait for B or for Divit to release them.

## Commands (Divit)
- start: `cd ~/emergent-hubs && rm -f STOP && nohup bash ops/schedule/overnight_run.sh >/dev/null 2>&1 &`
- watch: `tail -f ~/Library/Logs/emergent-overnight-run.log` (and `ls -t ~/emergent-hubs/.cache/overnight/` for each iteration's output)
- stop: `touch ~/emergent-hubs/STOP` (clean stop after the current iteration); hard stop: `kill $(cat ~/emergent-hubs/.cache/overnight/pid)`
