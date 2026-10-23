# Slug migration: the calls for Divit (2026-10-23)

Rule (DECISIONS 2026-10-23 SLUG MIGRATION): a child slug is only the page's own name, with no category word anywhere in it. Map: `plan/slug-migration.json`, built by `ops/slug_migrate.py map` from a fresh read of all 4 collections (GET only; nothing was written in Webflow).

## Totals

Live = the items in Webflow now (339). Planned = pages named in specs, status, the queue or additions that aren't in Webflow yet (280). Another 21 pages appear only in the git-ignored keyword map. They are mapped in `private/migration/`, and one of them needs a call.

| Hub | Live: unchanged | Live: auto-mapped | Live: class call | Live: needs a call | Planned: auto / class / call |
|---|---|---|---|---|---|
| LP (73) | 0 | 63 | 8 | 2 | 43 / 2 / 0 |
| Form (131) | 13 | 111 | 0 | 7 | 152 (+6 unchanged) / 0 / 1 |
| Auto (76) | 2 | 45 | 26 | 3 | 15 / 0 / 0 |
| SurveyQuiz (59) | 3 | 47 | 0 | 9 | 55 / 0 / 6 |

The checks ran on every new slug:
- No new slug is a duplicate within its collection.
- No new slug clashes with a current slug or any of the 4,843 sitemap paths, and none matches a hub path.
- None is a reserved word.
- Bare single words such as feedback, payment, sales and video are accepted. The hub path carries the meaning, the same way /ai-website-builder/video does.

## Two class rulings (one answer each)

| Class | Pages | Proposed | Recommendation |
|---|---|---|---|
| Auto "-workflow" | 26 live: 16 already end in -workflow (approval-workflow, sales-workflow, ...), 9 are "X-workflow-automation" and become "X-workflow", and marketing-automation-workflow becomes marketing-workflow (the category word sat in the middle) | Treat "workflow" as not the category word | **Keep "workflow".** Stripping it leaves generic stems (approval, content, sales, audit, legal) and collides with sales-automation becoming sales. A workflow is the page's own thing, the way a thank-you page is in LP. |
| LP "-page" types | 8 live (404-page, coming-soon-page, maintenance-page, pricing-page, splash-page, squeeze-page, thank-you-page, one-page-website) + 2 planned | Unchanged | **Keep.** Only "landing-page" is the category word. Stripping "page" would leave 404 (a number) and pricing (the same name as /pricing). |

## Pages needing your call

| Hub | Old | Proposed new | Issue | Recommendation |
|---|---|---|---|---|
| LP | category-landing-page | category | reads as an archive page | product-category |
| LP | landing-page-seo | seo | category word was at the start | accept seo |
| Form | contact-form | contact | generic (your example) | accept contact (the head term) |
| Form | order-form | order | generic (your example) | accept order; variants keep their qualifier (cake-order, purchase-order) |
| Form | sign-up-form | sign-up | reads as the site's sign-up | accept sign-up |
| Form | sign-in-form | sign-in | reads as the site's login | visitor-sign-in |
| Form | sign-out-form | sign-out | reads as logout | staff-sign-out |
| Form | checkout-form | checkout | reads as a cart checkout (the page tracks who has each item) | equipment-checkout |
| Form | interest-form | interest | reads as financial interest | interest-list |
| Form (planned) | approval-form | approval | generic (your example) | approval-request |
| Auto | it-automation | it | pronoun (your example) | it-operations |
| Auto | automated-inventory-management | unchanged | "automated" is the category word as an adjective | inventory-management |
| Auto | automated-loan-processing-system | unchanged | same | loan-processing |
| SQ | 360-survey | 360 | bare number (your example) | 360-feedback |
| SQ | it-survey | it | pronoun | it-support |
| SQ | pricing-survey | pricing | same name as /pricing | price-testing |
| SQ | style-quiz | style | ambiguous | personal-style |
| SQ | funny-survey-questions | funny | stripping "survey-questions" in the middle leaves an adjective | funny-questions |
| SQ | likert-questionnaire | unchanged | "questionnaire" is a survey synonym | likert-scale |
| SQ | team-survey / team-quiz (planned) | team / team | survey/quiz collision; generic | live survey takes team; quiz takes team-trivia |
| SQ | safety-survey / safety-quiz (planned) | safety / safety | survey/quiz collision | live survey takes safety; quiz takes safety-knowledge-check |
| SQ | wellness-survey / wellness-quiz (planned) | wellness / wellness | survey/quiz collision | live survey takes wellness; quiz takes wellness-check |
| SQ (planned) | quiz-funnel | funnel | category word was at the start and is the concept | accept funnel |
| SQ (planned) | matching-quiz-maker | matching-maker | "maker" is left dangling | matching |
| SQ (planned) | survey-questionnaire | questionnaire | only a synonym of the hub's head term is left | park it (the hub page owns the term) |
| SQ (keyword map only) | 1 page, see private/migration/slug-migration-kmap.json | | bare stem is ambiguous | decide with the rest |

Not flagged: poll-questions and yes-no-questions-survey, which becomes yes-no-questions. "questions" and "poll" are not category words.

## For steps 3 to 5

- **Redirects by API: no on this site.** The webflow MCP `data_enterprise_tool` has `create_301_redirect`, `list_301_redirects`, `update_301_redirect` and `delete_301_redirect`. A read-only `list_301_redirects` on site 6a0edf12 returned: "This site does not have an Enterprise hosting plan. This action requires an Enterprise site plan." The Data API v2 redirect endpoints have the same Enterprise gate, and `ops/webflow_api.py` has no redirect path. So the 301s go in by hand: Site settings > Publishing > 301 redirects (bulk CSV import is available there).
- **Hard-coded internal links to child pages:**
  - **Live CMS:** 891, all in `awb---faq-data` (FAQ answers): LP 201, Form 319, Auto 218, SQ 153, across 335 items. 764 of them point at a slug that changes.
  - **Specs** (`specs/*/*.json`, not archived): 2,094 matches in 416 files. 1,131 are rendered FAQ links (`fields.faq`) and 2 more sit in `faq_plan.a`. Link plans account for 908 (`faq_plan.link.url` 799, `pending_links.target` 109). The remaining 53 are notes in review and history, which need no rewrite.
  - **Elsewhere:** the 4 hub pages link to children only through collection lists (15 each, all dynamic), so they update by themselves. Other repo files hold URL lists, not page content: plan/queue-ranked.txt, plan/additions.json, plan/overrides.json, plan/batches/*.txt, pipeline/briefs/*.json, status/*.json, and the golden test fixtures.
  - **Not checked:** links from other collections (Learn, other build hubs) and from static pages outside the 4 hubs.
- Re-run after any new read: `hubctl api-read <HUB>` x4, then `.venv/bin/python3 ops/slug_migrate.py inventory && ... map && ... links`.
