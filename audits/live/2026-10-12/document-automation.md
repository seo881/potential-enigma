# /ai-automation-builder/document-automation: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-document-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-document-automation-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: tab_content_2; images.tab_image_2.alt; image_brief.tabs[1]
- caught by: B-QCA1stocknam (Layer B): The quote tab is built around 'Acme', a stock placeholder company. It sits in the live tab copy, the alt text and the drawn image ('Q-2291 for Acme').
- live text: When the Acme renewal moves to the Proposal stage in HubSpot, its line items fill

## 20261012-document-automation-B-QCA1stocknam-2 (P1, B-QCA1stocknam, proposed)
- field: tab_content_3; image_brief.tabs[2].main.blocks[1].rows[4][1]
- caught by: B-QCA1stocknam (Layer B): The certificate tab names 'Northwind Properties', a stock placeholder company, in the tab copy and the drawn table.
- live text: Vendors upload insurance certificates to Northwind Properties, and the app reads the policy number

## 20261012-document-automation-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, proposed)
- field: tab_content_1; image_brief.tabs[0]; images.tab_image_1.alt
- caught by: B-QCA1reusedpe (Layer B): 'Ana Ruiz' is the most reused persona in the plan (24 other specs). Here it is the attorney in the tab copy, the alt text and the image.
- live text: Ana Ruiz, the responsible attorney, can edit any clause before approving it

## 20261012-document-automation-B-QCA1reusedpe-2 (P1, B-QCA1reusedpe, proposed)
- field: tab_content_4; image_brief.tabs[3]; images.tab_image_4.alt
- caught by: B-QCA1reusedpe (Layer B): The offer-letter tab reuses two personas: 'Sam Okafor' (7 other specs, including purchase-order-automation) and 'Mei Chen' (2 other specs). 'Lumen Studio' also appears on independent-contractor-agreement.
- live text: Sam Okafor's letter carries a $96,000 base salary and goes to Mei Chen, the hiring manager, for approval.

## 20261012-document-automation-B-QCA1reusedpe-3 (P1, B-QCA1reusedpe, proposed)
- field: tab_content_2; image_brief.tabs[1]; images.tab_image_2.alt
- caught by: B-QCA1reusedpe (Layer B): 'Dev Patel', the sales director in the quote tab, is a reused persona (4 other specs).
- live text: Any quote over $25,000 waits for Dev Patel, the sales director, before the rep can send it.

## 20261012-document-automation-B-QCA1reusedpe-4 (P1, B-QCA1reusedpe, proposed)
- field: tab_content_3; image_brief.tabs[2]; images.tab_image_3.alt
- caught by: B-QCA1reusedpe (Layer B): 'Ridgeline' is a reused sample company (9 other specs, among them quote-form, proposal-form, event-landing-page and pricing-page). 'Calder' (tab 1, Calder Law) appears on 2 other specs.
- live text: Ridgeline Roofing's certificate lists $500,000 per occurrence

## 20261012-document-automation-B-HUBRULES8CON-1 (P1, B-HUBRULES8CON, proposed)
- field: faq (item 1)
- caught by: B-HUBRULES8CON (Layer B): The recorded source (Wikipedia) says document automation is 'also known as' document assembly. Calling it the 'older name' goes beyond what the source says.
- live text: The drafting half has an older name: document assembly.

## 20261012-document-automation-B-HUBRULES8CON-2 (P1, B-HUBRULES8CON, proposed)
- field: faq (item 3)
- caught by: B-HUBRULES8CON (Layer B): 'The most common use' is a market-wide fact with no domain_sources entry.
- live text: Reading loan applications, bills of lading, and supplier forms into named fields is the most common use

## 20261012-document-automation-B-HUBRULES5FAQ-1 (P2, B-HUBRULES5FAQ, backlog)
- field: faq (heading)
- caught by: B-HUBRULES5FAQ (Layer B): The FAQ heading drops 'Questions'. Every sibling uses the '{Topic} Questions, Answered' shape.
- live text: Document Automation, Answered

## 20261012-document-automation-B-HUBRULES2bno-1 (P2, B-HUBRULES2bno, backlog)
- field: faq (item 1)
- caught by: B-HUBRULES2bno (Layer B): A rhetorical question sits in the definition answer.
- live text: A quick test for where it pays off: does someone still retype values that already exist in another system?

## 20261012-document-automation-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: faq (item 5)
- caught by: B-CONTENTDEFEC (Layer B): 'usually' is an unsourced generalization about how agreements are handled.
- live text: Once drafted, an agreement usually passes through a contract approval workflow before anyone signs it.

## 20261012-document-automation-B-QCK7HUBRULES-1 (P2, B-QCK7HUBRULES, backlog)
- field: why_table
- caught by: B-QCK7HUBRULES (Layer B): None of the three tabled competitors (Zapier, Make, n8n) ranks in this page's top 10. This is still pending with Divit from the review.
- live text: Zapier | Make (Integromat) | n8n

