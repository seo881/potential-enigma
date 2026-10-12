# /ai-landing-page-builder/law-firm-landing-page: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-law-firm-landing-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-law-firm-landing-page-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): The "More things you can build" AI CRM Builder card draws the stock placeholder company "Acme Corp", now a listed AI tell; the card is a sitewide component outside the child collections.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-law-firm-landing-page-B-CONTENTDEFEC-1 (P1, B-CONTENTDEFEC, proposed)
- field: template
- caught by: B-CONTENTDEFEC (Layer B): The AI Schedule Builder card in "More things you can build" shows "Thursday, Oct 16", but 16 October 2026 is a Friday; it is a sitewide component outside the child collections.
- live text: Thursday, Oct 16 9:30 Team standup 1:30 Demo call Booked

## 20261012-law-firm-landing-page-B-HUBRULES5com-1 (P1, B-HUBRULES5com, fix-by-writer, fixed)
- field: why_table
- caught by: B-HUBRULES5com (Layer B): The Wix "Where submissions go" cell understates Wix: Wix Forms keeps submissions in the site dashboard with export, not only an email. The library fact (lp.json Wix.data, 2026-09-28) cites only "vendor pricing page".
- live text: Where submissions go | ... | Wix: Basic contact form to email
- mockup before: window.awbMockup = { injuryCaseReview: "Build a free case review page for my firm, Marlow Injury Law, for people hurt in car crashes. Ask whether they were injured, which county the crash happened in and whether a lawyer already represents them. Send anyone injured with no lawyer to our intake manager, Ellen Park, as a Slack direct message with the county. Show everyone else a polite note.", divorceConsults: "Build a consultation page for Bellweather Family Law. Before showing the calendar, ask 
- mockup after: window.awbMockup = { injuryCaseReview: "Build a free case review page for my firm, Pendry Injury Law, for people hurt in car crashes. Ask whether they were injured, which county the crash happened in and whether a lawyer already represents them. Send anyone injured with no lawyer to our intake manager, Ellen Pyke, as a Slack direct message with the county. Show everyone else a polite note.", divorceConsults: "Build a consultation page for Quarrie Family Law. Before showing the calendar, ask for 
- share_image before: Build a law firm landing page for every practice area, with Emergent
- share_image after: Build a law firm landing page for every practice area, with Emergent
- tab_content_1 before: Injured callers with no lawyer go straight to intake Crash victims on Marlow Injury Law's free case review page say whether they were hurt and whether a lawyer already represents them. Anyone injured with no lawyer reaches intake manager Ellen Park as a Slack direct message, with the crash county attached. Represented visitors see a polite note instead.
- tab_content_1 after: Injured callers with no lawyer go straight to intake Crash victims on Pendry Injury Law's free case review page say whether they were hurt and whether a lawyer already represents them. Anyone injured with no lawyer reaches intake manager Ellen Pyke as a Slack direct message, with the crash county attached. Represented visitors see a polite note instead.
- tab_content_2 before: No consult booked until the conflict check clears Before anyone books, Bellweather Family Law's consultation page asks for the visitor's name and the spouse's full name. Both run against the firm's client list. A clean result opens the calendar. A match holds the request for the conflicts clerk, Ruth Abara, before the visitor has written a word about the marriage.
- tab_content_2 after: No consult booked until the conflict check clears Before anyone books, Quarrie Family Law's consultation page asks for the visitor's name and the spouse's full name. Both run against the firm's client list. A clean result opens the calendar. A match holds the request for the conflicts clerk, Ruth Abara, before the visitor has written a word about the marriage.
- tab_content_3 before: Which estate plan fits, answered in five questions Two flat fees head Juniper Estate Law's page: $950 for a will package and $2,400 for a revocable living trust. A visitor answers five questions, and the page recommends a package by the firm's own rule, such as the trust for homeowners. The lead lands in the Clio Grow lead inbox with that package attached.
- tab_content_3 after: Which estate plan fits, answered in five questions Two flat fees head Rothwell Estate Law's page: $950 for a will package and $2,400 for a revocable living trust. A visitor answers five questions, and the page recommends a package by the firm's own rule, such as the trust for homeowners. The lead lands in the Clio Grow lead inbox with that package attached.
- tab_content_4 before: After-hours DUI inquiries for the attorney on call Dorsey Defense points its Google Ads at a DUI page with a short form and the firm's phone number. Inquiries that arrive after 6 PM go straight to Nina Holt, the attorney on call, in a Slack message that includes the ad keyword behind the click. Daytime inquiries go to the intake desk.
- tab_content_4 after: After-hours DUI inquiries for the attorney on call Dorsey Defense points its Google Ads at a DUI page with a short form and the firm's phone number. Inquiries that arrive after 6 PM go straight to Nina Quist, the attorney on call, in a Slack message that includes the ad keyword behind the click. Daytime inquiries go to the intake desk.
- tab_image_1 before: Marlow Injury Law's case review requests are sorted by injury and representation, and intake manager Ellen Park gets a Slack direct message for an injured visitor in Ashby County with no lawyer.
- tab_image_1 after: Pendry Injury Law's case review requests are sorted by injury and representation, and intake manager Ellen Pyke gets a Slack direct message for an injured visitor in Ashby County with no lawyer.
- tab_image_2 before: Bellweather Family Law's consultation page checks the spouse's full name against the client list, finds a match, and holds the booking for conflicts clerk Ruth Abara before any case details are asked.
- tab_image_2 after: Quarrie Family Law's consultation page checks the spouse's full name against the client list, finds a match and holds the booking for conflicts clerk Ruth Abara before any case details are asked.
- tab_image_3 before: Juniper Estate Law's page lists a $950 will package and a $2,400 revocable living trust, recommends the trust after five answers, and sends the lead to the Clio Grow lead inbox.
- tab_image_3 after: Rothwell Estate Law's page lists a $950 will package and a $2,400 revocable living trust, recommends the trust after five answers and sends the lead to the Clio Grow lead inbox.
- tab_image_4 before: Dorsey Defense's DUI page logs each inquiry with its ad keyword, and an inquiry at 9:02 PM goes to on-call attorney Nina Holt as a Slack direct message.
- tab_image_4 after: Dorsey Defense's DUI page logs each inquiry with its ad keyword, and an inquiry at 9:02 PM goes to on-call attorney Nina Quist as a Slack direct message.

## 20261012-law-firm-landing-page-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-QCA1reusedpe (Layer B): "Marlow" is reused as a company name in 10 other specs (sales-automation, interest-form, quote-form, product-landing-page and more).
- live text: Crash victims on Marlow Injury Law's free case review page say whether they were hurt

## 20261012-law-firm-landing-page-B-QCA1reusedpe-2 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_3
- caught by: B-QCA1reusedpe (Layer B): "Juniper" is reused as a company name in 19 other specs (one-page-website, squeeze-page, massage-intake-form and more).
- live text: Two flat fees head Juniper Estate Law's page: $950 for a will package and $2,400 for a revocable living trust.

## 20261012-law-firm-landing-page-B-QCA1reusedpe-3 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1reusedpe (Layer B): "Bellweather" also appears in equipment-rental-agreement-form.
- live text: Before anyone books, Bellweather Family Law's consultation page asks for the visitor's name and the spouse's full name.

## 20261012-law-firm-landing-page-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: faq (item 1)
- caught by: B-CONTENTDEFEC (Layer B): This is an absolute generalization: many law firm landing pages keep a slim header, so "no site menu" is advice, not a definition.
- live text: It has no site menu, and its form feeds the firm's intake.
