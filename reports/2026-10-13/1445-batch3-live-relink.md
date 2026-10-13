# Batch 3 live by item publish (60 child pages live), relink 16, live audit; no site publish

## Digest for Divit
- **Live: 60 child pages** (40 + batch 3's 20). The 20 were published with publish_collection_items on their own item IDs only; no site publish. All 20 return 200 on emergent.sh, and verify-live passes 20/20.
- **Relink:** 16 live pages had FAQ links waiting on batch-3 targets. Their FAQ field was updated and the 16 items published. verify-live passes 16/16. One page is still pending: contact-form, which is held and not live.
- **Live audit (all 60 pages + 4 hubs):** the run reported P0 18, P1 69, P2 46. The failing tail (13 pages "not 200", pricing-page, the 4 hubs) ran during a local network drop (`ERR_INTERNET_DISCONNECTED` in the raw output). Every one of those URLs returns 200 now. A re-run on those 14 pages was still in progress when this report was written. The hubs' "missing cards" is the expected state: carousels are hidden on production.
- **Template card links:** no site publish until the 12 Designer clicks are done and read back (plan/backlog.md, docs/WEBFLOW_API.md). The staged template changes stay staged.
- **FTC source:** the page is live; ftc.gov answers scripted requests with 404. No spec changed; the checker now treats that host's 404 as "blocked". QC is 0 on coming-soon-page and ecommerce-automation.

## Request
> Go: batch 3 to production by item publish only (publish_collection_items on the 20 batch-3 item IDs), no site publish. Skip the card-link rollback; staged template changes stay staged. 1. Before-values committed if your ship flow needs them, publish the 20 items, read back. 2. Verify all 20 live (verify-live: title, meta, H1, FAQ, images, share image, links 200), then live audit on all 60 and 4 hubs, then relink live pages that now have live targets (item updates + item publishes only). 3. Backlog note for tomorrow: no site publish (staging or production) until the 12 Designer clicks are done and read back, because the staged card links 404. Report under 10 lines: live count, any failure, anything I must do.
> (Earlier decisions on 1400-staging-b3-ruling14: 2 link fix via the working card's structure, then Designer clicks; 3 hub FAQ refit in our embed; 4 FTC source; 5 employee-handbook stays in the tranches.)

## Actions and results
1. Read the 20 items first: isDraft false, lastPublished 13:23 from the staging publish, 404 on emergent.sh. Committed as childedits/2026-10-13/batch3-publish.before.json (0a96d462).
2. publish_collection_items on Form 10, LP 4, SQB 4 and AAB 2: 20 published, no errors. HTTP 200 on 20/20; verify-live 20/20; status moved to published (5c588fc3).
3. Relink:
   - fresh read of the 4 collections;
   - `hubctl relink-payload --before-only`, with before-values committed (168a8e27);
   - 16 FAQ updates in 9 chunks, then item publish of those 16 (no errors);
   - verify-live 16/16; pending_links recomputed (993cba38).
4. Live audit `--all`: 60 pages and 4 hubs. The tail failures were the network drop; a re-run of the 14 affected pages is under way.
5. FTC: `guards.BOT_404_HOSTS`. Also docs/WEBFLOW_API.md and the backlog note (c6c4a871).

## Numbers
- Live child pages: 60 (LP 13, Form 26, Auto 11, SurveyQuiz 10).
- Items published: 20 batch-3 + 16 relinked.
- Pull wave at 14:37 UTC: 210 pulls, 152 credits (cap 400).

## Decisions
- Divit's go (item publish only, no site publish) and the no-site-publish rule (CLAUDE.md, 2026-10-10).
- Relink by item update and item publish only.
- Rule-file change (BOT_404_HOSTS) is a factual fix, so it lands the same day.

## Files changed and commits
0a96d462, 5c588fc3, 168a8e27, 993cba38, c6c4a871; this report.

## Webflow calls
- **Publish:** publish_collection_items on the 20 batch-3 IDs (status/ship/batch-3.json). Rollback: unpublish_collection_items on the same IDs.
- **Relink:** update_collection_items on 16 items (awb---faq-data only), then publish_collection_items on those 16. Rollback: before-values in childedits/2026-10-13/*.relink.before.json.
- **Reads:** list_collection_items, twice.
- **Site publish:** none.

## Not done
- The live-audit re-run of 14 pages (in progress).
- Link fix through the API (tomorrow, before batch 4 staging).
- Hub FAQ refit: the embed edit is staged tomorrow, behind the no-site-publish block.
- Tranche 2 sheets: as the wave lands.

## Open questions for Divit
1. Do the 12 Designer clicks (plan/backlog.md lists them) when you can. Until they're done and read back, nothing site-wide publishes.
