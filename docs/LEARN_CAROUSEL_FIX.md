# Learn list and carousel: causes and fix plan (read-only investigation, 2026-10-12)

> **Correction (Divit, 2026-10-13; DECISIONS 2026-10-13), which supersedes section A's Designer clicks below.** The source stays on each item's own "... - Learn" multi-reference field (Divit verified the Form source shows "AFB - Learn"). Never switch it to the Learn collection. The fix is data, not design:
> - Each child item's `acrm---learn` holds the 3 newest published Learn articles. The 39 live items were filled on 2026-10-13 and booking-form already had them. New items get them at creation (L12, config/learn_refs.json).
> - The card link `blog_link` is a collection-page link to `detail_learn` on all 4 templates. The advisor set Form, LP and Automation; B set Survey on 2026-10-13 (read back, logs/templates.md).
> - The cause stands: the lists read an empty field. The remedy changed from "switch the source" to "fill the field".
> - Section B (carousel) was applied by API on 2026-10-13 (logs/templates.md).

Both sections are hidden on production-bound templates (logs/templates.md, 2026-10-12 pre-production hide). Nothing below has been applied, and nothing is unhidden without Divit's go. All element IDs are `{component: <page id>, element: <id>}`.

## A. Learn list "No items found" (Form, LP, Automation templates)

**Cause: confirmed by elimination; the API cannot show it directly.** The three cloned lists are sourced from the item's own Learn multi-reference field, not from the Learn collection.

Evidence:
1. **API settings are identical.** Read via get_settings all_raw_settings and query_settings, the Form list `24cd8ebc-23b4-d766-1f9f-0d648fc0666a` and the Survey list `ba847d5e-85b3-fe51-eadf-ad4eebacf7e4` match exactly:
   - source `{collectionId: 6a0f028d0bfe272031dbddb8}` (Learn), type `collectionListSetting`, canBind false;
   - dynamic, no filters, sort learn---publishing-date descending, limit 3, offset 0;
   - no curated items.

   The API reports the source as a collection id only, so a list fed by a multi-reference field (whose target collection is also Learn) reads exactly the same.
2. **Every collection has the field.** All 4 child collections have a MultiReference field to Learn:
   - AFB - Learn 3c917f46426f105df5cc4b2c2cb7b494
   - ALPB - Learn e6eebe5d973e379ff830aa307e2597fb
   - AATB - Learn c2a4fee65310910ae503881010fba5e2
   - ASQB - Learn c56102510eaa0d01c26127d7d4a6a02a
3. **The field is empty on every live item.** Only two draft items (creator-application, thank-you-page) have Learn refs, per the 2026-10-12 read-back.
4. **The rendered results only fit one explanation.** Survey items with zero Learn refs (e.g. employee-engagement-survey) render the 3 newest Learn articles, so Survey's list reads the Learn collection. Form, LP and Automation items with zero refs render only `w-dyn-empty` ("No items found").
   - With no filters and limit 3, a list sourced from the Learn collection cannot be empty while Learn has published items, which Survey proves in the same publish.
   - The only source that gives an empty list on these items is the empty multi-reference field.
   - The 2026-10-12 API re-save rewrote the same `{collectionId}` and could not change this, which is why it had no effect.

Designer clicks, once per template: Form `AI Form Builder 📄 Template` (detail_ai-form-builder), LP `AI Landing Page Builder 📄 Template`, Automation `AI Automation Builder 📄 Template`.
1. Open the template page. In the Navigator, select section_blog-related > container-large > the Collection List Wrapper `blog_list-wrapper` (it is hidden: turn on "Show hidden elements" in the Navigator, or temporarily reveal it).
2. Open the Collection List settings panel (gear icon / Settings tab).
3. Under **Source**, the dropdown will show the multi-reference field (e.g. "AFB - Learn" under the current item). Change it to **Learn** under **Collections**: the plain collection, not the item's field.
4. Re-apply what Survey has, because changing the source resets them:
   - Sort orders: Publishing date, newest first (learn---publishing-date, descending).
   - Limit items: Show 3 items, start at 1.
   - Filters: none.
