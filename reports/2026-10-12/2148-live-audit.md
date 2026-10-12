# Live audit 2026-10-12

## Digest for Divit

Live audit 2026-10-12 on https://emergent.sh: 40 pages and 4 hubs checked; issues P0 1, P1 192, P2 174; fixed 74; rolled back 0; fix pending 0; proposals waiting for a go 119; drift 0; held pages live 0.

### P0: held pages live (unpublish at once) (0)


### Fixes (74)

- P1 /ai-form-builder/direct-deposit-form `tab_content_3` B-HUBRULES8CON: Unsourced generalization about payroll fraud stated as fact, and contestable (insider payroll schemes are common); the IC3 source covers redirected deposits only. [fixed]
- P1 /ai-form-builder/employee-information-form `tab_content_1` B-QCA1stocknam: Stock placeholder company name 'Northwind' (QC A1 now blocks it). [fixed]
- P1 /ai-form-builder/employee-information-form `tab_content_2` B-QCA1stocknam: Stock placeholder company name 'Northwind' in the second tab. [fixed]
- P1 /ai-form-builder/employee-information-form `tab_content_2` B-QCA1reusedpe: Reused persona names: 'Lena Park' appears in 6 other specs and 'Lena Ortiz' in 13; also in the tab 2 alt, the image brief and the cover (with payroll lead Grace Holt, also on employee-referral-form). [fixed]
- P1 /ai-form-builder/feedback-form `tab_content_1` B-QCA1reusedpe: Support lead 'Dana Ruiz' is a reused persona (14 other specs); also in the tab 1 alt, cover alt, image brief and mockup ('Dana'). [fixed]
- P1 /ai-automation-builder/ecommerce-automation `feature_5` B-HUBRULES6cla: The approved claim is 'no task cap'. 'Never pauses a workflow halfway' promises reliability beyond that claim; store API rate limits are outside Emergent's control. [fixed]
- P1 /ai-form-builder/liability-waiver-form `howto_step_7_des` B-HUBRULES8aso: The legal source (Rocket Lawyer) says a waiver can fail when its language is vague; the copy turns that into a frequency claim ('a common reason') that the source does not make. [fixed]
- P1 /ai-form-builder/massage-intake-form `features_subheading` B-HUBRULES2agr: 'Each one' has no antecedent under the H2, and 'your therapist' addresses a spa owner, while the page speaks to therapists themselves (solo practitioners included). [fixed]
- P1 /ai-form-builder/t-shirt-order-form `tab_content_4` B-HUBRULES2bQC: Stock placeholder company name Northwind in the New Hire Kits tab copy. [fixed]
- P1 /ai-landing-page-builder/404-page `tab_content_1` B-HUBRULES2bQC: Stock placeholder name Northwind in the Online Store tab copy (visible on load). [fixed]
- P1 /ai-landing-page-builder/404-page `tab_content_2` B-HUBRULES2bQC: Stock placeholder name Acme in the Developer Docs tab copy. [fixed]
- P1 /ai-landing-page-builder/404-page `tab_content_4` B-HUBRULES2bQC: Stock placeholder name Globex in the Site Migration tab copy. [fixed]
- P0 /ai-landing-page-builder/event-landing-page `why_table` B-HUBRULES5tab: The grouped column 'Landingi / Leadpages / Instapage' says 'Tiered by traffic on most plans', but the library's own Leadpages row (shown on ebook-landing-page) says 'No traffic caps', so the cell is false for Leadpages; one column for three vendors also states nothing exact. [fixed]
- P1 /ai-landing-page-builder/event-landing-page `tab_content_4` B-HUBRULES2bre: Dana Whitfield, the Austin rep, appears in 14 other specs. [fixed]
- P1 /ai-survey-and-quiz-builder/church-survey `feature_1` B-HUBRULES8tru: The example contradicts the rule it illustrates: a minimum of 5 does not hide a class of six, which is reported once all six answer. [fixed]
- P1 /ai-survey-and-quiz-builder/church-survey `why_title` B-HUBRULES6cla: The heading states that churches already run surveys on Emergent, a customer-adoption claim with no entry in rules/claims.json; it is also the only SQB page off the L6 profile. [fixed]
- P1 /ai-survey-and-quiz-builder/customer-feedback-survey `meta_description` B-DECISIONSser: A three-item list is missing its serial comma. [fixed]
- P1 /ai-survey-and-quiz-builder/customer-feedback-survey `tab_content_1` B-DECISIONSser: A three-item list is missing its serial comma. [fixed]
- P1 /ai-survey-and-quiz-builder/customer-feedback-survey `tab_content_3` B-DECISIONSser: A three-item list is missing its serial comma (the same sentence repeats in the serviceVisit mockup). [fixed]
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `feature_1` B-DECISIONSser: A three-item list is missing its serial comma. [fixed]
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `feature_6` B-DECISIONSser: A three-item list is missing its serial comma, although the sentence before it uses one. [fixed]
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `howto_step_4_des` B-DECISIONSser: A three-item list is missing its serial comma. [fixed]
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `tab_content_2` B-DECISIONSser: A three-item list is missing its serial comma (the nursingUnits mockup repeats it). [fixed]
- P1 /ai-landing-page-builder/webinar-landing-page `tab_content_4` B-QCA1Divit202: Tab 4 names the panel host "Northwind People" in copy, alt text and image; Northwind also appears on eight other live pages. [fixed]
- P1 /ai-landing-page-builder/webinar-landing-page `tab_content_1` B-QCA1Divit202: Kestrel Payroll reuses "Kestrel", a company name already used on six live pages (procurement, task and sales automation, booking, registration and massage intake forms). [fixed]
- P1 /ai-landing-page-builder/webinar-landing-page `tab_content_2` B-QCA1Divit202: Fieldnote is also the company in tab 4 of the live mobile landing page, a sibling in the same hub. [fixed]
- P1 /ai-landing-page-builder/webinar-landing-page `why_table` B-CONTENTDEFEC: The Wix column says submissions go to a "basic contact form to email", but Wix Forms also stores submissions in the site dashboard and contact list, so the cell understates Wix; the library fact cites only an approved table and a pricing page. [fixed]
- P1 /ai-survey-and-quiz-builder/brand-awareness-survey `tab_content_2` B-QCA1Divit202: Fernway, the insurer whose recall is tracked, is also the company in tab 1 of the live pricing page. [fixed]
- P1 /ai-survey-and-quiz-builder/brand-awareness-survey `tab_content_4` B-QCA1Divit202: Copperline Movers reuses "Copperline", the company in tab 3 of the live event landing page. [fixed]
- P1 /ai-survey-and-quiz-builder/brand-perception-survey `tab_content_3` B-QCA1Divit202: Ledgerline, the payroll app in tab 3, is also the company in tab 1 of the live ebook landing page. [fixed]
- P1 /ai-automation-builder/invoice-automation `tab_image_3` B-QCA1stocknam: Tab 3 image and image_brief draw 'Pinecrest Dental'; Pinecrest is the placeholder company in 12 other specs, a de facto stock name. [fixed]
- P1 /ai-automation-builder/sales-automation `tab_image_3` B-QCA1stocknam: Tab 3 image (image_brief rows) draws three stock names in the open-deals table. [fixed]
- P1 /ai-automation-builder/sales-automation `tab_image_2` B-QCA1stocknam: Tab 2 image and its alt text name the post-demo account Initech. [fixed]
- P1 /ai-automation-builder/sales-automation `tab_image_4` B-QCA1stocknam: Tab 4 image lists Acme Corp among the renewal accounts. [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `why_table` B-HUBRULES5com: The Wix "Where submissions go" cell understates Wix: Wix Forms keeps submissions in the site dashboard with export, not only an email. The library fact (lp.json Wix.data, 2026-09-28) cites only "vendor pricing page". [fixed]
- P1 /ai-landing-page-builder/mobile-landing-page `why_table` B-HUBRULES5com: The Wix "Where submissions go" cell understates Wix: Wix Forms keeps submissions in the site dashboard with export, not only an email. The library fact (lp.json Wix.data, 2026-09-28) cites only "vendor pricing page". [fixed]
- P1 /ai-landing-page-builder/pricing-page `why_table` B-HUBRULES5com: The Wix "Where submissions go" cell understates Wix: Wix Forms keeps submissions in the site dashboard with export, not only an email. The library fact (lp.json Wix.data, 2026-09-28) cites only "vendor pricing page". [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `tab_content_1` B-QCA1reusedpe: "Marlow" is reused as a company name in 10 other specs (sales-automation, interest-form, quote-form, product-landing-page and more). [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `tab_content_3` B-QCA1reusedpe: "Juniper" is reused as a company name in 19 other specs (one-page-website, squeeze-page, massage-intake-form and more). [fixed]
- P1 /ai-landing-page-builder/law-firm-landing-page `tab_content_2` B-QCA1reusedpe: "Bellweather" also appears in equipment-rental-agreement-form. [fixed]
- P1 /ai-landing-page-builder/mobile-landing-page `tab_content_2` B-QCA1reusedpe: "Brightway" is reused from consultation-form. [fixed]
- P1 /ai-landing-page-builder/mobile-landing-page `tab_content_4` B-QCA1reusedpe: "Fieldnote" is reused in 4 other specs (affiliate-, b2b- and webinar-landing-page, file-upload-form), three of them in this hub. [fixed]
- P1 /ai-landing-page-builder/pricing-page `tab_content_1` B-QCA1reusedpe: "Fernway" is reused in 9 other specs (saas-, b2b-, lead-generation-landing-page, coming-soon-page and more). [fixed]
- P1 /ai-landing-page-builder/pricing-page `tab_content_3` B-QCA1reusedpe: "Halden" is reused in 8 other specs (ppc-landing-page, product-landing-page, coming-soon-page and more). [fixed]
- P1 /ai-landing-page-builder/pricing-page `tab_content_4` B-QCA1reusedpe: "Ridgeline" is reused in 9 other specs (event-, ppc- and product-landing-page, quote-form and more). [fixed]
- P1 /ai-form-builder/order-form `howto_step_2_des` B-HUBRULES2agr: A comma splits the either/or pair: "either a delivery address, or a pickup time". [fixed]
- P1 /ai-form-builder/order-form `tab_image_3` B-QCA1Divit202: The buyer company in the tab 3 image, Brightline Logistics, is reused across 16 specs and is already live on data-entry-automation and booking-form. [fixed]
- P1 /ai-form-builder/registration-form `tab_image_3` B-QCA1Divit202: The tab 3 vendor table draws four stock company names, and the hero card and alt text name one of them. [fixed]
- P1 /ai-form-builder/registration-form `tab_content_2` B-QCA1Divit202: The product name Kestrel is reused across 15 specs and is already live on 5 other pages; it appears in the tab copy, the mockup prompt and the tab 2 image and alt. [fixed]
- P1 /ai-form-builder/registration-form `tab_image_4` B-QCA1Divit202: The gardener "D. Okafor" reuses a surname found in 38 specs and on 8 other live pages. [fixed]
- P1 /ai-form-builder/rental-agreement-form `feature_2` B-HUBRULES2awr: The feature names three follow-up questions (breed, weight, plate number) and then says "those two questions". [fixed]
- P1 /ai-form-builder/rental-agreement-form `howto_step_1_des` B-QCHUSspellin: "tap" is the British word for the fixture; the page is US English (faucet). Flagged in review notes twice and still live. [fixed]
- P1 /ai-form-builder/sign-in-form `tab_content_1` B-QCA1Divit202: The visitor's company is the stock name Northwind Freight, in the tab copy, the tab 1 image and its alt text (Northwind appears on 10 live pages). [fixed]
- P1 /ai-form-builder/sign-in-form `tab_content_1` B-QCA1Divit202: The visitor Lena Ortiz is a persona reused in 14 specs and live on task-automation and employee-information-form; also in the tab 1 image and alt. [fixed]
- P1 /ai-form-builder/sign-in-form `tab_content_3` B-QCA1Divit202: The listing agent Dana Whitfield is reused in 14 specs and live on ecommerce-automation, booking-form and event-landing-page; "18 Alder Lane" is also live on feedback-form. [fixed]
- P1 /ai-form-builder/sign-in-form `tab_image_4` B-QCA1Divit202: The volunteer table reuses personas from other live pages: Ana Ruiz (25 specs, 3 other live pages), Jordan Lee (11 specs, live on job-application-form and t-shirt-order-form), Leo Grant (8 specs). [fixed]
- P1 /ai-form-builder/sign-in-form `feature_1` B-HUBRULES2awr: The form described asks for name, company and host only, then says returning visitors prefill from their email address, a field it never asks for. [fixed]
- P1 /ai-automation-builder/task-automation `tab_content_4` B-QCA1stocknam: Stock placeholder company name Globex in the Month-End Close tab copy (hidden tab, live in the DOM). [fixed]
- P1 /ai-automation-builder/task-automation `tab_image_4` B-QCA1stocknam: Globex in the tab 4 alt text; the same string is in image_brief tab 4 and embedded in uc-4.svg, so the image must be re-rendered with the new name. [fixed]
- P1 /ai-automation-builder/task-automation `tab_content_4` B-QCA1AItellsr: Persona Dana Kerr is reused (liability-waiver-form), and 'Dana' is also the contact on booking-form (Dana Whitfield) and client-onboarding-questionnaire (Dana Whitlock). [fixed]
- P1 /ai-automation-builder/task-automation `tab_content_2` B-QCA1AItellsr: Company prefix Kestrel is reused on 15 other specs (procurement-automation, sales-automation, daycare-registration-form, ...). [fixed]
- P1 /ai-automation-builder/task-automation `tab_image_2` B-QCA1AItellsr: Alt reuses Ana Brooks (7 other specs), Lena Ortiz (13 other specs) and Kestrel (15); both people are also drawn in uc-2.svg and the cover. [fixed]
- P1 /ai-automation-builder/task-automation `cover_image` B-QCA1AItellsr: Cover alt and cover art reuse Lena Ortiz (13 other specs) and Ana Brooks (7 other specs). [fixed]
- P1 /ai-automation-builder/task-automation `tab_image_3` B-QCA1AItellsr: Alt reuses Theo Grant (4 other specs); uc-3.svg also draws Mia Chen (3 other specs) and Rafael Ortiz, a second Ortiz on this page. [fixed]
- P1 /ai-automation-builder/task-automation `tab_content_1` B-QCA1AItellsr: Persona Owen Pratt is reused (parent-consent-form); also drawn in uc-1.svg and named in tab_image_1 alt. [fixed]
- P1 /ai-form-builder/booking-form `tab_content_2` B-QCA1AItellsr: Brightline is reused on 15 other specs and is also a real US rail brand (earlier review note). [fixed]
- P1 /ai-form-builder/booking-form `tab_image_2` B-QCA1AItellsr: Brightline in the tab 2 alt; the image_brief heading 'Brightline windows' draws it in uc-2.svg too. [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `tab_content_2` B-QCA1AItellsr: Larkspur is reused on 12 other specs (social-media-automation, contact-form, checkout-form, ...). [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `tab_image_2` B-QCA1AItellsr: Larkspur Ceramics in the tab 2 alt; also drawn three times in uc-2.svg (image_brief tab 2). Re-render after renaming. [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `tab_content_1` B-QCA1AItellsr: Reused names: Fernbrook (2 other specs), Harbor Coffee (404-page; booking-form has Harbor Street Commons), Dana Whitlock (employee-feedback-form; third 'Dana' contact in this batch). [fixed]
- P1 /ai-form-builder/client-onboarding-questionnaire `tab_image_1` B-QCA1AItellsr: Same reused names in the tab 1 alt; Fernbrook Social, Harbor Coffee Roasters and Dana Whitlock are also drawn in uc-1.svg. Re-render after renaming. [fixed]
- P1 /ai-form-builder/credit-card-authorization-form `faq#7` B-HUBRULES5FAQ: The question asks how long to keep the form; the answer gives no period ('hold on to it after the final charge'). A period tied to card-network dispute windows needs a domain source first, so the wording is Divit's call. [fixed]
- P1 /ai-automation-builder/document-automation `image_brief` A1: stock company names live (QC A1, Divit 2026-10-12 ruling) [fixed]
- P1 /ai-form-builder/job-application-form `image_brief` A1: stock company names live (QC A1, Divit 2026-10-12 ruling) [fixed]

### Proposals waiting for a go (119)

- P1 /ai-landing-page-builder/landing-page-seo `template` A9-console: 1 console error(s) in Chromium: SyntaxError: Illegal return statement
- P1 /ai-form-builder/employee-information-form `images.tab_image_1.alt` B-QCA1stocknam: Stock placeholder company name in the tab 1 image alt (same string in image_brief.tabs[0].alt).
- P1 /ai-form-builder/employee-information-form `image_brief tab 3` B-QCA1reusedpe: The drawn table reuses persona names from other pages: Ana Ruiz (25 other specs), Priya Nair (22), Tom Becker (13), Mei Chen (2).
- P1 /ai-form-builder/employee-information-form `image_brief tab 4` B-QCA1reusedpe: The drawn directory reuses persona names: Rosa Diaz (6 other specs), Ben Okafor (2), Luis Romero (1).
- P1 /ai-form-builder/feedback-form `images.tab_image_4.alt` B-QCA1reusedpe: Practice manager 'Leah Park' is reused (new-employee-form, address-verification-form) and near-identical to 'Lena Park' used on 6 other pages.
- P1 /ai-automation-builder/accounts-payable-automation `image_brief.tabs[2] rows; image_brief.tabs[3].hero (uc-3.svg, uc-4.svg)` B-QCA1reusedpe: The approver initials in two tab images are reused personas: 'M. Chen' appears on 4 other pages and 'M. Rossi' on 2 others (customer-satisfaction is live).
- P1 /ai-automation-builder/accounts-payable-automation `template` B-QCA1stocknam: The sitewide 'More things you can build' AI CRM Builder card draws 'Acme Corp', a stock name now on Divit's AI-tell list. It shows on every child page in this batch. It is a template component outside the child collections.
- P1 /ai-automation-builder/data-entry-automation `faq (item 7)` B-HUBRULES6CON: This states built-in platform behaviour that is not in the claims ledger. Saving corrections is something the app does when it is built that way; Emergent does not do it on its own.
- P1 /ai-automation-builder/data-entry-automation `image_brief.tabs[3].mini (uc-4.svg)` B-CONTENTDEFEC: The mini card is a green 'ok' status that says the record was written to three systems. The copy and the same image say the QuickBooks customer is held on its tax ID, so only two systems were written.
- P1 /ai-automation-builder/data-entry-automation `tab_content_3; image_brief.tabs[2]` B-QCA1reusedpe: 'Brightline' is a reused sample company: the name appears on 15 other specs in the plan (checkout-form, booking-form, nda-form, b2b-landing-page and others).
- P1 /ai-automation-builder/data-entry-automation `tab_content_2; image_brief.tabs[1]` B-QCA1reusedpe: 'Halden' is a reused sample company: it appears on 8 other specs (shipping-address-form, nda-form, pricing-page, ppc-landing-page and others).
- P1 /ai-automation-builder/document-automation `tab_content_2; images.tab_image_2.alt; image_brief.tabs[1]` B-QCA1stocknam: The quote tab is built around 'Acme', a stock placeholder company. It sits in the live tab copy, the alt text and the drawn image ('Q-2291 for Acme').
- P1 /ai-automation-builder/document-automation `tab_content_3; image_brief.tabs[2].main.blocks[1].rows[4][1]` B-QCA1stocknam: The certificate tab names 'Northwind Properties', a stock placeholder company, in the tab copy and the drawn table.
- P1 /ai-automation-builder/document-automation `tab_content_1; image_brief.tabs[0]; images.tab_image_1.alt` B-QCA1reusedpe: 'Ana Ruiz' is the most reused persona in the plan (24 other specs). Here it is the attorney in the tab copy, the alt text and the image.
- P1 /ai-automation-builder/document-automation `tab_content_4; image_brief.tabs[3]; images.tab_image_4.alt` B-QCA1reusedpe: The offer-letter tab reuses two personas: 'Sam Okafor' (7 other specs, including purchase-order-automation) and 'Mei Chen' (2 other specs). 'Lumen Studio' also appears on independent-contractor-agreement.
- P1 /ai-automation-builder/document-automation `tab_content_2; image_brief.tabs[1]; images.tab_image_2.alt` B-QCA1reusedpe: 'Dev Patel', the sales director in the quote tab, is a reused persona (4 other specs).
- P1 /ai-automation-builder/document-automation `tab_content_3; image_brief.tabs[2]; images.tab_image_3.alt` B-QCA1reusedpe: 'Ridgeline' is a reused sample company (9 other specs, among them quote-form, proposal-form, event-landing-page and pricing-page). 'Calder' (tab 1, Calder Law) appears on 2 other specs.
- P1 /ai-automation-builder/document-automation `faq (item 1)` B-HUBRULES8CON: The recorded source (Wikipedia) says document automation is 'also known as' document assembly. Calling it the 'older name' goes beyond what the source says.
- P1 /ai-automation-builder/document-automation `faq (item 3)` B-HUBRULES8CON: 'The most common use' is a market-wide fact with no domain_sources entry.
- P1 /ai-automation-builder/ecommerce-automation `tab_content_1; images.tab_image_1.alt; image_brief.tabs[0]` B-QCA1stocknam: The dropship tab routes order #10482 to 'Northwind Textiles', a stock placeholder company. It appears in the live tab copy, the alt text and the image ('PO to Northwind Textiles', 'Northwind tracking').
- P1 /ai-automation-builder/ecommerce-automation `tab_content_3; mockup; image_brief.tabs[2]` B-QCA1reusedpe: 'Dana Whitfield' is a heavily reused persona (13 other specs, e.g. contact-form, booking-form, payment-form, nda-form). Here it appears in the tab copy, the mockup prompt and the image.
- P1 /ai-automation-builder/ecommerce-automation `tab_content_1; image_brief.tabs[0]; images.tab_image_1.alt` B-QCA1reusedpe: 'Fernhill' is a reused sample brand (15 other specs). 'Fernhill Home' itself also appears on complaint-form.
- P1 /ai-automation-builder/ecommerce-automation `image_brief.tabs[1]; images.tab_image_2.alt` B-QCA1reusedpe: The winback image and its alt reuse 'Priya Nair' (22 other specs) and 'Marcus Bell' (13 other specs).
- P1 /ai-automation-builder/ecommerce-automation `tab_content_4; mockup; image_brief.tabs[3]` B-QCA1reusedpe: 'Sam Ortega', the founder in the margin-report tab, also appears on employee-feedback-form.
- P1 /ai-form-builder/interest-form `image_brief.tabs[2].main.blocks[1].items` B-DECISIONS202: The live uc-3 image reuses persona names from other pages: 'Dana Kim' (also on training-request-form and grievance-form; 'Dana' is on 79 other specs) and 'Luis Ortega' (on 5 other specs).
- P1 /ai-form-builder/interest-form `tab_content_1, tab_content_2, tab_content_4 (and matching image_brief/alt)` B-DECISIONS202: The example businesses are recurring fictional names used across the hub: Fernhill (15 other specs), Brightwater (10), Pine Hollow (5).
- P1 /ai-form-builder/interest-form `template` B-DECISIONS202: The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- P1 /ai-form-builder/interest-form `template` B-DECISIONS202: The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- P1 /ai-form-builder/job-application-form `image_brief.tabs[0].main.blocks[0].title; images.cover_image.alt; image_brief.cover.alt` B-DECISIONS202: The live uc-1 image and the cover alt use the stock placeholder company 'Northwind'; QC on the spec now fails at TOTAL 3.
- P1 /ai-form-builder/job-application-form `image_brief.tabs[0..3] (uc-1 to uc-4)` B-DECISIONS202: The live images draw persona first names that recur across the hub: Dana Ruiz (Dana on 79 other specs), Priya Shah (50), Lena Fox (44), Tom Baker (35), Jordan Lee (33), Maya Ortiz (28), Leo Park (22), Grace Liu (20), Ben Walsh (19), Omar Haddad (16). 'Elm Street' is on 9 other specs, and Jordan and 
- P1 /ai-form-builder/job-application-form `template` B-DECISIONS202: The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- P1 /ai-form-builder/job-application-form `template` B-DECISIONS202: The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- P1 /ai-form-builder/liability-waiver-form `image_brief.tabs[0], image_brief.tabs[2] (uc-1, uc-3)` B-DECISIONS202: The live images reuse persona first names that recur across the hub: Dana Kerrigan (Dana on 79 other specs), Maya Singh (28), Owen Stroud (21), Ava Kerrigan (17).
- P1 /ai-form-builder/liability-waiver-form `template` B-DECISIONS202: The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- P1 /ai-form-builder/liability-waiver-form `template` B-DECISIONS202: The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- P1 /ai-form-builder/massage-intake-form `tab_content_4; image_brief.tabs[3].main.blocks[0].text; plan.openers[3]` B-DECISIONS202: The live tab copy and the uc-4 image use the stock placeholder company 'Globex'; QC on the spec now fails at TOTAL 2.
- P1 /ai-form-builder/massage-intake-form `tab_content_2; images.tab_image_2.alt; image_brief.tabs[0..3]` B-DECISIONS202: The live copy and images reuse names that recur across the hub: Dana Ellis in tab 2's copy and alt (Dana on 79 other specs), Sam Okafor and Sam Ortiz drawn on the same page (Sam on 51 specs), Grace Tully (20), Mia Porter (15), Chris Vale (8). The businesses Juniper (18 other specs) and Kestrel (13) 
- P1 /ai-form-builder/massage-intake-form `template` B-DECISIONS202: The shared 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp' on every page; this sits outside the child collections, so it needs Divit.
- P1 /ai-form-builder/massage-intake-form `template` B-DECISIONS202: The template testimonials use generic persona names and companies (Maya Chen of BrightSuite, Jordan Patel of LoopDesk, Alex Rivera of TaskFlow); if they are not real customers they read as stock personas, and the first names recur across the child pages' images. Needs Divit to confirm they are real.
- P1 /ai-form-builder/t-shirt-order-form `mockup` B-HUBRULES2bQC: Stock placeholder name Northwind in the newHireKits mockup prompt.
- P1 /ai-form-builder/t-shirt-order-form `image_brief.tabs[3].main.blocks[0].title` B-HUBRULES2bQC: Northwind is drawn in the tab 4 image (form title); re-render after the rename.
- P1 /ai-form-builder/t-shirt-order-form `image_brief.tabs[3].hero.blocks[1].text` B-HUBRULES2bre: Reused persona names drawn in the tab 4 image: Jordan Lee appears in 10 other specs, Sam Patel in 4.
- P1 /ai-form-builder/t-shirt-order-form `image_brief.tabs[1].hero.blocks[0].sub` B-HUBRULES2bre: Rosa Delgado is drawn in the tab 2 image and is reused in 5 other specs.
- P1 /ai-form-builder/t-shirt-order-form `template` B-HUBRULES2bQC: The 'More things you can build' carousel's AI CRM Builder card draws the stock name Acme Corp (hub cover asset outside the four hubs' collections).
- P1 /ai-landing-page-builder/404-page `images.tab_image_1.alt` B-HUBRULES5alt: Alt text carries Northwind.
- P1 /ai-landing-page-builder/404-page `images.tab_image_2.alt` B-HUBRULES5alt: Alt text carries Acme.
- P1 /ai-landing-page-builder/404-page `images.tab_image_4.alt` B-HUBRULES5alt: Alt text carries Globex.
- P1 /ai-landing-page-builder/404-page `image_brief.tabs[0].main.chrome; image_brief.tabs[1].main.chrome` B-HUBRULES2bQC: Stock names drawn in the images: the tab 1 browser bar reads northwind.example, tab 2 carries Acme.
- P1 /ai-landing-page-builder/404-page `template` B-HUBRULES2bQC: The carousel's AI CRM Builder card draws the stock name Acme Corp.
- P1 /ai-landing-page-builder/ebook-landing-page `template` B-HUBRULES2bQC: The carousel's AI CRM Builder card draws the stock name Acme Corp.
- P1 /ai-landing-page-builder/event-landing-page `mockup` B-HUBRULES2bre: Same reused persona in the cityRoadshow mockup prompt.
- P1 /ai-landing-page-builder/event-landing-page `images.tab_image_4.alt` B-HUBRULES5alt: Alt text carries the reused persona Dana Whitfield.
- P1 /ai-landing-page-builder/event-landing-page `image_brief.tabs[3]` B-HUBRULES2bre: Tab 4 image draws Dana Whitfield (14 other specs) and registrant Priya Shah (19 other specs).
- P1 /ai-landing-page-builder/event-landing-page `template` B-HUBRULES2bQC: The carousel's AI CRM Builder card draws the stock name Acme Corp.
- P1 /ai-survey-and-quiz-builder/church-survey `template` B-QCA1stocknam: The sitewide 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp'; one component fix covers every page.
- P1 /ai-survey-and-quiz-builder/customer-feedback-survey `mockup` B-DECISIONSser: Two lists in the mockup prompts drop the serial comma, while tab 2 uses it, so the page mixes both styles.
- P1 /ai-survey-and-quiz-builder/customer-feedback-survey `tab_image_2 alt` B-DECISIONSser: The alt text list drops the serial comma that tab 2's copy uses for the same four tags.
- P1 /ai-survey-and-quiz-builder/customer-feedback-survey `template` B-QCA1stocknam: The sitewide 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp'; one component fix covers every page.
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `image_brief / tab_image_3 alt` B-QCA1AItellsr: Persona names are reused across the site: 'Ana Ruiz' appears in 24 other specs, and 'K. Osei' and 'R. Diaz' each appear in 2 others.
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `mockup` B-DECISIONSser: The annualCensus prompt drops the serial comma twice, while feature_1 lists the same four drivers with it.
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `tab_image_1 alt` B-DECISIONSser: A four-item list is missing its serial comma.
- P1 /ai-survey-and-quiz-builder/employee-engagement-survey `template` B-QCA1stocknam: The sitewide 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp'; one component fix covers every page.
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `mockup` B-DECISIONSser: The mockup prompts drop the serial comma in two lists, while the remoteVsOffice prompt uses it.
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `tab_image_4 alt` B-DECISIONSser: A four-item list is missing its serial comma.
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `image_brief / tab_image_2` B-QCA1AItellsr: The nurse manager's name 'D. Okafor' is reused from /ai-form-builder/registration-form.
- P1 /ai-survey-and-quiz-builder/employee-satisfaction-survey `template` B-QCA1stocknam: The sitewide 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp'; one component fix covers every page.
- P1 /ai-landing-page-builder/video-landing-page `template` B-QCA1Divit202: The sitewide testimonial strip uses stock AI-style personas (Alex Rivera of TaskFlow, Maya Chen of BrightSuite, Jordan Patel of LoopDesk), repeated four times in the carousel on every child page.
- P1 /ai-landing-page-builder/video-landing-page `template` B-QCA1Divit202: The AI CRM Builder card image in the "More things you can build" section draws the stock company name "Acme Corp".
- P1 /ai-landing-page-builder/video-landing-page `image_brief.tabs[3]` B-CONTENTDEFEC: The copy says Owen is messaged once Edda passes the one-minute mark of a two-minute video, but the drawn DM and step both report 1:24, so the alert fires 24 seconds late in the picture.
- P1 /ai-landing-page-builder/webinar-landing-page `template` B-QCA1Divit202: The sitewide testimonial strip uses stock AI-style personas (Alex Rivera of TaskFlow, Maya Chen of BrightSuite, Jordan Patel of LoopDesk), repeated four times in the carousel on every child page.
- P1 /ai-landing-page-builder/webinar-landing-page `template` B-QCA1Divit202: The AI CRM Builder card image in the "More things you can build" section draws the stock company name "Acme Corp".
- P1 /ai-landing-page-builder/webinar-landing-page `image_brief.tabs[0]` B-QCA1Divit202: The tab 1 image fills the registrant field with "Maya Chen", the same name as the stock testimonial persona shown higher on the same page.
- P1 /ai-survey-and-quiz-builder/brand-awareness-survey `template` B-QCA1Divit202: The sitewide testimonial strip uses stock AI-style personas (Alex Rivera of TaskFlow, Maya Chen of BrightSuite, Jordan Patel of LoopDesk), repeated four times in the carousel on every child page.
- P1 /ai-survey-and-quiz-builder/brand-awareness-survey `template` B-QCA1Divit202: The AI CRM Builder card image in the "More things you can build" section draws the stock company name "Acme Corp".
- P1 /ai-survey-and-quiz-builder/brand-awareness-survey `template` B-LEARNCAROUSE: The Learn list renders live on the survey template with three off-topic AI-model articles whose cards link to "#", although the section is meant to be hidden.
- P1 /ai-survey-and-quiz-builder/brand-awareness-survey `image_brief.tabs[3]` B-CONTENTDEFEC: The copy runs the test in Phoenix before the first truck arrives, yet the drawn Phoenix respondent answers "Seen it on a truck"; the screen also asks about a logo that is not drawn.
- P1 /ai-survey-and-quiz-builder/brand-perception-survey `template` B-QCA1Divit202: The sitewide testimonial strip uses stock AI-style personas (Alex Rivera of TaskFlow, Maya Chen of BrightSuite, Jordan Patel of LoopDesk), repeated four times in the carousel on every child page.
- P1 /ai-survey-and-quiz-builder/brand-perception-survey `template` B-QCA1Divit202: The AI CRM Builder card image in the "More things you can build" section draws the stock company name "Acme Corp".
- P1 /ai-survey-and-quiz-builder/brand-perception-survey `template` B-LEARNCAROUSE: The Learn list renders live on the survey template with three off-topic AI-model articles whose cards link to "#", although the section is meant to be hidden.
- P1 /ai-automation-builder/incident-response-automation `template` B-QCA1stocknam: The sitewide 'More things you can build' component draws the stock name Acme Corp on the AI CRM Builder card thumbnail; it is outside the CMS and the hub collections.

### Drift (edited in Webflow, reported, not overwritten) (0)


### Needs a CMS read to classify (drift check) (0)


### Backlog (P2) (174)

- P2 /ai-automation-builder/accounts-payable-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/data-entry-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/document-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/ecommerce-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/incident-response-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/invoice-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/procurement-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/sales-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder/task-automation `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/booking-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/client-onboarding-questionnaire `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/credit-card-authorization-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/direct-deposit-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/employee-information-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/employment-verification-letter `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/feedback-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/interest-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/job-application-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/liability-waiver-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/massage-intake-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/order-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/registration-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/rental-agreement-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/sign-in-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-form-builder/t-shirt-order-form `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/404-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/ebook-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/event-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/landing-page-seo `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/law-firm-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/mobile-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/pricing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/video-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-landing-page-builder/webinar-landing-page `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-survey-and-quiz-builder/brand-awareness-survey `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-survey-and-quiz-builder/brand-perception-survey `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-survey-and-quiz-builder/church-survey `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-survey-and-quiz-builder/customer-feedback-survey `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-survey-and-quiz-builder/employee-engagement-survey `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-survey-and-quiz-builder/employee-satisfaction-survey `template` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in visible text
- P2 /ai-automation-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-form-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-landing-page-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-survey-and-quiz-builder `hub` A5-empty-p: empty paragraph (Webflow rich-text zero-width placeholder) in hub text
- P2 /ai-form-builder/direct-deposit-form `why_table` B-CONTENTDEFEC: The 'Response limits' row answers with pricing for ADP and Eddy, so the row label does not match the cells (library variant).
- P2 /ai-form-builder/direct-deposit-form `meta_title` B-HUBRULES2b: Meta title reads clipped and machine-assembled (carried review note).
- P2 /ai-form-builder/direct-deposit-form `howto_step_1_des` B-HUBRULES5390: At 390 px 'W-9' breaks at its hyphen across two lines ('a W-' / '9 before').
- P2 /ai-form-builder/direct-deposit-form `image_brief tab 1` B-CONTENTDEFEC: Confidence bar (100%) drawn on the value the employee typed, which reads as if the typed value were extracted (carried review note).
- P2 /ai-form-builder/employee-information-form `tab_content_1` B-HUBRULES8fie: The example runs the yearly check in January, while step 6 says to pick a quiet month away from year-end payroll (W-2 season).
- P2 /ai-form-builder/employee-information-form `faq item 10` B-HUBRULES2a: Advice to keep emergency contact forms at a front desk conflicts with FAQ 8's need-to-know access advice.
- P2 /ai-form-builder/employment-verification-letter `tab_content_3` B-HUBRULES8: Missouri service letter conditions omit that the written request must refer to the statute (Mo. Rev. Stat. 290.140); material conditions present (carried note).
- P2 /ai-form-builder/employment-verification-letter `why_table` B-CONTENTDEFEC: The 'Response limits' row answers BambooHR with pricing, not a limit.
- P2 /ai-form-builder/employment-verification-letter `image_brief tab 2` B-CONTENTDEFEC: The drawn letter omits the job title the copy says it states (carried note).
- P2 /ai-form-builder/employment-verification-letter `image_brief tab 1` B-CONTENTDEFEC: 100% confidence bars on values copied from the HR table read as document extraction (carried note).
- P2 /ai-form-builder/feedback-form `image_brief tab 1` B-HUBRULES2b: Order #10482 is the HUB_RULES 2b example number and appears on 8 specs, a repeated stock detail across pages.
- P2 /ai-form-builder/feedback-form `images.tab_image_2.alt` B-HUBRULES2b: Listing name 'Alder Lane' is reused on 5 other specs.
- P2 /ai-form-builder/feedback-form `tab_content_1` B-HUBRULES2b: All four tab paragraphs open on a general maxim before the story (templated shape; carried note).
- P2 /ai-automation-builder/document-automation `faq (heading)` B-HUBRULES5FAQ: The FAQ heading drops 'Questions'. Every sibling uses the '{Topic} Questions, Answered' shape.
- P2 /ai-automation-builder/document-automation `faq (item 1)` B-HUBRULES2bno: A rhetorical question sits in the definition answer.
- P2 /ai-automation-builder/document-automation `faq (item 5)` B-CONTENTDEFEC: 'usually' is an unsourced generalization about how agreements are handled.
- P2 /ai-automation-builder/document-automation `why_table` B-QCK7HUBRULES: None of the three tabled competitors (Zapier, Make, n8n) ranks in this page's top 10. This is still pending with Divit from the review.
- P2 /ai-automation-builder/ecommerce-automation `why_table` B-QCK7HUBRULES: n8n does not rank in this page's top 10.
- P2 /ai-form-builder/interest-form `image_brief.tabs[0].kpi.sub` B-CONTENTDEFEC: The image shortens the copy's 'Fernhill Community College' to 'Fernhill College'.
- P2 /ai-form-builder/interest-form `faq (item 6)` B-HUBRULES5lin: The last sentence exists to carry a sibling link and shifts to brands and creators, which no other part of the answer or page addresses.
- P2 /ai-form-builder/interest-form `mockup` B-HUBRULES5moc: Tab 4 is labelled 'Staff Mentoring' but its mockup key is workplaceMentoring (the template appears to map keys by position, so nothing visibly breaks).
- P2 /ai-form-builder/interest-form `why_table` B-HUBRULES5com: Typeform is in the table but not in the page's top 10, while Microsoft Forms (#7) is left out.
- P2 /ai-form-builder/liability-waiver-form `faq (item 4)` B-HUBRULES8: The source says notarization can add a layer of protection; the reason given ('easier to prove if someone later disputes it') is not in the source.
- P2 /ai-form-builder/liability-waiver-form `image_brief.tabs[3] (uc-4)` B-CONTENTDEFEC: The copy says any contractor within 30 days of expiry gets an email, but the image shows Ironvale Plumbing at 26 days with no request sent; only Thornbury Electric's request is drawn.
- P2 /ai-form-builder/liability-waiver-form `features_subheading` B-CONTENTDEFEC: The intro promises six parts a signed waiver depends on, but feature 6 (custom domain and code export) is not part of a waiver.
- P2 /ai-form-builder/massage-intake-form `image_brief.tabs[2].hero; image_brief.cover` B-CONTENTDEFEC: The Slack card to Owen Tate draws a channel '#' glyph, so a message to one therapist reads as a channel named after him.
- P2 /ai-form-builder/t-shirt-order-form `image_brief.tabs[2].main.blocks[1].rows` B-HUBRULES2bre: Captain names in the tab 3 image recur on other pages (M. Chen 4 specs, J. Alvarez 4, L. Brandt 2); 14 Elm Street in tab 4 recurs in 9 specs.
- P2 /ai-form-builder/t-shirt-order-form `faq` B-HUBRULES5FAQ: FAQ 10 ends on a sentence about race entries that does not answer whether the forms are free; it exists to carry the registration form link.
- P2 /ai-form-builder/t-shirt-order-form `tab_content_2` B-HUBRULES2are: Tab 2 H3 drops the article: 'a name on back'.
- P2 /ai-form-builder/t-shirt-order-form `faq` B-layoutat390p: At 390 px FAQ questions 5 and 7 break the line inside 'T-shirt' at the hyphen ('T-' / 'shirt').
- P2 /ai-form-builder/t-shirt-order-form `template` B-HUBRULES2bre: Sitewide testimonial strip uses generic placeholder personas (Alex Rivera, Maya Chen, Jordan Patel) with invented companies, repeated 4 times in the DOM.
- P2 /ai-landing-page-builder/404-page `faq` B-HUBRULES2apr: FAQ 9's last sentence implies exporting the code is how you confirm the status code, which step 6 says you check by requesting a missing URL.
- P2 /ai-landing-page-builder/404-page `faq` B-HUBRULES5que: Two FAQ questions read as broken English on the page.
- P2 /ai-landing-page-builder/404-page `faq` B-HUBRULES5CON: FAQ 5 closes on a thank-you-page sentence that only carries a link; FAQ 10 does the same for landing page SEO.
- P2 /ai-landing-page-builder/404-page `feature_1` B-HUBRULES2are: Feature 1 opens by narrating the user's prompt; the semicolon joins two unrelated instructions.
- P2 /ai-landing-page-builder/404-page `template` B-HUBRULES2bre: Sitewide testimonial strip uses generic placeholder personas.

## Request

Scheduled or requested live audit per docs/LIVE_AUDIT.md (DECISIONS 2026-10-09).

## Actions and results

- Layer A on 40 pages and 4 hubs at https://emergent.sh; Layer B batches: 10; recorded: 10.
- Findings: `audits/live/2026-10-12/findings.json`; per-page files `audits/live/2026-10-12/<slug>.md`; ledger `audits/live/LEDGER.md`.

## Webflow calls

- see the ledger rows for this date (update and item publish per fix, read back)

## Not done

- Proposals and drift wait for Divit.

## Open questions for Divit

- Each proposal above has a recommended fix in its per-page file.
