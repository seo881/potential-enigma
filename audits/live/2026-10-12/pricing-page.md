# /ai-landing-page-builder/pricing-page: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-pricing-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-pricing-page-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): The "More things you can build" AI CRM Builder card draws the stock placeholder company "Acme Corp", now a listed AI tell; the card is a sitewide component outside the child collections.
- live text: AI CRM Builder card: AC Acme Corp $24,000 Proposal

## 20261012-pricing-page-B-CONTENTDEFEC-1 (P1, B-CONTENTDEFEC, proposed)
- field: template
- caught by: B-CONTENTDEFEC (Layer B): The AI Schedule Builder card in "More things you can build" shows "Thursday, Oct 16", but 16 October 2026 is a Friday; it is a sitewide component outside the child collections.
- live text: Thursday, Oct 16 9:30 Team standup 1:30 Demo call Booked

## 20261012-pricing-page-B-HUBRULES5com-1 (P1, B-HUBRULES5com, fix-by-writer, fixed)
- field: why_table
- caught by: B-HUBRULES5com (Layer B): The Wix "Where submissions go" cell understates Wix: Wix Forms keeps submissions in the site dashboard with export, not only an email. The library fact (lp.json Wix.data, 2026-09-28) cites only "vendor pricing page".
- live text: Where submissions go | ... | Wix: Basic contact form to email
- share_image before: Build a pricing page where the numbers add up, with Emergent
- share_image after: Build a pricing page where the numbers add up, with Emergent
- tab_content_1 before: Thirty dollars per seat, twenty-five when billed yearly Fernway prices its tiers per user and recommends Team. The switch on the page opens on annual billing, where Team reads $25 per user a month, billed as $300 a year, against $30 on monthly billing. The Team card states the yearly saving of $60 per user. Every plan click is saved with the billing period chosen.
- tab_content_1 after: Thirty dollars per seat, twenty-five when billed yearly Pacelane prices its tiers per user and recommends Team. The switch on the page opens on annual billing, where Team reads $25 per user a month, billed as $300 a year, against $30 on monthly billing. The Team card states the yearly saving of $60 per user. Every plan click is saved with the billing period chosen.
- tab_content_3 before: Two set packages, with quotes for everything else Some work has no list price. Halden Studio shows a Brand Sprint at $4,500 and a Website build at $12,000, with a Custom card beside them. Custom opens a short quote form asking for a budget and a launch window. Each request is saved as a row and posted to the studio's #new-business channel in Slack.
- tab_content_3 after: Two set packages, with quotes for everything else Some work has no list price. Rennick Studio shows a Brand Sprint at $4,500 and a Website build at $12,000, with a Custom card beside them. Custom opens a short quote form asking for a budget and a launch window. Each request is saved as a row and posted to the studio's #new-business channel in Slack.
- tab_content_4 before: Which class option is cheapest for how often you come At Ridgeline Yoga, new students rarely know which option suits them. The pricing page lists a $25 drop-in, a 10-class pack for $200, and Unlimited at $140 a month, then asks how many classes a month each visitor plans. Anyone who answers 8 or more sees that Unlimited costs less than the pack.
- tab_content_4 after: Which class option is cheapest for how often you come At Quietwater Yoga, new students rarely know which option suits them. The pricing page lists a $25 drop-in, a 10-class pack for $200, and Unlimited at $140 a month, then asks how many classes a month each visitor plans. Anyone who answers 8 or more sees that Unlimited costs less than the pack.
- tab_image_1 before: Fernway's pricing page on annual billing shows Team at $25 per user a month, billed as $300 a year, a saving of $60 per user against $30 on monthly billing.
- tab_image_1 after: Pacelane's pricing page on annual billing shows Team at $25 per user a month, billed as $300 a year, a saving of $60 per user against $30 on monthly billing.
- tab_image_3 before: Halden Studio's Custom card opens a quote form, and the request is saved and posted to the #new-business Slack channel with an $8,000 budget and a 10-week launch.
- tab_image_3 after: Rennick Studio's Custom card opens a quote form, and the request is saved and posted to the #new-business Slack channel with an $8,000 budget and a 10-week launch.
- tab_image_4 before: Ridgeline Yoga's pricing page compares a $25 drop-in, a $200 10-class pack and $140 Unlimited, and shows that at 8 classes a month Unlimited costs less than the pack.
- tab_image_4 after: Quietwater Yoga's pricing page compares a $25 drop-in, a $200 10-class pack and $140 Unlimited, and shows that at 8 classes a month Unlimited costs less than the pack.

## 20261012-pricing-page-B-HUBRULES5lay-1 (P1, B-HUBRULES5lay, proposed)
- field: template
- caught by: B-HUBRULES5lay (Layer B): At 390 px the default-open first FAQ panel is one line too short, so the last word of the answer ("plan.") is cut off.
- live text: Most pricing pages also carry a feature comparison grid and a button for each

## 20261012-pricing-page-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-QCA1reusedpe (Layer B): "Fernway" is reused in 9 other specs (saas-, b2b-, lead-generation-landing-page, coming-soon-page and more).
- live text: Fernway prices its tiers per user and recommends Team.

## 20261012-pricing-page-B-QCA1reusedpe-2 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_3
- caught by: B-QCA1reusedpe (Layer B): "Halden" is reused in 8 other specs (ppc-landing-page, product-landing-page, coming-soon-page and more).
- live text: Halden Studio shows a Brand Sprint at $4,500 and a Website build at $12,000, with a Custom card beside them.

## 20261012-pricing-page-B-QCA1reusedpe-3 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-QCA1reusedpe (Layer B): "Ridgeline" is reused in 9 other specs (event-, ppc- and product-landing-page, quote-form and more).
- live text: At Ridgeline Yoga, new students rarely know which option suits them.

## 20261012-pricing-page-B-HUBRULES5FAQ-1 (P1, B-HUBRULES5FAQ, proposed)
- field: faq (item 2)
- caught by: B-HUBRULES5FAQ (Layer B): The question is an ungrammatical fragment. Sibling pages phrase this item as "How do you ...?", and HUB_RULES 5 allows light grammar edits to PAA phrasing.
- live text: How to make a pricing page?

## 20261012-pricing-page-B-HUBRULES5pro-1 (P2, B-HUBRULES5pro, backlog)
- field: meta_description
- caught by: B-HUBRULES5pro (Layer B): The page promises "working" examples, but the four tabs are illustrated scenarios for invented companies with nothing a visitor can open. The usecase_heading repeats this ("Four Working Pages").
- live text: See four working examples by pricing model and build yours from a prompt.

## 20261012-pricing-page-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: feature_5
- caught by: B-CONTENTDEFEC (Layer B): The example message sets a future effective date ("on March 1"), but the next sentence says Emergent makes the edit at once, which reads as scheduling Emergent does not claim.
- live text: Raise a price by sending a message, such as "Move Team to $32 on March 1." Emergent edits every card and the comparison grid in one change

## 20261012-pricing-page-B-CONTENTDEFEC-3 (P2, B-CONTENTDEFEC, backlog)
- field: howto_step_2_des / howto_step_4_des / howto_step_5_des
- caught by: B-CONTENTDEFEC (Layer B): Visitor behaviour is stated as fact with no source in three steps: step 2 "visitors start comparing columns", step 4 "Visitors who cannot decide take the default", step 5 "many will not bother".
- live text: Past that, visitors start comparing columns instead of choosing one. | Visitors who cannot decide take the default.
