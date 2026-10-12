# /ai-automation-builder/sales-automation: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-sales-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-sales-automation-B-QCA1stocknam-1 (P1, B-QCA1stocknam, fix-by-writer, fixed)
- field: tab_image_3
- caught by: B-QCA1stocknam (Layer B): Tab 3 image (image_brief rows) draws three stock names in the open-deals table.
- live text: Northwind  Jen Alvarez  Proposal  $24,000 / Globex  Marco Rossi  Evaluation  $52,000 / Initech  Dana Ruiz  Evaluation  $40,000
- cover_image before: Sales automation: a direct message tells rep Marco Rossi that a new lead, Corbel with 850 employees in the West, is his
- cover_image after: Sales automation: a direct message tells rep Marco Albani that a new lead, Corbel with 850 employees in the West, is his
- share_image before: Build sales automation for every lead, deal, and renewal, with Emergent
- share_image after: Build sales automation for every lead, deal, and renewal, with Emergent
- tab_image_1 before: Five new demo requests are routed by company size and region; Corbel, with 850 employees in the West, goes to enterprise rep Marco Rossi, and the two smaller companies go to the next reps in the rotation.
- tab_image_1 after: Five new demo requests are routed by company size and region; Corbel, with 850 employees in the West, goes to enterprise rep Marco Albani, and the two smaller companies go to the next reps in the rotation.
- tab_image_2 before: A post-demo sequence for Initech sent the recap on day 0 and a second email on day 3; with no reply by day 7, rep Dana Ruiz gets a call task as a Slack direct message, and any reply or booked meeting ends the sequence.
- tab_image_2 after: A post-demo sequence for Brockway sent the recap on day 0 and a second email on day 3; with no reply by day 7, rep Dana Baek gets a call task as a Slack direct message, and any reply or booked meeting ends the sequence.
- tab_image_3 before: Open deals are checked each morning for days since the last touch; Pinecrest, a $36,000 deal that reached 14 days without a touch today, is flagged and sent to owner Dana Ruiz with the last email sent, before Friday's forecast call.
- tab_image_3 after: Open deals are checked each morning for days since the last touch; Alderton, a $36,000 deal that reached 14 days without a touch today, is flagged and sent to owner Dana Baek with the last email sent, before Friday's forecast call.
- tab_image_4 before: Four accounts inside the 90-day renewal window are listed for account manager Priya Shah, who gets them as a Slack direct message; Tidewater entered the window this week and gets one renewal deal in HubSpot.
- tab_image_4 after: Four accounts inside the 90-day renewal window are listed for account manager Priya Basu, who gets them as a Slack direct message; Bracken Freight entered the window this week and gets one renewal deal in HubSpot.

## 20261012-sales-automation-B-QCA1stocknam-2 (P1, B-QCA1stocknam, fix-by-writer, fixed)
- field: tab_image_2
- caught by: B-QCA1stocknam (Layer B): Tab 2 image and its alt text name the post-demo account Initech.
- live text: A post-demo sequence for Initech sent the recap on day 0 ... / Initech demo, Oct 6 / Call Initech today

## 20261012-sales-automation-B-QCA1stocknam-3 (P1, B-QCA1stocknam, fix-by-writer, fixed)
- field: tab_image_4
- caught by: B-QCA1stocknam (Layer B): Tab 4 image lists Acme Corp among the renewal accounts.
- live text: AC Acme Corp  $18,000 a year, no open tickets  48 days

## 20261012-sales-automation-B-DECISIONS202-1 (P1, B-DECISIONS202, proposed)
- field: image_brief
- caught by: B-DECISIONS202 (Layer B): Images and alts reuse persona and company names found across many specs: Priya Shah (19 others), Dana Ruiz (14), Pinecrest (12), Tidewater (10), plus Lumen Grove and Kestrel roots.
- live text: Pinecrest, a $36,000 deal ... sent to owner Dana Ruiz / account manager Priya Shah ... Tidewater entered the window this week

## 20261012-sales-automation-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: hero_description
- caught by: B-CONTENTDEFEC (Layer B): The hero subhead ends on a trailing qualifier after the main clause.
- live text: Build sales automation that assigns new leads by territory and messages the owner in Slack when a deal stalls, beside your CRM.

## 20261012-sales-automation-B-HUBRULES2bsu-1 (P2, B-HUBRULES2bsu, backlog)
- field: features_subheading
- caught by: B-HUBRULES2bsu (Layer B): 'Below are six parts of that job' is a signpost sentence that reads machine-written.
- live text: Sales automation hands the repeat steps of a deal to software. Below are six parts of that job, each running as code your team owns.

## 20261012-sales-automation-B-HUBRULES2bCO-1 (P2, B-HUBRULES2bCO, backlog)
- field: faq
- caught by: B-HUBRULES2bCO (Layer B): FAQ 3 and FAQ 8 end on link-carrier sentences; both targets are pending, so the live sentences are orphans.
- live text: Keeping CRM fields current without manual entry is a separate CRM automation build. / ... start with a lead nurturing workflow.

## 20261012-sales-automation-B-QCA1stocknam-4 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): The sitewide 'More things you can build' component draws the stock name Acme Corp on the AI CRM Builder card thumbnail; it is outside the CMS and the hub collections.
- live text: AI CRM Builder ... Lead / Proposal / Won ... AC Acme Corp $24,000 Proposal

## 20261012-sales-automation-B-HUBRULES2bDE-1 (P1, B-HUBRULES2bDE, proposed)
- field: template
- caught by: B-HUBRULES2bDE (Layer B): Sitewide testimonial strip uses textbook generated persona names and companies on every page; needs Divit to confirm they are real customers or replace them.
- live text: Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, LoopDesk

## 20261012-sales-automation-B-layout390px-1 (P2, B-layout390px, backlog)
- field: template
- caught by: B-layout390px (Layer B): At 390 px the white hero subhead sits on the light sky with weak contrast, and the breadcrumb wraps into three narrow columns.
- live text: HOME / AI AUTOMATION BUILDER / ... (wrapped into 3-line columns); hero description low contrast over clouds
