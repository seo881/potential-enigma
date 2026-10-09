# Launch blockers: brand and file-format FAQ rules, hero and how-to descriptions, staged on the 20 pages

## Request

Divit (2026-10-09): "URGENT, launch blockers ... A. NEW HARD RULES (PA14 no brand or product names in FAQ questions, PA8 cap 0; PA15 no file formats or download asks; D1 hero description <= 130 chars, primary keyword, leads with what the visitor gets, plain words; D2 how-to description one sentence <= 140 chars, primary keyword, says what the steps achieve) ... B. FIX THE 20 LAUNCH PAGES ... C. LEARN LIST ... D. Report ... Then tell me \"Publish staging again\"." (full prompt in the session).

## Digest

- **Production is live and not yet fixed.**
  - emergent.sh and www were published at 11:38 UTC, and the items again at 13:14 UTC; no Webflow call in this session published anything.
  - All 20 launch pages return 200 on emergent.sh and still show the content from those publishes.
  - The 9 held pages return 404 on both domains.
  - The fixes below are staged, waiting for your staging publish.
- **Rules:** gate PA14 and PA15 and QC D1 and D2 are live in code, rules and docs. Golden suite: 18 cases with no regressions (4 known PA13 misses still open).
- **Counts across all 187 written specs** (not 183):

| Rule | Pages | Questions |
|---|---|---|
| PA14 brand reject | 80 | 120 |
| PA14 unlisted capitalised name (flag) | 43 | 110 |
| PA15 | 89 | 149 |
| D1 | 187 | — |
| D2 | 187 | — |

  - These are the counts before the fixes and do not reflect the acronym exclusions (HTML, PPC, UI) added afterwards. D1 and D2 fail on every spec because no page had been rewritten to them yet.
- **The 20 launch pages:**
  - 23 FAQ questions replaced on 12 pages.
  - 20 hero descriptions and 20 how-to descriptions rewritten.
  - QC 0 and gate 10/10 on all 20.
  - One review of the changed fields (5 reviewers) found 2 blocking unsourced facts; one rework fixed both.
  - CMS updated with changed fields only; bulk-verify 20/20; isDraft unchanged.
- **Learn list:** after the 13:49 staging publish, Form, LP and Automation still showed "No items found", so section_blog-related is hidden on those 3 templates (rollback: visibility true). Survey and Quiz shows 3 articles. MONDAY backlog item added.

## Changed FAQ questions (question text only)

| Page | Item | Old | New |
|---|---|---|---|
| job-application-form | Q4 | Can I download a job application form PDF? | What is the difference between an application form and a resume? |
| sales-automation | Q4 | Is Salesforce automation the same as sales force automation? | What is the difference between sales automation and marketing automation? |
| document-automation | Q8 | Can document automation work with PDFs? | What features should document automation tools have? |
| task-automation | Q9 | Can task automation work with PDFs? | How can I automate my daily tasks? |
| t-shirt-order-form | Q3 | Is there a T-shirt order form template for Word? | How do I add names and numbers to a shirt order form template? |
| t-shirt-order-form | Q4 | How to make a shirt order form on Google Forms? | How do I use a T-shirt order form for a fundraiser? |
| t-shirt-order-form | Q5 | Where can I find a printable T-shirt order form? | How do I count sizes from T-shirt order forms? |
| t-shirt-order-form | Q9 | Can you fill in a T-shirt order form PDF? | Should a shirt order form include spare shirts for size swaps? |
| interest-form | Q5 | Can I get an interest form as a PDF? | What to put in an interest form? |
| feedback-form | Q10 | Is there a feedback form template in Word or PDF? | What is a constructive feedback form? |
| massage-intake-form | Q4 | Can I get a massage intake form PDF? | Why do massage therapists use intake forms? |
| massage-intake-form | Q6 | Where can I find free printable massage intake forms? | When should clients fill out a massage intake form? |
| massage-intake-form | Q8 | Can I make a massage intake form in Word? | What does a therapist do with a massage client intake form? |
| employee-information-form | Q6 | Where can I get an employee information form PDF? | How do I customize an employee information form template for my company? |
| employee-information-form | Q8 | Can I make an employee information form in Word? | Who should have access to an employee information form? (last resort: built on the primary keyword) |
| employee-information-form | Q10 | Is there a printable employee information form? | How often should an employee information form be updated? (last resort: built on the primary keyword) |
| client-onboarding-questionnaire | Q5 | Is there a client onboarding questionnaire template in Word? | What does a client onboarding questionnaire example look like? |
| client-onboarding-questionnaire | Q6 | Should I send a client onboarding questionnaire PDF? | How do I use a client onboarding questionnaire template? |
| sign-in-form | Q7 | Can I get a sign in form PDF? | Is a digital sign in sheet better than paper? |
| sign-in-form | Q8 | How do I make a sign in form in Word? | What app can I use for a sign in form? |
| booking-form | Q4 | How to make a booking form on Google? | What does a booking form look like? |
| booking-form | Q7 | Should I use a booking form PDF? | How does an online booking form work? |
| booking-form | Q8 | Can I make a booking form template in Word? | Where can I find a booking form template? |

## New hero descriptions (D1) and how-to descriptions (D2), with character counts

