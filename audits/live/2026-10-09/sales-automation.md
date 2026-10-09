# /ai-automation-builder/sales-automation: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-sales-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-sales-automation-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-sales-automation-B-DECISIONS202-1 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: faq#3
- caught by: B-DECISIONS202 (Layer B): The crm-automation link was stripped because that page is not live, so "see CRM automation" sends readers to nothing.
- live text: For keeping CRM fields current without manual entry, see CRM automation.
- faq before: window.awbFAQ = {"heading": "Sales Automation Questions, Answered", "items": [{"q": "What is sales automation?", "a": "Sales automation is software that acts on events in a sales process: a form fill, a stage change, a date on a contract. Each event fires a step a rep would otherwise do by hand, like assigning the lead or sending the next email. Conversations with buyers stay with people."}, {"q": "How do you set up sales process automation?", "a": "Write each rule as one sentence that says what
- faq after: window.awbFAQ = {"heading": "Sales Automation Questions, Answered", "items": [{"q": "What is sales automation?", "a": "Sales automation is software that acts on events in a sales process: a form fill, a stage change, a date on a contract. Each event fires a step a rep would otherwise do by hand, like assigning the lead or sending the next email. Conversations with buyers stay with people."}, {"q": "How do you set up sales process automation?", "a": "Write each rule as one sentence that says what
- feature_1 before: Every new lead assigned on arrival Demo requests, chat leads and event scans land in one table. Each new lead goes to a rep by territory or by round-robin rotation. The queue shows whose turn is next.
- feature_1 after: Every new lead assigned on arrival Demo requests, chat leads, and event scans land in one table. Each new lead goes to a rep by territory or by round-robin rotation. The queue shows whose turn is next.
- feature_6 before: Territory rules stored as readable code Routing tables, cadences and the dashboard export to GitHub as code on paid plans. When a rep leaves, moving their accounts to a new owner is a prompt or a pull request.
- feature_6 after: Territory rules stored as readable code Routing tables, cadences, and the dashboard export to GitHub as code on paid plans. When a rep leaves, moving their accounts to a new owner is a prompt or a pull request.
- h1 before: Build Sales Automation for Every Lead, Deal and Renewal
- h1 after: Build Sales Automation for Every Lead, Deal, and Renewal
- share_image before: Build sales automation for every lead, deal and renewal, with Emergent
- share_image after: Build sales automation for every lead, deal, and renewal, with Emergent

## 20261009-sales-automation-B-DECISIONS202-2 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: h1
- caught by: B-DECISIONS202 (Layer B): The H1 list has no serial comma (the primary keyword is unchanged by the fix).
- live text: Build Sales Automation for Every Lead, Deal and Renewal

## 20261009-sales-automation-B-DECISIONS202-3 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: share_image alt
- caught by: B-DECISIONS202 (Layer B): A list in the alt text has no serial comma.
- live text: Build sales automation for every lead, deal and renewal, with Emergent

## 20261009-sales-automation-B-DECISIONS202-4 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_1
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: Demo requests, chat leads and event scans land in one table.

## 20261009-sales-automation-B-DECISIONS202-5 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_6
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: Routing tables, cadences and the dashboard export to GitHub as code on paid plans.

## 20261009-sales-automation-B-DECISIONS202-6 (P2, B-DECISIONS202, backlog)
- field: mockup
- caught by: B-DECISIONS202 (Layer B): A list of actions in the inboundLeads prompt has no serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- live text: rotate the rest among the team, write the owner to HubSpot and send the rep a Slack direct message

## 20261009-sales-automation-H3-sweep-1 (P1, H3-sweep, fix-by-writer, fixed)
- field: meta_description
- caught by: H3-sweep (Layer sweep): serial comma missing (widened H3 detector, golden h3-gap-*); fixed by serial_comma.fix
- meta_description before: Describe your process and get sales automation that routes leads, follows up after demos, flags stalled deals and opens renewals. Free to start.
- meta_description after: Describe your process and get sales automation that routes leads, follows up after demos, flags stalled deals, and opens renewals. Free to start.
