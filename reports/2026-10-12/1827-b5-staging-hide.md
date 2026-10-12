# B5 on staging: Learn and carousel hidden, everything else passes; publish to emergent.sh

## Digest for Divit
- **Hidden and read back, before production:**
  - Learn (section_blog-related) on the Form, LP and Automation templates. Survey's Learn is untouched and still visible.
  - Carousel (section_build) on all 4 templates and all 4 hubs.
  - Before-values committed first (8474081a), writes logged with rollback (e0e03231).
- **verify_launch on staging, 40 pages (20 new + 20 live) and 4 hubs:**
  - 22 of 26 checks pass on every page: H1, title, meta, canonical, og image, FAQ, hero prompt and chips, first tab, use-case images, table, hub link, no links to non-live pages. 0 console errors.
  - The only failures are Learn (34 non-Survey pages) and the carousel (40 pages, 4 hubs), the two sections now hidden. They clear with your next publish, since the hide isn't on staging yet.
- **Your B5 list:**
  - FAQ heading from the item: shown on 40/40.
  - JSON-LD: parses on 40/40, no HTML escapes.
  - Tables at 390 px (one page per hub): the table scrolls inside its frame, the label column stays put, and nothing spills past the page width.
- **Dry live audit (staging):** nothing blocking. The 186 P0 were one transient link probe (status 0) repeated on every page; all those links return 200. The audit tool is fixed so one bad probe can't repeat (b1b03cf0). Details below.
- **Publish to emergent.sh now.**

## Request
> Staging check by Divit: FAQs fine. Two sections are broken, so hide both before production:
> 1. Learn list still "No items found" on Form/LP/Automation: set section_blog-related visibility false on those 3 templates again (read back, log). Leave Survey visible.
> 2. Carousel cards: covers show, but the card link is "#" (not bound to the item page) and the title isn't shown. Set the carousel (section_build) visibility false on the 4 templates AND the 4 hubs (read back, log).
> Then finish B5 on staging for everything else and tell me "Publish to emergent.sh now" (I will republish staging first if you need it).
>
> AFTER the 20 are live (separate task, nothing unhidden until I approve):
> A) Learn list: ... B) Carousel: ... (separate task; not started)

## Actions and results
- **Read** all 11 sections (3 Learn, 8 carousel): all `visible: true`. Logged and committed as before-values.
- **Wrote** `set_visibility false` on 10 sections. **Read back:** 10 false, and Survey's Learn still true.
- **verify_launch:**
  - Manifests rebuilt from the current specs (`launch.py prepare` for batch-1 and batch-2; nothing sent).
  - Run: `node ops/verify_launch.mjs <40-page manifest> --base https://emergent-sh.webflow.io`.
  - The outside-page check failed at first. Its only difference was production's Cloudflare email obfuscation ("[email protected]") against the plain address on staging. Fixed to compare emails per text node (9099df84); the page now reads the same on both hosts.
- **Dry live audit:** `hubctl live-audit --urls <40> --base staging --dry`. 375 findings in Layer A, reviewed by rule:
  - **A7-link (186):**
    - Pattern: 4 sitewide nav links (/community, /enterprise, /pricing, /integrations/slack) × 40 pages, plus 2 others.
    - Cause: a status 0 (transport error) was cached for the run.
    - Rechecked with curl and Node: all return 200.
    - Fix: a status 0 is no longer cached (b1b03cf0).
  - **A9-carousel-shown (40), A5-learn and A5-stray "No items found" (34 each):** the hidden sections, not yet published.
  - **A8-alt-live (39):** carousel card cover alt (bound to the product name per T5); inside the hidden carousel.
  - **A5-empty-p (40, P2):** a template rich-text placeholder. Present on every page since the first audit on 2026-10-09; backlog, not new.
  - **A6-repeat (1):** "into job JOB-4471" on data-entry-automation. A false positive (a word next to an ID).
  - **A9-console (1), landing-page-seo:**
    - Chromium logs "Illegal return statement" on every load of this page.
    - Source, found with the Chrome debugger: the third-party tag `client.adwire.io/clarity/molecule.js`, which serves the body `return "ok";`.
    - It is not in our templates, CMS or embeds and loads only on this page, probably through GTM.
    - It breaks nothing on the page (all checks pass). Added to your GTM check.
