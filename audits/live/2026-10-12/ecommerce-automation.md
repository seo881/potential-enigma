# /ai-automation-builder/ecommerce-automation: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-ecommerce-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-ecommerce-automation-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: tab_content_1; images.tab_image_1.alt; image_brief.tabs[0]
- caught by: B-QCA1stocknam (Layer B): The dropship tab routes order #10482 to 'Northwind Textiles', a stock placeholder company. It appears in the live tab copy, the alt text and the image ('PO to Northwind Textiles', 'Northwind tracking').
- live text: order #10482 becomes a purchase order for Kilnworks and another for Northwind Textiles, each with the ship-to address.

## 20261012-ecommerce-automation-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, proposed)
- field: tab_content_3; mockup; image_brief.tabs[2]
- caught by: B-QCA1reusedpe (Layer B): 'Dana Whitfield' is a heavily reused persona (13 other specs, e.g. contact-form, booking-form, payment-form, nda-form). Here it appears in the tab copy, the mockup prompt and the image.
- live text: Dana Whitfield, the ops lead, gets a Slack direct message with both addresses

## 20261012-ecommerce-automation-B-QCA1reusedpe-2 (P1, B-QCA1reusedpe, proposed)
- field: tab_content_1; image_brief.tabs[0]; images.tab_image_1.alt
- caught by: B-QCA1reusedpe (Layer B): 'Fernhill' is a reused sample brand (15 other specs). 'Fernhill Home' itself also appears on complaint-form.
- live text: Fernhill Home sells through Shopify and holds no stock.

## 20261012-ecommerce-automation-B-QCA1reusedpe-3 (P1, B-QCA1reusedpe, proposed)
- field: image_brief.tabs[1]; images.tab_image_2.alt
- caught by: B-QCA1reusedpe (Layer B): The winback image and its alt reuse 'Priya Nair' (22 other specs) and 'Marcus Bell' (13 other specs).
- live text: Priya Nair gets the COMEBACK10 code for 10% off and the send is logged on her record

## 20261012-ecommerce-automation-B-QCA1reusedpe-4 (P1, B-QCA1reusedpe, proposed)
- field: tab_content_4; mockup; image_brief.tabs[3]
- caught by: B-QCA1reusedpe (Layer B): 'Sam Ortega', the founder in the margin-report tab, also appears on employee-feedback-form.
- live text: the report goes to Sam Ortega, the founder, by email.

## 20261012-ecommerce-automation-B-HUBRULES6cla-1 (P1, B-HUBRULES6cla, fix-by-writer, fixed)
- field: feature_5
- caught by: B-HUBRULES6cla (Layer B): The approved claim is 'no task cap'. 'Never pauses a workflow halfway' promises reliability beyond that claim; store API rate limits are outside Emergent's control.
- live text: There is no task cap, and a flash sale with four times the usual orders never pauses a workflow halfway.
- feature_5 before: No task cap during a sale week Runs every order through the same steps on the busiest day of your year. There is no task cap, and a flash sale with four times the usual orders never pauses a workflow halfway.
- feature_5 after: No task cap during a sale week Runs every order through the same steps on the busiest day of your year. When a flash sale brings in four times the usual orders, there is no task cap for the extra runs to hit.
- share_image before: Build ecommerce automation for the work behind every order, with Emergent
- share_image after: Build ecommerce automation for the work behind every order, with Emergent
- tab_content_1 before: Each paid order goes to the supplier who stocks it Fernhill Home sells through Shopify and holds no stock. When an order is paid, the app splits its lines by supplier: order #10482 becomes a purchase order for Kilnworks and another for Northwind Textiles, each with the ship-to address. The tracking number a supplier enters is written back to the Shopify order.
- tab_content_1 after: Each paid order goes to the supplier who stocks it Fernhill Home sells through Shopify and holds no stock. When an order is paid, the app splits its lines by supplier: order #10482 becomes a purchase order for Kilnworks and another for Bramwell Textiles, each with the ship-to address. The tracking number a supplier enters is written back to the Shopify order.
- tab_image_1 before: Shopify order #10482 at Fernhill Home is split into a purchase order for Kilnworks and one for Northwind Textiles; Kilnworks enters its tracking number on the supplier form and the app saves it to the Shopify order.
- tab_image_1 after: Shopify order #10482 at Fernhill Home is split into a purchase order for Kilnworks and one for Bramwell Textiles; Kilnworks enters its tracking number on the supplier form and the app saves it to the Shopify order.

## 20261012-ecommerce-automation-B-QCK7HUBRULES-1 (P2, B-QCK7HUBRULES, backlog)
- field: why_table
- caught by: B-QCK7HUBRULES (Layer B): n8n does not rank in this page's top 10.
- live text: Zapier | Make (Integromat) | n8n
