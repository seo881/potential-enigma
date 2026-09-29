# Carousel card covers (internal-linking section)
Slot: new class `.build_cover` (id 40f4cb8f-74aa-83d6-a9b4-10fe25fba9f2): 16:10, inset 0.5rem inside the white card, 8px radius,
object-fit cover, #F4F3F8 placeholder fill. No existing class was modified.
Displayed size: about 360x225 CSS px (3-column grid), so covers are designed for small display: one bold product moment, minimal text.

Fields (Image, optional), one per child collection:
- AAB  aatb---cover-image   330a718a68d16a849a62a15bba7e9123
- SQB  asqb---cover-image   92be997ab328a707a4e20915a1da796a
- LP   alpb---cover-image   b42f5db743e2e051b5be1fca7d6c3a99
- Form afb---cover-image    aef8e5a8fbe2df6814bd702f11ab8890
"Thumbnail Image" stays the social-share (OG) image: must be PNG/JPG 1200x630 (platforms reject SVG).

Slots bound to the Cover field:
- Hubs: AAB, SQB, LP card image 9f4d88f4-... (class added, rebound from Thumbnail); Form hub new image 33868d6a-...
- Templates (new images, prepended in the card link): AAB 480f5f8b-..., SQB a6ca094c-..., LP ca16aadc-..., Form 1d9a132d-...
Rollback: remove the 5 new image elements, remove class from 9f4d88f4 on 3 hubs and rebind to Thumbnail, delete the 4 fields.

## Live (imported 2026-09-29)
Covers (SVG): AAB 6abbb81095974b2ce616fe7c, SQB 6abbb8123311c47795024674, LP 6abbb81e7da1d9fc3027518a, Form 6abbb81f9fee69e3212d1b7b
Share images (PNG 1200x630, Thumbnail Image): AAB 6abbb81095974b2ce616fe70, SQB 6abbb8113311c4779502466f, LP 6abbb81e7da1d9fc3027518e, Form 6abbb81f9fee69e3212d1b77
Previous Thumbnail on all 4 items was the placeholder file 6a901aa8cda440349cd42c6c (restore it to roll back).
Carousels unhidden on the 4 hubs: section acd0c79f-f838-9a2e-53c7-b22c5244fdb6 (rollback: visibility false). First-draft duplicate 86e5ccd1-... stays hidden.
