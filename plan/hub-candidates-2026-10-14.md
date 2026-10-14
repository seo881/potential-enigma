# Next 2 hubs: candidates (A-h-1, 2026-10-14)

Divit's request (DECISIONS 2026-10-14, "Next 2 hubs"): propose 2 to 4 candidate hubs from Emergent's product, each with a Semrush-sized keyword pool (count of build-intent child keywords and total MSV) and what the template clone takes; Divit picks 2.

Public-safe: counts and totals only. The keyword lists, head terms, SERP checks and exclusions are in `.cache/review/hub-candidates-2026-10-14.md` (git-ignored); raw Semrush responses in `private/semrush/hubs/`.

## How the pools were sized
- Semrush API (database us): broad-match pulls on each theme's build modifiers, then exact volumes for every candidate child's build-intent phrasings.
- A child is one buildable artifact with a primary MSV of 50 or more on a build-intent phrasing. It is not a brand and not informational-only, it is merged with its variants, it is not already in `plan/keyword_map.json`, and it is not already a child page on emergent.sh.
- Counts are floors: pulls were capped for budget. A deep pull on the 2 chosen hubs sizes the full queue.
- **Found on the live site:** emergent.sh already runs 9 other builder hubs with child pages (app, web app, dashboard, CRM, agent, schedule, website, SaaS, chatbot; about 2,000 pages). Website, app or mobile app, dashboard, chatbot, CRM and booking candidates are therefore taken: a new hub there would cannibalize.

| Candidate | Build-intent children | Sum of child primary MSV | Child cluster MSV | Intent check (3 SERPs) |
|---|---|---|---|---|
| AI Checklist Builder (operational and inspection checklists) | 64 | 35,290 | 65,720 | template plus checklist-app vendors: fits |
| AI Portal Builder | 32 | 9,690 | 14,110 | software comparisons, build-your-own in the SERP: strong fit |
| AI Game Builder (generic formats) | 29 | 153,930 | 286,870 | free single-purpose generators: medium to weak |
| AI Game Builder, trademarked formats (needs a brand ruling) | 10 | 147,670 | 224,880 | same |
| AI Database Builder | 26 | 7,040 | 10,500 | not checked |
| AI Directory Builder | 15 | 4,220 | 7,950 | not checked |
| AI Tracker Builder (trackers not already live elsewhere) | 28 | 15,440 | 39,970 | not checked; about 40 trackers already live on other hubs |

Sized and set aside: calculator (thin build intent), internal tool and admin panel (navigational noise), marketplace (thin), booking (covered by the schedule hub and Form), management systems and online store (covered by the app and website builders).

## Recommendation: Checklist and Portal

1. **AI Checklist Builder** (`/ai-checklist-builder`, working name). It has the deepest supply: 64 children as a floor, and likely about 120 after a deep pull, because the inspection, cleaning, maintenance and onboarding families are each only partly pulled. The searchers are operators: property managers, fleet and warehouse leads, facilities, cleaning companies, HR. The SERPs show the same thing the Form hub already wins against: a PDF or template, plus checklist-app vendors. Emergent's angle is honest under approved claims: the checklist becomes an app with photos, failed items that alert someone (`alerts`), sign-off (`e-signature-capture`), history in the user's database (`database-owned`) and a live dashboard (`realtime`). Overlap with live pages is small and has been excluded. Watch item: "offline mode" for field inspections is not an approved claim, so it goes to `pending` or stays out of the copy.
2. **AI Portal Builder** (`/ai-portal-builder`). This is the closest fit to Emergent's core: a full-stack app with logins, roles, a database, integrations (`api-connect`) and a custom domain (`custom-domain`). The intent is commercial: the SERPs show buyers comparing portal software, and Softr and Budibase pitch build-your-own. It has 32 children; total MSV is small, but the value per visit is the highest of the candidates. Watch items: the hub must not target "client portal" as its head, because two live pages already use it. Portal SERPs also talk about SSO, encryption and compliance, which are pending claims, so the competitor library and writers must stay inside the approved list.

**Alternative if traffic matters more than fit:** AI Game Builder has 29 generic children with by far the most MSV (primary about 154k), plus 10 trademarked formats (about 148k). Three things weigh against it: (a) its intent fit is weaker, because the SERPs are free single-purpose generators; (b) its head term competes with `/ai-app-builder/ai-game` and `/ai-app-builder/game`; (c) the trademarked formats need Divit's brand ruling. **Database** (26 children) is a reasonable fourth. Directory (15) and Tracker (28 new, with about 40 trackers already live elsewhere) are too thin or too covered.

## Template clone: what it takes (per hub; both hubs run in parallel, staging first, new classes only)

