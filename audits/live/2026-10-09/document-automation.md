# /ai-automation-builder/document-automation: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-document-automation-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-document-automation-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-document-automation-B-HUBRULES8SEV-1 (P0, B-HUBRULES8SEV, fix-by-writer, fixed)
- field: faq#4
- caught by: B-HUBRULES8SEV (Layer B): Calling Gavel "often" the best tool for law firms is an unsourced market claim about a named company; domain_sources only says what Gavel does.
- live text: For a law firm, the best document automation tool is often Gavel, which drives legal templates from a questionnaire without code.
- faq before: window.awbFAQ = {"heading": "Document Automation, Answered", "items": [{"q": "What is document automation?", "a": "Document automation is software that produces and handles documents from data and rules instead of by hand. A quick test for where it pays off: does someone still retype values that already exist in another system? The drafting half has an older name: document assembly."}, {"q": "How do you build an automated document workflow?", "a": "Pick one document, find where each of its value
- faq after: window.awbFAQ = {"heading": "Document Automation, Answered", "items": [{"q": "What is document automation?", "a": "Document automation is software that produces and handles documents from data and rules instead of by hand. A quick test for where it pays off: does someone still retype values that already exist in another system? The drafting half has an older name: document assembly."}, {"q": "How do you build an automated document workflow?", "a": "Pick one document, find where each of its value
- tab_content_3 before: Catch an underinsured vendor before the job starts Vendors upload insurance certificates to Northwind Properties, and the app reads the policy number, expiry date and per-occurrence limit. Ridgeline Roofing's certificate lists $500,000 per occurrence, under its contract's $1,000,000 minimum. The vendor is asked for a new one, and the job stays on hold until one passes.
- tab_content_3 after: Catch an underinsured vendor before the job starts Vendors upload insurance certificates to Northwind Properties, and the app reads the policy number, expiry date, and per-occurrence limit. Ridgeline Roofing's certificate lists $500,000 per occurrence, under its contract's $1,000,000 minimum. The vendor is asked for another, and the job stays on hold until one passes.

## 20261009-document-automation-B-DECISIONS202-1 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: faq#10
- caught by: B-DECISIONS202 (Layer B): The document-approval-workflow link was stripped because that page is not live, so the sentence now points readers to a guide that does not exist.
- live text: For routing by role or amount, see the document approval workflow guide.

## 20261009-document-automation-B-DECISIONS202-2 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: tab_content_3
- caught by: B-DECISIONS202 (Layer B): A three-item list has no serial comma.
- live text: the app reads the policy number, expiry date and per-occurrence limit

## 20261009-document-automation-B-DECISIONS202-3 (P2, B-DECISIONS202, backlog)
- field: mockup
- caught by: B-DECISIONS202 (Layer B): Two lists in the visible tab prompts have no serial comma (engagementLetters, offerLetters). (mockup prompts are not rendered since the hero redesign; fix at next rework)
- live text: their name, contact details, matter type and a short description | the role, start date, manager and base salary

## 20261009-document-automation-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: faq item 3
- caught by: B-CONTENTDEFEC (Layer B): "The most common use" is an unsourced ranking.
- live text: Reading loan applications, bills of lading, and supplier forms into named fields is the most common use

## 20261009-document-automation-B-HUBRULES8-1 (P2, B-HUBRULES8, backlog)
- field: faq item 1
- caught by: B-HUBRULES8 (Layer B): The source says "also known as"; "older name" goes beyond it (noted at review, still open).
- live text: The drafting half has an older name: document assembly.
