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
