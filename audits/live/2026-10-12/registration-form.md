# /ai-form-builder/registration-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-registration-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-registration-form-B-QCA1Divit202-1 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The testimonial strip credits quotes to stock AI persona names (Alex Rivera, Maya Chen, Jordan Patel) at made-up-sounding companies, identical on every hub page; if these are not real customers the quotes are fabricated.
- live text: We saved over $10K and built a functional MVP in just days... Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founde...

## 20261012-registration-form-B-HUBRULES2apu-1 (P1, B-HUBRULES2apu, proposed)
- field: template
- caught by: B-HUBRULES2apu (Layer B): The third testimonial quote has no closing full stop, unlike the other two.
- live text: We tested our idea with real users early and used that feedback to avoid building features no one needed

## 20261012-registration-form-B-QCA1Divit202-2 (P1, B-QCA1Divit202, proposed)
- field: template
- caught by: B-QCA1Divit202 (Layer B): The AI CRM Builder card image in "More things you can build" draws the stock company name Acme Corp.
- live text: Lead / Proposal / Won ... AC Acme Corp $24,000 Proposal

## 20261012-registration-form-B-HUBRULES2bai-1 (P2, B-HUBRULES2bai, backlog)
- field: template
- caught by: B-HUBRULES2bai (Layer B): The pricing block uses AI-tell and hype phrasing (unlock, elegant, we've got you covered) and "we", which the child copy bans.
- live text: Choose the plan that fits your building ambitions. From weekend projects to enterprise applications, we've got you covered. ... Unlock all core platform feat...

## 20261012-registration-form-B-QCA1Divit202-3 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_image_3
- caught by: B-QCA1Divit202 (Layer B): The tab 3 vendor table draws four stock company names, and the hero card and alt text name one of them.
- live text: Northwind Bakery / Globex Kitchen / Initech Pottery / Acme Prints; hero "Globex Kitchen held"; alt "...holds Globex Kitchen because its health permit runs ou...
- mockup before: window.awbMockup = { paidEvents: "I run Harbor Food Bank and need a registration form for our spring dinner. We have 180 seats at $85 each. Guests pick a meal and pay through Stripe Checkout, and a seat counts only once payment clears. When the last seat sells, switch the form to a waitlist, and email the first person on it whenever someone cancels.", productWarranties: "Build a product registration form for our Kestrel coffee grinder. Buyers enter the serial number and upload a photo of their r
- mockup after: window.awbMockup = { paidEvents: "I run Harbor Food Bank and need a registration form for our spring dinner. We have 180 seats at $85 each. Guests pick a meal and pay through Stripe Checkout, and a seat counts only once payment clears. When the last seat sells, switch the form to a waitlist, and email the first person on it whenever someone cancels.", productWarranties: "Build a product registration form for our Kinross coffee grinder. Buyers enter the serial number and upload a photo of their r
- share_image before: Build a registration form with fees, caps, and a waitlist, with Emergent
- share_image after: Build a registration form with fees, caps, and a waitlist, with Emergent
- tab_content_2 before: A warranty date read straight off the receipt Buyers of the Kestrel grinder register it with the serial number and a photo of the receipt. The form reads the purchase date off the photo, adds two years, and saves the warranty end date to the buyer's contact in HubSpot. A receipt it cannot read goes to the support queue for a person to check.
- tab_content_2 after: A warranty date read straight off the receipt Buyers of the Kinross grinder register it with the serial number and a photo of the receipt. The form reads the purchase date off the photo, adds two years, and saves the warranty end date to the buyer's contact in HubSpot. A receipt it cannot read goes to the support queue for a person to check.
- tab_image_2 before: A Kestrel grinder receipt photo is read for its serial number and purchase date of Mar 14, 2026, and the warranty end date of Mar 14, 2028 is saved to the buyer's HubSpot contact.
- tab_image_2 after: A Kinross grinder receipt photo is read for its serial number and purchase date of Mar 14, 2026, and the warranty end date of Mar 14, 2028 is saved to the buyer's HubSpot contact.
- tab_image_3 before: A vendor table for the Riverside Saturday market holds Globex Kitchen because its health permit runs out before market day, while craft and art vendors go to booth assignment.
- tab_image_3 after: A vendor table for the Riverside Saturday market holds Jasper Kitchen because its health permit runs out before market day, while craft and art vendors go to booth assignment.
- tab_image_4 before: A plot table for Elm Street Garden shows 52 registrations for 40 plots, returning gardeners placed in week 1 and 12 newcomers on a waitlist ranked by registration time.
- tab_image_4 after: A plot table for Elm Street Garden shows 52 registrations for 40 plots, returning gardeners placed in week 1 and 12 newcomers on a waitlist ranked by registration time.

## 20261012-registration-form-B-QCA1Divit202-4 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1Divit202 (Layer B): The product name Kestrel is reused across 15 specs and is already live on 5 other pages; it appears in the tab copy, the mockup prompt and the tab 2 image and alt.
- live text: Buyers of the Kestrel grinder register it with the serial number and a photo of the receipt.

## 20261012-registration-form-B-QCA1Divit202-5 (P1, B-QCA1Divit202, fix-by-writer, fixed)
- field: tab_image_4
- caught by: B-QCA1Divit202 (Layer B): The gardener "D. Okafor" reuses a surname found in 38 specs and on 8 other live pages.
- live text: GARDENER STATUS ... D. Okafor Returning Week 1 B-07

## 20261012-registration-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: tab_image_3
- caught by: B-CONTENTDEFEC (Layer B): Inside the tab 3 image the table and meta say the permit is "Expired" while the hero says it "Expires before market day"; two different states.
- live text: Globex Kitchen Food Expired Held ... Expires before market day / Health permit: expired

## 20261012-registration-form-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: tab_image_2
- caught by: B-CONTENTDEFEC (Layer B): The copy and mockup have the buyer enter the serial number, but the image and alt read it off the receipt photo.
- live text: Buyers enter the serial number and upload a photo of their receipt. / alt: receipt photo is read for its serial number and purchase date

## 20261012-registration-form-B-HUBRULES2b-1 (P2, B-HUBRULES2b, backlog)
- field: howto_step_2_des
- caught by: B-HUBRULES2b (Layer B): A question in body copy.
- live text: Then decide what happens when a cap is reached: does the form close or switch to a waitlist?

## 20261012-registration-form-B-QCA1reusedna-1 (P2, B-QCA1reusedna, backlog)
- field: tab_content_3
- caught by: B-QCA1reusedna (Layer B): "Riverside" as the market name recurs in 19 specs and is live on booking-form and t-shirt-order-form.
- live text: Every vendor at the Riverside Saturday market registers for a booth and pays the booth fee.

## 20261012-registration-form-B-HUBRULES2b-2 (P2, B-HUBRULES2b, backlog)
- field: feature_6
- caught by: B-HUBRULES2b (Layer B): Same "included and paid for with credits" formula as the order and rental pages; reads as included yet paid.
- live text: Put the form on a custom domain, included and paid for with credits, or embed it on a site you already run.

## 20261012-registration-form-B-CONTENTDEFEC-3 (P2, B-CONTENTDEFEC, backlog)
- field: usecase_heading
- caught by: B-CONTENTDEFEC (Layer B): The "X Forms for Four Kinds of Y" heading shape is shared with the live order-form page and 25 other specs.
- live text: Registration Forms for Four Kinds of Lists
