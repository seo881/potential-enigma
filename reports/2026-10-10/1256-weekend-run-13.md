# Weekend run report 13

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

11 pages finished since the last report: 0 reviewed and ready for Divit, 11 parked.

- parked: /ai-form-builder/brand-questionnaire (rework): writer failed twice: PA11 PA12 PA1 PA3
- parked: /ai-form-builder/class-registration-form (rework): writer failed twice: PA11 PA3 PA14 PA15: no replacement source
- parked: /ai-form-builder/dental-intake-form (rework): writer failed twice: PA11 PA3 PA1 PA15
- parked: /ai-form-builder/expense-request-form (rework): writer failed twice: PA11
- parked: /ai-form-builder/file-upload-form (rework): writer failed twice: PA11
- parked: /ai-form-builder/food-bank-application-form (rework): writer failed twice: PA11 PA3: no replacement source
- parked: /ai-form-builder/overtime-request-form (rework): writer failed twice: PA11 PA3 PA15 PA12 F9
- parked: /ai-form-builder/rfq-form (rework): writer failed twice: PA11 PA3: no replacement source
- parked: /ai-form-builder/sign-out-form (rework): writer failed twice: PA11 PA3 PA15 PA14 PA8
- parked: /ai-form-builder/telemedicine-consent-form (rework): writer failed twice: PA11 PA3: no replacement source
- parked: /ai-form-builder/workshop-registration-form (rework): writer failed twice: PA11

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 3, rework Form images 18, rework Form images2 1, rework Form ready 27, rework Form review 1, rework Form stopped 80, rework Form writer 2, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 88630, mean 90377, pages with a log 11
  - /ai-form-builder/brand-questionnaire: writer 83208
  - /ai-form-builder/class-registration-form: writer 81072
  - /ai-form-builder/dental-intake-form: writer 77146
  - /ai-form-builder/expense-request-form: writer 88630
  - /ai-form-builder/file-upload-form: writer 103656
  - /ai-form-builder/food-bank-application-form: writer 83373
  - /ai-form-builder/overtime-request-form: writer 111581
  - /ai-form-builder/rfq-form: writer 100945
  - /ai-form-builder/sign-out-form: writer 128312
  - /ai-form-builder/telemedicine-consent-form: writer 89400
  - /ai-form-builder/workshop-registration-form: writer 46834
- AlsoAsked credits used this weekend: 20 of 300

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
