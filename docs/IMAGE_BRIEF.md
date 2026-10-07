# Image brief: how a page gets its six images

The writer, who already knows each tab's story, writes a structured brief in the spec (`image_brief`) in the same pass as the copy. The **image engine** (`pipeline/engine.py`) renders it into the six v5 images: 4 use-case SVGs (1200x800), the carousel cover (800x500) and the share image (1200x630 PNG). The design is identical to the 16 approved hand-built scenes: same layouts, palettes, type, shadows, motion and gates. Nobody designs pixels per page.

- **Lint:** `python3 ops/hubctl.py qc <url>` renders the brief in memory and reports problems as QC code I1, for example: `tab 2: hero.title: "..." is 592px wide, the space is 304px. Shorten it.` Shorten the brief; never ask for smaller type.
- **Render:** `python3 ops/hubctl.py images <url>` (or `images-batch reviewed`) writes `images/<dir>/<slug>/` and a contact sheet for review, and fills `spec.images` (paths + alt text).
- **Worked examples:** `pipeline/briefs/*.json` rebuild all 16 approved scenes. Copy their patterns.

## Structure
```json
"image_brief": {
  "tabs": [ {tab 1}, {tab 2}, {tab 3}, {tab 4} ],
  "cover": { "kind": "action|confirm|code|score", ..., "alt": "..." },
  "og":    { "headline": "Build a ...", "lines": null, "alt": "... with Emergent" }
}
```
Each tab:
```json
{ "recipe": "R1", "title": "Short title", "alt": "One or two specific sentences of alt text.",
  "prompt": "One sentence in the user's voice, 60-85 characters, no quotes",
  "main":  { "chrome": "window title or page URL", "blocks": [ ... ] },
  "panel": { "blocks": [ ... ] },          // R2, R3, R4, R11 only
  "kpi":   { "icon", "label", "value", "sub" },   // R10 only
  "rule":  "If X → Y",                     // R8 only
  "hero":  { ... },                        // every recipe: the one moment
  "mini":  { "icon", "title", "sub", "kind": "ok|acc|warn" },    // R1, R5, R6, R7, R8, R9
  "story": [ { "copy": "exact phrase from this tab's copy", "image": "exact text drawn" } ] }   // every tab
```

## Recipes (frames)
| Recipe | Main area | Also needs | Use when the tab is about | Example |
|---|---|---|---|---|
| R1 | App window (`chrome` = app name) | hero, mini | a request moving through steps, decided in Slack or email | `aab_approvals` tab 1 |
| R2 | Document (`scan: true` adds the scan line) | panel, hero | reading a document: invoice, receipt, upload | `aab_approvals` tab 2 |
| R3 | Wide document | panel, hero | review, redlines, several reviewers | `aab_approvals` tab 3 |
| R4 | Phone | panel, hero | something submitted or answered on a phone | `aab_approvals` tab 4, `sqb_csat` tab 2 |
| R5 | Browser (`chrome` = URL); `hero.h` 240-360 | hero, mini | a page the customer sees | `lp_thankyou` (all) |
| R6 | Form panel | hero, mini | a form and what happens on submit | `form_creators` tab 1 |
| R7 | Wide board | hero (150px tall), mini | a board or gallery of many entries | `form_creators` tab 2 |
| R8 | Table panel under a rule banner | rule, hero, mini | rules applied to rows (tiers, routing, scoring) | `form_creators` tab 3 |
| R9 | List panel | hero (message), mini | a scored list delivered to a channel | `form_creators` tab 4 |
| R10 | Wide panel (300px) | kpi, hero (840x260) | something tracked over time, or two views side by side (`columns`) | `sqb_csat` tabs 1, 4 |
| R11 | Wide table (360px) | panel, hero | per-account or per-person metrics with one outlier | `sqb_csat` tab 3 |

