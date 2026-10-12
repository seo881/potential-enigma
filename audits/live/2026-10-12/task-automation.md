# /ai-automation-builder/task-automation: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-task-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-task-automation-B-QCA1stocknam-1 (P1, B-QCA1stocknam, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-QCA1stocknam (Layer B): Stock placeholder company name Globex in the Month-End Close tab copy (hidden tab, live in the DOM).
- live text: On the 1st, Globex Logistics' month-end checklist starts fresh with 18 tasks, each assigned to an owner and due on a set workday.
- cover_image before: Task automation: office manager Lena Ortiz gets a direct message that the payroll record for new hire Ana Brooks is due today
- cover_image after: Task automation: office manager Lena Dowling gets a direct message that the payroll record for new hire Ana Cavanagh is due today
- share_image before: Build task automation for the recurring work your team repeats, with Emergent
- share_image after: Build task automation for the recurring work your team repeats, with Emergent
- tab_content_1 before: Client documents filed by the app, not by the front desk Every file a client emails to Tallis Accounting's documents inbox is read before anyone opens it. Owen Pratt's W-2 is recognized and saved to his client folder under a standard name, and his checklist moves to 5 of 7 received. A file from an address the firm does not know waits for a person.
- tab_content_1 after: Client documents filed by the app, not by the front desk Every file a client emails to Tallis Accounting's documents inbox is read before anyone opens it. Owen Dineen's W-2 is recognized and saved to his client folder under a standard name, and his checklist moves to 5 of 7 received. A file from an address the firm does not know waits for a person.
- tab_content_2 before: Before a new hire's first day, every owner has a task Signing the offer in Kestrel Dental Group's hiring tracker creates six setup tasks spread across four owners. Each one is dated back from the start date: payroll five days before, the laptop three days before. Whoever has not closed a task by its date gets a direct message each morning until it is done.
- tab_content_2 after: Before a new hire's first day, every owner has a task Signing the offer in Cardwell Dental Group's hiring tracker creates six setup tasks spread across four owners. Each one is dated back from the start date: payroll five days before, the laptop three days before. Whoever has not closed a task by its date gets a direct message each morning until it is done.
- tab_content_3 before: Anyone short on hours is asked by name on Friday At 3:00 PM on Friday, Fieldwork Studio's app compares each person's logged hours with the 40 they owe. Four people are under, and each gets a direct message showing their own total and the days with gaps. Anyone still short on Monday at 10:00 AM is listed for their team lead.
- tab_content_3 after: Anyone short on hours is asked by name on Friday At 3:00 PM on Friday, Draycott Studio's app compares each person's logged hours with the 40 they owe. Four people are under, and each gets a direct message showing their own total and the days with gaps. Anyone still short on Monday at 10:00 AM is listed for their team lead.
- tab_content_4 before: The close checklist, rebuilt on the 1st with owners On the 1st, Globex Logistics' month-end checklist starts fresh with 18 tasks, each assigned to an owner and due on a set workday. Bank reconciliation is due on workday 3. If a task is still open when its workday ends, Dana Kerr, the controller, gets a Slack message the next morning.
- tab_content_4 after: The close checklist, rebuilt on the 1st with owners On the 1st, Dunlevy Logistics' month-end checklist starts fresh with 18 tasks, each assigned to an owner and due on a set workday. Bank reconciliation is due on workday 3. If a task is still open when its workday ends, Ruth Dyer, the controller, gets a Slack message the next morning.
- tab_image_1 before: A W-2 that Owen Pratt emailed to Tallis Accounting's documents inbox is matched to his client record, renamed, and filed in his folder, and his tax checklist moves to 5 of 7 documents received.
- tab_image_1 after: A W-2 that Owen Dineen emailed to Tallis Accounting's documents inbox is matched to his client record, renamed, and filed in his folder, and his tax checklist moves to 5 of 7 documents received.
- tab_image_2 before: Signing Ana Brooks's offer at Kestrel Dental Group creates six setup tasks for four owners; the laptop is done and office manager Lena Ortiz gets a direct message that the payroll record is due today.
- tab_image_2 after: Signing Ana Cavanagh's offer at Cardwell Dental Group creates six setup tasks for four owners; the laptop is done and office manager Lena Dowling gets a direct message that the payroll record is due today.
- tab_image_3 before: At 3:00 PM on Friday, Fieldwork Studio's hours check finds four people under 40 hours, and Theo Grant gets a direct message showing 31.5 of 40 hours logged with gaps on Tuesday and Thursday.
- tab_image_3 after: At 3:00 PM on Friday, Draycott Studio's hours check finds four people under 40 hours, and Theo Dacre gets a direct message showing 31.5 of 40 hours logged with gaps on Tuesday and Thursday.
- tab_image_4 before: Globex Logistics' month-end close checklist is rebuilt on the 1st with 18 tasks; bank reconciliation is still open past workday 3, and controller Dana Kerr gets a Slack message about it.
- tab_image_4 after: Dunlevy Logistics' month-end close checklist is rebuilt on the 1st with 18 tasks; bank reconciliation is still open past workday 3, and controller Ruth Dyer gets a Slack message about it.

