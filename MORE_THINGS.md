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
