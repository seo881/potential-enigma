# Emergent build-hub image pipeline

Automated images for the Build hubs (LP, Form, Automation, Survey & Quiz).

- `pipeline/` scene library (`scenes.py`, `helpers.py`) and automated QA (`qa.py`)
- `masters/` editable SVG sources
- `images/<hub>/<slug>/uc-N.webp` published renders: 3000x2000 (3:2, matching the .build-usecase_image slot), lossless WebP, Inter font bundled at render time
- `manifest.json` maps every image to its Webflow CMS item, image field, and alt text

Webflow imports each image from its raw URL at a fixed commit, so files never need manual download or upload.

## Gates (pipeline/run.py): every image must pass before it ships
- Shape: canvas ratio must equal the slot's CSS aspect-ratio (3/2 for .build-usecase_image)
- Legibility: no text under 11px at the slot's desktop display width (830px)
- Layout (qa.py): no text overlaps, no text crossing a shape edge, nothing off-canvas

## v3: vector delivery (current)
Published images are SVGs with every letter converted to vector outlines (Inter, shaped by HarfBuzz with kerning).
Browsers draw them at the screen's native resolution, so they are sharp on every display and zoom level,
Webflow does not create resized copies of them, and there is no font dependency. `pipeline/outline.py` does the conversion.
Each file is verified in two independent renderers (cairo and librsvg). The WebP renders stay as a raster fallback.

## v5 design system (current standard, approved)
`pipeline/scenes_v5.py`: prompt-to-app motif, three depth levels with a spotlight on the hero card, one 60/1140 grid,
Lucide icons (ISC), and in-SVG motion (CSS keyframes, disabled under prefers-reduced-motion).
Gates (`pipeline/qa3.py`): WCAG AA contrast against each text's real background (gradients scored at their lightest stop),
occlusion-aware overlap and edge checks, off-canvas, 11px minimum on screen, and a build-time keycap-spacing guard.
