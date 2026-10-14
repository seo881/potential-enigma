# Consolidated template run (ruling 21, Divit 2026-10-14)

Sequence: prepare everything (reads, element IDs, before-values) first; then apply in one tight sequence, committing each before-value first and reading back after each write; then ask for ONE staging publish; then run the staging check; then ask for ONE production publish.

Safe-staged rule: no item is left half-done in the staged state. Each step leaves the template production-safe on its own: unhide a section only after its links, bindings and list pass their read-back. A teammate publish mid-run must ship nothing broken.

Out of scope: shared-component duplicate IDs; the Adwire tag (sitewide; separate decision).

Pages: child templates Form 6aaaaa03995bb2f9f4d6a3c2, LP 6aaaa937fe1a8d180b7c9f90, Automation 6ab2470540448c8f7d1ccc1c, Survey 6ab24754757025d10940d06a. Hubs Form 6aabb4c5789871e91d60f6f9, LP 6aaa658ea6d39733443fe69b, Automation 6ab2464303ee70548366671e, Survey 6ab246c3897d1c09d9d320ec. Learn template 6a0f028d0bfe272031dbddc1.

## Scope

| # | Item | Where (element IDs) | Action | Check |
|---|---|---|---|---|
| 1a | Carousel card link | build_link: Form tpl 24cd8ebc-...-06687, LP tpl d8a90b8f-...-0895c, AAB tpl cadd555f-...-da01, SQB tpl ba847d5e-...-f801; hubs: Form a0031ab3-...-a6bb, LP 993a2e98-...-33ae, AAB 7c8469e8-...-2da7, SQB 07f67163-...-1c57 | `data_element_tool set_link` linkType page = that hub's child template page ID, then designer_tool confirmation (A-wf-3, running) | raw read-back recorded; staging: every card href 200, opens the right item, no `#`, no `detail_` |
| 1b | Card structure | the same 8 lists | build_link wraps the whole card; build_cover bound to Cover Image (16:10, object-fit cover, alt = name); build_title bound to the name, under the cover; category label correct or removed when empty; classes build_link (or build_link Copy as they are), build_cover, build_content_wrapper, build_title; new classes only where needed; equal card heights | staging at 1440, 1024, 768 and 390 px: no overflow, clipping, stretching, broken images or layout shift |
| 1c | List | the 8 Collection Lists | only published items; 15 per page; Load more through intact Finsweet attributes; no duplicates; no "No items found" | staging |
| 1d | Hover and focus | IX3 i-4fd60c05 | the "within" filter, so only the hovered card lifts and zooms; keyboard focus visible | staging |
| 1e | Housekeeping | the hidden first-draft duplicate carousel 86e5ccd1-891e-bb61-1762-8591adc90744 on the AAB and SQB hubs | confirm it is unused (no interactions, no references), then delete it | read-back: gone |
| 1f | Unhide section_build | 4 templates and 4 hubs | only after 1a to 1d read back clean | staging |
| 2 | Learn (section_blog-related) | blog_link: Form 24cd8ebc-...-0666d, LP d8a90b8f-...-08942, AAB cadd555f-...-d9e7, SQB ba847d5e-...-f7e7 | `set_link` page = Learn template 6a0f028d0bfe272031dbddc1; the list shows the 3 newest published Learn articles per item (L12; acrm---learn bound or source Learn, newest 3); fix "No items found" on Form, LP and AAB (backlog); then unhide | every card href 200, images and titles render |
| 3 | Console errors | the 8 new errors ("reading 'sequence'", "reading 'unshift'") | fix the cause (A-dev-4 diagnosing: IX3 or Finsweet targets inside hidden or unhidden sections); no component or existing-class change | 0 console errors on every checked page |
| 3b | landing-page-seo "Illegal return statement" | CMS content of /ai-landing-page-builder/landing-page-seo | fix in the CMS through the API script (ruling 19) | verify-live, 0 console errors |
| 4 | Hub FAQ clip | our own FAQ embed on the 4 hubs | the refit script (staged 2026-10-13 decision 3) | staging: FAQ not clipped at 1440 and 390 px |
| 4b | Empty paragraphs | the 4 hubs (P2 A5-empty-p in hub text); child templates (empty paragraph after feature 1), if template-level | remove | read-back, staging |
| 5 | Quiz embed | SurveyQuiz template, at body level between the hero ba847d5e-...-f5cb and section_stats ba847d5e-...-f630 (re-added; removed 2026-10-14 under the staged-state rule) | only if the zero-footprint check passes before staging | staging: non-quiz pages pixel-identical at 390 and 1280 px; quiz playthrough on vocabulary-quiz and style-quiz |
| 6 | OG image and JSON-LD | the 4 templates | OG image bound to the Share/Thumbnail image; FAQPage JSON-LD matches the visible FAQ | staging: og:image present and 200; JSON-LD parses and matches |
| 7a | Backlog: JSON-LD description HTML-escaped (`&#39;`) | the LP template JSON-LD embed (and the others if the same) | bind plain text or escape for JSON | staging: valid JSON-LD, no entities |
| 7b | Backlog: FAQ heading always "Your Questions, Answered" | the template FAQ section | render the item's heading (window.awbFAQ.heading) | staging |
| 7c | Backlog: comparison tables clip at 390 px | template table container | horizontal scroll container or responsive layout; new class only | staging at 390 px |
| 7d | Backlog: mockup prompts not rendered (awb---mockup-data) | the template mockup | confirm they render once the carousel is back; fix the binding if not | staging |
| 7e | Backlog: hub selected-chip look (hubchip--on) | hubs | confirm on staging only; no change unless broken | staging screenshot |

