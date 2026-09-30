# "More things you can build" component (b4a27b0c-2847-3338-522f-2cf9e51e2671), edited 2026-09-30 at Divit's request
This is a component-definition edit. It affects every instance: the Testing page, the 4 child templates, and the hubs once they're placed. No classes were modified.

## Why the dashed divider misaligned
hub-card is a flex column and hub-card_links has margin-top:auto plus a dashed border-top, so the list is pinned to the card bottom. The divider only moved because some labels wrapped to 2 lines (e.g. "Project Management Web App Builder", 255px against about 169px available at a 992px viewport).
Fix: every label is now one line. I measured with Inter at 14/500 +4%; the worst new label is under 169px, so dividers align at every width.

## Labels (text block id → OLD → NEW); all in the component, links/hrefs unchanged
2687 Portfolio Website Builder → Portfolio website | 268b eCommerce Website Builder → Ecommerce website | 268f Restaurant Website Builder → Restaurant website
26a4 Food Delivery App Builder → Food delivery app | 26a8 Fitness App Builder → Fitness app | 26ac Ecommerce App Builder → Ecommerce app
26c1 Project Management Web App Builder → Project management | 26c5 Booking Web App Builder → Booking system | 26c9 Inventory Management Web App Builder → Inventory management
26de SaaS CRM Builder → CRM platform | 26e2 Project Management SaaS Builder → Project management | 26e6 HR Management SaaS Builder → HR management
26fb KPI Dashboard Builder → KPI dashboard | 26ff Sales Management Dashboard Builder → Sales dashboard | 2703 Executive Dashboard Builder → Executive dashboard
2718 Sales CRM Builder → Sales CRM | 271c Real Estate Investor CRM Builder → Investor CRM | 2720 Small Businesses CRM Builder → Small business CRM
2735 Customer Support Agent Builder → Support agent | 2739 Lead Generation Agent Builder → Lead generation agent | 273d (old not captured) → Recruiting agent
2752/2756/275a (old not captured) → Employee scheduling / Appointment booking / Shift scheduling
276f/2773/2777 (old not captured) → Support chatbot / Ecommerce chatbot / Real estate chatbot
All ids are prefixed b4a27b0c-2847-3338-522f-2cf9e51e…

## View-all (2693, 26b0, 26cd, 26ea, 2707, 2724, 2741, 275e, 277b): "View all N+ pages" → "View all pages". Each links to that builder's hub page.

## Descriptions (paragraph id: OLD → NEW)
2681 Build and publish responsive websites with AI, from landing pages to complete websites. → Responsive websites from a prompt, from a single page to a full site.
269e Create and launch mobile apps with AI, without the complexity of traditional app development. → Mobile apps for iOS and Android, built and launched from a prompt.
26bb Build and ship fully functional web apps with custom interfaces, logic, and workflows. → Web apps with real logic, data, and workflows, built from a prompt.
26d8 Build complete SaaS products with user accounts, subscriptions, dashboards, and core product workflows. → SaaS products with accounts, subscriptions, and dashboards built in.
26f5 Create interactive dashboards to visualize data, track KPIs, and manage business operations. → Live dashboards for your data, KPIs, and day-to-day operations.
2712 Build custom CRMs for managing contacts, leads, pipelines, campaigns, and automated workflows. → A CRM built around your contacts, pipeline, and workflows.
272f Create AI agents that can understand tasks, use tools, automate workflows, and work across your business. → AI agents that take on tasks, use your tools, and run workflows.
274c Build scheduling and booking systems that automate calendars, shifts, and reminders. → Scheduling and booking systems with calendars, shifts, and reminders.
2769 Build AI chatbots trained on your content and deploy them on your site or any channel. → Chatbots trained on your content, live on your site or any channel.

