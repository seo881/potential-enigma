# /ai-form-builder/order-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-order-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-order-form-B-QCA1Divit202-1 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The testimonial strip credits quotes to stock AI persona names (Alex Rivera, Maya Chen, Jordan Patel) at made-up-sounding companies, identical on every hub page; if these are not real customers the quotes are fabricated.
- live text: We saved over $10K and built a functional MVP in just days... Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founde...

## 20261012-order-form-B-HUBRULES2apu-1 (P1, B-HUBRULES2apu, proposed)
- field: template
- caught by: B-HUBRULES2apu (Layer B): The third testimonial quote has no closing full stop, unlike the other two.
- live text: We tested our idea with real users early and used that feedback to avoid building features no one needed

## 20261012-order-form-B-QCA1Divit202-2 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The AI CRM Builder card image in "More things you can build" draws the stock company name Acme Corp.
- live text: Lead / Proposal / Won ... AC Acme Corp $24,000 Proposal

## 20261012-order-form-B-HUBRULES2bai-1 (P2, B-HUBRULES2bai, backlog)
- field: template
- caught by: B-HUBRULES2bai (Layer B): The pricing block uses AI-tell and hype phrasing (unlock, elegant, we've got you covered) and "we", which the child copy bans.
- live text: Choose the plan that fits your building ambitions. From weekend projects to enterprise applications, we've got you covered. ... Unlock all core platform feat...

## 20261012-order-form-B-Brieflayoutb-1 (P1, B-Brieflayoutb, proposed)
- field: template
- caught by: B-Brieflayoutb (Layer B): At 390 px the open first FAQ item clips its last line: the answer ends at "long email" and "threads." is hidden (desktop shows it). Verify on a device; may be an accordion height set before fonts load.
- live text: Businesses use order forms to take orders without phone calls or long email

## 20261012-order-form-B-HUBRULES2agr-1 (P1, B-HUBRULES2agr, fix-by-writer, fixed)
- field: howto_step_2_des
- caught by: B-HUBRULES2agr (Layer B): A comma splits the either/or pair: "either a delivery address, or a pickup time".
- live text: They need a name, a phone number and either a delivery address, or a pickup time.
- howto_step_2_des before: Picture the order from the packer's side. They need a name, a phone number and either a delivery address, or a pickup time. Questions beyond that, like a birthday for marketing, belong on a later form or nowhere.
- howto_step_2_des after: Picture the order from the packer's side. They need a name, a phone number, and either a delivery address or a pickup time. Questions beyond that, like a birthday for marketing, belong on a later form or nowhere.
- tab_image_3 before: A signed software order form for 40 seats at $45 per seat per month on a 12-month term totals $21,600, and finance gets an email to invoice from the start date.
- tab_image_3 after: A signed software order form for 40 seats at $45 per seat per month on a 12-month term totals $21,600, and finance gets an email to invoice from the start date.

## 20261012-order-form-B-QCA1Divit202-3 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_image_3
- caught by: B-QCA1Divit202 (Layer B): The buyer company in the tab 3 image, Brightline Logistics, is reused across 16 specs and is already live on data-entry-automation and booking-form.
- live text: Order form: Brightline Logistics / Under the master agreement / Ezra Pennock, Brightline Logistics, buyer

## 20261012-order-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: tab_image_4
- caught by: B-CONTENTDEFEC (Layer B): The tab 4 image says "Delivery: Studio pickup" for the Ellis order while the hero pill says "Lab prints and ships"; the copy is silent, but the image tells two outcomes.
- live text: Delivery: Studio pickup ... Ellis family, studio pickup ... Lab prints and ships

## 20261012-order-form-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: why_description
- caught by: B-CONTENTDEFEC (Layer B): The description sets Emergent against "template sites", but the table compares Jotform, SurveyMonkey and AidaForm, form builders that do not deliver orders as PDFs typed into a spreadsheet.
- live text: Template sites hand you a layout. Each order still arrives as a PDF or an email that someone types into a spreadsheet.

## 20261012-order-form-B-HUBRULES2b-1 (P2, B-HUBRULES2b, backlog)
- field: feature_6
- caught by: B-HUBRULES2b (Layer B): "included and paid in credits" reads as a contradiction (included, yet paid) and the same formula sits in feature 6 of the registration and rental pages.
- live text: Publish the order form on a custom domain, included and paid in credits, or embed it on your site.

## 20261012-order-form-B-CONTENTDEFEC-3 (P2, B-CONTENTDEFEC, backlog)
- field: usecase_heading
- caught by: B-CONTENTDEFEC (Layer B): The "X Forms for Four Kinds of Y" heading shape is used in 27 specs, including the live registration-form page.
- live text: Order Forms for Four Kinds of Sellers
