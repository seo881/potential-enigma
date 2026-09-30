# Integrations banner (static, identical on all hubs and child pages)

Started 2026-09-30. This build is additive: new classes only, and no existing class or component definition was edited.

## Copy
- H2: "If it has an API, Emergent connects to it."
- Line: "Slack, Stripe, HubSpot, and every other tool with an API. No closed ecosystem, no approved-partner list, no waiting on a vendor roadmap."
- Button: "Explore integrations", linking to /integrations
- 8 tiles, each linking to /integrations/<slug> (all pages verified live). The logos are existing site assets from the hub chips.
  Slack 6aba3e2a2ae14558502ccc97 · Stripe 6aba3dcfe9697870784a657b · HubSpot 6aba3db0358d9d5435e52b73 · Salesforce 6aba69bce5e287c7c2125c88 ·
  Google Sheets 6aba69b4a230565c3d4c1cff · Gmail 6aba3dcbe9697870784a63e3 · Notion 6aba3de9ee7ca4b5088922ad · Airtable 6aba3de5cf9470efbfd43353

## New classes (style IDs)
| Class | ID |
|---|---|
| int-banner_section | ce45791f-ef24-e08d-1413-98e303f53e8b |
| int-banner | d1929918-5004-3381-ab43-77037500ccdc |
| int-banner_content | bd85b15f-41fc-c104-e058-1a745b0fd699 |
| int-banner_heading | d846e5f8-e609-a66e-6d55-d7cc5c719415 |
| int-banner_text | 9fbda9de-a769-1bf0-589f-ff48bf607cf5 |
| int-banner_button | 08280e40-4c8d-3686-6e77-07ce8fb9eb95 |
| int-banner_grid | d17a38fc-7a36-92a5-b7b0-d4a250de3660 |
| int-banner_tile | 68d1a07e-61da-3c9f-1e6c-88a7a9b4fd4d |
| int-banner_logo | 986d3878-8e78-f3e9-34fa-342843908660 |
| int-banner_name | cd3f1868-1272-630a-10d6-f8a3f9fbbf48 |

Responsive behaviour:
- Tablet (medium): the card stacks, and the grid stays at 4 across.
- Mobile (small): 2 columns, with row-style tiles (logo left, name right) and tighter padding.
- Hover lifts each tile 3px with a shadow. Keyboard users get a focus-visible ring on tiles and the button.

## Placements
| Page | Element | Position | Rollback |
|---|---|---|---|
| AAB template 6ab2470540448c8f7d1ccc1c | section f8af4c37-70af-830c-70f4-def66d1bb642 | directly after use-case (cadd555f-…-d95c), before how-to (…d976) | remove the section; how-to keeps its place before §11 (…d979) |

To place the section after the use-case component, the how-to instance (…d976) was moved to directly after the banner. Its relative order with everything else is unchanged.

## Hubs (pending)
Old orbit banners to be hidden, not deleted:
- LP, AAB and SQB: 13829ba5-695a-f487-3b54-ad7c924f8be2
- Form: e0f4d321-5094-59a7-790d-22132be392ab

## Schema cleanup the same session
The 4 runtime schema embeds were removed after the Designer-pasted Schema markup was verified (rawJsonLdSchema, reference token format). The code is kept in schema/page-schema.html.

## v2 motion layer (2026-09-30)
Inside the card (4055660b-a8da-dbaf-69db-e7952697d8c9) on the AI Automation Builder template:
- motion embed (class hide) 52c0f5c4-f170-c2de-7712-11d0d82958e5: keyframes int-glow-a / int-glow-b, tile-hover logo scale, prefers-reduced-motion off switch
- glow violet 06c7abc7-0ef5-95b9-61b6-a52fc338f31c (int-banner_glow + is-violet)
- glow blue 7abbc50e-044d-17d7-fdee-2a28b103b143 (int-banner_glow + is-blue)
New styles: int-banner_glow d693edfe-1dba-1df1-cee1-d6385700383d, combos is-violet b6f10776-2532-d934-86a0-2bac2d5fa0c7 and is-blue 7775e5e7-1600-a136-437a-543feb107363.
Updated (our own classes only): int-banner (position relative, overflow hidden, isolation), int-banner_content and int-banner_grid (z-index 2), int-banner_logo (transition).
Tile names fixed via the element text setting (the nested build had left placeholder text).

