# B's overnight run (ruling 20, Divit 2026-10-14)

Account B runs the overnight loop in its own clone `~/emergent-hubs-a` (CLAUDE_CONFIG_DIR=~/.claude). Every headless session starts with "Continue the overnight run per plan/overnight-run-b.md". Read CLAUDE.md, LESSONS.md, DECISIONS.md (rulings 15 to 20), docs/TWO_ACCOUNTS.md and this file first.

- start: `cd ~/emergent-hubs-a && git pull -q --rebase origin main && rm -f STOP && nohup bash ops/schedule/overnight_run_b.sh >/dev/null 2>&1 &`
- watch: `tail -f ~/Library/Logs/emergent-overnight-run-b.log`
- stop: `touch ~/emergent-hubs-a/STOP` (a clean stop after the current page; remove STOP before the next start)

## What B does (all 4 hubs: LP, Form, Automation, SurveyQuiz)

Run `.venv/bin/python3 ops/overnight_b.py next` and work its list in order. One page per writer subagent; up to 10 in parallel; ruling-15 pipeline only (`ops/skeleton.py build`, the section checks, `assemble`, `check all`).

1. **Reworks first.** Every page in state `rework`. Fix only the blocking findings named in its note or latest review; keep every other field byte-identical. Run QC to 0 and the gate to 0 rejects, re-render if the images changed (`hubctl images`), then `hubctl ready URL --by B-w-<n>`. One rework per page. If a page cannot be fixed from code-built skeleton slots, leave it in `rework` with a one-line note for A; do not hand-pick questions.
2. **In-flight B pages:** finish them (claimed or spec, by B-w or held by B).
   2b. **Slim reviews:** every `reviewed` page whose text changed after its review (a rework) gets a B-s slim review of the changed fields (`hubctl review-diff`, then `hubctl slim-review URL FILE --by B-s-<n>`, never by a writer of the page). Without it the page cannot ship (guards.review_ok).
3. **Render** every page at `qc_pass` (`hubctl images URL`), and read its contact sheet: one hero, readable text, numbers that add up.
4. **Review** every page at `images` with an independent **B-r** agent (page-reviewer), up to 4 pages each. A reviewer never reviews a page any part of which it wrote; hubctl refuses a match. Severity comes from rules/SEVERITY.md only. Blocking findings go to `rework`, with one rework by a different B-w writer, then `hubctl ready`. There is no second full review. Changed fields after a review get a **B-s** slim review (`hubctl slim-review`).
5. **Claim** from the top of `plan/queue-ranked.txt` with `hubctl claim HUB N --by B-w-<n>`, in all 4 hubs. Quiz pages are claimed only once `status/quiz-canary.json` says `pass`. Never claim or touch a page held by A.

After each review batch, list the flagged FAQ questions for A: run `.venv/bin/python3 ops/flag_packet.py list <reviewed URLs> --batch b-<HHMM>`, which writes to .cache (the question text stays out of git), and note its path and counts in the commit message.

## What B never does

- No Webflow, CMS writes, publishes or staging. Shipping is A's job through `hubctl api-*` (ruling 19). The API write commands are denied in this loop, and `EMG_HEADLESS` blocks any write.
- No AlsoAsked or Semrush calls, and no re-ranks; those stay with A (ruling 20).
- No edits to rules, QC, tooling, templates or config. Propose rule changes in `proposals/` as before.
- No question text, SERP data or anything from `private/` or `.cache/` in commits or reports.

## Commits and the morning

- Commit after every page with `bash ops/sync.sh "<msg>" <paths>`. The message names the page, the writer or reviewer id and the result (QC, gate and review outcome).
- Log tokens per page with `hubctl usage-log URL TOKENS --role writer|review --agent <id>`.
- When `next` has nothing left, it re-checks the queue every 30 minutes until 08:00 IST, then the loop ends.
- A reads the log and the commits at 10:00 and ships the `reviewed` pages through the API script.
