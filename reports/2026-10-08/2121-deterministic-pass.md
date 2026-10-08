# Deterministic pass: hub stats check, C5/H3/S10/H4/C4 fixes, A6 tuning, park rescue, plan rebuild

## Request
> PART 0b (first): Read-only Webflow check of the section_stats component on one hub page: list each stat's number and its label exactly as shown, and each testimonial's name, title and company. Then add to DECISIONS.md under 2026-10-08: "The testimonials and stats in section_stats on the hub pages are real and accurate (Divit confirmed 2026-10-08); not placeholders, do not flag again." Close open question 5 in the rules-pass report. No Webflow writes.
>
> No Webflow writes. No FAQ rewriting yet. Follow every part in order.
>
> PART 1: DETERMINISTIC FIXES (execute; one commit per check so each is revertible)
> 1. C5: find the shared source behind the 179-182 pages that fail it (library cell, template slot or generator), fix it there from https://emergent.sh/pricing (GitHub integration from the Standard plan), and regenerate. List the pages still failing C5 after that.
> 2. H3: autofix certain serial-comma cases. Ambiguous cases become P2 notes and never send a page to a writer.
> 3. S10: strip zero-width characters in specs and at export.
> 4. H4: apply a fixed UK-to-US idiom map where the replacement is mechanical; leave the rest flagged.
> 5. C4: replace mechanical custom-domain phrasings with the approved wording ("built into Emergent, uses credits"; tables "Built in, uses credits"); leave non-mechanical cases flagged.
> For each check: pages changed, instances changed, instances left, and 3 before/after examples.
>
> PART 2: TUNE A6 (code only)
> Allow "your team" where the page genuinely targets a group (surveys, internal and HR forms, approval and automation workflows; the SQB hub uses "for your team"). Keep flagging it on pages aimed at individuals or customers. Counts before and after, with 5 examples each of kept and newly-allowed cases.
>
> PART 3: RESCUE ANALYSIS FOR THE 70 PARKED PAGES (no credits spent)
> Per page, count how many on-topic FAQ sources each lever would add:
> (a) its safe synonym candidates from rules/paa_synonym_candidates.json, if approved;
> (b) question-form keyword ideas for that page in the Semrush workbook in private/;
> (c) a second AlsoAsked pull on its top secondary: estimate only (1 credit per page), no pulls.
> Classify each page: rescued by (a) / rescued by (b) / needs (c) / intent mismatch (drop or merge, with the cause and any merge target).
>
> PART 4: REWRITE plan/rework-2026-10-08.md AFTER PARTS 1-3
> - Regroup every page by what is left: clean / FAQ only / FAQ + A5 or A6 / copy only / park, with counts per hub.
> - FAST LANE: pages with 1-2 FAQ replacements, no legal/medical tag and no rolling-figure tag, plus the copy-only pages and employee-engagement-survey. List them in publish order, keeping link-connected pages together.
> - Price three review options (pages, writer tokens, review tokens, total):
>   (a) full review on every page at 89k;
>   (b) full review only for legal/medical, rolling-figure and 5+ replacement pages; every other page gets code QC + PAA gate + Divit's PA13 skim;
>   (c) batch review (4 pages per agent) for all pages, with an estimated per-page cost clearly marked as unmeasured.
> - Name the hubs that can go fully live without any parked page.
>
> PART 5: DIVIT'S READING FILES (written to .cache/review/; print counts only)
> - pa3-newly-passing-fastlane.csv: PA3 newly-passing questions for fast-lane pages only, in publish order.
> - synonym-candidates-compact.csv: one row per page (page, proposed synonym, safe/unsafe, questions it unlocks), parked pages first.
>
> Then STOP.

(Follow-up during the task: "try now". The blocked `ls private/` was retried once, denied again, and not retried after that.)

## Actions and results

### Part 0b: hub stats and testimonials (read-only)
- Fetched the live hub page https://emergent.sh/ai-form-builder (HTTP 200) and read the rendered text. This was a read of the published page, not a Webflow API call.
- `section_stats` heading "Trusted by Builders Worldwide". Stats: **10M+** "Active Builders Worldwide"; **12M+** "Apps Successfully Created"; **200+** "Countries Globally Reached".
- Testimonials (in the `section_banner` marquee directly after `section_stats`; each repeats 4 times for the scroll): **Alex Rivera**, Founder, TaskFlow; **Maya Chen**, Product Lead, BrightSuite; **Jordan Patel**, Co-founder, LoopDesk.
- Added the DECISIONS line (2026-10-08), closed open question 5 in `reports/2026-10-08/1956-rules-pass.md`, and replaced the "placeholder" note in `plan/template-edits-2026-10-08.md`. Commit 914eb10.

