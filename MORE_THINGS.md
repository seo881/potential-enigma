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

## #2 SQB collection 6ab24754757025d10940d04e (60/60). Deleted empty legacy fields (null on item 6aba7afb…):
80b73b278c2dd90c6cbda5d94752670d MultiRef "ASQB - CRM by Industry" acrm---crm-builder→6a3a6bea… · 9701937b3df9ed7ce6c814e13f9165fb RichText "ASQB - CRM by Industry Copy" ·
de89a69679cbc5a053990098024a252f MultiRef "ASQB - CRM by Department"→6a3a6bea… · 37a0b7229c25f373443686f164394e33 RichText "ASQB - CRM by Department Copy" ·
6aefbdb43618479bc2a10c583ca18c42 MultiRef "ASQB - CRM by Business Size"→6a3a6bea… · a05d6088602f517d133f6beafb0d6d76 RichText "ASQB - CRM by Business Size Copy"
How-to IDs: title 9fdc6a4a5b6adeff1ba323b2b693eb89 · desc 28af26808a77e039c6c4a731f42edacb · s1 6768b0a2c2df893c08006bc6bcc3c4e1/afbf9bb305ff756647dd7cfa42426167 · s2 d3d154a4ec7d54bcf0cb9521eaceeb02/3238143d6b4aaee777a7f2c9f6822792 · s3 edf1f2675fdd4c78c1eb21506c1bc9b6/cfc27aa639d5589387a0bd4439c38342 · s4 838f74ee9d6c64946e431dc2c7f5633e/f803990b27a4bd4244193e500cb35a81
SQB new fields: s5 3bb393c2a3e24ed2a218d1c713d8c271/42c13fbd6dcfc4d02c26c88b1c9ea9a5 · s6 ed47e57f9f2ec43842b247d1d105304a/3785563adcc43bfd8ce426be1dbd58f6 · s7 3e0584ddd03c0f0f7d75cb68f30cbd84/c04014d6d7981ae310cf7539482808a0.
Item written. Template: 7-step instance dea4db77-0ba0-cbea-43fd-598cf3ce42a6 bound (16 props). Old 4-step ba847d5e-…-f776 removed.
Carousels hidden (set_visibility false; re-show = true): templates AAB cadd555f-…-d9f6, LP d8a90b8f-…-8951, Form 24cd8ebc-…-667c, SQB ba847d5e-…-f7f6; hubs acd0c79f-f838-9a2e-53c7-b22c5244fdb6 on all 4.

## #2 LP collection 6aaaa937fe1a8d180b7c9f83 (60/60). Deleted empty legacy fields (null on item 6ab5158e…):
0dcf913c44f42e4a3669ddb9a22796d8 MultiRef "ALPB - CRM by Industry"→6a3a6bea… · d3ef4366695e67b644d4c5aad9d63278 RichText "ALPB - CRM by Industry Copy" ·
8ae4a8e4cc55d4614bf41df58d2de663 MultiRef "ALPB - CRM by Department"→6a3a6bea… · 826c840f592e53f3fbbfcf0301398cf8 RichText "ALPB - CRM by Department Copy" ·
96709b1f06a85f9ebd8aedb2d7e4fb90 MultiRef "ALPB - CRM by Business Size"→6a3a6bea… · d0bc576a2f94588569de5f803ac15f28 RichText "ALPB - CRM by Business Size Copy"
How-to IDs: title c28f71edc04afa0fa4fc37a6a3c716a4 · desc 4de413a8c3610b205c5ac7125c7e230b · s1 49f7275532a620b28e9efe2b02acbc15/a3b20b4fa5f80fc2c1724e2e358092d6 · s2 195967de079efc676d9b927a72d8b927/b90382acc0f8040d8ea600a7096c21ad · s3 c654a2b122fbd0403e1118b534c86f12/6d96a37632edfef9d432a5f916c98bfa · s4 2faccaf2e6779fb7452b60a46dcf1058/aebe9fae7686a9e780c6af3b9d993738
LP new fields: s5 e73ce29ddb08e691f339bf9a99005bbb/57ac21b0bfa570789ba53f45ef12251b · s6 0e9b13e5739c5daee9cb14ee707e9a1d/3d00912aaa5602816a0b1a6150c6daf6 · s7 a103770e20acff5702a2234230e95031/18cf25dbbc9c424a01c062ad11a9aa62.
Item written. Template: 7-step instance b7085709-325c-47dc-df0a-304a4712fd03 bound. Old 4-step d8a90b8f-…-889e removed.
Old component (7a11ed6a) prop map for rollback: Heading 4c013f09-d562-429e-f453-63642abe1dce · Description 814c6b86-8204-6aba-cd7b-21f46c8c67e7 · Button Text 347ff1a5-c4f3-70f8-415d-b3a05dad6fd2 = "" · Item1 T/D 92ad76ac-df81-893b-73d7-9d07bbc23a77/5c984d17-9685-bff1-35e0-f6b1f29d5b10 · Item2 1ad46bed-d2d8-5fae-b0e1-a1118873723e/48401fd1-a63f-6280-9f91-1514a5996721 · Item3 2bd8d76e-e8a5-d83e-f0c8-5eff6bcad1f3/8be0e9ca-0ae4-d475-039d-9d421e904ccb · Item4 777be265-0fcf-e885-eb10-29991a15e73d/dec646ad-9e0c-1948-e11c-3daff88dc0ed

