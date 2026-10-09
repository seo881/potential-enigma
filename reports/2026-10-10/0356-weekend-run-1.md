# Weekend run report 1

## Request

Divit, 2026-10-10 (WEEKEND RUN): rework the written non-live pages to the 2026-10-09/10 rules, then new pages from the planned queues, hub order LP, Automation, SurveyQuiz, Form; no Webflow tools; AlsoAsked at most 300 credits. Full prompt and rules: `plan/weekend-run.md`. Each iteration's prompt: "Continue the weekend run per plan/weekend-run.md".

**The staging canary happens Monday before anything publishes.** Nothing in this report is in Webflow.

## Actions and results

10 pages finished since the last report: 10 reviewed and ready for Divit, 0 parked.

- ready: /ai-landing-page-builder/app-landing-page (rework)
- ready: /ai-landing-page-builder/coming-soon-page (rework)
- ready: /ai-landing-page-builder/landing-page-seo (rework)
- ready: /ai-landing-page-builder/lead-generation-landing-page (rework)
- ready: /ai-landing-page-builder/one-page-website (rework)
- ready: /ai-landing-page-builder/ppc-landing-page (rework)
- ready: /ai-landing-page-builder/product-landing-page (rework)
- ready: /ai-landing-page-builder/saas-landing-page (rework)
- ready: /ai-landing-page-builder/splash-page (rework)
- ready: /ai-landing-page-builder/squeeze-page (rework)

## Numbers

- Weekend totals: rework Auto autofix 4, rework Form autofix 132, rework LP check2 1, rework LP ready 10, rework LP review 1, rework LP rework 1, rework SurveyQuiz autofix 9
- Tokens per finished page (logged agents): median 171525, mean 166358, pages with a log 10
  - /ai-landing-page-builder/app-landing-page: writer 144955, reviewer 40648
  - /ai-landing-page-builder/coming-soon-page: writer 113065, reviewer 40648
  - /ai-landing-page-builder/landing-page-seo: writer 127648, reviewer 45615
  - /ai-landing-page-builder/lead-generation-landing-page: writer 115430, reviewer 45615
  - /ai-landing-page-builder/one-page-website: writer 145508, reviewer 45615
  - /ai-landing-page-builder/ppc-landing-page: writer 178250, reviewer 40648
  - /ai-landing-page-builder/product-landing-page: writer 129843, reviewer 41682
  - /ai-landing-page-builder/saas-landing-page: writer 108596, reviewer 40649
  - /ai-landing-page-builder/splash-page: writer 89292, reviewer 45615
  - /ai-landing-page-builder/squeeze-page: writer 82585, reviewer 41681
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