## Staging check (after Divit's staging publish)

- Every live page and the 4 hubs:
  - every internal href 200, template links included (upgraded verify-live);
  - 0 console errors;
  - FAQ not clipped;
  - og:image and JSON-LD present.
- Carousel and Learn checks at 1440 and 390 px.
- Pixel diff against the pre-publish baseline on pages that should not change.
- Quiz playthrough on the 2 canary quiz pages.
- Screenshots for Divit at true size, 1440 and 390 px: one hub carousel, plus one template's carousel and Learn section.
- Any failure: fix it, then ask for one more staging publish. When everything passes, ask for the production publish. After it: the live audit on everything, and verify-live on all live pages.

## Order of writes (addendum, Divit 2026-10-14)

Rules: one agent on the Designer at a time, one page at a time, with no parallel Designer writes and one reused session (ses_3KdRZfKThMwzr1r57LsQEq1dI5W). Navigate to each page with switch_page and confirm get_current_page; never assume the open page. Read back after every write through both the Data API and designer_tool, and stop on any mismatch. KS (a teammate) is in the Designer too: if a page shows changes that are not ours, or another user is on it, stop and report.

0. **Snapshot:** get_all_elements on the 4 templates and 4 hubs, plus the raw settings of every element to be touched, into childedits/2026-10-14/template-run/<page>.tree.json. Commit and push before any write. This is the rollback.
1. **Card links**, 12 (A-wf-3): set_link page mode to the template page ID, then confirmation in the Designer (Page link to the Template), with both-way read-back.
2. **Carousel**, page by page (template, then its hub):
   - the build_link wraps the card;
   - build_cover bound to Cover Image (16:10, object-fit cover);
   - build_title bound to the name;
   - category label fixed or removed;
   - classes, including new equal-height classes;
   - the list: published only, 15 per page, Finsweet Load more intact;
   - the IX3 i-4fd60c05 "within" filter, and visible focus.
   Both-way read-back per page.
3. **Delete the hidden duplicate carousel** 86e5ccd1-891e-bb61-1762-8591adc90744 on the AAB and SQB hubs, after confirming it is unused.
4. **Learn list** (source, newest 3, no "No items found") on Form, LP and AAB; SQB checked.
5. **Console-error fix**, per A-dev-4's diagnosis, with no component or existing-class edits.
6. **Hub FAQ refit embed** on the 4 hubs; remove the empty paragraphs on the hubs and the template-level one after feature 1.
7. **OG image binding** checked or fixed on the 4 templates; JSON-LD description escaped; FAQPage JSON-LD matches; FAQ heading taken from the item; table 390 px fix.
8. **Quiz embed** on the SurveyQuiz template, last and only after its zero-footprint check passes.
9. **Final both-way read-back** of every touched element; a check that each section that is visible has passed its checks; then the staging-publish request to Divit.

Any step that cannot finish clean is rolled back to its snapshot before moving on, so the staged state stays production-safe at every point.

## KS header work (Divit 2026-10-14, 5:59 PM)

- KS (Webflow developer) is changing the header; nothing is published until he is done.
- A asks Divit for no publish (staging or production) until Divit says KS's header is done. When the staged run is complete and read back, A tells Divit "ready for staging" with the check plan, and Divit coordinates the single publish with KS.
- Never touch the header, navbar or any shared component. Header or navbar changes in snapshots or read-backs are KS, not drift: never revert them.
- Pixel-diff baseline: taken only after KS is done, or with the header region masked. The staging check still confirms the header renders on our pages with 0 console errors.
