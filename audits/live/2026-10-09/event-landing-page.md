# /ai-landing-page-builder/event-landing-page: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-event-landing-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-event-landing-page-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-event-landing-page-B-HUBRULES2gra-1 (P1, B-HUBRULES2gra, fix-by-writer, fixed)
- field: howto_step_2_des
- caught by: B-HUBRULES2gra (Layer B): The example subhead is set in running text without quotes, so the sentence does not parse.
- live text: A subhead such as for operations leads at companies with one warehouse sorts the room before anyone registers.
- faq before: window.awbFAQ = {"heading": "Event Page Questions, Answered", "items": [{"q": "What is an event landing page?", "a": "An event landing page is a single page built to get people to one event, such as a conference or a launch party. It gives the date and the venue, makes the case for coming and takes registrations through one form."}, {"q": "How do I build a landing page for an event?", "a": "Decide what each registrant has to tell you, then write down the date and the venue. With Emergent's AI la
- faq after: window.awbFAQ = {"heading": "Event Page Questions, Answered", "items": [{"q": "What is an event landing page?", "a": "An event landing page is a single page built to get people to one event, such as a conference or a launch party. It gives the date and the venue, makes the case for coming and takes registrations through one form."}, {"q": "How do I build a landing page for an event?", "a": "Decide what each registrant has to tell you, then write down the date and the venue. With Emergent's AI la
- howto_step_2_des before: A subhead such as for operations leads at companies with one warehouse sorts the room before anyone registers. Below it, list the sessions or acts with start times. A conference needs the full agenda; a party needs one line about the night.
- howto_step_2_des after: A subhead such as "For operations leads at companies with one warehouse" sorts the room before anyone registers. Below it, list the sessions or acts with start times. A conference needs the full agenda; a party needs one line about the night.

## 20261009-event-landing-page-B-HUBRULES6cla-1 (P1, B-HUBRULES6cla, fix-by-writer, fixed)
- field: faq
- caught by: B-HUBRULES6cla (Layer B): FAQ 4 extends the approved free-tier claim (building and publishing a page) to include the guest list and confirmation emails.
- live text: Emergent's free tier covers building and publishing the page with those pieces included.

## 20261009-event-landing-page-B-HUBRULES2aPr-1 (P2, B-HUBRULES2aPr, backlog)
- field: tab_content_1
- caught by: B-HUBRULES2aPr (Layer B): 72 stands for two different quantities in one sentence (hours and special meals).
- live text: gets an email 72 hours before doors open with the lunch count for the first day: 340 meals, 72 of them special

## 20261009-event-landing-page-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: mockup, faq
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
- faq before: window.awbFAQ = {"heading": "Event Page Questions, Answered", "items": [{"q": "What is an event landing page?", "a": "An event landing page is a single page built to get people to one event, such as a conference or a launch party. It gives the date and the venue, makes the case for coming and takes registrations through one form."}, {"q": "How do I build a landing page for an event?", "a": "Decide what each registrant has to tell you, then write down the date and the venue. With Emergent's AI la
- faq after: window.awbFAQ = {"heading": "Event Page Questions, Answered", "items": [{"q": "What is an event landing page?", "a": "An event landing page is a single page built to get people to one event, such as a conference or a launch party. It gives the date and the venue, makes the case for coming, and takes registrations through one form."}, {"q": "How do I build a landing page for an event?", "a": "Decide what each registrant has to tell you, then write down the date and the venue. With Emergent's AI l
- mockup before: window.awbMockup = { industryConference: "Build a registration page for Ridgeline's two-day operations summit in Portland. Show the dates, the venue address with a directions link and the agenda for each day. Ask every attendee for a name, a work email and one dietary need. Seventy-two hours before doors open, email our venue coordinator the lunch count for the first day, with each dietary type listed and counted.", communityMarket: "My team runs the Harbor Street Night Market. Build a page wher
- mockup after: window.awbMockup = { industryConference: "Build a registration page for Ridgeline's two-day operations summit in Portland. Show the dates, the venue address with a directions link, and the agenda for each day. Ask every attendee for a name, a work email, and one dietary need. Seventy-two hours before doors open, email our venue coordinator the lunch count for the first day, with each dietary type listed and counted.", communityMarket: "My team runs the Harbor Street Night Market. Build a page wh
