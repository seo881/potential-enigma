# 2026-10-23 1504 quiz embed CLS reservation (B-dev-23)

## Request
Divit, 2026-10-23: ".emgq-mount is created by OUR quiz embed on the SurveyQuiz template, so add the height reservation inside that embed's own code: a <style> with .emgq-mount min-height per breakpoint, measured from the rendered quiz (about 410 px at 1440; measure 768 and 390 too). Update it through the API (before-value committed, read back) the same way as the hub FAQ refit. No component or class edits. Tell me when it's staged and I'll publish staging (webflow.io only)."

## Actions and results
- Embed location: HtmlEmbed 117b49c2-044f-e98e-503d-a5470f7713be on the SurveyQuiz template 6ab24754757025d10940d06a (inserted 2026-10-15, logs/templates.md). Its code is ops/quiz/embed.min.html, built from ops/quiz/embed.html by ops/quiz/build.py. The staging render of team-survey has it byte for byte.
- Measured the mount with Playwright on stand-in pages (the staging team-survey HTML with the style-quiz or vocabulary-quiz carrier injected, the cls.mjs method). The first screen to render is the start screen, and that is what pushes section_stats down:
  - 1440 and 768: 403 px (style) and 438 px (vocabulary).
  - 390: 378 px and 435 px.
  - The first question is 642 to 676 px. It renders only after a click, so the shift has recent input and does not count toward CLS. Reserving that height would leave about 250 px of blank space under the start card, so I reserved the start-screen height instead (Divit's "about 410 px").
- The change is in embed.html and is rebuilt to embed.min.html: `body:has(#awb-quiz-data) .emgq-mount{display:block;min-height:438px}` plus `@media (max-width:479px){... min-height:435px}`.
  - Why the gate: the embed is on every SurveyQuiz page, and `.emgq-mount:empty{display:none}` hides the mount until the quiz renders. A bare `.emgq-mount{min-height}` would either do nothing (still hidden while empty) or, if it overrode the hide, put a blank 438 px block on every survey page.
  - The `:has(#awb-quiz-data)` gate reserves space only on pages whose hero carries the quiz block.
  - build.py's selector check allows exactly that prefix.
- Tests: `node quiz/test_embed.mjs` (run from ops/) passes 2543/0.
  - One expectation changed: badschema (the carrier is present but the data is invalid) now keeps the reserved space. QC Z1 P0 blocks such a page from shipping.
  - One check was added: hero-noquiz takes no space.
- Quiz golden kinds (102 cases): 101 pass. quiz-ship-block-quiz-page has failed since 7d1d6cee (2026-10-16, quiz_template_live true). That failure is not related to this change.
- Webflow: one set_settings on that embed's code key, read back = after-value. Not published.
- Local CLS with the new embed on the stand-in, 5 runs each (data in .cache/quiz/cls-2026-10-23-after.json):
  - style-quiz: 0.00059 at 1440 and 0.00078 at 390, every run.
  - vocabulary-quiz: 0.00053 to 0.00059 at 1440 and 0.00078 at 390.
  - Before the change: 0.059 and 0.036. Pass (< 0.01).

## Numbers
- 148 characters inserted. The embed went from 15095 to 15243 characters (limit 50,000).
- Reserved height: 438 px (480 px and up), 435 px (479 px and below).
- Mount height after the change: start 438/435, results 438 to 500. Non-quiz page: 0.

## Decisions
- Reservation inside our own embed, no component or class edit: Divit's 2026-10-23 instruction above; CLAUDE.md non-negotiables.
- Write path = the hub FAQ refit's (logs/templates.md 2026-10-14/15: before-value in childedits, then MCP data_element_settings set_settings code, then read back).
- NO SITE PUBLISH: CLAUDE.md (Divit 2026-10-10).

## Files changed and commits
- bcefdfde: childedits/2026-10-23/sqb-quiz-embed-117b49c2.before.json, .after.html, ops/quiz/embed.html, embed.min.html, build.py, test_embed.mjs (before-value committed before the write).
- This report's commit: logs/sqb.md, docs/QUIZ.md, this report, reports/INDEX.md.

## Webflow calls
- data_element_tool query_elements (read), data_element_settings_tool get_settings (read before).
- set_settings code on 6ab24754757025d10940d06a / 117b49c2-044f-e98e-503d-a5470f7713be:
  - before md5 255964e1 (15095 chars);
  - after md5 44c2d321 (15243 chars);
  - read back = after.
- Rollback: set_settings code = the before.json value.
- No publish of any kind.

## Not done
- Staging publish (Divit's).
- The post-publish CLS check on webflow.io: run the cls.mjs method on a quiz URL once staging is up. style-quiz and vocabulary-quiz are drafts, so use the stand-in or an item preview.
- The vocabulary-quiz and style-quiz drafts stay unpublished.

## Open questions for Divit
- I gated the reservation on `body:has(#awb-quiz-data)` (reason above) rather than using a bare `.emgq-mount` rule. Keep it?
- Browsers without `:has()` (Firefox before 121) get no reservation, which is the same as today.