5. Re-check the item bindings inside the list (image = Learn image, title = Learn title, date, category). Changing the source can drop them; re-bind any that show a purple "not connected" badge.
6. **Learn card link (also broken on Survey).** The `blog_link` on Survey renders `href="#"` too: the cards show but go nowhere. On all 4 templates select `blog_link` > Link settings > **Collection Page** and pick the **Learn template page**, the same page the /learn cards use.
7. Save. Do not unhide yet; Divit unhides after a staging check.

## B. Carousel (section_build) on the 4 templates and 4 hubs

### Comparison with the working carousel

The working carousel is on the AI app builder template 6a1d7bb928f573297633690a (live /ai-app-builder/vedic-astrology and the /ai-app-builder hub).

| Part | Working (AI app builder) | Ours (4 templates, 4 hubs) |
|---|---|---|
| Structure | Collection List `build_list-wrapper` > `build_list` > `build_item` > Link block `build_link` > `build_content_wrapper` > `build_content` (h2 `build_title` + category) + arrow, then a hidden category div | Same, plus our `img.build_cover` inserted as the first child of `build_link` (T5) |
| Link (rendered) | `href="/ai-app-builder/real-estate"` | `href="#"` on every card |
| Link (API raw) | `{mode: "collectionPage"}` | `{mode: "collectionPage"}` (identical; the target page is not exposed) |
| Title | h2 `build_title` bound to Product name | h2 `build_title` bound to the item's Product name (Form: AFB - Product name 8981ffa572ed9836c1f93391014c61b6). In the HTML: "Order Form Builder", etc. |
| Short description | none visible: `text-block-2` (fs-list-field category) is display:none | same; the design has no visible description slot |

### Why "the link is #"

The link mode is collectionPage, but the target page did not carry over when the section was cloned. A collection-page link that doesn't point at the template of the list's own collection renders `#`. The API reads the same `{mode}` on ours and the working card, so it cannot confirm the stored target. The fix is to set the target explicitly.

### Why "the title isn't shown"

The title is bound and present in the HTML. It renders **outside the card**. In Chromium on staging at 1440 px, the card link box is 312 px tall: the cover takes 240 px plus margin, then `build_content_wrapper` starts at y=249. The wrapper's class `.build_content_wrapper` has `height:100%; align-items:center` from the original design, made for a card with no image. With the cover above it, the full-height wrapper is pushed down by the cover's height, and the title lands at y≈394, below the card's bottom edge (313). The working card has no cover; its wrapper is 64 px tall and the title sits inside.

### API plan (not applied; each write needs Divit's go, with before-values committed first)

