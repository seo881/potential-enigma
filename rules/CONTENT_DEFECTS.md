# Content defect catalogue

Every defect that has made a page less than world class, why it fails, and what catches it now. Writers read this before writing; reviewers check against it. It only grows: each rejection by Divit or a reviewer adds an entry, a rule or a QC check, dated (ratchet).

| # | Defect | Before (real) | After | Criterion | Caught by |
|---|---|---|---|---|---|
| 1 | H1 narrows the page to one feature or a sibling's topic | Build Accounts Payable Automation That Fits Your Approval Rules | Build Accounts Payable Automation From Inbox to Paid | scope | QC Q3 (flag) + rubric `scope` (block) |
| 2 | Paragraph opens with a keyword label or fragment | Accounts payable invoice automation for teams that buy against purchase orders. | Each invoice is read, matched to its purchase order and goods receipt, and held with the variance shown... | openers | QC Q1 (block) |
| 3 | Comparison column in hub boilerplate, not the buyer's language | Workflow + trigger form + database + dashboard, as code you own | Intake, matching, approvals, payment runs, and ledger, as code you own | specificity | QC Q4 (block): library variant required when the competitors' category has one |
| 4 | Tacked-on clause at the end of a sentence | ...so cash leaves on the dates you choose and not before. | ...on the payment dates finance sets in advance. | craft | QC A1 (block): "and not before", "and more", "and so on", "etc" |
| 5 | Image panels with visible empty zones | Multi-entity table with 4 rows; contractor panel with 3 small blocks | 5 rows; a payout-schedule rule added | images | Engine balance gate, QC I1 (block): pooled empty space over 16% |
| 6 | Run-on list sentences in FAQ answers | Compare AP automation companies on four things: how they price (per user, per invoice, or by quote), how much... (42 words) | Two sentences, 29 and 15 words | craft | QC Q2 (block over 40 words, flag over 32) |
| 7 | Unsupported generalization | Teams usually move the same headcount from data entry to review and analysis. | AP roles shift from data entry toward review and control. | truth | Rubric `truth` |
| 8 | False differentiator against a competitor | "No per-approver seats" as the edge over Tipalti, which also charges no per-user fees | Each vendor's pricing model stated factually from the library | truth | Library facts with sources; rubric `truth` |
| 10 | A number that does not follow from the others | Support CSAT scene: agents 4.7, 4.5, 3.2 and a team CSAT of 4.4 | Team CSAT 4.1 (their average) | images | Engine `checks`: every drawn quantity declared and true |
| 11 | Heading wider than the template renders cleanly | FAQ heading "Accounts Payable Automation Questions, Answered" at 828px (widest approved 656px) | "AP Automation Questions, Answered" (587px) | craft | QC T1 rendered-width ceilings |
| 9 | Off-topic People Also Ask questions answered | "Which 3 jobs will survive AI?" on the AP page | Skipped as PAA drift | intent | Brief + QC F4 relevance filter |

## How to use it
- **Writer, before QC:** run the rubric (`rules/rubric.json`) on your own page, line by line, and fix anything that resembles a row above.
- **Reviewer:** score every rubric criterion pass or fail with one line of evidence (`hubctl review`). A fail goes back with the exact field and the fix.
- **Divit's rejections:** add a row here the same day, and a QC check if the defect can be measured.