## Hero kinds (exactly one hero per image; it holds the click)
- `"kind": "message"`: a Slack-style app message. `channel`, `title`, `lines` (1-2), optional `button` (+ `button2`). Needs a hero at least 260px tall (R1, R9, R5 with `h`).
- `"kind": "card"` (default): optional header (`channel` for a #channel bar, or `app: true` with `app_sub` for the Emergent APP row, or `title` with `icon`, `tone` ok|acc|warn|bad and `chip`), then `blocks`, and an optional `action` button (`{"label", "icon", "primary"}`; on wide heroes it sits bottom right, `action_mid: true` centres it vertically). A bell icon rings.
- One click per image. A hero `action` clicks by default; a block button clicks only with `"click": true`. Two clicks fail the lint.

## Blocks (in `main.blocks`, `panel.blocks`, `hero.blocks`, `columns`)
| Block | Fields | Notes |
|---|---|---|
| `heading` | `title`, `sub`, `eyebrow`, `size`, `right` (big amount), `right_sub`, `chip: [label, kind]` | panel or page title |
| `title` | `title`, `sub`, `size` | tight title + subtitle pair for heroes |
| `text` | `text`, `size`, `weight`, `color` ink/sub/muted/acc/ok/bad, `align` center | one line |
| `rule` | `text`, `icon` | accent banner: "Rule matched: ..." |
| `steps` | `items: [{state done/skip/live/next, title, sub, right}]` | stepper; one `live` step (pulses) |
| `kv` | `rows: [[label, value, highlight?]]` | document key fields |
| `lineitems` | `items: [[name, "$1.00"]]`, `total: [label, amount]`, `compact` | items must add up to the total |
| `extract` | `items: [[field, value, confidence%]]` | extracted fields with confidence bars |
| `doc_header` | `initials` or `icon`, `title`, `sub`, `label` | top of a document |
| `filler`, `redline`, `comment`, `note` | see `aab_approvals` tab 3 | document body pieces |
| `receipt` | `merchant`, `sub`, `total` | receipt card (phones) |
| `budget` | `used`, `this`, `total`, `legend`, `fmt` | used + this may not exceed total |
| `checks` | `items: [..]` | green check list |
| `list` | `items: [{initials, name, sub, chip / right / score, muted}]`, `cards`, `row_h`, `threshold` | people or entries |
| `table` | `columns`, `widths`, `rows` (cell or `[label, kind]` chip), `highlight`, `bad`, `num_cols`, `signed_cols`, `avatars`, `row_h` | `signed_cols` colours +/- values |
| `timeline` | `items: [{label, chip, kind ok/bad/next, live}]` (2-4) | a bad point pulses red |
| `bars` | `items: [{label, value, flag}]`, `max` | flagged bar turns red |
| `metric` | `label`, `value`, `sub` | one big number |
| `confirm` / `status` | `title`, `sub` (+ `icon`, `kind` for status) | big centred check / inline check |
| `event`, `slots`, `product`, `callout`, `item` | see `lp_thankyou` | page pieces for R5 |
| `fields`, `textarea`, `button`, `buttons` | see `form_creators` tab 1 | `button`: `full`, `align` center/right, `icon`, `primary`, `click` |
| `code` | `code`, `label` (omit for the short centred box), `size` | referral or discount code |
| `linkbox`, `chips`, `pill`, `meta`, `quote`, `bullets` | small pieces | `quote` adds curly quotes itself |
| `stars`, `scale`, `media` | ratings, 1-5 scale, video tiles | `media` needs a wide panel |
| `columns` | `cols: [{w, gap, blocks}]` | two views side by side |
| `space` | `h` | rarely needed: the engine balances spacing |

Icons are Lucide names (lucide.dev/icons); an unknown name fails the lint.

## Numbers: declare every one (`checks`)
Every quantity an image draws (money, percentages, decimals, grouped numbers) must be accounted for in `image_brief.checks`, by value, for that image. The engine evaluates every expression, confirms every declared number is drawn exactly as written, and blocks the page otherwise.
```json
"checks": [
  {"expr": "3200 + 860 + 340 == 4400", "shows": ["$3,200.00", "$860.00", "$340.00", "$4,400.00"], "where": 1},
  {"expr": "round(330 / 1650 * 100) == 20", "shows": ["20%"], "where": 2},
  {"same": "$38,210", "where": [2, "cover"]},
  {"fact": ["99%", "97%"], "where": 2}
]
```
- `expr`: numbers, + - * / %, `round()` and one comparison. It must be true.
- `shows`: the strings exactly as drawn in that image.
- `same`: a value that must appear identically in several images (a tab and the cover).
- `fact`: standalone numbers that are not derived from anything (a price, a confidence score). Never use `fact` for a total, a difference or a percentage change; the reviewer checks this.
- `where`: the tab number (1-4) or "cover".

## Story links: copy and image tell the same story (`story`)
Every tab carries a `story` list that ties the tab copy to its image, one entry per key fact: the rule the tab is about, and every number the copy states.
```json
"story": [
  {"copy": "any license due to lapse within 60 days", "image": "If a license expires within 60 days"},
  {"copy": "more than a tenth", "image": "up more than 10%"}
]
```
- `copy`: a phrase that appears word for word in that tab's copy (`tab_content_N`, heading or body).
- `image`: text drawn in that tab's image, exactly as rendered (one text line, or a run of words across wrapped lines).
- The numbers in the two sides must agree. Words count as numbers: "five" is 5, "a tenth" is 10, "half" is 50.

The engine checks every link and QC blocks the tab (I4) when:
1. a `copy` phrase is not in the tab copy, or an `image` text is not drawn in that tab;
2. a linked pair states different numbers;
3. the tab copy states a number the image never shows (draw it, or take it out of the copy);
4. the image draws a rule (R8 `rule` banner or a `rule` block) that no story link ties to the copy;
5. a tab has no story links at all.

This is how "the image holds any variance" against "the copy sets a 2% tolerance" is caught before review: the rule drawn has to be linked to a phrase in the copy, and the numbers have to match.

## Covers (800x500, carousel card) and share image
- `action`: `channel`, `title`, `sub`, `primary`, `secondary` (approval-style).
- `confirm`: `title`, `button`, `icon` (browser with a big check).
- `code`: `title`, `label`, `code`, `foot` (approved + code).
- `score`: `title`, `stars` (optional), `label`, `value`, `delta`. With `stars`, a rating card; without, a shorter metric card (title, the metric and its delta), centred with no empty band.
- `og`: `headline` (wraps to a 480px column, max 3 lines, no one-word last line; set `lines` to break it by hand).

## Rules (the engine enforces the first four)
1. Everything must fit at the approved sizes; the lint names the field and the overflow. Shorten the words.
2. Numbers add up (line items and totals, budgets); one `live` step; one click; 4 tabs exactly.
3. Alt text: specific, one or two sentences, no "image of"; it becomes the CMS alt text.
4. A panel under 55% full is flagged as looking empty: add a block or choose a tighter recipe.
5. One moment per tab, frozen at its most informative point; the hero is that moment.
6. Fictional people and companies (Northwind, Globex, Initech, Acme); real brands only as tools (Slack, Xero, HubSpot).
7. The story matches the tab copy word for word on names, numbers and outcomes. The engine checks the `story` links (I4); the reviewer checks the rest on the contact sheet.
