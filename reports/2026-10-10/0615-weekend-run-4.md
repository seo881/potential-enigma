# Weekend run report 4

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

11 pages finished since the last report: 11 reviewed and ready for Divit, 0 parked.

- ready: /ai-form-builder/ach-form (rework)
- ready: /ai-form-builder/advance-directive-form (rework)
- ready: /ai-form-builder/affidavit-form (rework)
- ready: /ai-form-builder/consent-form (rework)
- ready: /ai-form-builder/direct-deposit-form (rework)
- ready: /ai-form-builder/employee-evaluation-form (rework)
- ready: /ai-form-builder/intake-form (rework)
- ready: /ai-form-builder/order-form (rework)
- ready: /ai-form-builder/rental-application-form (rework)
- ready: /ai-form-builder/sign-up-form (rework)
- ready: /ai-form-builder/time-off-request-form (rework)

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 107, rework Form check2 1, rework Form images 2, rework Form ready 15, rework Form review 4, rework Form writer 3, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 184043, mean 205685, pages with a log 11
  - /ai-form-builder/ach-form: writer 176560, reviewer 44696
  - /ai-form-builder/advance-directive-form: writer 180055, reviewer 44696
  - /ai-form-builder/affidavit-form: writer 144947, reviewer 39096
  - /ai-form-builder/consent-form: writer 141639, reviewer 39127
  - /ai-form-builder/direct-deposit-form: writer 256721, reviewer 49465
  - /ai-form-builder/employee-evaluation-form: writer 132301, reviewer 44696
  - /ai-form-builder/intake-form: writer 98142, reviewer 44695
  - /ai-form-builder/order-form: writer 137341, reviewer 39127
  - /ai-form-builder/rental-application-form: writer 198749, reviewer 39096
  - /ai-form-builder/sign-up-form: writer 126165, reviewer 39096
  - /ai-form-builder/time-off-request-form: writer 206997, reviewer 39128
- AlsoAsked credits used this weekend: 8 of 300

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
