# /ai-form-builder/client-onboarding-questionnaire: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-client-onboarding-questionnaire-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-client-onboarding-questionnaire-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-client-onboarding-questionnaire-B-HUBRULES5-1 (P1, B-HUBRULES5, fix-by-writer, fixed)
- field: explore_cta
- caught by: B-HUBRULES5 (Layer B): At 390 px the 40-character comparison CTA overflows its pill: the leading 'B' is clipped and the arrow touches the edge (the 34-character employee-information-form CTA just fits).
- live text: Build My Client Onboarding Questionnaire
- explore_cta before: Build My Client Onboarding Questionnaire
- explore_cta after: Build My Onboarding Questionnaire
- faq before: window.awbFAQ = {"heading": "Client Onboarding Questions, Answered", "items": [{"q": "What is a client onboarding questionnaire?", "a": "A client onboarding questionnaire is the set of questions a business sends a new client before work begins. It gathers the company background, goals, key contacts and anything the team needs access to. The best ones ask only what the team needs to begin."}, {"q": "How do I create a client onboarding questionnaire?", "a": "Write down what the work cannot start w
- faq after: window.awbFAQ = {"heading": "Client Onboarding Questions, Answered", "items": [{"q": "What is a client onboarding questionnaire?", "a": "A client onboarding questionnaire is the set of questions a business sends a new client before work begins. It gathers the company background, goals, key contacts, and anything the team needs access to. The best ones ask only what the team needs to begin."}, {"q": "How do I create a client onboarding questionnaire?", "a": "Write down what the work cannot start 
- howto_step_2_des before: Group questions under the service the client is paying for. A monthly retainer needs brand and audience sections, while a one-time project needs scope, a deadline and the person who signs off. Each client sees only their own sections, which keeps the form short.
- howto_step_2_des after: Group questions under the service the client is paying for. A monthly retainer needs brand and audience sections, while a one-time project needs scope, a deadline, and the person who signs off. Each client sees only their own sections, which keeps the form short.
- mockup before: window.awbMockup = { marketingAgencies: "I run a social media agency that manages Instagram, Facebook, LinkedIn and TikTok for small food brands. Build an onboarding questionnaire where each new client gives us access on every account and ticks it off, with no passwords. Keep the kickoff call unbooked until all four are shared, and email the client's contact a reminder when one is still missing after two days.", brandPhotography: "I shoot half-day brand sessions for small businesses. Build a cli
- mockup after: window.awbMockup = { marketingAgencies: "I run a social media agency that manages Instagram, Facebook, LinkedIn, and TikTok for small food brands. Build an onboarding questionnaire where each new client gives us access on every account and ticks it off, with no passwords. Keep the kickoff call unbooked until all four are shared, and email the client's contact a reminder when one is still missing after two days.", brandPhotography: "I shoot half-day brand sessions for small businesses. Build a cl
- why_table before: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Typeform Google Forms How you build Describe it in plain English Templates, editor, AI generator Templates, editor, AI assist Manual, field by field Response limits No response caps Monthly submission caps by plan; the form stops at the cap Monthly response caps by plan
- why_table after: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Typeform Google Forms How you build Describe it in plain English Templates, editor, AI generator Templates, editor, AI assist Editor, with Gemini drafting on some Workspace plans Response limits No response caps Monthly submission caps by plan; the form stops at the cap

## 20261009-client-onboarding-questionnaire-B-HUBRULES2b-1 (P1, B-HUBRULES2b, fix-by-writer, fixed)
- field: faq#8
- caught by: B-HUBRULES2b (Layer B): A missing comma creates a garden-path sentence that reads as 'taking them on call'.
- live text: Firms that screen a prospect before taking them on call that first step an intake form.
- faq before: window.awbFAQ = {"heading": "Client Onboarding Questions, Answered", "items": [{"q": "What is a client onboarding questionnaire?", "a": "A client onboarding questionnaire is the set of questions a business sends a new client before work begins. It gathers the company background, goals, key contacts and anything the team needs access to. The best ones ask only what the team needs to begin."}, {"q": "How do I create a client onboarding questionnaire?", "a": "Write down what the work cannot start w
- faq after: window.awbFAQ = {"heading": "Client Onboarding Questions, Answered", "items": [{"q": "What is a client onboarding questionnaire?", "a": "A client onboarding questionnaire is the set of questions a business sends a new client before work begins. It gathers the company background, goals, key contacts and anything the team needs access to. The best ones ask only what the team needs to begin."}, {"q": "How do I create a client onboarding questionnaire?", "a": "Write down what the work cannot start w

## 20261009-client-onboarding-questionnaire-B-HUBRULES2a-1 (P2, B-HUBRULES2a, backlog)
- field: features_heading
- caught by: B-HUBRULES2a (Layer B): The section promises what happens after submit, but two of its six features (service sections, the access checklist) work while the client is filling it in.
- live text: What Happens After the Client Hits Submit

## 20261009-client-onboarding-questionnaire-LIB-gforms-build-1 (P1, LIB-gforms-build, fix-by-writer, fixed)
- field: why_table
- caught by: LIB-gforms-build (Layer sweep): Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table

## 20261009-client-onboarding-questionnaire-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: mockup, howto_step_2_des, faq
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
