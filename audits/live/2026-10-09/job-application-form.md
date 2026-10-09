# /ai-form-builder/job-application-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-job-application-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-job-application-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-job-application-form-B-HUBRULES2a-1 (P1, B-HUBRULES2a, fix-by-writer, fixed)
- field: faq
- caught by: B-HUBRULES2a (Layer B): FAQ 7 says 'the blank PDF', but the live page never introduces a blank PDF (step 6 handles walk-ins with a QR code and typed-in paper copies), so the reference points to nothing.
- live text: Limit the blank PDF to one past job and one reference and it fits on a single letter page, certification included.
- faq before: window.awbFAQ = {"heading": "Job Application Questions, Answered", "items": [{"q": "What is a job application form?", "a": "A job application form is the record a candidate fills out to apply for a specific opening, usually before any interview. Employers covered by federal EEOC rules keep every application for at least one year, including those from people they never hired."}, {"q": "How do I create a job application form online?", "a": "Describe the role in a few sentences, and Emergent's AI f
- faq after: window.awbFAQ = {"heading": "Job Application Questions, Answered", "items": [{"q": "What is a job application form?", "a": "A job application form is the record a candidate fills out to apply for a specific opening, usually before any interview. Employers covered by federal EEOC rules keep every application for at least one year, including those from people they never hired."}, {"q": "How do I create a job application form online?", "a": "Describe the role in a few sentences, and Emergent's AI f
- feature_4 before: A filled PDF of every application Each online application can be kept as a filled PDF in the same layout for the personnel file, typed signature included. Name each file by applicant and role, like Haddad_RN.pdf.
- feature_4 after: A filled PDF of every application Keep each application as a filled PDF laid out like your paper form, typed signature included, for the personnel file. Name each file by applicant and role, like Haddad_RN.pdf.

## 20261009-job-application-form-B-HUBRULES2a-2 (P1, B-HUBRULES2a, fix-by-writer, fixed)
- field: feature_4
- caught by: B-HUBRULES2a (Layer B): 'In the same layout' has no referent in the feature or anywhere above it, so the sentence does not say what the PDF matches.
- live text: Each online application can be kept as a filled PDF in the same layout for the personnel file, typed signature included.

## 20261009-job-application-form-B-HUBRULES5-1 (P2, B-HUBRULES5, backlog)
- field: meta_description
- caught by: B-HUBRULES5 (Layer B): The meta promises a printable blank PDF for walk-ins, but the body's walk-in step uses a QR code and staff typing in paper copies and never shows a blank PDF.
- live text: Print a blank PDF for walk-ins.

## 20261009-job-application-form-LIB-gforms-build-1 (P1, LIB-gforms-build, fix-by-writer, fixed)
- field: why_table
- caught by: LIB-gforms-build (Layer sweep): Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table
- feature_1 before: Every section, field by field Emergent drafts the six standard sections with the right input for each answer: a date picker for the start date, a phone field and a block that repeats for each past employer.
- feature_1 after: Every section, field by field Emergent drafts the six standard sections with the right input for each answer: a date picker for the start date, a phone field, and a block that repeats for each past employer.
- tab_image_3 before: An internal job application checks tenure before submit, 18 months in role against a 12-month minimum, keeps the application confidential and messages the employee's current manager in Slack only once a final interview is booked.
- tab_image_3 after: An internal job application checks tenure before submit, 18 months in role against a 12-month minimum, keeps the application confidential, and messages the employee's current manager in Slack only once a final interview is booked.
- why_table before: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Typeform Google Forms How you build Prompt for the application form and the hiring pipeline around it Templates, editor, AI generator Templates, editor, AI assist Manual, field by field Resume uploads Resumes and portfolios saved to storage you own, no sign-in Included;
- why_table after: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Typeform Google Forms How you build Prompt for the application form and the hiring pipeline around it Templates, editor, AI generator Templates, editor, AI assist Editor, with Gemini drafting on some Workspace plans Resume uploads Resumes and portfolios saved to storage

## 20261009-job-application-form-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: feature_1, tab_image_3 alt
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
