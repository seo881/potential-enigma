# Ruling 12: pull wave running, PA3 tranche 1 ready for your read, replacement screen (2 rows), ranked queue, split write, 12 reviews

## Digest for Divit
- **Tranche 1 is ready for your read.**
  - Reading copy: `.cache/review/pa3-tranche-1.md`. Decision sheet: `.cache/review/pa3-tranche-1.csv`. Both are git-ignored.
  - In the CSV, put yes or no on every phrase row, and an x on any question row you want struck.
  - 21 pages: the 19 queued pilot pages (assessment-form is already written) plus shipping-automation and automated-loan-processing-system.
  - **15 pages have phrases; 12 of them reach 10 with both phrases.** Today 3 reach 10.
- **Pull wave (`wave-r12`, cap 400 credits) is running:** 296 queued pages had no pull. At 13:16 UTC, 17 were pulled for 17 credits; it should finish around 16:30 UTC.
  - Next, automatically: the LP --kw secondary pulls.
  - After that: the 11 released parked pages, then tranches 2 to 7 as the pulls land (all queued pages by 10-16).
  - Pulls now run in A only: `weekend.py aa` refuses in B's clone.
- **Correction to my 1400 report: the AMBER sheet is not replacement supply.**
  - All 113 AMBER rows are angles for pages already in the plan (52 queued, 42 parked, the rest further along).
  - Of the 26 new-idea rows: 8 fail on intent (7 are /learn/ articles, 1 is a take-a-quiz), 4 cannibalise a planned page, and 12 can't be confirmed without a SERP check. **2 pass (both Form).**
  - The sheet is `.cache/review/replacements-2026-10-13.csv`; dropped rows and reasons are in `-dropped.csv`.
  - So the "about 110 replacements" I projected does not exist. The 500 gap has to close through synonyms and parked rescues (open question 2).
- **Ranked queue and claims:**
  - `plan/queue-ranked.txt` is live: ready, then syn-pending, then no-pull, then short; MSV breaks ties inside each class. `hubctl claim` takes from the top only.
  - 11 parked pages that reach 10 were released (5 Auto, 2 Form, 4 SurveyQuiz). They rank no-pull until A pulls them.
  - The Auto pilot hold is lifted.
- **Split write:** a page waiting on synonyms can't go to qc_pass, images or reviewed (hubctl refuses). B already has split writes in progress (attendance-form, culture-survey and others).
- **Reviews (item 7):**
  - Full reviews: assessment-form reviewed. sales-workflow is rework: its FAQ 8 claims a platform feature that `rules/capabilities.json` doesn't cover. wellness-survey is rework: why_description states the wrong pricing basis, and feature_2 is contradicted by the page's own tabs.
  - Slim reviews of B's reworks: the ledger shows **11** (not 13) moved to reviewed by B today. ach-form and photo-release-form are unchanged since A-s-12 (their hashes match). Of the other 9, 7 are reviewed. hotel-booking-form and model-release-form go to rework, each for one reworded AlsoAsked question (FAQ 2, FAQ 7) that had passed review before.
  - Every reviewer now runs the new `hubctl verbatim`.

## Request
> Divit ruling 12 (2026-10-13), approved: PA3 synonyms per page and replacement keywords, with zero quality change. Record in DECISIONS and TWO_ACCOUNTS. 1. AlsoAsked: A runs every pull; B never pulls and uses saved pulls only (0 credits). Tonight: pull every queued page with no pull (cap 2 per page, stop at 400 credits total), plus --kw pulls on the top secondaries of LP pages that returned no_results and are under 10. 2. PA3 synonyms, per page, my read: candidate sheets in tranches of 50 pages in queue-rank order (.cache only, AlsoAsked text never in git). Per page: the top 2 phrases, and under each phrase EVERY question it admits, so I can strike single questions as well as whole phrases. Tranche 1 tonight = the 20 pilot pages; next tranches as pulls land, all queued pages covered by 10-16. Approved phrases go into rules/paa_synonyms.json at once (per-page data, outside the Monday window). Struck questions go on that page's PA4 skip list with a golden case. Every admitted question still passes every other gate rule; a reviewer treats a drifting admitted question as blocking. 3. Replacement keywords: AMBER (116) and new-idea (29) rows, each screened for intent and cannibalisation against existing and queued pages (K-sibling). Rows that fail or cannot be confirmed are dropped, not sent. The rest go to me as one sheet ranked by MSV for a yes/no per row by 10-15. Approved rows enter the plan with the same pull and feasibility steps. 4. Queue: plan/queue-ranked (feasibility, then MSV), regenerated after every pull wave and synonym approval; B claims from the top only. Release to B any parked Form/Auto/Survey page whose feasibility reaches 10. 5. Split write (B): pages pending synonym approval get everything but the FAQ written first; QC, gate and the one review run on the whole page only after the FAQ lands. A page whose synonyms I reject goes back to the queue end, its draft kept. 6. Capacity: B measured about 7% of its weekly cap on about 5.6M tokens; plan for 50 pages/day. 7. Today: full review of wellness-survey, sales-workflow, assessment-form; slim review of B's 13 reworked pages (hash check, verbatim check on every restored AlsoAsked question). Batch 3 staging flow as soon as I say "staging published". Report per CLAUDE.md, under 15 lines in chat.

