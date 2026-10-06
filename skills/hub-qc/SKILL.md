---
name: hub-qc
description: Quality-check Emergent build-hub child pages before they are created in Webflow or published. Runs the deterministic QC engine (qc/qc_hub.py), then a judgment pass on search intent, claims, cannibalisation and quality, then a P0/P1/P2 report. Use this whenever Divit asks to check, QC, audit, review or verify a child page, a batch, a hub, or anything "before it goes live", and always before asking Divit to approve a batch, even if he does not name the skill.
---

# hub-qc: the gate before Webflow and before publish

Prime directive: a page moves forward only at QC TOTAL = 0 (P0 + P1). P2 items are read and either fixed or explicitly accepted in the review notes. Rules only tighten; changing one needs Divit and a dated line in `DECISIONS.md`.

## Setup
If the repo is not set up in this chat: `git clone https://github.com/seo881/potential-enigma.git /home/claude/pe && cd /home/claude/pe && bash ops/setup.sh`. Read `rules/HUB_RULES.md` and `DECISIONS.md`.

## Layer 1: deterministic (code)
`python3 qc/qc_hub.py <spec>` (or `--hub <HUB>`, `--all`). It checks:
- **S** structure: fields in the collection map, required fields, `<h3>`+`<p>` shapes, how-to numbering, FAQ JSON (10-16 items, heading, `?`), 4 mockup keys, Emergent-first table, 6 images with alt.
- **L** limits calibrated on approved pages: meta title (60 chars, 580px, " | Emergent"), meta description (110-160), H1 (differs from title, 70 chars, "Build ..."), hero (about 30 words), why (25 words), H2s (48 chars), feature bodies (165-182, spread 12), FAQ answers (15-75 words), chips and tabs (26 chars).
- **H** hygiene: dashes, curly quotes, "built-in", "Type II", exclamations, emoji, we/our/us, British spellings, Title Case, a/an.
- **K** keywords: primary placement, slug, exactly one hub link in the FAQ, no external FAQ links, sibling primaries in headings (cannibalisation), secondary coverage, competitors outside the page's top 10.
- **V/C/D** vendor numbers without a dated check, claims against `rules/claims.json`, sentences duplicated from sibling pages.

## Layer 2: judgment (read the page against its brief)
Run `python3 ops/hubctl.py brief <url>` and check, writing each as P0/P1/P2:
1. **Intent:** would this page satisfy someone who searched the primary, given what the top 10 shows? Does an AMBER page carry its angle?
2. **Promise vs delivery:** everything the title and meta promise ("examples", "templates", "free", "for Shopify") is on the page.
3. **Truth:** every Emergent claim is in the register; every third-party fact is current; nothing contradicts another field (numbers, steps, tab content vs images).
4. **Depth:** the definition up top where an AI Overview appears; FAQ questions match how people ask; the how-to is specific to this primary, not generic.
5. **Distinctness:** reads as its own page, not a sibling with nouns swapped; tab H3s do not use sibling primaries; watch-list guidance from the brief is followed.
6. **Images:** each matches its tab copy; numbers add up; one hero; cursor on a button edge; true-size review done.

## Report format
For each page: `url | QC TOTAL | P0 list | P1 list | P2 list (fixed / accepted with reason)`. Then a batch line: pages passing, pages blocked, and the one decision (if any) that needs Divit. Fix methodology: root cause first, re-run the whole batch after any fix, never weaken a rule to pass.
