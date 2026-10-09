# /ai-form-builder/booking-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-booking-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-booking-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-booking-form-B-HUBRULES8-1 (P1, B-HUBRULES8, fix-by-writer, fixed)
- field: faq#4
- caught by: B-HUBRULES8 (Layer B): The answer contradicts itself: it opens by saying the form fits on one phone screen, then walks through several screens ending with 'the last screen'.
- live text: Most booking forms fit on one phone screen. The customer picks a service, then a calendar opens ... The last screen repeats the date and time back
- faq before: window.awbFAQ = {"heading": "Booking Form Questions, Answered", "items": [{"q": "What is a booking form?", "a": "A booking form is how a customer claims a time or a resource you have a limited supply of. It records the request and the slot they want. A good one offers only times that are still open and turns each request into a confirmed booking."}, {"q": "How do I create a booking form?", "a": "Describe the booking in plain English to Emergent's AI form builder , including how long a slot runs 
- faq after: window.awbFAQ = {"heading": "Booking Form Questions, Answered", "items": [{"q": "What is a booking form?", "a": "A booking form is how a customer claims a time or a resource you have a limited supply of. It records the request and the slot they want. A good one offers only times that are still open and turns each request into a confirmed booking."}, {"q": "How do I create a booking form?", "a": "Describe the booking in plain English to Emergent's AI form builder , including how long a slot runs 

## 20261009-booking-form-B-HUBRULES5-1 (P2, B-HUBRULES5, backlog)
- field: faq#5
- caught by: B-HUBRULES5 (Layer B): The question compares reservation and booking forms, but the answer contrasts reservation with 'appointment form', so the reader never learns where 'booking form' sits.
- live text: A reservation form counts down a fixed stock of seats or rooms until none are left. An appointment form treats each hour of one person's time as a single slot

## 20261009-booking-form-B-HUBRULES5-2 (P2, B-HUBRULES5, backlog)
- field: faq#3
- caught by: B-HUBRULES5 (Layer B): The question keeps the searcher's ungrammatical 'How to ...?' form; HUB_RULES 5 allows a light grammar edit.
- live text: How to write a reservation form?

## 20261009-booking-form-B-HUBRULES5-3 (P2, B-HUBRULES5, backlog)
- field: template
- caught by: B-HUBRULES5 (Layer B): The FAQ heading renders as the template's fixed 'Your Questions, Answered', not the spec heading '{Topic} Questions, Answered'; it is the same on all 20 live pages.
- live text: FREQUENTLY ASKED QUESTIONS Your Questions, Answered
