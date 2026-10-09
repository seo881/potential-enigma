# Backlog (rules freeze for launch)

Divit, 2026-10-08: no new QC rule or rule change until batches 1-3 are live. New feedback, proposed rules and recurring review notes land here and are taken up after launch. Only factual errors on a page are fixed immediately (on the page itself).

Format: date, source (Divit, reviewer, QC, orchestrator), the item, pages it touches, proposed change.

## Deferred by decision (2026-10-08)
- The 12 synonym rescues (parked pages rescued by safe PA3 synonyms): `.cache/review/synonym-candidates-compact.csv`.
- The 51 parked pages that need a second AlsoAsked pull (1 credit each): `.cache/review/park-rescue.csv`.
- The 7 intent-mismatch pages stay parked (merge or drop proposals in `reports/2026-10-08/2121-deterministic-pass.md`).

## Items
- 2026-10-09, reviewer launch-r-b1-3: QC K7 said Google Forms is not in the top 10 for sign-in-form while it ranks #1; possible URL-matching bug in K7. Pages: sign-in-form. Proposed: check K7's competitor URL matching after launch.
- 2026-10-09, writers (batch 1): QC F4 still requires DataForSEO PAA questions that the approved PAA gate (PA1-PA13) rejects; the only exit is a reasoned per-page skip in rules/paa_blocklist.json, which needs Divit (auto mode refused it as a gate bypass). Pages: ecommerce-automation, contact-form, 404-page, pricing-page, employee-engagement-survey, booking-form. Proposed: F4 honours gate rejects, or Divit approves the skips page by page.
- 2026-10-09, writer launch-w-booking-form: QC F2 has no source type for AlsoAsked-only questions (paa requires the DataForSEO capture), so a gate-passing AlsoAsked replacement cannot be recorded validly; writers recorded them as secondary or keyword with provenance. Proposed: F2 accepts source "alsoasked" with prov.
- 2026-10-09, writers (batch 1): no allowed replacement source left on consultation-form, checkout-form, conference-registration-form, summer-camp-registration-form (AlsoAsked pulls thin or empty, every secondary already carried). Proposed: per-page PA3 synonyms, keyword-idea sources, or second pulls (Divit).

## Found in Divit's PA13 read (2026-10-09)
- PA9 missed a near-duplicate pair on employee-engagement-survey (Q4 "good questions for an employee engagement survey" vs Q5 "best questions to ask in an employee survey"): same-intent test is too lexical.
- PA8 did not cap Contact Form 7 (a WordPress plugin brand); add plugin and product names to the brand list.
- Question display text: normalise keyword spellings ("tshirt", "t shirt") to the house form ("T-shirt") while keeping the original in provenance.
- PA4/PA6: "What is a contact form owner?" and "What does 'form of contact' mean?" passed; dictionary-sense and ownership questions are drift.

## Found while applying the PA13 fixes (2026-10-09, orchestrator)
- PA9 should compare questions after display normalisation: once "tshirt"/"t shirt" read "T-shirt", t-shirt-order-form Q2 ("make a T-shirt order form online") and Q4 ("make an order form for T-shirts") were the same intent. Q4 was replaced (gate-passing AlsoAsked, Google Forms question).
- t-shirt-order-form: answers and the FAQ heading still carry the keyword spellings "t shirt" and "tshirt" (heading "T Shirt Order Form Questions, Answered"); Divit's ruling covered question display text only. Decide whether answers and heading follow the house form.
- PA10 flag: t-shirt-order-form Q4 (shirt order form on Google Forms) overlaps pre-order-form's Google Forms questions (not shipped); pick the owner when pre-order-form ships.
- 2026-10-09, orchestrator: delete the 187 og.png files under images/ in one commit once the 20 launch pages are verified live (Divit 2026-10-09; WebP replaces them).
- 2026-10-09, orchestrator: `hubctl qc` rewrites qc_passed stamps in every spec it checks, so an all-spec QC sweep dirties ~60 specs; a read-only mode would help regression diffs.

## Duplicate IDs in shared components (Webflow Audits, 2026-10-09)
- email-form (5 elements) and field (4) on child templates come from forms inside shared site-wide components, not from our template content. Fix needs component-definition edits (Divit's go) after checking no script or form handler targets #email-form or #field. Proposed: give each component form a unique DOM id (or bind it to a component prop) one component at a time, with read-back and rollback.

- MONDAY: carousel (section_build) formatting rework on hubs + child templates, then unhide.
- 2026-10-09, orchestrator: the reference page /ai-app-builder/vedic-astrology shows no black selected-chip state (its is-active renders like the default chip; hover is light grey). hubchip--on uses the hero submit arrow's black (#000, white text) as asked; confirm the look on staging.
- MONDAY: Learn list fix: Form, LP and AAB child templates render "No items found" (limit 3, source Learn, no filters, same as SQB which renders); section_blog-related hidden on those 3 for launch (logs/templates.md).
- 2026-10-09 (Divit): add FAQ moat lines to the 20 live pages at next rework (QC F9 applies from batch 2; live pages exempt until then).

## Found in the first live audit (2026-10-09, orchestrator)
- QC H3 serial-comma detector files real misses as "ambiguous" (P2): verb series, noun phrases with modifiers or relative clauses, 4-item lists. Golden cases h3-gap-* (open). Then sweep the 20 live pages; confirmed leftovers include event-landing-page faq#1, faq#7, meta_description, howto_step_3_title/des; booking-form faq#2, faq#3; client-onboarding-questionnaire faq#1, faq#2, faq#8; t-shirt-order-form howto_step_1_des, howto_step_5_des, faq; 404-page features_subheading, tab_content_4.
- live-fix verify compares image fields by fileId only when the spec has file_id: after a re-render, write the new fileId/cdn_url to the spec in the same step (ecommerce-automation tab_image_4 was set by hand).
- live-fix verify runs must be sequential (each rewrites findings.json); add a lock file.
- Mockup prompts (awb---mockup-data) are not rendered: Layer B findings on them are P2 until the carousel is back (MONDAY).
- Template (Divit's go): FAQ heading always renders "Your Questions, Answered" instead of the item's heading; JSON-LD description is HTML-escaped (&#39;); comparison tables clip at 390 px; an empty zero-width paragraph after feature 1 (A5-empty-p, 24 P2).