## #2 Form collection 6aaaaa02995bb2f9f4d6a36c (60/60). Deleted empty legacy fields (null on item 6ab505a8…):
c503633e51ff866d297ae9192f719b51 MultiRef "AFB - CRM by Industry"→6a3a6bea… · 6a983a11eba22ed98c997a575f0cd497 RichText "AFB - CRM by Industry Copy" ·
3454c64517fc23af007d5e041056dc13 MultiRef "AFB - CRM by Department"→6a3a6bea… · e37915dc6c4a504b6d16ba9efbabd57d RichText "AFB - CRM by Department Copy" ·
5affefb84c122f2820e04e57493df6e2 MultiRef "AFB - CRM by Business Size"→6a3a6bea… · b7c41d607104672dee2c6cd0c3793511 RichText "AFB - CRM by Business Size Copy"
How-to IDs: title d2413f0b0ac05bf62d65f1b220134004 · desc 82ab5f20e6de29638473cb93059ad2ef · s1 4dc3402cb2a7a71da6a47893fd99aec5/d69654c05c0436788fe0e76f64155420 · s2 f1db675b17168dba619141a4302e4150/8c412bfcd13e68402c2517380f4b7d7c · s3 69a7c39b26009edaa6d6000968b671be/e69f9290fb5fb5bd5b60163d1561209e · s4 a3dccf9cdad7dc5dbdf79f99255a1a4c/63e20e804dc9695448f76c9d9471dc48
Form new fields: s5 5b21258793f4329034e5dd9a6758f989/fdc670f42483427bc293fd6e26335966 · s6 615efe57dbf7ba1fa0916986bf1fd84d/5644adcbdc973f399d0912c9df2dc02b · s7 8363dcf441d51bc3f1321ccb6b22628a/509a8094688868d773bcb94e00ef5e0f.
Item written. Template: 7-step instance b70d6134-eec6-21c1-3d15-d3927acaff22 bound. Old 4-step 24cd8ebc-…-65c9 removed.
Verified the SQB template has only dea4db77 (the new one).
#2 COMPLETE on all 4 templates: 7-step "Global / Sticky List" CMS-bound, fade i-da197b65 on the 8 pages. Hubs already use this component.

