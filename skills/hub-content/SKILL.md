---
name: hub-content
description: Write child pages for Emergent's build hubs (AI Landing Page Builder, AI Form Builder, AI Automation Builder, AI Survey and Quiz Builder, and later hubs) from the Semrush keyword plan, as page specs ready for QC, images and the Webflow CMS. Use this whenever Divit asks to write, draft, create, brief or continue child pages, claim the next batch, work a hub queue, or says "next pages", "start the LP/Form/Automation/Survey hub", even if he does not name the skill.
---

# hub-content: writing build-hub child pages

The source of truth is the repo `seo881/potential-enigma`. This skill is the workflow; the detailed rules live in the repo so they can change without reinstalling anything.

## Before writing anything
1. Read the Project file `EMERGENT_BUILD_HUBS_HANDOFF.md` sections 0 and 2 (Divit's working rules, access, the GitHub token).
2. Clone and set up: `git clone https://github.com/seo881/potential-enigma.git /home/claude/pe && cd /home/claude/pe && bash ops/setup.sh`. Expect `SETUP OK`.
3. Read `RUNBOOK.md`, `DECISIONS.md`, `rules/HUB_RULES.md`, `SETUP_STATUS.md`, and the latest lines of `logs/<dir>.md` for your hub.
4. `python3 ops/hubctl.py status <HUB>`: resume any page that is mid-flight before claiming new ones.

## Per batch (5 pages by default, never more than 10)
1. **Claim:** `python3 ops/hubctl.py claim <HUB> 5 --by <chat-id>`; commit and push the status file at once so other chats see it.
2. **Brief each page:** `python3 ops/hubctl.py brief <url>`. Read all of it: the verdict and angle decide what kind of page wins; the top 10 decides the comparison competitors and the depth; SERP features decide whether a definition goes up top (AI Overview) and how FAQ questions are phrased (People Also Ask); the sibling list tells you which primaries you may not use as headings. Wave 3 pages have no top 10: get the live top 10 and apply the cut rules in `rules/HUB_RULES.md` section 3 before writing; park the page with evidence if a rule is met.
3. **Write the spec:** `python3 ops/hubctl.py init <url>` creates `specs/<dir>/<slug>.json`. Fill every field per `rules/HUB_RULES.md` sections 4 and 5. Write rich-text fields as exact HTML; build the FAQ and mockup embeds in Python (`json.dumps` for the FAQ object) so quoting is exact. List the secondaries you used in `keywords.secondaries_used`.
4. **QC:** `python3 ops/hubctl.py qc <url>` until TOTAL = 0, fixing root causes. Then use the `hub-qc` skill's judgment pass. Move the page to `qc_pass` with `hubctl state`.
5. **Images:** from the approved tab copy, per `IMAGE_PIPELINE_KT.md` and `SETUP_STATUS.md` (recipe library). Alt texts go into `spec.images`.
6. **Review:** show Divit the batch in one review artifact: each page's title, H1, meta, hero, features, tabs, how-to, FAQ, table, QC result and image contact sheet. Wait for his explicit go. Record it with `hubctl state <url> approved`.
7. **Create in Webflow:** commit and push; then `hubctl payload <url> --sha <sha>` and pass the file's content as the `actions` of `data_cms_tool`. Always drafts. Read back to disk (RUNBOOK 4.3), `hubctl verify`, `hubctl record`, commit, `hubctl log`.

## Writing standard (the short version; the full one is rules/HUB_RULES.md)
- Write the page that wins the actual SERP for the primary, at the depth the top 10 shows. Operator grade, specific, no fluff.
- Primary in the meta title, H1, meta description and first FAQ item. Secondaries woven in once each where natural.
- Never another page's primary in a heading. Link to sibling pages instead.
- "Emergent" / "Emergent's", never we/our. No em dashes, curly quotes, "built-in", exclamation marks, CTAs in body copy.
- Only claims in `rules/claims.json`. No vendor numbers unless checked that day and dated in the spec.
- Vary hooks and phrasing across the batch; no two pages share sentences.

## When to stop and ask Divit
A page meets a cut rule; the SERP wants something the template cannot deliver (a downloadable document, a playable quiz); a claim is not in the register; anything borderline. Give options with a recommendation and one question.

## Ending the chat
Before the context runs long (about 10 pages): commit and push everything, log the exact state and next step in `logs/<dir>.md`, and tell Divit to start a new chat with the prompt in `KICKOFF.md`.
