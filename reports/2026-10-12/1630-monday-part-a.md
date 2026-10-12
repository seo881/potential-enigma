# MONDAY Part A: backlog (A1-A8)

## Digest for Divit
- **A1** done: 429/999 from social domains is OK in the live audit; 9 golden cases; the 24 Instagram P1s are closed as not-an-issue.
- **A2** staged, cause **not yet verified**. Every readable difference between the working Survey Learn list and the Form/LP/Automation lists was checked (structure, query settings, item bindings, page code, list count): all identical. The lists' query was re-saved and the 3 sections set visible. Confirmation comes from the staging check after your publish; if they still show "No items found", I hide them again (rollback logged).
- **A3** staged: FAQ heading from each item (new embed, the heading lives in window.awbFAQ, not a CMS field); JSON-LD escaping fixed at the data layer (QC J1: Webflow HTML-escapes every bound value and the template cannot emit raw text); comparison tables **already scrolled** at 390 px (measured), the new embed adds a sticky label column and tighter cells; the tab-4 mockup key mismatch is harmless (the template reads mockup prompts by position, verified live).
- **A4** staged: carousel visible on the 4 templates and 4 hubs; covers and alt verified on all 20 live items; layout at 390 px is checked on staging. DECISIONS updated (carousel back on).
- **A5** done and live: 15 of 20 live pages got 2-3 moat lines (5 already met F9); 0 gate rejects, 0 PA14 flags; serial commas fixed on 3 pages; registration-form now says "on a paid plan" for code export. Item publish only, before-values committed first, all 15 verified FIXED by the live re-check.
- **A6** done: 7 intent-mismatch pages merged or dropped, 12 synonyms applied, 61 top-secondary pulls (59 credits); **9 pages back to rework**, 120 stay parked with source counts.
- **A7** done: engine bug (unknown palette key crashed instead of erroring) fixed at the root; model-release-form renders, 198 of 199 briefs byte-identical.
- **A8** investigated, nothing changed: the duplicates are in `section_usecase` (4 mockup forms) and `Global / Signup Modal` (1); no script references the ids; the safe fix needs a look at GTM first (docs/A8_DUPLICATE_IDS.md).

