# Weekend run report 14

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

11 pages finished since the last report: 6 reviewed and ready for Divit, 5 parked.

- ready: /ai-form-builder/accident-report-form (rework)
- ready: /ai-form-builder/address-verification-form (rework)
- ready: /ai-form-builder/background-check-form (rework)
- ready: /ai-form-builder/driver-application-form (rework)
- ready: /ai-form-builder/event-planning-form (rework)
- ready: /ai-form-builder/home-care-intake-form (rework)
- parked: /ai-form-builder/anesthesia-consent-form (rework): writer failed twice: PA11 PA12 PA1 PA3: no replacement source
- parked: /ai-form-builder/car-rental-form (rework): writer failed twice: PA11 PA4: head word on PA4 wrong-sense list, 0/10 by construction
- parked: /ai-form-builder/chemical-peel-consent-form (rework): writer failed twice: PA11 PA3: no replacement source
- parked: /ai-form-builder/employee-referral-form (rework): writer failed twice: PA11 PA3: no replacement source
- parked: /ai-form-builder/rental-history-form (rework): writer failed twice: PA11 PA3: no replacement source, 3/10 reachable

## Numbers

- Weekend totals: rework Auto ready 4, rework Form images2 1, rework Form ready 33, rework Form review 11, rework Form rework 2, rework Form stopped 85, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 106044, mean 119617, pages with a log 11
  - /ai-form-builder/accident-report-form: writer 138233, reviewer 42378
  - /ai-form-builder/address-verification-form: writer 103838, reviewer 42378
  - /ai-form-builder/anesthesia-consent-form: writer 106044
  - /ai-form-builder/background-check-form: writer 62181, reviewer 42378
  - /ai-form-builder/car-rental-form: writer 82928
  - /ai-form-builder/chemical-peel-consent-form: writer 62285
  - /ai-form-builder/driver-application-form: writer 112309, reviewer 42378
  - /ai-form-builder/employee-referral-form: writer 64506
  - /ai-form-builder/event-planning-form: writer 107571, reviewer 40396
  - /ai-form-builder/home-care-intake-form: writer 129830, reviewer 40396
  - /ai-form-builder/rental-history-form: writer 95758
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