IX3: i-91daba51 "Build hubs / Integrations banner reveal", scope = 4 hubs + 4 templates. Scroll trigger on .int-banner at top 85%: card opacity 0→100, y 48→0, scale 0.98→1 (1.0s, expo.out); tiles opacity 0→100, y 18→0 (0.7s, position 0.3, stagger 0.06). Reduced motion: off; tiny/small: skip to end.
Rollback: delete i-91daba51; remove the 3 elements above; remove the 3 glow styles.
Logos: all 8 assets are SVG (resolution-independent).

## v3 "turned up" (2026-09-30, for review; v2 kept as fallback in banner/v2-fallback.*)
- Embed 52c0f5c4-… now holds banner/v3-turned-up.css.html: 3 aurora glows on 14s/17s/20s loops with wide drift, a 28s rotating sheen (::before), grain overlay (::after), lilac shimmer sweeping the H2 every 9s, gradient ring on tile hover/focus.
- New elements in the card: glow cyan c6b19274-a294-7d41-374f-1dd982c6dea1 (is-cyan 3809bb5a-…), spotlight 225f795a-3e21-2d99-e6f7-d79987e358f5 (is-spot f2a074cd-…).
- Style tweaks (our classes only): int-banner_glow mix-blend-mode screen; is-violet/is-blue stronger; int-banner_tile position relative + isolation.
- IX3 i-1e93bc94 "Build hubs / Integrations banner cursor spotlight": mouse-move on .int-banner moves the spotlight (xPercent −120→120, yPercent −90→90, smoothness .85). Desktop only; reduced motion off. Scope: 4 hubs + 4 templates.
Rollback to v2: see banner/v2-fallback.md (set embed code back, remove the 2 elements + 2 combos, delete i-1e93bc94, drop mix-blend-mode/isolation).

## Rollout (2026-09-30), approved v3
Banner converted to component "Build hubs / Integrations banner" 088920eb-03f5-b79b-e93c-585301aaa052 (group Build hubs). The source section on the AI Automation Builder template was replaced by its first instance.
New component placed from the dev's "More things you can build" b4a27b0c-2847-3338-522f-2cf9e51e2671 (group Hub Cards, 9 card visibility props, all default on).

Child templates, final order: … use-case → Integrations banner → how-to → old §11 (section_build-hub) → comparison → related → pricing → carousel → FAQ → More things you can build → CTA.
| Template | Banner instance | More things instance | Moves made (rollback = move back) |
|---|---|---|---|
| LP 6aaaa937… | d9fcd0f1-d027-8915-7d85-ab0505644e8f | b1c79508-8de4-dc8f-93ab-d5f750df25d8 | how-to …889e before §11 …88a1; FAQ 0bc02375-…-911c after carousel …8951 |
| Form 6aaaaa03… | 6e369d69-9cc7-35a9-8c66-f739e7cc1db7 | 762a301c-5955-e42a-b4f9-01abfb74e948 | how-to …65c9 before §11 …65cc; FAQ 734e06be-…-9bb0 after carousel …667c |
| AAB 6ab24705… | (converted source instance) | 67729791-12bd-aa85-0c54-5986aa1813ad | FAQ 57af2551-…-d9a8 after carousel …d9f6 |
| SQB 6ab24754… | 5c72ca2f-163a-601c-4a59-6b9105560546 | 3f0bd7d6-1a7d-182c-8bc8-fbf5525487f6 | how-to …f776 before §11 …f779; FAQ 8dd08c41-…-60d5 after carousel …f7f6 |
Rollback per template: remove the 2 instances. Moving how-to/FAQ back is optional, since their relative order to everything else is unchanged.
Hubs: pending.

