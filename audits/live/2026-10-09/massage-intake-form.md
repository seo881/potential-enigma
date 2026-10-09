# /ai-form-builder/massage-intake-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-massage-intake-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-massage-intake-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-massage-intake-form-B-HUBRULES2aUS-1 (P1, B-HUBRULES2aUS, fix-by-writer, fixed)
- field: feature_1
- caught by: B-HUBRULES2aUS (Layer B): The heading and body use British 'tick' and 'ticked', and the body's next sentence switches to the US 'checks'.
- live text: Follow-up questions on a tick / Open a follow-up only when a box is ticked. A client who checks recent surgery is asked what was done and when
- faq before: window.awbFAQ = {"heading": "Massage Intake Questions, Answered", "items": [{"q": "What is a massage intake form?", "a": "A massage intake form is the questionnaire a client completes before a session, covering contact details, health history, medications, pressure and the areas to work on or avoid. It closes with a signed consent. A massage client intake form tells the therapist what to adjust on the table before anyone starts."}, {"q": "How do I make a massage intake form online?", "a": "List 
- faq after: window.awbFAQ = {"heading": "Massage Intake Questions, Answered", "items": [{"q": "What is a massage intake form?", "a": "A massage intake form is the questionnaire a client completes before a session, covering contact details, health history, medications, pressure and the areas to work on or avoid. It closes with a signed consent. A massage client intake form tells the therapist what to adjust on the table before anyone starts."}, {"q": "How do I make a massage intake form online?", "a": "List 
- feature_1 before: Follow-up questions on a tick Open a follow-up only when a box is ticked. A client who checks recent surgery is asked what was done and when, and one who checks pregnancy is asked how many weeks along.
- feature_1 after: Follow-up questions on a checked box Open a follow-up only when a box is checked. A client who checks recent surgery is asked what was done and when, and one who checks pregnancy is asked how many weeks along.
- howto_step_7_des before: Send the link with the booking confirmation, then fill it once yourself as a test client who ticks every box. Check that each alert lands. On the day itself, read the session sheet at the front desk, before the client is in the room.
- howto_step_7_des after: Send the link with the booking confirmation, then fill it out once yourself as a test client who checks every box. Check that each alert lands. On the day itself, read the session sheet at the front desk, before the client is in the room.

## 20261009-massage-intake-form-B-HUBRULES2aUS-2 (P1, B-HUBRULES2aUS, fix-by-writer, fixed)
- field: howto_step_7_des
- caught by: B-HUBRULES2aUS (Layer B): The step uses British 'ticks every box' and drops the particle in 'fill it once', which is not idiomatic US English.
- live text: then fill it once yourself as a test client who ticks every box.

## 20261009-massage-intake-form-B-HUBRULES2a-1 (P1, B-HUBRULES2a, fix-by-writer, fixed)
- field: faq
- caught by: B-HUBRULES2a (Layer B): FAQ 2 says 'fill it on a phone' without the particle, which is not idiomatic US English.
- live text: It builds the form with a client database behind it, and clients fill it on a phone from the booking confirmation.

## 20261009-massage-intake-form-B-HUBRULES2a-2 (P2, B-HUBRULES2a, backlog)
- field: features_subheading
- caught by: B-HUBRULES2a (Layer B): 'Your therapist' speaks to a spa owner, but the meta title targets therapists and tab 1 is a solo practice, so the reader is often the therapist.
- live text: Each one answers a question your therapist would otherwise ask with the client already on the table.
