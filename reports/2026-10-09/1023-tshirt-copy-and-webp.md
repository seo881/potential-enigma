# T-shirt house spelling, and share images moved from PNG to WebP

## Request
Divit (2026-10-09), first message:

> t-shirt-order-form: use "T-shirt" in all visible copy (answers, FAQ heading, any body text); keep keyword variants only in provenance. QC K-checks must treat "T-shirt" / "t shirt" / "tshirt" as the same keyword. QC 0, gate 10/10, update the draft (changed fields only), bulk-verify. Then tell me to publish staging.

Second message (sent while the first was running):

> git pull first (71c6d3c: DECISIONS 2026-10-09 image formats).
>
> Share image PNG -> WebP, all pages:
> 1. Pipeline: the renderer writes og.webp instead of og.png (1200x630, Pillow WebP, method 6; use lossless or quality 90, whichever is smaller while text stays crisp at 100%). Hard limits: <= 300 KB, exactly 1200x630. Image gates run on the WebP. Future pages get WebP only.
> 2. Convert every existing og.png in images/ (all written pages). Keep the PNGs in the repo until the 20 are verified live, then delete them in one commit.
> 3. CMS: for the 20 launch items (they are non-draft but unpublished), update ONLY the thumbnail-image field from the raw GitHub URL pinned to the commit SHA, with the same alt text. Read the before-values first into childedits/2026-10-09/ (rollback). Read back: the new file resolves, and the format is WebP. Also update the drafts that already have a share image (the 4 originals, contact-form, other written drafts): same field only, isDraft unchanged.
> 4. Add to verify_launch.mjs: og:image URL ends in .webp, responds 200 with content-type image/webp, is 1200x630, and is under 300 KB.
> 5. Pre-flight 20/20 again, then tell me: "Publish to staging only now."

## Actions and results

**T-shirt page**
- **Copy:** 31 visible spellings changed to "T-shirt" across meta title and description, H1/name, product name, hero description, breadcrumb, explore CTA, why title, how-to title, FAQ heading and answers, hero prompt and the 4 chip prompts, cover alt, share-image alt and share-image headline. Keywords, slug, file paths and FAQ provenance keep their variants.
- **QC:** new `rules/keyword_variants.json` maps the three spellings to one form. K1, K2, K5, K6 and K8 compare against that form (`qc/qc_hub.py` `kwn`/`kwmap`; `kw_bag` uses it too).
  - **H3 conflict:** the Title Case check (H3) flagged "shirt" in "T-shirt" headings, which conflicted with your "T-shirt everywhere". H3 now accepts the house form, as listed in the same rule file.
  - **All-spec sweep:** I ran QC on all 192 specs with the old and new QC. Only this page's P0/P1 result changes: 7 findings before (K1 x2, K2, K8, H3 x3), 0 after.
- **Gates:** QC 0 (strict and plain), PAA gate 10/10.
- **Images:** re-rendered, because the share-image headline changed. The cover SVG differs only in its description text (alt), and the use-case images are unchanged. Page state stays "reviewed", since this was a fix you ordered, not a new review cycle.

**Share image WebP**
- **Encoder:** `pipeline/raster.og_webp` encodes the share image twice (method 6, lossless and q90) and keeps the smaller. The lossy one is used only if PSNR against the render is at least 38 dB; I also compared it with the PNG by eye at 100%, and the text is equally crisp.
  - **Gates on the WebP as written:** the file must be WebP, exactly 1200x630 and at most 300 KB.
  - **Wiring:** `pipeline/engine.py` (render and contact sheet), `pipeline/build.py` (reference pages) and `ops/hubctl.py` (new-spec default) now write og.webp.
- **Conversion:** `ops/og_webp.py` converted 186 existing og.png files; the 187th, the T-shirt page, was re-rendered as WebP instead. All passed the gates: q90 every time, 20-33 KB, against 78-227 KB for the PNGs. 182 specs now point at og.webp, plus the T-shirt spec through its re-render. The PNGs stay until the 20 are verified live; the deletion is in the backlog.
- **Raw URL:** before the CMS update, I confirmed the raw GitHub URL at 0575c73 serves `image/webp`.

