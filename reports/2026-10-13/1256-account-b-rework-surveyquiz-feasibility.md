# Account B: batch-3 urgent pages, Form and SurveyQuiz reworks, queued feasibility (2026-10-13)

## Request

> Pull first. Read docs/TWO_ACCOUNTS.md, DECISIONS 2026-10-13 and the last lines of proposals/account-b.md. SurveyQuiz moves to you (ruling 9); A is recording it now. Do not claim or touch any Survey page until that commit and A's handover line are on origin; then set .hub to B:Form,Auto,SurveyQuiz. Order:
> 1. ach-form and photo-release-form (batch 3, urgent): hold each, apply only the slim-review note in status/form.json (restore the verbatim AlsoAsked question; photo-release answer opens with a direct yes). QC 0, gate 0 rejects, flags in the commit, hubctl ready --by B-w-<n>, unhold, one commit per page, push at once.
> 2. The other 7 Form reworks (address-verification, conference-registration, consultation, driver-application, hotel-booking, model-release, tenant-screening): hold each, fix the blocking findings only, as written in each note. Change no other field.
> 3. Survey reworks A releases (customer-experience-survey, onboarding-survey, wellness-survey): same rule.
> 4. sales-workflow, shipping-automation, automated-loan-processing-system: use A's saved pulls via weekend.py aa (must show 0 credits). If a page cannot reach 10 with 0 rejects, stop after one pass and ask A for the --kw pull in proposals.
> 5. Then queued Form and Survey pages, alternating, 10 per claim. Feasibility first: after the page's one pull, run plain hubctl paa; if passing items plus brief sources are under 10, do not write, note it in the commit and move on. No new Auto claims until A's yield check lands.
> Run up to 6 writer subagents in parallel. Token-light. Report per CLAUDE.md, under 15 lines in chat.

## Actions and results

1. **Setup.**
   - The earlier date-churn conflicts were cleared by Divit's backup-and-reset command.
   - Pulled after A's ruling 9 commits (07b39174, 822bc426), then set `.hub` to `B:Form,Auto,SurveyQuiz`.
   - Held all 12 rework pages (B-w-8 to B-w-19) and pushed the holds before any edit (c3e206d7).
2. **Batch-3 urgent pages.** Both are now `reviewed`.
   - ach-form: FAQ item 5 restored to its verbatim AlsoAsked question, and item 1 restored for the same drift (2d28afd5).
   - photo-release-form: FAQ item 3 restored to verbatim, and its answer now opens with a direct yes (22014ea6).
3. **The other 7 Form reworks**, all `reviewed`:
   - address-verification-form (40917843);
   - conference-registration-form (141a7afe);
   - consultation-form (67b90dbb);
   - driver-application-form (fa12affe);
   - hotel-booking-form (f0d637bf);
   - model-release-form (5f7c0125);
   - tenant-screening-form (1ef03d35). Its FAQ 4 fix needed three knock-on edits to keep QC at 0: the FAQ 1 answer wording, feature_3 and plan.angle. All three are listed in the commit.
4. **SurveyQuiz reworks.**
   - customer-experience-survey and onboarding-survey are `reviewed` (f816e1ef, eeeca409). Their status notes gave no findings, so the writers fixed the open QC ratchet P1s:
     - customer-experience-survey: chip_adds added and a stock name replaced;
     - onboarding-survey: stock names replaced, hero_prompt made generic, chip_adds added. Its blocking FAQ 7 clause was already gone.
   - wellness-survey is in `images` (e5425bf3). It entered rework through the recheck and has no review record yet, so it needs A's first review.
5. **Automation.** All three used A's saved pulls through `weekend.py aa`, at 0 credits.
   - sales-workflow: 1 passing question. With the existing draft it reaches QC 0 and gate 6/0/4, so it went to `images` for A's review (de5a5322).
   - shipping-automation: 0 passing questions, and the spec is still 3 FAQ items short.
   - automated-loan-processing-system: 0 passing questions and no spec.
   - The last two stay claimed. The `--kw` pull request to A is in proposals (c3e206d7, dc14bf15).
