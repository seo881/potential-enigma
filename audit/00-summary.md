# Build hubs: pre-launch audit summary (4 hubs)

**Date:** 30 Sep 2026.
**Scope:** every visible string on the 4 hub pages (component props, page sections, table cells, FAQs), SEO meta, OG, and JSON-LD.
**Method:**
- Live Designer and CMS reads.
- Every competitor figure re-checked against vendor pricing pages or reviews dated June–Sept 2026.
- Every Emergent claim checked against previously approved wording.
- Heading lengths measured against the 2-line wrap on these pages.

Per-hub files: `01-ai-landing-page-builder.md`, `02-ai-form-builder.md`, `03-ai-automation-builder.md`, `04-ai-survey-and-quiz-builder.md`. Each lists the current text, the issue and the exact rewrite.

## Totals
| Hub | P0 fact | P1 SEO | P1 readability | P2 polish | FAQ edits |
|---|---|---|---|---|---|
| AI Landing Page Builder | 2 | 3 | 3 | 2 | 0 |
| AI Form Builder | 4 | 2 | 3 | 1 | 1 |
| AI Automation Builder | 10 | 4 | 2 | 2 | 4 |
| AI Survey and Quiz Builder | 6 | 3 | 4 | 2 | 3 |

**P0** means false or unverifiable as written; these must be fixed before launch.

## Cross-hub issues (fix once, applies to several pages)
1. **P0: the comparison subheading is now false on all 4 hubs.** "Each use-case page compares Emergent with the tools people usually pick for that job" stopped being true when child pages took the hub's table. Replace it with: *"Based on each vendor's published plans, checked September 2026."*
2. **P0: "Postgres" is unverified (LP, Form, Survey and Quiz).** Five cards and features say responses write to "a Postgres table". Emergent's default database could not be confirmed as Postgres. The rewrites use the approved phrasing "a database in your project" / "a database you own". **If you confirm Postgres is accurate, say so and I'll keep it.**
3. **P0: Zapier ships more than workflows (AI Automation Builder hub and the Approval Workflow child page).** Zapier's plans bundle Tables (a database) and Interfaces (forms and pages). So "The workflow only", "every other tool…" and "Zapier and Make expect you to bring your own" are rebuttable.
   - The rewrites keep the moat: the app, data and code are **yours, as code**, not hosted inside the vendor.
   - The same "What you get" row sits on the Approval Workflow page's table, so it gets fixed in both places.
4. **P0: Interact's behaviour at the cap is overstated (Survey and Quiz hub and the Customer Satisfaction Survey page).** Only the Free plan is confirmed to pause, at 100 completions; paid plans cap leads, but the overage behaviour isn't published. The table, value card and FAQ are all fixed.
5. **P1 SEO: no H1 contains the primary keyword.** Each hub gets an H1 that includes it and keeps the approved voice. Form's H1 was approved by you on 24 Sep, so that one is your call.
6. **P1 readability: 13 H2s wrap to 3 or 4 lines.**
   - Measured on these pages, a section H2 fits 2 lines at 48 characters or fewer (about 24–26 per line). Every rewrite is at or under that, checked by script.
   - Three integrations H2s also have a forced line break that makes the first line too long; the rewrites drop the break.
7. **P1 SEO: related articles on the AI Automation Builder and Survey and Quiz hubs sort oldest-first.** LP and Form are newest-first, the approved setting.
8. **Schema check.**
   - Each hub's JSON-LD has WebPage, FAQPage and BreadcrumbList.
   - The WebPage `publisher` points to `https://emergent.sh/#organization`, but that Organization node isn't in these pages' JSON-LD. If the site's global head code doesn't define it, the reference dangles. I'll check the published HTML after launch, or add Organization and WebSite nodes now if you prefer.
   - FAQPage stays valuable for AI answer engines. Since Google's 2023 change, it rarely produces FAQ rich results for commercial sites, so don't expect SERP FAQ snippets.
   - **Any FAQ edit means rebuilding the FAQPage schema word for word.** I'll do that in the same pass.
