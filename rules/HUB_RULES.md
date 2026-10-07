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
- **US spelling everywhere [QC, blocking]:** -ize not -ise (organize, customize), color, behavior, center, catalog, license, inquiry, canceled, traveled, analyze, judgment, toward, among, while. Full list in `rules/us_spelling.json`.
- **Subject-verb agreement** is checked by reading every sentence whose subject is a list or a collective noun.
- **Numbers:** numerals for 10 and above and for all amounts, scores and durations. Thousands separators. Currency as $4,800.00 only where cents matter.

## 2a. Voice: a world-class SaaS company (Divit, 2026-10-07)

Every page should read like it came from the best product companies' marketing and docs teams: Stripe, Linear, Vercel, Notion, Figma. That voice is:

- **Confident and calm.** State what the product does. No hype, no exclamation, no hedging ("can help you potentially"). If a claim needs a qualifier, it is the wrong claim.
- **Precise.** Real nouns and numbers: "routes anything over $5,000 to the CFO", not "handles complex approvals". Name the trigger, the field, the tool, the outcome.
- **Product-led.** Show the product doing the job; the reader infers the benefit. "Every response is a row in your database" beats "gain powerful insights".
- **Economical.** Short declarative sentences, one idea each. Cut every word that does not change the meaning: very, really, just, simply, basically, actually, easily, a wide range of, in order to [QC flags them].
- **Respectful of the reader.** Speak to a capable operator. Never explain the obvious, never sell with fear, never talk down.
- **Consistent.** Same term for the same thing across the page (pick "response" or "submission", not both). Sentence case for body headings, Title Case where rule 2 says so.

| Instead of | Write |
|---|---|
| Unlock seamless approvals that empower your team | Route each request to the right approver and log every decision |
| Easily create beautiful forms in seconds | Describe the form; Emergent builds the fields, logic and database |
| Our powerful AI handles everything for you | Emergent writes the workflow, the trigger and the dashboard from one prompt |
| A wide range of integrations to supercharge your stack | Connects to Slack, HubSpot, Stripe and anything with an API |

The reviewer's test for every paragraph: would it ship unedited on Linear's or Stripe's site?

## 2b. Human voice: the page must never read as AI-written

The reader should feel an operator who has built this many times wrote it. Claude Code is only how we scale; the standard is a senior human writer's.

