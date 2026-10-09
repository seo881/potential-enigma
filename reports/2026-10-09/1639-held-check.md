# Held items, launch items, and the template pages that block every child URL

## Request
Divit (2026-10-09): "git pull (f7e71a4). Read-only check, then one small code change: 1. The 5 held items (IDs in logs/*.md, 2026-10-09 advisor lines) must be isDraft true and return 404 on both https://emergent.sh/<hub>/<slug> and https://emergent-sh.webflow.io/<hub>/<slug>. If any is still live, unpublish it and tell me. 2. The 20 launch items: confirm isDraft false and report whether any is live on emergent.sh (they should be on staging only). 3. Live audit Layer A: add a check that every page held in status/ship/*.json is not live anywhere; if one is, it's a P0: unpublish the item and put it at the top of the digest. Then wait for "staging published"."

## Actions and results
1. **The 5 held items:** thank-you-page 6ab5158e23395050bc86ca79, creator-application 6ab505a8d621dc692561a85a, approval-workflow 6aba7ac40efe4e6ac8693159, customer-satisfaction 6aba7afb6271de33629b812c and contact-form 6ac8a2bff143d8ebe327735f.
   - All 5 are isDraft true with lastPublished empty (the advisor's unpublish at 11:04 UTC).
   - All return 404 on emergent.sh and on emergent-sh.webflow.io.
   - Nothing needed unpublishing.
2. **The 20 launch items:** all isDraft false, with lastPublished 2026-10-09 10:29:23 UTC on all 20.
   - The site was also published to emergent.sh and www at 10:59:52 UTC (`get_site`).
   - Even so, **none of the 20 is live on either domain**: every URL returns 404 on emergent.sh and on staging, and no child URL of the 4 hubs is in either sitemap.
3. **Why:** `get_page_metadata` on the 4 child collection template pages (LP 6aaaa937fe1a8d180b7c9f90, Form 6aaaaa03995bb2f9f4d6a3c2, Automation 6ab2470540448c8f7d1ccc1c, Survey and Quiz 6ab24754757025d10940d06a) shows `draft: false` but `shouldPublish: false`.
   - The live Form hub page (6aabb4c5789871e91d60f6f9) shows `shouldPublish: true`.
   - So the templates are left out of every publish and every item in these collections 404s, whatever the item state. That is also why the accidental publish of the 5 held items never showed.
   - Staging will show the same 404s until the template pages are included in the publish.
4. **Layer A check (A0-held-live):** every page held in `status/ship/*.json` (9 today: the 4 originals and 5 batch-1 pages) is fetched on emergent.sh and on staging on every run.
   - A 200 anywhere is a P0 at the top of the digest. `ops/out/live/ID.unpublish.json` (unpublish plus read back) is written and sent first, even in a dry run.
   - `hubctl live-audit held-done ID RESPONSE` verifies isDraft true and re-checks the URLs.
   - Tested on the real held pages (all 404) and on a synthetic live held page (P0 line first, payload written).

## Decisions
- DECISIONS 2026-10-09 (live audit standing go); LESSONS section 5 (incident of 2026-10-09, held items published by hand).
- Unpublishing a live held page is done even in a dry run, per this request.

## Files changed and commits
- `ops/live_audit.py`, `ops/live_audit.mjs`, `rules/live_audit.json` (held_hosts), `ops/schedule/live_audit_prompt.md`, `docs/LIVE_AUDIT.md`; this commit.

## Webflow calls
Reads only: all items of the 4 child collections, `get_site`, `get_collection_details` (Form), and `get_page_metadata` on the 4 templates and the Form hub. No writes.

## Not done
- The template pages' publish setting: a page setting I won't change without your go.

## Open questions for Divit
- **Include the 4 child template pages in publishing?** Recommended default: yes, it is required for any child page to exist. This is a page setting (Designer page settings, or a page-settings API write if it exposes the flag), and it needs your go.
