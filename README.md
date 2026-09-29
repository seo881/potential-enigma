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
