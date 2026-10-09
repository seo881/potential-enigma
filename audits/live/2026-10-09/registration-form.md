# /ai-form-builder/registration-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-registration-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-registration-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-registration-form-B-HUBRULES6rul-1 (P1, B-HUBRULES6rul, fix-by-writer, fixed)
- field: feature_6
- caught by: B-HUBRULES6rul (Layer B): The custom-domain claim uses the banned 'built in' wording without the hyphen, which slips past the H/claims regex.
- live text: Put the form on a custom domain, built in and paid for with credits, or embed it on a site you already run.
- faq before: window.awbFAQ = {"heading": "Registration Form Questions, Answered", "items": [{"q": "What is a registration form?", "a": "A registration form collects what an organizer needs to add someone to a list, whether that list is an event, a program, a membership, or a product warranty. It starts with a name and contact details. The rest depends on the list, such as a ticket type or a serial number."}, {"q": "How do I create a registration form?", "a": "Start with the list you want at the end, then wor
- faq after: window.awbFAQ = {"heading": "Registration Form Questions, Answered", "items": [{"q": "What is a registration form?", "a": "A registration form collects what an organizer needs to add someone to a list, whether that list is an event, a program, a membership, or a product warranty. It starts with a name and contact details. The rest depends on the list, such as a ticket type or a serial number."}, {"q": "How do I create a registration form?", "a": "Start with the list you want at the end, then wor
- feature_6 before: Code you can take with you Put the form on a custom domain, built in and paid for with credits, or embed it on a site you already run. On paid plans, export the full code to GitHub and keep building there.
- feature_6 after: Code you can take with you Put the form on a custom domain, included and paid for with credits, or embed it on a site you already run. On paid plans, export the full code to GitHub and keep building there.

## 20261009-registration-form-B-HUBRULES5FAQ-1 (P1, B-HUBRULES5FAQ, fix-by-writer, fixed)
- field: faq
- caught by: B-HUBRULES5FAQ (Layer B): The creator-application link was held back because that page is not live (404), and without the link FAQ 8's last sentence points the reader to a build that cannot be seen.
- live text: A creator application shows the same build for screening applicants instead of registering them.
