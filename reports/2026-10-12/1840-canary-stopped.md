# Item-publish canary stopped: production templates show the broken Learn list and carousel (site publish at 10:05 UTC)

## Digest for Divit
- **Canary published, failed, rolled back.**
  - ebook-landing-page (LP) and employment-verification-letter (Form) were item-published.
  - verify_launch on emergent.sh failed on both: Learn shows "No items found" and the carousel is visible.
  - Per your stop rule, both were unpublished. They return 404 on both hosts and are now drafts.
  - The other 18 were not published.
- **Root cause is the production templates, not the items.**
  - emergent.sh was site-published at **10:05:51 UTC today** (Last Published stamp). That was after this morning's staged template edits (Learn on, carousel on, FAQ heading embed) and before my hide at about 12:00.
  - Since 10:05, the **20 live pages and 4 hubs on emergent.sh show the broken sections**: Learn "No items found" on 19 live pages (Survey renders), and carousel cards linking to "#" on all 20 and on the 4 hubs.
  - verify_launch on production: 24 failures, all of them Learn and carousel. Nothing else fails.
- Staging was last published at 11:56:34 UTC, also before the hide.
- **Only a site publish (yours) can fix production.** The hide is staged and read back on 3 + 8 elements. No CMS item publish can change template sections.
- **Staged template improvements, live or not:** the FAQ heading embed and the sticky table column **are already live** on emergent.sh (they went out in the 10:05 publish). The only staged template change **not live** is the hide (Learn on 3 templates, carousel on 4 templates and 4 hubs).
- A (Learn source) and B (carousel link and title): investigation started, read-only. The plan and Designer clicks come next. Nothing is unhidden.

## Request
> No site publish. Publish today's 20 as CMS ITEM publishes only (publish_collection_items), on the templates already live on emergent.sh:
> 1. Canary: item-publish 2 pages (one LP, one Form), then run verify_launch + verify-live on emergent.sh for both. Any failure: unpublish those 2 and stop.
> 2. If both pass: item-publish the other 18, verify all 20 live, relink, re-verify, then the live audit with fixes on (item publishes only), then the retro.
> 3. Note in the report which staged template improvements (FAQ heading embed, sticky table column) are NOT live yet and wait for a site publish by Divit.
> Then continue with A (Learn source) and B (carousel links/titles); nothing unhidden without my go.

## Actions and results
- **Pre-check:** the CMS export of all 20 links only to live pages or hubs. Links to unpublished pages wait in `pending_links` for relink. So no batch-2 page would link to a 404.
- **Canary publish:** `publish_collection_items` on LP 6accb1512c9cca4363e93f7c and Form 6accb96b8570d8ef2122bde8. Both returned published, no errors, and HTTP 200 on emergent.sh.
- **verify_launch (emergent.sh):** both pages failed `learn_not_empty`, `learn_launch_state` and `carousel_hidden`. The other 23 checks passed.
  - verify-live was not run. It sets the page state to published on a pass, and the stop rule applied.
- **Rollback:** `unpublish_collection_items` on the same 2 IDs. Re-fetch: 404 on emergent.sh and on staging. Both items are now isDraft true.
- **Diagnosis:**
  - The page that was already live, job-application-form, shows the same sections on production. Its HTML contains the hub-fixes embed, which exists only since this morning.
  - The Last Published stamp reads 10:05:51 UTC on emergent.sh and 11:56:34 UTC on staging.
  - verify_launch on production for the 20 live pages and 4 hubs: 24 failing, all Learn and carousel (Learn on 19, carousel on 20 and on 4 hubs).
- **Logged** in logs/lp.md and logs/form.md.

## Numbers
- Webflow: 2 item publishes and 2 unpublishes. No site publish, no template write.
- Live breakage on emergent.sh since 10:05 UTC:
  - Learn "No items found" on 19 pages.
  - Carousel cards linking to "#" on 20 pages and 4 hubs (LP 5 cards, Automation 4, Survey 1, Form 10).

## Decisions
- Stopped on the first failure, as instructed: "Any failure: unpublish those 2 and stop."
- Did not run verify-live on the failed canaries: it would mark them published.
- No CMS workaround attempted. CSS injected through a CMS field could hide the sections on child pages only. The hubs are static pages, not CMS items, and it would put template-level styling into content. Not recommended.

## Files changed and commits
- logs/lp.md, logs/form.md, this report and the INDEX line (this commit).

## Webflow calls
- `publish_collection_items`: LP 6aaaa937fe1a8d180b7c9f83 / 6accb1512c9cca4363e93f7c; Form 6aaaaa02995bb2f9f4d6a36c / 6accb96b8570d8ef2122bde8.
  - Before: isDraft false, lastPublished 10:50:15 (staging only), 404 on emergent.sh.
  - After the publish: 200 on emergent.sh.
- `unpublish_collection_items` on the same 2 IDs (rollback). After: 404 on both hosts, isDraft true.
- To bring them back on your go: update isDraft false, then `publish_collection_items`.

## Not done
- Steps 2–3 of the publish plan (the 18, relink, live audit, retro): stopped by the canary failure.
- A and B: investigation running (read-only). Findings go to docs/LEARN_CAROUSEL_FIX.md.

## Open questions for Divit (recommended first)
1. **Site-publish emergent.sh yourself now** to push the staged hide and end the live breakage on 20 pages and 4 hubs.
   - Note: a site publish also takes the **18 batch-2 items that are isDraft false** live. They passed every staging check, so this is their launch. The 2 canaries stay drafts.
   - After your publish I'll verify all 38 live pages and the 4 hubs, relink, and run the live audit (fixes as item publishes only). Then, on your go, I'll set the 2 canaries isDraft false and item-publish them.
2. If the 18 must wait for an item-publish canary flow instead: say so, and I'll set those 18 to isDraft true (18 writes, before-values committed) before your site publish.
3. If you won't site-publish today: the live pages keep showing "No items found" and the "#" carousel until A and B are fixed and you publish.