| Page | Hero description | How-to description |
|---|---|---|
| job-application-form | Create a job application form that takes resume uploads and saves every applicant to a database you own. (104) | Seven steps to turn what a role requires into a job application form that fills your applicant table. (101) |
| employee-engagement-survey | Build an employee engagement survey with confidential team results and manager dashboards that rank what to fix first. (118) | Seven steps to run an employee engagement survey that managers act on, with most of the time spent after it closes. (115) |
| sales-automation | Build sales automation that assigns new leads by territory and messages the owner in Slack when a deal stalls, beside your CRM. (127) | Seven steps to turn your routing and follow-up rules into sales automation, then roll it out one lead source at a time. (119) |
| document-automation | Build document automation that drafts quotes and letters from your data and reads incoming PDFs into named fields. (114) | Seven steps to decide what your document automation drafts and reads, then test it on a week of real requests. (110) |
| task-automation | Create task automation that files documents, sends reminders, and moves data between tools on a schedule or trigger. (116) | Seven steps to turn one repeated chore into task automation that runs on its own trigger and replaces the manual version. (121) |
| registration-form | Create a registration form that collects the fee with each sign-up and offers freed spots to the waitlist. (106) | Seven steps to plan a registration form around its caps and fee, then build it with Emergent and register as a test. (116) |
| t-shirt-order-form | Build a T-shirt order form that takes card payment and totals every size for your printer when orders close. (108) | Seven steps to agree on the shirt with your printer, then run a T-shirt order form that closes on time. (103) |
| webinar-landing-page | Create a webinar landing page that emails each registrant a personal join link and keeps every sign-up in a table you own. (122) | Seven steps to a webinar landing page that turns sign-ups into attendees and shows you who actually came. (105) |
| event-landing-page | Build an event landing page with a registration form and a guest list you own, then check guests in at the door. (112) | Seven steps to build an event landing page that shows guests where and when to come, then checks them in on event day. (118) |
| interest-form | Build an interest form that tallies demand for each option and alerts you when one reaches your go-ahead number. (112) | Seven steps to make an interest form that settles one decision with a clear go-ahead number, then build it with Emergent. (121) |
| 404-page | Build a 404 page that searches your own content and logs every missed URL in a database you own. (96) | Seven steps to a 404 page that points lost visitors to a useful page and returns the right status code. (103) |
| feedback-form | Create a feedback form people finish on a phone, with an alert to the right teammate whenever a rating comes in low. (116) | Seven steps to a short feedback form that goes out at the right moment and reaches someone who can act on it. (109) |
| ecommerce-automation | Create ecommerce automation that sends each paid order to its supplier and alerts your team when an order needs a person. (121) | Seven steps to start ecommerce automation with one store event and one rule, then run it beside your manual process. (116) |
| massage-intake-form | Build a massage intake form that asks a follow-up on any yes and saves every signed visit to a client database you own. (119) | Seven steps to plan a massage intake form around the answers that change a session, then build and test it in Emergent. (119) |
| employee-information-form | Build an employee information form that keeps one record per person and asks each employee to confirm it every year. (116) | Seven steps to plan an employee information form that gives payroll what it needs and stays current year after year. (116) |
| client-onboarding-questionnaire | Create a client onboarding questionnaire that shows each client only their sections and reminds them about anything still open. (127) | Seven steps to a client onboarding questionnaire that clients finish before the kickoff call. (93) |
| law-firm-landing-page | Create a law firm landing page for one practice area that asks the intake questions and sends each inquiry to the right attorney. (129) | Seven steps to plan a law firm landing page around one practice area and decide who calls each inquiry back. (108) |
| sign-in-form | Create a sign in form that records every arrival and departure, then messages staff when their guest is at the front desk. (122) | Seven steps to set up a sign in form at your entrance that keeps a complete record of everyone on site. (103) |
| pricing-page | Create a pricing page with a billing switch that does the yearly math and a record of which plan each visitor picks. (116) | Seven steps to a pricing page that shows each visitor which tier fits and what it will cost. (92) |
| booking-form | Build a booking form that hides taken slots, collects deposits, and sends each customer a link to reschedule or cancel. (119) | Seven steps to plan a booking form around your schedule and payment rule, then build it with Emergent. (102) |

## Decisions

- DECISIONS 2026-10-09: the launch-blocker rules.
- **Replacement sources:** approved secondaries, gate-passing AlsoAsked or DataForSEO questions, related searches and captured keyword ideas, per "approved secondaries or gate-passing questions".
- **Last resort:** two employee-information questions had no searched source left without a brand or file format, so they are built on the primary keyword. Each is marked LAST-RESORT in `faq_sources` (provenance_note).

## Files changed and commits

- e7ac7dd: rules (`qc/paa_gate.py` PA14/PA15, `qc/qc_hub.py` D1/D2, `rules/*`, HUB_RULES, rubric, severity, writer brief, LESSONS, DECISIONS, golden).
- 1f9ed78: writer fixes and the Learn hide.
- 0801c33: rework and before-values.
- This commit: fingerprints, checklist, logs, this report.

## Webflow calls

- **Learn hide:** 3 set_visibility false on section_blog-related (Form 24cd8ebc-23b4-d766-1f9f-0d648fc0665f, LP d8a90b8f-142b-5c77-eae7-a06e09b08934, AAB cadd555f-249f-2bfd-b8af-165dc634d9d9). Read back false. Rollback: true.
- **CMS:** 6 update_collection_items calls (20 items, changed fields only).
- **Reads:** get_site, plus full collection reads before and after.
- **No publish of any kind.**

## Not done

- Production still serves the 11:38 and 13:14 content. Fixing it needs a publish, which is your call.
- Part 2 staging verification waits for "staging published".
- The 183 other written specs that fail the new rules are not fixed. They follow in the next batch's combined pass.

## Open questions for Divit

- **Production:** push the fixes to production right after staging verification passes (recommended), or unpublish the 20 until then?
