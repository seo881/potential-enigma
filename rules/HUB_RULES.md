# Build-hub child pages: writing rules

Applies to every child page in the four build hubs (AI Landing Page Builder, AI Form Builder, AI Automation Builder, AI Survey and Quiz Builder) and to the next hubs. Sources: Divit's rules (handoff section 0), Divit's builder-pages rulebook (global copy rules and QC method), the hub profile locked on 2026-10-06, and the Semrush keyword plan (pass 3). Where these conflict, Divit's explicit instruction in conversation wins, then `DECISIONS.md`, then this file.

`qc/qc_hub.py` enforces everything marked **[QC]**. Everything else is judgment, checked in review.

---

## 1. Non-negotiables (Divit)

1. Nothing goes to the live site without Divit's explicit go. Approval for one thing never extends to the next.
2. Before every write: read the current value and commit it. After every write: read back and diff. Rollback must always be one call.
3. Touch only the pages in scope. Never edit a component definition, an existing class, a template, or another hub's collection.
4. Do not assume. If something is borderline, ask, with options and a recommendation, one question at the end.
5. Copy is operator grade: concrete, no fluff, never narrows the audience ("for you", "for your business"; "for your team" only when the subject is a group).
6. Write "Emergent" or "Emergent's". Never "we", "our", "us". **[QC]**
7. Quality bar: world class. If asked "is this your best?", answer honestly.

## 2. Global copy rules (rulebook)

- **Hard bans [QC]:** em dash and en dash; curly quotes and apostrophes (ASCII only); "built-in" (write "included"); "Type II" (only SOC 2 Type I is approved); "&amp;amp;"; exclamation marks; emoji; placeholder text.
- **No CTAs in body copy.** The template carries the CTA buttons ("Start building free", "Build My ..."). Body copy explains; it does not say "sign up now".
- **Title Case [QC]** on the H1, section H2s, prompt chips and tab labels. AP style: lowercase only articles, coordinating conjunctions and prepositions of three letters or fewer (a, an, the, and, but, or, for, in, of, on, to, by, at, via, vs) unless first or last. Capitalise each part of a hyphenated compound ("Multi-Level Routing"). Feature H3s, tab H3s and how-to step titles are sentence case.
- **Articles [QC]:** a/an by sound. "an FAQ", "an HR team", "an NPS question", "an SLA", "a UGC creator", "a one-page site", "an hour".
- **US spelling [QC]:** inquiry, color, customize, behavior, favorite, license, center, canceled.
- **Subject-verb agreement** is checked by reading every sentence whose subject is a list or a collective noun.
- **Numbers:** numerals for 10 and above and for all amounts, scores and durations. Thousands separators. Currency as $4,800.00 only where cents matter.

## 3. SEO method (from the Semrush plan)

Read the page's brief first: `python3 ops/hubctl.py brief <url>`. It gives the primary, every secondary with volume, intent, KD, the SERP verdict, the AMBER angle, SERP features, the top 10, watch-list guidance and the sibling pages in the same cluster.

1. **Primary placement [QC]:** in the meta title and the H1 (P0), the meta description (P1), the first FAQ item and the hero or features subheading (P2). Natural phrasing; plural or singular both count.
2. **Match the SERP, not your assumption.** The top 10 tells you what searchers want: tool roundups mean a software angle; example galleries mean show examples; guides mean definitional depth; template sites mean the page must yield the finished artifact. Write the page that wins that SERP.
3. **AMBER pages** rank only with the angle on their row. The angle is not optional; it shapes the H1, the tabs and the FAQ.
4. **AI Overview on the SERP** (61% of Automation, 39% of LP primaries): put a one or two sentence definition of the primary in the hero description or the features subheading, and make FAQ item 1 the definition. Answer-first sentences get cited.
5. **People Also Ask on the SERP:** FAQ questions should mirror real PAA phrasing for the primary and its top secondaries.
6. **Secondaries:** use the top 15 by volume where they fit naturally, each once, across body, FAQ and tabs. Coverage under 40% is flagged [QC P2]. Never stuff; never use a secondary as a heading if it reads unnaturally.
7. **Cannibalisation [QC]:** never use another page's primary in an H1, H2, H3 or FAQ question. When a tab or FAQ naturally covers a sibling topic (for example "invoice" on an approval page), phrase it differently and link to the sibling in body copy. The keyword plan assigns every keyword to exactly one URL across all four hubs; respect it.
8. **Watch-list pairs** come with guidance in the brief (for example: patient intake stays strictly medical; CX survey is journey-wide while CSAT is the transactional score). Follow it.
9. **Wave 3 pages** (no top 10 pulled): get the live top 10 before writing, then apply the cut rules: A (8+ of 10 owned by the issuer the searcher must use, no builder or template site), B (8+ of 10 are one numbered government form or guides to it), C (a document only a government office issues, 5+ of 10 that office). A page meeting a cut rule is parked, with evidence, for Divit.