**CMS**
- **Before-values:** I read all 25 child items and committed `childedits/2026-10-09/webp-thumbnails.before.json` and `t-shirt-order-form.before-tshirt.json` (ca03f4e).
- **Same picture:** every PNG in the CMS was pixel-identical to the repo PNG, so each WebP is the same picture. The exception is the T-shirt page's new headline.
- **Update:** `thumbnail-image` only, with the same alt and isDraft left out so it stays unchanged. This covered the 20 launch items, contact-form and the 4 originals: 25 items in total, which is every item in the 4 child collections. The T-shirt item also took its 12 changed copy and image fields.
- **Read-back** (separate full read):
  - every thumbnail is a Webflow .webp served as image/webp, 1200x630 and byte-identical to the repo file;
  - alts are unchanged (the T-shirt alt is updated as instructed) and isDraft is unchanged;
  - a field-by-field before/after diff shows nothing else changed.
- File IDs and draft fingerprints are recorded in 21 specs.

**Verifier and pre-flight**
- **`ops/verify_launch.mjs`:** the og:image must be a .webp URL that responds 200 with content-type image/webp, measures exactly 1200x630 (read from the RIFF header) and is at most 300 KB.
- **Pre-flight:** 20/20 (`status/launch-checklist.md`).
  - It now accepts an item that is a draft or staged (isDraft false), because the 20 were staged in the previous step.
  - It adds a check that the share image is WebP.
- `ops/out/launch/*` and `.cache/review/batch-1.html` regenerated for the 20.

## Numbers
- T-shirt: 31 spellings in visible copy; QC P0/P1 7 -> 0 under the new K-checks; gate 10/10.
- Share images: 186 converted, 1 re-rendered; WebP 20-33 KB; 25 CMS items updated; 0 read-back failures.
- Pre-flight: 20/20.

## Decisions
- **"T-shirt" in all visible copy, with variants as one keyword in QC:** Divit, 2026-10-09 (this request), recorded in `rules/keyword_variants.json`. H3 accepting "T-shirt" in title-case headings follows from the same instruction.
- **Share image WebP:** DECISIONS 2026-10-09 (image formats); LESSONS.md section 4.
- **q90 over lossless:** q90 was smaller every time, crisp at 100% and at least 43 dB PSNR.

## Files changed and commits
- 1de5c92: T-shirt copy; `rules/keyword_variants.json`; `qc/qc_hub.py`.
- 0575c73: WebP pipeline, conversion, 186 og.webp, 183 spec paths, T-shirt re-render; `ops/og_webp.py`; `ops/verify_launch.mjs`.
- ca03f4e: CMS before-values.
- This commit: file IDs and fingerprints in 21 specs; `ops/launch.py` (pre-flight); `status/launch-checklist.md`; hub logs; backlog; this report; INDEX.

## Webflow calls
- **Session** ses_3KS7I2bs2N7e4yiavva4p4u12Dm; **agent** opus-5.5|claude-code|pub20.
- **Reads:** all items of the 4 child collections, twice (before and after).
- **Write:** `update_collection_items` on 25 items in 4 collections, with isDraft omitted.
  - On 24 items: `thumbnail-image` only, pointing at the raw GitHub og.webp at 0575c73.
  - On the T-shirt item 6ac8a04200f35689bf9ff3c2: 13 fields.
  - IDs are listed per collection in `logs/form.md`, `logs/sqb.md`, `logs/aab.md` and `logs/lp.md`.
  - Rollback: re-send the values in `childedits/2026-10-09/`.
- **No publish calls.**

## Not done
- Deleting the og.png files: after the 20 are verified live, in one commit (backlog).
- Steps 6 and 7 of the launch prompt wait for "staging published".

## Open questions for Divit
None.
