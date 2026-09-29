# Emergent build-hub image pipeline

Automated images for the Build hubs (LP, Form, Automation, Survey & Quiz).

- `pipeline/` scene library (`scenes.py`, `helpers.py`) and automated QA (`qa.py`)
- `masters/` editable SVG sources
- `images/<hub>/<slug>/uc-N.webp` published renders: 2400x2000, lossless WebP, Inter font bundled at render time
- `manifest.json` maps every image to its Webflow CMS item, image field, and alt text

Webflow imports each image from its raw URL at a fixed commit, so files never need manual download or upload.
