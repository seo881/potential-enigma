# Weekend run report 7

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

11 pages finished since the last report: 0 reviewed and ready for Divit, 11 parked.

- parked: /ai-form-builder/credit-application-form (rework): writer failed twice: PA11, PA3, PA1, PA12 (no allowed sources; spec unchanged)
- parked: /ai-form-builder/grievance-form (rework): writer failed twice: PA11, PA1, PA3, PA15: gate 4/10, no allowed replacements
- parked: /ai-form-builder/identity-verification-form (rework): writer failed twice: PA3, PA11: gate 5/10, no allowed replacements
- parked: /ai-form-builder/membership-form (rework): writer failed twice: PA11, PA12
- parked: /ai-form-builder/mileage-reimbursement-form (rework): writer failed twice: PA11, PA3: gate 6/10, no allowed replacements
- parked: /ai-form-builder/petition-form (rework): writer failed twice: PA11, PA3, PA4, PA1, PA14, PA15 (gate 3/10)
- parked: /ai-form-builder/project-request-form (rework): writer failed twice: PA3, PA11, PA12, PA14, PA15
- parked: /ai-form-builder/rfp-form (rework): writer failed twice: PA11, PA3, PA14, PA7, PA12, PA1 (no allowed sources; spec unchanged)
- parked: /ai-form-builder/tattoo-consent-form (rework): writer failed twice: PA11, PA3, PA1, PA7 (gate 3/10)
- parked: /ai-form-builder/time-sheet-form (rework): writer failed twice: PA11 (no allowed sources; spec unchanged)
- parked: /ai-form-builder/travel-request-form (rework): writer failed twice: PA11

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 71, rework Form images 11, rework Form images2 1, rework Form ready 27, rework Form review 1, rework Form stopped 19, rework Form writer 2, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 133842, mean 138027, pages with a log 11
  - /ai-form-builder/credit-application-form: writer 146354
  - /ai-form-builder/grievance-form: writer 135397
  - /ai-form-builder/identity-verification-form: writer 133842
  - /ai-form-builder/membership-form: writer 176471
  - /ai-form-builder/mileage-reimbursement-form: writer 131224
  - /ai-form-builder/petition-form: writer 196080
  - /ai-form-builder/project-request-form: writer 109009
  - /ai-form-builder/rfp-form: writer 130755
  - /ai-form-builder/tattoo-consent-form: writer 143293
  - /ai-form-builder/time-sheet-form: writer 116112
  - /ai-form-builder/travel-request-form: writer 99767
- AlsoAsked credits used this weekend: 12 of 300

## Decisions

- Rules applied: DECISIONS 2026-10-09 (PA14, PA15, D1, D2, F9) and 2026-10-10 (D3, serial comma H3); HUB_RULES section 5; rules/SEVERITY.md for review.
- One review per page (batch of up to 4), one rework; a page failing a stage twice is parked (ops/ship.py MAX_FAILS, DECISIONS 2026-10-07).
- New pages: canary of 3 per hub through review before more claims (Divit 2026-10-10).

## Files changed and commits

- specs/, status/ (ledgers status/ship/wk-*.json, status/weekend-run.json, status/readiness.md), plan/batches/wk-*.txt, plan/weekend-run.md; SHAs: `git log --grep '^weekend:'`.

## Webflow calls

None (weekend run: no Webflow tools).

## Not done

- Nothing created or published in Webflow; Divit's preview review and the Monday staging canary come first.

## Open questions for Divit

- Parked pages above: rescue or drop (default: leave parked until after the Monday canary).
