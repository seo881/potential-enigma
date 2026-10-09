# Part 3: production verified, first live audit with fixes, cleanup, retro

## Request

Divit (2026-10-09), PART 3, after the 14:38 UTC production publish: "Do not unpublish anything unless a page fails. 1. VERIFY LIVE (verify_launch on emergent.sh for the 20 launch pages and the 4 hubs; hubctl verify-live per page, state -> published; links --relink, update and publish those items only, re-verify; confirm hero and how-to descriptions, no PA14/PA15 FAQ questions, FAQ schema matches the visible FAQ, generic hero prompt with chips that add and remove with the black selected state, carousel hidden, Learn hidden on Form/LP/AAB and 3 articles on Survey and Quiz, og:image WebP, cover alt, hub link, no links to non-live pages, canonical self, no noindex, in the sitemap; held pages 404). 2. FIX: run the first live audit with fixes ON ... 3. CLEANUP: delete og.png; install render.yml and live-audit.yml and confirm the first runs are green; run hubctl retro batch-1 ... 4. LESSONS line ... 5. Batch 2 onward FAQ moat lines ... Report per the standing rule, digest first." (full prompt in the session).

Mid-run: "missing FAQPage schema on child pages is not a defect (DECISIONS 2026-10-06). Remove that check ... drop those P1s from the ledger as not-an-issue ... add a golden case so it never flags again. Finish Layer B, apply the in-scope fixes (incl. ecommerce-automation 'gray'), write the report with the digest first, then stop."

## Digest

- **Pages passing live: 20/20.** After the fixes, verify_launch on emergent.sh passed all 20 pages, the 4 template card sets and the 4 hubs, with 0 failing. verify-live put all 20 pages in state published.
- **Held pages:** all 9 return 404 on emergent.sh. www returns a 301 to the same path on emergent.sh, which then 404s.
- **Live audit 2026-10-09, issues found:**
  - Layer A (deterministic) found 0 P0, 22 P1 and 24 P2.
    - 20 of the P1s are the missing FAQPage schema, closed as not-an-issue (DECISIONS 2026-10-06).
    - 1 P1 is "grey" in an alt text.
    - 1 P1 is the HTML-escaped JSON-LD on 404-page.
  - Layer B (5 reviewers on all 20 pages) found 1 P0, 51 P1 and 29 P2.
  - Drift: 0. Held pages live: 0.
- **Fixed: 48 findings on 15 pages, including the P0** (the unsourced Gavel "best tool" claim on document-automation). Each page went through the same steps:
  - one CMS update with the changed fields only;
  - publish of that item only;
  - read-back;
  - a Layer A re-run on the live URL.
- **Rolled back: 0.** No page broke.
- **Waiting for your go: 6 proposals** (outside the auto-fix scope; exact fixes below). Template items are on the backlog.
- **Cleanup:**
  - The 187 og.png files are deleted (a2d0db9).
  - render.yml: 4 of 4 runs green.
  - live-audit.yml: its first run (on the install push) failed on a YAML parse error, a colon in a step name; fixed in 9f4d92a. A manual dispatch returned 403 because the token has no Actions write. **The first real run is the 04:17 UTC schedule today**, or you can run it from the Actions tab.
  - Publish watch is loaded (launchd, every 30 min): it runs the audit as soon as the site's Last Published stamp changes. The LESSONS line is in.
  - Retro: status/metrics.md (first-pass QC 21/25, review blocking 6/21, writer about 113k tokens a page).
- **Batch 2 FAQ moat lines** are added to HUB_RULES, the writer brief and the rubric, plus QC F9 (P1, pages not yet in Webflow). The 20 live pages are unchanged, with a backlog line to add the moat lines at their next rework.

## Actions and results

1. **Verify live (5bb93e9, 42a678f).**
   - verify_launch passed 20/20 pages and 4 hubs on emergent.sh. That covers:
     - the hero and how-to descriptions;
     - the chips (add, remove, typed text survives, black selected state);
     - the carousel hidden;
     - Learn: 3 items on Survey and Quiz and hidden elsewhere;
     - og:image WebP, the hub link, the FAQ list, canonical, noindex and the sitemap.
   - Three checker false positives were fixed in verify_live.py:
     - the cover image appears only in the hidden carousel;
     - the og:image regex depended on attribute order;
     - the link check counted links that non-live targets ship as plain text.
   - All 20 pages were moved to state published.
2. **Relink (14:48 UTC).**
   - Pages: task-automation, interest-form, t-shirt-order-form and event-landing-page.
   - Change: FAQ links to pages that are now live restored, then each item published on its own.
   - Read back and fetched live: all links return 200.
3. **Live audit Layer A, calibration (5005c44).**
   - The first run raised 395 findings, almost all checker errors:
     - an old chip field in the manifest;
     - transport errors under load;
     - lazy images not scrolled into view;
     - the product name shown only in the hidden carousel;
     - hub carousel checks running while the carousel is hidden.
   - After fixing those: 0 P0, 22 P1, 24 P2.
