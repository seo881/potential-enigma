# /ai-form-builder/feedback-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-feedback-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-feedback-form-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-QCA1reusedpe (Layer B): Support lead 'Dana Ruiz' is a reused persona (14 other specs); also in the tab 1 alt, cover alt, image brief and mockup ('Dana').
- live text: Direct message to Dana Ruiz / support lead Dana Ruiz gets a direct message with the order and the comment
- cover_image before: Feedback form: a direct message tells support lead Dana Ruiz that order #10482 got a 2-star rating
- cover_image after: Feedback form: a direct message tells support lead Rhea Gentry that order #10482 got a 2-star rating
- mockup before: window.awbMockup = { customerFeedback: "Build a customer feedback form for my online store. Seven days after an order is delivered, email the customer a short form with a 1 to 5 star rating and an optional comment box. If the rating is 2 stars or lower, send our support lead Dana a Slack direct message with the order number, the rating, and the comment. Save every answer to the orders database.", openHouseFeedback: "Make an open house feedback form for my real estate listings. Visitors scan a QR
- mockup after: window.awbMockup = { customerFeedback: "Build a customer feedback form for my online store. Seven days after an order is delivered, email the customer a short form with a 1 to 5 star rating and an optional comment box. If the rating is 2 stars or lower, send our support lead Rhea a Slack direct message with the order number, the rating, and the comment. Save every answer to the orders database.", openHouseFeedback: "Make an open house feedback form for my real estate listings. Visitors scan a QR
- share_image before: Build a feedback form that routes every low rating, with Emergent
- share_image after: Build a feedback form that routes every low rating, with Emergent
- tab_image_1 before: A customer rates order #10482 two of five stars with the comment that the box arrived crushed, and support lead Dana Ruiz gets a direct message with the order and the comment.
- tab_image_1 after: A customer rates order #10482 two of five stars with the comment that the box arrived crushed, and support lead Rhea Gentry gets a direct message with the order and the comment.
- tab_image_2 before: Visitors to the Alder Lane open house answer three questions on their phones, and the seller report shows 7 of 12 visitors found the asking price too high.
- tab_image_2 after: Visitors to the Hawley Lane open house answer three questions on their phones, and the seller report shows 7 of 12 visitors found the asking price too high.
- tab_image_4 before: A patient at the Midtown clinic reports a 45-minute wait, so the visit is flagged to practice manager Leah Park with the patient's comment.
- tab_image_4 after: A patient at the Midtown clinic reports a 45-minute wait, so the visit is flagged to practice manager Leah Galvin with the patient's comment.

## 20261012-feedback-form-B-QCA1reusedpe-2 (P1, B-QCA1reusedpe, proposed)
- field: images.tab_image_4.alt
- caught by: B-QCA1reusedpe (Layer B): Practice manager 'Leah Park' is reused (new-employee-form, address-verification-form) and near-identical to 'Lena Park' used on 6 other pages.
- live text: so the visit is flagged to practice manager Leah Park with the patient's comment.

## 20261012-feedback-form-B-HUBRULES2b-1 (P2, B-HUBRULES2b, backlog)
- field: image_brief tab 1
- caught by: B-HUBRULES2b (Layer B): Order #10482 is the HUB_RULES 2b example number and appears on 8 specs, a repeated stock detail across pages.
- live text: Order #10482 / 2-star rating on #10482

## 20261012-feedback-form-B-HUBRULES2b-2 (P2, B-HUBRULES2b, backlog)
- field: images.tab_image_2.alt
- caught by: B-HUBRULES2b (Layer B): Listing name 'Alder Lane' is reused on 5 other specs.
- live text: Visitors to the Alder Lane open house answer three questions on their phones

## 20261012-feedback-form-B-HUBRULES2b-3 (P2, B-HUBRULES2b, backlog)
- field: tab_content_1
- caught by: B-HUBRULES2b (Layer B): All four tab paragraphs open on a general maxim before the story (templated shape; carried note).
- live text: A 2-star rating is worth more today than in next month's report.
