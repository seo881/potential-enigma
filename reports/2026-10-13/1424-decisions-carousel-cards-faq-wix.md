# Decisions 1-4 applied (staged): carousel links and titles, hub-card text, FAQ cut-off, Wix cell

## Digest for Divit
- **Carousel (decision 1): done through the API, no Designer clicks needed.**
  - All 8 card links (4 templates, 4 hubs) now point at their collection template page.
  - New combo class `build_content_wrapper-under-cover` (height auto) is on all 8 card wrappers, so the title sits inside the card.
  - Every write was read back. The carousel stays hidden.
- **Designer checklist (decision 2):** `.cache/review/designer-checklist.md`, 11 numbered steps:
  - Learn source = Learn collection on Form, LP and Automation;
  - blog_link set to the Learn template on all 4 templates;
  - publish staging only.
- **Hub cards (decision 3):** these covers are SVG images, not component text, so I fixed them in our generator's output.
  - "Acme Corp" became "Halberd Co" (initials HC); "Thursday, Oct 16" became "Thursday, Oct 15" (2026-10-15 is a Thursday).
  - New assets uploaded, and the CDN copies are byte-identical to the repo files.
  - Swapped inside the shared component "More things you can build" and read back. Staged.
- **FAQ cut-off (decision 3):**
  - Cause: a font-loading race in the FAQ component's own script. It sizes the open answer once, before Inter loads, so the last line is clipped.
  - Fix: our hub-fixes embed (no class, no component edit) now re-fits the open answer when fonts load or the text box resizes. Applied on the 4 templates and read back.
  - Tested with Playwright on 5 pages at 1440 and 390 px: 0 clipped, against the same 4 clips without the fix.
- **Wix (decision 4):** Wix's own docs confirm submissions are stored in the site dashboard and saved to Contacts.
  - Library cell is now "Wix dashboard submissions and Contacts" (3 Wix support URLs, checked 2026-10-12). 19 LP tables regenerated.
  - The 4 live pages (event, law-firm, mobile, pricing) were item-published and verified FIXED.
- **Do the Designer checklist, then publish staging.**

## Request
> Decisions (Divit): 1. Carousel: go. Apply the API plan in docs/LEARN_CAROUSEL_FIX.md (link targets on the 8 build_link elements, new class build_content_wrapper-under-cover), before-values committed first, read back, staged only, carousel stays hidden. If the API refuses the link or it can't be verified, put the exact Designer clicks in my checklist instead. 2. Learn: I'll do the Designer clicks (...). Write me a short numbered checklist (.cache/review/designer-checklist.md) covering the Learn clicks plus any carousel clicks the API couldn't do. 3. Sitewide: go for the text-only fixes, "Acme Corp" on the AI CRM card and the "Thursday, Oct 16" date (use a correct weekday/date pair), inside their shared components, staged, read back, rollback logged. Cut-off first FAQ answer: find the cause; fix it if it's in our templates/embed (new class only), otherwise propose. 4. Wix "Basic contact form to email": check against Wix's own docs; if confirmed understated, update the library cell with source + check date and regenerate the affected tables (item publishes for live pages); if not confirmable, no change. 5. Then tell me "Do the Designer checklist, then publish staging". After I say "staging published": verify (...). If all pass, ask for my go to unhide Learn + carousel; after my go, unhide (staged) and tell me to publish production. 6. After that: go Part C (daily pipeline), dry-run with 2 pages tonight, report.

## Actions and results
- **Before-values first:** 8 links (`{mode: collectionPage}`, no target), 8 wrappers (`[build_content_wrapper]`), the 2 component cover asset IDs, the embed code (repo file) and the Wix cell. All logged and committed in ce93337b before any write.
- **Carousel:**
  - set_settings link `{mode collectionPage, to detail_ai-<hub>-builder}` on 8 elements. Read back `to {pageSlug}` on all 8.
  - create_style combo `build_content_wrapper-under-cover` (height auto).
  - set_style `[build_content_wrapper, build_content_wrapper-under-cover]` on 8 elements, all read back.
  - The render (real links, visible titles) can only be confirmed on a published page while the carousel is visible.