## Covers v6 imported (2026-09-30 ~16:50 IST), from commit c6f6988 images/hubcards/*.svg
New classes: hub-card_cover 302662bc-26d4-3668-c9a1-99676ba9a134 (full-bleed: width calc(100%+3rem), margins -1.5rem top/left/right, 5:2, cover, top radius calc(1.5rem-1px), 1px bottom hairline).
Combo: hub-card_icon-wrap.is-on-cover a3b55fb6-3132-dfc5-9d45-2dfc4f69debf (margin-top -1.75rem = half of the 3.5rem tile, white, shadow, z-index 1).
The card padding is 1.5rem at every breakpoint (verified), so the full-bleed maths holds on tablet and mobile.
| Card | cover image element | asset |
|---|---|---|
| Website 2679 | 9aa7074b-ed22-d167-377b-7526199ce57c | 6abcedb1379a0ba56f205081 |
| App 2696 | 09464781-8ba4-33ac-dd4e-8317c73a3a5a | 6abcedb8833dcc431b6cca45 |
| Web App 26b3 | bb8fad20-283d-82a1-a175-c2b32f497b03 | 6abcedc047b3694866ab7b8e |
| SaaS 26d0 | af003b35-6d99-adc4-2264-9c1e3cdcd61b | 6abcedc791766c45a2d0c914 |
| Dashboard 26ed | 020e4564-f072-febe-af57-0540caea6f97 | 6abcedce2b665aec4164eaad |
| CRM 270a | 9c779f56-ced3-15f8-2eb4-786cd4a68523 | 6abcedd60d27cf8d7db39cc1 |
| Agent 2727 | fbf5e402-d7e0-aa8b-ae66-c59ac22d792d | 6abcedde5eec0f9123bc001f |
| Schedule 2744 | 8b661772-7001-56a6-959a-ddc45464229d | 6abcede50c22665880035d84 |
| Chatbot 2761 | 7a1f54b6-7419-b52c-2681-2dd1f556e9de | 6abcededc2678fd8ec1356dc |
The icon wraps (267a, 2697, 26b4, 26d1, 26ee, 270b, 2728, 2745, 2762) now carry [hub-card_icon-wrap, is-on-cover].
Rollback: remove the 9 images; set the icon wraps back to [hub-card_icon-wrap].

## Anchors + links v2 (2026-09-30 ~17:35 IST), per Sannivas's URL list + the Top Pages sheet; every destination verified live in its CMS collection first
| Card | Anchor text | href |
|---|---|---|
| Website | Portfolio Website Builder · Ecommerce Website Builder · 3D Website Builder | /ai-website-builder/portfolio · /ecommerce · /3d (replaces restaurant) |
| App | Ecommerce App Builder · Game App Builder · Cryptocurrency Wallet App Builder | /ai-app-builder/ecommerce · /game · /cryptocurrency-wallet |
| Web App | Progressive Web App Builder · Python Web App Builder · Gaming Web App Builder | /ai-web-app-builder/progressive · /python · /gaming |
| SaaS | SEO SaaS Builder · Healthcare SaaS Builder · Marketing Automation SaaS Builder | /ai-saas-builder/seo · /healthcare · /marketing-automation |
| Dashboard | SEO Dashboard Builder · Marketing Dashboard Builder · KPI Dashboard Builder | /ai-dashboard-builder/seo · /marketing · /kpi |
| CRM | Marketing CRM Builder · Startup CRM Builder · Customer Support CRM Builder | /ai-crm-builder/marketing · /startups · /customer-support |
| Agent | SEO Agent Builder · Voice Agent Builder · Marketing Agent Builder | /ai-agent-builder/seo · /voice · /marketing |
| Schedule | Social Media Scheduler Builder · Course Schedule Planner Builder · Class Schedule Builder | /ai-schedule-builder/social-media · /course · /class |
| Chatbot | Lead Qualification Chatbot Builder · Customer Support Chatbot Builder · HR Chatbot Builder | /ai-chatbot-builder/lead-qualification · /customer-support · /hr |
Previous hrefs (for rollback): website portfolio/ecommerce/restaurant; app food-delivery/fitness/ecommerce; web app project-management/booking/inventory-management; saas crm/project-management/hr-management; dashboard kpi/sales-management/executive; crm sales/real-estate-investor/small-business; agent customer-support/lead-generation/recruiting; schedule employee/appointment/shift; chatbot customer-service/ecommerce/real-estate.

One-line guarantee: embed f11a368f-b61f-71b3-3a28-0292c126a76b (class hide) inside the component, scoped to .hub-cards_section:
- nowrap on links, with an ellipsis safety on the label.
- 992–1199px: the grid goes to 2 columns.
- 1200–1279px and ≤991px: 13px labels with 14px side padding.
- ≤479px: 12.5px labels.
Measured: the longest label (Marketing Automation SaaS Builder) is 242px at 14px. Text room: 252px at 1280 (3 columns), 230px at 768 (2 columns, 13px = 224), 220px at 360 (12.5px = 216).
Rollback: remove the embed.