## 4. The hub profile (locked 2026-10-06)

| Element | Pattern | Limit [QC] |
|---|---|---|
| Meta title | Keyword-led natural phrase ending " \| Emergent". Colon optional. Must read like something a person would write: no keyword lists, no slogans. | 30-60 chars and 580px or less at Google's 20px Arial |
| Meta description | What the page delivers, in the searcher's words, ending "Free to start." where it fits. No vendor numbers. | 110-160 chars (155 ideal) |
| H1 (`name`) | "Build a/an {keyword} {outcome hook}". Different from the meta title. | 70 chars |
| Hero description | 2 lines: what to describe, what Emergent builds, one differentiator. | about 30 words |
| Section H2s | Title Case, one idea. | 48 chars (2 lines) |
| Features subheading | One or two sentences. | 135 chars |
| Why title | "Why Build Your {Keyword} With Emergent?"; shorten the keyword if over 48 chars. | 48 chars |
| Why description | The core reason in one breath. | 25 words |
| How-to title | "How to Build a/an {Keyword}" or "How to Create ..." (use the verb people search). | 48 chars |
| Breadcrumb | The display name, Title Case. | |
| Explore CTA | "Build My {Display Name}". | |

## 5. Field-by-field guide

**Features (6) [QC]:** `<h3>title</h3><p>body</p>`. Titles are concrete capabilities, 2 lines max (48 chars). Bodies are 165-182 characters with a spread of 12 or less across the six, so the grid is level. Feature 6 is usually "Full code export"; vary its wording per page.

**Use-case tabs (4):** four distinct sub-use-cases of the primary, each a real segment searchers have (industries, roles, document types). Tab labels: Title Case, 26 chars max. Tab content `<h3>` + `<p>`: the H3 names the outcome, the paragraph says what gets built, what it connects to and what lands in the database. The tab copy is the brief for that tab's image: write it concretely enough to draw.

**Mockup prompts (`window.awbMockup`, 4 keys) [QC]:** one prompt per tab, in the user's voice ("my team", "my store"), 40-80 words, describing exactly what that tab shows. Keys are camelCase tab names.

**Prompt chips (4) + hero prompt:** chips name the four most-searched capabilities for the primary, Title Case, 26 chars max. Hero prompt: one plain sentence a user would type.

**How-to (7 steps) [QC]:** titles "01 ..." to "07 ...", sentence case, each an action. Descriptions 35-50 words, practical, specific to the primary. Step 1 can frame the choice of approach; never a hard sell.

**Comparison table (`why_table`) [QC]:** the Emergent-first layout (`cmp cmp--emg-first`), Emergent column first, 3 competitor columns, 4-6 rows. Competitors come from the page's top 10 (the tools that actually rank), not from memory. No vendor prices or plan limits unless checked that day and dated in `spec.vendor_facts_checked`; prefer durable facts ("form stops collecting at the plan cap") over numbers.

**FAQ (`window.awbFAQ`) [QC]:** heading "{Topic} Questions, Answered". 10-14 items. Item 1 defines the primary. Answers 15-75 words, answer-first. Exactly one link, to the hub, inside the "How do I create ..." answer: `Emergent's <a href=\"https://emergent.sh/{hub-path}\">{hub link text}</a>` (escaped quotes as stored). No external links. Questions end with "?". This field is a single rich-text embed: edit it in code, never by hand.

**Images (6):** 4 use-case SVGs, 1 cover SVG, 1 share PNG, through the v5 image pipeline (see `IMAGE_PIPELINE_KT.md` in the Project and `SETUP_STATUS.md` for the recipe library). Alt text is specific, one or two sentences, no "image of".

**References:** `learn` (up to 3 relevant Learn articles), `integration` (only integrations that have a live page). Leave empty rather than link something loosely related.

## 6. Claims

Only claims in `rules/claims.json` (approved) may be stated as fact. Anything else about Emergent's capabilities, compliance, pricing or limits goes to Divit first. The agent can build what is explicitly asked, so "you can build X" is fine; "Emergent includes Y out of the box" needs a source.

## 7. Batches and variety

- A batch is at most 10 pages per chat (5 is the default), reviewed together.
- Within a batch and a hub, vary H1 hooks, why descriptions, FAQ phrasing and feature 6. Two pages must never share two or more identical sentences [QC].
- Check the last page of a batch as carefully as the first.

## 8. Fixing (from the QC rulebook)

- Fix the root cause, then re-run QC on the whole batch, not just the line that failed.
- Never weaken a rule to make a page pass. Rules only tighten (ratchet). A rule change needs Divit and a dated line in `DECISIONS.md`.
- A page ships only at QC TOTAL = 0 (P0 + P1). P2 items are read and either fixed or explicitly accepted in the review notes.