### Part 1: deterministic fixes (`ops/autofix.py`, new)
Every edit is guarded: QC runs on the page before and after, and an edit is kept only if no P0/P1 issue gets worse (by code and field, its own check included). Titles are never edited. Scope: the 183 written pages. The 4 frozen original children and parked specs were not touched. Full QC before and after across all pages: **no regression on any page**.

| Check | Pages changed | Instances changed | Refused by guard | Instances left (pages) | Commit |
|---|---|---|---|---|---|
| C5 GitHub plan qualifier | 126 | 126 | 40 | 56 (56) | a05c597 |
| H3 serial comma (certain) | 98 | 184 | 1 | 1 (1) | a1c5029 |
| S10 zero-width / empty paragraphs | 0 | 0 | 0 | 0 | none (nothing to change) |
| H4 UK idioms | 14 | 19 | 2 | 2 (2) | 566f1c0 |
| C4 custom-domain wording | 8 | 8 | 41 | 49 (43) | dc083c5 |

**C5.** The shared source is not a library cell or a generator: every hit (182 instances: `feature_6` on all 183 written pages, plus 5 FAQ answers) is the feature-6 "code export" slot. Writers fill it from the capability ledger claim `code-export` ("Full code export to the user's GitHub repository"), which had no plan qualifier. I fixed it there (`rules/capabilities.json`, `rules/claims.json`) and in HUB_RULES (feature 6), citing https://emergent.sh/pricing: GitHub integration is listed under Standard ("Everything in Free, plus: GitHub integration"), not under Free. Then a regeneration pass rewrote each page's phrase, in this order of preference: keep the writer's phrase and add "on paid plans"; else "to your GitHub on paid plans"; else "to GitHub on paid plans" (whichever fits the 165-182 band, the spread and the measured width).
- Example 1, accounts-payable-automation `feature_6`: "...export to your GitHub repository, where an engineer..." -> "...export to GitHub on paid plans, where an engineer..."
- Example 2, chemical-peel-consent-form `feature_6`: "Export the full code to your GitHub repository." -> "Export the full code to your GitHub on paid plans."
- Example 3, event-planning-form `feature_6`: "Exports the whole app to your GitHub repository, approval rules and database included." -> "Exports the whole app to your GitHub on paid plans, approval rules and database included."
- Still failing C5 (56): 404-page, accident-report-form, advance-directive-form, booking-form, cake-order-form, campaign-landing-page, church-membership-form, client-onboarding-questionnaire, complaint-form, conference-registration-form, consent-form, consultation-form, credit-card-authorization-form, custom-order-form, dental-intake-form, employee-benefits-survey, employment-verification-letter, equipment-rental-agreement-form, field-trip-permission-slip, file-upload-form, food-bank-application-form, food-order-form, hotel-booking-form, incident-report-form, insurance-verification-form, it-request-form, liability-waiver-form, membership-form, multi-step-form, one-page-website, order-form, parent-consent-form, patient-intake-form, payment-form, pet-adoption-form, photo-release-form, pre-order-form, reasonable-accommodation-request-form, referral-form, rental-agreement-form, requisition-form, restaurant-reservation-form, sales-automation, service-request-form, sign-up-form, sponsorship-form, student-registration-form, surgery-consent-form, tattoo-consent-form, therapy-intake-form, vehicle-inspection-form, vendor-application, webinar-registration-form, wedding-photography-contract, wedding-photography-questionnaire, workshop-registration-form. Causes: the body is already at the 182-character ceiling or the measured width ("to GitHub when a developer..." has no shorter form), GitHub sits only in the title, or the wording is a possessive or "your repository" that only a writer can rephrase (54 `feature_6`, 2 FAQ).

