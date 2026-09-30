# AI Form Builder hub: pre-launch audit

**Page:** `/ai-form-builder` (page ID `6aabb4c5789871e91d60f6f9`, Draft)  
**Audited:** 30 Sep 2026, against live Designer content, live schema, and vendor pricing checked this week.

## Scorecard

| Priority | Count |
| --- | --- |
| P0 fact | 4 |
| P1 SEO | 2 |
| P1 readability | 3 |
| P2 polish | 1 |

P0 = factually wrong or unverifiable claim (must fix before launch). P1 = ranking or readability. P2 = polish.

## 1. Meta title, description, OG

| Field | Current | Chars | Proposed | Chars | Why |
| --- | --- | --- | --- | --- | --- |
| SEO title | AI Form Builder: Free Online Form Builder / Emergent | 52 | Free AI Form Builder With Unlimited Responses / Emergent | 56 | Replaces the repeated 'Form Builder' with the strongest differentiator in this SERP (Typeform and Jotform cap responses). Keyword stays first. |
| Meta description | The online form builder that writes every response to a database you own. Describe the form, get the fields, logic, and integrations. Free to start. | 148 | Keep |  | 149 chars, good. Keep. |
| OG title | AI Form Builder / Emergent | 26 | Keep |  | Fine. |

## 2. Findings, section by section

| # | Priority | Section / element | Current text | Issue | Proposed text | Len |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | P1 SEO | Hero H1 | Build any form in minutes. Own every response. | No 'AI form builder' or 'form builder' in the H1. You approved this line on 24 Sep, so it's your call. The rewrite adds 'with AI' and keeps the rhythm. | Build any form with AI. Own every response. | ✅ (43) |
| 2 | P1 readability | 3-column cards: heading | Three things Typeform and Jotform meter or gate, and Google Forms can't do. | 75 chars, 3 lines. | What Typeform and Jotform meter or gate | ✅ (39) |
| 3 | P1 readability | 3-column cards: subheading | The values that make Emergent different from every metered, capped, vendor-locked online form builder. | 'The values' reads oddly. Stacked adjectives. | Where Emergent differs from Typeform, Jotform, and Google Forms: no response caps, no plan gates, and a database you own. | ✅ (121) |
| 4 | P0 fact | Value card 1: text | …Emergent writes every response to a Postgres table in your project… | 'Postgres' is unverified (see summary). | …Emergent writes every response to a database in your project that you own… | 75 |
| 5 | P0 fact | Value card 2: text | …included from the free tier. Other form makers gate these behind higher plans with monthly response caps. | Jotform includes conditional logic and payments on its free plan (payments metered at 10/mo), and Google Forms has free logic, so 'gate these behind higher plans' is inaccurate. | …included from the free tier. Jotform meters payment submissions on every plan, and Typeform stops collecting at its monthly response cap. | 138 |
| 6 | P1 readability | Features: heading | Everything an AI form builder should ship with, in one build. | 61 chars, 3 lines. | Everything a form needs, in one build | ✅ (37) |
| 7 | P0 fact | Features: Feature 2 | Every submission from your online forms writes to a Postgres table in your project. | 'Postgres' is unverified. | Every submission from your online forms writes to a database in your project. | 77 |
| 8 | P0 fact | Comparison: subheading | Based on each vendor's published 2026 plans. Each use-case page compares Emergent with the tools people usually pick for that job. | The second sentence is now false: child pages show this same table. | Based on each vendor's published plans, checked September 2026. | ✅ (63) |
| 9 | P1 SEO | How-to: heading | How to create a form | 'How to create an online form' matches a higher-intent query and the page's 'online form builder' term. | How to create an online form | ✅ (28) |
| 10 | P2 polish | How-to: Step 01 description | …Drag and drop tools are quick but meter your responses… | Google Forms doesn't meter responses. | …Drag and drop tools are quick, and most meter your responses… | 62 |

## 3. FAQ changes (the FAQPage schema must be rebuilt word-for-word after these land)

| # | Question | Current (excerpt) | Issue | Proposed answer |
| --- | --- | --- | --- | --- |
| 1 | Which AI form builder has conditional logic? | Typeform includes logic from its Basic plan. | Typeform's free plan includes basic logic; advanced logic starts at Plus. | Most AI form makers stop at generating fields. Emergent includes conditional fields, scoring, calculations, and routing on every plan. Typeform includes basic logic on every plan and advanced logic from Plus. Jotform includes conditions on all plans. Google Forms supports basic section branching. |

## 4. Verified as accurate (no change)

- Typeform: Free 10 responses/mo, Basic 100, Plus 1,000, Business 10,000; the form stops collecting at the cap; Basic $28/mo annual (July 2026 price rise).
- Jotform: Starter 5 forms and 100 submissions/mo; Bronze, Silver and Gold 1,000, 2,500 and 10,000; payments metered 10/100/250/1,000; Bronze $34/mo annual; forms stop at the cap.
- The comparison table's 5 rows are accurate.
- 'SOC 2 Type I and ISO 27001' matches approved wording.
