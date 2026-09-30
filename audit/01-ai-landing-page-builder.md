# AI Landing Page Builder hub: pre-launch audit

**Page:** `/ai-landing-page-builder` (page ID `6aaa658ea6d39733443fe69b`, Draft)  
**Audited:** 30 Sep 2026, against live Designer content, live schema, and vendor pricing checked this week.

## Scorecard

| Priority | Count |
| --- | --- |
| P0 fact | 2 |
| P1 SEO | 3 |
| P1 readability | 3 |
| P2 polish | 2 |

P0 = factually wrong or unverifiable claim (must fix before launch). P1 = ranking or readability. P2 = polish.

## 1. Meta title, description, OG

| Field | Current | Chars | Proposed | Chars | Why |
| --- | --- | --- | --- | --- | --- |
| SEO title | AI Landing Page Builder: Prompt to Live Page / Emergent | 55 | Free AI Landing Page Builder: Live in Minutes / Emergent | 56 | Leads with 'free' (the top modifier in this SERP) plus a speed promise; keeps the exact keyword at the front. |
| Meta description | Emergent is an AI landing page builder that turns one prompt into a live page, a working form, and a database you own, on your domain. Free to start. | 149 | Keep |  | 148 chars, keyword in first 40, moat and CTA present, no vendor numbers. Keep. |
| OG title | AI Landing Page Builder / Emergent | 34 | Keep |  | Fine for share cards. |
| OG image | Generic emergent.webp | 21 | Hub-specific 1200×630 (pipeline can make it) | 44 | Share cards all look identical across the 4 hubs. Optional. |

## 2. Findings, section by section

| # | Priority | Section / element | Current text | Issue | Proposed text | Len |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P1 SEO | Hero H1 | Ship a landing page today. Own every lead it captures. | The H1 carries no form of the primary keyword ('AI landing page builder'). The H1 is the strongest on-page relevance signal after the title. | Build a landing page with AI. Own every lead. | ✅ (45) |
| 2 | P1 readability | 3-column cards: heading | Three things other landing page builders gate, meter, or keep. | 63 chars, so it wraps to 3 lines. | What other landing page builders gate or meter | ✅ (46) |
| 3 | P1 readability | Features: heading | Everything an AI landing page builder should ship with, in one build. | 69 chars, 3 lines. | Everything a landing page needs, in one build | ✅ (45) |
| 4 | P0 fact | Features: Feature 2 | Every form writes to a Postgres table in your project. | 'Postgres' is not verified as Emergent's default database. The approved claim is 'a database you own'. There is also a stray blank line (three line breaks) after the title. | Every form writes to a database in your project that you own. (Also remove the extra blank line.) | 97 |
| 5 | P1 readability | Integrations: H2 | Every tool your landing page [line break] needs to talk to | The forced break leaves a 29-char first line, which re-wraps to 3 lines. | Every tool your landing page connects to | ✅ (40) |
| 6 | P1 SEO | Comparison: H2 | The best landing page builders compared, with the numbers | 58 chars, 3 lines. After the table was cut to 5 rows it carries fewer numbers. | The best landing page builders, compared | ✅ (40) |
| 7 | P0 fact | Comparison: subheading | Based on each vendor's published 2026 plans. Each use-case page compares Emergent with the tools people usually pick for that job. | The second sentence is now false: child pages show this same table. | Based on each vendor's published plans, checked September 2026. | ✅ (63) |
| 8 | P2 polish | How-to: Step 01 description | …Drag-and-drop tools are quick but keep your leads locked inside… | 'Locked inside' is overstated; Unbounce exports and integrates leads. | …Drag-and-drop tools are quick but store your leads in their own system… | 72 |
| 9 | P2 polish | How-to: Step 03 description | …ready for the A/B tests in step seven.[newline] | Stray trailing line break in the prop. | Same text without the trailing line break. | 42 |
| 10 | P1 SEO | How-to: heading | How to create a landing page | Good. It matches the 'how to create a landing page' query. Keep. | (remove) |  |

## 4. Verified as accurate (no change)

- Unbounce Starter 500 visitors, Build 20,000, Experiment 30,000; A/B testing from Experiment at $112/mo annual; 14-day trial; $22/mo Starter and $74/mo Build on annual billing (vendor pricing, verified Aug 2026). The comparison table and the FAQ 'How much does a landing page builder cost?' are accurate.
- All 14 FAQ answers checked. No false claims found. Emergent claims (custom domain uses credits, code export, free tier) match approved wording.
- Meta description, OG copy and breadcrumb schema are consistent.

## 5. Housekeeping

- Webflow page name reads 'AI landing page Builder' (inconsistent casing). This is internal only, but fix to 'AI Landing Page Builder'.