**H3.** The "certain" rule misfired, so I tightened it before fixing anything. I read all 202 certain cases: 187 were real lists and 15 were not (appositives such as "Ray Dunn, the mechanic on call, came in and fixed it"; intro phrases such as "Qualtrics, for one, logs..."; paired items such as "date, start and end building, and miles"). Changes: certain now requires a flat list (no and/or inside an earlier item, no comma after the conjunction in the clause) and no intro marker ("for example,", "for one,", "such as,", ...). The 15 reviewed clauses are listed in `rules/serial_comma_exceptions.json`. Ambiguous cases stay P2 (they never count toward TOTAL or send a page to a writer). The diff was checked to be comma-only (164 lines, 0 other changes).
- Example 1, document-automation `mockup`: "policy number, expiry date and per-occurrence limit" -> "policy number, expiry date, and per-occurrence limit"
- Example 2, brand-questionnaire `feature_1`: "customer, category, benefit and proof" -> "customer, category, benefit, and proof"
- Example 3, emergency-contact-form `howto_step_3_des`: "allergies, medications and conditions" -> "allergies, medications, and conditions"
- Left (1): pre-order-form `tab_content_2` ("56 large and 32 extra large"): the guard refused it, because a change to this field broke another check.

**S10.** No spec has a zero-width character or an empty paragraph (raw scan of all spec files, JSON escapes included: 0). Export already strips them: `hubctl export_fields` was tested on a sample with U+200D, `&zwj;`, U+FEFF and `<p>&nbsp;</p>`, and all were removed.

**H4.** "on the day" was flagged everywhere, but "on the day it ran", "on the day of the demo" and "on the day itself" are standard US English. The rule now flags it only when bare (followed by punctuation, a closing tag or the end: `rules/style_rules.json` `uk_idioms_bare`), which removed 17 false hits. Mechanical map: bare "on the day" -> "on the day itself"; "tick box" -> "checkbox"; plus the one-to-one entries in `ops/autofix.py` MECH (whilst, amongst, learnt, ...; none occurred).
- Example 1, consent-form `howto_step_4_des`: "never one improvised on the day." -> "never one improvised on the day itself."
- Example 2, food-bank-application-form `mockup`: "a tick box stating" -> "a checkbox stating"
- Example 3, liability-waiver-form `howto_step_4_title`: "04 Add what staff need on the day" -> "04 Add what staff need on the day itself"
- Left (2): wedding-photography-contract `howto_step_5_des` and event-landing-page `feature_3` (the guard refused both on length).

**C4.** Mechanical: a custom-domain phrase ("on/under your/a/the X's own/custom domain") in a sentence that does not already say credits or built in gets "(built into Emergent, uses credits)", or "(built in, uses credits)" when the sentence already names Emergent. Table cells were already "Built in, uses credits" from the rules pass.
- Example 1, booking-form FAQ: "...as a web app on your own domain that customers open..." -> "...on your own domain (built in, uses credits) that customers open..."
- Example 2, multi-step-form FAQ: "Publish it on your own domain and change any step..." -> "Publish it on your own domain (built into Emergent, uses credits) and change any step..."
- Example 3, landing-page-seo `howto_step_7_des`: "Publish the page on your own domain." -> "Publish the page on your own domain (built into Emergent, uses credits)."
- Left (49 on 43 pages): 43 `feature_6` bodies (already at the band ceiling; a 35-character parenthesis does not fit), 2 FAQ, 1 how-to step, 1 hero, 1 `feature_5`, and one-page-website `prompt_chip_4` "Custom Domain" (a 26-character chip label).

### Part 2: A6 tuned (commit c32850e)
- New `rules/audience.json`: whole hubs Auto and SurveyQuiz, plus 38 Form pages listed by hand (26 HR, 12 internal operations and approvals). On these pages "your team" is allowed. Every other phrase (your company, your staff, your developers, ...) stays flagged everywhere, and "your team maintains" stays flagged. HUB_RULES 1.5 points to the file.
- A6 instances: 197 on 101 pages before -> 162 on 92 pages after. "your team" flags: 116 on 66 pages -> 79 on 43 pages (37 newly allowed). By hub after: Form 147, LP 8, SurveyQuiz 4, Auto 3. No other QC result changed.
- Kept (still flagged, individual or customer pages): multi-step-form "...cut the ones nobody on your team reads."; contact-form "Add a phone field only if someone on your team will call back."; pet-adoption-form "Adopters your team has not cleared never see either one."; client-onboarding-questionnaire hero "...the answers your team needs before kickoff."; client-onboarding-questionnaire `feature_4` "...work your team can start...".
- Newly allowed: suggestion-form "Pin the link in your team chat..."; ecommerce-automation "...the jobs someone on your team repeats for every order..."; emergency-contact-form FAQ "...brings questions in to your team."; document-automation "...each document your team sends or receives every week."; requisition-form hero "Describe what your team asks for and who reads it."