Facts this rests on:
- The 4 child collections are clones of the CRM collection: 62 field slugs each, at Webflow's 60-custom-field cap (`config/collections.json`).
- Cloned collections share field slugs, but the prefix-named fields get new prefixes (KT 11.3).
- `ops/webflow_api.py` derives its allowlist from `config/collections.json`, so a new hub entry extends the CMS write path without code changes.
- Designer-only behaviours that bit us before:
  - the "Publish this Collection Template page" switch (LESSONS 2026-10-09: 20 pages 404'd);
  - collectionPage links on the carousel and Learn cards (WEBFLOW_API 2026-10-13);
  - the OG image binding (T11);
  - the cover alt binding (T5).

| # | Step | Who | How | Time |
|---|---|---|---|---|
| 1 | Pick 2 hubs, names and slugs | Divit | reply | 5 min |
| 2 | Deep keyword pull for the 2 hubs (Keyword Magic equivalent, about 2-3k rows each), then build the keyword map rows and queue (`plan/build_map.py` reads the workbook today; add a reader for `private/semrush/hubs/`) | A | Semrush API + repo | 3 h, about 40-60k units per hub |
| 3 | Duplicate an existing child collection (Form or SurveyQuiz) with its template page: Collection settings, Duplicate (UNVERIFIED on this site: check that the template's bindings and embeds come along). Name it, set the collection slug, turn ON "Publish this Collection Template page" | Divit (Designer) | click steps from A | 15 min |
| 4 | Duplicate the matching hub page; set slug, SEO title and description | Divit (Designer) | click steps from A | 10 min |
| 5 | Read back the new collection (`get_collection_details`), template and hub page: map the 62 slugs and new prefixes into `config/collections.json` (`collection_id`, `template_page_id`, `hub_page_id`, `path`, `repo_dir`, `prefix`, `chip_prefix`, `hub_link_text`, `palette`, `category_option_ids`) | A | Webflow MCP read only + repo | 1 h |
| 6 | Template checks against the 12 T-edits: hero chips embed (T1), FAQ guard (T2), Learn list (T3), aria-label (T4), form names / duplicate IDs (T9). Re-add by API only what the duplicate lost | A | MCP read, then staged writes on Divit's go | 1-2 h |
| 7 | Designer-only settings on the new template and hub page: OG image = Thumbnail (T11), cover alt = Product name (T5), carousel `build_link` and Learn `blog_link` to the collection page, the hub carousel list sourced from the new collection, default tab (T10) | Divit (Designer) | click steps; A verifies by reading | 30 min |
| 8 | Hub page copy (hero, value cards, FAQ) and 6 hub value-card visuals; new classes only, nothing sitewide (nav and footer links stay Divit's call) | A (writer + reviewer) | spec, QC, MCP staged writes on go | half a day |
| 9 | Repo wiring: hub key in `ops/hubctl.py` (`WRITER_HUBS`, `.hub` ownership), `ops/skeleton.py` hero-prompt line, `ops/semrush_questions.py` `HUB_PATH`, `ops/rework_plan.py`/`weekend.py`/`overnight.py` lists, `status/<dir>.json`, `logs/<dir>.md`, `specs/<dir>/` | A | repo | 1 h |
| 10 | Competitor library `rules/competitors/<dir>.json` (names, categories, pricing facts with sources) and the why-table variants; `rules/audience.json` ("your team" allowed?); any new capability lines go to `pending` for Divit | A | research + repo | 2-3 h |
| 11 | Image pipeline: palette in `pipeline/hubs_v5.py` PALS (contrast-tested with `qa3`), `pipeline/engine.py` PALETTE, `scenes.py`, cover in `covers_v5.py`, hub card in `hubcards_v6.py`; read the new template's use-case slot CSS (3:2 shape gate) | A | repo + MCP read | 2-3 h |
| 12 | Page schema: `schema/templates.json` + `build_templates.py` (JSON-LD for the new template) | A | repo; the paste into page settings is a Designer step for Divit | 30 min + 5 min Divit |
| 13 | QC: golden cases for the new hub (`tests/golden`), an exemplar page (`specs/<dir>/_exemplar.md`), run the full golden suite (0 regressions) | A | repo | 1 h |
| 14 | Canary (LESSONS rule 1): 3 child pages written, reviewed and imaged, created as drafts through `hubctl api-create --limit 2` then 1, and checked by Divit in the Designer. Then a staging publish request (Divit publishes staging; Claude never publishes the site) and `verify_launch` on webflow.io | A, then Divit | `hubctl` + Designer + staging | 1 day elapsed |
| 15 | Production go: Divit publishes the site (template and hub page); children go live only as item publishes, followed by `verify-live` | Divit, then A | Designer, then `hubctl api-publish` | 30 min |

**Estimate:**
- Divit: about 1.5 h of Designer clicks per hub (about 2.5-3 h for both), plus canary review and the staging and production publishes.
- A: about 2 working days of effort for both hubs, mostly in parallel with production.
- Elapsed time to the first writable batch: about 3 days. Day 1: the pull, Divit's duplicates, readback and config. Day 2: library, palette, schema, hub copy and QC. Day 3: the canary on staging. Bulk writing starts after the canary passes.
- No Webflow call in any of this happens without Divit's per-call approval. Nothing is published by Claude except item publishes after his go.

## Semrush units
107,950 units for this task (balance delta per call), inside the 150,000 task cap and the 25% line.
