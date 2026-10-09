# /ai-automation-builder/ecommerce-automation: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-ecommerce-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-ecommerce-automation-A6-uk-1 (P1, A6-uk, fix-by-writer, fixed)
- field: tab_image_4
- caught by: A6-uk (Layer A): UK spelling "grey" (use "gray") in alt text
- live text: grey
- faq before: window.awbFAQ = {"heading": "Store Automation Questions, Answered", "items": [{"q": "What is ecommerce automation?", "a": "Ecommerce automation is software that runs the repeat steps of an online store without someone clicking through them. A store event, such as a paid order or a customer going quiet, triggers a rule. The app then sends the message or holds the order for a person."}, {"q": "How do you build ecommerce automation software?", "a": "Describe one repeat job in Emergent's AI automati
- faq after: window.awbFAQ = {"heading": "Store Automation Questions, Answered", "items": [{"q": "What is ecommerce automation?", "a": "Ecommerce automation is software that runs the repeat steps of an online store without someone clicking through them. A store event, such as a paid order or a customer going quiet, triggers a rule. The app then sends the message or holds the order for a person."}, {"q": "How do you build ecommerce automation software?", "a": "Describe one repeat job in Emergent's AI automati
- feature_1 before: Starts on the store event you pick Connects to Shopify, WooCommerce or BigCommerce through their APIs. A paid order or a new customer signup starts each run, and every run is saved as a row you can search.
- feature_1 after: Starts on the store event you pick Connects to Shopify, WooCommerce, or BigCommerce through their APIs. A paid order or a new customer signup starts each run, and every run is saved as a row you can search.
- howto_step_3_des before: Put every SKU in one sheet with its supplier, the supplier's order inbox and the unit cost. Workflows that route orders or report margin read from this table, and any SKU missing a supplier is flagged for you instead of guessed.
- howto_step_3_des after: Put every SKU in one sheet with its supplier, the supplier's order inbox, and the unit cost. Workflows that route orders or report margin read from this table, and any SKU missing a supplier is flagged for you instead of guessed.
- tab_image_4 before: A Monday margin report lists last week's units, revenue, cost and shipping for four SKUs; the grey linen throw is flagged at 12% margin, under the 20% line, and emailed to founder Sam Ortega.
- tab_image_4 after: A Monday margin report lists last week's units, revenue, cost, and shipping for four SKUs; the gray linen throw is flagged at 12% margin, under the 20% line, and emailed to founder Sam Ortega.

## 20261009-ecommerce-automation-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-ecommerce-automation-B-DECISIONS202-1 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: faq#8
- caught by: B-DECISIONS202 (Layer B): The shipping-automation link was stripped because that page is not live, so "covered under shipping automation" points to a page that does not exist.
- live text: Label buying and carrier choice are their own build, covered under shipping automation.

## 20261009-ecommerce-automation-B-DECISIONS202-2 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_1
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: Connects to Shopify, WooCommerce or BigCommerce through their APIs.

## 20261009-ecommerce-automation-B-DECISIONS202-3 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: howto_step_3_des
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: with its supplier, the supplier's order inbox and the unit cost

## 20261009-ecommerce-automation-B-DECISIONS202-4 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: faq#6
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: A first purchase, an abandoned cart or a birthday month each starts its own sequence.

## 20261009-ecommerce-automation-B-DECISIONS202-5 (P2, B-DECISIONS202, backlog)
- field: mockup
- caught by: B-DECISIONS202 (Layer B): Two lists in the marginReport prompt have no serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- live text: units, revenue, product cost from our SKU table and shipping. Work out margin ..., flag any SKU under 20% and email the table

## 20261009-ecommerce-automation-B-DECISIONS202-6 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: tab_image_4 alt
- caught by: B-DECISIONS202 (Layer B): A list in the alt text has no serial comma (fold this into the pending gray alt fix).
- live text: lists last week's units, revenue, cost and shipping for four SKUs

## 20261009-ecommerce-automation-B-HUBRULES2apr-1 (P2, B-HUBRULES2apr, backlog)
- field: tab_content_3
- caught by: B-HUBRULES2apr (Layer B): The H3 says "the $500 order", but the rule holds orders over $500 and the image shows $742.00.
- live text: Hold the $500 order that ships somewhere new

## 20261009-ecommerce-automation-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: mockup
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
- mockup before: window.awbMockup = { dropshipOrders: "Build dropship order routing for my home goods store on Shopify. When an order is paid, split its lines by supplier using our SKU table and email each supplier a purchase order with only their items and the ship-to address. Give suppliers a form to enter the tracking number and write it back to the Shopify order.", winbackEmails: "Build winback emails for my store. Every morning, find customers whose last order was 90 days ago. If they are still subscribed, 
- mockup after: window.awbMockup = { dropshipOrders: "Build dropship order routing for my home goods store on Shopify. When an order is paid, split its lines by supplier using our SKU table and email each supplier a purchase order with only their items and the ship-to address. Give suppliers a form to enter the tracking number and write it back to the Shopify order.", winbackEmails: "Build winback emails for my store. Every morning, find customers whose last order was 90 days ago. If they are still subscribed, 