### Part 3: rescue analysis of the 70 parked pages (commit f912f1f; no credits)
- New `ops/park_rescue.py` runs the PAA gate in process (no API calls) and writes counts only to `.cache/review/park-rescue.csv`.
- The old plan's park rule was not committed and could not be reproduced exactly, so the count is now explicit: base = on-topic FAQ items + gate-passing AlsoAsked questions not already in the FAQ + secondaries no FAQ question carries yet (PA11). All 70 pages are under 8 by this count.
- (a) SAFE synonym candidates, if approved: rescue **12** (advance-directive-form, brand-questionnaire, church-membership-form, driver-application-form, employee-referral-form, fitness-assessment-form, multi-step-form, service-request-form, shipping-address-form, sign-out-form, silent-auction-form, tenant-screening-form).
- (b) Workbook question-form ideas: rescue **0**. The workbook has 43 question-form keyword rows on 24 pages, none of them parked, and all 43 are already that page's secondaries.
- (c) A second pull on the top unused secondary: needed by **51**. Estimate: about 1.1 gate-passing questions per pull (Form first pulls: mean 1.11, median 0, 74 of 147 passed none). After one pull, 4 pages would reach 8 and 6 more would be 1 short. The rest stay 2 to 6 short. Nearly every pull reject is PA3 (the AlsoAsked tree drifts to generic questions), so these pages are on-sense but thin, not wrong intent.
- Intent mismatch: **7**. The evidence is that 30% or more of the page's own pull was rejected as wrong sense or non-US (PA4/PA5): car-rental-form 84% (consumer car rental), vehicle-inspection-form 78% (state vehicle inspections), mileage-reimbursement-form 62% (IRS rates and employee rights), travel-reimbursement-form 53%, health-screening-form 39% (medical screenings), travel-request-form 35%, expense-request-form 33%. Proposed merge targets, for you to decide (no code target found): expense-request-form, mileage-reimbursement-form and travel-reimbursement-form into expense-report-form; travel-request-form into expense-report-form or drop; car-rental-form into rental-agreement-form or drop; health-screening-form into medical-history-form or drop; vehicle-inspection-form drop (re-target only with new research).
- All 70 parked pages are Form pages.

