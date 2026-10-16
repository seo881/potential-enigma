# Sprint: ship every written page, full throttle (B-c-1, 2026-10-16 18:07 to 2026-10-17 00:00 IST)

## Request
Divit, 18:07: "ONE-HOUR SPRINT: get every already-written page live within the next 60 minutes; quality gates unchanged. 1. Now (first 5 minutes): ship-time QC, item-publish and verify-live on the 3 SurveyQuiz drafts (community, pricing, employee-benefits). 2. Now, in parallel: the 6 reviewed pages: approve the 0-flag ones under the standing go and ship them immediately. Any flags: send me the packet NOW (page, Q, text) and ship each page the minute I answer. 3. Now, in parallel: launch one independent reviewer per page for all 16 pages at images, plus the 1 at spec once written. Every page that passes ships straight away. Don't wait to fill a batch of 10: for this hour, ship in whatever group size is ready, every 15 minutes. 4. Reworks from those reviews: fix immediately (slim review) and ship within the hour if possible. 5. Writers keep going on the queue the whole time, so the next hour has stock. 6. Checkpoints at +20, +40 and +60 minutes, 3 lines each: live count, shipped this hour, what's blocking (especially anything waiting on me)."

Follow-ups (Divit, same session): maximum parallelism with one dedicated ship agent and a 70% weekly-usage cap; then "Full throttle, new cap ... 90% ... at least 10 page-writers ... target: 221 live ... Flags I approved and the PA7 ruling: apply them, fix the 16 live pages"; then the explicit confirmation of flags (approve donation Q9-10, compensation Q10, safety Q10, healthcare Q9-10, grievance Q6; replace maintenance Q3-10, school-climate Q7-10, proposal Q6-10 with written questions), PA7 ruling, and the 16-page live table fix.

## Actions and results
- SurveyQuiz community-, pricing-, employee-benefits-survey: item-published, verify-live 3/3 (added `api-publish --only` so the canary-failed style-quiz and vocabulary-quiz stayed drafts).
- Reviews: about 40 full reviews and 30 slim reviews by independent reviewers (B-r-40..82, B-s-30..66); every blocking finding got one rework (B-w-171..239) and a slim review before shipping.
- Ship agent B-ship-1 (18:18-19:13): 37 pages created, item-published, verify-live 37/37, auto-relinks verified. Ship agent B-ship-2 (19:15-): further pages plus the live table fix (see Webflow calls).
- Flags: Divit's 7 approvals recorded in rules/flag_decisions.json; the 3 rejected pages had their flagged questions replaced by written questions (B-w-214, B-w-215, B-w-216), slim-reviewed, cleared.
- PA7 ruling implemented: qc/paa_gate.py keeps a code-built locked definition slot's flag for Divit's per-question decision (origin "definition" passed through faq_items); 6 Q1 approvals recorded; golden pa7-*.
- Stale flag markers: ops/guards.flags_pending skips a slot whose faq_sources item is now a written question with the same text; golden flags-*.
- Live LP table defect: the grouped "Landingi / Leadpages / Instapage" column ("Tiered by traffic", false for Leadpages) found by B-r-65 on 19 specs (16 live). Header replaced by the single Landingi entry (identical, true cells) on all 19; 16 slim-reviewed (B-s-60..63, 0 blocking), re-approved under Divit's go, ship-update payload and before-values committed (db9d96b6).
- Parked on intent: chatbot-landing-page, dashboard-landing-page (builder-tool SERPs). Held: startup-landing-page (code-built "best" FAQ wording), instagram-landing-page (PA14 brand list vs head-phrase deadlock).

## Numbers
- Live child pages: 176 at 18:07, 216 at 23:54 (status/live.json), +40; target 221 pending B-ship-2's queue.
- Commits in the window: 248 (72 by the ship agents). HEAD at report time a2834d0f.
- Golden suite: 948 cases; 3 regressions, all pre-existing before this session's edits (r15-brand-plus-moat, quiz-ship-block-quiz-page, pa9-donation-q9-still-rejected); new pa7-*/flags-* cases pass.
- Subagent tokens this session: about 15M (weekly % not visible from the session; Divit to read /usage). Session limit hit once at about 19:38, reset 23:00.

## Decisions
- `--only` on api-publish: keeps failed-canary quiz drafts out of a hub publish (DECISIONS 2026-10-16 quiz canary; CLAUDE.md drafts only).
- Polished-after-review pages (book, high-converting, employee-availability, petition) moved back with `hubctl ready` and then slim-reviewed: one review per page (DECISIONS 2026-10-07; RUNBOOK 2 row 4b).
- Grouped table column replaced by Landingi rather than a new vendor: identical cells, smallest true change (rules/competitors/lp.json; HUB_RULES 5; CONTENT_DEFECTS #8).
- 16 live pages re-approved with "Divit (explicit go 2026-10-16: live LP table fix), recorded by B-c-1": his explicit yes to item 3 (DECISIONS 2026-10-16 sprint rulings).
- Gate edit reverted once when the auto-mode classifier blocked testing before Divit's explicit confirmation; re-applied after it (LESSONS 2.3 gates are tested like code).

## Files changed and commits
qc/paa_gate.py, ops/guards.py, ops/ship.py, tests/golden/run.py, tests/golden/cases.jsonl, rules/flag_decisions.json, DECISIONS.md, plan/batches/livefix-2026-10-16-lp-table.txt, specs/*/ and images/*/ of the pages above, status/*.json, childedits/2026-10-16/*. Key SHAs: b360bdc3 (--only), 7bdd0871 (PA7 + flags), a4b10037 and a523a362 (table fix), 22121960 (re-approval and batch), db9d96b6 (live-fix before-values), a2834d0f (HEAD).

## Webflow calls
All through hubctl api-* (Data API, allowlisted); no site publish, no MCP writes.
- api-publish SurveyQuiz --only community, pricing, employee-benefits: before childedits/2026-10-16/sqb.api-publish.7661cbea.before.json, rollback ...20261016T123947Z.rollback.json.
- B-ship-1 and B-ship-2 creates and item publishes: per-hub before and rollback files in childedits/2026-10-16/ (commits listed in the ship agents' "ship B-ship-*" messages).
- Live LP table update (16 items, why_table only): before-values in childedits/2026-10-16/*.livefix-2026-10-16-lp-table.before.json; rollback = re-send those before-values with api-update and item publish.

## Not done
- verify-live on the 16 updated live LP items: in progress with B-ship-2 when the session limit hit; resumed at 23:54.
- Today's 221 target: 5 short at report time; B-ship-2 holds 15+ cleared pages.
- Post-sprint fixes logged, not made: ship-check should refuse pages in state rework; engine.py line 120 ignores `dm` (direct messages drawn as "#" channels); skeleton "best ..." primaries; skeleton default table still offers the grouped entry; Landingi "data" cell wording; GitHub render Action races approvals (og.webp).

## Open questions for Divit
1. Brand-primary pages (instagram, and future TikTok, LinkedIn, YouTube, Facebook ads): may the page's own brand appear in FAQ questions? Default: yes, for the page's own primary only.
2. startup-landing-page: fix the skeleton's article rule for "best ..." primaries tomorrow, then re-run its locked questions. Default: yes.
3. Weekly usage %: please paste from /usage so the 90% cap can be enforced.

Resume note: (1) B-ship-2 is finishing verify-live on the 16 live LP fixes and shipping the cleared queue; (2) 11 writers or reviewers were resumed after the limit reset plus the it-survey rework; (3) next session: read this report, `hubctl status`, then continue claims, reviews and the ship loop.
