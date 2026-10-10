# Weekend run report 8

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

10 pages finished since the last report: 0 reviewed and ready for Divit, 10 parked.

- parked: /ai-form-builder/accounting-client-intake-form (rework): writer failed twice: PA11, PA12
- parked: /ai-form-builder/cake-order-form (rework): writer failed twice: PA11 source-starved (PA3, PA1, PA14, PA8)
- parked: /ai-form-builder/custom-order-form (rework): writer failed twice: PA11 source-starved (PA3, PA14, PA15)
- parked: /ai-form-builder/daycare-registration-form (rework): writer failed twice: PA11 source-starved (PA3, PA6, PA14, PA15)
- parked: /ai-form-builder/employee-feedback-form (rework): writer failed twice: PA1, PA3, PA11, PA12, PA14, PA15
- parked: /ai-form-builder/esthetician-intake-form (rework): writer failed twice: PA11 source-starved (PA3, PA1)
- parked: /ai-form-builder/interview-evaluation-form (rework): writer failed twice: PA11 source-starved (PA3, PA1, PA14, PA15, PA8)
- parked: /ai-form-builder/life-coaching-intake-form (rework): writer failed twice: PA11 source-starved
- parked: /ai-form-builder/maintenance-request-form (rework): writer failed twice: PA11 source-starved
- parked: /ai-form-builder/wedding-photography-contract (rework): writer failed twice: PA11 source-starved (PA3, PA12, PA14, PA15)

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 61, rework Form images 11, rework Form images2 1, rework Form ready 27, rework Form review 1, rework Form stopped 29, rework Form writer 2, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 58722, mean 59237, pages with a log 10
  - /ai-form-builder/accounting-client-intake-form: writer 61337
  - /ai-form-builder/cake-order-form: writer 58536
  - /ai-form-builder/custom-order-form: writer 55083
  - /ai-form-builder/daycare-registration-form: writer 61055
  - /ai-form-builder/employee-feedback-form: writer 57164
  - /ai-form-builder/esthetician-intake-form: writer 58722
  - /ai-form-builder/interview-evaluation-form: writer 61460
  - /ai-form-builder/life-coaching-intake-form: writer 63382
  - /ai-form-builder/maintenance-request-form: writer 58200
  - /ai-form-builder/wedding-photography-contract: writer 57435
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