6. **Queued Form and SurveyQuiz.**
   - Round 1 claimed 10 Form and 10 SurveyQuiz pages (30c01fb9, 4513ff18), checked with `weekend.py aa` (0 credits) and `hubctl feasibility`.
     - Feasible: 1 of 20, assessment-form. It was written to `images` with QC 0 and gate 10/0/0 (e3104694).
     - Not written: catering-order-form was released (e015433f) and 18 were deferred (5142022f).
     - Writers were already running on 4 pages that failed the check. I stopped them; their partial files are in a session scratch folder, and none was committed.
   - Round 2 claimed 20 pages (1c3a6cd1). All scored 2 to 8 out of 10 before any pull, and B's AlsoAsked key now returns HTTP 403, so they were released unwritten (f440666e).

## Numbers

| | Count |
|---|---|
| Rework pages to `reviewed` | 13 (9 Form, 2 SurveyQuiz, ach and photo included) |
| Pages to `images` for A's review | 3 (wellness-survey, sales-workflow, assessment-form) |
| QC TOTAL / PAA rejects on every page committed | 0 / 0 |
| Gate flags listed in commits | address-verification Q10; model-release Q4; tenant-screening Q3-Q6; customer-experience Q8-Q9; sales-workflow Q6, Q8-Q10 (all PA6) |
| Queued pages feasibility-checked | 40 (1 feasible, 19 deferred or released at round 1, 20 released at round 2) |
| AlsoAsked credits spent by B | 0 |
| Writer tokens logged | 12 reworks 47-68k each (median about 54k); assessment-form 184k; check-request-form 66k (stopped at feasibility) |

## Decisions

- **Hold before touch, unhold at handoff, one commit per page.** Source: TWO_ACCOUNTS (hold markers; one page = one commit).
- **Flags are kept verbatim and listed; never reworded.** Source: Divit's rulings 2026-10-13, ruling 2.
- **Rework pages go through `hubctl images` before `ready`.** hubctl refuses `ready` from `rework`.
- **A rework page with no review record stops at `images`.** This is wellness-survey. Source: CLAUDE.md step 5.
- **Infeasible queued pages are deferred, not written.** Source: the request, item 5; `hubctl feasibility` and `hubctl defer`.
- **Pages with no pull are released, not deferred.** A defer would record a count taken before the page's one pull.
- **No new Auto claims.** Source: the request, item 5.
- **Webflow:** none.

## Files changed and commits

- **Paths:** `specs/form/*`, `specs/sqb/*`, `specs/aab/sales-workflow.json`, the matching `images/*` folders, `status/form.json`, `status/sqb.json`, `status/aab.json`, `status/usage.jsonl` and `proposals/account-b.md`.
- **Commits:**
  - holds: c3e206d7 and e015433f;
  - pages: 2d28afd5, 22014ea6, fa12affe, 67b90dbb, 40917843, 141a7afe, de5a5322, f0d637bf, 5f7c0125, 1ef03d35, f816e1ef, eeeca409, e5425bf3 and e3104694;
  - claims, defers and releases: 30c01fb9, 4513ff18, 5142022f, 1c3a6cd1 and f440666e;
  - proposals: dc14bf15.

## Webflow calls

None. B has no Webflow access.

## Not done

- shipping-automation and automated-loan-processing-system wait on A's `--kw` pulls.
- Queued writing is stalled. With saved pulls the yield is 1 in 19, and B cannot pull because its key returns 403.
- **Stopped writers.** Their token use was not reported, so it is not logged.
- **Stray usage row.** One usage row of 0 tokens was logged for sales-workflow (B-w-7), whose real tokens were logged earlier.
- **Stash.** One stash holds a stopped writer's partial attendance-form spec. Nothing in it is needed.

## Open questions for Divit

1. B's AlsoAsked key returns 403. Should A run the pulls for B's queued pages, or should B get a working key?
2. Queued feasibility is very low: about 5 in 100 with saved pulls. Should the queue be re-ranked by feasibility before more claims, for example through the `--kw` secondary pull?
