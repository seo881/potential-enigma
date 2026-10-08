# Image generation: complete knowledge transfer
### Emergent.sh build hubs: use-case visuals, card covers, share images, and every future image

**Written:** 2026-09-30.
**Repo state it describes:** `seo881/potential-enigma` at commit `47d060c` or later.
**Standalone:** a new chat with only this document can produce any image for any page at the approved standard. Read it end to end before touching the pipeline.
**Related docs:**
- `EMERGENT_BUILD_HUBS_HANDOFF.md`: the whole project, the rules and the GitHub token.
- In the repo: `COVERS.md`, `INTERACTIONS.md`, `BANNER.md`, `SCHEMA.md`.

---

## Part 0. The five rules that override everything

1. **Measure the slot before designing.** Read the Webflow class CSS for the slot: aspect ratio, object-fit and display width. The first batch was stretched because I assumed the shape. Divit called that "just plain dumb", and it must never happen again.
2. **Ship vector SVG with every letter outlined.** Share (OG) images are the one exception: they must be PNG, because social platforms reject SVG.
3. **The gates are necessary but not sufficient.** Always review the images yourself at **true display size** before they ship.
4. **Tell a true story.** Numbers add up, statuses agree with each other, and every claim is true at the moment shown. A cursor never sits on a label.
5. **Divit approves the standard; the pipeline enforces it.** Nothing touches Webflow without his go. Image imports touch **only** image fields. Everything is logged and reversible.

---

## Part 1. Every image type: slots, sizes, formats and fields

| Type | Where it shows | Webflow slot (class) | Slot CSS (measured) | Display size | Design canvas | Output file | Format | CMS field |
|---|---|---|---|---|---|---|---|---|
| **Use-case image** (4 per child page) | Child page, use-case tabs | `.build-usecase_image` (`455d8a8a-bf35-3333-ac1c-7e7489513e97`), inside component `section_usecase` (`4a1e2fed-…`, 11 instances site-wide) | `aspect-ratio: 3/2; object-fit: fill` (**stretches** anything not 3:2) | About 830 CSS px wide on desktop | **1200×800** | `images/<hub>/<slug>/uc-1..4.svg` | Outlined SVG with CSS motion | uc-1 `awb---key-feature-1-image`, uc-2 `acrm---key-feature-2-image`, uc-3 `acrm---key-feature-3-image`, uc-4 `acrm---key-feature-4-image` |
| **Card cover** (1 per child page) | Internal-linking carousel on the hub and on the other child pages | `.build_cover` (`40f4cb8f-74aa-83d6-a9b4-10fe25fba9f2`), **our class** | `aspect-ratio: 16/10; object-fit: cover; width: calc(100% - 1rem); margin: .5rem .5rem 0; radius 8px; bg #F4F3F8` | About 360×225 CSS px (3-column grid) | **800×500** | `images/<hub>/<slug>/cover.svg` | Outlined SVG, static | AAB `aatb---cover-image`; SQB `asqb---cover-image`; LP `alpb---cover-image`; Form `afb---cover-image` |
| **Share image (OG)** (1 per child page) | LinkedIn, Slack, X and iMessage previews | Page settings → Open Graph → Thumbnail Image (template binding) | Platforms render 1.91:1 | Up to 1200×630 | **1200×630** | `images/<hub>/<slug>/og.png` | **PNG** (platforms reject SVG) | `thumbnail-image` |
| **Hub value-card image** (3 per hub; legacy, done) | Hub value cards | `.product-integrations_image` (`f60aac1b-…`), component "Global / 3 Column (Cards)" | `aspect-ratio: 3/2.5 (6:5); object-fit: cover` | About 380 px wide | 1200×1000 | Site assets, uploaded by Divit | SVG | Component prop "Image 1..3" (asset IDs in the handoff §4) |
| **Integration banner logos** (8, static) | The integrations banner component (built 2026-09-30 by the Project chat) | `.int-banner_logo` | See `BANNER.md` | Small tiles | n/a | Existing site assets (hub chip logos) | SVG | Static, not CMS |

**The ID/field facts behind this table:**
- The four child collections share field slugs, **except the Cover field**, which has a per-collection prefix.
- **Collections:** AAB `6ab2470540448c8f7d1ccbf0`; SQB `6ab24754757025d10940d04e`; LP `6aaaa937fe1a8d180b7c9f83`; Form `6aaaaa02995bb2f9f4d6a36c`.
- **Items:**
  - AAB approval-workflow `6aba7ac40efe4e6ac8693159`
  - SQB customer-satisfaction `6aba7afb6271de33629b812c`
  - LP thank-you-page `6ab5158e23395050bc86ca79`
  - Form creator-application `6ab505a8d621dc692561a85a`
- **These are all in `pipeline/pages.json`.**

---

## Part 2. Why the pipeline looks like this (the history, so nobody repeats it)

| Version | What we shipped | What went wrong | The lesson, now enforced |
|---|---|---|---|
| **v1** | 6:5 lossless WebP, 2400×2000 | The slot is 3:2 with `object-fit: fill`, so every image was **squashed** about 20% vertically. Text was also too small: about 9 px on screen. | Read the slot CSS first. Add a **shape gate** and a **legibility gate** (11 px minimum on screen). |
| **v2** | 3:2 lossless WebP, 3000×2000, larger type | Looked **soft**: Webflow serves downsized responsive copies of CMS *raster* images (p-1080 and similar) and the browser upscales them. On top of that, a raster of text never matches live text. | Use vector. |
| **v3** | SVG with text converted to glyph outlines (Inter, HarfBuzz-shaped) | Nothing went wrong. Webflow kept `<defs>` and `<use>`; Divit zoomed to 5× and it stayed razor-sharp. | Vector is the delivery format. |
| **v4** | New design language (the reference set) | Divit said "much better" and asked whether it was my best. It wasn't. | Push honestly. |
| **v5** (current, approved) | v4 plus in-SVG motion, one grid, a hero spotlight, a live prompt chip, WCAG AA contrast | Approved by Divit: *"these outclass the placeholder images in every domain… approved"*. | This is the standard. |

**Measured sizes, same scene at 3000×2000:**
- **SVG:** about 102 KB, or about 23 KB if gzipped by the CDN (**UNVERIFIED**: ask Divit to check `content-encoding` in DevTools).
- **Lossy WebP q90:** 179 KB. **Lossless WebP:** 181 KB. **JPEG q90:** 461 KB. **PNG:** 826 KB.
- **The old `Default.png` fallback:** 1,565 KB.
- **At 3,200 use-case images:** about 330 MB as SVG, against about 2.6 GB as PNG.

---

## Part 3. The environment (a fresh chat starts from nothing)

```bash
git clone https://github.com/seo881/potential-enigma.git /home/claude/pe
cd /home/claude/pe && bash pipeline/bootstrap.sh          # expect: BOOTSTRAP OK: 20 scenes/covers built, all gates clean
python3 pipeline/build.py check                            # expect: 24/24 identical
```

