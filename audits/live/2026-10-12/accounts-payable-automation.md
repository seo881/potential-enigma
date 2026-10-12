# /ai-automation-builder/accounts-payable-automation: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-accounts-payable-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-accounts-payable-automation-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, proposed)
- field: image_brief.tabs[2] rows; image_brief.tabs[3].hero (uc-3.svg, uc-4.svg)
- caught by: B-QCA1reusedpe (Layer B): The approver initials in two tab images are reused personas: 'M. Chen' appears on 4 other pages and 'M. Rossi' on 2 others (customer-satisfaction is live).
- live text: M. Rossi | Calla Brannock, approved by M. Chen

## 20261012-accounts-payable-automation-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): The sitewide 'More things you can build' AI CRM Builder card draws 'Acme Corp', a stock name now on Divit's AI-tell list. It shows on every child page in this batch. It is a template component outside the child collections.
- live text: AC Acme Corp $24,000 Proposal
