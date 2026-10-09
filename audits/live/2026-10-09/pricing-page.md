# /ai-landing-page-builder/pricing-page: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-pricing-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-pricing-page-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-pricing-page-B-GrammarHUBRU-1 (P1, B-GrammarHUBRU, fix-by-writer, fixed)
- field: feature_5
- caught by: B-GrammarHUBRU (Layer B): The example message is run into the sentence with no quotation marks, so it reads as a broken clause.
- live text: Raise a price by sending a message, such as move Team to $32 on March 1.
- faq before: window.awbFAQ = {"heading": "Pricing Page Questions, Answered", "items": [{"q": "What is a pricing page?", "a": "A pricing page is the page on a website that lists what a product or service costs, usually as plans side by side with what each one includes. Most pricing pages also carry a feature comparison grid and a button for each plan."}, {"q": "How to make a pricing page?", "a": "Start from your pricing model, then write each plan's price and billing unit, followed by its top features. Decide
- faq after: window.awbFAQ = {"heading": "Pricing Page Questions, Answered", "items": [{"q": "What is a pricing page?", "a": "A pricing page is the page on a website that lists what a product or service costs, usually as plans side by side with what each one includes. Most pricing pages also carry a feature comparison grid and a button for each plan."}, {"q": "How to make a pricing page?", "a": "Start from your pricing model, then write each plan's price and billing unit, followed by its top features. Decide
- feature_1 before: One card per plan, priced as you sell it List each tier with its price, its billing unit and its top features. Emergent lays out a card per plan, marks the one you recommend and keeps every card the same height.
- feature_1 after: One card per plan, priced as you sell it List each tier with its price, its billing unit, and its top features. Emergent lays out a card per plan, marks the one you recommend, and keeps every card the same height.
- feature_5 before: Price changes made by message Raise a price by sending a message, such as move Team to $32 on March 1. Emergent edits every card and the comparison grid in one change, leaving no stale number on the page.
- feature_5 after: Price changes made by message Raise a price by sending a message, such as "Move Team to $32 on March 1." Emergent edits every card and the comparison grid in one change, leaving no stale number on the page.
- howto_step_5_des before: If yearly billing is cheaper, print the monthly equivalent, the yearly total and the saving on each card. A discount stated only as a percentage leaves visitors working out the real number for themselves, and many will not bother.
- howto_step_5_des after: If yearly billing is cheaper, print the monthly equivalent, the yearly total, and the saving on each card. A discount stated only as a percentage leaves visitors working out the real number for themselves, and many will not bother.
- tab_content_4 before: Which class option is cheapest for how often you come At Ridgeline Yoga, new students rarely know which option suits them. The pricing page lists a $25 drop-in, a 10-class pack for $200 and Unlimited at $140 a month, then asks how many classes a month each visitor plans. Anyone who answers 8 or more sees that Unlimited costs less than the pack.
- tab_content_4 after: Which class option is cheapest for how often you come At Ridgeline Yoga, new students rarely know which option suits them. The pricing page lists a $25 drop-in, a 10-class pack for $200, and Unlimited at $140 a month, then asks how many classes a month each visitor plans. Anyone who answers 8 or more sees that Unlimited costs less than the pack.

## 20261009-pricing-page-B-DECISIONS202-1 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_1
- caught by: B-DECISIONS202 (Layer B): Two three-item lists in one body without the serial comma (body 170 -> 172 chars, within limits).
- live text: List each tier with its price, its billing unit and its top features. Emergent lays out a card per plan, marks the one you recommend and keeps every card the sa

## 20261009-pricing-page-B-DECISIONS202-2 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-DECISIONS202 (Layer B): Three-item price list without the serial comma.
- live text: The pricing page lists a $25 drop-in, a 10-class pack for $200 and Unlimited at $140 a month

## 20261009-pricing-page-B-DECISIONS202-3 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: howto_step_5_des
- caught by: B-DECISIONS202 (Layer B): Three-item list without the serial comma.
- live text: print the monthly equivalent, the yearly total and the saving on each card.

## 20261009-pricing-page-B-DECISIONS202-4 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: faq
- caught by: B-DECISIONS202 (Layer B): FAQ 5 lists three pricing bases without the serial comma.
- live text: Study the ones from companies that charge the way you do, by seat, by usage or by project.

## 20261009-pricing-page-B-DECISIONS202-5 (P2, B-DECISIONS202, backlog)
- field: mockup
- caught by: B-DECISIONS202 (Layer B): Three visible tab prompts drop the serial comma (perSeatSaasTiers, agencyPackages, classMemberships). (mockup prompts are not rendered since the hero redesign; fix at next rework)
- live text: Starter, Team and Business plans | budget, launch timing and project details | a 10-class pack for $200 and an unlimited monthly membership

## 20261009-pricing-page-B-HUBRULES5lig-1 (P2, B-HUBRULES5lig, backlog)
- field: faq
- caught by: B-HUBRULES5lig (Layer B): FAQ 2 question is a searcher fragment rather than a question.
- live text: How to make a pricing page?
