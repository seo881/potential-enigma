# /ai-form-builder/t-shirt-order-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-t-shirt-order-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-t-shirt-order-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-t-shirt-order-form-B-HUBRULES5com-1 (P1, B-HUBRULES5com, fix-by-writer, fixed)
- field: why_table
- caught by: B-HUBRULES5com (Layer B): Google Forms build cell says it is built manually, field by field; Google has added Gemini form generation ('Help me create a form') to Forms, and the library fact (checked 2026-09-28) cites the old approved table, not vendor documentation, so it may now be a false competitor fact.
- live text: How you build | Describe it in plain English | Templates, editor, AI generator | Manual, field by field
- tab_content_2 before: Printing a name on back adds $5 The Delgado family reunion has 41 relatives coming this summer. Each picks a navy or heather gray shirt at $20, adds a name on the back for $5 and pays by card. Cousins out of state enter a mailing address. Everyone else collects at the welcome table, and the organizer sees both groups in one table.
- tab_content_2 after: Printing a name on back adds $5 The Delgado family reunion has 41 relatives coming this summer. Each picks a navy or heather gray shirt at $20, adds a name on the back for $5, and pays by card. Cousins out of state enter a mailing address. Everyone else collects at the welcome table, and the organizer sees both groups in one table.
- why_table before: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Google Forms Typeform How you build Describe it in plain English Templates, editor, AI generator Manual, field by field Templates, editor, AI assist Response limits No response caps Monthly submission caps by plan; the form stops at the cap No limit Monthly response cap
- why_table after: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Jotform Google Forms Typeform How you build Describe it in plain English Templates, editor, AI generator Editor, with Gemini drafting on some Workspace plans Templates, editor, AI assist Response limits No response caps Monthly submission caps by plan; the form stops at the cap

## 20261009-t-shirt-order-form-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: tab_content_2
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
