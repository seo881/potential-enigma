# /ai-form-builder/sign-in-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-sign-in-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-sign-in-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-sign-in-form-B-HUBRULES5com-1 (P1, B-HUBRULES5com, fix-by-writer, fixed)
- field: why_table
- caught by: B-HUBRULES5com (Layer B): Google Forms build cell says it is built manually, field by field; Google has added Gemini form generation ('Help me create a form') to Forms, and the library fact (checked 2026-09-28) cites the old approved table, not vendor documentation, so it may now be a false competitor fact.
- live text: How you build | Describe it in plain English | Manual, field by field
- tab_content_1 before: Sam Keller hears about his visitor in Slack Visitors at Fieldstone Architects sign in on a tablet in the lobby. Lena Ortiz types her name and company, picks Sam Keller from the host list and taps Sign in. Sam gets a Slack direct message at 2:04 PM naming her and Northwind Freight, and he walks out to meet her.
- tab_content_1 after: Sam Keller hears about his visitor in Slack Visitors at Fieldstone Architects sign in on a tablet in the lobby. Lena Ortiz types her name and company, picks Sam Keller from the host list, and taps Sign in. Sam gets a Slack direct message at 2:04 PM naming her and Northwind Freight, and he walks out to meet her.
- why_table before: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Google Forms Jotform Typeform How you build Describe it in plain English Manual, field by field Templates, editor, AI generator Templates, editor, AI assist Where responses live A database table you own, plus any integration Google Sheets Jotform account Typeform account Respon
- why_table after: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Google Forms Jotform Typeform How you build Describe it in plain English Editor, with Gemini drafting on some Workspace plans Templates, editor, AI generator Templates, editor, AI assist Where responses live A database table you own, plus any integration Google Sheets Jotform a

## 20261009-sign-in-form-B-HUBRULES2aCo-1 (P2, B-HUBRULES2aCo, backlog)
- field: h1, breadcrumb, faq, feature_6, prompt_chip_1
- caught by: B-HUBRULES2aCo (Layer B): The page writes the open compound 'sign in form' (keyword form) beside the hyphenated 'sign-in' (chip 'Visitor Sign-In', 'sign-in app', 'sign-in button').
- live text: Build a Sign in Form That Tracks Who Comes and Goes ... Visitor Sign-In

## 20261009-sign-in-form-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: tab_content_1
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