- **Dry-run side effect, undone:** the run overwrote today's committed `audits/live/2026-10-12/findings.json`. Restored; the staging-dry findings are kept at `.cache/live/2026-10-12/findings-staging-dry-b5.json`.

## Numbers
- 11 element reads, 10 visibility writes, 11 read-backs (3 rate-limit retries).
- verify_launch: 40 pages × 26 checks.
  - Every failure is a Learn or carousel check: Learn on 34 pages, carousel on 40.
  - 0 console errors, 0 og failures.
- Live audit (dry), 375 findings by kind:
  - Hidden sections: 108 (carousel 40; Learn 34 counted twice as A5-learn and A5-stray).
  - False positives: 187 (186 links, 1 repeated word).
  - Inside the hidden carousel: 39.
  - Old template P2: 40.
  - Third-party tag: 1.

## Decisions
- Hide both sections: Divit's instruction (this request). Survey's Learn stays visible, as asked.
- No staging republish requested: a visibility switch is deterministic and read back. Hidden sections are confirmed after the production publish by verify-live (it checks the published HTML for Learn and carousel).
- FAQPage JSON-LD is not on child pages (production child pages lack it too); no HUB_RULES requirement. Not a regression.

## Files changed and commits
- 8474081a logs (before-values), e0e03231 logs (writes), 9099df84 ops/verify_launch.mjs, b1b03cf0 ops/live_audit.mjs, this report and the INDEX line.

## Webflow calls
- set_visibility false:
  - Learn: Form template 6aaaaa03995bb2f9f4d6a3c2/24cd8ebc-23b4-d766-1f9f-0d648fc0665f, LP 6aaaa937fe1a8d180b7c9f90/d8a90b8f-142b-5c77-eae7-a06e09b08934, AAB 6ab2470540448c8f7d1ccc1c/cadd555f-249f-2bfd-b8af-165dc634d9d9.
  - Carousel, templates: Form 24cd8ebc-23b4-d766-1f9f-0d648fc0667c, LP d8a90b8f-142b-5c77-eae7-a06e09b08951, AAB cadd555f-249f-2bfd-b8af-165dc634d9f6, SQB 6ab24754757025d10940d06a/ba847d5e-85b3-fe51-eadf-ad4eebacf7f6.
  - Carousel, hubs: Form 6aabb4c5789871e91d60f6f9/a0031ab3-d167-ad84-c89c-90a14c07a6b0, LP 6aaa658ea6d39733443fe69b/993a2e98-59bb-16c2-a552-a805b88a33a3, AAB 6ab2464303ee70548366671e/7c8469e8-95dd-19f9-811e-e6276d9b2d9c, SQB 6ab246c3897d1c09d9d320ec/07f67163-1778-b5f9-55e1-26f8141b8c4c.
- Before true, after false on all 10.
- Rollback (only on your go after A and B are fixed): set_visibility true on the same IDs.
- No publish of any kind.

## Not done
- **After the production publish:** verify-live on emergent.sh (20 new + 20 live + 4 hubs, including Learn and carousel gone), relink, live audit with fixes on, retro.
- **A and B** (the Learn source and carousel binding investigation): a separate task after the 20 are live, as you asked. Nothing will be unhidden without your go.
- **`hubctl recheck` after today's rules:** not run yet; scheduled with the post-live steps.

## Open questions for Divit
1. **Publish to emergent.sh now.**
2. In your GTM check, also look at the Adwire tag (`client.adwire.io`): it throws a console error on /ai-landing-page-builder/landing-page-seo.
