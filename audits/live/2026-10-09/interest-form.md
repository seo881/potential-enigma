# /ai-form-builder/interest-form: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-interest-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-interest-form-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-interest-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: faq
- caught by: B-CONTENTDEFEC (Layer B): FAQ 4 says every form builder and template site offers a free interest form template, then hedges with 'usually' and 'Most': a sweeping claim about unnamed third parties.
- live text: Form builders and template sites each offer a free interest form template, usually for student clubs or volunteer programs. Most give you fields only.

## 20261009-interest-form-B-HUBRULES2a-1 (P2, B-HUBRULES2a, backlog)
- field: howto_step_7_title
- caught by: B-HUBRULES2a (Layer B): 'Fill it in' is the British idiom; the rest of the hub says fill out.
- live text: 07 Fill it in yourself first

## 20261009-interest-form-LIB-gforms-build-1 (P1, LIB-gforms-build, fix-by-writer, fixed)
- field: why_table
- caught by: LIB-gforms-build (Layer sweep): Google Forms 'How you build' cell updated in the library (Gemini drafting confirmed in Google's docs, 2026-10-10); regenerated table
- howto_step_5_des before: Paste the questions and the threshold into one prompt, and name who gets alerted. Emergent builds the form, a database of replies and a dashboard with a count per option. Change any part later by asking, such as lowering the threshold to 10.
- howto_step_5_des after: Paste the questions and the threshold into one prompt, and name who gets alerted. Emergent builds the form, a database of replies, and a dashboard with a count per option. Change any part later by asking, such as lowering the threshold to 10.
- mockup before: window.awbMockup = { eveningClasses: "I run continuing education at a community college and want to add a beginner woodworking course. Build an interest form that asks for name, email, which weeknight they could attend and their experience level. Show a count for each night on a dashboard, and email me when any night reaches 12 people.", youthSports: "I'm on the board of a youth lacrosse club. Build a player interest form for parents with the player's name, age group, position and seasons played
- mockup after: window.awbMockup = { eveningClasses: "I run continuing education at a community college and want to add a beginner woodworking course. Build an interest form that asks for name, email, which weeknight they could attend, and their experience level. Show a count for each night on a dashboard, and email me when any night reaches 12 people.", youthSports: "I'm on the board of a youth lacrosse club. Build a player interest form for parents with the player's name, age group, position, and seasons play
- why_table before: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Google Forms Jotform Typeform How you build Describe it in plain English Manual, field by field Templates, editor, AI generator Templates, editor, AI assist Where responses live A database table you own, plus any integration Google Sheets Jotform account Typeform account Respon
- why_table after: .cmp--emg-first thead th.col-brand-head { background: #ebebeb; } .cmp--emg-first tbody tr:nth-child(odd) td.col-brand { background: #f2f2f2; } .cmp--emg-first tbody tr:nth-child(even) td.col-brand { background: #e6e6e6; } Google Forms Jotform Typeform How you build Describe it in plain English Editor, with Gemini drafting on some Workspace plans Templates, editor, AI generator Templates, editor, AI assist Where responses live A database table you own, plus any integration Google Sheets Jotform a

## 20261009-interest-form-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: mockup, howto_step_5_des
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