**What `bootstrap.sh` does** (verified from a wiped state; rebuilt output is byte-identical to production):
1. `pip install cairosvg uharfbuzz fonttools pillow --break-system-packages`, then `apt-get install librsvg2-bin` (for `rsvg-convert`).
2. Installs **Inter 4.1** from `https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip`. It copies `Inter-{Regular,Medium,SemiBold,Bold,ExtraBold}.ttf` to `/root/.fonts/`. Weights map to font-weight **400/500/600/700/800**.
3. Installs the **Lucide icons** (`npm pack lucide-static@latest`, ISC licence) to `/home/claude/lucide/package/icons/*.svg` (2,118 icons).
4. Creates the working copy `/home/claude/pipe/`. The repo file names differ from the import names, so it creates aliases: `scenes_v5.py→ds5.py`, `hubs_v5.py→hubs5.py`, `covers_v5.py→covers5.py`, `scenes.py→scenes32.py`. It also creates `/home/claude/cards/helpers.py` (legacy).
5. **Smoke test:** every approved scene and cover, through every gate, then vector conversion.

**After adding or editing any pipeline module, re-copy it:** `cp pipeline/*.py /home/claude/pipe/`. Re-running the bootstrap also works. `build.py` imports from `/home/claude/pipe`.

**Network:** bash can reach github.com, raw.githubusercontent.com, release-assets.githubusercontent.com, npm and pypi. It **cannot** reach the Webflow CDN, so Divit opens CDN URLs in his browser when a real-browser check is needed.

**Pushing** uses a token held in the handoff doc and sent as a transient header, never stored:
```bash
T='<token>'; B=$(printf 'x-access-token:%s' "$T" | base64 -w0)
git -c user.name="seo881" -c user.email="seo881@users.noreply.github.com" commit -qm "<msg>"
git -c http.extraheader="AUTHORIZATION: basic $B" push -q origin main 2>&1 | sed "s/$T/[token]/g"; unset T B
```
**If a push is rejected** because another chat pushed first: `git fetch`, then **inspect** the remote commits (`git log HEAD..origin/main`, `git diff --stat`), then `git rebase origin/main`, then push. **Never force-push.** The Project chat also commits to this repo.

---

## Part 4. Architecture: the files and the flow

```
scene function (Python) ──► SVG source with real <text> ──► GATES ──► outline.py ──► vector SVG (no <text>, no font dependency)
      │                                                    (refuse on fail)                 │
      │                                                                                     ├─► rsvg-convert review renders at true display size
      ▼                                                                                     ▼
 pages.json registry                                                          images/<hub>/<slug>/{uc-N.svg, cover.svg, og.png}
                                                                                            │  git commit + push
                                                                                            ▼
                                                   raw.githubusercontent.com/<SHA>/<path>  ── build.py verify (byte-identical)
                                                                                            │  build.py payload → JSON
                                                                                            ▼
                                     Webflow MCP data_cms_tool.update_collection_items (fields = {url, alt}) → Webflow copies the file to its CDN
                                                                                            │  returns fileIds
                                                                                            ▼
                                                     build.py record → manifest.json / assets.json → commit + push (audit trail)
```

| File | Role |
|---|---|
| `pipeline/scenes_v5.py` (as `ds5`) | **Core design system**: tokens, primitives, defs (gradients, filters, grid, spotlight), motion `STYLE`, `canvas()`, `window()`, `prompt()`, `spot()`, `cursor()`. Also the **4 AAB scenes**: `po`, `invoice`, `contract`, `expense`, plus `SCENES`. |
| `pipeline/hubs_v5.py` (as `hubs5`) | **Palettes** (`PALS`) and `set_hub()`, which swaps tokens and defs for a hub. Higher-level primitives: `browser`, `panel`, `appmsg`, `mini`, `stars`, `field`, `click`, `hair`, auto-width `prompt(text)`. Also the **12 scenes** `lp1-4`, `form1-4` and `sqb1-4`. |
| `pipeline/covers_v5.py` (as `covers5`) | **Cover** canvas (800×500), `big_button`, and the 4 covers in `COVERS = {aab, lp, form, sqb}`. |
| `pipeline/outline.py` | **Text-to-vector.** HarfBuzz shaping (kerning and ligatures; `data-tnum` gives tabular figures). Each glyph is stored once in `<defs>` and reused with `<use>`. Handles `text-anchor`, `letter-spacing`, `opacity` and per-`tspan` fill. Removes `font-family`. |
| `pipeline/qa.py` | `width(text, size, weight, ls)`, the true Inter advance-width measurement (no kerning, so off by about 1%). Plus the legacy v1/v2 checks. |
| `pipeline/qa3.py` | **The current layout and contrast gate:** `run(svg) → [issues]`. |
| `pipeline/build.py` | **The CLI for everything** (Part 9). |
| `pipeline/pages.json` | **Registry**, one entry per child page (Part 9.2). |
| `pipeline/bootstrap.sh` | Environment setup and smoke test. |
| `pipeline/scenes.py`, `helpers.py`, `run.py` | **Legacy v2.** Kept for history; don't use. |
| `manifest.json` | One entry per **use-case** image (Part 10.3). |
| `assets.json` | Cover and OG file IDs per page. |
| `masters/` | Legacy v2 SVG masters. |
| `images/…/uc-N.webp` | v2 raster fallbacks, not used live. |

---

## Part 5. The v5 design system in full (exact values)

### 5.1 Canvas and grid
- **Use-case:** 1200×800. **Outer grid:** left edge **x=60**, right edge **x=1140**, top **y=40** (the prompt chip), content from **y≈164** to **y≈760**. Every scene aligns to it.
- **Cover:** 800×500. The hero card is centred, roughly x 130–670 and y 60–440.
- **OG:** 1200×630. Text column x=72, max line width **480**; the card image sits at x 590–1180, y 130–499.

### 5.2 Background (every image)
Four stacked full-canvas layers, emitted by `canvas()`:
1. `bg`: a linear gradient, top-left to bottom-right, from `bg1` to `bg2`.
2. `glowA`: a radial glow at (12%, 8%), r 0.55, `glow` colour at 0.95 opacity, fading to 0.
3. `glowB`: a radial glow at (92%, 96%), r 0.5, `glow` colour at 0.85 opacity (0.9 in ds5), fading to 0.
4. `grid`: a 40 px pattern of 1 px lines in the hub's `grid` colour at 7% opacity, **masked** by a radial fade (centre 0.5/0.45, r 0.65), so the grid dissolves toward the edges.

### 5.3 Depth and elevation (three levels)
| Level | What sits there | How it's drawn |
|---|---|---|
| 1, background app | App window, browser, document, phone, big panel | `rect(…, fill #fff, stroke LINE 1px, filter e1)`, radius 14–18 |
| 2, supporting cards | Secondary cards (`mini`, summaries) | Same as level 1 (`e1`) |
| 3, **hero** (the one focal element) | Floating Slack message, match card, reminder, decision | `spot(x,y,w,h)` **drawn first** (a radial glow ellipse, rx=w·0.78, ry=h·0.95, hub `spot` colour at 0.24–0.26 opacity), then the card with **filter e2**, radius 20 |

