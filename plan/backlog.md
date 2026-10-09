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
