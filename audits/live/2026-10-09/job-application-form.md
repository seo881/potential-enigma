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
