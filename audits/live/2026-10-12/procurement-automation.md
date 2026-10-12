# /ai-automation-builder/procurement-automation: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-procurement-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-procurement-automation-B-HUBRULES2bCO-1 (P2, B-HUBRULES2bCO, backlog)
- field: faq
- caught by: B-HUBRULES2bCO (Layer B): Two answers close on a sentence that exists to carry a sibling link (FAQ 4, 8); the PO link is pending, so FAQ 4's tail is an orphan on the live page.
- live text: Turning an approved request into a supplier order is the job of purchase order automation. / That end of the cycle is accounts payable automation.

## 20261012-procurement-automation-B-grammarcompo-1 (P2, B-grammarcompo, backlog)
- field: faq
- caught by: B-grammarcompo (Layer B): 'procure to pay' is written without hyphens in FAQ 2 and FAQ 8; the standard term is procure-to-pay (kept unhyphenated for the secondary keyword).
- live text: How do you build procure to pay automation? ... Procure to pay runs through requisition, approval, purchase order, goods receipt

## 20261012-procurement-automation-B-DECISIONS202-1 (P2, B-DECISIONS202, backlog)
- field: tab_content_4
- caught by: B-DECISIONS202 (Layer B): 'Brightwell Office' also appears in reference-check-form and quote-form; 'Cedar' (Cedar Lab Supply) is a name root in 37 specs.
- live text: Brightwell Office holds the furniture contract at $455 for the same model.

## 20261012-procurement-automation-B-QCA1stocknam-1 (P1, B-QCA1stocknam, proposed)
- field: template
- caught by: B-QCA1stocknam (Layer B): The sitewide 'More things you can build' component draws the stock name Acme Corp on the AI CRM Builder card thumbnail; it is outside the CMS and the hub collections.
- live text: AI CRM Builder ... Lead / Proposal / Won ... AC Acme Corp $24,000 Proposal

## 20261012-procurement-automation-B-HUBRULES2bDE-1 (P1, B-HUBRULES2bDE, proposed)
- field: template
- caught by: B-HUBRULES2bDE (Layer B): Sitewide testimonial strip uses textbook generated persona names and companies on every page; needs Divit to confirm they are real customers or replace them.
- live text: Alex Rivera, Founder, TaskFlow / Maya Chen, Product Lead, BrightSuite / Jordan Patel, Co-founder, LoopDesk

## 20261012-procurement-automation-B-layout390px-1 (P2, B-layout390px, backlog)
- field: template
- caught by: B-layout390px (Layer B): At 390 px the white hero subhead sits on the light sky with weak contrast, and the breadcrumb wraps into three narrow columns.
- live text: HOME / AI AUTOMATION BUILDER / ... (wrapped into 3-line columns); hero description low contrast over clouds