- **Specific beats general.** Name the fields, the trigger, the approver, the tool, the number. "Route anything over $5,000 to the CFO" beats "handle complex approvals".
- **Say what Emergent builds, not how it feels.** No hype, no promises of transformation. Plain verbs: builds, sends, saves, routes, flags, exports.
- **Banned vocabulary [QC P1]:** the AI-tell list in `rules/ai_tells.json` (seamless, unlock, elevate, empower, delve, robust-as-filler, "in today's...", "the power of", "it's not just X, it's Y", and the rest). Borderline words (leverage, streamline, ensure, solution, journey) are flagged [QC P2] and stay only when they are the plainest literal word.
- **Rhythm.** Vary sentence length and openers; no run of sentences starting the same way [QC P2]; no connector openers (Moreover, Furthermore, Additionally). Short declaratives are fine. One idea per sentence.
- **No filler structures:** no "Whether you're X or Y", no rhetorical questions in body copy, no tidy triplets everywhere, no summary sentence restating the paragraph.
- **Read it aloud.** If a sentence would sound strange said by a product lead to a customer, rewrite it.
- **Voice of the examples:** concrete, slightly unglamorous details (order #10482, a $180 client dinner, a two-day reminder) are what make a page read as real.

## 3. SEO method (from the Semrush plan)

Read the page's brief first: `python3 ops/hubctl.py brief <url>`. It gives the primary, every secondary with volume, intent, KD, the SERP verdict, the AMBER angle, SERP features, the top 10, watch-list guidance and the sibling pages in the same cluster.

1. **Primary placement [QC]:** in the meta title and the H1 (P0), the meta description (P1), the first FAQ item and the hero or features subheading (P2). Natural phrasing; plural or singular both count.
2. **Match the SERP, not your assumption.** The top 10 tells you what searchers want: tool roundups mean a software angle; example galleries mean show examples; guides mean definitional depth; template sites mean the page must yield the finished artifact. Write the page that wins that SERP.
3. **AMBER pages** rank only with the angle on their row. The angle is not optional; it shapes the H1, the tabs and the FAQ.
4. **AI Overview on the SERP** (61% of Automation, 39% of LP primaries): put a one or two sentence definition of the primary in the hero description or the features subheading, and make FAQ item 1 the definition. Answer-first sentences get cited.
5. **People Also Ask drives the FAQ (Divit, 2026-10-06).** Before writing, pull the live Google SERP for the primary through DataForSEO (United States, English, PAA click depth 2) and save it (`hubctl serp-save`). The brief then lists the PAA questions and related searches. See section 5, FAQ.
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

**Comparison table (`why_table`) [QC V2, V3]:** generated, never typed: `hubctl table <url> --vs A,B,C --rows id[=Label],...` builds it from the hub's vetted competitor library (`rules/competitors/<dir>.json`, `hubctl library <HUB>` lists it). Pick the 3 competitors that rank for this page's query (the brief's top 10 and live SERP) and the 4-5 dimensions that matter for it. Every fact in the library carries a source and a check date; numeric facts expire after 90 days, others after 180 (QC V3). A competitor or dimension the page needs that is not in the library is added to the library first, with sources, by the coordinator, never written into the page. The Emergent column uses approved claims only.

**FAQ (`window.awbFAQ`) [QC]:** sourced from what people actually search, never invented. Order of sources: (1) every People Also Ask question in the captured SERP, phrased the way searchers ask it (light grammar edits only; QC F3 checks the wording stays close), except PAA questions that name another page's primary, which belong to that page's FAQ (the brief marks them); (2) related searches, turned into the question they imply; (3) the page's secondaries, as questions. A definition item for the primary is allowed if PAA has none. Record the source of every item in `spec.faq_sources` as `{"q": <FAQ question>, "source": "paa|related|secondary|definition", "ref": <the exact PAA question, related search, secondary or primary>}`; QC F2 checks each one exists, F4 that no eligible PAA question is left unanswered. Answers are written in your own words: never copy or paraphrase the snippet Google shows under a PAA question. Heading "{Topic} Questions, Answered". **Exactly 15 items** [QC]. Item 1 defines the primary. Answers 15-75 words, answer-first. **Secondaries:** the FAQ carries as many of the page's secondaries verbatim as read naturally, at least 10 (or all of them if fewer) [QC K8]; the question-per-secondary pattern makes this easy. When PAA, related searches and secondaries run out before 15, use the DataForSEO keyword ideas captured with `hubctl serp-keywords` (source `keyword`). **Links** [QC K4]: exactly one hub link, in item 2 (the how-to-build answer): `Emergent's <a href='https://emergent.sh/{hub-path}'>{hub link text}</a>`; plus 2-3 links to related Emergent pages (sibling child pages, or another hub), one per answer, never in item 1, each anchored with the target page's exact keyword, e.g. `<a href='https://emergent.sh/ai-automation-builder/invoice-automation'>invoice automation</a>`. Use single quotes in href. No external links. A page whose FAQ links to a page that is not live yet is held at publish until that page is live or ships in the same batch. Questions end with "?". This field is a single rich-text embed: build it in code, never by hand.

**Images (6):** 4 use-case SVGs, 1 cover SVG, 1 share PNG from the page's `image_brief` (`docs/IMAGE_BRIEF.md`). Style (Divit and the Webflow developer, 2026-10-07): neutral grey canvas behind every image; the artifact carries colour, one accent per image, rotating across the page's four tabs (hub colour first, then blue, emerald, orange, violet), so no page is one colour. Alt text is specific, one or two sentences, no "image of".

**References:** `learn` (up to 3 relevant Learn articles), `integration` (only integrations that have a live page). Leave empty rather than link something loosely related.

## 6. Claims

Only claims in `rules/claims.json` (approved) may be stated as fact. Anything else about Emergent's capabilities, compliance, pricing or limits goes to Divit first. The agent can build what is explicitly asked, so "you can build X" is fine; "Emergent includes Y out of the box" needs a source.

## 7. Batches, scale and variety
- Content-first: writers produce copy and the image brief; review, images, drafts and publishing are separate bulk stages (`RUNBOOK.md` section 2). Target 200 pages a day across all writers.
- A writer chat takes 25 pages; a Claude Code writer subagent takes exactly 1. Commit every 5 pages.
- Every page is reviewed by an independent reviewer before images. Nobody reviews their own writing.
- Divit reviews the first batch of each hub in full (calibration), then a daily random 10% plus every flagged page. A defect he finds becomes a rule, and QC re-runs on all unpublished pages.
- Within a hub, vary H1 hooks, why descriptions, FAQ phrasing and feature 6. Two pages must never share two or more identical sentences [QC]. At 200 pages a day this check is what keeps pages from reading alike: treat a D1 failure as a writing problem, not a wording tweak.
- Check the last page of a batch as carefully as the first.

## 7b. Rendered width (the template's real typography) [QC T1]
Every field is measured in the template's own type (Brockmann headings, Inter body, at the sizes and tracking set in Webflow) and may not render wider than the widest approved rendering of that field (`config/typography.json`). Shorten the words, never the meaning. The breadcrumb and the Explore button carry the keyword and are confirmed in the real template instead. Ceilings grow only with proof: a page Divit approves as rendered in Webflow (`hubctl verified`) joins the calibration. Meta descriptions stay within about 920px at Google's 14px Arial.

## 8. First pass at the final standard
- The bar is set by `rules/rubric.json` (10 criteria) and `rules/CONTENT_DEFECTS.md` (every defect seen so far, before and after). The writer scores the page against both before QC; the reviewer scores it again, independently, and records the result (`hubctl review`). A page cannot move past review without 10/10 (QC R1).
- What can be measured is blocked by code: Q1 keyword-label openers, Q2 sentences over 40 words, Q4 generic comparison column, A1 tacked-on endings and AI tells, I1 image panels with empty zones. Q3 flags H1s leaning on a sibling's topic for the rubric's scope check.
- Every rejection becomes a catalogue row the same day, and a QC check when it can be measured.

## 9. Fixing (from the QC rulebook)

- Fix the root cause, then re-run QC on the whole batch, not just the line that failed.
- Never weaken a rule to make a page pass. Rules only tighten (ratchet). A rule change needs Divit and a dated line in `DECISIONS.md`.
- A page ships only at QC TOTAL = 0 (P0 + P1). P2 items are read and either fixed or explicitly accepted in the review notes.