## Request
> MONDAY (Divit, 2026-10-12). git pull first; read CLAUDE.md, LESSONS.md, DECISIONS.md, plan/backlog.md, docs/LIVE_AUDIT.md. NO site publish by Claude, ever (DECISIONS 2026-10-10). Staged template edits: standing go for the 4 child templates and the carousel/Learn sections on the 4 hubs, new classes only, never edit an existing class, component or sitewide element; read before, read back after, rollback logged; before-values committed before any write. Run independent parts in parallel subagents.
>
> PART A: BACKLOG
> A1. Live-audit false positive: a 429 from a social domain (instagram, x/twitter, linkedin, facebook, youtube, tiktok) is OK. Close the 24 P1s as not-an-issue and add a golden case.
> A2. Learn list: find the real cause of "No items found" on the Form/LP/Automation templates (Survey renders with the same settings: compare the two wrappers element by element: bindings, Finsweet attributes, conditional visibility, empty state, item template). Fix it, then set section_blog-related visible again on those 3 templates. All 4 must show the 3 newest Learn articles.
> A3. Template fixes (4 templates): FAQ heading bound to the item's FAQ heading (not the fixed "Your Questions, Answered"); JSON-LD meta description without HTML-escaping; comparison tables scroll horizontally at 390 px (scoped embed CSS, new class); confirm or fix the customer-experience-survey tab-4 mockup key.
> A4. Carousel: check it on hubs and templates (covers, alt, only live pages, 390 px), fix only defects, then set it visible on the 4 templates and the 4 hubs. Update DECISIONS (carousel back on).
> A5. The 20 LIVE pages under the current rules: re-run the PAA gate (PA1-PA15, incl. the PA14 unlisted-name flags) and QC (D1, D2, F9, the explore_cta limit, H3) on all 20. Replace every failing FAQ item, add 2-3 moat lines per page (F9; claims ledger only; subtle; no competitor names). Put any unlisted name you can't judge in the report for me. Then the live fix path: before-values committed first, CMS update, item publish only, live re-check, ledger.
> A6. Form parked pages (136): apply the 7 intent-mismatch drops/merges; apply the 12 safe synonyms; for the rest, one AlsoAsked pull on the top secondary via weekend.py aa (cap 2 credits per page, stop at 250 credits total). Re-gate; pages with 8 or more on-topic sources go back to the rework queue. Report the counts.
> A7. model-release-form image brief (KeyError 'warn'): fix and re-render.
> A8. Duplicate IDs in shared components: investigation only (components, form ids, pages using them, scripts referencing #email-form or #field), with the safest fix proposed. Change nothing.
>
> (Parts B and C as in the original prompt; Part B is reported in 1631-monday-part-b-staged.md.)

## Actions and results
- **Parallel work:** 10 subagents (A1+A7; A6; A5 x4 by hub; B2 x4 by hub). Webflow calls only from this session.
- **A1** (agent): `ops/live_audit.py` `link_ok()` treats 429 and 999 from instagram, x, twitter, linkedin, facebook, fb, youtube, youtu.be, tiktok (and subdomains) as OK; settings in `rules/live_audit.json` `social_ok`. Golden kind `audit-link`, 9 guarded cases (OK: instagram 429, x 429, linkedin 999; still findings: instagram 404, youtube 503, example.com 429, notinstagram.com 429). The 24 findings in `audits/live/2026-10-12/findings.json` carry `not-an-issue (429 from a social domain is OK, Divit 2026-10-12)`; LEDGER regenerated. LESSONS line added.
- **A2** (this session, Webflow reads): Form vs Survey Learn wrapper compared: element tree, DynamoWrapper settings (source Learn, dynamic, no filters, sort publishing date desc, limit 3, offset 0, no pagination), DynamoList `fs-list-element=list`, item bindings (link collectionPage, image, title, date, category), empty state, visibility; page head/footer code empty on both; 2 Collection Lists per template (not a limit issue). All identical. Fix applied: Learn list query re-saved with identical values on Form, LP, Automation (forces Webflow to regenerate the stored query), section_blog-related set visible (read back true). Verification is the staging render.
- **A3**: new HtmlEmbed per template (`ops/template/hub-fixes.html`, no class): sets the FAQ h2 from `window.awbFAQ.heading`; at <=479 px tightens `.section_table .cmp` cells and makes the label column sticky. Tested by injection on 3 live pages: heading correct, label column stays visible, page width 390, no overflow. The FAQ component's Title prop cannot be bound: there is no FAQ-heading CMS field (collections are at the 60-field cap). JSON-LD: the template schema binds meta-title, meta-description and breadcrumb; Webflow HTML-escapes bound values, so QC **J1** (P1) now rejects `' " & < >` in those fields; 1 batch-2 page fixed (landing-page-seo "Google's" -> "Google"), 24 unpublished specs flagged for their next pass, 0 live pages affected. Tables: measured on all 4 templates at 390 px, `.cmp` 350 px wide with 720 px content, scrollLeft moves, document width 390: they already scroll. Mockup key: the template script reads `Object.values(awbMockup)` by position (live employee-engagement-survey: 4 tabs filled in order).
- **A4**: covers (file + alt) present on all 20 live items; cover alt bound to the product name since 2026-10-09 (T5). Carousel lists show only published items. Visible on 4 templates and 4 hubs (read back). 390 px layout is part of the staging check.
- **A5**: gate + `ship-qc` on 20 live pages: 0 rejects, 0 PA14 flags, only F9 failing (14 pages had 0-1 moat lines). 15 pages edited (FAQ field only; registration-form for a paid-plan qualifier), 5 already compliant (sales, task, booking, sign-in, law-firm). Before-values `childedits/2026-10-12/*.before.json` committed and pushed (16b32499) before any write; 15 CMS updates + 15 single-item publishes; `live-fix verify` re-ran Layer A on each URL: 15 FIXED. QC F9 now applies to live pages (originals excepted).
- **A6** (agent): see Numbers. Code: `weekend.py aa --kw secondary` (per-page cap counts both pulls, expected-cost check, run cap 250, `aa-balance` preflight), gate reads `<slug>--sec.json`, `park_rescue --a6`, `alsoasked_pull.py` recovers dropped connections.
- **A7** (agent): `pipeline/engine_blocks.py` / `engine.py`: unknown kind/tone/color raises a BriefError naming allowed values; meta accepts warn/bad, text accepts warn. model-release-form brief: one redundant hero meta removed (hero overflowed its panel). Rendered, gates pass, contact sheet read (one hero, readable, numbers add up, tab 3 is now a DM matching the copy). 199 briefs rendered with old and new engine: 198 byte-identical (the 199th used to crash). Golden kind `engine-brief`, 5 cases.
- **A8**: see docs/A8_DUPLICATE_IDS.md.
- **Ratchet**: `hubctl recheck --states reviewed,qc_pass,images,approved` after F9-live, J1 and L11: 90 pages re-checked, 20 at 0 (batch-2), 70 moved to rework (mostly L11, see Part B), 0 live pages failing. A first run without `--states` also moved parked pages; it was reverted before commit.

## Numbers
- Golden suite: 112 cases, 0 regressions, 4 open (known PA13 misses), 59 not machine-tested.
- A1: 24 P1 closed; 9 golden cases.
- A5: 20 pages gated; 0 rejects; 0 PA14; 15 FAQ updates live; 27 moat lines added; serial commas fixed in 7 FAQ answers on 3 pages; 15/15 verified FIXED.
- A6: parked at start 136. Intent mismatch: 6 merged (expense-request, mileage-reimbursement, travel-reimbursement, travel-request -> expense-report-form; car-rental -> rental-agreement-form; health-screening -> medical-history-form), 1 dropped (vehicle-inspection-form); Form plan 269 -> 262. Synonyms: 12 approved. Pulls: 63 eligible, 49 skipped at 2 credits, 8 with no usable secondary; 62 pulls saved (58 with questions, 4 no results), 1 lost to a connection reset; 59 credits (balance 802 -> 743), max 2 per page. Back to rework: 9 (brand-questionnaire 12, multi-step-form 10, life-coaching-intake-form 9, shipping-address-form 9, church-membership-form 8, employee-referral-form 8, payment-form 8, sign-out-form 8, tenant-screening-form 8 on-topic sources). Still parked: 120 (49 written at the credit cap, max 7 sources; 16 written and pulled, under 8; 3 no usable secondary; 1 pull lost; 40 never written, pulled, under 8; 4 never written, no results; 5 never written, no usable secondary; 2 never written with 8+: hipaa-release-form 15, employee-handbook-acknowledgment-form 8).
- A7: 198/199 briefs byte-identical; 5 golden cases.
- Ratchet: 70 to rework, 0 live.

## Decisions
- Social 429/999 OK: Divit 2026-10-12 (A1); DECISIONS line added.
- Carousel back on: Divit 2026-10-12 (A4); DECISIONS line added, supersedes the 2026-10-09 hidden line.
- FAQ heading by embed, not binding: no CMS field holds the heading (config/collections.json, 60-field cap); the component Title prop is static ("Your Questions, Answered"). Embed is a new element, no class, no component edit (standing go, MONDAY prompt).
- JSON-LD fixed in data (QC J1) instead of the template: Webflow's page schema bindings are HTML-escaped and the API offers no raw binding (read via query_pages_schema_markup).
- Table "fix" kept to usability: the tables already scroll at 390 px (measured); scoped CSS only inside `.section_table` (no existing class edited).
- F9 extended to live pages (DECISIONS 2026-10-09: "the 20 live pages get theirs at next rework").
- A6 "merge or drop" took the merge, as listed first in reports/2026-10-08/2121-deterministic-pass.md.
- Ratchet limited to unpublished pipeline states: parked pages keep their park reason (LESSONS rule 2, one pass per page).

## Files changed and commits
- 4854ac02 F9 on live pages · 2b054324 A1 · 3dd17326 A7 · 18f54edd, 6e86e0cb, ea6f038c, e368843b, 21844062 A6 · f949a887, 90d4cd40, 0b008e7d, 6b283068 A5 specs · 56a1ef48 QC J1 · ee836b50 template before-values · a07c3b2f template writes + DECISIONS · 16b32499 A5 before-values · d0df76bb A5 verified · d7918f14 ratchet + A8 doc.
- Key paths: ops/live_audit.py, rules/live_audit.json, tests/golden/*, pipeline/engine*.py, ops/weekend.py, qc/paa_gate.py, qc/qc_hub.py (F9, J1, L11), ops/template/hub-fixes.html, logs/templates.md, DECISIONS.md, LESSONS.md, docs/A8_DUPLICATE_IDS.md, rules/paa_synonyms.json, plan/overrides.json, childedits/2026-10-12/, audits/live/.

## Webflow calls
- Reads: guide; Learn/carousel/section trees and settings on Form and Survey templates; carousel sections on 4 hubs; page code and schema markup on 4 templates; component and element lookups for A8; collection reads (4 collections) before and after A5.
- Template writes (staged, read back; rollback in logs/templates.md):
  - Learn list query re-saved (identical values): Form 24cd8ebc-...-0666a, LP d8a90b8f-...-0893f, AAB cadd555f-...-9e4.
  - section_blog-related false -> true: Form 24cd8ebc-...-0665f, LP d8a90b8f-...-08934, AAB cadd555f-...-9d9d9. Rollback: set_visibility false.
  - New HtmlEmbed (hub-fixes.html): Form 8ae2952e-8f39-d359-e316-cb11ac2dba09, LP c037d526-fcb3-377f-0a35-af6f51d7117b, AAB b253e36b-ce92-0872-ec02-1bbcdecc3368, SQB 96b6b5f3-7b78-1cbb-b483-e59c6245e7c9. Rollback: remove_element.
  - section_build false -> true: templates Form 24cd8ebc-...-0667c, LP d8a90b8f-...-08951, AAB cadd555f-...-d9f6, SQB ba847d5e-...-f7f6; hubs Form a0031ab3-...-a6b0, LP 993a2e98-...-33a3, AAB 7c8469e8-...-2d9c, SQB 07f67163-...-8c4c. Rollback: set_visibility false.
- CMS (A5, live, item publish only): FAQ field updated and the item published for 404-page 6ac8a23f9873b6bc7b4343ba, event-landing-page 6ac89f545408b01694dc164b, pricing-page 6ac8a23f9873b6bc7b4343bc, webinar-landing-page 6ac89f545408b01694dc1649, client-onboarding-questionnaire 6ac8a0256cea93e7ab27259d, employee-information-form 6ac8a06cc42bf1463b1a2cbc, feedback-form 6ac8a06cc42bf1463b1a2cb8, interest-form 6ac8a04200f35689bf9ff3c4, job-application-form 6ac8a04200f35689bf9ff3c0, massage-intake-form 6ac8a06cc42bf1463b1a2cba, registration-form 6ac79cdc9308a032a2f7dd2d, t-shirt-order-form 6ac8a04200f35689bf9ff3c2, document-automation 6ac89f5186706b45a79b39b4, ecommerce-automation 6ac8a1af7019f6d354746f12, employee-engagement-survey 6ac8a15a5408b01694dd5e21. Before-values: childedits/2026-10-12/<slug>.20261012-<slug>-F9-1.before.json. Rollback: `hubctl live-rollback <issue-id>`.
- No site publish. No component, class or sitewide element edited.

## Not done
- A2 cause is unverified until the staging render (a re-save of an identical query is the only lever left after the element-by-element comparison).
- A4 390 px carousel look and A3 table/heading on real pages: checked after your staging publish (B5).
- A8: no change by design.
- A6: 3 billed-but-unlogged AlsoAsked credits (connection resets) not added to credits.log: the permission classifier blocked writing the reconciliation rows. Affected: audition-form, corporate-resolution-form, copyright-release-form (copyright-release-form is really at 2 credits; avoid a pull there).
- A6 side effects: expense-report-form (reviewed) now fails K8 after the merges (needs one writer sentence); medical-history-form (parked) the same.
- Not fixed, noted by A5 writers: document-automation Q9 says "twenty invoices" (numerals rule for 10+); sales and task automation Q10 each carry two Emergent sentences; employee-engagement-survey Q8 near the width limit (P2).

## Open questions for Divit (recommended default first)
1. **Unlisted PA14 names (A5):** none on the 20 live pages.
2. **A8:** check GTM-NCCB99P9 for triggers on Form ID `email-form` (default: if none, change the 3 components' form ids one at a time as in the doc).
3. **A6:** approve 3 reconciliation rows in credits.log (default yes); leave the 49 credit-capped written pages parked (default); re-queue the never-written pages parked only for the retired F4 (default yes); hipaa-release-form (15 sources) stays parked under the HIPAA ruling (default yes).
4. **K7 matcher:** fix multi-word brands ("Adobe Acrobat" vs adobe.com/acrobat) so it stops false-flagging (default yes, next rule pass with a golden case).