## 20261012-task-automation-B-QCA1stocknam-2 (P1, B-QCA1stocknam, fix-by-writer, fixed)
- field: tab_image_4
- caught by: B-QCA1stocknam (Layer B): Globex in the tab 4 alt text; the same string is in image_brief tab 4 and embedded in uc-4.svg, so the image must be re-rendered with the new name.
- live text: Globex Logistics' month-end close checklist is rebuilt on the 1st with 18 tasks; bank reconciliation is still open past workday 3

## 20261012-task-automation-B-QCA1AItellsr-1 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: tab_content_4
- caught by: B-QCA1AItellsr (Layer B): Persona Dana Kerr is reused (liability-waiver-form), and 'Dana' is also the contact on booking-form (Dana Whitfield) and client-onboarding-questionnaire (Dana Whitlock).
- live text: Dana Kerr, the controller, gets a Slack message the next morning.

## 20261012-task-automation-B-QCA1AItellsr-2 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1AItellsr (Layer B): Company prefix Kestrel is reused on 15 other specs (procurement-automation, sales-automation, daycare-registration-form, ...).
- live text: Signing the offer in Kestrel Dental Group's hiring tracker creates six setup tasks spread across four owners.

## 20261012-task-automation-B-QCA1AItellsr-3 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: tab_image_2
- caught by: B-QCA1AItellsr (Layer B): Alt reuses Ana Brooks (7 other specs), Lena Ortiz (13 other specs) and Kestrel (15); both people are also drawn in uc-2.svg and the cover.
- live text: Signing Ana Brooks's offer at Kestrel Dental Group creates six setup tasks for four owners; the laptop is done and office manager Lena Ortiz gets a

## 20261012-task-automation-B-QCA1AItellsr-4 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: cover_image
- caught by: B-QCA1AItellsr (Layer B): Cover alt and cover art reuse Lena Ortiz (13 other specs) and Ana Brooks (7 other specs).
- live text: Task automation: office manager Lena Ortiz gets a direct message that the payroll record for new hire Ana Brooks is due today

## 20261012-task-automation-B-QCA1AItellsr-5 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: tab_image_3
- caught by: B-QCA1AItellsr (Layer B): Alt reuses Theo Grant (4 other specs); uc-3.svg also draws Mia Chen (3 other specs) and Rafael Ortiz, a second Ortiz on this page.
- live text: and Theo Grant gets a direct message showing 31.5 of 40 hours logged with gaps on Tuesday and Thursday.

## 20261012-task-automation-B-QCA1AItellsr-6 (P1, B-QCA1AItellsr, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-QCA1AItellsr (Layer B): Persona Owen Pratt is reused (parent-consent-form); also drawn in uc-1.svg and named in tab_image_1 alt.
- live text: Owen Pratt's W-2 is recognized and saved to his client folder under a standard name, and his checklist moves to 5 of 7 received.

## 20261012-task-automation-B-QCA1AItellsr-7 (P1, B-QCA1AItellsr, proposed)
- field: image_brief
- caught by: B-QCA1AItellsr (Layer B): Drawn names reused across the hub: Ridgeway Freight (Ridgeway on 7 other specs, tab 1) and owner J. Park (3 other specs, tab 4). Re-render after renaming.
- live text: Employer: Ridgeway Freight | Bank reconciliation, J. Park, Workday 3

## 20261012-task-automation-B-QCA1stocknam-3 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): Stock name Acme Corp drawn in the AI CRM Builder card of the 'More things you can build' component; same component on all four pages in this batch. Sitewide, outside the hub collections: Divit's call.
- live text: Lead | Proposal | Won | AC Acme Corp $24,000 Proposal

## 20261012-task-automation-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: image_brief
- caught by: B-CONTENTDEFEC (Layer B): Tab 2 messages Lena Ortiz on the due date ('Due today, sent each morning until closed') while the copy messages whoever has not closed a task by its date; the timeline also lists the laptop (3 days before) above payroll (5 days before).
- live text: Whoever has not closed a task by its date gets a direct message each morning until it is done.

## 20261012-task-automation-B-CONTENTDEFEC-2 (P2, B-CONTENTDEFEC, backlog)
- field: image_brief
- caught by: B-CONTENTDEFEC (Layer B): Tab 1 list shows 2 received and 2 missing under a '5 of 7 received' badge; a reader counting rows sees 2 of 4.
- live text: Owen Pratt, tax documents  5 of 7 received

## 20261012-task-automation-B-CONTENTDEFEC-3 (P2, B-CONTENTDEFEC, backlog)
- field: faq#10
- caught by: B-CONTENTDEFEC (Layer B): Generalization about unnamed free plans; overage billing is a paid-plan behavior (Zapier), so 'others bill extra' is shaky for free plans.
- live text: check what happens when a free plan's monthly run limit is reached, since some pause and others bill extra.

## 20261012-task-automation-B-HUBRULES1Num-1 (P2, B-HUBRULES1Num, backlog)
- field: tab_content_2
- caught by: B-HUBRULES1Num (Layer B): Durations spelled out; the rule asks for numerals for all durations. Same on howto_step_1_des 'for one week', howto_step_6_des 'For two weeks', howto_step_7_des 'Once two weeks pass'.
- live text: payroll five days before, the laptop three days before.