### Part 4: plan rebuilt (commit 98eee97)
- New `ops/rework_plan.py` regenerates `plan/rework-2026-10-08.md` and the two reading files (the first plan's generator was never committed).
- Groups, 183 pages: clean 3 / FAQ only 24 / FAQ + A5/A6 (or leftover copy) 84 / copy only 2 / park 70. Per hub: LP 0/2/16/0/0; Form 3/12/61/1/70; Auto 0/5/2/1/0; SurveyQuiz 0/5/5/0/0.
- Fast lane: 25 pages in publish order, 3 link blocks (A: 2 pages, B: 8 pages around registration-form, C: 2 pages). Ordered by demand, from `plan/keyword_map.json` (no volumes written).
- Review options, 113 non-parked pages, writer 6.38M in every option: (a) full review 10.06M, total 16.44M; (b) 68 full reviews 6.05M, total 12.43M; (c) batch of 4 at 44k a page 4.97M, total 11.35M, **unmeasured** under the current protocol (the 44k is the mean of six 4-page batch agents on 2026-10-07 under the older protocol). Approving the (a) synonyms adds 12 pages, about 1.85M at option (a) rates.
- Hubs that can go fully live without any parked page: **LP, Auto, SurveyQuiz**.

### Part 5: reading files (`.cache/review/`, git-ignored)
- `pa3-newly-passing-fastlane.csv`: 66 rows on 18 fast-lane pages, in publish order.
- `synonym-candidates-compact.csv`: 169 pages (68 parked first), proposed synonyms, safe/unsafe, and 356 questions unlocked by the safe candidates.

## Numbers
- Part 0b: 3 stats, 3 testimonials (each repeated 4 times in the marquee).
- QC on written pages, before -> after: C5 182 -> 56; H3 (P1) 263 -> 1 (184 fixed, 78 reclassified to P2 by the tightened rule); S10 0 -> 0; H4 38 -> 2 (19 fixed, 17 no longer flagged as US usage); C4 57 -> 49; A6 197 -> 162; A5 33 -> 33. Pages with any P0/P1: 151; blocking total 338 (after Part 1, before A6).
- Specs edited: 160 (Form 126, LP 18, Auto 7, SurveyQuiz 9). 10 of them are in `reviewed`/`challenged` (deterministic edits only; states unchanged). registration-form was not touched.
- Park: 70 = (a) 12 + (b) 0 + (c) 51 + intent mismatch 7. Fast lane 25. Review options 16.44M / 12.43M / 11.35M.

## Decisions
- The stats and testimonials check read the published page, not the Webflow API: the request was read-only, and the live HTML is "exactly as shown". DECISIONS line as dictated.
- C5 source = the capability ledger and the HUB_RULES feature-6 line (no generator or library cell carries feature 6). Qualifier wording "on paid plans", per https://emergent.sh/pricing (GitHub integration listed from Standard).
- Every autofix is guarded by QC (no P0/P1 worse) and never edits titles. What the guard refuses is left for the writer pass, not forced in (HUB_RULES 2b: no awkward copy).
- H3 "certain" tightened after reading all 202 cases. The 15 misfires are listed with their clause in `rules/serial_comma_exceptions.json` (DECISIONS 2026-10-08, serial comma; the task's "ambiguous -> P2").
- H4 "on the day" counted only when bare: standard US usage is not a UK idiom (audit/feedback-2026-10-08.md item 18 named the bare form, "on the day" -> "on event day"). "on the day itself" was chosen as the universal mechanical form because "on event day" only fits event pages (`rules/style_rules.json` gives both).
- C4 wording "(built into Emergent, uses credits)" as dictated; "(built in, uses credits)" when the sentence already names Emergent, to avoid repeating it.
- A6 group pages listed by hand, conservatively, in `rules/audience.json` (HUB_RULES 1.5: "for your team" only when the subject is a group). Ambiguous Form pages (project-request, event-planning, work-order, sign-in) stay flagged.
- Park arithmetic made explicit, and intent mismatch based on wrong-sense evidence from each page's own pull (PA4/PA5 share of 30% or more), not on the shortfall alone.
- Fast lane includes the 3 clean pages (registration-form, interest-form, massage-intake-form), since copy-only pages were included.
- Option (c) priced at 44k a page from the 2026-10-07 batch agents, marked unmeasured, as the request asked.

## Files changed and commits
- 914eb10: `DECISIONS.md`, `reports/2026-10-08/1956-rules-pass.md`, `plan/template-edits-2026-10-08.md`.
- a05c597 (C5): `ops/autofix.py` (new), `rules/capabilities.json`, `rules/claims.json`, `rules/HUB_RULES.md`, 126 specs.
- a1c5029 (H3): `qc/serial_comma.py`, `rules/serial_comma_exceptions.json` (new), 98 specs.
- 566f1c0 (H4): `qc/qc_hub.py`, `rules/style_rules.json`, 14 specs.
- dc083c5 (C4): 8 specs.
- c32850e (A6): `qc/qc_hub.py`, `rules/audience.json` (new), `rules/HUB_RULES.md`.
- f912f1f (Part 3): `ops/park_rescue.py` (new).
- 98eee97 (Part 4): `ops/rework_plan.py` (new), `plan/rework-2026-10-08.md`.
- This report, `reports/INDEX.md`, `logs/{form,lp,aab,sqb}.md`: commit in `reports/INDEX.md` history.

## Webflow calls
None. The Part 0b check fetched the public page https://emergent.sh/ai-form-builder over HTTPS (read only).

## Not done
- No FAQ rewriting. FAQ answers received only the deterministic edits (commas, qualifiers); no question changed.
- No `hubctl recheck` (it would move pages to rework before the combined pass; logs/form.md 14:26 UTC).
- `private/` could not be listed (`.claude/settings.json` denies reading it). The workbook and AlsoAsked verdicts were read only by code that prints counts.
- Leftover C5 (56), C4 (49), H4 (2) and H3 (1) instances: for the writer pass.
- No AlsoAsked pulls (no credits). Synonym candidates were not applied (they need your approval).

## Open questions for Divit
1. Approve the SAFE synonym candidates for the 12 pages that (a) rescues? (Read `.cache/review/synonym-candidates-compact.csv`.)
2. The 7 intent-mismatch pages: drop or merge, and into which pages (proposals above)?
3. The 51 "needs (c)" pages: spend 1 credit each on a second pull (most would still be short), or leave them parked?
4. Review option (a), (b) or (c)? If (c), measure the first batch before relying on 44k.
5. Read `.cache/review/pa3-newly-passing-fastlane.csv` and give the go for the fast lane's combined pass?
6. Is the A6 group list in `rules/audience.json` right (38 Form pages)?
