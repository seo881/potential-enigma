# Account B: A-routed FAQ swaps, product-launch LP review, new-page claims (2026-10-14)

## Request

> Pull first. If private/semrush is empty in your clone, tell me before claiming (Divit runs the rsync).
> 1. Swaps A routes to you: compliance-automation Q7, crm-automation Q10, healthcare-automation Q9 and Q10. Replace each from the page's passing set (no vendor-comparison, "which platform/middleware/tools", or off-sense questions), keep everything else, QC 0, 0 rejects, slim review by a B-s agent, ready. it-automation: finish its rework once A unlocks alt:tab_image_2.
> 2. Then claim the 19 new-keyword pages through hubctl claim from the top of the ranked queue (Form 13, SurveyQuiz 4, seo-automation, maintenance-page), ruling-15 pipeline, independent B-r reviews, flagged FAQ questions per page listed in your report for the advisor's check.
> 3. vocabulary-quiz and style-quiz are reviewed; leave them until the quiz template is live.
> 4. No Webflow, AlsoAsked or Semrush calls.
> Up to 10 writer and 4 reviewer subagents. Report under 15 lines when the swaps are done and again when the 19 are reviewed.

Follow-up from Divit: "Pull now: A registered the 37 new-keyword pages at 18:19 (06712b21); 19 are claimable. Competitor library is being extended for finance, CRM, compliance, healthcare and RPA; use it on new pages as soon as it lands. Continue: product-launch-landing-page review, then the swaps when A routes them, then the 19 new pages. Every claim sentence needs a claim ID or a quoted source span; 6 truth findings in 9 pages is too many."

## Actions and results

1. **Pull.** Done; 06712b21 is present. Semrush question data loads in this clone (ops/skeleton.py plan_slots returns Semrush slots, e.g. 18 on compliance-automation), so no rsync was needed. private/ itself was not read.
2. **product-launch-landing-page.**
   - Written by B-w-71 and taken to images (c6ef8993).
   - B-r-7 reviewed it: 0 blocking, 4 notes, state reviewed (f80dde9a). Truth check: every Emergent sentence maps to a claim ID, and the FTC and Kickstarter lines match their quotes.
3. **compliance-automation Q7.**
   - B-w-72 replaced it with the first filtered code-built Semrush slot (recurring control testing). The answer is advice only, with no Emergent or third-party claim.
   - Checks: QC 0, gate 8/0/2, verbatim ok, render CURRENT, ready (f8961cde).
   - B-s-1 slim review of `faq`: 0 blocking, 1 note (the owner idea is repeated from FAQ 2 and 8), state reviewed (180a5e28).
4. **crm-automation Q10, healthcare-automation Q9 and Q10: not swapped.** plan_slots leaves 0 candidates on both pages after filtering against kept and dropped questions. Both pages are unchanged at reviewed. Recorded for A to re-park (03c59b0a).
5. **it-automation.** Still waiting on A's `hubctl unlock ... alt:tab_image_2` (asked in 84e8cf59). The rework sits in B's working tree, and B-w-63 holds the page.
6. **19 new-keyword pages.**
   - Claimed one per writer ID, B-w-73 to B-w-91, ranks 1-19, then held (d1813d3c). Skeletons built.
   - r15 writer prompt: every claim sentence needs a claim ID or a 6+ word quoted source span, or it is cut.
   - yes-no-questions-survey (B-w-74) is at images (be6764ad); B-r-8 is reviewing it. The other writers are running.
7. **Skeleton defect.** ops/skeleton.py shortens names into garbled code-built fields: "Build My or No Questions Survey", doubled "Questions Questions", and dropped head words on 7 pages. Reported to A (6b69a3b8, 9e7c196b). B does not edit code-built fields, and these pages will not go to ready until A fixes them.

## Numbers

| | Count |
|---|---|
| Routed swaps done | 1 of 4 items (compliance Q7) |
| Routed swaps with no code-built slot | 3 items on 2 pages |
| Full reviews | 1 (0 blocking) |
| Slim reviews | 1 (0 blocking) |
| New pages claimed and held | 19 |
| Writer tokens | 160,103 (B-w-71), 71,563 (B-w-72), 141,419 (B-w-74) |
| Reviewer tokens | 84,623 (B-r-7), 48,605 (B-s-1) |

## Flagged FAQ questions (for the advisor)

- product-launch-landing-page: Q9, Q10 (PA6).
- compliance-automation: Q6 (PA14, pre-existing), Q7 (PA6, new).
- yes-no-questions-survey: none (10/0/0).

## Decisions

- **Candidate filter for Q7.** The routing excludes "which tool" questions and off-sense candidates, so B dropped "access compliance" and the garbled "Is it lab..." candidates.
- **Ready before the slim review.** swap_b.md runs ready, and the slim review then renews the review hash (hubctl slim-review, ruling 1).
- **Conflict resolution on status/aab.json.** A's ship batch and B's slim-review note collided. B kept A's CMS fields and B's note.
- **Webflow:** none.

## Files changed and commits

- **Paths:** specs/lp/product-launch-landing-page.json, images/lp/product-launch-landing-page/, specs/aab/compliance-automation.json, specs/sqb/yes-no-questions-survey.json, images/sqb/yes-no-questions-survey/, status/{lp,aab,form,sqb}.json, status/usage.jsonl, proposals/account-b.md.
- **Commits:** c6ef8993, d1813d3c, 03c59b0a, f80dde9a, f8961cde, 180a5e28, be6764ad, 6b69a3b8, 9e7c196b.

## Webflow calls

None.

## Not done

- **crm-automation and healthcare-automation swaps.** No slot remains, so they wait on A.
- **it-automation.** Waits on A's unlock.
- **The 19 new pages.** Writing is in progress. The second report comes when all 19 are reviewed.
- **Competitor library extension.** Not landed yet. Any pages whose tables were built before it lands will need a table rebuild.

## Open questions for Divit

1. **Code-built fields on new pages.** Should A fix the shortener and rewrite the fields, or authorize B to set explore_cta and faq_heading by hand on the affected pages?