## 17:5x IST: 3 columns restored (Divit). The grid is never overridden now. Embed f11a368f… uses fluid label sizes instead:
- 992–1279px: clamp(11px, 1.87vw − 8px, 14px), 12px side padding.
- 768–991px: clamp(11px, 2.8vw − 8.8px, 14px).
- ≤767px: clamp(11px, 5.6vw − 8.1px, 14px).
nowrap stays, with an ellipsis safety.

## 18:2x IST: final revisions
#1 Gap under the hero: new combo section_ai-hero.is-tight-bottom b9f6808f-d24f-8186-40bf-707a092cbdd7 (pb 2.5rem / tablet 2rem / mobile 1.5rem; the base class is 12/10/8/6rem).
Applied to the template heroes only: AAB cadd555f-…-d7cb, LP d8a90b8f-…-872b, Form 8722ef76-…-6799, SQB ba847d5e-…-f5cb.
Rollback: set their classes back to [section_ai-hero].
#3 Hub tables are hub-specific with named competitors (AAB: Zapier/Make/n8n; SQB: SurveyMonkey/Typeform/Interact). Hub embed fd1c2c5f-bfde-ed88-6f57-20e4ef04369f.
Proposed: per hub family, 5 rows chosen from the hub table, shared by the hub and all its child pages. Awaiting Divit.

## 18:3x IST
Hub gap (4 hubs only): the page-level style embed (class hide, prepended to main-wrapper 44671d6e-…) sets .section_product-hero {height:auto; padding-bottom:2.5rem} at ≥992px only.
The base class is height 53.125rem / pb 8rem. The shared hero component is untouched.
Embeds: AAB hub b8a2c5a1-3ec6-40a2-723c-10dd4df70442 · LP hub 25e43d56-05f5-0341-e6c8-27d56e18dd62 · SQB hub 3b7963ef-7faa-e842-3573-c6f15499aaca · Form hub 9dd01394-efab-aceb-cc72-c1b582223a38.
Rollback: remove the embed.
Hub tables → 5 rows, in embed fd1c2c5f-bfde-ed88-6f57-20e4ef04369f on all 4 hubs. Originals are saved in tables/<hub>_hub_original.html; new tables in tables/<hub>_hub_5row.html (generated by tables/build_tables.py from the live cells).
Rows kept (Emergent beats all 3 named competitors):
- AAB: How you build / What you get / Behavior at cap / AI and agent steps / Code ownership
- SQB: How you build / Response limits / Behavior at cap / Where responses live / Code ownership
- LP: How you build / Where submissions go / Visitor limits / A/B testing / Code ownership
- Form: How you build / Response limits / Where responses live / Payments in the form / Code ownership
Next: child items' acrm---why-emergent-table → same 5-row table as their hub (originals to be saved first). Then #2, the 7-step how-to.
Child tables (acrm---why-emergent-table), isDraft still true on every item:
- AAB approval-workflow 6aba7ac4…: now the AAB hub 5-row table (original in tables/aab_child_original.html).
- SQB customer-satisfaction 6aba7afb…: now the SQB hub 5-row table (original in tables/sqb_child_original.html).
- LP thank-you-page and Form creator-application: pending (back up first, then update).
Rollback: write the saved original HTML back into the field.
#2 plan: the hubs use component "Global / Sticky List" 9730644b-cdbc-73d2-8383-ad695f602395, with props Heading, How to create desc, HW_Step_01..07 Title/des (step 7 des = "Text").
The child templates use "Global / Sticky List (Icons)" 7a11ed6a… (4 steps).
There are 6 empty legacy CRM fields per collection (acrm---crm-builder, -by-industry-copy, -by-department, -by-department-copy, -by-business-size, -by-business-size-copy), null on the items. They free exactly the 6 slots needed for steps 5–7.
- LP thank-you-page 6ab5158e… and Form creator-application 6ab505a8…: now their hub's 5-row table (originals in tables/lp_child_original.html and tables/form_child_original.html). isDraft still true.
#3 COMPLETE: each hub and its child pages show the same 5-row named-competitor table; headings and subheadings stay page-specific.

