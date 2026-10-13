# Prevention map (ruling 15.1, Divit 2026-10-13)

Every review finding and rework note to date, grouped by precise class, with the one thing that stops each class in the constrained writing pipeline (code builds the skeleton; writers write prose section by section; QC per section). Bar for the canary: QC 0 on the first run and 0 blocking findings in review.

**Mined:** `specs/*/*.json` (`review.findings`, `slim_reviews[].findings`, `review_notes` deduped against both, `history` rework notes), `audits/live/*/findings.json` (layer B content findings, deduped by url, code and field), `rules/SEVERITY.md`, `rules/CONTENT_DEFECTS.md`, `LESSONS.md`, `qc/qc_hub.py`, `qc/paa_gate.py`, `ops/autofix.py`, `rules/ai_tells.json`. The tally script is in the A-p-1 scratchpad (`tally.py`); rerun it to refresh the numbers.

**Severity.** 679 findings carry a recorded severity (review and slim review). The 319 older `review_notes` (written before `SEVERITY.md` existed) carry none: their severity is inferred from the SEVERITY table through the class. A note stays a note when its own text says "pending with Divit", "carried over", "not a contradiction" or similar, or when that reviewer's verdict had 0 blocking findings. The **Blocking** column below is recorded plus inferred; the recorded share is in brackets.

## 1. Classes ranked by blocking findings