## 19:3x IST: comparison CTA + positive table phrasing
Template comparison CTA ("Global / Table Comparison" cba0e5d1, prop Button Text 9a6d9caf-c294-2a9c-f81e-dc8d19dc65c1) was empty; it is now CMS-bound to explore-cta:
AAB instance cadd555f-…-d9d8 → 9a1fda497a5b6155b47e5e40585b7546 · SQB ba847d5e-…-f7d8 → 380d92718921afecb6e98fbc13a5b9dd · LP d8a90b8f-…-8900 → 6ad11e8fe33f02f6fb6898e23d2ec8d5 · Form 24cd8ebc-…-662b → 51414cb4a8a55e8270ba9b781c897bff.
Rollback: set Button Text to "".
Hub table CTAs already had text: Build My Landing Page / Form / Automation / Survey.
Tables v2 (Emergent cells only): Form and SQB Response limits "None"→"Unlimited"; SQB Behavior at cap "No cap"→"Keeps collecting, no cap"; AAB "No task or execution cap"→"Keeps running, no task cap".
Applied to the 3 hub embeds (fd1c2c5f…) and 3 child items (6ab505a8…, 6aba7afb…, 6aba7ac4…).
v1 is kept in tables/*_hub_5row_v1.html. LP is unchanged ("No per-visitor pricing" was Divit-approved).
Related articles: LP and Form hubs sort newest first; AAB and SQB hubs sort oldest first (the sort prop is not settable by API, so this is a Designer fix). Templates show newest site-wide.

## 19:4x IST: audit applied (Designer). Old values are in audit/hubs.json ("cur") and in the transcript reads.
LP hub: H1, cards heading, features heading, F2 (rich text rebuilt: H3 50ed1fc8… + P, stray break removed, 'database you own'), integrations H2, table H2 and subheading, how-to s1/s3.
Form hub: H1, cards heading/subheading/card1/card2, features heading, F2 (H3 30445a1a… rebuilt), table subheading, how-to heading and s1, table v3 (Google Forms 'No limit').
AAB hub: H1, cards heading/subheading/card1/card2, features heading, F4/F6 (H3 0cfa8ba1… / 74a0490b… rebuilt), how-to heading and s3, CTA, integrations H2, table H2 and subheading, table v3.
Deleted the hidden duplicate carousel 86e5ccd1-891e-bb61-1762-8591adc90744.
Rich-text method: set the prop to plain text (the paragraph), then data_element_builder prepends an H3 into {page, instance, prop}. set_text on inner rich-text elements returns "Element not found".
SQB hub: H1, subhead, cards heading/card1/card3, features heading, F2/F3 (H3 42559f39… / 273c1c0b… rebuilt), how-to s1, integrations H2, table H2 and subheading, table v3 (Interact).
Deleted the hidden duplicate carousel 86e5ccd1….
FAQs (collection 6a1985ab…): 8 answers updated (Form 1, AAB 4, SQB 3). Originals in audit/faq_rollback.json. The items are published, so the edits stage until the next site publish.
Child tables v3 synced: AAB 6aba7ac4…, SQB 6aba7afb…, Form 6ab505a8… (all still isDraft true).
Meta titles set: "Free AI Landing Page Builder: Live in Minutes | Emergent" · "Free AI Form Builder With Unlimited Responses | Emergent" · "Workflow Automation Software With No Task Caps | Emergent" · "Free AI Survey Maker, Quiz Maker & Poll Maker | Emergent". The LP page name is now "AI Landing Page Builder".
Schema rebuilt on all 4 hubs: Organization + WebSite + WebPage (new name, isPartOf) + FAQPage (live answers, word for word) + BreadcrumbList.
NOT touched: sitewide components (section_stats, Global/Pricing). Standing rule: never.
PENDING (Designer only, API can't set Sort): the related-articles sort on the AAB and SQB hubs → Publishing date, Descending.

## 2026-10-01 pre-launch QA (4 hubs)
Interactions: all 9 build-hub IX3 present, scopes correct (use-case reveal/tilt on templates only; the rest on the 8 pages). Sitewide i-c9cb180a has showMarkers:true (NOT ours, not touched; Webflow renders markers in Designer/preview only).
Links: hub page-level links OK (Explore integrations → Integrations page; CTAs → modal; hidden legacy cards → page links). More things: 27 child anchors + 9 View all + 9 title links OK. Banner: /integrations + 12 tiles, all 12 integration items published. Chips (12 per hub): every /integrations/<slug> verified published (slack, stripe, hubspot, salesforce, google-sheets, gmail, notion, airtable, paypal, asana, calendly, twilio, excel, klaviyo, attio, square, supabase); chips without a page (Webhook, Postgres, GA4, Meta Pixel, PostHog, Hotjar, Zapier) go to /integrations.
Icons: banner "corrected" logos are byte-equivalent re-uploads of the chip logos; added alt text to 4 banner assets that had none.
Rebuilt rich-text feature cards verified (H3 + P) on LP F2 and AAB F4/F6.
Open for Divit: related-articles sort on AAB and SQB hubs (Designer), and the 'exclude from sitemap' toggle is not readable by API — confirm it is off in page settings.

## 2026-10-01 pre-launch fixes (hubs only; child items stay drafts, NOT published)
Em dashes removed (full rescan of hub copy, components, FAQs):
- SQB: how-to step 2 + how-to desc.
- AAB: how-to step 3; integrations card 1 paragraph (f55c5493-…-38fa).
- FAQs: AAB 6ab249c80dc672dfb044a16c/a166/a15c/a15a/a158 and SQB 6ab2480dede0a8922f281d3b/d35.
- Clean already: LP, Form, banner, More things, all 4 heroes, tables.
- Schema rebuilt for AAB + SQB to match the FAQs word for word.
Card copy levelled (titles 32-41 chars = 2 lines; bodies within 12 chars per hub): cards/cards.json. Originals are in the transcript reads of 2026-10-01.
Card image-above-text: page-level CSS in the 4 hub embeds (b8a2c5a1, 25e43d56, 3b7963ef, 9dd01394) flex-column + order. The shared component 763a7c4c is untouched. Rollback: remove the 3 card lines.
Hero prompt box: the same "Build page hero" component as the live builder hubs, with props only. Component internals are not API-readable, so Divit to confirm in Preview.

## 2026-10-01 features grid levelled on 4 hubs (section_features instance 7a732eca-…; component untouched)
Copy is in features/feats.json. Titles are 22-38 chars and wrap-checked at 24 chars/line (stricter than the live render), so all are 1-2 lines. Bodies are 165-184 chars, spread 10-13 per hub. No em dashes.
Method: set the rich-text prop to the paragraph, then prepend an H3 (no class, same as the original). Read back on all 4 hubs: 6 x (title + paragraph).
The SQB titles were missing for a short time (the builder call was not approved on the first attempt); restored.
2026-10-01: child explore-cta switched to first person to match the hubs (all still isDraft true).
"Build My Approval Workflow" / "Build My Customer Satisfaction Survey" / "Build My Thank You Page" / "Build My Creator Application Form".
Previous values: "Build Your …".

## 2026-10-01: schema parity with the live reference hubs (AI Website / App / Dashboard Builder)
The reference hubs carry WebPage (about → #softwareapplication) + FAQPage + BreadcrumbList + SoftwareApplication + Product.
Added SoftwareApplication + Product to all 4 hubs, same structure and the same 5 pricing offers (Free 0, Standard 20 / 17 annual, Pro 200 / 167 annual, Enterprise ×2).
Builder-specific: name, applicationCategory (LP DesignApplication; others BusinessApplication), applicationSubCategory, category, featureList (only page-claimed features), description = meta description.
Kept Organization + WebSite (extra, harmless). FAQ text unchanged (latest, em-dash-free).
Needs a site publish to go live. Re-run the Rich Results Test afterwards.

## 2026-10-05: value-card alignment fix (4 hubs, page-scoped)
Cause: after the image-above-text flip, the text block stayed bottom-pinned (the variant's layout), so titles started at different heights.
Fix: added justify-content:flex-start on the item, margin-top:0 + justify/align-content flex-start on the content, flex:0 0 auto on the image.
Embeds b8a2c5a1 / 25e43d56 / 3b7963ef / 9dd01394. Needs a site publish.

## 2026-10-05: INCIDENT. "More things you can build" (b4a27b0c) is the developer's component (group Hub Cards, 9 instances = our 8 + his Testing page).
On 2026-09-30 I edited its DEFINITION (labels, hrefs, descriptions, View-all text, 9 cover images + hub-card_cover class, icon-wrap combo is-on-cover, embed f11a368f).
That changed his Testing page too. It should have been a duplicate.
Every other build-hub change was instance props or page-level embeds. The banner 088920eb is ours (8 instances, all ours). No existing class was modified.
Restore plan (pending Divit's go):
1. Duplicate into "Build hubs / More things you can build" and move our 8 instances onto it.
2. Revert b4a27b0c to the logged originals.
Originals NOT captured: labels 273d, 2752/2756/275a, 276f/2773/2777 and the "View all N+ pages" counts (need the dev or a backup).

## 2026-10-05: child pages formatting pass (4 draft CMS items; our pages only, nothing shared)
Rewritten to the hub limits (H2 ≤48, subheads ≤135, hero subhead ≈ hub length):
- features H2 + subhead, use-case H2, "why" H2 + subhead, hero description.
- 24 feature boxes levelled (bodies 165-182, spread ≤12 per page).
- FAQ heading "Got Questions? We've Got Answers" → "[Topic] Questions, Answered"; FAQ answers unchanged.
- CSAT H1 left as approved.
Originals: childqa/originals_2026-10-05.json; full old feature HTML is in the transcript read of 2026-10-05.
Template schema: the API rejects CMS-linked (raw) schema, so the Designer paste code is in childqa/*-template.html.
It mirrors the reference child template (6a184b3f…): Organization, BreadcrumbList, CollectionPage, child SoftwareApplication, hub SoftwareApplication, Product.
Not yet applied (needs Divit's paste).

## 2026-10-05: final QA
Hubs: all 4 exported via the localization API (83 nodes each: text, component overrides, embeds) and scanned by script. Clean.
No dashes, Postgres, we/our, British spellings, placeholders, or curly quotes; links verified 2026-10-01. Hub FAQ answers (56) are clean.
Card-alignment root cause existed only in the 4 hub value cards (the component is absent from the child templates); fixed.
Child drafts fixed:
- features H2 → Title Case (matches the other child headings);
- LP: "enquiry" → "inquiry" (tab 4 + hero prompt), serial comma in tab 2, meta description reworded;
- AAB: "red-lines" → "redlines";
- Form: serial commas across tabs, FAQ, hero prompts and meta; affiliate prompt "10,000 followers" → "10,000 monthly reach" (matches the tab and image).
Left as-is (image-field alt text; editing via API would re-import the files): 3 alt texts use "enquiry" or drop a serial comma (LP uc-4, AAB uc-2/uc-3, SQB uc-1). Divit can edit them in the CMS item editor.
