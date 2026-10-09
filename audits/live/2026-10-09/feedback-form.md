# /ai-form-builder/feedback-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-feedback-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-feedback-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-feedback-form-LIB-gforms-build-1 (P1, LIB-gforms-build, fix-by-writer, fixed)
- field: why_table
- caught by: LIB-gforms-build (Layer sweep): Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table
- faq before: window.awbFAQ = {"heading": "Feedback Form Questions, Answered", "items": [{"q": "What is a feedback form?", "a": "A feedback form asks people to rate one experience and say what should change. It usually goes out right after a purchase or an appointment. Most pair a single rating, often 1 to 5 stars, with an optional comment box. The rating shows how it went, and the comment says why."}, {"q": "How do I create a feedback form?", "a": "Pick the decision the answers will inform, then write one ra
- faq after: window.awbFAQ = {"heading": "Feedback Form Questions, Answered", "items": [{"q": "What is a feedback form?", "a": "A feedback form asks people to rate one experience and say what should change. It usually goes out right after a purchase or an appointment. Most pair a single rating, often 1 to 5 stars, with an optional comment box. The rating shows how it went, and the comment says why."}, {"q": "How do I create a feedback form?", "a": "Pick the decision the answers will inform, then write one ra
- mockup before: window.awbMockup = { customerFeedback: "Build a customer feedback form for my online store. Seven days after an order is delivered, email the customer a short form with a 1 to 5 star rating and an optional comment box. If the rating is 2 stars or lower, send our support lead Dana a Slack direct message with the order number, the rating and the comment. Save every answer to the orders database.", openHouseFeedback: "Make an open house feedback form for my real estate listings. Visitors scan a QR 
- mockup after: window.awbMockup = { customerFeedback: "Build a customer feedback form for my online store. Seven days after an order is delivered, email the customer a short form with a 1 to 5 star rating and an optional comment box. If the rating is 2 stars or lower, send our support lead Dana a Slack direct message with the order number, the rating, and the comment. Save every answer to the orders database.", openHouseFeedback: "Make an open house feedback form for my real estate listings. Visitors scan a QR
- why_table before: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Google Forms Typeform How you build Describe it in plain English Templates, editor, AI generator Manual, field by field Templates, editor, AI assist Response limits No response caps Monthly submission caps by plan; the form stops at the cap No limit Monthly response cap
- why_table after: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Google Forms Typeform How you build Describe it in plain English Templates, editor, AI generator Editor, with Gemini drafting on some Workspace plans Templates, editor, AI assist Response limits No response caps Monthly submission caps by plan; the form stops at the cap

## 20261009-feedback-form-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: mockup, faq
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
