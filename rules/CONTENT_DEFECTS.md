# Content defect catalogue

Every defect that has made a page less than world class, why it fails, and what catches it now. Writers read this before writing; reviewers check against it. It only grows: each rejection by Divit or a reviewer adds an entry, a rule or a QC check, dated (ratchet).

| # | Defect | Before (real) | After | Criterion | Caught by |
|---|---|---|---|---|---|
| 1 | H1 narrows the page to one feature or a sibling's topic | Build Accounts Payable Automation That Fits Your Approval Rules | Build Accounts Payable Automation From Inbox to Paid | scope | QC Q3 (flag) + rubric `scope` (block) |
| 2 | Paragraph opens with a keyword label or fragment | Accounts payable invoice automation for teams that buy against purchase orders. | Each invoice is read, matched to its purchase order and goods receipt, and held with the variance shown... | openers | QC Q1 (block) |
| 3 | Comparison column in hub boilerplate, not the buyer's language | Workflow + trigger form + database + dashboard, as code you own | Intake, matching, approvals, payment runs, and ledger, as code you own | specificity | QC Q4 (block): library variant required when the competitors' category has one |
| 4 | Tacked-on clause at the end of a sentence | ...so cash leaves on the dates you choose and not before. | ...on the payment dates finance sets in advance. | craft | QC A1 (block): "and not before", "and more", "and so on", "etc"; QC Q5 (2026-10-07): "which/that is what" block, ", so" endings flag, more than 2 on a page block |
| 5 | Image panels with visible empty zones | Multi-entity table with 4 rows; contractor panel with 3 small blocks | 5 rows; a payout-schedule rule added | images | Engine balance gate, QC I1 (block): pooled empty space over 16% |
| 6 | Run-on list sentences in FAQ answers | Compare AP automation companies on four things: how they price (per user, per invoice, or by quote), how much... (42 words) | Two sentences, 29 and 15 words | craft | QC Q2 (block over 40 words, flag over 32) |
| 7 | Unsupported generalization | Teams usually move the same headcount from data entry to review and analysis. | AP roles shift from data entry toward review and control. | truth | Rubric `truth` |
| 8 | False differentiator against a competitor | "No per-approver seats" as the edge over Tipalti, which also charges no per-user fees | Each vendor's pricing model stated factually from the library | truth | Library facts with sources; rubric `truth` |
| 10 | A number that does not follow from the others | Support CSAT scene: agents 4.7, 4.5, 3.2 and a team CSAT of 4.4 | Team CSAT 4.1 (their average) | images | Engine `checks`: every drawn quantity declared and true |
| 11 | Heading wider than the template renders cleanly | FAQ heading "Accounts Payable Automation Questions, Answered" at 828px (widest approved 656px) | "AP Automation Questions, Answered" (587px) | craft | QC T1 rendered-width ceilings |
| 9 | Off-topic People Also Ask questions answered | "Which 3 jobs will survive AI?" on the AP page | Skipped as PAA drift | intent | Brief + QC F4 relevance filter |
| 12 | A weekday that contradicts its date (2026-10-07) | "Payout runs every other Friday, next on Oct 24" (Oct 24, 2026 is a Saturday) | "next on Oct 23" | truth | Rubric `truth`, `images` |
| 13 | A false fact about a real brand inside an image (2026-10-07) | "Figma Organization plan, billed monthly" (Figma bills it annually) | "Design tool subscription, billed monthly" | truth | Rubric `truth`; real brands only as tools (docs/IMAGE_BRIEF.md rule 6) |
| 14 | Platform behaviour stated as automatic, or knowledge Emergent cannot have (2026-10-07) | "Each page gets a canonical tag and a sitemap entry"; image chip "Page indexed" | "Prompt for a canonical tag and a sitemap entry"; "Page published" | truth | Rubric `truth`; capability ledger (QC C2) |
| 15 | Image dates that go stale (2026-10-07) | "Expires Nov 28, 2026" flagged "within 60 days" (false from Nov 29) | "Expires in 52 days, under 60", declared in checks | images | Rubric `images` |
| 16 | Feature body opens without a verb (2026-10-07) | "Contact details, position, start date, work history, education, references, and a signed certification, generated from your prompt." | "Emergent generates the sections a standard job application carries: ..." | openers | Rubric `openers` (QC Q1 catches keyword labels only) |
| 17 | The we/our ban firing on a form's own field labels (2026-10-07) | "may we contact" forced into "permission to contact" | A quoted label is the form's words: "May we contact your employer?" | craft | QC H1 skips quoted labels and the country "US" |
| 18 | The same phrase in two fields; an FAQ answer that restates the body (2026-10-07) | FAQ 2 "Write down the rules your controller already applies" repeats the how-to description | Each FAQ answer adds something the body does not say | faq | QC Q6 (block): any 6-word phrase in two fields |
| 19 | Filler "from X to Y" ranges (2026-10-07) | 11 on the AP page, e.g. "from QuickBooks to any ERP with an API" | Real journeys only | voice | QC Q7 (block over 3) |
| 20 | The image tells a different story from its tab copy (2026-10-07) | Image prompt "hold any price variance"; copy "a price or quantity outside the tolerance holds it" | Story link: the rule drawn matches the copy, numbers included | images | Engine story links, QC I4 (block) |

## How to use it
- **Writer:** read this catalogue and the hub exemplar (`specs/<dir>/_exemplar.md`) before writing, then run QC until TOTAL 0. Writers do not self-score. On rework, fix the class, not the instance: search the whole page for every occurrence of the defect in the note.
- **Reviewer:** read the page cold, then verify earlier fixes; score every rubric criterion pass or fail with evidence (`hubctl review`). A fail lists every instance on the page, each with its field and the fix.
- **Divit's rejections:** add a row here the same day, and a QC check if the defect can be measured.
