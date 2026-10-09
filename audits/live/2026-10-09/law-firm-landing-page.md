# /ai-landing-page-builder/law-firm-landing-page: live audit 2026-10-09

Base: https://emergent.sh

## 20261009-law-firm-landing-page-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261009-law-firm-landing-page-A10-faq-schema-1 (P1, A10-faq-schema, not-an-issue, not-an-issue (DECISIONS 2026-10-06))
- field: template
- caught by: A10-faq-schema (Layer A): no FAQPage JSON-LD on the page (not needed: DECISIONS 2026-10-06)

## 20261009-law-firm-landing-page-B-HUBRULES2aco-1 (P1, B-HUBRULES2aco, fix-by-writer, fixed)
- field: faq
- caught by: B-HUBRULES2aco (Layer B): FAQ 7 renders the pending-link anchor as plain text with the acronym in lowercase, right after 'PPC landing pages' in the same answer.
- live text: The same habits apply to any ppc landing page: one keyword theme and one form.
- faq before: window.awbFAQ = {"heading": "Law Firm Page Questions, Answered", "items": [{"q": "What is a law firm landing page?", "a": "A law firm landing page is a single page built for one practice area and one goal, like a free case review for car crash victims. It has no site menu, and its form feeds the firm's intake. Ads and local search results point to it instead of the home page."}, {"q": "How do you design a landing page for lawyers?", "a": "Start with one case type, then put that case type, the at
- faq after: window.awbFAQ = {"heading": "Law Firm Page Questions, Answered", "items": [{"q": "What is a law firm landing page?", "a": "A law firm landing page is a single page built for one practice area and one goal, like a free case review for car crash victims. It has no site menu, and its form feeds the firm's intake. Ads and local search results point to it instead of the home page."}, {"q": "How do you design a landing page for lawyers?", "a": "Start with one case type, then put that case type, the at
- feature_4 before: Copy and fee changes by message Ask Emergent to raise the consult fee, add a Spanish version or swap the headshot. The page updates at the same address, and inquiries saved before the change stay in the table.
- feature_4 after: Copy and fee changes by message Ask Emergent to raise the consult fee, add a Spanish version, or swap the headshot. The page updates at the same address, and inquiries saved before the change stay in the table.
- howto_step_5_des before: A phone number, the type of case and one qualifying answer cover most first calls. Leave the full story for the consultation, where an attorney can ask follow-up questions and explain what the firm does with the answers.
- howto_step_5_des after: A phone number, the type of case, and one qualifying answer cover most first calls. Leave the full story for the consultation, where an attorney can ask follow-up questions and explain what the firm does with the answers.
- meta_description before: Build a law firm landing page for each practice area, with intake questions, a conflict check and every inquiry routed to the right attorney.
- meta_description after: Build a law firm landing page for each practice area, with intake questions, a conflict check, and every inquiry routed to the right attorney.

## 20261009-law-firm-landing-page-B-DECISIONS202-1 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: meta_description
- caught by: B-DECISIONS202 (Layer B): Three-item list without the serial comma.
- live text: with intake questions, a conflict check and every inquiry routed to the right attorney.

## 20261009-law-firm-landing-page-B-DECISIONS202-2 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: feature_4
- caught by: B-DECISIONS202 (Layer B): Three-item list without the serial comma (body 177 -> 178 chars, within limits).
- live text: Ask Emergent to raise the consult fee, add a Spanish version or swap the headshot.

## 20261009-law-firm-landing-page-B-DECISIONS202-3 (P1, B-DECISIONS202, fix-by-writer, fixed)
- field: howto_step_5_des
- caught by: B-DECISIONS202 (Layer B): Three-item list without the serial comma.
- live text: A phone number, the type of case and one qualifying answer cover most first calls.

## 20261009-law-firm-landing-page-B-DECISIONS202-4 (P2, B-DECISIONS202, backlog)
- field: mockup
- caught by: B-DECISIONS202 (Layer B): Visible tab prompt (injuryCaseReview) lists three asks without the serial comma. (mockup prompts are not rendered since the hero redesign; fix at next rework)
- live text: Ask whether they were injured, which county the crash happened in and whether a lawyer already represents them.

## 20261009-law-firm-landing-page-B-HUBRULES2a-1 (P2, B-HUBRULES2a, backlog)
- field: faq
- caught by: B-HUBRULES2a (Layer B): FAQ 3 comparison is loosely attached: 'Like any lead generation landing page' modifies 'the form', not the page.
- live text: Like any lead generation landing page, the form asks only what the first call needs.
