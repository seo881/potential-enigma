---
name: hub-qc
description: Quality-check Emergent build-hub child pages before they are created in Webflow or published. Runs the deterministic QC engine (qc/qc_hub.py), then a judgment pass on search intent, claims, cannibalisation and quality, then a P0/P1/P2 report. Use this whenever Divit asks to check, QC, audit, review or verify a child page, a batch, a hub, or anything "before it goes live", and always before asking Divit to approve a batch, even if he does not name the skill.
---

# hub-qc: the gate before Webflow and before publish

Two independent roles use this skill, and neither may be the agent that wrote the page. Every review cycle uses a new reviewer and every challenge a new challenger (hubctl refuses a repeat). The reviewer reads the page cold first, then verifies earlier fixes; both list **every instance** of each defect they find, with its field and a quote, so the writer fixes the class, not the example: the **reviewer** scores the rubric (`hubctl review`, page in state `images`), then a different agent, the **challenger**, hunts for defects assuming there is at least one (`hubctl challenge`, page in state `reviewed`; see `.claude/agents/page-challenger.md`). A page reaches Divit only after both pass. Never review or challenge a page you wrote. In bulk work, take pages with `python3 ops/hubctl.py next qc_pass <HUB>` and end each with `hubctl state <url> reviewed --note ...` or `hubctl state <url> rework --note "<field: what to fix>"`. Small, certain fixes (a typo, an article) you may make and re-run QC; anything that changes meaning goes back as rework.

Prime directive: a page moves forward only at QC TOTAL = 0 (P0 + P1). P2 items are read and either fixed or explicitly accepted in the review notes. Rules only tighten; changing one needs Divit and a dated line in `DECISIONS.md`.

## Setup
If the repo is not set up in this chat: `git clone https://github.com/seo881/potential-enigma.git /home/claude/pe && cd /home/claude/pe && bash ops/setup.sh`. Read `rules/HUB_RULES.md` and `DECISIONS.md`.

## Layer 1: deterministic (code)
`python3 qc/qc_hub.py <spec>` (or `--hub <HUB>`, `--all`). It checks:
- **S** structure: fields in the collection map, required fields, `<h3>`+`<p>` shapes, how-to numbering, FAQ JSON (10-16 items, heading, `?`), 4 mockup keys, Emergent-first table, 6 images with alt.
- **L** limits calibrated on approved pages: meta title (60 chars, 580px, " | Emergent"), meta description (110-160), H1 (differs from title, 70 chars, "Build ..."), hero (about 30 words), why (25 words), H2s (48 chars), feature bodies (165-182, spread 12), FAQ answers (15-75 words), chips and tabs (26 chars).
- **H** hygiene: dashes, curly quotes, "built-in", "Type II", exclamations, emoji, we/our/us, US spelling everywhere (any UK form blocks), Title Case, a/an.
- **K** keywords: primary placement, slug, exactly one hub link in the FAQ, no external FAQ links, sibling primaries in headings (cannibalisation), secondary coverage, competitors outside the page's top 10.
- **V2/V3** comparison table generated from the vetted competitor library, unedited, with no fact past its re-check date.
- **V/C/D** vendor numbers without a dated check, claims against `rules/claims.json`, sentences duplicated from sibling pages.
- **FAQ shape:** exactly 10 items, every one an on-topic question a searcher asks (no filler); at least 6 secondaries, read naturally, each counted when all its words sit in one sentence in any order, and never two secondaries in back-to-back sentences of one answer (K8); one hub link in item 2 and 2-3 exact-match links to real Emergent pages (K4).
- **F** FAQ sourced from the live SERP: every item has a recorded source that exists (F2), stays close to the searcher's phrasing (F3), and no eligible People Also Ask question is left unanswered (F4).
- **T** rendered width: every field measured in the template's real typography against the widest approved rendering (T1); meta description pixels (L2); rich-text HTML shape identical to the approved live pages (S9).
- **Image numbers:** every quantity drawn is declared and true (`image_brief.checks`), shared values match across images, and every glyph exists in the font.
- **C2/C3** truth: no capability claim outside the approved ledger (high-risk terms block outright; `claims_used` lists the ledger ids), no unsourced third-party fact or statistic in prose.
- **D2** near-duplicates: no section sharing more than 30% of its phrases with another page in the hub.
- **F6/R3** SERP data under 30 days old; nothing changed since Divit's approval.
- **P** plan before prose (P1) and sourced domain claims (P2).
- **Q** craft: keyword-label openers (Q1), sentence length (Q2), H1 scope (Q3), category variant for the comparison column (Q4). Whole page, every instance reported: tacked-on endings ("which is what", "that is what" block; ", so" endings flag, more than 2 block) (Q5); any 6-word phrase in two different fields, FAQ answers included and the page's own keywords excluded (Q6); more than 3 "from X to Y" ranges (Q7); more than 8 "A, B, and C" lists, flagged (Q8).
- **R** the reviewer's rubric is recorded and passing for any page past review (R1).
- **I** the image brief, including the balance gate (no panel with more than 16% pooled empty space), rendered in memory through the image engine and its gates: fit, numbers adding up, one click, balance (I1 blocks, I2 notes). Copy-to-image story links (I4): every tab's `story` phrases exist in the tab copy and the drawn image, their numbers agree, every number in the tab copy is drawn, and every rule the image draws is linked to the copy.