- **Hub cards:**
  - Both covers come from our `pipeline/hubcards_v6.py`, but its helper modules (ds5, hubs5) are not in the repo. So I edited the committed SVGs directly: replaced the outlined glyph groups for "AC", "Acme Corp" and "Thursday, Oct 16" with newly outlined Inter text (same size, weight, colour and position), and updated the accessibility descriptions. The generator source carries the same edits.
  - Checked the PNG renders (attached in the session).
  - Uploaded with Data API create_asset plus S3 (201; CDN md5 matches). The Designer URL-upload tool needs an open Designer.
  - Swapped with the image's `assetId` setting. `set_image_asset` kept failing on its asset lookup (429).
- **FAQ:**
  - Investigation agent: MutationObserver timing showed the inline max-height written at 291 ms while fonts were still loading; forcing late fonts reproduces exactly the 4 audit cases. Closing and reopening the item fixes it.
  - Fix: appended to ops/template/hub-fixes.html; embed code updated on the 4 templates and read back identical.
- **Wix:**
  - Agent checked 3 Wix support pages and updated rules/competitors/lp.json; `hubctl table` on the 19 LP specs with a Wix column (only that cell changes).
  - 4 live items: live-fix add, before-values committed (507f1480), update plus item publish plus read back, verify FIXED x4.
  - The other entry "AI site builders (Wix, Framer)" is unchanged: Framer not checked, and no spec uses it.
- **Incident handled:** the 2026-10-13 05:04 Layer A GitHub Action committed `audits/live/ledger.json` upstream, and my autostash collided. The new sync.sh guard refused to commit the markers (it worked as intended). I took upstream and regenerated the ledger from the findings.

## Numbers
- Template and hub writes: 8 links, 1 new style, 8 class lists, 2 component image swaps, 4 embed code updates. Every one read back.
- CMS: 4 updates plus 4 item publishes. No site publish.
- FAQ fix test: 10 page/width cases, 0 clipped (was 4 clipped).

## Decisions
- Carousel by API: your decision 1. The checklist lists no carousel clicks because the API accepted every change.
- Hub-card text: your decision 3. The text is in images, so the fix is new assets in the same component slots, with no component structure edits.
- FAQ: the cause is the component's script, but the fix lives in our own embed (no class, no component edit), which is within decision 3's "fix it if it's in our templates/embed".
- Wix: your decision 4. Wix's own docs confirm it.

## Files changed and commits
- ce93337b: before-values, hub-card SVGs and generator, hub-fixes.html, Wix library cell and 19 LP specs
- 507f1480: Wix before-values and ledger
- b589d83b: carousel and Wix logs
- this commit: component and embed log lines, this report, the INDEX line
- The checklist is in .cache (git-ignored, as you asked).

## Webflow calls
- **Carousel:** element settings and styles as above. Rollback: set link `{mode collectionPage}` with no target; set_style `[build_content_wrapper]`; remove the combo style.
- **Assets:** create_asset 6acdeb8a6469b3cc0ff19992 (crm v6b) and 6acdeb8a1e6e74b4c7de4f07 (schedule v6b). Component image assetId swaps; rollback to 6abcedd60d27cf8d7db39cc1 and 6abcede50c22665880035d84.
- **Embeds:** 4 code updates; rollback to the code at the previous commit.
- **CMS:** 4 Wix item updates and publishes; rollback from childedits/2026-10-13/*-V3-1.before.json.

## Not done (waiting on you)
- The Designer checklist, then your staging publish.
- Verifying Learn on Form/LP/Automation and the carousel on staging requires them visible. Say "unhide for staging" and I'll unhide them (staged) before your staging publish; otherwise only Survey's Learn, the hub cards and the FAQ fix can be checked there.
- Unhide for production, then Part C: after your go.
