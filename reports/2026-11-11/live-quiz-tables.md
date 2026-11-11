# Live quiz tables: slim review of the proposed quiz-maker table (A-s-24, 2026-11-11)

Request (A-c-1 to A-s-24): "Then the 2 LIVE quiz pages style and vocabulary: run `hubctl table <url>` output vs their current why_table; slim-review the proposed quiz-maker table only, and write the result to reports/2026-11-11/live-quiz-tables.md (no CMS writes; the ship agent does ship-update)."

Follows: DECISIONS 2026-11-11 (Divit, decisions) item 3 (quiz-maker category; live pages via ship-update with before-values, item publish, verify-live); library rules/competitors/sqb.json (b2b88608, category_sets.quiz-maker); status/quiz-table-2026-11-11.json (style, vocabulary: live-needs-update).

No CMS writes, no spec change. Note: `hubctl table <url>` writes the rebuilt table into the spec; both specs were restored to the live table right after (style.json clean; vocabulary.json keeps only another agent's uncommitted verify-live history entry). The ship agent runs `hubctl table <url>` again at ship-update time.

## Current (live) vs proposed

| | Live (general survey set) | Proposed (quiz-maker set) |
|---|---|---|
| Vendors | SurveyMonkey, Microsoft Forms, SurveyHero | ProProfs, Interact (quiz specialist), Typeform |
| Rows | output, pricing, data, ownership | build, pricing, data, ownership |
| Emergent column | hub default (approved claims) | hub default (approved claims) |

Identical proposal on both pages. The live table's "What you get" row compares the quiz to employee engagement and employee satisfaction survey templates, which does not fit a style or vocabulary quiz searcher; the proposal fixes that.

Proposed cells (Emergent | ProProfs | Interact | Typeform):
- How you build: Prompt for the survey, quiz, or poll and the app around it | Templates, question library, and AI quiz builder | Templates and AI quiz maker | Templates and editor, AI assist
- Pricing model: Credits, no response caps or per-response fees | Free plan, then billed per active quiz taker | Free plan capped by monthly responses, then paid plans | Plans by monthly response limit; discount for annual billing
- Where responses live: A database table you own, plus any integration | ProProfs account; reports export to Excel, CSV, or PDF | Interact account | Typeform account
- Code ownership: Full code export to GitHub on paid plans | None | None | None

## Slim review (proposed table only)

| Page | Verdict | Blocking | Notes |
|---|---|---|---|
| /ai-survey-and-quiz-builder/style | PASS | 0 | 1 |
| /ai-survey-and-quiz-builder/vocabulary | PASS | 0 | 1 |

Checks:
- Vendors fit the query: quiz makers for a searcher who wants to build a style or vocabulary quiz (decision 3). None of the three ranks in either page's top 10 (style: stylist, retailer and quiz-content sites; vocabulary: dictionaries and ESL sites), so QC K7 will flag P2 on each: note, not blocking (SEVERITY.md).
- Every cell traces to a library fact checked 2026-11-11 with a quoted vendor span (ProProfs quiz-school and business signup pages; tryinteract.com plans, terms and help; typeform.com pricing and service terms), except Typeform "editor", carried from the 2026-09-28 approved check; within the re-check window.
- No prices, plan numbers or invented features; the Emergent column is the approved hub default (rules/claims.json).
- Reads human: short noun phrases, no hype, consistent with the five quiz pages approved today.
- Renders within limits: the same cells pass QC T1/V2/V3 on personality, geography, fitness, funnel and hair-type (QC TOTAL 0 each).

Note (both pages): no library quiz-maker ranks in the top 10 (K7 P2); ships.

## Not done
- No ship-update, item publish or verify-live (ship agent's job, with before-values).

## Open questions for Divit
- None.
