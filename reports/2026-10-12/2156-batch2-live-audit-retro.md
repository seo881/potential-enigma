# Batch-2 live: 40 pages verified on emergent.sh, relinked, live audit with 74 fixes, retro; publish-watch gap fixed

## Digest for Divit
- **All 40 child pages are live and pass verification on emergent.sh:** the 18 from your 13:39 UTC publish, the 2 canaries item-published afterwards, and the 20 from batch-1.
  - verify_launch: 40 pages, 4 templates, 4 hubs, 0 failing (after all fixes). Learn is hidden on Form/LP/Automation and the carousel is hidden everywhere. FAQ, chips, tables at 390 px, og and links all pass.
  - verify-live passes on all 40, and all are in state published.
- **Relink:** 10 live items now link to pages that went live today (FAQ link-only diffs, item publishes, read back exact). contact-form stays held.
- **Live audit (fixes on, item publishes only):** Layer A plus a full Layer B read of all 40 pages (10 reviewers). 74 writer fixes on 30 live pages, every one item-published and verified (read-back exact plus a fresh Layer A). 0 rolled back.
  - **P0 fixed:** event and webinar landing pages had a grouped "Landingi / Leadpages / Instapage" column whose "tiered by traffic" cell was false for Leadpages. Each now has single vendors that rank for its query.
  - **Stock names on 12 live pages, now gone:** Northwind, Globex, Initech and Acme, in copy and images. Reused persona and business names were replaced on 25 pages.
  - Claims tightened (church "Why Churches Run Surveys on Emergent", liability waiver, direct deposit, document automation). Serial commas restored. Credit-card FAQ 7 now gives a sourced 120-day dispute window.
- **Publish-watch gap:** the 10:05 UTC publish was seen at 10:29, but the audit was skipped twice ("git pull failed" on a dirty checkout), then rated the broken Learn and carousel P1.
  - Fix: a read-only smoke check runs first on every new stamp (no git, no Claude) and raises a macOS alert on failure.
  - Template regressions are now P0 and lead the digest. 3 golden cases added, plus a LESSONS line.
- **Retro batch-2:** written (status/metrics.md, LESSONS). The retro tool is now batch-aware; it had reported "2000%".
- **A and B, read-only:** causes confirmed, with the Designer clicks in docs/LEARN_CAROUSEL_FIX.md (summary below). Nothing unhidden.

## Request
> Option 1: emergent.sh site-published by Divit just now. Verify all 38 live pages + 4 hubs (Learn hidden on Form/LP/Automation, carousel hidden everywhere, FAQ heading, tables, chips), relink, live audit with fixes on (item publishes only), retro. If all pass, item-publish the 2 canaries (ebook-landing-page, employment-verification-letter), verify them live, relink. Then continue A and B read-only; nothing unhidden without my go.
> Also: production was site-published at 10:05:51 UTC today outside the plan (not by Claude). Check why the publish watcher didn't catch the broken Learn/carousel within 30 minutes and fix that gap; add a LESSONS line.

## Actions and results
1. **Verify (13:39 UTC publish).**
   - verify_launch on 38 pages and 4 hubs: 0 failing.
   - FAQ heading data and embed on 38/38. Tables at 390 px on 5 pages across the 4 hubs: scroll inside the frame, sticky label column, no page overflow.
   - verify-live: 38/38 pass, state published.
2. **Relink.**
   - New `hubctl relink-payload` sends only fields whose difference is exactly the restored links, and refuses drift.
   - 10 items: before-values committed (abd5ebff), update read back exact, item publishes, verify-live pass.
   - task-automation, interest-form and event-landing-page already carried their links.