## 12 tiles (2026-09-30): added PayPal (6aba3de2…), Asana (6aba3df7…), Calendly (6aba3dd3…), Twilio (6aba3e18…) inside the component grid 088920eb-…-a061.
New tiles: d58d13fe-783e-fc40-43ed-07c671c1b841, 4e97ea69-473d-1b9f-513e-bba3f3465529, 38d06748-70be-50cd-2df5-363769bbfd97, 7719d814-4813-20dc-1e9f-e3ebca669918.
Compact sizing: tile aspect-ratio auto, padding 1rem/0.875rem, radius 10px; logo 1.875rem; name 0.8125rem nowrap; grid gap 0.625rem. Grid is 4 across on desktop, 6 on tablet, 3 on mobile.
Rollback: remove the 4 tiles; restore tile aspect-ratio 1/1, radius 12px, logo 2.5rem, name 0.9375rem.

## Logo fix (2026-09-30)
HubSpot (clipped by a tight viewBox) → new asset 6abce59a3c5ebfc8b4d51cab: Simple Icons CC0 path in #FF7A59, viewBox -4 -4 32 32.
Gmail (simplified mark) → new asset 6abce5a1fa9c5fa556ba8a58: official 4-colour 2020 mark, square centred frame.
Source: logos/*.svg @ 20476b7. Set on component images 088920eb-…-a06b (HubSpot) and …-a077 (Gmail).
Rollback: set the assetIds back to 6aba3db0358d9d5435e52b73 / 6aba3dcbe9697870784a63e3. The old assets are untouched and still used by the hub chips.
The other 10 logos were checked in Divit's screenshot and render cleanly.

## Hub pass (2026-09-30)
On each hub: the banner is inserted after section_product-integrations; More things is inserted directly after the Global/FAQ; old blocks are HIDDEN (visibility false), not deleted.
| Hub | Banner inst | More things inst | Hidden: orbit banner / spacer / old §11 |
|---|---|---|---|
| LP 6aaa658e… | c30f5504-060e-bffb-2bbe-dd096ce70598 | 24e0e006-800e-dd1d-9972-089be48321d5 | 13829ba5-695a-f487-3b54-ad7c924f8be2 / 9c8e3d06-0bab-12b7-7ead-617497c6aed4 / f350b269-7ea7-1a0f-3cd9-5ce3e33898bd |
| Form 6aabb4c5… | 17bd5422-cf28-b9b8-724a-615faebc4dad | 0a700be6-0cad-24d9-4fe8-9d54c19b67fc | e0f4d321-5094-59a7-790d-22132be392ab / e0f4d321-…-392aa / 5175601b-006f-1460-b96d-c84aa9968d64 |
| AAB 6ab24643… | e5417864-6522-13d9-c894-9451cbf1af8d | a1d7763f-d07a-01b0-5055-ea231a4bfc8f | 13829ba5-… / 9c8e3d06-… / fdfbf8cf-c309-6002-0123-486847fc1192 |
| SQB 6ab246c3… | 2408c195-7499-75f2-0609-4722a353e9ca | f95b60b2-4aaf-a779-d572-9d90f9fc815b | 13829ba5-… / 9c8e3d06-… / 6f1cd26d-cadb-90d0-329b-a5994b1dc5fc |
Templates: old §11 hidden: LP d8a90b8f-…-88a1, Form 24cd8ebc-…-65cc, AAB cadd555f-…-d979, SQB ba847d5e-…-f779.
Verified order on the AAB hub: … integrations section → banner → carousel → table → how-to → blog → pricing → FAQ → More things → (old §11 hidden) → CTA.
Rollback: remove the 2 instances per page; set the hidden elements' visibility back to true.
