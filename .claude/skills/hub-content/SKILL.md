---
name: hub-content
description: Write child pages for Emergent's build hubs (AI Landing Page Builder, AI Form Builder, AI Automation Builder, AI Survey and Quiz Builder, and later hubs) from the Semrush keyword plan, content-first and in bulk, as page specs (copy plus image brief) ready for independent review, images and the Webflow CMS. Use this whenever Divit asks to write, draft, create, brief or continue child pages, claim the next batch, work a hub queue, or says "next pages", "start the LP/Form/Automation/Survey hub", even if he does not name the skill.
---

# hub-content: writing build-hub child pages

The source of truth is the repo `seo881/potential-enigma`. This skill is the workflow; the detailed rules live in the repo so they can change without reinstalling anything.

## Before writing anything
1. Read the Project file `EMERGENT_BUILD_HUBS_HANDOFF.md` sections 0 and 2 (Divit's working rules, access, the GitHub token).
2. Clone and set up: `git clone https://github.com/seo881/potential-enigma.git /home/claude/pe && cd /home/claude/pe && bash ops/setup.sh`. Expect `SETUP OK`.
3. Read `RUNBOOK.md`, `DECISIONS.md`, `rules/HUB_RULES.md`, `SETUP_STATUS.md`, and the latest lines of `logs/<dir>.md` for your hub.
4. `python3 ops/hubctl.py status <HUB>`: resume any page that is mid-flight before claiming new ones.

## Content-first, in bulk (target 200 pages a day across all writers)
You write copy and the image brief only. Review, images, Webflow drafts and publishing are separate stages run by other agents or chats (`RUNBOOK.md` section 2). This is what lets one chat write 25 pages without its context filling up.

1. **Claim:** `python3 ops/hubctl.py claim <HUB> 25 --by <chat-id>` (or take the pages the orchestrator assigned); commit and push the status file at once.
2. **For each page, in queue order:**
   - Pull the live SERP first: DataForSEO's Google organic live SERP for the primary (United States, English, People Also Ask click depth 2); save it with `python3 ops/hubctl.py serp-save <url> <raw.json> "<primary>"`.
   - `python3 ops/hubctl.py brief <url>` and read all of it, including the People Also Ask questions and related searches. The verdict and angle decide what kind of page wins; the top 10 decides the comparison competitors and the depth; SERP features decide whether a definition goes up top (AI Overview) and how FAQ questions are phrased (People Also Ask); the sibling list tells you which primaries you may not use as headings. Wave 3 pages have no top 10: get it first and apply the cut rules (`rules/HUB_RULES.md` section 3); park the page with evidence if a rule is met.
   - `python3 ops/hubctl.py init <url>`, then fill every field per `rules/HUB_RULES.md` sections 4 and 5, with exactly 10 FAQ items (every one a real, on-topic search; never filler) sourced from People Also Ask, then related searches, secondaries and keyword ideas, each recorded in `faq_sources`, carrying as many secondaries as read naturally (6+), with the hub link in item 2 and 2-3 exact-match links to related pages (rules/HUB_RULES.md section 5). Write the `image_brief` too, with `checks` declaring every number each image draws (docs/IMAGE_BRIEF.md); QC renders it in memory and measures every field in the template's real typography. Build the FAQ and mockup embeds in Python (`json.dumps`) so quoting is exact. List the secondaries you used in `keywords.secondaries_used`. Build the comparison table with `hubctl table <url> --vs A,B,C --rows ...` from the vetted library (never type it); write the `image_brief` per `docs/IMAGE_BRIEF.md`.
   - `python3 ops/hubctl.py qc <url>` until TOTAL = 0, fixing root causes; then `hubctl state <url> qc_pass`.
   - Commit and push every 5 pages, so nothing is lost if the chat ends.
3. **Rework:** pages a reviewer sent back (`hubctl next rework <HUB>`) come before new claims. Fix exactly what the note says, re-run QC, set `qc_pass`.
4. **Hand-off:** when your pages are all `qc_pass`, log the range in `logs/<dir>.md` and stop. Reviewers take it from there.

## First pass at the final standard
Before writing, read `rules/CONTENT_DEFECTS.md`: every defect that has ever made a page less than world class, with the before and after. Before running QC, score your own page against the 10 criteria in `rules/rubric.json` (scope, intent, specificity, openers, craft, voice, truth, distinct, faq, images) and rewrite anything that fails. QC then catches what can be measured: keyword-led openers (Q1), sentences over 40 words (Q2), H1s that lean on a sibling's topic (Q3), the wrong Emergent column for the category (Q4), tacked-on endings (A1), and images with empty zones (I1). A page should pass QC on its first run.

## Writing standard (the short version; the full one is rules/HUB_RULES.md)
- Write the page that wins the actual SERP for the primary, at the depth the top 10 shows. Operator grade, specific, no fluff.
- **Voice of a world-class SaaS company** (Stripe, Linear, Vercel, Notion): confident, precise, product-led, economical, US spelling throughout (`rules/HUB_RULES.md` 2a).
- **It must never read as AI-written** (`rules/HUB_RULES.md` section 2b): concrete details, plain verbs, varied rhythm, none of the words in `rules/ai_tells.json`. Read every paragraph as if a product lead were saying it to a customer.
- Primary in the meta title, H1, meta description and first FAQ item. Secondaries woven in once each where natural.
- Never another page's primary in a heading. Link to sibling pages instead.
- "Emergent" / "Emergent's", never we/our. No em dashes, curly quotes, "built-in", exclamation marks, CTAs in body copy.
- Only capabilities in `rules/capabilities.json` (approved section); list their ids in `claims_used`. Pending terms (money movement, tax, compliance, SLAs, security specifics, native mobile, accuracy numbers, e-signature, real-time) block until Divit approves. Third-party facts and statistics in prose only if they are in `rules/facts.json`. Comparison tables only from the library.
- Vary hooks and phrasing across the batch; no two pages share sentences.

## When to stop and ask Divit
A page meets a cut rule; the SERP wants something the template cannot deliver (a downloadable document, a playable quiz); a claim is not in the register; anything borderline. Park the page with a note (`hubctl state <url> parked --note ...`), keep writing the rest, and list parked pages for Divit at the end with options, a recommendation and one question.

## Ending the chat
After 25 pages, or earlier if replies slow down: commit and push everything, log the exact state and next step in `logs/<dir>.md`, and tell Divit to start a new chat with the prompt in `KICKOFF.md`. In Claude Code this skill runs inside a `page-writer` subagent, one page per subagent, so there is no such limit.
