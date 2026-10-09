# Live audit 2026-10-09

## Digest for Divit

Live audit 2026-10-09 on https://emergent.sh: 20 pages and 4 hubs checked; issues P0 1, P1 98, P2 53; fixed 79; rolled back 0; fix pending 0; proposals waiting for a go 0; drift 0; held pages live 0.

### P0: held pages live (unpublish at once) (0)


### Fixes (79)

- P1 /ai-automation-builder/ecommerce-automation `tab_image_4` A6-uk: UK spelling "grey" (use "gray") in alt text [fixed]
- P1 /ai-landing-page-builder/404-page `template` A6-entity: broken HTML entity shown as text in jsonld text [fixed]
- P1 /ai-form-builder/sign-in-form `why_table` B-HUBRULES5com: Google Forms build cell says it is built manually, field by field; Google has added Gemini form generation ('Help me create a form') to Forms, and the library fact (checked 2026-09-28) cites the old approved table, not vendor documentation, so it may now be a false competitor fact. [fixed]
- P1 /ai-form-builder/t-shirt-order-form `why_table` B-HUBRULES5com: Google Forms build cell says it is built manually, field by field; Google has added Gemini form generation ('Help me create a form') to Forms, and the library fact (checked 2026-09-28) cites the old approved table, not vendor documentation, so it may now be a false competitor fact. [fixed]
- P1 /ai-landing-page-builder/404-page `faq` B-HUBRULES2cop: FAQ 10 writes the acronym in lowercase in the link anchor, next to 'SEO' in the same sentence. [fixed]
- P1 /ai-landing-page-builder/404-page `howto_step_3_des` B-HUBRULES5how: Step 3 is 23 words, below the 35-50 word range, and never mentions the search its title promises. [fixed]
- P1 /ai-landing-page-builder/404-page `feature_1` B-HUBRULES6cla: States that an Emergent-hosted site answers unknown URLs with a real 404 status; that hosting capability is not in rules/claims.json or rules/capabilities.json and has been pending with Divit since review. [fixed]
- P1 /ai-landing-page-builder/404-page `why_table` B-HUBRULES5com: The Emergent build cell falls back to the LP hub default and calls a 404 page a campaign page; no LP variant fits, so the library needs a new cell. [fixed]
- P1 /ai-landing-page-builder/event-landing-page `howto_step_2_des` B-HUBRULES2gra: The example subhead is set in running text without quotes, so the sentence does not parse. [fixed]
- P1 /ai-landing-page-builder/event-landing-page `faq` B-HUBRULES6cla: FAQ 4 extends the approved free-tier claim (building and publishing a page) to include the guest list and confirmation emails. [fixed]
- P1 /ai-form-builder/booking-form `faq#4` B-HUBRULES8: The answer contradicts itself: it opens by saying the form fits on one phone screen, then walks through several screens ending with 'the last screen'. [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `explore_cta` B-HUBRULES5: At 390 px the 40-character comparison CTA overflows its pill: the leading 'B' is clipped and the arrow touches the edge (the 34-character employee-information-form CTA just fits). [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `faq#8` B-HUBRULES2b: A missing comma creates a garden-path sentence that reads as 'taking them on call'. [fixed]
- P0 /ai-automation-builder/document-automation `faq#4` B-HUBRULES8SEV: Calling Gavel "often" the best tool for law firms is an unsourced market claim about a named company; domain_sources only says what Gavel does. [fixed]
- P1 /ai-automation-builder/document-automation `faq#10` B-DECISIONS202: The document-approval-workflow link was stripped because that page is not live, so the sentence now points readers to a guide that does not exist. [fixed]
- P1 /ai-automation-builder/document-automation `tab_content_3` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/ecommerce-automation `faq#8` B-DECISIONS202: The shipping-automation link was stripped because that page is not live, so "covered under shipping automation" points to a page that does not exist. [fixed]
- P1 /ai-automation-builder/ecommerce-automation `feature_1` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/ecommerce-automation `howto_step_3_des` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/ecommerce-automation `faq#6` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/ecommerce-automation `tab_image_4 alt` B-DECISIONS202: A list in the alt text has no serial comma (fold this into the pending gray alt fix). [fixed]
- P1 /ai-automation-builder/sales-automation `faq#3` B-DECISIONS202: The crm-automation link was stripped because that page is not live, so "see CRM automation" sends readers to nothing. [fixed]
- P1 /ai-automation-builder/sales-automation `h1` B-DECISIONS202: The H1 list has no serial comma (the primary keyword is unchanged by the fix). [fixed]
- P1 /ai-automation-builder/sales-automation `share_image alt` B-DECISIONS202: A list in the alt text has no serial comma. [fixed]
- P1 /ai-automation-builder/sales-automation `feature_1` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/sales-automation `feature_6` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/task-automation `features_subheading` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/task-automation `feature_3` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/task-automation `feature_5` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/task-automation `howto_step_2_des` B-DECISIONS202: A three-item list has no serial comma. [fixed]
- P1 /ai-automation-builder/task-automation `tab_image_1 alt` B-DECISIONS202: A three-item list in the alt text has no serial comma. [fixed]
- P1 /ai-form-builder/job-application-form `faq` B-HUBRULES2a: FAQ 7 says 'the blank PDF', but the live page never introduces a blank PDF (step 6 handles walk-ins with a QR code and typed-in paper copies), so the reference points to nothing. [fixed]
- P1 /ai-form-builder/job-application-form `feature_4` B-HUBRULES2a: 'In the same layout' has no referent in the feature or anywhere above it, so the sentence does not say what the PDF matches. [fixed]
- P1 /ai-form-builder/massage-intake-form `feature_1` B-HUBRULES2aUS: The heading and body use British 'tick' and 'ticked', and the body's next sentence switches to the US 'checks'. [fixed]
- P1 /ai-form-builder/massage-intake-form `howto_step_7_des` B-HUBRULES2aUS: The step uses British 'ticks every box' and drops the particle in 'fill it once', which is not idiomatic US English. [fixed]
- P1 /ai-form-builder/massage-intake-form `faq` B-HUBRULES2a: FAQ 2 says 'fill it on a phone' without the particle, which is not idiomatic US English. [fixed]
- P1 /ai-form-builder/registration-form `feature_6` B-HUBRULES6rul: The custom-domain claim uses the banned 'built in' wording without the hyphen, which slips past the H/claims regex. [fixed]
- P1 /ai-form-builder/registration-form `faq` B-HUBRULES5FAQ: The creator-application link was held back because that page is not live (404), and without the link FAQ 8's last sentence points the reader to a build that cannot be seen. [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `faq` B-HUBRULES2aco: FAQ 7 renders the pending-link anchor as plain text with the acronym in lowercase, right after 'PPC landing pages' in the same answer. [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `meta_description` B-DECISIONS202: Three-item list without the serial comma. [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `feature_4` B-DECISIONS202: Three-item list without the serial comma (body 177 -> 178 chars, within limits). [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `howto_step_5_des` B-DECISIONS202: Three-item list without the serial comma. [fixed]
- P1 /ai-landing-page-builder/pricing-page `feature_5` B-GrammarHUBRU: The example message is run into the sentence with no quotation marks, so it reads as a broken clause. [fixed]
- P1 /ai-landing-page-builder/pricing-page `feature_1` B-DECISIONS202: Two three-item lists in one body without the serial comma (body 170 -> 172 chars, within limits). [fixed]
- P1 /ai-landing-page-builder/pricing-page `tab_content_4` B-DECISIONS202: Three-item price list without the serial comma. [fixed]
- P1 /ai-landing-page-builder/pricing-page `howto_step_5_des` B-DECISIONS202: Three-item list without the serial comma. [fixed]
- P1 /ai-landing-page-builder/pricing-page `faq` B-DECISIONS202: FAQ 5 lists three pricing bases without the serial comma. [fixed]
- P1 /ai-landing-page-builder/webinar-landing-page `meta_description` B-DECISIONS202: Three-verb list without the serial comma. [fixed]
- P1 /ai-landing-page-builder/webinar-landing-page `feature_4` B-DECISIONS202: Four-item list without the serial comma (body 172 -> 173 chars, within limits). [fixed]
- P1 /ai-landing-page-builder/webinar-landing-page `howto_step_2_des` B-DECISIONS202: Three-item list without the serial comma. [fixed]
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `meta_description` B-DECISIONS202: Four-item list without the serial comma. [fixed]
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `feature_1` B-DECISIONS202: The first list drops the serial comma while the next sentence uses it (body 180 -> 181 chars, spread 12). [fixed]
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `feature_5` B-DECISIONS202: Four-item list without the serial comma. [fixed]
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `howto_step_7_des` B-DECISIONS202: Three-verb list without the serial comma. [fixed]
- P1 /ai-form-builder/booking-form `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-form-builder/employee-information-form `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-form-builder/feedback-form `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-form-builder/interest-form `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-form-builder/job-application-form `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-form-builder/massage-intake-form `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-form-builder/registration-form `why_table` LIB-gforms-build: Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table [fixed]
- P1 /ai-automation-builder/document-automation `mockup` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-automation-builder/ecommerce-automation `mockup` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-automation-builder/sales-automation `meta_description` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/booking-form `faq, howto_step_5_des` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `mockup, howto_step_2_des, faq` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/employee-information-form `mockup, howto_step_2_des, faq` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/feedback-form `mockup, faq` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/interest-form `mockup, howto_step_5_des` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/job-application-form `feature_1, tab_image_3 alt` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/massage-intake-form `faq, howto_step_5_des` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/sign-in-form `tab_content_1` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-form-builder/t-shirt-order-form `tab_content_2` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-landing-page-builder/404-page `features_subheading, tab_content_4, mockup` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-landing-page-builder/event-landing-page `mockup, faq` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `tab_image_2 alt, tab_image_3 alt` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `mockup, tab_image_1 alt` H3-sweep: serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix [fixed]
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `explore_cta` D3: explore CTA 35 chars (max 34, QC D3): 'Build My Engagement Survey' [fixed]

### Proposals waiting for a go (0)


### Drift (edited in Webflow, reported, not overwritten) (0)


### Needs a CMS read to classify (drift check) (0)


### Backlog (P2) (53)

- P2 /ai-automation-builder/document-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/ecommerce-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/sales-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/task-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/booking-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/client-onboarding-questionnaire `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/employee-information-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/feedback-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/interest-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/job-application-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/massage-intake-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/registration-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/sign-in-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/t-shirt-order-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/404-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/event-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/law-firm-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/pricing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/webinar-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-survey-and-quiz-builder/employee-engagement-survey `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-form-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-landing-page-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-survey-and-quiz-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-form-builder/sign-in-form `h1, breadcrumb, faq, feature_6, prompt_chip_1` B-HUBRULES2aCo: The page writes the open compound 'sign in form' (keyword form) beside the hyphenated 'sign-in' (chip 'Visitor Sign-In', 'sign-in app', 'sign-in button').
- P2 /ai-landing-page-builder/404-page `faq` B-HUBRULES5FAQ: FAQ 4 reads 'access a 404 page' as getting past one while FAQ 6 answers the viewing reading, so the two items overlap.
- P2 /ai-landing-page-builder/event-landing-page `tab_content_1` B-HUBRULES2aPr: 72 stands for two different quantities in one sentence (hours and special meals).
- P2 /ai-form-builder/booking-form `faq#5` B-HUBRULES5: The question compares reservation and booking forms, but the answer contrasts reservation with 'appointment form', so the reader never learns where 'booking form' sits.
- P2 /ai-form-builder/booking-form `faq#3` B-HUBRULES5: The question keeps the searcher's ungrammatical 'How to ...?' form; HUB_RULES 5 allows a light grammar edit.
- P2 /ai-form-builder/booking-form `template` B-HUBRULES5: The FAQ heading renders as the template's fixed 'Your Questions, Answered', not the spec heading '{Topic} Questions, Answered'; it is the same on all 20 live pages.
- P2 /ai-form-builder/client-onboarding-questionnaire `features_heading` B-HUBRULES2a: The section promises what happens after submit, but two of its six features (service sections, the access checklist) work while the client is filling it in.
- P2 /ai-form-builder/employee-information-form `howto_step_6_des` B-CONTENTDEFEC: Step 6 advises a quiet month away from year-end payroll, while the page's own Annual Check tab runs the check in January, in W-2 season.
- P2 /ai-form-builder/employee-information-form `tab_content_2` B-CONTENTDEFEC: Generalization stated as fact: not every marriage changes a surname.
- P2 /ai-form-builder/employee-information-form `faq#4` B-HUBRULES5: The question keeps the searcher's ungrammatical 'How to ...?' form; HUB_RULES 5 allows a light grammar edit.
- P2 /ai-automation-builder/document-automation `mockup` B-DECISIONS202: Two lists in the visible tab prompts have no serial comma (engagementLetters, offerLetters). (mockup prompts are not rendered since the hero redesign; fix at next rework)
- P2 /ai-automation-builder/document-automation `faq item 3` B-CONTENTDEFEC: "The most common use" is an unsourced ranking.
- P2 /ai-automation-builder/document-automation `faq item 1` B-HUBRULES8: The source says "also known as"; "older name" goes beyond it (noted at review, still open).
- P2 /ai-automation-builder/ecommerce-automation `mockup` B-DECISIONS202: Two lists in the marginReport prompt have no serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- P2 /ai-automation-builder/ecommerce-automation `tab_content_3` B-HUBRULES2apr: The H3 says "the $500 order", but the rule holds orders over $500 and the image shows $742.00.
- P2 /ai-automation-builder/sales-automation `mockup` B-DECISIONS202: A list of actions in the inboundLeads prompt has no serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- P2 /ai-automation-builder/task-automation `mockup` B-DECISIONS202: A list of actions in the clientDocumentFiling prompt has no serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- P2 /ai-form-builder/interest-form `faq` B-CONTENTDEFEC: FAQ 4 says every form builder and template site offers a free interest form template, then hedges with 'usually' and 'Most': a sweeping claim about unnamed third parties.
- P2 /ai-form-builder/interest-form `howto_step_7_title` B-HUBRULES2a: 'Fill it in' is the British idiom; the rest of the hub says fill out.
- P2 /ai-form-builder/job-application-form `meta_description` B-HUBRULES5: The meta promises a printable blank PDF for walk-ins, but the body's walk-in step uses a QR code and staff typing in paper copies and never shows a blank PDF.
- P2 /ai-form-builder/massage-intake-form `features_subheading` B-HUBRULES2a: 'Your therapist' speaks to a spa owner, but the meta title targets therapists and tab 1 is a solo practice, so the reader is often the therapist.
- P2 /ai-landing-page-builder/law-firm-landing-page `mockup` B-DECISIONS202: Visible tab prompt (injuryCaseReview) lists three asks without the serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- P2 /ai-landing-page-builder/law-firm-landing-page `faq` B-HUBRULES2a: FAQ 3 comparison is loosely attached: 'Like any lead generation landing page' modifies 'the form', not the page.
- P2 /ai-landing-page-builder/pricing-page `mockup` B-DECISIONS202: Three visible tab prompts drop the serial comma (perSeatSaasTiers, agencyPackages, classMemberships). (mockup prompts are not rendered since the hero redesign; fix at next rework)
- P2 /ai-landing-page-builder/pricing-page `faq` B-HUBRULES5lig: FAQ 2 question is a searcher fragment rather than a question.
- P2 /ai-landing-page-builder/webinar-landing-page `tab_image_4` B-CONTENTDEFEC: The Slack card header draws a channel hash before Lena Okafor while the copy and the card below say direct message.
- P2 /ai-survey-and-quiz-builder/employee-engagement-survey `mockup` B-DECISIONS202: Visible tab prompts drop the serial comma in four lists (annualCensus x3, frontlineStaff x1). (mockup prompts are not rendered since the hero redesign; fix at next rework)
- P2 /ai-survey-and-quiz-builder/employee-engagement-survey `why_description` B-CONTENTDEFEC: Category-wide claim that the table beside it qualifies: SurveyMonkey is shown with per-user pricing, not per employee.
- P2 /ai-survey-and-quiz-builder/employee-engagement-survey `tab_image_1` B-CONTENTDEFEC: Sales eNPS +9 with 84 answers is reachable only by truncating (8/84 = 9.5), not by rounding.

## Request

Scheduled or requested live audit per docs/LIVE_AUDIT.md (DECISIONS 2026-10-09).

## Actions and results

- Layer A on 20 pages and 4 hubs at https://emergent.sh; Layer B batches: 5; recorded: 5.
- Findings: `audits/live/2026-10-09/findings.json`; per-page files `audits/live/2026-10-09/<slug>.md`; ledger `audits/live/LEDGER.md`.

## Webflow calls

- see the ledger rows for this date (update and item publish per fix, read back)

## Not done

- Proposals and drift wait for Divit.

## Open questions for Divit

- Each proposal above has a recommended fix in its per-page file.
