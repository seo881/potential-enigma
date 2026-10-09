# /ai-form-builder/employee-information-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-employee-information-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-employee-information-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-employee-information-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: howto_step_6_des
- caught by: B-CONTENTDEFEC (Layer B): Step 6 advises a quiet month away from year-end payroll, while the page's own Annual Check tab runs the check in January, in W-2 season.
- live text: Choose a quiet month, away from open enrollment and year-end payroll.

## 20261009-employee-information-form-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: tab_content_2
- caught by: B-CONTENTDEFEC (Layer B): Generalization stated as fact: not every marriage changes a surname.
- live text: Marriage changes a surname, and payroll has to time the switch.

## 20261009-employee-information-form-B-HUBRULES5-1 (P2, B-HUBRULES5, backlog)
- field: faq#4
- caught by: B-HUBRULES5 (Layer B): The question keeps the searcher's ungrammatical 'How to ...?' form; HUB_RULES 5 allows a light grammar edit.
- live text: How to fill out an employee information form?

## 20261009-employee-information-form-LIB-gforms-build-1 (P1, LIB-gforms-build, fix-by-writer, fixed)
- field: why_table
- caught by: LIB-gforms-build (Layer sweep): Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table
- faq before: window.awbFAQ = {"heading": "Staff Record Questions, Answered", "items": [{"q": "What is an employee information form?", "a": "An employee information form is the record an employer keeps on each person: legal name, contact details, job title, start date, and emergency contacts. HR collects it at hiring and goes back to it whenever payroll or a manager needs a detail."}, {"q": "How do I make an employee information form online?", "a": "List the fields payroll and HR use, decide who may see each 
- faq after: window.awbFAQ = {"heading": "Staff Record Questions, Answered", "items": [{"q": "What is an employee information form?", "a": "An employee information form is the record an employer keeps on each person: legal name, contact details, job title, start date, and emergency contacts. HR collects it at hiring and goes back to it whenever payroll or a manager needs a detail."}, {"q": "How do I make an employee information form online?", "a": "List the fields payroll and HR use, decide who may see each 
- howto_step_2_des before: Group the questions under personal details, contact details, job details and emergency contacts. One section per screen keeps the form short on a phone, and HR can later resend a single section when only that part needs an update.
- howto_step_2_des after: Group the questions under personal details, contact details, job details, and emergency contacts. One section per screen keeps the form short on a phone, and HR can later resend a single section when only that part needs an update.
- mockup before: window.awbMockup = { annualRecordCheck: "Build an employee information form for my freight company's 140 employees. Every January, send each person their own record with last year's answers filled in, and let them confirm it or edit any field. Show me a dashboard of who has confirmed, who edited and who has not replied. Ten days after the send, email a reminder to everyone still open.", legalNameChanges: "Let my employees request a legal name change from their record. Ask for the new name and wh
- mockup after: window.awbMockup = { annualRecordCheck: "Build an employee information form for my freight company's 140 employees. Every January, send each person their own record with last year's answers filled in, and let them confirm it or edit any field. Show me a dashboard of who has confirmed, who edited and who has not replied. Ten days after the send, email a reminder to everyone still open.", legalNameChanges: "Let my employees request a legal name change from their record. Ask for the new name and wh
- why_table before: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Google Forms Typeform How you build Describe it in plain English Templates, editor, AI generator Manual, field by field Templates, editor, AI assist Where responses live A database table you own, plus any integration Jotform account Google Sheets Typeform account Respon
- why_table after: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Google Forms Typeform How you build Describe it in plain English Templates, editor, AI generator Editor, with Gemini drafting on some Workspace plans Templates, editor, AI assist Where responses live A database table you own, plus any integration Jotform account Google 

## 20261009-employee-information-form-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: mockup, howto_step_2_des, faq
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
