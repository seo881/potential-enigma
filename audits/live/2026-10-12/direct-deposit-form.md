# /ai-form-builder/direct-deposit-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-direct-deposit-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-direct-deposit-form-B-HUBRULES8CON-1 (P1, B-HUBRULES8CON, fix-by-writer, fixed)
- field: tab_content_3
- caught by: B-HUBRULES8CON (Layer B): Unsourced generalization about payroll fraud stated as fact, and contestable (insider payroll schemes are common); the IC3 source covers redirected deposits only.
- live text: Payroll fraud rarely starts in payroll. A stolen login or a spoofed email asks to switch the deposit account.
- tab_content_3 before: No new account until the employee confirms Payroll fraud rarely starts in payroll. A stolen login or a spoofed email asks to switch the deposit account. The app holds the change and emails a confirmation link to the address on file. Once the employee confirms, the payroll manager gets a Slack direct message naming the employee.
- tab_content_3 after: No new account until the employee confirms A redirected paycheck starts outside payroll: a stolen login or a spoofed email asks to switch the deposit account. The app holds the change and emails a confirmation link to the address on file. Once the employee confirms, the payroll manager gets a Slack direct message naming the employee.

## 20261012-direct-deposit-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: why_table
- caught by: B-CONTENTDEFEC (Layer B): The 'Response limits' row answers with pricing for ADP and Eddy, so the row label does not match the cells (library variant).
- live text: Response limits | Quoted by payroll frequency and headcount | ... | Priced per person plus a monthly base fee

## 20261012-direct-deposit-form-B-HUBRULES2b-1 (P2, B-HUBRULES2b, backlog)
- field: meta_title
- caught by: B-HUBRULES2b (Layer B): Meta title reads clipped and machine-assembled (carried review note).
- live text: Direct Deposit Form: What It Asks and an App | Emergent

## 20261012-direct-deposit-form-B-HUBRULES5390-1 (P2, B-HUBRULES5390, backlog)
- field: howto_step_1_des
- caught by: B-HUBRULES5390 (Layer B): At 390 px 'W-9' breaks at its hyphen across two lines ('a W-' / '9 before').
- live text: while a contractor also owes you a W-9 before the first payment goes out.

## 20261012-direct-deposit-form-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: image_brief tab 1
- caught by: B-CONTENTDEFEC (Layer B): Confidence bar (100%) drawn on the value the employee typed, which reads as if the typed value were extracted (carried review note).
- live text: Routing typed  ending 4477  100%