## Actions and results
1. **Pulls.**
   - `ops/pull_wave.py` runs every queued page with no pull, in queue-rank order, through `weekend.py aa --run wave-r12`. Then it runs the LP --kw secondaries for pages whose pull returned no_results and that are under 10.
   - `AUTH_RUNS` in weekend.py registers wave-r12 at 400 credits. Inside an authorised run, the run cap replaces the 300-credit weekend cap and can never exceed it.
   - The per-page cap of 2 is unchanged. aa refuses in B's clone.
   - The balance before the wave was 722 credits.
2. **Synonyms.**
   - `ops/synonyms.py sheet N` builds each tranche. The first phrase admits the most questions; the second admits the most the first does not. Every admitted question is re-gated with all other rules on. Under each phrase the sheet lists every question it admits, each with a question id.
   - `synonyms.py apply N --by A-coord` reads your sheet. It refuses any phrase row left blank.
     - Approved phrases go to `rules/paa_synonyms.json` at once.
     - Struck questions go on the page's PA4 skip list as a question hash (no AlsoAsked text in git), each with a `gate-pull-skip` golden case.
     - A split write whose phrases are all rejected goes back to the queue with its draft kept.
   - Tested on a copy: the strike is caught and the golden case passes. The test also showed the release step catching B's ordinary claims; it now releases only split-write pages (LESSONS line). Rules and status were restored after the test.
3. **Replacements:** screened by A-k-1 from the workbook. No SERP calls were made: the dataforseo MCP is not loaded in this session, and Semrush units were not approved.
4. **Queue:**
   - `ops/queue_rank.py` writes `plan/queue-ranked.txt` (rank, hub, url, class, feasibility; no Semrush data).
   - `--release-parked` released 11 pages through `hubctl release --by A-coord` with a ruling-12 note (logged in logs/<hub>.md).
5. **Split write:**
   - Claims from syn-pending rows carry `faq_pending`.
   - `set_state` refuses qc_pass, images, reviewed and approved while a page is `faq_pending`, or while its tranche is undecided and it is under 10 without the phrases.
6. **Reviews:**
   - Full review: A-r-4.
   - Slim reviews: A-s-13 (5 pages) and A-s-14 (4 pages).
   - B was told about the two FAQ fixes in proposals. hotel-booking-form's verbatim original fails PA3, so item 2 is re-sourced as a keyword question, as conference-registration-form was.

## Numbers
- Tranche 1: 21 pages, 15 with phrases, 12 reaching 10 with both phrases, 3 at 10 today.
- Wave at 13:16 UTC: 17 pulls, 17 credits. Planned: 296 primary pulls, then the LP secondaries.
- Replacements: 139 rows read; 113 already in the plan, 8 fail on intent, 4 cannibalise, 12 unconfirmed, **2 pass**.
- Queue: 313 queued. ready 3, syn-pending 0 (B has already claimed them as split writes), no-pull 282, short 28. 11 parked released.
- Reviews:
  - full: 3 (1 pass, 2 rework);
  - slim: 9 (7 pass, 2 rework);
  - review tokens about 400k in total (A-r-4 152k, slim 206k).
- Golden suite: 337 cases, 0 regressions. review-lock-2 is now pinned to a commit, and one open case that started passing was marked guarded.

## Decisions
- Ruling 12, items 1 to 7, as recorded in DECISIONS 2026-10-13 and TWO_ACCOUNTS 3d.
- Severity follows rules/SEVERITY.md.
- Reworded AlsoAsked questions are blocking under DECISIONS 2026-10-13 ruling 4.

## Files changed and commits
- 94034561: ruling 12 tooling and docs: weekend.py, pull_wave.py, synonyms.py, queue_rank.py, hubctl.py, park_rescue.py, paa_gate.py, golden suite, DECISIONS, TWO_ACCOUNTS, LESSONS, proposals.
- deee2232: 12 reviews (specs, status, usage).
- 7adcbfae: parked releases, split-write gate, ranked queue.

## Webflow calls
None.

## Not done
- **Batch 3 staging checks:** waiting for "staging published". All 11 sections are still unhidden for staging.
- **Tranches 2 to 7:** as the wave lands (by 10-16).
- **Pulls for the 11 released pages:** after the wave.
- **SERP checks on the 12 unconfirmed replacement rows:** see open question 1.
- **church-membership-form:** still held by B.

## Open questions for Divit
1. Replacements: should the 12 unconfirmed rows get SERP checks? That needs the dataforseo MCP loaded in A's session, or your OK to spend Semrush units (about 12 to 16 calls).
2. The 500 gap after the correction: with no AMBER supply, reaching 500 depends on synonyms (tranches) and the 42 parked AMBER pages. Should parked pages get synonym tranches too, after the queued ones?
3. Tranche 1: please fill in `.cache/review/pa3-tranche-1.csv`. I apply it the moment it is saved.
