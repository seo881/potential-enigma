# AlsoAsked yield pilot (ruling 10A) and throughput: 500 is out of reach on current rules; PA3 synonyms are the lever

## Digest for Divit
- **Pilot:** 23 pages, 18 credits (balance about 722).
  - The next 5 queued pages per hub in plan order, plus the secondary pull for sales-workflow, shipping-automation and automated-loan-processing-system.
  - **Measured yield is very low:** 475 distinct pull questions, **18 pass the gate (3.8%)**. PA3 (no head phrase) rejects 92% of them.
  - **All 5 LP pulls returned no_results** at 0 credits; LP pages live on Semrush secondaries alone.
- **Feasibility (B1) with today's rules: 4 of 23 pages reach 10.**
  - Those 4: nonprofit and waitlist LP, content-approval-workflow, and sales-workflow after its secondary pull.
  - By hub: LP 2/5, Form 0/5, SurveyQuiz 0/5, Auto 1/5 (plus 1 of the 3 secondary pulls).
- **PA3 synonym candidates, for your read only and NOT applied:** with each page's top 2 candidates, **16 of the 18 pages with pull results would reach 10**; the median moves from 6 to 14.
  - The full question lists per candidate are in `.cache/review/pa3-candidates-2026-10-13.md` (git-ignored; it holds AlsoAsked text).
- **500 by 10-27 is not reachable on current rules.**
  - Projected shippable total: **about 200** today, **about 390** if you approve synonyms page by page.
  - Past that, the gap is supply (keywords), not speed: about 110 replacement keywords would be needed, from the workbook's AMBER (116) and new-idea (29) lists.
- **Weekly caps:** both accounts are **UNVERIFIED**. Neither clone exposes a readable plan cap or weekly usage. Measured today (status/usage.jsonl): A about 2.05M tokens logged, B about 5.6M.

## Per page (counts only)

| Hub | Page | Questions | Pass | PA3 | PA4 | PA14 | PA15 | Secondaries | Feasibility | With top-2 synonyms |
|---|---|---|---|---|---|---|---|---|---|---|
| LP | recruiting | 0 (no_results) | 0 | 0 | 0 | 0 | 0 | 4 | 6 | 6 |
| LP | lead-magnet | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 5 | 5 |
| LP | nonprofit | 0 | 0 | 0 | 0 | 0 | 0 | 8 | **10** | 10 |
| LP | giveaway | 0 | 0 | 0 | 0 | 0 | 0 | 6 | 8 | 8 |
| LP | waitlist | 0 | 0 | 0 | 0 | 0 | 0 | 8 | **10** | 10 |
| Form | attendance | 29 | 1 | 21 | 5 | 11 | 4 | 2 | 5 | 13 |
| Form | check-request | 17 | 4 | 12 | 0 | 0 | 1 | 0 | 5 | 12 |
| Form | assessment | 29 | 3 | 24 | 6 | 1 | 1 | 2 | 7 | 23 |
| Form | check-in | 51 | 1 | 50 | 1 | 12 | 13 | 1 | 4 | 24 |
| Form | home-inspection | 19 | 0 | 19 | 0 | 0 | 1 | 2 | 4 | 19 |
| SurveyQuiz | dei | 26 | 0 | 26 | 0 | 0 | 0 | 4 | 6 | 14 |
| SurveyQuiz | culture | 25 | 3 | 22 | 0 | 0 | 0 | 4 | 9 | 17 |
| SurveyQuiz | restaurant | 27 | 0 | 27 | 1 | 1 | 1 | 4 | 6 | 13 |
| SurveyQuiz | post-webinar | 15 | 1 | 14 | 0 | 0 | 0 | 1 | 4 | 4 |
| SurveyQuiz | pricing | 19 | 1 | 18 | 0 | 0 | 0 | 3 | 6 | 12 |
| Auto | order-processing | 14 | 0 | 14 | 2 | 1 | 1 | 4 | 6 | 13 |
| Auto | property-management | 23 | 0 | 23 | 3 | 1 | 0 | 4 | 6 | 18 |
| Auto | restaurant | 21 | 1 | 20 | 2 | 0 | 0 | 3 | 6 | 13 |
| Auto | content-approval-workflow | 15 | 1 | 14 | 1 | 1 | 1 | 7 | **10** | 22 |
| Auto | recruitment | 25 | 0 | 25 | 1 | 0 | 0 | 2 | 4 | 13 |
| Auto (secondary pull) | sales-workflow | 26 | 1 | 25 | 0 | 1 | 1 | 0 | **11** | 29 |
| Auto (secondary pull) | shipping-automation | 49 | 0 | 49 | 4 | 5 | 0 | 0 | 7 | 22 |
| Auto (secondary pull) | automated-loan-processing-system | 41 | 0 | 41 | 13 | 1 | 0 | 7 | 9 | 26 |

