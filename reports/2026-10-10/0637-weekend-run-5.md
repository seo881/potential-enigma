# Weekend run report 5

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

10 pages finished since the last report: 8 reviewed and ready for Divit, 2 parked.

- ready: /ai-form-builder/emergency-contact-form (rework)
- ready: /ai-form-builder/field-trip-permission-slip (rework)
- ready: /ai-form-builder/independent-contractor-agreement (rework)
- ready: /ai-form-builder/nda-form (rework)
- ready: /ai-form-builder/patient-intake-form (rework)
- ready: /ai-form-builder/photo-release-form (rework)
- ready: /ai-form-builder/purchase-order-form (rework)
- ready: /ai-form-builder/work-order-form (rework)
- parked: /ai-form-builder/parent-consent-form (rework): writer failed twice: gate 5/10: PA11, PA3, PA1, PA4, PA10
- parked: /ai-form-builder/vehicle-inspection-form (rework): writer failed twice: PA4 PA3 PA11: gate 0/10, head term on wrong-sense list

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 101, rework Form check 2, rework Form images 2, rework Form ready 23, rework Form rework 1, rework Form stopped 2, rework Form writer 1, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 173764, mean 164303, pages with a log 10
  - /ai-form-builder/emergency-contact-form: writer 129527, reviewer 39493
  - /ai-form-builder/field-trip-permission-slip: writer 141702, reviewer 39945
  - /ai-form-builder/independent-contractor-agreement: writer 143229, reviewer 39945
  - /ai-form-builder/nda-form: writer 113959, reviewer 39945
  - /ai-form-builder/parent-consent-form: writer 194689
  - /ai-form-builder/patient-intake-form: writer 104720, reviewer 39493
  - /ai-form-builder/photo-release-form: writer 139298, reviewer 39096
  - /ai-form-builder/purchase-order-form: writer 128111, reviewer 39493
  - /ai-form-builder/vehicle-inspection-form: writer 96622
  - /ai-form-builder/work-order-form: writer 133819, reviewer 39945
- AlsoAsked credits used this weekend: 10 of 300

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
