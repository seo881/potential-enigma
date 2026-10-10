# Readiness board

Regenerated 2026-10-10 11:08 UTC by `hubctl readiness` (also after every `hubctl ship` step). Public: counts and IDs only.

## Template blockers (plan/template-edits-2026-10-08.md)

| # | Edit | Blocks first publish | Status |
|---|---|---|---|
| T1 | Hero default prompt + chips | yes | REPLACED 2026-10-09 by the hero-chips embed (ops/template/hero-chips.html) on all 4 templates; T1 embeds removed; chips carry data-hubchip |
| T2 | FAQ guard | yes | staged on 4 templates (2026-10-08) |
| T3 | Learn list (Option A, Designer only) | yes | DONE (verified read-only 2026-10-09 by the advisor chat): Form, LP and SQB Learn lists source the whole Learn collection, no filters, sorted learn---publishing-date descending; AAB is the reference template (not re-read); 2026-10-09: limit 100 -> 3 on Form, LP, AAB (limit 100 rendered "No items found"; SQB already 3) |
| T4 | Arrow aria-label | yes | staged on 4 templates (2026-10-08) |
| T5 | Cover alt binding (Designer only) | yes | DONE (2026-10-09, advisor chat): cover altText bound to the item Product name on the 4 templates and the 4 hub carousels (Webflow Audits non-descriptive link flag); staged until the next publish; see logs/templates.md |
| T6 | Carousel (section_build) visible on all 4 child templates | no | HIDDEN again 2026-10-09 (Divit): carousel hidden on hubs and child templates until its formatting is reworked; revisit Monday |
| T7 | Form schema | no | no edit needed |
| T8 | "Add Features :" text | no | not approved (needs Divit's go) |
| T9 | Hero form and input names (duplicate IDs) | yes | staged on 4 templates (2026-10-08) |
| T10 | Tabs default (verify tab 1) | yes if tab 1 is not default | VERIFY ON STAGING: the API does not expose the default tab; verify_launch checks the first use-case tab is active on load |
| T11 | OG image binding, meta, breadcrumbs, mobile table | yes | DONE (verified read-only 2026-10-09): all 4 templates have SEO title/description bound to meta-title/meta-description, Open Graph image bound to thumbnail-image, OG title and description copied from SEO |
| T12 | Audits panel on each template | no | NON-BLOCKING (Divit, 2026-10-09): QC covers it; run the Audits panel after launch |

## Pages

| Batch | Page | QC TOTAL | PAA gate | Review (launch) | Images current | PA13 approved | Pending links | CMS item | Draft synced | Published | Ship stage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| batch-0 | /ai-automation-builder/approval-workflow | 6 | 10/10 | no | no | no | 0 | 6aba7ac40efe4e6ac8693159 | no | no | stopped (stopped) |
| batch-0 | /ai-form-builder/creator-application | 52 | 4/12 | no | no | no | 0 | 6ab505a8d621dc692561a85a | no | no | stopped (stopped) |
| batch-0 | /ai-landing-page-builder/thank-you-page | 4 | 9/10 | no | no | no | 0 | 6ab5158e23395050bc86ca79 | no | no | stopped (stopped) |
| batch-0 | /ai-survey-and-quiz-builder/customer-satisfaction | 8 | 10/10 | no | no | no | 0 | 6aba7afb6271de33629b812c | no | no | stopped (stopped) |
| batch-1 | /ai-automation-builder/document-automation | 0 | 10/10 | yes, launch-r-b1-4 | yes | no | 3 | 6ac89f5186706b45a79b39b4 | yes | yes | done |
| batch-1 | /ai-automation-builder/ecommerce-automation | 0 | 10/10 | yes, launch-r-b1-5 | yes | no | 2 | 6ac8a1af7019f6d354746f12 | yes | yes | done |
| batch-1 | /ai-automation-builder/sales-automation | 0 | 10/10 | yes, launch-r-b1-4 | yes | no | 3 | 6ac89f5186706b45a79b39b2 | yes | yes | done |
| batch-1 | /ai-automation-builder/task-automation | 0 | 10/10 | yes, launch-r-b1-4 | yes | no | 2 | 6ac89f5186706b45a79b39b6 | yes | yes | done |
| batch-1 | /ai-form-builder/booking-form | 0 | 10/10 | yes, launch-r-b1-6 | yes | no | 2 | 6ac8a2bff143d8ebe3277361 | yes | yes | done |
| batch-1 | /ai-form-builder/checkout-form | 11 | 8/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/client-onboarding-questionnaire | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 3 | 6ac8a0256cea93e7ab27259d | yes | yes | done |
| batch-1 | /ai-form-builder/conference-registration-form | 5 | 7/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/consultation-form | 9 | 7/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/contact-form | 10 | 7/10 | yes, launch-r-b1-5 | yes | no | 2 | 6ac8a2bff143d8ebe327735f | no | no | done (stopped) |
| batch-1 | /ai-form-builder/employee-information-form | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 3 | 6ac8a06cc42bf1463b1a2cbc | yes | yes | done |
| batch-1 | /ai-form-builder/feedback-form | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 3 | 6ac8a06cc42bf1463b1a2cb8 | yes | yes | done |
| batch-1 | /ai-form-builder/interest-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 3 | 6ac8a04200f35689bf9ff3c4 | yes | yes | done |
| batch-1 | /ai-form-builder/job-application-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 2 | 6ac8a04200f35689bf9ff3c0 | yes | yes | done |
| batch-1 | /ai-form-builder/massage-intake-form | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 2 | 6ac8a06cc42bf1463b1a2cba | yes | yes | done |
| batch-1 | /ai-form-builder/registration-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 2 | 6ac79cdc9308a032a2f7dd2d | yes | yes | done |
| batch-1 | /ai-form-builder/sign-in-form | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 3 | 6ac8a0256cea93e7ab27259f | yes | yes | done |
| batch-1 | /ai-form-builder/summer-camp-registration-form | 6 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/t-shirt-order-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 2 | 6ac8a04200f35689bf9ff3c2 | yes | yes | done |
| batch-1 | /ai-landing-page-builder/404-page | 0 | 10/10 | yes, launch-r-b1-5 | yes | no | 2 | 6ac8a23f9873b6bc7b4343ba | yes | yes | done |
| batch-1 | /ai-landing-page-builder/event-landing-page | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 2 | 6ac89f545408b01694dc164b | yes | yes | done |
| batch-1 | /ai-landing-page-builder/law-firm-landing-page | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 3 | 6ac89f545408b01694dc164d | yes | yes | done |
| batch-1 | /ai-landing-page-builder/pricing-page | 0 | 10/10 | yes, launch-r-b1-6 | yes | no | 2 | 6ac8a23f9873b6bc7b4343bc | yes | yes | done |
| batch-1 | /ai-landing-page-builder/webinar-landing-page | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 2 | 6ac89f545408b01694dc1649 | yes | yes | done |
| batch-1 | /ai-survey-and-quiz-builder/employee-engagement-survey | 0 | 10/10 | yes, launch-r-b1-5 | yes | no | 2 | 6ac8a15a5408b01694dd5e21 | yes | yes | done |
| wk-new-aab | /ai-automation-builder/data-entry-automation | 0 | 10/10 | no | yes | no | 0 | - | no | no | check |
| wk-new-aab | /ai-automation-builder/incident-response-automation | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-new-aab | /ai-automation-builder/procurement-automation | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-new-lp | /ai-landing-page-builder/ebook-landing-page | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-new-lp | /ai-landing-page-builder/mobile-landing-page | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-new-lp | /ai-landing-page-builder/video-landing-page | 0 | 10/10 | no | no | no | 0 | - | no | no | check |
| wk-new-sqb | /ai-survey-and-quiz-builder/brand-awareness-survey | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-new-sqb | /ai-survey-and-quiz-builder/brand-perception-survey | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-new-sqb | /ai-survey-and-quiz-builder/church-survey | 0 | 10/10 | no | yes | no | 0 | - | no | no | check |
| wk-rework-aab | /ai-automation-builder/accounts-payable-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 0 | - | no | no | payload |
| wk-rework-aab | /ai-automation-builder/invoice-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 0 | - | no | no | payload |
| wk-rework-aab | /ai-automation-builder/purchase-order-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 0 | - | no | no | payload |
| wk-rework-aab | /ai-automation-builder/social-media-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/accident-report-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/accounting-client-intake-form | 6 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/ach-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/address-verification-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/advance-directive-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/affidavit-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/anesthesia-consent-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/anonymous-feedback-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/approval-form | 5 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/audition-form | 9 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/background-check-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/botox-consent-form | 5 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/brand-questionnaire | 7 | 7/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/cake-order-form | 7 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/car-rental-form | 6 | 0/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/chemical-peel-consent-form | 7 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/church-membership-form | 12 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/class-registration-form | 6 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/cobra-election-form | 6 | 0/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/complaint-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/conditional-logic-form | 6 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/consent-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/contest-entry-form | 8 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/copyright-release-form | 6 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/credit-application-form | 0 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/credit-card-authorization-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/custom-order-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/daycare-registration-form | 5 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/dental-intake-form | 6 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/direct-deposit-form | 0 | 10/10 | yes, wk-r-8 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/driver-application-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/drug-test-consent-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/emergency-contact-form | 0 | 10/10 | yes, wk-r-13 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/employee-availability-form | 0 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/employee-evaluation-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/employee-feedback-form | 5 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/employee-referral-form | 5 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/employment-verification-letter | 0 | 10/10 | yes, wk-r-8 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/equipment-rental-agreement-form | 8 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/esthetician-intake-form | 5 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/event-planning-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/expense-report-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/expense-request-form | 7 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/field-trip-permission-slip | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/file-upload-form | 8 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/fitness-assessment-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/food-bank-application-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/food-order-form | 6 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/grievance-form | 0 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/health-screening-form | 7 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/home-care-intake-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/hotel-booking-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/identity-verification-form | 0 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/incident-report-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/independent-contractor-agreement | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/insurance-verification-form | 8 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/intake-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/interior-design-questionnaire | 6 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/interview-evaluation-form | 7 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/it-request-form | 8 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/lead-capture-form | 0 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/legal-intake-form | 8 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/liability-waiver-form | 0 | 10/10 | yes, wk-r-8 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/life-coaching-intake-form | 5 | 7/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/maintenance-request-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/medical-history-form | 0 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/membership-form | 0 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/mileage-reimbursement-form | 0 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/model-release-form | 0 | 10/10 | yes, wk-r-13 | no | no | 0 | - | no | no | images2 |
| wk-rework-form | /ai-form-builder/multi-step-form | 8 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/nda-form | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/new-employee-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/order-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/overtime-request-form | 1 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/parent-consent-form | 0 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/patient-intake-form | 0 | 10/10 | yes, wk-r-13 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/payment-form | 1 | 7/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/payroll-change-form | 8 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/permanent-makeup-consent-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/personal-injury-intake-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/pet-adoption-form | 11 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/petition-form | 0 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/photo-release-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/pre-order-form | 8 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/project-request-form | 14 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/proposal-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | check2 |
| wk-rework-form | /ai-form-builder/pt-intake-form | 5 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/purchase-order-form | 0 | 10/10 | yes, wk-r-13 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/quote-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/reasonable-accommodation-request-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/reference-check-form | 6 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/referral-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-form | /ai-form-builder/refund-request-form | 8 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/rental-agreement-form | 0 | 10/10 | yes, wk-r-8 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/rental-application-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/rental-history-form | 8 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/requisition-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-form | /ai-form-builder/restaurant-reservation-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-form | /ai-form-builder/rfp-form | 0 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/rfq-form | 6 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/service-request-form | 8 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/shipping-address-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/shipping-form | 5 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sign-out-form | 0 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sign-up-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/silent-auction-form | 6 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sponsorship-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-form | /ai-form-builder/student-registration-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sublease-form | 5 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/suggestion-form | 7 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/surgery-consent-form | 9 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/tattoo-consent-form | 0 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/telemedicine-consent-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/tenant-screening-form | 8 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/testimonial-form | 8 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/therapy-intake-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-form | /ai-form-builder/time-off-request-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/time-sheet-form | 0 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/tournament-registration-form | 8 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/training-feedback-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-form | /ai-form-builder/training-request-form | 7 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/travel-reimbursement-form | 6 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/travel-request-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/vehicle-inspection-form | 0 | 0/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/vendor-application | 7 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/volunteer-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-form | /ai-form-builder/webinar-registration-form | 6 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/website-design-questionnaire | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/wedding-photography-contract | 9 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/wedding-photography-questionnaire | 9 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/work-order-form | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/workshop-registration-form | 7 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-lp | /ai-landing-page-builder/app-landing-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/b2b-landing-page | 0 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/campaign-landing-page | 0 | 10/10 | yes, wk-r-4 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/coming-soon-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/landing-page-seo | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/lead-generation-landing-page | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/one-page-website | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/ppc-landing-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/product-landing-page | 0 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/real-estate-landing-page | 0 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/saas-landing-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/splash-page | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/squeeze-page | 0 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/360-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/customer-effort-score | 0 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/customer-experience-survey | 0 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/customer-feedback-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/employee-benefits-survey | 6 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-sqb | /ai-survey-and-quiz-builder/employee-satisfaction-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/exit-survey | 0 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/onboarding-survey | 0 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/pulse-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 0 | - | no | no | payload |

Stages: check 3, check2 1, done 21, images2 1, payload 63, review 13, stopped 94 (196 pages)
