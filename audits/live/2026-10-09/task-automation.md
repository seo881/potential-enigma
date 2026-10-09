# /ai-automation-builder/task-automation: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-task-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-task-automation-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-task-automation-B-DECISIONS202-1 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: features_subheading
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: Each task gets a trigger, a rule and a person to answer to.
- feature_3 before: AI steps for reading and sorting Read an attachment, decide what kind of document it is and pull out the fields you name. A step the model is unsure about pauses until someone on your team checks it.
- feature_3 after: AI steps for reading and sorting Read an attachment, decide what kind of document it is, and pull out the fields you name. A step the model is unsure about pauses until someone on your team checks it.
- feature_5 before: A log of every task the app ran Write each run to a database you own: what triggered it, what it changed and who acted on it. Filter by person or by week when someone asks why a task did not run last month.
- feature_5 after: A log of every task the app ran Write each run to a database you own: what triggered it, what it changed, and who acted on it. Filter by person or by week when someone asks why a task did not run last month.
- features_subheading before: Each task gets a trigger, a rule and a person to answer to. Add the parts below as the job asks for them.
- features_subheading after: Each task gets a trigger, a rule, and a person to answer to. Add the parts below as the job asks for them.
- howto_step_2_des before: Describe a single task in a few sentences: what starts it, which record it reads and what counts as done. Include the exceptions people handle without thinking, like a client who sends documents from a spouse's email address.
- howto_step_2_des after: Describe a single task in a few sentences: what starts it, which record it reads, and what counts as done. Include the exceptions people handle without thinking, like a client who sends documents from a spouse's email address.
- tab_image_1 before: A W-2 that Owen Pratt emailed to Tallis Accounting's documents inbox is matched to his client record, renamed and filed in his folder, and his tax checklist moves to 5 of 7 documents received.
- tab_image_1 after: A W-2 that Owen Pratt emailed to Tallis Accounting's documents inbox is matched to his client record, renamed, and filed in his folder, and his tax checklist moves to 5 of 7 documents received.

## 20261009-task-automation-B-DECISIONS202-2 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_3
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: Read an attachment, decide what kind of document it is and pull out the fields you name.

## 20261009-task-automation-B-DECISIONS202-3 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_5
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: what triggered it, what it changed and who acted on it

## 20261009-task-automation-B-DECISIONS202-4 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: howto_step_2_des
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: what starts it, which record it reads and what counts as done

## 20261009-task-automation-B-DECISIONS202-5 (P2, B-DECISIONS202, backlog)
- field: mockup
- caught by: B-DECISIONS202 (Layer B): A list of actions in the clientDocumentFiling prompt has no serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- live text: read it, work out which client and which form it is, rename it and save it to that client's folder

## 20261009-task-automation-B-DECISIONS202-6 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: tab_image_1 alt
- caught by: B-DECISIONS202 (Layer B): A three-item list in the alt text has no serial comma.
- live text: is matched to his client record, renamed and filed in his folder
