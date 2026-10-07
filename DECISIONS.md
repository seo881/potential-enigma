# Decisions log (Divit)

Every ruling Divit has made that a future chat must respect. Newest first. Add a line for every new decision, with the date and where it came from. Never re-ask something settled here.

## 2026-10-07
- **Wave 3 calls** (delegated by Divit to Claude's judgment): cut the 8 Rule A pages (citizen complaint, whistleblower, dependent verification, wire transfer request, 401k rollover, financial assistance, HSA reimbursement, dealer application); merge agency into design-agency landing page, author into book landing page, business coaching intake into life coaching intake. Applied in `plan/overrides.json`; 588 pages queued.
- **Voice: a world-class SaaS company** (Stripe, Linear, Vercel, Notion): `rules/HUB_RULES.md` 2a; filler and hedge words flagged by QC.
- **US spelling everywhere**, UK forms block (`rules/us_spelling.json`, QC H2).
- **DataForSEO:** connected in Claude Code. Custom connectors are not allowed for the org in Claude.ai, so SERP pulls run in Claude Code; a chat that needs one gets the saved file uploaded.

## 2026-10-06
- **FAQs come from People Also Ask** (Divit): live Google SERP per page through DataForSEO (MCP `https://mcp.dataforseo.com/mcp`, OAuth); every FAQ item carries a recorded source (PAA, related search, secondary, or the definition); QC F1-F5. SERP data stays in `private/` (git-ignored).
- **Images on hold** (Divit): the hub palettes are not Emergent's brand colours. No image briefs or renders until the brand palette is set; then the engine's palettes change and everything re-renders. The 4 live pages' images are untouched.
- **Wave 3 SERP report merged** into the plan: 155 more pages have their top 10; 11 pages (8 cut Rule A, 3 merges) are held as `needs-decision` and out of the queue until Divit decides; 87 pages with no Semrush data get their live SERP from DataForSEO at brief time.
- **Image engine for all new pages** (Divit asked for it before the dry run): images come from the page's `image_brief`, rendered through layouts taken from the 16 approved v5 scenes, with the same design system and gates. Validated by rebuilding all 16 approved scenes from briefs. The 24 live images are untouched (byte-identical rebuild). Contact sheets per page are reviewed before Divit's go.
- **Claude Code permissions:** every Webflow MCP call prompts Divit (explicit ask rule, holds in auto mode); file edits auto-approved; force-push, hard reset and reading `private/` denied. Never answer a Webflow prompt with "don't ask again".
- **Runtime: Claude Code** (Divit), for scale only. The content standard does not change: every page human, operator grade, world class, exactly per this log and `rules/HUB_RULES.md`. It must never read as AI-written: enforced by `rules/ai_tells.json` in QC (A1 block, A2/A3/A4 flag) and the reviewer's human-voice check (HUB_RULES 2b).
- **Target 200 pages a day with no loss of quality.** Content-first staged pipeline: writers (copy + image brief) → independent reviewer per page → images rendered in bulk from briefs via the recipe library → Divit's review (first batch per hub in full, then a daily random 10% plus everything flagged) → bulk drafts (100 per call) → bulk publish on his go. Defects become rules and re-run on every unpublished page. Recommended runtime: Claude Code (orchestrator + per-page writer and reviewer subagents); Claude.ai Project chats remain a supported mode. See `RUNBOOK.md` section 2.
- **Parallel setup is persistent.** Everything lives in this repo (runbook, rules, config, plan generator, status, logs) and in two skills; no chat holds state that is not committed.
- **Build order:** descending total volume (primary + secondaries), lowest-volume pages last. Wave 4 quiz pages (need a playable quiz) at the end.
- **The 4 existing child pages stay as they are** (thank-you-page, creator-application, approval-workflow, customer-satisfaction): primaries, slugs and content unchanged. The keyword plan was reconciled to them (`plan/overrides.json`): the CSAT cluster stays on `/customer-satisfaction`; `/approval-workflow` keeps "approval workflow" as primary; `/creator-application` stays live although the Semrush plan cut it.
- **FAQ schema on child templates: not needed.** Google shows no FAQ rich results; JS-built schema is unseen by most AI crawlers.
- **Carousels stay hidden** until there are child pages to show.
- **Meta title rule:** a keyword-led natural phrase ending " | Emergent", colon optional, 60 chars and about 580px max. No keyword lists ("Examples, Templates, Builder") and no slogans ("Confirm, Deliver, Convert").
- **Titles and H1s:** LP title "Free Thank You Page Templates and Examples | Emergent"; SQB title "Customer Satisfaction Survey: Free CSAT Template | Emergent"; SQB H1 "Build a Customer Satisfaction Survey That Acts on Every Low Score". Other H1s kept.
- **Hub profile locked:** see `rules/HUB_RULES.md` section 4.
- **Phase 1 fixes approved and applied** to the 4 child drafts (Shopify claim, "real examples" promise, vendor numbers in the Form FAQ, LP hub link, chip casing, SQB hero length, unconfirmed free-tier claim removed). Rollback in `childedits/2026-10-06/`.
- **Python automation pipelines (Sheets + Gemini + Drive + direct publish) are retired.** All CMS work goes through the Webflow connector with a review gate. Their hard-coded keys must be rotated.

## 2026-09-29 to 2026-10-05 (from the handoff and MORE_THINGS.md)
- No change to the live site without explicit approval; plan first; rollback always ready; touch nothing outside scope; never edit component definitions or existing classes; never make a site-wide style change.
- Copy is operator grade; never narrow the audience; write "Emergent's", never "our".
- Approved claims: SOC 2 Type I and ISO 27001; custom domains included in Emergent and use credits; conversational one-question flows; no task cap; no response caps. See `rules/claims.json`.
- Rolling vendor numbers: use wording that does not need monthly updates.
- Comparison tables put Emergent first, darker grey alternating column.
- Image standard: v5 design system, outlined SVG at the slot's exact aspect (use-case 3:2, object-fit fill), share images PNG 1200x630. No Anthropic API key in the image process.
- GitHub token is fine-grained to this repo only, expires 2026-12-28; never commit it.