## 20261012-document-automation-A1-1 (P1, A1, fix-by-writer, fixed)
- field: image_brief
- caught by: A1 (Layer sweep): stock company names live (QC A1, Divit 2026-10-12 ruling)
- cover_image before: Document automation: an engagement letter drafted from a client intake, ready for attorney review
- cover_image after: Document automation: an engagement letter drafted from a client intake, ready for attorney review
- faq before: window.awbFAQ = {"heading": "Document Automation, Answered", "items": [{"q": "What is document automation?", "a": "Document automation is software that produces and handles documents from data and rules instead of by hand. A quick test for where it pays off: does someone still retype values that already exist in another system? The drafting half has an older name: document assembly."}, {"q": "How do you build an automated document workflow?", "a": "Pick one document, find where each of its value
- faq after: window.awbFAQ = {"heading": "Document Automation, Answered", "items": [{"q": "What is document automation?", "a": "Document automation is software that produces and handles documents from data and rules instead of by hand. A quick test for where it pays off: does someone still retype values that already exist in another system? The drafting half is also called document assembly."}, {"q": "How do you build an automated document workflow?", "a": "Pick one document, find where each of its values al
- share_image before: Build document automation for every file in and out, with Emergent
- share_image after: Build document automation for every file in and out, with Emergent
- tab_content_1 before: Turn a client questionnaire into an engagement letter draft Every answer in Calder Law's intake form fills a field in the engagement letter, such as the matter type and the fee basis. Because this matter is litigation, the draft adds the $5,000 retainer clause. Ana Ruiz, the responsible attorney, can edit any clause before approving it, and only the approved version goes out.
- tab_content_1 after: Turn a client questionnaire into an engagement letter draft Every answer in Cottrell Law's intake form fills a field in the engagement letter, such as the matter type and the fee basis. Because this matter is litigation, the draft adds the $5,000 retainer clause. Noor Cresswell, the responsible attorney, can edit any clause before approving it, and only the approved version goes out.
- tab_content_2 before: A priced quote the moment a deal reaches Proposal When the Acme renewal moves to the Proposal stage in HubSpot, its line items are copied into the quote template. That quote, Q-2291, comes to $28,400. Any quote over $25,000 waits for Dev Patel, the sales director, before the rep can send it.
- tab_content_2 after: A priced quote the moment a deal reaches Proposal When the Delmore renewal moves to the Proposal stage in HubSpot, its line items are copied into the quote template. That quote, Q-2291, comes to $28,400. Any quote over $25,000 waits for Dev Cade, the sales director, before the rep can send it.
- tab_content_3 before: Catch an underinsured vendor before the job starts Vendors upload insurance certificates to Northwind Properties, and the app reads the policy number, expiry date, and per-occurrence limit. Ridgeline Roofing's certificate lists $500,000 per occurrence, under its contract's $1,000,000 minimum. The vendor is asked for another, and the job stays on hold until one passes.
- tab_content_3 after: Catch an underinsured vendor before the job starts Vendors upload insurance certificates to Castleby Properties, and the app reads the policy number, expiry date, and per-occurrence limit. Dunholt Roofing's certificate lists $500,000 per occurrence, under its contract's $1,000,000 minimum. The vendor is asked for another, and the job stays on hold until one passes.
- tab_content_4 before: Offer letters that go out once the hiring manager signs off Moving a candidate to Offer in Lumen Studio's hiring tracker fills the offer letter template from the hiring record. Sam Okafor's letter carries a $96,000 base salary and goes to Mei Chen, the hiring manager, for approval. Sam then signs from a link on a phone.
- tab_content_4 after: Offer letters that go out once the hiring manager signs off Moving a candidate to Offer in Coverdale Studio's hiring tracker fills the offer letter template from the hiring record. Sam Corran's letter carries a $96,000 base salary and goes to Mei Durnford, the hiring manager, for approval. Sam then signs from a link on a phone.
- tab_image_1 before: A Calder Law intake form for a litigation matter produces an engagement letter draft with a $5,000 retainer clause, waiting for review by Ana Ruiz, the responsible attorney.
- tab_image_1 after: A Cottrell Law intake form for a litigation matter produces an engagement letter draft with a $5,000 retainer clause, waiting for review by Noor Cresswell, the responsible attorney.
- tab_image_2 before: The Acme renewal reaches Proposal in HubSpot, its line items fill quote Q-2291 for $28,400, and the quote waits for Dev Patel, the sales director, because it is over $25,000.
- tab_image_2 after: The Delmore renewal reaches Proposal in HubSpot, its line items fill quote Q-2291 for $28,400, and the quote waits for Dev Cade, the sales director, because it is over $25,000.
- tab_image_3 before: A certificate of insurance from Ridgeline Roofing is read into fields, and its $500,000 per-occurrence limit falls under the $1,000,000 minimum; the vendor is asked for a new one and the job is held.
- tab_image_3 after: A certificate of insurance from Dunholt Roofing is read into fields, and its $500,000 per-occurrence limit falls under the $1,000,000 minimum; the vendor is asked for a new one and the job is held.
- tab_image_4 before: Sam Okafor signs a Lumen Studio offer letter with a $96,000 base salary from a link on a phone after Mei Chen, the hiring manager, approves it.
- tab_image_4 after: Sam Corran signs a Coverdale Studio offer letter with a $96,000 base salary from a link on a phone after Mei Durnford, the hiring manager, approves it.