Feasibility = pull items that pass or flag + uncarried Semrush secondaries + recoverable keyword items + 2 template slots on unwritten pages (B1). Rejects can carry several rules each.

## Supply and the date 500 is reached

| | Today's rules | With approved synonyms |
|---|---|---|
| Live + staged (batch 3) | 60 | 60 |
| Reviewed, not in the CMS | 44 | 44 |
| Rework / images (about 70% ship) | about 12 | about 12 |
| Queued 315 × feasible rate | 17% → about 55 | about 75% → about 235 |
| Parked rescues (B's 31–45 estimate, discounted for this yield) | about 20 | about 40 |
| **Projected total** | **about 190–200** | **about 390** |
| **Date reached at 35/day** | about 10-17 (supply runs out) | about 10-22 (supply runs out) |

- At measured tokens, a shipped page costs about 230k end to end:
  - write: about 60k median for a B rework, about 113k for a new page;
  - review: full 44k, slim 18k;
  - ship: about 15–20k;
  - pages that stop at feasibility cost no writer.
- That is about 8M tokens for 35 pages a day across both accounts. Whether that fits the weekly caps is UNVERIFIED.

## Recommendation (your call)
1. **Read the PA3 candidates** for the 23 pilot pages and approve or reject per page. Approved phrases go into rules/paa_synonyms.json in the Monday window (B3), or at once if you say so.
2. If you approve a pattern rather than single pages (for example the head phrase without its format word), I can generate candidates for all 315 queued pages for the same kind of read. That costs about 1 credit per page for pulls not yet made, under the cap.
3. **Close the 110-page gap with replacement keywords** from the workbook's AMBER and new-ideas lists. Each goes through the same plan, pull and feasibility steps.

## Request
> Divit ruling 10 (2026-10-13), part A: the yield pilot (max 45 credits, 5 queued per hub in plan order, plus the 3 secondary pulls); per-page and per-hub yield; projected supply; the date 500 is reached at measured yield and tokens; weekly caps or UNVERIFIED; PA3 synonym candidates for Divit's read, never applied without his go.

## Actions and results
- 23 pulls through `weekend.py aa --run pilot-r10 --run-cap 45`: 18 credits, every pull saved.
  - The 5 LP pulls (no_results, both normal and fresh) cost 0.
  - The 4 Form pages that already had no_results pulls took their one allowed fresh retry.
- Analysis with `qc/paa_gate.py` (run_pull) and `ops/park_rescue.feasibility`. The candidates are generated from the PA3-rejected questions (n-grams containing the head's distinctive word, plus the gate's own format and abbreviation candidates), and each is re-gated with every other rule on.

## Numbers
- Pass rate 3.8% (18 of 475).
- Feasible 4 of 23 now, 20 of 23 with top-2 synonyms (2 LP pages and post-webinar-survey stay short).
- Credits: 18. Golden suite unchanged: 337 cases, 0 regressions.

## Decisions
Ruling 10A; DECISIONS 2026-10-08 (synonyms are proposed, never applied without Divit's go); AlsoAsked text stays out of git and reports.

## Files changed and commits
This report and its INDEX line. The candidate file is in `.cache/review/` (git-ignored).

## Webflow calls
None.

## Not done
- No synonym applied.
- No Auto page handed to B (pilot hold) until you rule on the candidates.
- Full reviews of B's 3 new pages in `images` (wellness-survey, sales-workflow, assessment-form): next, while staging waits.

## Open questions for Divit
1. Approve PA3 synonyms per page from the candidate file, or name a pattern to apply across the queue?
2. Add replacement keywords (AMBER and new ideas) to the plan to close the roughly 110-page gap?
3. Can you read either account's weekly cap and usage? Neither is visible from Claude Code here.
4. B's AlsoAsked key returns HTTP 403 in B's session (nothing charged). Fix the key in B's environment, or should A run pulls for B's queue (about 1 credit a page)?
