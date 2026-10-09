# Readiness board

Regenerated 2026-10-09 22:22 UTC by `hubctl readiness` (also after every `hubctl ship` step). Public: counts and IDs only.

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
| batch-0 | /ai-automation-builder/approval-workflow | 7 | 10/10 | no | no | no | 0 | 6aba7ac40efe4e6ac8693159 | no | no | stopped (stopped) |
| batch-0 | /ai-form-builder/creator-application | 41 | 4/12 | no | no | no | 0 | 6ab505a8d621dc692561a85a | no | no | stopped (stopped) |
| batch-0 | /ai-landing-page-builder/thank-you-page | 5 | 9/10 | no | no | no | 0 | 6ab5158e23395050bc86ca79 | no | no | stopped (stopped) |
| batch-0 | /ai-survey-and-quiz-builder/customer-satisfaction | 9 | 10/10 | no | no | no | 0 | 6aba7afb6271de33629b812c | no | no | stopped (stopped) |
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
| wk-rework-lp | /ai-landing-page-builder/app-landing-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | check2 |
| wk-rework-lp | /ai-landing-page-builder/b2b-landing-page | 0 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | rework |
| wk-rework-lp | /ai-landing-page-builder/campaign-landing-page | 0 | 10/10 | no | yes | no | 0 | - | no | no | images |
| wk-rework-lp | /ai-landing-page-builder/coming-soon-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/landing-page-seo | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/lead-generation-landing-page | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/one-page-website | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/ppc-landing-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | check2 |
| wk-rework-lp | /ai-landing-page-builder/product-landing-page | 0 | 10/10 | yes, wk-r-3 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/real-estate-landing-page | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |
| wk-rework-lp | /ai-landing-page-builder/saas-landing-page | 0 | 10/10 | yes, wk-r-2 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/splash-page | 0 | 10/10 | yes, wk-r-1 | yes | no | 0 | - | no | no | payload |
| wk-rework-lp | /ai-landing-page-builder/squeeze-page | 0 | 10/10 | no | yes | no | 0 | - | no | no | review |

Stages: check2 2, done 21, images 1, payload 7, review 2, rework 1, stopped 8 (42 pages)