4. **FAQ schema ruling (f233aed).**
   - A10 now checks only a FAQPage that exists.
   - The 20 findings are closed as "not-an-issue (DECISIONS 2026-10-06)".
   - Golden case live-audit-no-faq-schema-flag (audit-noflag) is guarded.
5. **Layer B (f233aed).**
   - 5 reviewers covered all 20 pages.
   - Findings on the mockup prompts were downgraded to P2: those prompts are not rendered while the carousel is hidden.
6. **Fixes.**
   - Writers made 48 in-scope fixes in 15 specs, then QC 0 and gate 10/10.
   - The ecommerce-automation tab image 4 was re-rendered with "gray" in both the drawn text and the alt.
   - I re-checked each payload before sending. One writer fix put a comma between subject and verb (client-onboarding FAQ 8: "...before taking them on, call that first step...").
     - I rewrote it to "When a firm screens a prospect before taking them on, it calls that first step an intake form."
     - QC 0 again, payload re-prepared.
   - All 15 payloads were sent between 18:29 and 18:59 UTC. Every update and publish returned errors [].
   - live-fix verify reported FIXED on 15/15, with the Layer A re-run clean apart from template P2s.
   - The ecommerce tab image 4 file ID (6ac932936f4448c30272371b) was written to the spec, and the cms_draft fingerprint recomputed.
7. **Re-verify after the fixes.**
   - The launch manifest was rebuilt from the current specs (`launch.py prepare`, which writes files only and sends nothing).
   - verify_launch on emergent.sh: 20 pages, 4 templates, 4 hubs, 0 failing.
   - The first post-fix run failed 5 checks (meta_description and h1 on the pages we had just fixed, and the ecommerce image). That manifest was stale; nothing was wrong on the site.
8. **Cleanup, LESSONS, moat lines, retro:** see 146f305, 341d26c, a2d0db9 and 9f4d92a. The retro was re-run after the audit.

## Numbers

| | Count |
|---|---|
| Launch pages passing live | 20/20 |
| Hubs passing | 4/4 |
| Held pages 404 | 9/9 |
| Layer A findings (P0/P1/P2) | 0 / 22 / 24 |
| Layer B findings (P0/P1/P2) | 1 / 51 / 29 |
| Closed as not-an-issue (FAQ schema) | 20 |
| Fixed and verified live | 48 (15 pages) |
| Rolled back | 0 |
| Proposals waiting for a go | 6 |
| P2 on the backlog | 53 |
| Golden suite | 82 cases, 0 regressions, 8 open misses (4 PA13, 4 new H3) |

## Decisions

- **Item-only publishes for the relink and the fixes, no site publish.** This follows Part 3 steps 1 and 2 ("update and publish those items only"; auto-fix scope "child CMS items, item publish only").
- **FAQ schema check removed.** DECISIONS 2026-10-06, as restated by Divit mid-run; rules/live_audit.json `faq_schema` is info-only.
- **Serial commas fixed as P1:**
  - US style, serial comma required (HUB_RULES 2a);
  - reviewers' DECISIONS 2026-10-09 lines.
- **Unsourced Gavel claim at P0.** rules/SEVERITY.md (unsourced claim about a named company); HUB_RULES section 8.
- **Mockup-prompt findings at P2.** They are not rendered while the carousel is hidden (backlog, MONDAY).
- **Client-onboarding FAQ 8 rewrite.** HUB_RULES 2b: a sentence must parse, and a comma between subject and verb is a grammar error. The fix stays within the one field the finding named.
- **Proposals left for Divit.** They touch the comparison-library facts, the claim registry, a pattern rule or a template, all outside the auto-fix scope (docs/LIVE_AUDIT.md).

## Proposals waiting for your go (exact fixes)

1. **sign-in-form and t-shirt-order-form, why_table, Google Forms "How you build" cell** (P1, comparison library).
   - Current: "Manual, field by field".
   - Google Forms now has Gemini "Help me create a form", and the library fact cites the old table, not vendor docs.
   - Proposed: "Editor, with Gemini drafting on some Workspace plans". This changes the shared library cell, so booking-form and registration-form change too. Needs a fact check against Google's docs first.
2. **404-page feature_1** (P1, claim). "Your prompt asks for every unknown URL to answer with a 404 and the designed page." The hosting capability is not in rules/claims.json.
   - Either confirm the claim (add it to claims.json),
   - or replace it with: "Your prompt asks for the designed page on every unknown URL; check its status code with your host before launch."
3. **404-page why_table, Emergent build cell** (P1, library). The cell reads "Prompt for a campaign page".
   - Proposed new LP cell for utility pages: "Prompt for the page and the rules behind it".
4. **client-onboarding-questionnaire explore_cta** (P1, overflow at 390 px). Change "Build My Client Onboarding Questionnaire" to "Build My Onboarding Questionnaire".
   - Pattern question: should the rule be to shorten any CTA over 34 characters?