9. **Sitewide components (not changed, flagged only):**
   - `section_stats` says "200+ Countries Globally Reached". There are about 195 countries, so it only holds if it means countries *and territories*. Worth confirming with whoever owns that number.
   - `Global / Pricing` says "we've got you covered", which clashes with the "Emergent's, never our" voice rule.
   - Both components are shared site-wide, so changing either touches other pages. That needs your explicit go.

## Meta titles (proposed; all 60 characters or fewer)
| Hub | Current | Proposed |
|---|---|---|
| LP | AI Landing Page Builder: Prompt to Live Page \| Emergent (55) | Free AI Landing Page Builder: Live in Minutes \| Emergent (56) |
| Form | AI Form Builder: Free Online Form Builder \| Emergent (52) | Free AI Form Builder With Unlimited Responses \| Emergent (56) |
| AI Automation Builder | Workflow Automation Software, from a Prompt \| Emergent (54) | Workflow Automation Software With No Task Caps \| Emergent (57) |
| Survey and Quiz | AI Survey Maker, Quiz Maker & Poll Maker in One \| Emergent (58) | Free AI Survey Maker, Quiz Maker & Poll Maker \| Emergent (56) |

- The logic: the head keyword stays first, then "Free" (the dominant modifier on all four SERPs) or the moat versus the category leader (response caps for Typeform and Jotform, task caps for Zapier and n8n).
- All 4 meta descriptions are already 142–149 characters, keyword-first, free of vendor numbers and end with a CTA. **Keep them.**

## Verified accurate (no change needed)
Zapier (Free 100 tasks; Pro $19.99/mo annual, 750 tasks; 1.25× overage) · Make (Free 1,000 credits, 2 scenarios) · n8n (Starter 2,500 executions; no free cloud tier; CE free) · Typeform (10 / 100 / 1,000 / 10,000; stops at cap; Basic $28 annual) · Jotform (5 forms & 100 free; 1,000 / 2,500 / 10,000; payments metered; Bronze $34 annual) · SurveyMonkey (25/survey free; Advantage 15,000/yr at $46 annual; $0.15 overage) · Interact (Lite 500 leads $27, Growth 2,000 $53) · Unbounce (Starter 500 visitors $22 annual; Build 20,000 $74; Experiment 30,000 $112, where A/B starts; 14-day trial).

**Conflicting sources:** Make Core is quoted at $9, $12 or $16/mo depending on source and billing. The FAQ keeps $9 and adds "on annual billing" (two September 2026 captures of make.com show $9 annual). No Make price appears in the tables.

## Decisions needed from you
1. The Postgres claim: confirm it, or use "a database you own" (my recommendation).
2. The Form H1 change (you approved the current one).
3. Whether to fix the two sitewide component issues, which would touch other pages.

Everything else is ready to apply as written. The plan:
1. Apply all P0 and P1 fixes and the FAQ edits.
2. Rebuild the FAQ schema to match.
3. Read everything back.
4. Commit the old values for rollback.

## Sources checked (Sept 2026)
- **Zapier:** nocode.mba, toolradar, eesel, Zapier blog (for Tables and Interfaces).
- **Make:** latenode (read from make.com 14 Sep), jetadmin (captured 26 Sep), Zapier blog.
- **n8n:** hackceleration (from n8n.io/pricing), axshul, cloudzero.
- **Typeform:** toolradar, automationatlas (July 2026), meetergo.
- **Jotform:** Jotform Answers, formnx (June 2026), automationatlas.
- **SurveyMonkey:** research.net pricing page (SurveyMonkey), formnx, surveysparrow.
- **Interact:** tryinteract.com/ai-info, uplup (19 July 2026), getpulsesignal.
- **Unbounce:** casrai (18 Aug 2026), hackceleration, ppc.io (30 Aug 2026).