## 18:4x IST: gap below the testimonials (section_stats → next section), our 8 pages only
The stats and features sections both use the same section-padding var top and bottom. Page-level rule: .section_stats{padding-bottom:1.5rem}.
- Hubs: added to the existing hub embeds (b8a2c5a1…, 25e43d56…, 3b7963ef…, 9dd01394…).
- Templates: new embeds (class hide, prepended to main-wrapper): AAB 42aee989-7399-cdba-6b8a-e6b43970f486 · LP cd6dd4bb-f02c-fece-484d-ed9f5dde5dcc · Form 33851df7-d88d-1492-6f50-7c340f86f0b2 · SQB 46520f82-686f-e070-d13f-57167c417482.
Rollback: remove the line or the embed.

## #2 fields: AI Automation Builder collection 6ab2470540448c8f7d1ccbf0 (was 60/60)
Deleted legacy CRM fields, all empty on the only item (verified 6aba7ac4… fieldData = null for all six), with no template binding:
- e539899bc3a5fbab16a79480da5bbaaa MultiReference "AATB - CRM by Industry" slug acrm---crm-builder → CRM builder coll 6a3a6beafcbf2114d556f4f4
- c7ca5e325fecd9527ed42253cd8fb5bc RichText "AATB - CRM by Industry Copy" slug acrm---crm-by-industry-copy
- 26cdea0f3ad0f21d289ab36ac2b38c4d MultiReference "AATB - CRM by Department" slug acrm---crm-by-department → 6a3a6beafcbf2114d556f4f4
- b99f8d98a32528409e9640bb5e8faa2d RichText "AATB - CRM by Department Copy" slug acrm---crm-by-department-copy
- 851802d657fe95a3d4318bd72bc2e4dd MultiReference "AATB - CRM by Business Size" slug acrm---crm-by-business-size → 6a3a6beafcbf2114d556f4f4
- f2affcfca32190651a007bad95ccd065 RichText "AATB - CRM by Business Size Copy" slug acrm---crm-by-business-size-copy
Rollback: recreate the same types and names (no data to restore).
Existing how-to field IDs: title 580544c71e663a5c30a43f28fb6838c9 · desc a3204871b4f124e19c027bfb65637cd6 · s1 893d6562e86409d721a7f3bc8d4a4de6/1f053b64d3c135de478636e65259bbb6 · s2 315e39e322936054194b9e4b47671c6a/f55a95da465e6d1d7acfee38ab4ccb12 · s3 86cf60a12dd1bc90885539ca4a1126c3/4f6c04cd43b23eafc2e0a5dac06dfdbb · s4 be91f7c10d3a4649967d40b8b1a61dc1/5e75052ea5f0de70e63bf07b40c87dad
New AAB how-to fields: s5 title 3ca34f47cd33444ef7cd6fa8608048c9 / des 113e018f984bf8bd6e0bc722caf36b99 · s6 d56fbcd7fac45d50b27b86126bc5ff33 / 4338b339cf27c14e3fa3388c06aa8282 · s7 fd9a45567c75fea2bbb0195b066546a0 / ddf874a6e18508351f116c91799944d1 (slugs aatb---how-to-step-5..7-title/des).
Item 6aba7ac4…: how-to title, desc and steps 1–7 written from howto/howto7.json. Old step 1–4 copy is in the item backup read at 18:3x (see transcript).
AAB template: inserted "Global / Sticky List" 9730644b instance 51b2669c-ced8-5bdb-bb3b-f27864048814 (before hidden §11, i.e. right after the banner).
All 16 props are CMS-bound. Removed the old "Global / Sticky List (Icons)" instance cadd555f-…-d976 (instances cannot be hidden).
Rollback: remove 51b2669c; insert 7a11ed6a-ab12-c739-dba4-4e0c0eca1e46 before §11 and bind Heading→580544c7, Description→a3204871, Item1-4 Title/Description→s1-4 fields, Button Text "".
Fade: new IX3 i-da197b65 "Build hubs / 7-step how-to comes into focus". It copies i-dcb777ac but targets .sticky_list-item (471c3d25-01b0-ba09-6099-51e9ae643e5b); scope is the 8 pages.
Only one scroll trigger is allowed per interaction, hence the twin. Rollback: delete i-da197b65.