5. **404-page JSON-LD shows `&#39;`** (P1, template).
   - The LP template's JSON-LD embed HTML-escapes the bound meta description. Only this page has an apostrophe in that field.
   - Quick fix in the CMS item: "doesn't exist" becomes "does not exist" in meta_description.
   - Lasting fix: a template change (your go).
6. **Template P2s (backlog):**
   - the FAQ heading always renders "Your Questions, Answered" instead of the item's heading;
   - comparison tables clip at 390 px;
   - an empty zero-width paragraph after feature 1 (24 findings).

Also found: QC's serial-comma detector (H3) files verb series, noun phrases with clauses and 4-item lists as "ambiguous" (P2), so some live pages still have them. Examples:
- event-landing-page FAQ 1 and 7;
- booking-form FAQ 2;
- client-onboarding FAQ 1 and 2.

There are 4 open golden cases and a backlog item. **Proposed:** fix the detector, then one sweep of the 20 live pages (item publishes only, same fix path).

## Files changed and commits

- 5bb93e9: verify-live checker fixes and relink before-values.
- 42a678f: 20 pages to state published.
- a2d0db9: og.png files deleted.
- 341d26c: workflows installed.
- 9f4d92a: live-audit.yml YAML fix.
- 146f305: moat lines, F9, publish watch, LESSONS, DECISIONS, retro.
- 5005c44: Layer A calibration and the gray re-render.
- f233aed: Layer B, writer fixes, FAQ schema ruling.
- f7d8099: first 5 pages verified, before-values, client-onboarding rewrite.
- 5d19ff7: 15/15 verified, ledger, audit report (reports/2026-10-09/0113-live-audit.md), hub logs, retro, golden, backlog.
- This report and the INDEX line are in the next commit.

## Webflow calls

All calls were data_cms_tool on the 4 child collections. No site publish was sent, and nothing was unpublished.

- **Relink, 14:48 UTC.**
  - Call: update_collection_items (awb---faq-data), then publish_collection_items on those items only.
  - Items: 6ac89f5186706b45a79b39b6, 6ac8a04200f35689bf9ff3c4, 6ac8a04200f35689bf9ff3c2, 6ac89f545408b01694dc164b.
  - Before: childedits/2026-10-09/relink.before.json.
  - Rollback: re-send that file and publish the items.
- **Live-audit fixes, 18:29 to 18:59 UTC.** Call per item: update_collection_items (changed fields only), then publish_collection_items for that item only, then a read-back.

| Page | Item |
|---|---|
| ecommerce-automation | 6ac8a1af7019f6d354746f12 |
| 404-page | 6ac8a23f9873b6bc7b4343ba |
| webinar-landing-page | 6ac89f545408b01694dc1649 |
| employee-engagement-survey | 6ac8a15a5408b01694dd5e21 |
| task-automation | 6ac89f5186706b45a79b39b6 |
| booking-form | 6ac8a2bff143d8ebe3277361 |
| registration-form | 6ac79cdc9308a032a2f7dd2d |
| client-onboarding-questionnaire | 6ac8a0256cea93e7ab27259d |
| event-landing-page | 6ac89f545408b01694dc164b |
| law-firm-landing-page | 6ac89f545408b01694dc164d |
| pricing-page | 6ac8a23f9873b6bc7b4343bc |
| job-application-form | 6ac8a04200f35689bf9ff3c0 |
| massage-intake-form | 6ac8a06cc42bf1463b1a2cba |
| document-automation | 6ac89f5186706b45a79b39b4 |
| sales-automation | 6ac89f5186706b45a79b39b2 |

  - Before-values: childedits/2026-10-09/<slug>.<issue>.before.json (client-onboarding: childedits/2026-10-10/).
  - After: the specs at 5d19ff7.
  - Rollback: re-send the before-value, then publish that item (`hubctl live-fix verify` writes ops/out/live/<issue>.rollback.json on failure; none was needed).
  - Logged in logs/aab.md, form.md, lp.md and sqb.md.

## Not done

- **Before-values committed late.** They were read and saved to disk before each write, but committed with the first verify commit (f7d8099), not before the writes.
- **live-audit.yml has no green run yet.** It waits for the 04:17 UTC schedule or a manual run (403 on dispatch with the current token).
- **The 6 proposals and the serial-comma sweep are not applied.** They need your go or a detector fix first.

## Open questions for Divit

1. Google Forms "How you build" cell: approve the new wording (after a docs check), or keep it?
2. 404-page: is "unknown URLs return a real 404 status" an approved hosting claim?
3. CTA length: shorten the client-onboarding CTA, and make "34 characters or fewer" a rule?
4. 404-page meta description: change "doesn't" to "does not" now (CMS item, publish that item only), or wait for the template fix?
5. Fix the H3 detector, then sweep the serial commas on the 20 live pages?