## Layer 2: judgment (read the page against its brief)
Run `python3 ops/hubctl.py brief <url>` and check, writing each as P0/P1/P2:
0. **Claims:** every sentence about what Emergent does maps to an id in `claims_used`, and every id is approved in `rules/capabilities.json`. A claim with no matching entry is a defect, however plausible it sounds.
1. **Intent:** would this page satisfy someone who searched the primary, given what the top 10 shows? Does an AMBER page carry its angle?
2. **Promise vs delivery:** everything the title and meta promise ("examples", "templates", "free", "for Shopify") is on the page.
3. **Truth:** every Emergent claim is in the register; every third-party fact is current; nothing contradicts another field (numbers, steps, tab content vs images).
4. **Depth:** the definition up top where an AI Overview appears; FAQ questions match how people ask; the how-to is specific to this primary, not generic.
5. **Voice:** would this paragraph ship unedited on Linear's or Stripe's site (HUB_RULES 2a)? And would a reader suspect a machine wrote it? Look for generic claims where a specific detail belongs, hype verbs, tidy triplets, summary sentences, the same rhythm paragraph after paragraph. Any one of these is a rework note, even when the code QC passed.
6. **Distinctness:** reads as its own page, not a sibling with nouns swapped; tab H3s do not use sibling primaries; watch-list guidance from the brief is followed.
7. **Image brief and images:** every `fact` in `image_brief.checks` is truly standalone (never a total, difference or percentage change); the brief matches its tab copy (people, numbers, statuses agree); after rendering, each contact sheet shows one hero, readable text, numbers that add up, the cursor on a button edge.

## Divit's daily review page
Build one review page per day: a table of every page that reached `images` (URL, primary, H1, meta title, QC result, reviewer notes, contact sheet link), with the calibration batch (first batch of each hub) shown in full and, afterwards, a random 10% plus every page with an accepted P2 or a reviewer note shown in full. Divit's rejections become rule fixes (`rules/HUB_RULES.md`, `qc/qc_hub.py`, dated in `DECISIONS.md`), then QC re-runs on every page not yet published.

## Scored rubric (required)
Score all 10 criteria in `rules/rubric.json` pass or fail, each with evidence that quotes the page (for a fail, every instance on the page), and write them to a JSON file `{"scope": {"result": "pass", "evidence": "..."}, ...}`. Record it with `python3 ops/hubctl.py review <url> <file> --by <id>`: all pass moves the page to `reviewed`; any fail sends it to `rework` with your evidence as the fix list. QC code R1 blocks any page past review without a full pass, and `hubctl state <url> reviewed` refuses without one. Check every row of `rules/CONTENT_DEFECTS.md` as you score. When you find a new kind of defect, tell the coordinator so it joins the catalogue.

## Report format
For each page: `url | QC TOTAL | P0 list | P1 list | P2 list (fixed / accepted with reason)`. Then a batch line: pages passing, pages blocked, and the one decision (if any) that needs Divit. Fix methodology: root cause first, re-run the whole batch after any fix, never weaken a rule to pass.

## Rework protocol (writers, reviewers, challengers)
Fix the defect class, not the instance. After any note, search the whole page (every field, the FAQ, the image brief) for every occurrence of that class and fix them all, then search again, because rewrites create new instances. Reviewers and challengers list every instance they find. Each review cycle uses a new reviewer agent that reads the page cold before it reads earlier notes.

## Findings are rule violations (2026-10-07)
Every reviewer and challenger finding names the rubric criterion, cites the `rules/HUB_RULES.md` section or `rules/CONTENT_DEFECTS.md` row it breaks, quotes the field, and is marked `blocking` or `note`. `hubctl review` and `hubctl challenge` reject findings without a valid citation, and a criterion fails exactly when a blocking finding cites it. Only blocking findings send a page to rework; notes go to `spec.review_notes`, and `hubctl metrics` proposes a rule to Divit when a note recurs on 3+ pages. Check every third-party, legal and best-practice claim against `spec.domain_sources` (HUB_RULES 8): an unsourced or contradicted claim is blocking.

## Batch mode
One reviewer agent may review up to 4 pages, and one challenger up to 4, never a page it wrote or reviewed (hubctl refuses). Review each page as if it were the only one. Writers stay one page each.

## Plan and sources (QC P1, P2)
A spec without `spec.plan` (angle, four tab stories, openers, heading shapes, claims to source) is blocked, and so is any claim in the plan without a `spec.domain_sources` entry.

## Efficiency and severity (Divit, 2026-10-07)
- Agents read `hubctl pack <url> --role reviewer|challenger` plus the spec, not the full rulebook.
- Blocking: untrue claims, unsourced statements of fact about the world, every CONTENT_DEFECTS row (repeated ideas #21 included). Note: unsourced recommendations and wording improvements. Notes never trigger rework; `hubctl metrics` proposes a rule when one recurs on 3+ pages.
- Sources: at most 8 per page (QC P4); liveness is `hubctl sources-check` (QC P3 blocks dead or moved sources), never an agent re-reading pages.
- QC V4: a category variant must define every table row it is used with. Engine: hero cards are held to the balance gate (max 21% pooled), images draw only reserved example domains, and the code cover is only for codes.