3. **Canaries.** isDraft false (fields unchanged), item publish, verify_launch plus verify-live PASS. No live page had a pending link to them.
4. **Live audit.**
   - The publish watcher had started its own unattended audit in the same checkout at 13:40 UTC. I stopped mine to avoid two writers (and killed my orphaned browser process), let the watcher's run end (it could not call Webflow), then ran Layer A once on all 40 pages.
   - Two checker fixes, then re-scored the same capture with the new `--from-raw` option:
     - the sitemap check now follows the new sitemap index (40 false P1s);
     - IDs no longer trip the repeated-word rule ("job JOB-4471").
   - Layer A after re-scoring: 1 P1 (the third-party Adwire console error) and 44 old P2s.
   - Layer B: 10 page-reviewers, 320 findings recorded.
   - Fixes:
     - 10 page-writers with disjoint name-letter ranges, 30 pages. QC 0, ship-qc 0 and gate 10/10 re-checked by me on all 30.
     - Before-values committed (8f85352b, fbcd8370).
     - 5 combined batches of tool-built payloads (update, item publish, read back), then `live-fix verify` per page: 74 FIXED, 0 failed.
   - Tool fixes found on the way:
     - `live-fix prepare` sends re-rendered images (the file changed since the last sync commit), and verify records the new CDN file IDs.
     - `--max-fields` override for ruled name sweeps, recorded on the finding.
     - `ops/sync.sh` refuses conflict markers (see Decisions).
   - Final verify_launch: 40 pages, 4 templates, 4 hubs, 0 failing. Report: reports/2026-10-12/2148-live-audit.md.
