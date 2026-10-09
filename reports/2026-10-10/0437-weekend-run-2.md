# Weekend run report 2

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

10 pages finished since the last report: 10 reviewed and ready for Divit, 0 parked.

- ready: /ai-landing-page-builder/b2b-landing-page (rework)
- ready: /ai-landing-page-builder/campaign-landing-page (rework)
- ready: /ai-landing-page-builder/real-estate-landing-page (rework)
- ready: /ai-automation-builder/accounts-payable-automation (rework)
- ready: /ai-automation-builder/invoice-automation (rework)
- ready: /ai-automation-builder/purchase-order-automation (rework)
- ready: /ai-automation-builder/social-media-automation (rework)
- ready: /ai-survey-and-quiz-builder/customer-feedback-survey (rework)
- ready: /ai-survey-and-quiz-builder/employee-satisfaction-survey (rework)
- ready: /ai-survey-and-quiz-builder/pulse-survey (rework)

## Numbers

- Weekend totals: rework Auto ready 4, rework Form autofix 132, rework LP ready 13, rework SurveyQuiz images 4, rework SurveyQuiz ready 3, rework SurveyQuiz rework 1, rework SurveyQuiz writer 1
- Tokens per finished page (logged agents): median 182091, mean 178360, pages with a log 10
  - /ai-automation-builder/accounts-payable-automation: writer 117181, reviewer 41078
  - /ai-automation-builder/invoice-automation: writer 111444, reviewer 41078
  - /ai-automation-builder/purchase-order-automation: writer 147503, reviewer 41078
  - /ai-automation-builder/social-media-automation: writer 153891, reviewer 41077
  - /ai-landing-page-builder/b2b-landing-page: writer 140409, reviewer 41682
  - /ai-landing-page-builder/campaign-landing-page: writer 111962, reviewer 65708
  - /ai-landing-page-builder/real-estate-landing-page: writer 171637, reviewer 41682
  - /ai-survey-and-quiz-builder/customer-feedback-survey: writer 132038, reviewer 67239
  - /ai-survey-and-quiz-builder/employee-satisfaction-survey: writer 85197, reviewer 67239
  - /ai-survey-and-quiz-builder/pulse-survey: writer 97243, reviewer 67238
- AlsoAsked credits used this weekend: 0 of 300

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
