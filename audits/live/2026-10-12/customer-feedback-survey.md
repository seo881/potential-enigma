# /ai-survey-and-quiz-builder/customer-feedback-survey: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-customer-feedback-survey-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-customer-feedback-survey-B-DECISIONSser-1 (P1, B-DECISIONSser, fix-by-writer, fixed)
- field: meta_description
- caught by: B-DECISIONSser (Layer B): A three-item list is missing its serial comma.
- live text: sorts comments by theme, saves each answer with its customer and routes complaints to an owner.
- meta_description before: Build a customer feedback survey that sorts comments by theme, saves each answer with its customer and routes complaints to an owner.
- meta_description after: Build a customer feedback survey that sorts comments by theme, saves each answer with its customer, and routes complaints to an owner.
- mockup before: window.awbMockup = { cancellationSurvey: "Build a cancellation survey for my coffee subscription. When Stripe reports a canceled subscription, email the subscriber three questions: the main reason, picked from a list, what would bring them back, and an open box for anything else. Save each answer with the plan and how many months they subscribed. Show a dashboard of reasons over the last 30 days with the number who answered.", inAppFeedback: "Add a feedback button to every screen of my web app. 
- mockup after: window.awbMockup = { cancellationSurvey: "Build a cancellation survey for my coffee subscription. When Stripe reports a canceled subscription, email the subscriber three questions: the main reason, picked from a list, what would bring them back, and an open box for anything else. Save each answer with the plan and how many months they subscribed. Show a dashboard of reasons over the last 30 days with the number who answered.", inAppFeedback: "Add a feedback button to every screen of my web app. 
- tab_content_1 before: Find out why subscribers cancel Once Stripe reports a canceled subscription, the subscriber gets a three-question email: the main reason, what would bring them back and anything else. Each answer is saved with the plan and months subscribed. Over 30 days, 112 of 160 canceling subscribers answered, and price led with 41.
- tab_content_1 after: Find out why subscribers cancel Once Stripe reports a canceled subscription, the subscriber gets a three-question email: the main reason, what would bring them back, and anything else. Each answer is saved with the plan and months subscribed. Over 30 days, 112 of 160 canceling subscribers answered, and price led with 41.
- tab_content_3 before: A text after every repair visit Two hours after the technician closes the job, the customer gets a text through Twilio. It asks for a star rating, whether the tech arrived in the booked window and what went wrong, if anything. A rating of 2 or lower becomes a callback task for the dispatcher, with the job number and the comment.
- tab_content_3 after: A text after every repair visit Two hours after the technician closes the job, the customer gets a text through Twilio. It asks for a star rating, whether the tech arrived in the booked window, and what went wrong, if anything. A rating of 2 or lower becomes a callback task for the dispatcher, with the job number and the comment.
- tab_image_2 before: In-app comments are saved with their page and plan and tagged as a bug, idea, question or praise; a CSV export bug reported 9 times this week is posted to the product team's Slack channel.
- tab_image_2 after: In-app comments are saved with their page and plan and tagged as a bug, idea, question, or praise; a CSV export bug reported 9 times this week is posted to the product team's Slack channel.

## 20261012-customer-feedback-survey-B-DECISIONSser-2 (P1, B-DECISIONSser, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-DECISIONSser (Layer B): A three-item list is missing its serial comma.
- live text: the main reason, what would bring them back and anything else.

## 20261012-customer-feedback-survey-B-DECISIONSser-3 (P1, B-DECISIONSser, fix-by-writer, fixed)
- field: tab_content_3
- caught by: B-DECISIONSser (Layer B): A three-item list is missing its serial comma (the same sentence repeats in the serviceVisit mockup).
- live text: It asks for a star rating, whether the tech arrived in the booked window and what went wrong, if anything.

## 20261012-customer-feedback-survey-B-DECISIONSser-4 (P1, B-DECISIONSser, proposed)
- field: mockup
- caught by: B-DECISIONSser (Layer B): Two lists in the mockup prompts drop the serial comma, while tab 2 uses it, so the page mixes both styles.
- live text: inAppFeedback: "Save each comment with the page, the account's plan and the browser"; serviceVisit: "...in the booked window and what went wrong"

## 20261012-customer-feedback-survey-B-DECISIONSser-5 (P1, B-DECISIONSser, proposed)
- field: tab_image_2 alt
- caught by: B-DECISIONSser (Layer B): The alt text list drops the serial comma that tab 2's copy uses for the same four tags.
- live text: tagged as a bug, idea, question or praise

## 20261012-customer-feedback-survey-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): The sitewide 'More things you can build' AI CRM Builder card image draws the stock placeholder company 'Acme Corp'; one component fix covers every page.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-customer-feedback-survey-B-HUBRULES2b-1 (P2, B-HUBRULES2b, backlog)
- field: faq
- caught by: B-HUBRULES2b (Layer B): FAQ 4 forces the secondary into a stilted sentence that reads as keyword placement.
- live text: Start these survey questions for customers with a rating of the delivery, then ask for the main reason behind it.

## 20261012-customer-feedback-survey-B-HUBRULES6-1 (P2, B-HUBRULES6, backlog)
- field: faq
- caught by: B-HUBRULES6 (Layer B): FAQ 6 answers 'Yes' to a template question, then 'Start from either one' reads as if Emergent ships a template library, which the ledger does not claim.
- live text: Yes. A post-onboarding check-in and a delivery survey are two common first drafts. Start from either one,

## 20261012-customer-feedback-survey-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: prompt_chip_2
- caught by: B-CONTENTDEFEC (Layer B): The hero chip uses 'Exit Survey', the primary of the sibling page /exit-survey; the tab on this page is 'Cancellation Survey'.
- live text: Exit Survey

## 20261012-customer-feedback-survey-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: tab_image_1
- caught by: B-CONTENTDEFEC (Layer B): The reason bar labelled 'Too much' does not say too much of what, so the second-largest reason can't be read.
- live text: Price 41 / Too much 33 / Other 21 / Taste 17
