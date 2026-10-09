# /ai-form-builder/client-onboarding-questionnaire: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-client-onboarding-questionnaire-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-client-onboarding-questionnaire-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-client-onboarding-questionnaire-B-HUBRULES5-1 (P1, B-HUBRULES5, proposed)
- field: explore_cta
- caught by: B-HUBRULES5 (Layer B): At 390 px the 40-character comparison CTA overflows its pill: the leading 'B' is clipped and the arrow touches the edge (the 34-character employee-information-form CTA just fits).
- live text: Build My Client Onboarding Questionnaire

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
