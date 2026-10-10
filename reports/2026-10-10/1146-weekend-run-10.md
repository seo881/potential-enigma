# Weekend run report 10

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

10 pages finished since the last report: 0 reviewed and ready for Divit, 10 parked.

- parked: /ai-form-builder/church-membership-form (rework): writer failed twice: PA11 source-starved (3/10)
- parked: /ai-form-builder/contest-entry-form (rework): writer failed twice: PA11 source-starved (3/10)
- parked: /ai-form-builder/equipment-rental-agreement-form (rework): writer failed twice: PA11 source-starved (4/10)
- parked: /ai-form-builder/pet-adoption-form (rework): writer failed twice: PA11 source-starved (6/10)
- parked: /ai-form-builder/pre-order-form (rework): writer failed twice: PA11 source-starved (3/10)
- parked: /ai-form-builder/reference-check-form (rework): writer failed twice: PA11 source-starved (6/10), PA12
- parked: /ai-form-builder/service-request-form (rework): writer failed twice: PA11 source-starved (4/10), PA12
- parked: /ai-form-builder/student-registration-form (rework): writer failed twice: PA11 source-starved (3/10), PA12
- parked: /ai-form-builder/travel-reimbursement-form (rework): writer failed twice: PA11 source-starved (2/10)
- parked: /ai-form-builder/website-design-questionnaire (rework): writer failed twice: PA11 source-starved (4/10)

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 41, rework Form images 11, rework Form images2 1, rework Form ready 27, rework Form review 1, rework Form stopped 49, rework Form writer 2, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 51576, mean 51826, pages with a log 10
  - /ai-form-builder/church-membership-form: writer 51576
  - /ai-form-builder/contest-entry-form: writer 51678
  - /ai-form-builder/equipment-rental-agreement-form: writer 51358
  - /ai-form-builder/pet-adoption-form: writer 51259
  - /ai-form-builder/pre-order-form: writer 51555
  - /ai-form-builder/reference-check-form: writer 53520
  - /ai-form-builder/service-request-form: writer 52218
  - /ai-form-builder/student-registration-form: writer 51525
  - /ai-form-builder/travel-reimbursement-form: writer 51358
  - /ai-form-builder/website-design-questionnaire: writer 52217
- AlsoAsked credits used this weekend: 14 of 300

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