**Filters:**
- **`e1`:** a 1 px close shadow (dy 1, σ 1.2, #0F172A or #1E1B4B, 0.07) plus a soft shadow (dy 12, σ 18, hub `sh` colour, 0.08).
- **`e2`:** dy 2, σ 3, 0.10, plus dy 28, σ 34, hub `sh` colour, 0.20.

The shadows are tinted with the hub colour, which is a deliberate premium touch.

### 5.4 Typography (Inter, outlined)
| Role | Size / weight | Notes |
|---|---|---|
| Prompt text | 19 / 500 | In the chip; auto-width in hubs5 |
| Prompt label "Emergent prompt" | 16 / 600, `ACC_D` | |
| Big numbers | 30–44 / 700–800 | `ls` −0.3 to −0.8, `tnum=True` |
| Card titles | 22–28 / 700–800 | `ls` −0.2 to −0.4 for 24 px and above |
| Row titles, names | 18–21 / 600–700 | |
| Body, secondary | 16–19 / 500 | Colour `SUB` (#475569) or `MUTED` (#64748B) |
| Caps labels | 16 / 700, `MUTED`, `ls` 1–1.2 | e.g. "REQUESTER", "AMOUNT" |
| **Minimum** | **16 design px on 1200** (11 px or more at 830 px on screen); **26 on 800 covers** | Enforced by the gates |
| Tabular figures | `T(..., tnum=True)` | For amounts, times, scores and table columns |

Separators in UI text are `·` (ds5) or commas (hubs5). Both are fine, but stay consistent within one scene.

### 5.5 Colour
**Neutrals (all hubs):**
- **Ink** `#0F172A`. **Sub** `#475569`. **Muted** `#64748B`; never use a lighter grey for text.
- **Chrome grey** `#94A3B8` is for **icons only**, never text.

**Status:**
- OK `#15803D` on `#DCFCE7`.
- Warn `#B45309` on `#FEF3C7`. Also `#92400E` on `#FEF3C7` in v2.
- Bad `#B91C1C` on `#FEE2E2`.
- Neutral chip `#475569` on `#F1F5F9`.

**Hub palettes** (`hubs5.PALS`; accents chosen so **white 17 px text passes AA on the lightest gradient stop**):

| Key | acc → acc2 (`gAcc`) | accd | accs | accm | bg1 → bg2 | glow | grid | spot | sh | line | hair | stroke1 → stroke2 (prompt chip border) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **aab** violet | #7C3AED → #4F46E5 | #5B21B6 | #F1ECFF | #DDD3FF | #FCFBFF → #EFE9FF | #E2D6FF | #6D28D9 | #8B5CF6 | #2E1065 | #E6E3F0 | #EEEBF5 | #A78BFA → #818CF8 |
| **lp** blue | #2563EB → #1D4ED8 | #1E40AF | #EAF1FF | #BFD7FF | #FBFCFF → #E6EEFF | #D3E2FF | #1D4ED8 | #3B82F6 | #1E3A8A | #E2E7F2 | #ECF0F7 | #93C5FD → #818CF8 |
| **form** emerald | #047857 → #0F766E | #065F46 | #E6F7EF | #BCEBD5 | #FAFFFC → #E1F6EC | #CBF0DE | #047857 | #10B981 | #064E3B | #E0EDE7 | #EBF4EF | #6EE7B7 → #5EEAD4 |
| **sqb** burnt orange | #C2410C → #9A3412 | #9A3412 | #FFF1E6 | #FED7B0 | #FFFCF8 → #FFEDDC | #FFE0C4 | #C2410C | #F97316 | #7C2D12 | #F0E6DD | #F6EEE7 | #FDBA74 → #FB923C |

**Rejected accents, and why:**
- Violet #8B5CF6 as the start stop gives 4.23:1 with white 17 px text, which fails AA.
- Emerald #059669 gives 3.77:1, which fails.
- Orange #EA580C gives 3.56:1, which fails.

**Avatars** (white initials, bold at 16 px and above, so they need 4.5:1 on the lightest stop):
- Use deep pairs only: `#C2410C→#9F1239`, `#2563EB→#4338CA`, `#047857→#115E59`, or the hub's own `acc→acc2`.
- Pastels (#FDBA74, #86EFAC, #93C5FD) **failed**, so they're banned for initials.
- Decorative stack avatars with no initials can be lighter (the `window()` stack uses #F9A8D4→#A78BFA and similar).

### 5.6 Shapes and components (radius and stroke)
- **Radius:** cards 18–20 (hero 20); document or paper 14; inputs 12; buttons 12; chips fully rounded (h/2); icon tiles 12–16; phone bezel 46, screen 37.
- **Hairlines:** 1.5 px `HAIR`. Card borders: 1 px `LINE`.
- **Connectors:** dashed accent strokes, `stroke-dasharray="4 5"` or `"2 12"`, width 2–5, opacity 0.55. Curves use a cubic `C`. The end dot is r=4, in the accent colour.

### 5.7 Icons
- Lucide, drawn with `icon(name, x, y, size, color, sw)`. The default stroke width is 2, in icon units (it scales with size).
- **Used so far:** check, circle-check, sparkles, hash, git-branch, workflow, inbox, chart-column, settings, database, file-text, receipt, scan-line, signature, calendar, calendar-clock, bell, send, download, package, tag, copy, lock, user-plus, star, link, mail, gauge, command, corner-down-left, arrow-right.
- **Check that an icon exists** before using it: `test -f /home/claude/lucide/package/icons/<name>.svg`.

### 5.8 Signature motif: the Emergent prompt chip
- **Primitive:** `prompt(x,y,w,text)` in ds5, or `hubs5.prompt(text)` for auto-width at x=60, y=40.
- **What it draws:** a white chip with a gradient hairline border (`gStroke`) and filter e2; a gradient circle with a white sparkles icon; the label "Emergent prompt"; the text in curly quotes “…”; a **blinking caret** (class `caret`) after the text; and **⌘ ↵ keycaps** at the right.
- **Build-time guard:** `assert caret_x + 26 <= keycaps_x`, which fails loudly if the prompt text is too long. **Fix it by shortening the prompt**; never shrink the text below 19 px. The chip's maximum width is 1080.
- **Writing the prompt:** one sentence in the voice of a user asking Emergent, which describes exactly what the scene shows. For example: “Route purchase requests by amount and post each one to #approvals”.

### 5.9 Motion inside the SVG (Layer A)
CSS keyframes are embedded in every SVG (`STYLE`). They run inside `<img>` in all modern browsers. `@media (prefers-reduced-motion: reduce){*{animation:none!important}}` turns them all off. Apply a class to an element or `<g>`:

| Class | Effect | Timing | Use for |
|---|---|---|---|
| `pulse` | Scales to 2.1× while fading out (a "live" ring) | 2.4s loop | The live or active step, the next arrival, a low-score node. Draw the pulsing circle **behind** the solid node. |
| `caret` | Blinks | 1.1s steps | The prompt caret (automatic) |
| `press` | A cursor press dip | 3.2s loop | Wrap the cursor: `<g class="press">cursor</g>` (hubs5 `click()` does this) |
| `ripple` | An expanding circle at the click point | 3.2s, synced to the press | `click()` adds it, with base opacity 0 |
| `sweep` | Moves from −470px to 0 in y (a scan beam) | 4.8s | A `<g>` holding the beam rect and line, whose **resting position is the final place** |
| `ring` | A bell wiggle | 4s | Wrap the bell icon in `<g class="ring">` |
| `glow` | Opacity 1 → 0.45 → 1 | 2.6s | Highlight a bar segment ("this expense") |
| `float` | Drifts −6 px in y | 6s | Available, not used yet |

**Rule: the resting frame must be the complete, correct image.** Static renderers, reduced-motion users and share-image crops all see the resting frame. `ripple` rests invisible; `sweep` rests at its final position.

### 5.10 Accessibility built into every file
- `canvas(b, title=…, desc=…)` writes `<svg role="img"><title>…</title><desc>…</desc>`.
- **The `<desc>` is the source of the CMS alt text** for use-case images (`build.py payload` reads it). So write the desc as proper alt text: one or two sentences, specific, describing what the image shows.

---

## Part 6. Primitive reference (signatures and gotchas)

**ds5 (the core), with `x,y` at the top-left unless noted:**
- `T(x, y, s, size=18, w=500, fill=INK, anchor="start"|"middle"|"end", ls=0, tnum=False, op=None)`: text, where y is the **baseline**. Escapes `& < >`.
- `rect(x, y, w, h, r=16, fill="#fff", stroke=None, sw=1, f=None|"e1"|"e2", op=None)`.
- `chip(x, y, label, kind="acc"|"ok"|"warn"|"bad"|"n", w=None, h=36, size=16, dot=True)`.
  - **Gotcha:** the auto width is an estimate (`len*size*0.56+38`). For anything tight, **measure** with `qa.width(label, size, 600) + 56` and pass `w`. The covers do this.
- `button(x, y, w, h, label, primary=True, ic=None)`: primary is the `gAcc` gradient with white 17 px text; secondary is white with a LINE border and ink text. Label centring is approximate; keep generous widths (`qa.width(label,17,600) + 72`).
- `avatar(cx, cy, r, ini=None, c1, c2, gid=…)`: a centred circle with a white ring.
  - **Always pass a unique `gid`.** The default uses Python `hash()`, which is randomised per process, so output would stop being byte-reproducible and could collide.
  - With initials: r of 20 or more, so the text is at least 16 px.
- `icon(name, x, y, size=20, color=INK, sw=2)`.
- `cursor(x, y)`: the arrow's **tip** is at (x, y). Filter e1.
- `spot(x, y, w, h)`: the hero glow. Call it **before** the hero `rect`.
- `window(x, y, w, h, title, active=0, icons=(…4 lucide names…), avatars=True)`: the app chrome. A 48 px title bar with neutral traffic lights, a centred app icon and title, an avatar stack, and a 64 px sidebar with icons (the active one gets an accent tile). **Content starts at x+96 and y+96.**
- `prompt(x, y, w, text, h=84)`: the signature chip (see 5.8).
- `canvas(body, extra="", title="", desc="")`: wraps everything. Uses module globals `W, H` (defaults 1200 and 800).

**hubs5 (call `set_hub("<hub>")` first in every scene function):**
- `set_hub(h)`: sets `L.ACC`, `ACC2`, `ACC_D`, `ACC_S`, `ACC_M`, `LINE` and `HAIR`, and swaps `L.defs` to the hub palette. The helpers `A()`, `AD()` and `AS()` return the accent, dark and soft colours.
- `prompt(text)`: auto-width at (60, 40); width = min(1080, width(text)+230).
- `panel(x,y,w,h,f="e1")`: a white card, radius 18. `hair(x1, y, x2)` draws a hairline.
- `browser(x,y,w,h,url)`: a 52 px bar with traffic lights, a URL pill and a lock icon. **Content starts at y+100.**
- `click(x,y)`: a ripple plus a pressing cursor at the tip (x, y). **Put the tip on the button's lower-right edge**, about (button_x+button_w−16…−40, button_y+button_h−10…−14), never on the label.
- `appmsg(x,y,w,h, channel, title, lines=[…], btn=None, btn2=None, cur=True, when="now")`: a Slack-style hero card. It includes the spotlight and e2, a `#channel` header, the Emergent app avatar with an "APP" badge, the title and muted lines, and optionally a primary button (with a check icon unless there's a `btn2`), a secondary button and the cursor.
  - **Needs h ≥ 260 with a button.** On short cards the button collides with the text; that happened once (form2), so build a custom row layout instead.
- `mini(x,y,w,h, icon, title, sub, kind="ok"|"acc"|"warn")`: a secondary card with an icon tile and two lines.
- `stars(x, y_center, n, size=28, gap=8)`: 5 stars, the first n filled amber (#F59E0B), the rest #E5E7EB.
- `field(x,y,w,label,val,h=52)`: a form field (the label sits 10 px above the box).
- `canvas(b, title, desc)`.

**covers5:**
- `cv(b, title, desc)`: an 800×500 canvas. It temporarily sets `L.W, L.H`, then restores them.
- `big_button(x,y,w,h,label,ic=None,primary=True)`: 28 px/700 labels, with the width measured.

---

## Part 7. Composition recipes (the patterns of the 16 approved scenes)

Reuse these layouts, and copy the coordinates from the named scene. Each gives one **hero**, supporting context and a live moment.

| Recipe | Layout (1200×800) | Hero (level 3) | Used in |
|---|---|---|---|
| **R1: App window with a floating message** | `window(60,164,700,596)` on the left; hero `appmsg`-style card at (730,196,410,300) overlapping the window's right edge; `mini` or an audit card at (770,540,370,104) | Slack approval with Approve/Decline and a cursor | `ds5.po` |
| **R2: Document with extraction and match** | Paper `panel(60,164,440,596)` with highlight boxes (accent soft fill, 2 px accent stroke) and a scan `sweep`; extraction panel (560,164,580,330); curved dashed connectors from highlights to rows; hero at (560,524,580,236) | Match and route card ("Amounts agree", route, approver, synced) | `ds5.invoice` |
| **R3: Document with parallel review** | Document (60,164,510,596) with a redline (strike line plus green inserted chip, **measured widths**) and a comment box; review panel (610,164,530,372) with a progress ring and 3 reviewer rows; hero (610,568,530,176) | Reminder card (ringing bell) | `ds5.contract` |
| **R4: Phone with a check and decision** | Phone bezel (60,164,300,600); status bar with signal and battery; screen content from x=90; budget/check panel (430,164,710,304); hero (430,500,710,260); dashed connector from phone to panel | Decision card (avatar, "Within policy", approved state) | `ds5.expense`, `hubs5.sqb2` |
| **R5: Browser page with side cards** | `browser(60,164,700–720,596)` holding the page (the customer's output page); hero on the right (790–820, 196–214, 320–350 wide); `mini` below it | New lead / discount code / reminders / Slack enquiry | `lp1`–`lp4` |
| **R6: Form with the result** | Form `panel(60,164,520,596)` with fields and a primary button; dashed connector; hero (620,196,520,330) | "Approved" with a referral code | `form1` |
| **R7: Wide board with a bottom hero** | Wide panel (60,164,1080,420); hero row (420,612,720,150); `mini` (60,612,330,150) | Row-style message with a button on the right | `form2`, `sqb4` (wide hero 60,540,1080,220) |
| **R8: Rule bar, table and side hero** | Rule bar (60,164,1080,90) in accent soft; table panel (60,284,720,476), with row 1 highlighted; hero (820,300,320,300); `mini` (820,630,320,120) | Tracked link created | `form3` |
| **R9: List with a Slack hero** | List panel (60,164,660,596) with 4 scored rows (bars, and scores under 80 muted); hero `appmsg` (760,196,380,300); `mini` (760,540,380,120) | Shortlist ready with a View button | `form4` |
| **R10: Timeline with a wide alert** | Timeline panel (60,164,1080,300) with 3 nodes (the bad one pulses red) and chips; hero (300,500,840,260) with a quote and a button; KPI card (60,500,210,260) | Low-score alert | `sqb1` |
| **R11: Table with alert and summary** | Table panel (60,164,1080,360) with the bad row tinted BAD_S; hero (560,560,580,200); summary card (60,560,460,200) | NPS-drop AE alert | `sqb3` |

**Composition rules drawn from Divit's feedback and my reviews:**
- Keep **one** hero per scene, and give the spotlight only to the hero.
- A dashed connector links cause to effect (form → result, highlight → extracted row).
- Leave breathing room: nothing within 24 px of a card edge, and nothing within about 30 px of the canvas edge.
- Balance: if a panel has an empty lower third, **redistribute** the content. That happened with lp1 and form1 in v2.
- Show **one moment**, and freeze it at its most informative point. For example: the click on Approve while the stepper shows "In review"; the scan line just finished; 2 of 3 approvals with a reminder scheduled.

---

## Part 8. Catalogue of the 16 live scenes (the reference stories)

| Page / tab | Function | Recipe | The story (all facts consistent) | Motion |
|---|---|---|---|---|
| AAB · Purchase Order | `ds5.po` | R1 | PR-2041, Design licenses ×12, $4,800.00, Marketing. Rule $500–$5,000 goes to the department head. Stepper: Submitted 9:12 AM ✓ → Manager "Not required" → Dept head Priya Shah "In review" → Sync to Xero (next). The Slack card is clicked on Approve. "Every decision is logged". | pulse (live step), press and ripple, caret |
| AAB · Invoice | `ds5.invoice` | R2 | Northwind Supplies INV-7731, PO-2231, due Nov 12, 2026. Items $1,420 + $640 + $280 = **$2,340.00**. 4 of 4 fields extracted (99/100/99/97%). Hero: INV ✓ PO, amounts agree, over $1,000 goes to Finance, approved by J. Alvarez, synced to Xero. | sweep, caret |
| AAB · Contract | `ds5.contract` | R3 | MSA v3, 14 pages. Redline: Net ~~45 days~~ → 30 days of receipt. Lena Grant (Legal) comment. Parallel review 2/3: Lena ✓, Omar Aziz ✓, David Kim waiting. Sent Tuesday 9:04 AM, reminder Thursday 9:00 AM (2 days). | ring, caret |
| AAB · Expense | `ds5.expense` | R4 | Bistro Nord, client dinner $180.00, Project Atlas. Budget $3,200 + **$180** = $3,380 of $4,000, $620 left. Checks: receipt, under the $250 meal limit, within budget. Marcus Lee approved in 12 minutes. | glow, caret |
| LP · Lead Magnet | `hubs5.lp1` | R5 | "You're in. Your playbook is ready." Download (clicked). Next step: book a 15-minute walkthrough. New lead Maya Chen, utm_source linkedin, saved. Conversion tracked (GA4 and Meta pixel). | press and ripple, caret |
| LP · Ecommerce Order | `lp2` | R5 | Order #10482; Ordered Mon ✓, Shipped Tue ✓, Arrives Thu (pulse). Upsell: travel case $29, "Add to order" clicked. Trail runner 2 $129.00, shipping free, total $129.00. THANKS10 for 10% off within 30 days. Order saved, source Instagram ad. | pulse, press, caret |
| LP · Webinar | `lp3` | R5 | "You're registered". Oct 14, "Scaling onboarding with AI", Tue 10:00 AM PT, 45 minutes. Add to Google (clicked), Outlook, Apple. Invite a colleague. Reminders: 1 day (email), 1 hour (email and SMS), starting now (join link, pulse). Seat saved. | ring, pulse, press, caret |
| LP · Contact and Booking | `lp4` | R5 | "Thanks, we got it", reply within 24 hours. Thursday October 16 slots, 1:30 PM selected, confirm (clicked). #sales new enquiry Priya Nair, Acme Corp, demo, 50 seats. "Call booked Thu 1:30 PM". Deal created in HubSpot. | press, caret |
| Form · Brand Ambassadors | `form1` | R6 | Application for @maya.moves, Trail runner 2, marathon answer. Approved: fit score 92, 18k audience, US West. Code **MAYA15**, welcome kit Friday. Saved to the creators table. | caret |
| Form · UGC Creators | `form2` | R7 | 12 to review. Jordan (Skincare 5★, Unboxing 0:28), Aisha (Fitness 4★), Leo (Tech 3★). Jordan Diaz ready to book, "Send the brief" clicked. Top rated this week. | press, caret |
| Form · Affiliate | `form3` | R8 | Rule: reach ≥ 10,000 means approve, tracked link, tier. @runwithsam 48,200 Gold; @techwithtara 22,900 Silver; @homecafe.kim 12,400 Silver; @minimal.nate 6,100 Waitlist. Tracked link yourbrand.co/r/sam. Welcome email sent. | caret |
| Form · Creator Hiring | `form4` | R9 | Shortlist: Riya Patel 94, Sam Ortiz 88, Chen Wei 81, Ada Brooks 67 (muted). #creative-hiring "3 candidates scored above 80", View shortlist clicked. Interview Riya Thursday 2:00 PM. | press, caret |
| SQB · SaaS Onboarding | `sqb1` | R10 | Acme Corp: Day 7 CSAT 5 easy, Day 30 CSAT 4 easy, Day 90 **CSAT 2 hard** (pulse red). #cs-alerts quote about SSO. CSM Dana Ruiz, previous scores 5 and 4. "Schedule a call" clicked. Replies 64% this quarter. | pulse, press, caret |
| SQB · Post-Purchase | `sqb2` | R4 | Phone: "How did we do?", delivered Thursday, Trail runner 2 black size 9, product 5★ delivery 4★, "Arrived early, love them". 5 stars → review request (M. Chen). 2 stars → returns team flagged, order #10377 sizing, "Start exchange" clicked. | press, caret |
| SQB · B2B Quarterly | `sqb3` | R11 | Q3 by account: Northwind 4.6 +52 (+6), Globex 4.2 +31 (+2), **Initech 3.1 −8 (−24)**, Umbrella 4.4 +40 (+4). AE alert "NPS dropped 24 at Initech" to M. Rossi, Review account clicked. QBR summary in HubSpot. | press, caret |
| SQB · Support Ticket | `sqb4` | R7 | Ticket #8841 closed; score 4 selected. Agent Sofia, Billing, 38 minutes. CSAT by agent: Sofia 4.7, Marcus 4.5, Priya 4.1, **Tom 3.2** (red). #support-leads low score on #8790, CSAT 2, Tom, 2 days, refund quote. Open ticket clicked. | press, caret |

**The 4 covers** (`covers5`, recipe "one bold moment"):
- **aab:** `#approvals`, "$4,800 request, Design licenses", Approve (clicked) and Decline.
- **lp:** a browser with a big check, "You're in." and Download (clicked).
- **form:** "Approved", a referral-code box with MAYA15, "Fit score 92".
- **sqb:** "How did we do?", 5 big stars, CSAT **4.6** and a "+0.4 this month" chip (width measured).

**The 4 share images:**
- **Headlines:** AAB "Build an approval workflow your team actually uses"; LP "Build a custom / thank you page / in minutes" (manual lines, to avoid an orphan); Form "Build a creator application form with AI"; SQB "Build a customer satisfaction survey".
- **Fixed parts:** the wordmark text "emergent" in accd at 30/800 and the subline "From a prompt to a working app. Free to start." at 22/500.

---

## Part 8b. Where each scene's story comes from (the content-to-scene method)

For each tab of a new child page:
1. **Read the tab's CMS content.** The tab label is `acrm---key-feature-filter-N`; the body is in `awb---key-feature-1-content`, `awb---integration-feature-1`, `awb---integration-feature-2` and `acrm---integration-feature-4` (an h3 plus a p).
   - Example: Purchase Order's text says *"Tiered routing to the manager, department head, or CFO by amount … a Slack alert per approver, and every decision saved with the approver chain and timestamp"*. The scene shows exactly those elements.
2. **Pick the one moment** that proves the tab's promise, and pick the recipe (Part 7) that fits the output: an app, a page, a phone, a board or a table.
3. **Write the prompt chip text** in the user's voice, about 60–85 characters.
4. **Invent consistent mock data:**
   - Fictional people and companies (Northwind, Globex, Initech and Acme are fine; never real individuals).
   - Real integration brands only as tools (Slack, Xero, HubSpot).
   - USD amounts with cents where it's financial; dates in 2026.
5. **Cross-check the arithmetic, the statuses, the timelines and the counts.** "2/3" must match the rows; "4 of 4" must match the fields.
6. **Write `title` and `desc`.** The desc becomes the alt text: specific, 1–2 sentences, with no "image of".

**No AI API is involved.** Divit ruled that out: *"idt [I don't want] anthropic's api key to be involved in the process"*. Scenes and specs are written in chat, alongside the page content, and the pipeline is deterministic.

---

## Part 9. The CLI (`pipeline/build.py`) and the registry

### 9.1 Commands (run from the repo root, after the bootstrap)
| Command | Does |
|---|---|
| `python3 pipeline/build.py usecase <hub/slug>` | Builds the 4 scenes and runs the **shape**, **legibility** and **qa3** gates. **It refuses to write anything that fails.** Then outlines them, writes `uc-1..4.svg`, and renders a review sheet at true desktop size to `/home/claude/review/<hub>_<slug>_usecase.png`. |
| `python3 pipeline/build.py cover <hub/slug>` | Cover gates (shape 800×500, legibility at 360 px, qa3 excluding off-canvas), writes `cover.svg`, and renders a card-size mock to `/home/claude/review/…_cover_in_card.png` |
| `python3 pipeline/build.py og <hub/slug>` | Builds the share image: strips the cover's background, word-wraps the headline to 480 px (or uses `og_lines`), refuses lines that are too wide or more than 3 lines, warns on an orphan, and writes `og.png` (1200×630, PIL-optimised) |
| `python3 pipeline/build.py all <hub/slug>` | All three |
| `python3 pipeline/build.py check` | Rebuilds **everything** in memory and compares it byte for byte with the repo. **Currently 24/24 identical.** Run it after any pipeline change to prove nothing live changed unintentionally. |
| `python3 pipeline/build.py verify <sha> <hub/slug>` | Fetches each file from `raw.githubusercontent.com/<sha>/…` and compares it with the local file |
| `python3 pipeline/build.py payload <sha> <hub/slug> [usecase,cover,og]` | Prints the exact `data_cms_tool` action JSON (`update_collection_items`). Alt text for use-case images comes from each SVG's `<desc>`; for cover and OG it comes from `pages.json`. **`isDraft: true` is always emitted**, so a push never publishes an item. |
| `python3 pipeline/build.py record <hub/slug> usecase <id1> <id2> <id3> <id4>` | Writes Webflow `fileId`s into `manifest.json`, creating the entries for new pages |
| `python3 pipeline/build.py record <hub/slug> cover <id>` (or `og <id>`) | Writes into `assets.json` |

### 9.2 `pipeline/pages.json`, one entry per page
```json
"aab/approval-workflow": {
  "hub": "aab", "item_id": "6aba7ac40efe4e6ac8693159", "collection_id": "6ab2470540448c8f7d1ccbf0", "cover_field": "aatb---cover-image",
  "scenes": ["ds5:po", "ds5:invoice", "ds5:contract", "ds5:expense"], "cover": "covers5:aab",
  "og_headline": "Build an approval workflow your team actually uses",
  "og_lines": ["optional", "manual", "breaks"],
  "cover_alt": "…", "og_alt": "… with Emergent"
}
```
- `scenes` are `module:function` references in uc-1…uc-4 order.
- `cover` is `covers5:<key>`, looked up in `COVERS`.
- **Tab order must match the CMS tab order:** uc-1 is tab 1 (`acrm---key-feature-filter-1`), and so on.

---

## Part 10. The gates, in detail (what they catch and what they don't)

### 10.1 What runs
| Gate | Where | Threshold | Catches |
|---|---|---|---|
| **Shape** | `build.py gates_usecase/cover` | viewBox exactly 3:2 (use-case) or 800×500 (cover) | The v1 stretch disaster |
| **Legibility** | `build.py` | Every `font-size × display_width / canvas_width ≥ 11` (830 px for use-case, 360 px for covers) | Text too small to read |
| **Overlap** | `qa3.run` | Text boxes overlapping by more than 2 px | Colliding labels (e.g. the button over "Emergent APP") |
| **Crosses shape** | `qa3.run` | Text partially inside a rect it doesn't sit fully within, **occlusion-aware**: rects drawn *before* the text's topmost container are ignored, so floating cards over windows are fine | Text running off a chip, a card or a phone screen |
| **Contrast (WCAG AA)** | `qa3.run` | 4.5:1, or 3:1 for text of 24 px or more or bold text of 18.66 px or more, against the **topmost solid container**. Circles count as containers; gradients are scored at their **lightest stop**. | Grey on tinted boxes, white on light gradients, pastel avatars |
| **Off-canvas** | `qa3.run` | Text outside 0–1200 × 0–800 | Text beyond the edge (**ignored for covers**; see limitations) |
| **Keycap guard** | `ds5.prompt` assert | Caret plus 26 ≤ keycaps x | Prompt text crowding ⌘↵ |
| **OG headline** | `build.py og` | Each line ≤ 480 px at 50/800, ls −1.2; ≤ 3 lines; warns on a one-word last line | Headlines cut by the card; orphans |
| **Vector integrity** | `build.py` asserts | No `<text>` and no `font-family` after outlining | A font dependency slipping through |
| **Determinism** | `build.py check` | Byte-identical rebuilds | Accidental changes to live images |

### 10.2 Known limitations (a human review must cover these)
- `qa3` hard-codes **1200×800** for off-canvas, so it's filtered out for covers. Check cover edges by eye.
- `qa3` **ignores transforms** (rotation, translate and scale groups), `<path>` shapes and ellipses as containers, and text inside `<image>`.
- `qa.width` has **no kerning**, so measured widths run about 1% wide; keep 10–20 px of slack.
- **Contrast defaults:** when no container is found, the page background is assumed to be `#F6F3FF`. Put text on explicit cards.
- The gates can't judge **truth** (arithmetic, consistent statuses), **balance** (empty areas), **cursor placement**, **awkward line breaks** or **taste**. That's why review is mandatory.

### 10.3 Defect catalogue: every real defect so far, now on the review checklist
1. A stretched image (wrong aspect ratio).
2. Text too small at display size.
3. Soft rendering (raster served downsized).
4. A cursor covering a button label (the Approve cursor in v4; 11 cursors in the v5 rollout).
5. The same time shown twice in one row.
6. A glossy "shine band" on buttons that looked dated (removed).
7. A claim that's false at that moment ("Saved to the audit trail" while approval was pending, changed to "Every decision is logged").
8. A scan pill covering an amount.
9. A connector attached to the wrong row.
10. Percentages colliding with their bar.
11. Redline words floating apart (fixed with measured widths).
12. Grey 16 px text on a tinted box at 4.12:1.
13. Pastel avatars with white initials.
14. White text on #8B5CF6 at 4.23:1.
15. Prompt text crowding the keycaps.
16. Text running off a phone screen onto the bezel.
17. A button colliding with text in a short card.
18. A cramped Slack card title ("New enquiry from Priya Nair" within 18 px of the edge).
19. Share-image headlines cut off by the card.
20. The cover background showing as a box on the share image.
21. An orphaned last headline line.
22. A cover chip at 20 px (9 px on screen) overflowing.
23. Empty lower thirds in panels (lp1, form1).

### 10.4 The manual review checklist (do it for every image, at true size)
- Is there exactly **one** hero, and does the eye land on it first?
- Does everything align to the 60/1140 grid? Is nothing crowded against an edge?
- Do the numbers add up? Do statuses, counts and dates agree? Is every claim true at this moment?
- Is the cursor on the button's lower-right edge, with the label fully readable?
- Is there any empty zone that makes the layout feel unbalanced?
- Does anything look pasted on (a visible box or background)?
- Are there awkward line breaks, orphans or cramped titles?
- Is the resting frame complete, so it would look right with motion off?
- Is the colour right for the hub? Do the avatars and initials pass?
- Does the image match the tab's CMS copy and the prompt chip?

---

## Part 11. Runbooks

### 11.1 Images for a NEW child page in an existing hub (the most common job)
1. **Get the page data:**
   - The item must exist in the CMS. Get its `item_id` (via `list_collection_items`) and its tab labels and copy.
   - Confirm the collection's Cover field slug (the table in Part 1).
2. **Write the 4 scenes:**
   - Create a module per page, e.g. `pipeline/scenes_aab_expense_report.py`, with `import ds5 as L, hubs5 as H` (and so on). Call `H.set_hub("aab")` at the start of **each** function. Reuse the recipes in Part 7 and write the stories using Part 8b.
   - Give each function `canvas(b, title, desc)` with a proper desc.
3. **Write the cover:** add a function to `covers_v5.py` (e.g. `COVERS["aab_expense_report"]`) or a per-page module. One bold moment, text at 26 px or more.
4. **Register it:** add a `pages.json` entry (scenes, cover, `og_headline`, `cover_alt`, `og_alt`). Then `cp pipeline/*.py /home/claude/pipe/`.
5. **Build:** `python3 pipeline/build.py all <hub/slug>`. Fix every gate failure (a failure blocks writing).
6. **Review:** `view` each sheet in `/home/claude/review/` and walk the 10.4 checklist. Iterate until it's clean. Show Divit the review sheets at true display size, with before/after where relevant, and **wait for his approval** on new visual work.
7. **Regression check:** `python3 pipeline/build.py check` should still be identical for every existing page.
8. **Commit and push** (Part 3). Then `python3 pipeline/build.py verify <sha> <hub/slug>` should report 6/6.
9. **Payload:** `python3 pipeline/build.py payload <sha> <hub/slug>`, then pass the JSON as the `actions` of **`data_cms_tool`**, with `agent_id`, `session_id` and a `context` string. Up to 100 items per call; group items from the same collection.
10. **Record:** take the returned `fileId`s (in field order), then run `build.py record <hub/slug> usecase <4 ids>`, `record … cover <id>` and `record … og <id>`. Commit and push the audit trail.
11. **Tell Divit** to hard-refresh the Designer (Cmd+Shift+R) and check the template with that item selected. Motion runs only in Preview.

### 11.2 Many pages at once (the scale plan: about 800 pages)
- Do batches of about 5 pages per hub (Divit will name them).
- Write every page's scenes in chat, alongside the page content (the copy and the image specs together).
- Build them all, review all the sheets, commit once, then one `payload` per page. Combine them into one `update_collection_items` call per collection, up to 100 items.
- **Pace Webflow calls:** a 429 on `/v2/pages` means wait about 65 seconds.
- **Planned refactor, to make 800 pages practical without losing quality:**
  1. Turn the recipes R1–R11 into **parameterised functions** that take a data dict (people, amounts, labels, statuses).
  2. Each page's scenes become small JSON specs in `specs/<hub>/<slug>.json`, rendered by the recipes.
  3. The same gates and review still apply.
  4. **It isn't built yet.** Build it only after Divit approves the plan.

### 11.3 Starting a NEW hub (the next 2 hubs)
1. **Read the new template's use-case slot CSS** (`query_styles` on its image class). If it isn't `build-usecase_image` at 3/2, **set the canvas to match** and update the shape gate in `build.py`.
2. **Confirm the field slugs** with `get_collection_details`; cloned collections share the slugs but get new prefixes. Add a Cover field with `data_cms_tool.create_collection_static_field` (type Image; the display name follows the collection's prefix). Add `build_cover` slots the same way as before (`COVERS.md`: `data_element_builder` prepends an Image into the card link with `set_style ["build_cover"]`, then `set_settings` binds `assetId` to the cover field). **Never modify existing classes.**
3. **Choose a palette:**
   - Pick `acc→acc2` so that white 17 px text passes 4.5:1 at the **lighter** stop. Test it with `qa3.contrast`.
   - Derive `accd` (text on soft, 7:1 or better), `accs` (a very light tint), `accm`, `bg1`/`bg2`, `glow`, `grid`, `spot`, `sh` (a very dark shade), `line`/`hair` (tinted neutrals) and `stroke1`/`stroke2`.
   - Add the palette to `PALS`, and run a sample scene through `qa3`.
4. Continue with 11.1.

### 11.4 Revising a live image
Edit the scene. `build.py` the page, review, then run `check`: only the intended files should differ. Commit, push, verify, then payload (only the changed kinds, e.g. `payload <sha> <page> og`). Record, commit and push. The old CDN file stays on the CDN, which does no harm.

### 11.5 Rolling back an image
The previous version is in git history. Find the earlier commit SHA for that path (`git log -- images/<hub>/<slug>/uc-2.svg`), then run `payload <old_sha> <page> usecase`, or hand-edit the JSON to include only the fields you need. Import, record, commit and push. For covers and share images, the previous values are in `COVERS.md`: the placeholder `6a901aa8cda440349cd42c6c` was the old Thumbnail.

### 11.6 Verifying in a real browser (only Divit can)
- Ask Divit to open the CDN URL and zoom to 300–500%. It should stay razor-sharp, and all text must be present.
- For motion, use Designer **Preview**, or open the CDN SVG directly; the animations run in the browser.
- **Compression:** DevTools → Network → the `.svg` → Response headers → `content-encoding` (gzip or br).

---

## Part 12. Webflow behaviour for images (hard facts)

- **Import by URL:** an image field value of `{"url": "<public URL>", "alt": "..."}` makes Webflow copy the file to `cdn.prod.website-files.com/6a0f028de6df6a6fd88c3f89/<fileId>_<name>` and return `fileId` plus url in the item's `fieldData`. **Always pin the URL to a commit SHA, never `main`.**
- **SVGs are stored and served unchanged** (`<defs>` and `<use>` survive; verified at 5× zoom). **Rasters get responsive downsized variants**, which is why v2 looked soft.
- **Touch only the image fields.** `update_collection_items` with `fieldData` containing just those keys leaves every other field untouched. Keep `isDraft: true` unless Divit approves publishing.
- **The Designer caches images:** hard-refresh after a swap.
- **The OG image binding on templates is Designer-only:** Page settings → Open Graph → image = Thumbnail Image. It's done for AAB and SQB (**UNVERIFIED for LP and Form**).
- **The use-case slot class can't be changed.** Divit refused `object-fit: cover` site-wide, so images must always be exactly 3:2.
- **The Tabs element cross-fades natively** (300 ms in, 100 ms out). IX3 reveals would hide images until triggered, so don't use them on tabs.
- **Page-level motion (IX3) complements Layer A:**
  - `i-54e50d55`: reveal. y 64→0, scale 0.96→1, opacity 0→1 over 1.0 s when `.section_usecase` passes top 85%.
  - `i-af43ffd6`: a 3D tilt of ±3° at 1400 px perspective. Desktop only.
  - Both are scoped to the 4 templates. The full list is in `INTERACTIONS.md`.

---

## Part 13. Current inventory (all live, all child items still drafts)

| Page | uc-1…uc-4 fileIds | Cover | OG |
|---|---|---|---|
| aab/approval-workflow | `6abba58e85926d9cd515b37f`, `…b374`, `…b37a`, `…b382` | `6abbb81095974b2ce616fe7c` | `6abbb81095974b2ce616fe70` |
| lp/thank-you-page | `6abbb0caac422a048331d970`, `…d97b`, `…d96a`, `…d978` | `6abbb81e7da1d9fc3027518a` | `6abbb81e7da1d9fc3027518e` |
| form/creator-application | `6abbb0cb9a445d8d6d247d56`, `6abbb0cc9a445d8d6d247d5f`, `…d62`, `…d5c` | `6abbb81f9fee69e3212d1b7b` | `6abbb81f9fee69e3212d1b77` |
| sqb/customer-satisfaction | `6abbb0da1c58063f412db282`, `…288`, `…27c`, `…285` | `6abbb8123311c47795024674` | `6abbb8113311c4779502466f` |

- **Source commits:** use-case AAB `0a392ab`, others `f599273`; covers and OG `9449685`.
- **Full detail:** `manifest.json` and `assets.json`.

---

## Part 14. The plan forward (image side)

1. **Next child pages:** Divit names about 5 pages per hub. Build each with runbook 11.1, showing him the review sheets before import.
2. **Build the recipe library** (11.2), after Divit approves it, before the volume ramps toward 800 pages.
3. **Phase 2 automation** (optional, needs Divit's approval): a GitHub Action that runs `bootstrap` plus `build.py check` and the builds on every push, and posts the review sheets as build artifacts.
   - It uses the built-in `GITHUB_TOKEN` only, with **no Anthropic key**.
   - A Webflow site token as a repo secret (added by Divit, never in chat) would allow hands-off imports. Otherwise imports stay in chat through the MCP connector.
4. **Next 2 hubs:** runbook 11.3 (palette, fields, slots).
5. **Open checks:**
   - SVG `content-encoding` on the CDN.
   - The OG binding on the LP and Form templates.
   - The card-hover "within" behaviour (`i-4fd60c05`; hover one card in Preview).
6. **Optional upgrades:**
   - The hub value-card visuals (6:5) redone in v5.
   - Custom hub share images.
   - Page-specific integration tiles, if Divit wants them later. The banner built on 2026-09-30 is static and identical on all pages; for page-specific tiles, see `BANNER.md` and handoff §9 P1.

---

## Appendix A. The quick-start card

```bash
git clone https://github.com/seo881/potential-enigma.git /home/claude/pe && cd /home/claude/pe
bash pipeline/bootstrap.sh && python3 pipeline/build.py check
# new page: write scenes module + cover → add pages.json entry → cp pipeline/*.py /home/claude/pipe/
python3 pipeline/build.py all <hub/slug>            # gates + files + review sheets in /home/claude/review
python3 pipeline/build.py check                     # existing pages untouched
# commit + push (token header) → then:
python3 pipeline/build.py verify <sha> <hub/slug>
python3 pipeline/build.py payload <sha> <hub/slug>  # → data_cms_tool actions
python3 pipeline/build.py record <hub/slug> usecase <id1> <id2> <id3> <id4>; ... cover <id>; ... og <id>
# commit + push the audit trail
```

## Appendix B. A minimal new scene (a template to copy)

```python
import ds5 as L, hubs5 as H
from qa import width as tw
T, rect, chip, button, avatar, icon = L.T, L.rect, L.chip, L.button, L.avatar, L.icon

def my_scene():
    H.set_hub("aab")                                              # palette first, always
    b = H.prompt("“Describe exactly what this scene shows, in the user's words”")
    b += H.panel(60, 164, 700, 596)                               # level 1: the app / page / document
    b += T(96, 224, "Primary object title", 26, 700, L.INK, ls=-0.3)
    b += T(96, 254, "Supporting context line", 16, 500, L.MUTED)
    # ... rows, fields, table; numbers with tnum=True ...
    X, Y, Wd, Ht = 800, 214, 340, 300                             # level 3: the ONE hero
    b += H.spot(X, Y, Wd, Ht) + rect(X, Y, Wd, Ht, 20, "#fff", L.LINE, 1, "e2")
    b += T(X + 24, Y + 48, "The moment", 20, 700, L.INK)
    bw = int(tw("Approve", 17, 600) + 72)
    b += button(X + 24, Y + Ht - 74, bw, 50, "Approve", True, "check")
    b += H.click(X + 24 + bw - 16, Y + Ht - 34)                   # cursor tip on the button's lower-right edge
    b += H.mini(800, 560, 340, 120, "database", "Secondary fact", "short supporting line")   # level 2
    return H.canvas(b, "Short title", "Specific alt-text description of what the image shows.")
```

## Appendix C. `manifest.json` entry schema (use-case images)
`image`, `hub`, `path` (`images/<hub>/<slug>/uc-N.svg`), `item_id`, `collection_id`, `field`, `alt` (as sent to Webflow), `source_url` (raw URL at a SHA), `webflow_file_id`, `status`, `design_system` (`v5`), plus legacy keys `path_raster_fallback`, `format` and `size`.
