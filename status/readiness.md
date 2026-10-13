# Readiness board

Regenerated 2026-10-13 11:21 UTC by `hubctl readiness` (also after every `hubctl ship` step). Public: counts and IDs only.

## Template blockers (plan/template-edits-2026-10-08.md)

| # | Edit | Blocks first publish | Status |
|---|---|---|---|
| T1 | Hero default prompt + chips | yes | REPLACED 2026-10-09 by the hero-chips embed (ops/template/hero-chips.html) on all 4 templates; T1 embeds removed; chips carry data-hubchip |
| T2 | FAQ guard | yes | staged on 4 templates (2026-10-08) |
| T3 | Learn list (Option A, Designer only) | yes | CORRECTED 2026-10-13 (Divit, DECISIONS 2026-10-13): the Learn list source stays on each item's own '... - Learn' multi-reference field (the 2026-10-09 note saying Form/LP/SQB source the whole Learn collection was wrong for Form/LP/AAB); fix = acrm---learn filled with the 3 newest published Learn articles (39 live items 2026-10-13, new items at creation, L12) + blog_link to detail_learn on all 4 templates; section_blog-related hidden on Form/LP/AAB until Divit's production go |
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
| batch-0 | /ai-automation-builder/approval-workflow | 13 | 10/10 | no | no | no | 0 | 6aba7ac40efe4e6ac8693159 | no | no | stopped (stopped) |
| batch-0 | /ai-form-builder/creator-application | 54 | 4/12 | no | no | no | 0 | 6ab505a8d621dc692561a85a | no | no | stopped (stopped) |
| batch-0 | /ai-landing-page-builder/thank-you-page | 7 | 9/10 | no | no | no | 0 | 6ab5158e23395050bc86ca79 | no | no | stopped (stopped) |
| batch-0 | /ai-survey-and-quiz-builder/customer-satisfaction | 15 | 10/10 | no | no | no | 0 | 6aba7afb6271de33629b812c | no | no | stopped (stopped) |
| batch-1 | /ai-automation-builder/document-automation | 0 | 10/10 | yes, launch-r-b1-4 | yes | no | 3 | 6ac89f5186706b45a79b39b4 | yes | yes | done |
| batch-1 | /ai-automation-builder/ecommerce-automation | 0 | 10/10 | yes, launch-r-b1-5 | yes | no | 2 | 6ac8a1af7019f6d354746f12 | yes | yes | done |
| batch-1 | /ai-automation-builder/sales-automation | 0 | 10/10 | yes, launch-r-b1-4 | yes | no | 3 | 6ac89f5186706b45a79b39b2 | yes | yes | done |
| batch-1 | /ai-automation-builder/task-automation | 0 | 10/10 | yes, launch-r-b1-4 | yes | no | 1 | 6ac89f5186706b45a79b39b6 | yes | yes | done |
| batch-1 | /ai-form-builder/booking-form | 0 | 10/10 | yes, launch-r-b1-6 | yes | no | 2 | 6ac8a2bff143d8ebe3277361 | yes | yes | done |
| batch-1 | /ai-form-builder/checkout-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/client-onboarding-questionnaire | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 3 | 6ac8a0256cea93e7ab27259d | yes | yes | done |
| batch-1 | /ai-form-builder/conference-registration-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/consultation-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/contact-form | 0 | 10/10 | yes, launch-r-b1-5 | yes | no | 2 | 6ac8a2bff143d8ebe327735f | no | no | done (stopped) |
| batch-1 | /ai-form-builder/employee-information-form | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 2 | 6ac8a06cc42bf1463b1a2cbc | yes | yes | done |
| batch-1 | /ai-form-builder/feedback-form | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 3 | 6ac8a06cc42bf1463b1a2cb8 | yes | yes | done |
| batch-1 | /ai-form-builder/interest-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 2 | 6ac8a04200f35689bf9ff3c4 | yes | yes | done |
| batch-1 | /ai-form-builder/job-application-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 2 | 6ac8a04200f35689bf9ff3c0 | yes | yes | done |
| batch-1 | /ai-form-builder/massage-intake-form | 0 | 10/10 | yes, launch-r-b1-2 | yes | no | 1 | 6ac8a06cc42bf1463b1a2cba | yes | yes | done |
| batch-1 | /ai-form-builder/registration-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 2 | 6ac79cdc9308a032a2f7dd2d | yes | yes | done |
| batch-1 | /ai-form-builder/sign-in-form | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 2 | 6ac8a0256cea93e7ab27259f | yes | yes | done |
| batch-1 | /ai-form-builder/summer-camp-registration-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| batch-1 | /ai-form-builder/t-shirt-order-form | 0 | 10/10 | yes, launch-r-b1-1 | yes | no | 0 | 6ac8a04200f35689bf9ff3c2 | yes | yes | done |
| batch-1 | /ai-landing-page-builder/404-page | 0 | 10/10 | yes, launch-r-b1-5 | yes | no | 1 | 6ac8a23f9873b6bc7b4343ba | yes | yes | done |
| batch-1 | /ai-landing-page-builder/event-landing-page | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 1 | 6ac89f545408b01694dc164b | yes | yes | done |
| batch-1 | /ai-landing-page-builder/law-firm-landing-page | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 3 | 6ac89f545408b01694dc164d | yes | yes | done |
| batch-1 | /ai-landing-page-builder/pricing-page | 0 | 10/10 | yes, launch-r-b1-6 | yes | no | 2 | 6ac8a23f9873b6bc7b4343bc | yes | yes | done |
| batch-1 | /ai-landing-page-builder/webinar-landing-page | 0 | 10/10 | yes, launch-r-b1-3 | yes | no | 2 | 6ac89f545408b01694dc1649 | yes | yes | done |
| batch-1 | /ai-survey-and-quiz-builder/employee-engagement-survey | 0 | 10/10 | yes, launch-r-b1-5 | yes | no | 1 | 6ac8a15a5408b01694dd5e21 | yes | yes | done |
| wk-new-aab | /ai-automation-builder/data-entry-automation | 0 | 10/10 | yes, wk-r-20 | yes | no | 0 | 6accb27bf4e029b5515a4626 | yes | yes | payload |
| wk-new-aab | /ai-automation-builder/incident-response-automation | 0 | 10/10 | yes, wk-r-20 | yes | no | 1 | 6accb27bf4e029b5515a4628 | yes | yes | payload |
| wk-new-aab | /ai-automation-builder/procurement-automation | 0 | 10/10 | yes, wk-r-20 | yes | no | 2 | 6accb32573d2b6b752fb8d4e | yes | yes | payload |
| wk-new-aab | /ai-automation-builder/report-automation | 0 | 10/10 | no | yes | no | 0 | - | no | no | check |
| wk-new-lp | /ai-landing-page-builder/affiliate-landing-page | 2 | 10/10 | no | yes | no | 0 | - | no | no | check |
| wk-new-lp | /ai-landing-page-builder/ebook-landing-page | 0 | 10/10 | yes, wk-r-19 | yes | no | 1 | 6accb1512c9cca4363e93f7c | yes | yes | payload |
| wk-new-lp | /ai-landing-page-builder/mobile-landing-page | 0 | 10/10 | yes, wk-r-19 | yes | no | 1 | 6accb1fc9cd3f94473f62a80 | yes | yes | payload |
| wk-new-lp | /ai-landing-page-builder/sales-funnel-landing-page | 1 | 10/10 | no | yes | no | 0 | - | no | no | check |
| wk-new-lp | /ai-landing-page-builder/video-landing-page | 0 | 10/10 | yes, wk-r-19 | yes | no | 1 | 6accb1fc9cd3f94473f62a82 | yes | yes | payload |
| wk-new-sqb | /ai-survey-and-quiz-builder/brand-awareness-survey | 0 | 10/10 | yes, wk-r-21 | yes | no | 1 | 6accb39f13e0be4f1e5be581 | yes | yes | payload |
| wk-new-sqb | /ai-survey-and-quiz-builder/brand-perception-survey | 0 | 10/10 | yes, wk-r-21 | yes | no | 1 | 6accb39f13e0be4f1e5be583 | yes | yes | payload |
| wk-new-sqb | /ai-survey-and-quiz-builder/church-survey | 0 | 10/10 | yes, wk-r-21 | yes | no | 0 | 6accb44a40d5b6e947b71558 | yes | yes | payload |
| wk-new-sqb | /ai-survey-and-quiz-builder/wellness-survey | 1 | 10/10 | no | yes | no | 0 | - | no | no | check |
| wk-rework-aab | /ai-automation-builder/accounts-payable-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 2 | 6accb32573d2b6b752fb8d50 | yes | yes | payload |
| wk-rework-aab | /ai-automation-builder/invoice-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 2 | 6accb32573d2b6b752fb8d52 | yes | yes | payload |
| wk-rework-aab | /ai-automation-builder/purchase-order-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 0 | - | no | no | payload |
| wk-rework-aab | /ai-automation-builder/social-media-automation | 0 | 10/10 | yes, wk-r-5 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/accident-report-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/accounting-client-intake-form | 7 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/ach-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/address-verification-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/advance-directive-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/affidavit-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/anesthesia-consent-form | 10 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/anonymous-feedback-form | 10 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/approval-form | 8 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/audition-form | 10 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/background-check-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/botox-consent-form | 7 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/brand-questionnaire | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/cake-order-form | 8 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/car-rental-form | 8 | 0/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/chemical-peel-consent-form | 9 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/church-membership-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/class-registration-form | 7 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/cobra-election-form | 9 | 0/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/complaint-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/conditional-logic-form | 14 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/consent-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/contest-entry-form | 15 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/copyright-release-form | 15 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/credit-application-form | 1 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/credit-card-authorization-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 2 | 6accba1c29454f1af2f01f11 | yes | yes | payload |
| wk-rework-form | /ai-form-builder/custom-order-form | 8 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/daycare-registration-form | 6 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/dental-intake-form | 9 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/direct-deposit-form | 0 | 10/10 | yes, wk-r-8 | yes | no | 1 | 6accb96b8570d8ef2122bdec | yes | yes | payload |
| wk-rework-form | /ai-form-builder/driver-application-form | 0 | 10/10 | yes, wk-r-15 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/drug-test-consent-form | 12 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/emergency-contact-form | 0 | 10/10 | yes, wk-r-13 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/employee-availability-form | 1 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/employee-evaluation-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/employee-feedback-form | 6 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/employee-referral-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/employment-verification-letter | 0 | 10/10 | yes, wk-r-8 | yes | no | 2 | 6accb96b8570d8ef2122bde8 | yes | yes | payload |
| wk-rework-form | /ai-form-builder/equipment-rental-agreement-form | 9 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/esthetician-intake-form | 8 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/event-planning-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/expense-report-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/expense-request-form | 10 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/field-trip-permission-slip | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/file-upload-form | 13 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/fitness-assessment-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/food-bank-application-form | 10 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/food-order-form | 7 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/grievance-form | 1 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/health-screening-form | 10 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/home-care-intake-form | 0 | 10/10 | yes, wk-r-16 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/hotel-booking-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/identity-verification-form | 9 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/incident-report-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/independent-contractor-agreement | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/insurance-verification-form | 9 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/intake-form | 0 | 10/10 | yes, wk-r-10 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/interior-design-questionnaire | 8 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/interview-evaluation-form | 13 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/it-request-form | 9 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/lead-capture-form | 1 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/legal-intake-form | 11 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/liability-waiver-form | 0 | 10/10 | yes, wk-r-8 | yes | no | 2 | 6accba1c29454f1af2f01f0f | yes | yes | payload |
| wk-rework-form | /ai-form-builder/life-coaching-intake-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/maintenance-request-form | 8 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/medical-history-form | 4 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/membership-form | 2 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/mileage-reimbursement-form | 2 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/model-release-form | 0 | 10/10 | yes, wk-r-13 | yes | no | 0 | - | no | no | images2 |
| wk-rework-form | /ai-form-builder/multi-step-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/nda-form | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/new-employee-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/order-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 3 | 6accba1c29454f1af2f01f13 | yes | yes | payload |
| wk-rework-form | /ai-form-builder/overtime-request-form | 3 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/parent-consent-form | 1 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/patient-intake-form | 0 | 10/10 | yes, wk-r-13 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/payment-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/payroll-change-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/permanent-makeup-consent-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/personal-injury-intake-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/pet-adoption-form | 12 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/petition-form | 1 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/photo-release-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/pre-order-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/project-request-form | 22 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/proposal-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/pt-intake-form | 6 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/purchase-order-form | 0 | 10/10 | yes, wk-r-13 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/quote-form | 0 | 10/10 | yes, wk-r-17 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/reasonable-accommodation-request-form | 0 | 10/10 | yes, wk-r-14 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/reference-check-form | 7 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/referral-form | 0 | 10/10 | yes, wk-r-18 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/refund-request-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/rental-agreement-form | 0 | 10/10 | yes, wk-r-8 | yes | no | 2 | 6accb96b8570d8ef2122bdea | yes | yes | payload |
| wk-rework-form | /ai-form-builder/rental-application-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/rental-history-form | 15 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/requisition-form | 0 | 10/10 | yes, wk-r-18 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/restaurant-reservation-form | 0 | 10/10 | yes, wk-r-18 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/rfp-form | 6 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/rfq-form | 7 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/service-request-form | 14 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/shipping-address-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/shipping-form | 12 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sign-out-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sign-up-form | 0 | 10/10 | yes, wk-r-11 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/silent-auction-form | 7 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sponsorship-form | 0 | 10/10 | yes, wk-r-18 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/student-registration-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/sublease-form | 20 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/suggestion-form | 8 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/surgery-consent-form | 15 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/tattoo-consent-form | 1 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/telemedicine-consent-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/tenant-screening-form | 0 | 10/10 | no | yes | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/testimonial-form | 12 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/therapy-intake-form | 0 | 10/10 | yes, wk-r-22 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/time-off-request-form | 0 | 10/10 | yes, wk-r-9 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/time-sheet-form | 2 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/tournament-registration-form | 9 | 4/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/training-feedback-form | 0 | 10/10 | yes, wk-r-22 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/training-request-form | 8 | 1/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/travel-reimbursement-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/travel-request-form | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/vehicle-inspection-form | 11 | 0/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/vendor-application | 8 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/volunteer-form | 0 | 10/10 | yes, wk-r-22 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/webinar-registration-form | 10 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/website-design-questionnaire | 9 | 2/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/wedding-photography-contract | 20 | 5/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/wedding-photography-questionnaire | 10 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-form | /ai-form-builder/work-order-form | 0 | 10/10 | yes, wk-r-12 | yes | no | 0 | - | no | no | payload |
| wk-rework-form | /ai-form-builder/workshop-registration-form | 8 | 3/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-lp | /ai-landing-page-builder/app-landing-page | 1 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/b2b-landing-page | 24 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/campaign-landing-page | 1 | 10/10 | yes, wk-r-4 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/coming-soon-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/landing-page-seo | 0 | 10/10 | yes, wk-r-1 | yes | no | 2 | 6accb1fc9cd3f94473f62a84 | yes | yes | payload |
| wk-rework-lp | /ai-landing-page-builder/lead-generation-landing-page | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/one-page-website | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/ppc-landing-page | 1 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/product-landing-page | 2 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/real-estate-landing-page | 1 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/saas-landing-page | 4 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/splash-page | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/squeeze-page | 1 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/360-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/customer-effort-score | 0 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/customer-experience-survey | 2 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/customer-feedback-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 3 | 6accb44a40d5b6e947b7155a | yes | yes | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/employee-benefits-survey | 7 | 6/10 | no | no | no | 0 | - | no | no | stopped (stopped) |
| wk-rework-sqb | /ai-survey-and-quiz-builder/employee-satisfaction-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 1 | 6accb44a40d5b6e947b7155c | yes | yes | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/exit-survey | 0 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/onboarding-survey | 10 | 10/10 | yes, wk-r-7 | yes | no | 0 | - | no | no | payload |
| wk-rework-sqb | /ai-survey-and-quiz-builder/pulse-survey | 0 | 10/10 | yes, wk-r-6 | yes | no | 0 | - | no | no | payload |

Stages: check 4, done 21, images2 1, payload 80, stopped 94 (200 pages)