1. **Link target.** data_element_settings_tool > set_settings on each `build_link`, setting `{key: "link", static_link: {mode: "collectionPage", to: "<template page slug>"}}`. The schema says collectionPage takes a page slug.
   - Template slugs, all four confirmed with get_page_metadata (2026-10-12): Form `detail_ai-form-builder`, LP `detail_ai-landing-page-builder`, Automation `detail_ai-automation-builder`, Survey `detail_ai-survey-and-quiz-builder`.
   - Uncertain: whether the API accepts this for a Link inside a Collection List. If it is refused or still renders `#` on staging, use the Designer clicks below.

   | Page | Link element | Target slug |
   |---|---|---|
   | Form template 6aaaaa03995bb2f9f4d6a3c2 | 24cd8ebc-23b4-d766-1f9f-0d648fc06687 | detail_ai-form-builder |
   | LP template 6aaaa937fe1a8d180b7c9f90 | d8a90b8f-142b-5c77-eae7-a06e09b0895c | detail_ai-landing-page-builder |
   | Automation template 6ab2470540448c8f7d1ccc1c | cadd555f-249f-2bfd-b8af-165dc634da01 | detail_ai-automation-builder |
   | Survey template 6ab24754757025d10940d06a | ba847d5e-85b3-fe51-eadf-ad4eebacf801 | detail_ai-survey-and-quiz-builder |
   | Form hub 6aabb4c5789871e91d60f6f9 | a0031ab3-d167-ad84-c89c-90a14c07a6bb | detail_ai-form-builder |
   | LP hub 6aaa658ea6d39733443fe69b | 993a2e98-59bb-16c2-a552-a805b88a33ae | detail_ai-landing-page-builder |
   | Automation hub 6ab2464303ee70548366671e | 7c8469e8-95dd-19f9-811e-e6276d9b2da7 (confirmed) | detail_ai-automation-builder |
   | Survey hub 6ab246c3897d1c09d9d320ec | 07f67163-1778-b5f9-55e1-26f8141b8c57 (confirmed) | detail_ai-survey-and-quiz-builder |

   Note: the Automation and Survey hub IDs were confirmed with query_elements `{style: "build_link"}` (content wrappers 7c8469e8-...-2d9a9 and 07f67163-...-8c59).
2. **Title placement.** Use a new class only; no edit to `.build_content_wrapper` or any existing class.
   - Create one new style `build_content_wrapper-under-cover` (data_style_tool) with `height: auto`.
   - Add it as a second class to each card's content wrapper with set_style `["build_content_wrapper", "build_content_wrapper-under-cover"]`. set_style replaces the class list, so pass both.
   - Wrappers: Form template 24cd8ebc-...-0d648fc06688, LP template d8a90b8f-...-a06e09b0895d, Automation template cadd555f-...-165dc634da02, Survey template ba847d5e-...-ad4eebacf802, Form hub a0031ab3-...-90a14c07a6bd, LP hub 993a2e98-...-a805b88a33b0, Automation hub 7c8469e8-...-e6276d9b2da9 (derived), Survey hub 07f67163-...-26f8141b8c59 (derived).
   - Alternative with no class work: a scoped rule `.section_build .build_cover + .build_content_wrapper{height:auto}` in our own hub-fixes embed on the 4 templates, plus a new embed in each hub's section_build. That overrides an existing class's property without editing the class itself; it needs Divit's ruling.
3. **Title binding:** already correct on all 4 (Product name); no change.
4. **Short description:** there is no visible slot in the design (`text-block-2` is display:none in both carousels), so nothing to bind. The Survey cards' hidden category slot is bound to a description-like field (it shows "Build an Employee Satisfaction Survey Scored by Topic"); harmless while hidden.

### Designer clicks (if the API refuses the link target)

On each of the 4 templates and 4 hubs:
1. Open the page; in the Navigator, select section_build > build_list-wrapper > build_item > **build_link** (show hidden elements).
2. Element settings (gear) > Link settings > choose the **Collection Page** tab/icon > from the dropdown pick this hub's template ("AI Form Builder 📄 Template", "AI Landing Page Builder 📄 Template", "AI Automation Builder 📄 Template" or "AI Survey and Quiz Builder 📄 Template"). It must match the list's source collection: on a hub, the list's collection; on a template, the same collection.
3. For the title: select build_content_wrapper > Selector field > add the new class `build_content_wrapper-under-cover` (with height Auto). Do this once, then on the other 7 wrappers just add the existing combo.
4. Save, publish to staging (Divit), then verify: every card links to /<hub>/<slug>, the title sits inside the card at 1440 px and 390 px, and the cover alt is non-empty.

## Uncertain
- A is confirmed by elimination; the Designer's Source dropdown will show the field name directly when opened.
- Whether set_settings `link` collectionPage + `to: <slug>` works through the API for a link inside a Collection List.
- (Resolved 2026-10-12: template slugs and the Automation and Survey hub element IDs confirmed by reads.)