| # | Class | Blocking (recorded) | Note | Example field(s) | Prevention |
|---|---|---|---|---|---|
| 1 | Image contradicts its tab copy (status label, outcome, recipient, a detail the copy names but the image leaves out) | 23 (0) | 52 | image_brief tabs, tab_image_N alt | code check (exists: QC I4 story links; new: see 3.1, every name, number, status word and recipient drawn must be declared in `plan.tab_stories[i]` and appear in tab_content_i) |
| 2 | Cited source does not say what the copy claims (the claim is wider than the source, drops its qualifier, or applies one case to all) | 19 (13) | 20 | faq, howto_step_N_des, tab_content_N | skeleton (code builds it: claims menu; every third-party sentence is picked from `domain_sources[].claim` whose `quote` is checked against the fetched source, see 3.2) |
| 3 | Unsourced claim about a third party, a law or a standard (no `domain_sources` entry) | 18 (10) | 24 | faq, howto_step_N_des | code check (exists: QC C3, brand + fact verb or statistic only; new: see 3.3, any named third party, statute, agency or "the law" sentence without a claims-menu id blocks) |
| 4 | Platform capability not in `capabilities.json` (or built-in behaviour stated as automatic) | 10 (5) | 38 | feature_4, feature_6, faq | skeleton (code builds it: Emergent sentences come from the approved phrasing of each `claims_used` id) + code check (exists: QC C2, A5; new: see 3.4) |
| 5 | Page contradicts itself (a heading, meta description or FAQ against a tab or another field) | 9 (6) | 17 | faq, features_subheading, meta_description, tab H3 | pack instruction (P1) + code check (new: see 3.9, a number or amount in a tab H3 must appear in its body) |
| 6 | Number that does not add up across copy and image | 7 (1) | 16 | faq, features_subheading, image_brief | code check (new: see 3.5, copy numbers that also appear in the tab's brief must match; totals and averages declared with their formula) |
| 7 | Sibling primary or a sibling page's topic in a heading or answered at length | 6 (0) | 30 | faq, feature_N | code check (exists: QC K5 sibling primary in a heading, Q3 H1, D2 near-duplicates) + skeleton (FAQ locked per page, PA10 owner) |
| 8 | False differentiator or wrong fact about a competitor | 6 (5) | 21 | why_table, why_description, faq | skeleton (code builds it: table from the library, `hubctl table`; QC V1-V5 exist) + code check (new: see 3.6, competitor sentences outside the table must quote a library fact) |
| 9 | Reworded verbatim AlsoAsked question | 6 (6) | 4 | faq | skeleton (code builds it: FAQ questions locked from `faq_sources[].prov.original`; `hubctl verbatim` exists, run as QC, see 3.7) |
| 10 | Comparison table: hub default cell, or competitors not in the top 10 | 4 (0) | 53 | why_table | code check (exists: QC Q4, K7, V4) + skeleton (variant row set by the library) |
| 11 | Page does not deliver the intent (meta promises what no field gives; an FAQ answer does not answer its question) | 4 (0) | 13 | meta_description, faq | pack instruction (P2) |
| 12 | False claim about the world, the law or a third-party system | 3 (2) | 4 | faq, feature_N | skeleton (claims menu, as class 2) |
| 13 | Soft quantifier or generalization ("most", "many", "usually") | 2 (2) | 130 | faq, howto_step_1_des, why_description | code check (new: see 3.8, block when the sentence names a third party or a class of products; P2 otherwise) + pack instruction (P4) |
| 14 | Image alert sent to a channel when the copy names one person | 2 (1) | 12 | image_brief hero | code check (new: see 3.10, recipient kind in the brief must match the copy) |
| 15 | Names that borrow third-party IP or a real person | 2 (0) | 5 | tab_image_N, mockup | code check (new: see 3.11, IP-fiction and notable-people list in `rules/ai_tells.json`) + skeleton (names from a generated pool) |
| 16 | Hero default prompt names an industry, person or scenario | 2 (2) | 4 | hero_prompt | skeleton (code builds it: "Build a {primary} ..." default from a fixed template; writers never write it) |
| 17 | Names map ethnicity, gender or age onto a negative outcome | 2 (2) | 3 | image_brief tables | skeleton (code assigns names from a pool) + code check (new: see 3.12) |
| 18 | One company plays incompatible roles across tabs | 2 (0) | 2 | tab_image_N, mockup | code check (new: see 3.13, one role per company in `plan.tab_stories`) |
| 19 | A stated count disagrees with the items it introduces (steps, rows, companies) | 2 (2) | 0 | howto_description, tab_image alt | code check (new: see 3.14) |
| 20 | chip_adds clause does not build what its chip says, or wrong voice | 2 (2) | 13 | chip_adds | code check (new: see 3.15) |
| 21 | Same idea restated in several fields with words swapped | 1 (1) | 97 | faq, feature_2, feature_3 | code check (exists: QC Q6 exact phrases) + skeleton (section ownership map, see 3.16) + pack instruction (P3) |
| 22 | FAQ question names a brand or asks for a file format | 1 (1) | 1 | faq | skeleton (FAQ locked) + code check (exists: PA14, PA15) |
| 23 | Machine-written or imprecise wording | 0 | 47 | faq, tab_content_N | code check (exists: QC A1-A4 from `rules/ai_tells.json`) + pack instruction (P5) |
| 24 | Word choice or grammar error | 0 | 42 | faq, tab_content_1 | pack instruction (P5) |
| 25 | Other image brief finding (detail, label, layout) | 0 | 37 | image_brief, mockup | code check (exists: engine gates, QC I1, I2) |
| 26 | Serial comma missing or inconsistent | 0 | 31 (54 live P1) | mockup, faq, feature_N | autofix (exists: autofix h3) + code check (exists: QC H3); run on mockup prompts too |
| 27 | Unsourced recommendation (advice) | 0 | 30 | faq, howto_step_N_des | pack instruction (P6) |
| 28 | Paragraph or feature body opens on a label or fragment | 0 | 19 | feature_N, faq | code check (exists: QC Q1) + pack instruction (P7) |
| 29 | Other (precision notes on a source, link density) | 0 | 16 | faq | none (notes) |
| 30 | FAQ link to a sibling page that is not live | 0 | 15 | faq | skeleton (code builds the links: link-to-live list only; K4 exists) |
| 31 | Templated sentence or heading shape repeated | 0 | 15 | why_description, features_subheading | code check (exists: QC A4, D2, `hubctl plan-check`) |
| 32 | Image layout polish | 0 | 10 | image_brief, cover_image | code check (exists: engine balance gate, QC I1) |
| 33 | Numerals for durations and quantities | 0 | 7 | howto_step_N_des | autofix (new: see 3.17) |
| 34 | How-to description promises what the steps do not do | 0 | 7 | howto_description | skeleton (code builds the description from the step titles' verbs) |
| 35 | domain_sources hygiene (orphan, dead, over the ceiling) | 0 | 6 | domain_sources | code check (exists: QC P2, P3, P4; new: orphan source, see 3.18) |
| 36 | Two terms for one thing, or a UK term | 0 | 5 | meta_description, feature_N | code check (exists: QC H2, H4) + pack instruction (P5) |
| 37 | FAQ answer arrives late or never says yes or no | 0 | 5 | faq | code check (exists: PA12 answer-first) + pack instruction (P2) |
| 38 | Tacked-on ending or run-on list | 0 | 5 | feature_N | code check (exists: QC A1, Q2, Q5) |
| 39 | FAQ link forced into an answer it does not help | 0 | 4 | faq | skeleton (code picks the link slot: the item whose topic matches the target's primary) |
| 40 | Stock or reused names across pages | 0 | 3 (36 live P1) | tab_content_N, image_brief | code check (exists: QC A1 stock_names; new: see 3.11, reused persona names across specs) |
| 41 | Weekday or date that does not match | 0 | 2 | plan | code check (exists: engine date checks) |

Live audit layer A (template: empty paragraphs, 390 px layout, sitewide testimonials) is template work, outside the writer loop, and is not counted above.

## 2. Page-pack instructions

These go into every page pack, next to the section they govern. The examples are generic and written for this doc.

**P1. One story, said the same way everywhere (class 5).** Before you write a heading, the meta description or an FAQ answer, read the tab or field it summarizes and state only what that field shows. A summary covers every tab or names the one it means. A rule keeps its exact threshold, unit and trigger wherever it appears.
- GOOD: H3 "Orders over $500 wait for a manager", body "An order over $500 waits for the manager", image "Rule: over $500".
- BAD: H3 "Large orders wait for a manager", body "Monthly spend of $500 or more waits", image "Rule: $750". Three different rules.
- BAD: meta "Every study compares you with rivals" when only one of four tabs does.

**P2. Deliver what the page promises, and answer the question asked (classes 11, 37).** The meta title and description may promise only what a body field delivers; check each promise against a field before you keep it. An FAQ answer's first sentence answers the question exactly as asked (yes or no, the number, the name), in the question's own terms.
- GOOD: Q "Is a quote the same as an invoice?" A "No: a quote is the price you offer before the work; an invoice asks for payment after it."
- BAD: the same question answered by contrasting quotes with estimates, so "invoice" is never placed.
- BAD: meta "Learn how to word your request" on a page with no wording guidance.

**P3. Each point has one home (class 21).** The section map lists which field owns each idea (the rule, the threshold, the test run, the export). Say it there once. Another field that touches it adds something new (the number, the exception, the next step) or leaves it out. FAQ answers add what the body does not say.
- GOOD: feature_3 "Low-confidence values go to a reviewer"; FAQ 5 "You set the threshold, and the queue shrinks as corrections teach the rules."
- BAD: feature_3, tab 1, step 7 and FAQ 5 each say "unclear values are sent to a person to check" with the words swapped.

**P4. Quantify or name; never "most" (class 13).** Do not use most, many, usually, often, typically or generally about businesses, platforms or the world. Name the source's subject ("Three of the four tools in the table charge per user"), state the rule as advice ("Keep it under ten questions"), or cut it.
- GOOD: "Both tools in the table email a receipt by default" (each sourced).
- BAD: "Most payment tools email a receipt" (sourced for one tool).

**P5. Plain operator wording (classes 23, 24, 36).** Write what happens, to whom, with what number. One term per thing on the whole page (pick "vendor" or "supplier", not both). US terms only. Read every sentence aloud: if a verb cannot act on its object ("hours are checked against a rate"), name the thing that is checked.
- GOOD: "The billed rate is checked against the contract rate."
- BAD: "Hours get validated against the rate, keeping everything aligned."

**P6. Advice is advice, labeled as yours (class 27).** A recommendation is phrased as an instruction to the reader ("Test it with five real entries first"), never as what the law, an industry or "experts" require. Anything framed as a requirement needs a claims-menu entry.
- GOOD: "Ask for the start date in the first section, so it can drive the reminders."
- BAD: "Employers are required to confirm the start date before day one."

**P7. Open on a full sentence with a verb (class 28).** Every paragraph, feature body and FAQ answer starts with a subject and a verb that says what happens. No keyword labels, no noun lists ending in "generated from your prompt".
- GOOD: "Emergent builds the sections a standard application carries: contact, history, references."
- BAD: "Contact details, history, references and a signed certification, from your prompt."

## 3. New code checks and autofixes to build (priority order)

Ordered by blocking findings prevented. Each names the rule and the field it reads.

1. **I5 story lock (class 1, 23 blocking; class 14 and 18 share the data).** Field: `image_brief.tabs[i]` against `tab_content_{i+1}` and `images.tab_image_{i+1}.alt`. Rule: every person name, company name, number with unit, and status word drawn in tab i (hero, main, mini) must be listed in `plan.tab_stories[i].entities`, and every entity listed there must appear in tab_content_{i+1}. One status word per item per image (an item drawn twice must carry the same label). Alt numbers must equal the brief's declared counts. P1.
2. **Claims menu with quotes (classes 2 and 12, 22 blocking).** Field: `domain_sources[]` and every copy field. Rule: each `domain_sources` entry gains `quote` (the source's own sentence) and `scope` (who it covers: one vendor, one state, one plan). `hubctl sources-check` fails the entry when `quote` is not found in the fetched page text. The skeleton hands the writer a menu of claim sentences built from the quotes; a copy sentence that names a third party, a law or an agency must carry the claim id (spec `claims_map: {field: [ids]}`), and QC fails a sentence that widens the scope (plural subject when `scope` is one vendor or state). P1.
3. **C3 widened (class 3, 18 blocking).** Field: every copy field except why_table. Rule: a sentence blocks when it names any third party (competitor library, `rules/facts.json` brands, plus capitalised product, agency and statute patterns: "Act", "Code", "§", "CFR", "IRS", "EEOC", ".gov") with a factual verb (is, has, requires, lets, charges, stores, keeps, supports, must), and its field has no claims-menu id that covers it. P1.
4. **C2 phrasing lock (class 4, 10 blocking).** Field: every copy field. Rule: a sentence with Emergent or "the app" as subject and a platform verb (hosts, exports, keeps, logs, indexes, stores, sends, signs) must match an `approved[].phrasings` regex of an id in `claims_used`; otherwise P1. Add `phrasings` to each entry in `rules/capabilities.json`.
5. **N1 numbers agree (class 6, 7 blocking).** Fields: tab_content_N, faq, features_subheading against `image_brief` checks. Rule: a number with a unit or currency that appears in a tab's copy and its brief must be equal; any total, average, share or difference in copy must be declared in `plan.numbers` as `{value, formula}` and the formula must evaluate to the value. P1.
6. **V6 competitor sentences (class 8, 6 blocking).** Fields: why_description, faq. Rule: a sentence naming a competitor in the page's `table.vs` must contain a phrase from that competitor's library fact cells (`rules/competitors/*.json`); a comparative ("unlike", "no per-", "only Emergent") against a named competitor blocks unless the library cell for that competitor states the opposite. P1.
7. **F7 verbatim as QC (class 9, 6 blocking).** Field: faq. Rule: an FAQ question whose `faq_sources[i].prov.tool` is alsoasked-api must equal `prov.original` after whitespace and final-`?` normalization (the logic of `hubctl verbatim`, run inside `qc_hub.check`). P0.
8. **Q10 soft quantifier on a third party (class 13, 2 blocking, 130 notes).** Fields: every copy field. Rule: most, many, usually, often, typically, generally, the majority in a sentence that also names a product class or a third party (competitor library, "platforms", "tools", "banks", "agencies", "employers") blocks (P1) unless the field has a claim id with `scope: class`; anywhere else P2.
9. **T2 heading agrees with body (class 5).** Field: tab_content_N and feature_N. Rule: any number, amount or threshold in the H3 must appear in the same field's body. P1.
10. **I6 recipient kind (class 14, 2 blocking).** Field: `image_brief.tabs[i]` message blocks. Rule: when tab_content names a person as the receiver ("to Ana", "alerts the manager", "messages {Name}"), the drawn message must be a direct message or a card addressed to that person; a `#channel` target blocks. P1.
11. **A7 names list (classes 15 and 40, 2 blocking, 36 live P1).** Fields: every copy field and every image_brief string. Rule: `rules/ai_tells.json` gains `ip_names` (fiction companies such as the CONTENT_DEFECTS #23 list) and `notable_people` (block, P1); a person or company name already used in more than 2 other specs blocks (P1, reused persona). The skeleton supplies a fresh per-page name pool, so writers do not invent names.
12. **I7 outcome spread (class 17, 2 blocking).** Field: image_brief rows with tone warn or bad. Rule: names on negative rows are drawn from the same pool buckets as names on positive rows; if all negative rows share a bucket that no positive row uses, block. Buckets come from the name pool's origin tags. P1.
13. **I8 one role per company (class 18, 2 blocking).** Field: `plan.tab_stories[].entities`, image_brief. Rule: each company carries one role (lead, customer, vendor, applicant); the same name in two tabs with two roles blocks. P1.
14. **S11 counts agree (class 19, 2 blocking).** Fields: howto_description, alt text. Rule: a count word or numeral before "steps" must equal the number of filled howto steps; "N {noun}" in an alt must equal the count the brief draws for that noun. P0.
15. **L12 chip clause matches its label (class 20, 2 blocking).** Field: chip_adds[i]. Rule: the clause must contain the head noun (or its stem) of chip label i, and no first or second person pronoun ("my", "your"). P1.
16. **Section ownership map (class 21).** Field: spec.plan. Rule: the skeleton writes `plan.owns: {idea: field}` from the angle; QC Q6 widens to a content-word overlap test (5 or more shared content stems in one sentence pair across two fields, page keywords excluded) and reports it as P2 against the owning field. P2.
17. **Autofix numerals (class 33).** Fields: every copy field except titles. Transform: spelled-out cardinals two to ninety-nine before a duration or unit (minutes, hours, days, weeks, months, years, steps, questions) become numerals ("two weeks" to "2 weeks"); sentence-initial words untouched. Guarded by the autofix QC-before-after rule.
18. **P5 orphan source (class 35).** Field: domain_sources. Rule: every entry's claim id must be referenced by `claims_map`; an unreferenced entry is P2 and counts toward the 8-source ceiling.

## 4. Totals

| Measure | Count |
|---|---|
| Findings mined (specs: review, slim review, review notes, deduped) | 998 |
| of which severity recorded / inferred | 679 / 319 |
| Live audit content findings (unique by page, code and field; counted separately) | 354 |
| Classes | 41 (plus "other") |
| Blocking findings | 133 (60 recorded, 73 inferred) |
| Note findings | 865 |
| Blocking prevented by code (check, autofix or skeleton): classes 1-4, 6-10, 12-20, 22 | 119 of 133 (89%) |
| Blocking left to the page pack: classes 5, 11, 21 | 14 of 133 (11%) |

Caveat: the claims menu (3.2) moves source accuracy from the writer to the menu builder. A menu claim is checked once against its quote, then reused, so a bad quote fails in one place instead of on every page. Classes 2 and 12 (22 blocking) count as code only once `quote` and `scope` are filled for every source.
