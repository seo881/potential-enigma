# Weekend run report 6

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

10 pages finished since the last report: 4 reviewed and ready for Divit, 6 parked.

- ready: /ai-form-builder/complaint-form (rework)
- ready: /ai-form-builder/incident-report-form (rework)
- ready: /ai-form-builder/new-employee-form (rework)
- ready: /ai-form-builder/reasonable-accommodation-request-form (rework)
- parked: /ai-form-builder/anonymous-feedback-form (rework): writer failed twice: PA11 PA3 (gate 2/10, source-starved)
- parked: /ai-form-builder/employee-availability-form (rework): writer failed twice: PA11 PA12 (gate 3/10, source-starved)
- parked: /ai-form-builder/lead-capture-form (rework): writer failed twice: PA11, PA14, PA8, PA3: gate 5/10, no allowed replacements
- parked: /ai-form-builder/medical-history-form (rework): writer failed twice: PA11 PA3 PA1 (gate 5/10)
- parked: /ai-form-builder/payment-form (rework): writer failed twice: PA11 PA1 PA3 F2 (gate 7/10, QC 1)
- parked: /ai-form-builder/vendor-application (rework): writer failed twice: PA11 PA3 (gate 3/10, source-starved)

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 84, rework Form images 8, rework Form images2 1, rework Form ready 27, rework Form review 1, rework Form stopped 8, rework Form writer 3, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 161934, mean 139369, pages with a log 10
  - /ai-form-builder/anonymous-feedback-form: writer 80043
  - /ai-form-builder/complaint-form: writer 126735, reviewer 39877
  - /ai-form-builder/employee-availability-form: writer 85208
  - /ai-form-builder/incident-report-form: writer 146832, reviewer 39877
  - /ai-form-builder/lead-capture-form: writer 125435
  - /ai-form-builder/medical-history-form: writer 172859
  - /ai-form-builder/new-employee-form: writer 122057, reviewer 39877
  - /ai-form-builder/payment-form: writer 120137
  - /ai-form-builder/reasonable-accommodation-request-form: writer 157836, reviewer 39877
  - /ai-form-builder/vendor-application: writer 97047
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
