# MONDAY Part B: today's 20, staged (B1-B4); stopped at B5 for your staging publish

## Digest for Divit
- **20 pages created in the CMS and staged** (isDraft false, not published): the 9 canaries plus 11 high-volume reworked pages. ship-cms verify 20/20, launch pre-flight 20/20.
- **Every page at QC 0 and gate 10/10** (0 rejects) under today's rules.
- **K7 fixed** with competitors that rank for each query: 37 vendors added to the libraries, each fact sourced 2026-10-12. Three pages keep one K7 P2: two are a matcher false positive on "Adobe Acrobat", one is a fill (video-landing-page, where only two real builders rank).
- **Caught before create:** none of the 20 specs had the hero chip clauses (`chip_adds`), so the hero prompt box would have loaded empty. 80 clauses were written, QC rule L11 added, and the 61 other reviewed pages with the same gap went back to rework.
- **Review file:** `.cache/review/batch-2.html` (H1, subhead, meta, 10 FAQ questions; only risky items highlighted). Notification sent.
- **Publish to staging only now.**

## Request
> PART B: TODAY'S 20 LIVE
> B1. Pick 20 from the 81 reviewed pages: the 9 canaries plus the 11 highest-value reworked pages across hubs (MSV, link clusters kept together).
> B2. Fix the K7 note on those 20 (competitors that actually rank for each page's query, from the Semrush/Wave 3 data), regenerate the tables, QC 0, gate 10/10.
> B3. Create the 20 CMS items, verify, then set isDraft false (not published). Pre-flight 20/20.
> B4. Write .cache/review/batch-2.html (H1, subhead, meta, 10 FAQ questions per page; highlight only risky items) and send a notification.
> B5. STOP and tell me: "Publish to staging only now." After I say "staging published": run verify_launch on staging for the 20 + the 20 live + 4 hubs (Learn, carousel, FAQ heading, tables at 390 px, JSON-LD), then the dry live audit. Finish with "Publish to emergent.sh now" or a fix list. After "live": verify-live, relink, live audit with fixes on, retro.

## Actions and results
- **B1:** `plan/batches/batch-2.txt`. Canaries (first 3 new pages per hub through review over the weekend): ebook, mobile, video landing page; data entry, incident response, procurement automation; brand awareness, brand perception, church survey. Reworked (weekend rework ledgers), highest total MSV with every hub represented and link clusters kept together: employment-verification-letter (65,410), rental-agreement-form (42,000), accounts-payable-automation (23,740), direct-deposit-form (22,280), customer-feedback-survey (19,940), liability-waiver-form (15,500), credit-card-authorization-form (14,930), order-form (12,750), invoice-automation (10,490), employee-satisfaction-survey (9,930), landing-page-seo (9,810). The AP, invoice and procurement cluster ships together. contact-form (7,450) stays held (DECISIONS 2026-10-09).
- **B2** (4 agents, one per hub): competitors from the Semrush top 10 and saved SERPs; libraries extended (LP: Instapage, Leadpages, MailerLite, ConvertFlow; Auto: Basware, Rossum, Rillion, Parseur, DocuWare, PagerDuty, Swimlane, Exabeam, Ivalua, Precoro, Procurify; SQB: easyfeedback, LimeSurvey, Attest, Microsoft Forms, SurveyHero, Jotform; Form: Docusign, Adobe Acrobat, BambooHR, PlatoForms, LawDepot, ADP, Eddy, WaiverSign, Square, SurveyMonkey, AidaForm). Tables regenerated with `hubctl table` (row sets and variants unchanged); copy naming old competitors updated (AP FAQ 3 and 8, invoice FAQ 3, landing-page-seo why_description, employee-satisfaction why_description). No FAQ item failed the gate.
- **Hero prompt catch:** all 20 specs had `chip_prompts` (full scenario sentences) but no `chip_adds`. The template script (`ops/template/hero-chips.html`) needs `{label, add}`, so the prompt box would have loaded empty with dead chips. 80 "Add ..." clauses written (one per existing chip label, under 90 characters); 2 defaults made generic (liability-waiver "for my kayak rental business"; landing-page-seo now carries the primary keyword). QC **L11** (P1) added with a golden case.
- **B3:** A6's merges and the new rules re-checked first: QC 0 and gate 10/10 on all 20. Slug check against a fresh read (`cms-check`, 0 of 20 existed). The ship pipeline took each page through check2, images current and `hubctl ready` (the B2 table pass was recorded as the post-review rework, no second review). Payloads built at 0460a249 (images pinned to that commit). Canary first (ebook-landing-page: created, read back, every field present), then the other 19 by collection. `ship-cms` verified 20 drafts, 0 mismatches. `launch.py prepare` (now batch-aware via LAUNCH_BATCH) built the isDraft-false payload and 20 rollback files; sent; all 20 read back `isDraft: false, lastPublished: null`. Pre-flight `LAUNCH_BATCH=batch-2 launch.py preflight`: 20 of 20 pass.
- **B4:** `ops/batch_review.py --slim` writes H1, subhead (hero description), meta and the 10 questions; highlights only real gate flags and a "Check these" box per page (stock company names, persona names reused on other pages, table cells sourced from snippets or absence, remaining K7). macOS notification sent.

## Numbers
- 20 pages: LP 4, Form 6, Auto 5, SurveyQuiz 5. QC 0 on 20/20; gate 10 items, 0 rejects on 20/20.
- 37 library vendors added (LP 4, Auto 11, SQB 6, Form 11), all facts dated 2026-10-12.
- K7 remaining: 3 pages (EVL and liability-waiver: Adobe Acrobat matcher false positive; video-landing-page: Landingi fill). direct-deposit also shows a K7 P2 for Eddy, chosen from the top secondary.
- Gate flags highlighted: PA7 on 3 definition questions (rental-agreement, liability-waiver, credit-card); PA14 on 4 questions whose "names" are acronyms, AP (3 on accounts-payable-automation) and OCR (1 on invoice-automation). I judge neither a brand.
- Highlighted risks: stock company names on 9 pages (Northwind, Globex, Initech, Acme); reused personas (Dana Reyes on video LP and EVL; Dana Whitfield on invoice and 4 live pages; Priya Shah, Ana Ruiz, Sam Ortiz, Marcus Lee, Jonah Reyes).
- Webflow: 20 creates, 20 isDraft updates, 3 bulk reads. Time from first create to pre-flight about 40 minutes.
- Ratchet after L11/J1: 70 unpublished pages to rework (61 reviewed pages lacked chip_adds).

## Decisions
- Selection rule: B1 as written; "across hubs" read as every hub represented, highest MSV within the reworked set; contact-form excluded (held, DECISIONS 2026-10-09).
- B2 pass treated as the one post-review rework (DECISIONS 2026-10-07: one review, one rework, no second review; notes ship).
- chip_adds required (DECISIONS 2026-10-09 hero prompt: generic default + one "Add ..." clause per chip). L11 makes it a gate.
- isDraft false without publish: B3 as written; LESSONS rule 7 risk accepted because your staging publish is the next step (a production publish now would take these 20 live).

## Files changed and commits
- 2e52de3c batch-2 list · 14ddbecd, e377ec3c, a6693278, 4c5783ec B2 tables + libraries · 748ea38c check2/ready · 0460a249 chip_adds + L11 · 00c86a79 drafts verified · d28ab7f8 staged + batch_review --slim · d7918f14 ratchet.
- Paths: plan/batches/batch-2.txt, rules/competitors/*.json, specs (20), status/ship/batch-2.json, status/launch-checklist-batch-2.md, ops/launch.py, ops/batch_review.py, qc/qc_hub.py, tests/golden/*.

## Webflow calls
- create_collection_items (isDraft true), 20 items: LP ebook 6accb1512c9cca4363e93f7c, mobile 6accb1fc9cd3f94473f62a80, video 6accb1fc9cd3f94473f62a82, landing-page-seo 6accb1fc9cd3f94473f62a84; Auto data-entry 6accb27bf4e029b5515a4626, incident-response 6accb27bf4e029b5515a4628, procurement 6accb32573d2b6b752fb8d4e, AP 6accb32573d2b6b752fb8d50, invoice 6accb32573d2b6b752fb8d52; SQB brand-awareness 6accb39f13e0be4f1e5be581, brand-perception 6accb39f13e0be4f1e5be583, church 6accb44a40d5b6e947b71558, customer-feedback 6accb44a40d5b6e947b7155a, employee-satisfaction 6accb44a40d5b6e947b7155c; Form EVL 6accb96b8570d8ef2122bde8, rental-agreement 6accb96b8570d8ef2122bdea, direct-deposit 6accb96b8570d8ef2122bdec, liability-waiver 6accba1c29454f1af2f01f0f, credit-card-authorization 6accba1c29454f1af2f01f11, order-form 6accba1c29454f1af2f01f13.
- update_collection_items isDraft false on exactly those 20 (before: isDraft true, never published; after: isDraft false, lastPublished null). Rollback: set isDraft true on the same IDs (or ops/out/launch-batch-2/rollback/<slug>.json after a publish).
- No publish of any kind.

## Not done
- B5 onward: waiting for your staging publish.
- Part C: not started (build after B is live, per the prompt).
- Persona/stock-name cleanup on the 20: highlighted for your read, not changed (copy passed review; a change now needs a writer pass).

## Open questions for Divit (recommended default first)
1. **Publish to staging only now** (webflow.io; not emergent.sh). The 20 items are non-draft and the 3 Learn sections, 8 carousels and 4 embeds are staged.
2. Stock names (Northwind, Globex, Initech, Acme) on 9 pages: ship as is and add them to QC's AI-tell list for future pages (default), or fix these 9 first.
3. video-landing-page: keep Landingi as the third table column with its K7 P2 (default), or drop to 2 columns (`hubctl table` needs 3).
4. Procurement and incident-response tables use the hub-default Emergent column: approve a procurement variant (default yes) and an incident variant, then regenerate.
5. Batch-2 PA14 "names" AP and OCR: acronyms, not brands (default: add a head-phrase and acronym exemption to PA14 with golden cases).