5. **Publish-watch gap.**
   - Log, in UTC:
     - 10:05 publish.
     - 10:29 stamp seen, audit skipped ("git pull --rebase failed": this session's dirty checkout); skipped again at 10:59.
     - 11:29 audit ran and finished at 12:10, filing A5-learn and A9-carousel-shown as P1 among 102 P1s, with "P0 0" in the digest.
   - Fixes:
     - `ops/publish_smoke.py`: on each new stamp, verify_launch on the 4 hubs plus one live page per hub, HTTP only, no git, no Claude. A macOS alert and a "SMOKE FAIL" log line on any failure, once per stamp. Tested: production 0 failing; staging (pre-hide templates) 8 failing, caught.
     - `publish_watch.sh` runs it before the full audit; swapped atomically while the watcher was running.
     - `live_audit.py`: A5-learn, A9-carousel-shown and a hub carousel shown are P0 and lead the digest ("P0 TEMPLATE REGRESSION ... tell Divit now").
     - Golden cases audit-template-learn-p0, audit-template-carousel-p0, audit-hub-carousel-p0. Golden suite: 0 regressions.
6. **Retro.**
   - `hubctl retro batch-2`. The tool had batch-1's rows hard-coded and divided by zero.
   - Now: n/a where the ledger has no writer or review stage, and batch facts come from status/retro_notes/<batch>.json. The LESSONS line was written by the tool.

## A and B (read-only; details and element IDs in docs/LEARN_CAROUSEL_FIX.md)
- **A, Learn "No items found":** confirmed by elimination.
  - The Form, LP and Automation lists read the item's own (empty) Learn multi-reference field. Survey reads the Learn collection.
  - The API shows both as the same collection ID; the rendered output only fits this cause.
  - Designer, per template: blog_list-wrapper > Collection List settings > Source: Learn (under Collections, not "AFB/ALPB/AATB - Learn") > sort Publishing date newest first, show 3, no filters > re-bind any "not connected" fields.
  - **Also:** Survey's Learn cards link to "#". On all 4 templates, blog_link > Link settings > Collection Page > the Learn template.
- **B, carousel:** same structure as the working AI app builder carousel, plus our cover.
  - **Link:** "#" because the collection-page target was lost in the clone. API plan: set_settings link {mode collectionPage, to: detail_ai-…-builder} on the 8 build_link elements. All 4 template slugs and the 8 element IDs are confirmed by reads.
  - **Title:** bound correctly but pushed outside the card, because the content wrapper is full-height under the 240 px cover. Plan: a new combo class `build_content_wrapper-under-cover` with height auto.
  - **Description:** the design has no visible slot for one.
  - Nothing applied. Designer fallback clicks are in the doc.

## Numbers
- Webflow:
  - 2 + 2 canary publish calls (rollback earlier, re-publish now);
  - relink 4 update + 4 publish calls (10 items);
  - fix pass 30 updates + 30 item publishes in 6 calls, plus read-backs;
  - 0 site publishes, 0 template writes this task (reads only for A/B).
- Live audit 2026-10-12: 367 findings.
  - Fixed: 74 (1 P0, 73 P1).
  - Proposals waiting for you: 119. Most are sitewide template items: the "Acme Corp" AI CRM card on every page, the testimonial strip (marked real in DECISIONS 2026-10-08), the "Thursday, Oct 16" schedule card, the FAQ first-item clipping, and the Wix library cell.
  - P2 backlog: 174.
- Name sweep: stock names removed from 12 live pages and reused names replaced on 25; every new name was checked to appear in exactly one spec.

## Decisions
- Fixes as item publishes only, no site publish: your instruction and DECISIONS 2026-10-10.
- Names: DECISIONS 2026-10-12 (stock and reused names are AI tells, QC A1). Writers changed surnames and business words, keeping pronouns.
- P0 table: HUB_RULES 5 (comparison table, one real vendor per column), rules/SEVERITY.md (false claim about a named company = P0).
- Field cap override (`--max-fields 14`): name swaps that run through every image legitimately exceed the 10-field auto-fix cap. Recorded on each finding.
- Watcher run: I let your automation finish rather than kill it. Its stamp is marked handled so it doesn't re-audit the same publish.

## Files changed and commits
- 9cc08644 publish smoke, watch, P0 template codes, golden, LESSONS
- c27d14da canaries
- 764270ec A/B doc confirmations
- 3d644a44 audit checker fixes
- 7bd54d9c fix pass specs and images
- 8f85352b, fbcd8370 before-values
- 8be223af render.json repair plus sync guard
- 9f7291de fixes verified and logs
- abd5ebff, 152ea140 relink
- this commit: retro tool, status/retro_notes, status/metrics.md, LESSONS, this report

## Webflow calls
- Canaries: update isDraft false + publish_collection_items (LP 6accb1512c9cca4363e93f7c, Form 6accb96b8570d8ef2122bde8).
- Relink: update_collection_items + publish_collection_items on 10 items. Before-values: childedits/2026-10-12/*.relink.before.json.
- Fix pass: update_collection_items (changed fields only) + publish_collection_items on 30 items.
  - Before-values: childedits/2026-10-12/<slug>.<issue>.before.json.
  - Item IDs and fields in audits/live/2026-10-12/findings.json (status fixed).
  - Rollback: send the before-value fieldData to the same ID and item-publish (`hubctl live-rollback`).
- Reads only: element and page metadata for A/B.

## Not done
- **A and B fixes** (Learn source, carousel link and title): plans ready, waiting for your go. Nothing unhidden.
- **119 proposals** need your call (sitewide template items, the Wix library cell, a few claims needing sources).
- **Retire the grouped "Landingi / Leadpages / Instapage" library entry:** 8 unpublished LP specs still use it, and a rules change needs your go.
- **`hubctl recheck` across the 83 non-live specs with stock names:** not run. The ratchet will catch them as they are touched.

## Open questions for Divit
1. Go to apply B via the API: link target on 8 cards, plus the new class `build_content_wrapper-under-cover`. Then you publish staging and I verify.
2. A is Designer-only (the Source dropdown). Will you do the clicks in docs/LEARN_CAROUSEL_FIX.md, or should I try the API source change first?
3. The sitewide "Acme Corp" AI CRM card, the "Thursday, Oct 16" schedule card, and the FAQ first-item clipping at 390/1440 px on some pages: all template or component work. Yours to schedule?
4. Wix "Basic contact form to email" library cell (flagged on law-firm, mobile, pricing and event; webinar no longer uses Wix): approve a recheck and a corrected cell?
5. GTM: the Adwire tag (`client.adwire.io`) still throws a console error on landing-page-seo.
