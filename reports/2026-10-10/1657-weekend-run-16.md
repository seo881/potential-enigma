# Weekend run report 16

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

10 pages finished since the last report: 10 reviewed and ready for Divit, 0 parked.

- ready: /ai-landing-page-builder/ebook-landing-page (new)
- ready: /ai-automation-builder/incident-response-automation (new)
- ready: /ai-automation-builder/procurement-automation (new)
- ready: /ai-form-builder/expense-report-form (rework)
- ready: /ai-form-builder/fitness-assessment-form (rework)
- ready: /ai-form-builder/proposal-form (rework)
- ready: /ai-form-builder/referral-form (rework)
- ready: /ai-form-builder/requisition-form (rework)
- ready: /ai-form-builder/restaurant-reservation-form (rework)
- ready: /ai-form-builder/sponsorship-form (rework)

## Numbers

- Weekend totals: new Auto ready 2, new Auto rework 1, new LP ready 1, new LP review 2, new SurveyQuiz review 3, rework Auto ready 4, rework Form images2 1, rework Form ready 43, rework Form review 3, rework Form stopped 85, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 213353, mean 196475, pages with a log 10
  - /ai-automation-builder/incident-response-automation: writer 186858, reviewer 54694
  - /ai-automation-builder/procurement-automation: writer 299671, reviewer 54693
  - /ai-form-builder/expense-report-form: writer 69546, reviewer 40396
  - /ai-form-builder/fitness-assessment-form: writer 172957, reviewer 40396
  - /ai-form-builder/proposal-form: writer 193724, reviewer 41018
  - /ai-form-builder/referral-form: writer 51504, reviewer 33302
  - /ai-form-builder/requisition-form: writer 116252, reviewer 33302
  - /ai-form-builder/restaurant-reservation-form: writer 106829, reviewer 33302
  - /ai-form-builder/sponsorship-form: writer 116513, reviewer 33302
  - /ai-landing-page-builder/ebook-landing-page: writer 235531, reviewer 50969
- AlsoAsked credits used this weekend: 22 of 300

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
