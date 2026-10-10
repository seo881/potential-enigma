# Weekend run report 17 (final)

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

9 pages finished since the last report: 9 reviewed and ready for Divit, 0 parked.

- ready: /ai-landing-page-builder/mobile-landing-page (new)
- ready: /ai-landing-page-builder/video-landing-page (new)
- ready: /ai-automation-builder/data-entry-automation (new)
- ready: /ai-survey-and-quiz-builder/brand-awareness-survey (new)
- ready: /ai-survey-and-quiz-builder/brand-perception-survey (new)
- ready: /ai-survey-and-quiz-builder/church-survey (new)
- ready: /ai-form-builder/therapy-intake-form (rework)
- ready: /ai-form-builder/training-feedback-form (rework)
- ready: /ai-form-builder/volunteer-form (rework)

## Numbers

- Weekend totals: new Auto ready 3, new LP ready 3, new SurveyQuiz ready 3, rework Auto ready 4, rework Form images2 1, rework Form ready 46, rework Form stopped 85, rework LP ready 13, rework SurveyQuiz ready 8, rework SurveyQuiz stopped 1
- Tokens per finished page (logged agents): median 234597, mean 238260, pages with a log 9
  - /ai-automation-builder/data-entry-automation: writer 221249, reviewer 54694
  - /ai-form-builder/therapy-intake-form: writer 116974, reviewer 43966
  - /ai-form-builder/training-feedback-form: writer 128908, reviewer 43966
  - /ai-form-builder/volunteer-form: writer 108801, reviewer 43966
  - /ai-landing-page-builder/mobile-landing-page: writer 183628, reviewer 50969
  - /ai-landing-page-builder/video-landing-page: writer 276621, reviewer 50969
  - /ai-survey-and-quiz-builder/brand-awareness-survey: writer 183048, reviewer 46091
  - /ai-survey-and-quiz-builder/brand-perception-survey: writer 304723, reviewer 46091
  - /ai-survey-and-quiz-builder/church-survey: writer 193587, reviewer 46091
- AlsoAsked credits used this weekend: 25 of 300

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
