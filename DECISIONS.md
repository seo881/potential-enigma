# Decisions log (Divit)

Every ruling Divit has made that a future chat must respect. Newest first. Add a line for every new decision, with the date and where it came from. Never re-ask something settled here.

## 2026-10-14
- **Ruling 21 (Divit, 2026-10-14): one consolidated template run, then one production publish.**
  - Every Designer or template fix in plan/backlog.md is done in this run, plus the carousel, Learn, console errors, hub FAQ clip, empty paragraphs, quiz embed (only if zero-footprint), OG image and JSON-LD.
  - Prepare everything first, then apply in one tight sequence: before-values committed, each write read back. Then ONE staging publish. Then the staging check, with screenshots to Divit. Then ONE production publish, then the live audit and verify-live.
  - Nothing half-done may sit staged.
  - Out of scope: shared-component duplicate IDs and the Adwire tag.
  - Plan: plan/template-run-2026-10-14.md.
- **Standing rule (Divit, 2026-10-14, after a teammate's site publish shipped everything staged): on this shared site, never leave anything staged that is not production-safe at that moment; a teammate publish can ship it any time.**
  - Every staged template change must be safe to go live as it stands; anything unverified stays out of the staged state entirely.
  - On 2026-10-14 the site was published at 08:11, 10:01 and 11:18 UTC; none of these was ours. The staged card links (404) and the Learn and carousel sections went live, giving 10 P0 and 8 new P1 console errors.
  - P0 order:
    1. Card links by `data_element_tool set_link` (linkType page, template page IDs), read back, with designer_tool confirmation; then a staging publish and a check of every carousel and Learn card href.
    2. If they are all right: production publish (Divit). If not: hide the SurveyQuiz Learn section (before-value committed) and publish to production.
    3. The quiz embed and the console-error fix ship only once each is verified safe on staging; until then they stay out of the staged state.
    4. Hourly publish watch: any publish that is not ours runs the live audit at once and alerts Divit.
    5. Then the full live audit (125 pages and 4 hubs), and a verify-live upgrade that checks every internal href, template links included.
- **Ruling 20 (Divit, 2026-10-14): rebalance to B.** At the time of the ruling, A had used 65% of its weekly budget and B 12%.
  1. **B writes all 4 hubs, LP included.**
     - `.hub` is `B:LP,Form,Auto,SurveyQuiz` in B's clone and `A:none` in A's.
     - A's LP claims and reworks are released to B with a handover line.
  2. **B does every full and slim review** with B-r and B-s agents.
     - A reviewer never reviews a page any part of which it wrote. The writers and reviewers of each page are recorded, and hubctl refuses a match.
     - A spot-checks only if B's blocking rate goes over 20% on a day.
  3. **A keeps:**
     - Webflow and all shipping, through the API script;
     - tooling, rules and QC;
     - the quiz template;
     - all AlsoAsked and Semrush pulls, and re-ranks;
     - the advisor flag list and the daily report.
  4. **The overnight loop runs on B's account tonight.**
     - Script: ops/schedule/overnight_run_b.sh, for ~/emergent-hubs-a, with CLAUDE_CONFIG_DIR=~/.claude (preflight refuses any other config dir). Same reset-wait and caffeinate; STOP file ~/emergent-hubs-a/STOP; no Webflow tools.
     - plan/overnight-run-b.md: write all hubs from the top of the ranked queue, review every page with independent B-r agents, reworks first.
  5. A reports its weekly reset date and time, and what its remaining 35% must cover until then.
- **Quiz data carrier approved: `alpb---prompt` (Divit).**
  - The quiz data goes in its own script block with a unique id (window.awbQuiz), separate from the prompt and chip data; the hero prompt text renders unchanged.
  - Only quiz pages carry the block; non-quiz SurveyQuiz pages are untouched.
  - verify-live and QC parse the prompt field with the quiz block present and still check the hero prompt exactly.
  - A canary of 2 quiz pages runs on staging before any quiz page ships.
- **Ruling 19 (Divit, 2026-10-14 afternoon): every CMS item write goes through the direct API script in ops/ship.py.** This covers create, update, relink, swap fix and publish (`hubctl api-create | api-update | api-publish`, ops/webflow_api.py).
  - The Webflow connector is never used for CMS item writes again. It stays only for Designer-level reads and anything the API script must not do, such as collection schema fields and template embeds, staging only.
  - The token is in the macOS keychain (service `webflow`); never in the repo, reports or chat.
  - The 2-item canary runs on the next write and is measured end to end; after it, the script is used for everything.
  - Lesson: tooling that types payloads through a connector is a throughput bug; script it.
- **Settings (Divit):**
  - Divit applies the settings change himself: an "ask" rule for the three `--live` write commands in interactive sessions, and deny in the headless loop.
  - After 2 clean daytime script runs, A proposes letting the overnight loop ship, with automatic verify-live and automatic unpublish on any failure.
- **board-survey:** routed to B as a swap of the "form board survey" construction questions and the American Community Survey question.
- **New keywords (ruling 13 sheet, 44 non-thin rows):**
  - Approved: all except rows 5, 9, 12, 16, 32, 35 and 39.
  - † rows (under 10 without format variants) count only if they reach 10 without pdf or printable variants; template variants are fine.
  - Row 1 (friendship quiz) waits for the quiz template.
  - Pull, derive, re-rank and push. B writes the Form, Automation and SurveyQuiz rows; A writes the LP rows.
- **Next 2 hubs:** supply is the limit for 500.
  - Today A proposes 2 to 4 candidate hubs from Emergent's product, each with a Semrush-sized keyword pool (count of build-intent child keywords and total MSV) and what the template clone takes.
  - Divit picks 2. The clone runs in parallel with everything else, staging first, new classes only.
- **Flag checks:** with each review batch, the advisor-check list (page, Q number, flagged question) goes out straight away, not once in the morning.
  - A-coord note, not part of the ruling: the question text stays in .cache, linked from the report, because the repo is public.
- **Divit, day 10-14 standing instruction:** push supply and throughput by every lever that does not lower quality, without asking. Ask only for:
  - a change to the quality bar;
  - spend past the 25% line;
  - a production site publish;
  - anything that touches live pages beyond item publishes.
- **The day's steps:**
  1. Ship the 64 approved pages by item publish, verify-live and relink.
  2. Route the ruling-18 swap pages in Form, Automation and SurveyQuiz to B as rework with the exact Q numbers; restore `.hub` to `A:LP`; B starts.
  3. Pull the 11 Automation no-pull pages through AlsoAsked (cap 2 each), derive and re-rank.
  4. Show the new-keyword rows; approved rows get pulls and enter the queue at once.
  5. Build the playable-quiz template today, staging first:
     - JSON quiz CMS field(s) and a self-contained accessible embed, new classes only;
     - skeleton, pack and QC for the quiz JSON, with golden cases;
     - a canary of 2 quiz pages;
     - then one staging-publish request covering the quiz template, the hub FAQ fix and the 12 card links (after Divit's Designer clicks), with the checks.
     - Production only on Divit's go. Until the template is live, quiz pages can be written and reviewed but not shipped.
  6. Loop logic: whenever pages become writable, A writes LP and B writes Form, Automation and SurveyQuiz (including quizzes after the canary); re-rank after every change.
- **Ship speed (Divit):** finish the 64 with the connector, with remaining creates in parallel agents. From the next batch, CMS writes go through a direct Data API v2 script with:
  - an allowlist: the 4 child collections; create, update, read and publish of items only; site publish refused in code;
  - before-values committed and pushed before every write;
  - read-back and a diff against the spec after;
  - batches of up to 100, backoff, and idempotent re-runs;
  - golden tests with a dry run;
  - a 2-item canary first.
  - Built as `hubctl api-*`, commit bb51f037.
- **Ruling 18 (Divit, 2026-10-14): flags are judged per page on the questions actually in the FAQ, not by subtype.** The subtype packet is retired; no subtype is approved or rejected as a whole (`ops/flag_packet.py` stays only as a counter).
  1. **Ship now** (with the 36 clean pages of the day's step 1): these flagged pages are approved as written, and every listed page ships with 0 gate rejects:
     - LP: nonprofit-landing-page, product-landing-page, saas-landing-page, sales-funnel-landing-page, squeeze-page, waitlist-landing-page.
     - Form: home-care-intake-form, independent-contractor-agreement, medical-history-form, model-release-form, nda-form, new-employee-form, permanent-makeup-consent-form, quote-form, referral-form, restaurant-reservation-form, tenant-screening-form, volunteer-form, wedding-photography-contract.
     - Automation: audit-workflow, automated-loan-processing-system, content-approval-workflow, document-approval-workflow, shipping-automation.
     - SurveyQuiz: customer-experience-survey, needs-assessment-survey, post-event-survey, volunteer-survey.
     - That is 28 names; volunteer-form and volunteer-survey are separate pages.
  2. **invoice-approval-workflow:** FAQ 10 "cfos" becomes "CFOs" (casing only), then a slim review, then it ships.
  3. **Question swaps:** one rework per page, with the replacement taken from the page's passing set. A page that cannot reach 10 is re-parked with its draft kept. Each swapped page ships the same day after its slim review.
     - address-verification-form Q10 (USPS, navigational)
     - church-membership-form Q8 (a letter, not the form)
     - contact-form Q5 ("form of contact", wrong sense)
     - grievance-form Q6 and Q7 (duplicates of Q8); Q10 (legal remedy)
     - identity-verification-form Q7 (gate reject); Q8 (land title, off-intent)
     - multi-step-form Q3 (spelling trivia)
     - petition-form Q10 (duplicate of Q9)
     - proposal-form Q5, Q6, Q7 (insurance sense; the page is business proposals)
     - requisition-form Q3 (medical lab sense)
     - vendor-application Q9 (state-specific, navigational); Q10 (gate reject)
     - customer-service-automation Q7 (gate reject)
     - proposal-automation Q9 and Q10 (duplicates of Q6)
     - returns-automation Q7 (duplicate of Q6)
     - community-survey Q1, Q3, Q5, Q6 (American Community Survey, a named program)
     - compensation-survey Q10 (invites vendor names)
     - mental-health-survey Q5 (gate reject); Q6 (named program); Q7 and Q8 (research findings, off-intent)
     - parent-survey Q7 (self-judgement); Q9 (translation trivia)
     - safety-survey Q10 (firefighter procedure, off-intent)
     - school-climate-survey Q10 (citation trivia)
  4. **Prevention** (code with golden cases; applies to new writing only):
     - Near-duplicates: same-intent variants count as one question (fill / complete / fill out / write / draw up; shorten / speed up).
     - Sense check against the page's H1 and primary keyword (insurance vs business proposal; medical vs purchase requisition).
     - Named program, agency or state check (American Community Survey, USPS, WHO surveys, state abbreviations).
     - Trivia filter: the spelling of the term, a translation, a citation.
     - Acronym casing in keyword-sourced rewrites (CFOs, KYC).
  5. **Skeletons may include flagged questions,** except the shapes code now drops: fragment or name, self-quiz, navigational ("where is", "where to find"), and platform- or state-specific questions.
     - Every day, the 10:00 report lists every flagged question in each newly reviewed page's FAQ (page, Q number, text), for the advisor's per-page check and Divit's confirm. That list stays in .cache, linked from the report: the repo is public and the question text is AlsoAsked or Semrush data.
     - Re-rank the queue under this rule now, and report how many non-quiz pages become writable.
  6. **`.hub`:** restore `A:LP` (from .cache/hub.before) and push before B claims. B restarts now on Form, Automation and SurveyQuiz.
  - **Report:** the live count after the first publish, then the 18:00 daily line.
- **Divit, night of 10-13/14 (final for the night):**
  - **Canary bar:** 3 non-quiz pages written fully on the new pipeline, any hubs (different hubs not required). The third round-2 page is the next writable LP or Automation page, with no wait for Form.
  - **Quiz pages stay last** (they need a playable quiz).
  - **C2 approved:** flag compliance claims only, i.e. HIPAA/SOC 2/GDPR (and PCI, CCPA, FERPA, SOX) followed by compliant, compliance, certified, certification or ready; never the bare word. In rules/capabilities.json pending `compliance`, with golden cases c2-*.
  - **hipaa-release-form stays parked.**
  - **Next steps:** when 3 of 3 pass, A removes STOP, starts the overnight loop, confirms the first iteration ran cleanly, and this session then runs only fetch, discovery, packet and audit. A failed round means: fix the cause and re-canary until 06:00 IST. Never wait on Divit tonight; anything needing his call goes in the 10:00 report.

## 2026-10-13
- **Ruling 17 (Divit, 2026-10-13): overnight, A alone (B stopped).**
  - After the canary passes, scaling runs headless so it survives session limits: `ops/schedule/overnight_run.sh`, copied from weekend_run.sh.
  - The script runs with this session's own config dir. That is `~/.claude-b`: account A's sessions in ~/emergent-hubs run there, while ~/.claude holds the ~/emergent-hubs-a (B) sessions.
  - Prompt "Continue the overnight run per plan/overnight-run.md". Same reset-wait, 7-hour give-up and weekly-stop logic; caffeinate, STOP file, no Webflow tools.
  - `plan/overnight-run.md`:
    - up to 10 A-w writers on the new pipeline (ruling 15), all 4 hubs tonight (a temporary .hub override, recorded);
    - claims only through hubctl claim, from the top of the ranked queue; never touch B-held pages;
    - order: A's 10 LP reworks first, then the tranche-1 pages that reach 10, then any page that becomes writable as Semrush results and the packet land;
    - every page is reviewed by an A-r agent that did not write it.
  - Nothing ships overnight.
- **Ruling 16 (Divit, 2026-10-13): daily cadence from 10-14.**
  - Standing go for item publishes (never a site publish) of every page that is reviewed, hash-matching, at 0 rejects, with pre-flight passing. Flagged pages wait for Divit's packet tick.
  - verify-live after each batch; a failing page is unpublished at once.
  - Day: 10:00 report + packet; Divit's answers by 12:00; 14:00 create items; 16:00 publish, verify, audit, relink; 18:00 daily line.
- **Ruling 15 (Divit, 2026-10-13): constrained writing.** New writing only; no recheck or ratchet of pages already reviewed.
  1. Prevention map (time-box 45 min): mine every review finding and rework note to date (status notes, reports, CONTENT_DEFECTS.md, SEVERITY, live audits). Each class gets a code check or autofix in the writer loop, or a precise page-pack instruction with a good and a bad example. `docs/PREVENTION.md`.
  2. Code builds the skeleton before a writer starts:
     - the 10 FAQ questions from the passing set (verbatim, US-normalised, locked; keyword-sourced ones in their filtered form);
     - secondaries in FAQ slots, hub and related links;
     - the hero default prompt from the primary keyword;
     - the comparison table;
     - a claims menu with IDs from claims.json and capabilities.json.
  3. Writers write prose only, section by section, with QC on each section as it is written. Claim IDs and quoted source spans are required, and deterministic rules are autofixed by code. One compact page pack per page. page-writer and page-reviewer are updated (the reviewer judges truth, intent and quality), with golden cases.
  4. Canary: 3 writable pages from different hubs, written by A-w agents and fully reviewed by A-r agents that did not write them. Pass = QC 0 on the first run and 0 blocking. Fix the causes and re-canary until 3 of 3 pass; no scaling before that.
- **Ruling 13 (Divit, 2026-10-13): new keywords to close the gap to 500.**
  - Semrush discovery with seeds per hub from head terms and from live and queued page patterns. Target about 250 candidates not already planned, cut, merged or live.
  - Screen each: clear build intent for the hub (SERP check), no cannibalisation (K-sibling), on-brand, and FAQ supply that projects to 10 with 0 rejects (flags allowed).
  - Spend under the 25% line, cached, never repeated. Semrush data stays in private/ and .cache.
  - One sheet to Divit by 10-14 18:00 IST, ranked by MSV; his yes/no per row by 10-15.
  - Approved rows enter the plan, ranked into plan/queue-ranked.txt. Parked pages are interleaved with queued pages by feasibility and MSV.
- **Semrush phrase_questions as a keyword-sourced FAQ source (Divit, 2026-10-13; pilot first, under ruling 13's Semrush budget).** Filter in code (`ops/semrush_questions.py`): keep only questions that contain the page's full head phrase or an approved multi-word variant, contiguous and in order; drop political, personal-finance advice, salary, best/top-N listicle and competitor-brand questions; 0 gate rejects; dedupe against existing candidates. Keyword-sourced, so a natural-question reword is allowed only if the head phrase stays (backlog line 91). Provenance records the source keyword and its volume. Feasibility counts them, and QC F2 accepts them only from the page's derived list. Pilot: the 10 short pages, head phrase + top 2 secondaries, display_limit 30, at most 35 calls. If 6 or more of 10 reach 10, propose running it on every short queued and parked page, with the unit cost.
- **Semrush budget (Divit, 2026-10-13):** spend what the work needs, carefully.
  - Read the API unit balance before the first call (free endpoint; the key is in the macOS keychain, service semrush, never in the repo).
  - Cache every response in private/ and never repeat a call for the same phrase and database.
  - Use the smallest display_limit that works (30 first).
  - Pilot cap: 35 calls.
  - After the pilot, scale to all short queued and parked pages without asking while total spend stays under 25% of the balance read; past that, stop and ask.
  - Report units per page and the running total in the 10:00 report.
  - Balance read 2026-10-13 17:32 UTC: 7,293,510 units.
- **Ruling 14 (Divit, 2026-10-13): spelling variants.** "acknowledgement" is a spelling variant of "acknowledgment" for PA3 matching. The display text of any verbatim AlsoAsked question is normalised to US spelling, with the original kept in provenance (same as the 2026-10-09 T-shirt ruling). This is a spelling normalisation, not a reword; ruling 4 still forbids rewording a verbatim question.
  - One general variant list, `rules/us_spelling.json` (`map`), feeds everything through `qc/spelling.py`: H2 blocks the UK form in copy, PA3 (`paa_gate.norm`) and the K keyword checks (`qc_hub.kwmap`) read it as the US form, and `hubctl verbatim` accepts exactly the original or its US-spelling/house-form display.
  - Golden cases r14-*.
- **Claims (Divit, 2026-10-13):** `hubctl claim` takes syn-pending rows of plan/queue-ranked.txt (split writes), and `hubctl state … claimed` refuses a queued page. Metrics count a logged run once (0-token rows and duplicate "corrects" rows dropped; sales-workflow's writer run counted once).
- **Staging, batch 3 (Divit, 2026-10-13 amendment):** if every check passes (batch 3, Learn on 4 templates, carousel on 4 templates and 4 hubs), leave the sections visible and ask for both goes (batch 3 production; Learn + carousel production). If any check fails, or only the batch 3 go is given, re-hide all 11 at once, read back, and Divit publishes with them hidden.
- **Ruling 12 (Divit, 2026-10-13): PA3 synonyms per page and replacement keywords approved, with zero quality change.**
  1. **AlsoAsked:** A runs every pull; B never pulls and uses saved pulls only (0 credits). `weekend.py aa` refuses outside Account A. Tonight: every queued page with no pull (cap 2 per page, stop at 400 credits in total: run `wave-r12`, `ops/pull_wave.py`), then a --kw pull on the top secondary of each LP page whose pull returned no_results and that is under 10.
  2. **PA3 synonyms, per page, Divit's read:** candidate sheets in tranches of 50 pages in queue-rank order (`ops/synonyms.py sheet N`, `.cache/review/pa3-tranche-N.md` and `.csv`; AlsoAsked text never in git). Per page the top 2 phrases, and under each EVERY question it admits, so Divit can strike single questions as well as whole phrases. Tranche 1 = the pilot pages; the next tranches follow as pulls land, with every queued page covered by 10-16.
     - Approved phrases go into `rules/paa_synonyms.json` at once (per-page data, outside the Monday window).
     - Struck questions go on that page's PA4 skip list (`rules/paa_blocklist.json`, stored as a question hash) with a golden case (`gate-pull-skip`).
     - Every admitted question still passes every other gate rule; a reviewer treats a drifting admitted question as blocking.
  3. **Replacement keywords:** the workbook's AMBER (116) and new-idea (29) rows, each screened for intent and for cannibalisation against existing and queued pages (K-sibling). Rows that fail or cannot be confirmed are dropped, not sent. The rest go to Divit as one sheet ranked by MSV for a yes/no per row by 10-15; approved rows enter the plan with the same pull and feasibility steps.
  4. **Queue:** `plan/queue-ranked.txt` (feasibility, then MSV; `ops/queue_rank.py`), regenerated after every pull wave and every synonym approval. B claims from the top only (`hubctl claim` reads it). Any parked Form/Auto/SurveyQuiz page whose feasibility reaches 10 is released to B (`queue_rank.py --release-parked`). The ruling 10 pilot hold on Auto is lifted: the pilot has landed, and Auto pages are claimed from the ranked queue like the others.
  5. **Split write (B):** a page pending synonym approval (class syn-pending) gets everything but the FAQ written first (`faq_pending` on its status entry). QC, the gate and the one review run on the whole page only after the FAQ lands; hubctl refuses qc_pass, images and reviewed until then. A page whose synonyms Divit rejects goes back to the queue end, its draft kept.
  6. **Capacity:** B measured about 7% of its weekly cap on about 5.6M tokens; plan for 50 pages a day.
  7. **Today:** full review of wellness-survey, sales-workflow and assessment-form; slim review of B's reworked pages (hash check, and a verbatim check on every restored AlsoAsked question: `hubctl verbatim`). Batch 3 staging flow as soon as Divit says "staging published".
- **Ruling 10 (Divit, 2026-10-13): AlsoAsked yield pilot plus 5 speed changes; the quality bar is unchanged (same gates, one review, one rework, same packet).**
  - **A. Yield pilot:** at most 45 credits, all through weekend.py aa, cap 2 per page.
    - The next 5 queued pages per hub in plan order, one pull each, plus the --kw secondary pull for sales-workflow, shipping-automation and automated-loan-processing-system.
    - Per page: the yield and the feasibility count. Per hub: the yield rate and projected supply.
    - PA3 synonym candidates are proposed only, never applied without Divit's go (DECISIONS 2026-10-08).
    - No more Auto pages go to B until the pilot lands.
  - **B1. Feasibility before writing:** code counts gate-passing pull items plus brief sources after the page's one pull. Keyword-sourced rejects count as recoverable when the source keyword contains the head phrase (backlog line 91). Under 10: no writer is spawned, and the page goes to the end of the queue (not parked). Refused at claim and in weekend.py next.
  - **B2. Review lock:** after review, hubctl refuses changes to any field not named in a blocking finding (mechanical H3/J1 autofixes exempt), at ready and in sync.sh's pre-commit check.
  - **B3. Weekly rule window:** new rules go to plan/backlog.md and land once a week, on Mondays, in one combined pass plus recheck. Factual errors are still fixed on the page the same day, and blocking review findings still block.
  - **B4. Daily ship:** each day's batch is every page that is reviewed, not held and text-hash matching. Same staging flow, one daily packet, one production go from Divit per day. Batch 4 starts on 2026-10-14 from the reviewed Form pool, plus ach-form and photo-release-form.
  - **B5. Around the clock:** B may run a headless writer loop in its own clone (no Webflow, only its paths; Divit starts it), with 6–8 writer subagents per account. The loop preflights at start (AlsoAsked key exported, Bash and hubctl reachable from subagents, render status readable) and refuses to run otherwise.
  - **Read-only checks:** read-only qc and paa never write qc_passed stamps or audit/paa/summary.md.
- **Ruling 9 (Divit, 2026-10-13): SurveyQuiz writing moves to B.** A keeps LP writing, every review (full and slim, B's SurveyQuiz pages included), all Webflow, rules and tooling, and shipping. B writes Form, Auto and SurveyQuiz. `.hub`: `A:LP` and `B:Form,Auto,SurveyQuiz`. The 4 batch-3 SurveyQuiz pages stay A-coord held and ship with A.
- **Naming (Divit, 2026-10-13, ruling 0):**
  - **Account A = the coordinator** (`~/emergent-hubs`): LP and SurveyQuiz writing, every review, the only Webflow writer, rules and tooling, shipping.
  - **Account B = the writer** (`~/emergent-hubs-a`): Form and Automation.
  - Agent ids: coordinator `A-`, writer `B-`. `.hub` = `A:LP,SurveyQuiz` / `B:Form,Auto`. Holds and ownership map by clone.
  - Mapping note: between about 08:00 and 11:30 UTC on 2026-10-13 the letters were reversed. In history, `A-w-*`, `writer-a-*` and `proposals/account-a.md` were the writer; `B-w-b3-*` and `B-coord` were the coordinator. Those ids stay as written.
- **500 pages live by 2026-10-27 with two Claude Code accounts (Divit, 2026-10-13):**
  - The writer (B) does rework first, then queued pages, then parked pages A releases for rescue.
  - B never edits rules/, qc/, ops/, templates or DECISIONS.md; it proposes in proposals/account-b.md.
  - Protocol: docs/TWO_ACCOUNTS.md.
- **Review rule (Divit, 2026-10-13, ruling 1):** a page ships only if its current text was reviewed.
  - A hash of the reviewable text fields is stored at review time.
  - Text changed after review, beyond mechanical autofixes (H3 commas, J1), needs a slim review of the changed fields by an A reviewer who did not write them.
  - `hubctl ship` refuses a page whose hash does not match.
- **Reviews on 2026-10-13 (ruling 2):**
  - slim review of batch 3 (all 20) and of the writer's 36 reviewed pages;
  - full first review of the writer's 11 pages at `images`.
  - Blocking findings get one rework; Form/Auto pages go back to B.
- **Batch 3 (ruling 3):** after review, CMS items with the L12 Learn refs, verify 20/20, isDraft false. Then the staging flow, then ask Divit for the production go.
- **Gate (ruling 4):** pass = 0 rejects.
  - Flags are allowed only when every flagged question is in Divit's daily packet.
  - A verbatim AlsoAsked question is never reworded to clear a flag; fix the PA6 patterns instead (golden cases from photo-release-form, ach-form).
- **PA12 (ruling 5):** a page with no Semrush secondaries uses the workbook's keyword ideas for the page as its secondaries (at least 4, on-topic), not min(6, 0). Golden cases: brand-questionnaire, shipping-address-form.
- **Collisions (ruling 6):** batch files take only pages in state `reviewed`, and nothing is claimed or batched over a hold. `--by` on every claim and state change, and a hold marker on origin before anyone works a page it did not just claim.
- **Learn refs (ruling 7):** keep the current 3. Tie-break for the 3 newest published: newest learn---publishing-date, then newest createdOn (L12).
- **Rule re-run (ruling 8):** run it now only on pages B does not hold; run it on B's pages at the end of B's wave, coordinated through holds. Never change a held page's state.
- **Learn section design (Divit, 2026-10-13):**
  - The Learn list's source stays on the item's own "... - Learn" multi-reference field; never change it.
  - blog_link is a collection-page link to detail_learn on all 4 templates.
  - Each child item's acrm---learn holds the 3 newest published Learn articles, set at creation (L12, config/learn_refs.json).
  - The 39 live items were filled field-only on 2026-10-13; the refs ship with the next site publish.
- **Unhide for staging, one condition (Divit, 2026-10-13):** unhide, publish STAGING ONLY, run the checks, then re-hide immediately whether or not they pass, and read back the hide before anything else happens. No production publish while anything is unhidden.
- **Writer proposals F2 and read access, fixed by A (Divit, 2026-10-13):**
  - F2: legacy-capture pages accept the source "alsoasked" when the page has a pull.
  - `hubctl brief` prints the gated AlsoAsked candidates, so writers never read private/.

## 2026-10-12
- **Stock placeholder names are an AI tell (Divit, 2026-10-12: "Add these names to the AI-tell list with golden cases"):** Northwind, Globex, Initech, Acme, Contoso, Fabrikam, Wayne Enterprises, Umbrella Corp(oration) block (QC A1, P1), whole words, case-insensitive, in every copy field, chip_adds, image alt text and every string of the image brief (rules/ai_tells.json `stock_names`; golden stock-name-*). Unpublished specs that carry them fail QC and go to rework through the ratchet.
- **K7 matches multi-word brands (Divit, 2026-10-12: "K7 matcher multi-word brands: yes, with a golden case"):** a column header ranks when one top-10 URL has the brand's first word as a host label and its other distinctive words in the host or path ("Adobe Acrobat" = adobe.com/acrobat/..., "Google Forms" = docs.google.com/forms/); single-word brands match as before; the same domain with a different product still raises K7 (qc/qc_hub.py `k7_ranks`; golden k7-*).
- **PA14 acronym exemption (Divit, 2026-10-12: "PA14 acronym exemption (AP, OCR): yes, with golden cases"):** an unlisted capitalised token is not flagged when it is a word of the page's primary or an approved secondary, or the initials of a 2-3 word run in them (AP = accounts payable), or in `pa14_domain_ok` (AP, AR, OCR, ACH, COBRA, PO, GL, ERP, CRM, HR, W-9, I-9), or part of a US state name (`pa14_us_states`; backlog line 92). Listed brands still reject, unlisted brands still flag (rules/paa_blocklist.json; golden pa14-*).
- **A6 defaults (Divit, 2026-10-12: "A6 defaults: yes to all"):** 3 reconciliation rows in private/alsoasked/credits.log for the billed-but-unlogged connection-reset pulls (audition-form, corporate-resolution-form, copyright-release-form, 1 credit each); the credit-capped written pages stay parked; the never-written Form pages parked only for the retired F4 go back to the queue (`hubctl release --note`, which now accepts a parked page only with a note); hipaa-release-form stays parked.
- **video-landing-page keeps Landingi (Divit, 2026-10-12):** Landingi stays the third comparison column, with its K7 P2 (only two real builders rank for the query; `hubctl table` needs 3).
- **Procurement and incident table variants approved (Divit, 2026-10-12):** procurement-automation and incident-response-automation get their own Automation library variants instead of the hub-default Emergent column; regenerate their tables.
- **A8 waits for Divit (2026-10-12):** the duplicate form-ID fix (docs/A8_DUPLICATE_IDS.md) waits until Divit has checked GTM for triggers on `email-form`; nothing changes before then.
- **A6, Form parked pages (Divit, 2026-10-12):** the 7 intent-mismatch pages leave the queue as proposed in reports/2026-10-08/2121-deterministic-pass.md (plan/overrides.json `intent_merges`, `intent_drops`): expense-request-form, mileage-reimbursement-form, travel-reimbursement-form and travel-request-form merge into expense-report-form; car-rental-form into rental-agreement-form; health-screening-form into medical-history-form (where the report said "merge or drop", the merge was taken); vehicle-inspection-form is dropped. The 12 SAFE PA3 synonyms of the 2026-10-08 rescue analysis are approved (rules/paa_synonyms.json). The other parked pages get one AlsoAsked pull on their top secondary (`weekend.py aa <url> --kw secondary`, at most 2 credits per page in total, 250 for the run); pages with 8 or more on-topic sources go back to rework.

## 2026-10-12
- **Carousel back on (Divit, MONDAY A4):** section_build visible again on the 4 child templates and the 4 hubs (staged 2026-10-12, logs/templates.md); it goes live with Divit's next site publish, after the staging check (covers, alt, live pages only, 390 px). Supersedes the 2026-10-09 "carousel hidden" line.
- **429 from a social domain is OK (Divit, MONDAY A1):** instagram, x/twitter, linkedin, facebook, youtube, tiktok (rules/live_audit.json social_ok; golden audit-link-*).
- **Template fixes (MONDAY A3):** FAQ heading from the item (window.awbFAQ.heading) via a new embed; JSON-LD fields kept free of characters Webflow HTML-escapes (QC J1, P1); comparison table at 390 px gets a sticky label column (it already scrolled).

## 2026-10-10
- **DataForSEO is retired (Divit, 2026-10-10).** AlsoAsked replaces it for People Also Ask; no live SERP pull is required. QC F1 passes with an AlsoAsked pull (`private/alsoasked/<slug>.json`); top-10 and intent context come from the Semrush workbook and the Wave 3 SERP data in `private/`; keyword ideas come from the Semrush workbook. `mcp__dataforseo` removed from `.claude/settings.json`. Legacy DataForSEO captures stay as F2 checks on pages written before this date.
- Live-audit proposals (reports/2026-10-10/0120-part3-live.md), all approved:
  - Google Forms "How you build" becomes "Editor, with Gemini drafting on some Workspace plans", if Google's docs confirm it. Confirmed: support.google.com/docs/answer/16346789 and Workspace Updates 2025-06-11. All form tables regenerated.
  - 404-page feature_1 uses the safe wording: "Your prompt asks for the designed page on every unknown URL; check its status code with your host before launch."
  - New LP library variant `utility`, with the build cell "Prompt for the page and the rules behind it" (used on 404-page).
  - Explore CTA: at most 34 characters (QC D3, P1). client-onboarding-questionnaire gets "Build My Onboarding Questionnaire".
  - 404-page meta description: "does not exist" as a quick fix; the template JSON-LD escaping goes to the MONDAY backlog, along with the template P2s.
  - Fix the H3 serial-comma detector, then sweep the 20 live pages (item publish only).
- Process: before-values are committed and pushed BEFORE any Webflow write; `live-fix prepare` refuses otherwise.

## 2026-10-10
- **NO SITE PUBLISH, EVER (Divit, 2026-10-10).** Claude (Claude Code, headless jobs, subagents and the advisor chat) never publishes the site or any domain: no publish_site call, no "publish to selected domains", not to staging, not to production, not as a fix or a rollback. CMS changes go live only as item publishes (publish_collection_items) of the specific items changed. Template, page, component or style changes are staged only; Divit alone publishes the site, deliberately, from the Designer. The Webflow sites tool is denied in .claude/settings.json; any script or prompt that would publish the site must refuse and report.

## 2026-10-09
- **FAQ moat lines, batch 2 onward (Divit, 2026-10-09):** "In 2-3 of the general FAQ answers per page (not the definition or the item-2 how-to), add one subtle, natural line on what Emergent does better for that exact question: its question-specific moat, e.g. no response caps, a database you own, code export, no per-seat pricing, built from a prompt. One sentence at most, claims only from rules/claims.json, no hard sell, never in branded or competitor-comparison phrasing." QC F9 (P1) for pages not yet in Webflow; the 20 live pages get theirs at next rework.
- **Two production publishes outside the plan (2026-10-09, 11:38 and 13:14 UTC)** shipped unverified content; the daily live audit now runs at once whenever the site's lastPublished has changed since its last run.
- **Launch-blocker rules (Divit, 2026-10-09; override the rules freeze):** FAQ questions contain no brand or product names (gate PA14, PA8 brand cap 0) and no file formats or download asks (PA15); hero description at most 130 characters with the primary keyword, leading with what the visitor gets, plain words (QC D1, P0); how-to description one sentence of at most 140 characters with the primary keyword saying what the steps achieve (QC D2, P0). Details: rules/HUB_RULES.md section 5.
- **Carousel hidden on hubs and child templates until its formatting is reworked (Divit); revisit Monday.**
- **Hero prompt (Divit, 2026-10-09):** one generic default with the primary keyword (no industries, names or scenarios) plus one short "Add ..." clause per chip; chips toggle their clause (several at once, chip order, typed text kept); selected chip black on white text via new names only (data-hubchip, hubchip--on); script in our own embed (ops/template/hero-chips.html), the older chip script blocked by a capture-phase handler, not edited.
- **Live audit with auto-fix (Divit, 2026-10-09):** after every publish and daily, every live child page and hub is audited character by character (docs/LIVE_AUDIT.md). Standing go for Claude to fix P0 and P1 issues on child CMS items itself (text, FAQ, meta, alt, CMS links, image fields), publishing that item only, each fix with a saved before-value, a ledger row and a rollback. Never automatic: slugs, primary keyword, deletions, templates, components, classes, sitewide elements, hub pages, or anything a person edited in Webflow (drift is reported, not overwritten).
- **Image formats (Divit, 2026-10-09):** use-case images and card covers stay SVG; the share image (Thumbnail Image / og:image) moves from PNG to **WebP** (1200x630, at most 300 KB), for all pages, current and future. AVIF is not used for og:image (previews fail on LinkedIn, Slack, iMessage, X, Discord). AVIF only for raster images visitors load, after an inventory and Divit's go. See LESSONS.md section 4.
- **LESSONS.md is the learning loop (2026-10-09):** every incident adds a log line and an automated check; read at session start.
- **Launch set = 20 (Divit, 2026-10-09): contact-form held.** Its FAQ has two drift questions ("What is a contact form owner?", "What does 'form of contact' mean?") and three Contact Form 7 (WordPress plugin) questions. Its CMS item 6ac8a2bff143d8ebe327735f stays a draft; rework it in a later batch.
- **PA13 fixes before publish (Divit, 2026-10-09):** employee-information-form Q4 (ADP fill-out question) replaced; employee-engagement-survey Q5 replaced (near-duplicate of Q4); t-shirt-order-form question display text normalised to "T-shirt" (original wording kept in provenance); feedback-form Q1 reads "What is a feedback form?".
- **Template launch steps (Divit, 2026-10-09):** T3 and T11 verified already done; T6 done (carousel visible on all 4 child templates, staged); T5 (cover alt) and T10 (default tab) are verified on staging, with a standing go to bind cover altText to the item Name field if staging shows it empty; T12 (Audits panel) is non-blocking, run after launch. Nothing for Divit in the Designer before publish.
- **Publish order (Divit, 2026-10-09):** staging (webflow.io) first, verify_launch must pass, then emergent.sh.
- **F4 retired: superseded by the PAA gate; conflicting rules, allowed under the freeze (Divit).** QC F4 (answer the first 10 eligible DataForSEO PAA questions) conflicted with the approved PAA gate PA1-PA13 on 6 batch-1 pages; its code stays in `qc/qc_hub.py`, disabled (`F4_RETIRED`), and it no longer counts toward the QC TOTAL.
- **Launch today = 21 pages (Divit):** the 15 batch-1 pages already reviewed plus the 6 that F4 held (ecommerce-automation, contact-form, 404-page, pricing-page, employee-engagement-survey, booking-form). Held and untouched: consultation-form, checkout-form, conference-registration-form, summer-camp-registration-form and the 4 originals (they stay drafts); links to them ship as plain text. Batches 2 and 3 wait.

## 2026-10-08
- **LAUNCH RUN (Divit, 2026-10-08):**
  - **Rules freeze for launch:** no new QC rule or rule change until batches 1-3 are live. New feedback goes to `plan/backlog.md`; only factual errors on a page are fixed immediately.
  - **Review = batch review** (4 pages per agent) on every non-parked page (option (c) of `plan/rework-2026-10-08.md`); per-page cost is measured on batch 1 and logged. This review replaces any earlier review on the page (earlier reviews are archived in `spec.reviews`).
  - **PA13 skim and the PA3 newly-passing read are ONE file per batch** for Divit: `.cache/review/batch-N.html`.
  - **Deferred until after launch:** the 12 synonym rescues and the 51 second-pull pages. The 7 intent-mismatch pages stay parked. `rules/audience.json` accepted as is.
  - **The 4 original child pages** (thank-you-page, creator-application, approval-workflow, customer-satisfaction) are brought to the same standard: slugs and primaries unchanged. This supersedes the 2026-10-06 "unchanged" line for their content.
  - **Standing go for STAGED Webflow writes only:** CMS items with `isDraft: true` and template edits T1, T2, T4 and T9 (`plan/template-edits-2026-10-08.md`). Nothing is published, and site publish is never triggered, without Divit's explicit "publish batch N".
- **The testimonials and stats in section_stats on the hub pages are real and accurate (Divit confirmed 2026-10-08); not placeholders, do not flag again.** Checked read-only on the live /ai-form-builder: stats 10M+ Active Builders Worldwide, 12M+ Apps Successfully Created, 200+ Countries Globally Reached; testimonials Alex Rivera (Founder, TaskFlow), Maya Chen (Product Lead, BrightSuite), Jordan Patel (Co-founder, LoopDesk).
- **Standing work report after every task** (Divit): `reports/YYYY-MM-DD/HHMM-<slug>.md` with Request (verbatim), Actions and results, Numbers, Decisions (with their source), Files and commits, Webflow calls (IDs, before/after, rollback), Not done, Open questions; a line in `reports/INDEX.md`; nothing secret or from `private/`/`.cache/`, no SERP or AlsoAsked question text (public repo); push via `ops/sync.sh`; chat reply under 15 lines (summary, path, SHA). Rule text: RUNBOOK section 6, CLAUDE.md.
- **Hub link and link-to-live** (Divit): every child page links directly to its hub page exactly once (FAQ item 2, QC K4, P0); 2-3 links to related child pages are welcome but only to pages live at publish time. Links to non-live pages ship as plain text and are re-linked when the target goes live.
- **The 4 hub pages are live** (Divit confirmed 2026-10-08).
- **Serial (Oxford) comma everywhere**, matching the live hubs (Divit).
- **Fixes run as ONE combined pass per page** (Divit): code applies deterministic fixes, one writer pass handles FAQ replacements and semantic flags, then one QC and one review.
- **PA3 widened** (Divit): a question is on-topic if it contains the head phrase exactly, the head phrase reordered or inflected, or an approved secondary of the page. Every question admitted only by the widening is exported for Divit's full read before any rework; any he rejects goes on that page's PA4 skip list with his reason. PA13 (Divit reads every page's 10 questions before publish) stays mandatory.
- Canary passed (Divit checked the registration-form draft in the Designer): repo -> CMS draft path validated.
- **AlsoAsked Phase 2 approved** (Divit): pull every written page, ceiling 200 credits, stop if a page costs over 2; PA3 synonyms proposed by code as candidates only, applied after Divit approves the batch. PA1 applies to PAA-sourced items only (definition and how-to slots and secondaries are exempt).
- **PAA rules PA1-PA13 approved as written** (Divit); thresholds tuned after the first full run. Gate built against a real AlsoAsked API pull (registration-form), not a UI export.
- **Production moves to the second (paid team) account as it is** (Divit): the first account is at about 80% of its weekly limit until Tuesday. Open decisions are taken up there. Full context: `docs/HANDOVER_2026-10-08.md`.
- **No new pages**; priority is QC and taking existing pages live; minimal token use (code QC with summaries only).
- **The post-75 pages of the overnight run were authorised by Divit directly in Claude Code** (not a scope breach).
- **DataForSEO PAA is no longer trusted as an FAQ source; Divit bought AlsoAsked.** In-depth PAA rules and QC must exist before any publish (proposal PA1-PA13 in the handover, pending approval).

## 2026-10-07
- **Final process (Divit, after the 8-page measurement run): stop the review loop.** Write in bulk, QC to zero, **one review** with a fixed severity table, **one rework**, then Divit reviews the previews.
  - Severity table `rules/SEVERITY.md`, the only severity source for the reviewer. Blocking: untrue or unsourced claims, wrong facts, structure, image contradicting copy, a sibling's keyword, missing intent. Everything else is a note that ships. Every finding names its class; `hubctl review` rejects a class whose severity disagrees with the table.
  - Template slots (hero pitch restated in FAQ 2) are not repeated ideas. Soft quantifiers are notes unless they state a fact about a named third party. Repeated ideas (#21) are notes. This supersedes the earlier rulings "repeated ideas become blocking" and the per-CONTENT_DEFECTS-row blocking rule.
  - Challenger pass retired: the agent file stays, but it is out of the pipeline and CLAUDE.md; `hubctl challenge` refuses. After the one rework, `hubctl ready <url>` moves a QC-clean, re-rendered page to `reviewed`. Divit approves from `reviewed` (legacy `challenged` pages too).
  - Image names block (Divit, follow-up): CONTENT_DEFECTS #23 (names borrowing third-party IP) and #29 (names mapping ethnicity, gender or age onto a negative outcome) are class `image-names`, blocking.
  - The five measurement-run pages left in rework (404-page, one-page-website, employment-verification-letter, customer-feedback-survey, employee-satisfaction-survey): the challenger's findings count as their one review; blocking items only (by SEVERITY.md), QC to zero, images, then Divit.
  - `hubctl export-csv <HUB>`: one row per page, every CMS field, image paths and alt text, `.cache/review/<hub>.csv`.
  - Tonight (no more cycles): one-sentence fixes applied to accounts-payable-automation, landing-page-seo, rental-agreement-form, invoice-automation, document-automation; image flags fixed on sales-automation (code cover -> action cover drawn as a DM to the named rep; engine `dm` option) and employee-engagement-survey (two hero cards filled, code cover -> score cover). All 8 at QC 0, re-rendered, previewed, exported.
- **Divit's decisions after cycle 5, and the efficiency target (under 350k tokens and 1.5 cycles per new page):**
  - AP variant pricing "Credits, free to start". One more blocking-only cycle for job-application-form and landing-page-seo. Survey and sales go to Divit's preview review; on his approval each becomes its hub's exemplar.
  - Every category variant defines every row it is used with (QC V4). Rows that were falling back (ap/sales ownership; hiring limits, data, ownership; seo seo, ownership, data, visitors; employee pricing, data, ownership) were copied verbatim from the hub defaults so no table changed; Divit to confirm or replace.
  - Approved checks and rows 27-31: source link check (hubctl sources-check, QC P3), hero balance gate (max 21%, calibrated on the 16 approved scenes), name patterns, reserved example domains in images (page specs only; the reference scenes that rebuild the live images are untouched), code cover only for codes. Repeated ideas (#21) are blocking; unsourced advice is blocking when it states a fact about the world, a note when it is a recommendation.
  - QC Q4 bug fix: a variant is required only when every competitor in the table shares that specialist category and no general tool category (form-builder etc.). Every Form-hub competitor is tagged hiring, so Q4 was forcing the hiring variant onto a rental agreement page.
  - Efficiency: rework fixes blocking findings only, notes never trigger edits; re-source only claims a blocking finding names; at most 8 sources per page (QC P4), search snippets preferred; agents read role packs (hubctl pack) instead of the full rulebook; batch review and challenge up to 4 pages per agent.
- **Defects are rule violations; plan before prose; sourced domain claims** (Divit, after cycle 2: every page at QC 0, fresh reviews 4-7/10):
  - Every reviewer and challenger finding names the rubric criterion, cites the HUB_RULES section or CONTENT_DEFECTS row it breaks, and is blocking or a note. hubctl rejects findings without a valid citation; only blocking findings send a page to rework; notes go to spec.review_notes, and a note that recurs on 3+ pages is proposed as a rule (hubctl metrics).
  - Writers write spec.plan first (angle vs the top 10, four tab stories, opener variety, heading shapes different from siblings, claims to source) and run hubctl plan-check; QC P1 blocks a spec without a plan.
  - Claims about third-party systems, legal or professional terms and best practice are verified with web search while writing and recorded in spec.domain_sources {claim, source_url, date}; QC P2 blocks an unsourced planned claim; reviewers check claims against them.
  - Confirmed: the narrowed PAA filter (e951a1c) stays. Sales pricing cell: "Credits; reps using the app are not billed as seats". Form table labels "Application limits" and "Where applications live" approved. QC C3 allows percentages that are thresholds or settings (after over, under, above, below, more than, less than, at least, up to, within; or before variance, tolerance, threshold, discount, off); outcome statistics still block. Catalogue rows 21-26 added.
  - Throughput: hubctl metrics reports first-pass yield, cycles per page, median minutes per stage and tokens per page (hubctl usage-log). Batch mode: one reviewer and one challenger may each take up to 4 pages, never their own. ops/worktrees.sh sets up one worktree per hub for four parallel sessions; ops/sync.sh rebases before every commit.
- **Dry-run fixes before any re-run** (Divit, after the first dry run: 0 of 5 pages through review and challenge; first reviews 3-7/10 against writers' 10/10 self-scores; rework kept recreating the same defect classes):
  - Whole-page craft checks in QC, every instance reported: "which/that is what" tails block, ", so" endings flag and block over 2 (Q5); any 6-word phrase in two fields, FAQ answers included, the page's own keywords excluded, blocks (Q6); over 3 "from X to Y" ranges block (Q7); over 8 "A, B, and C" lists flag (Q8).
  - Copy-to-image story links: every image_brief tab has `story` pairs; the engine checks both sides exist, numbers agree, every number in the tab copy is drawn and every rule drawn is linked (QC I4, docs/IMAGE_BRIEF.md).
  - Rework protocol: fix the defect class, not the instance; reviewers and challengers list every instance; every cycle uses a new reviewer (and challenger) that reads the page cold first, then verifies earlier fixes (hubctl refuses a repeat agent).
  - Writer self-scoring dropped as a gate. Writers run QC and read the hub exemplar: the first page per hub that is challenged and approved by Divit is written to `specs/<dir>/_exemplar.md` by `hubctl state <url> approved`.
  - K8: a secondary counts when all its words are in one sentence, any order (minimum 6, per the 10-item FAQ ruling); two secondaries in back-to-back sentences of one answer block.
  - Bugs: "US" (the country) is not the pronoun in the we/our check; quoted form-field labels are exempt. `serp-keywords` counts against the DataForSEO budget.
  - PAA relevance (QC F4), applying Divit's 10-on-topic-items ruling: a question that shares only a generic word with the page's keywords ("ai", "seo", "automation", "form", "survey"...) is drift and no longer required; it must share a specific word (plan/serp.py GENERIC). Skipped questions stay usable if they are on topic.
  - Library: the LP `seo` variant's build cell is "Prompt for the page and its on-page SEO" (no ranking promise). The six proposed catalogue rows are approved (rules/CONTENT_DEFECTS.md 12-17). Score-style covers may show a metric without stars.
- **FAQ back to exactly 10 items** (Divit): the dry run showed that filling 15 forced drifting PAA questions and stuffed keywords onto pages. Every item must be an on-topic question searchers ask; secondaries in the FAQ at least 6 (or all if fewer), read naturally. QC S5 and K8 updated. The hub link stays in item 2 with 2-3 related-page links.
- **Brockmann pins come from the CDN files** (Divit): Webflow's fileHash describes the originally uploaded file, not the one the CDN serves, so `config/typography.json` pins the md5 of the served files (verified with fontTools: family Brockmann, weights 400/500/600/700, 458 glyphs each, printable ASCII plus ’ “ ” – — × · → £ € covered). Brockmann has no backslash (U+005C); the live site already falls back for it. No new rule: `ops/typeset.py` missing_glyphs (QC T1, P0) already blocks text the heading font cannot draw.
- **Capability principle** (Divit): Emergent's agent builds whatever it is instructed to, so anything a built app does may be stated (payments out via bank file or payments API, W-9 collection and 1099-ready records, real-time dashboards, e-signature capture, native mobile). Still gated: guarantees about Emergent's own platform (compliance beyond SOC 2 Type I and ISO 27001, SSO/SAML, SLAs and uptime, encryption specifics) and claims that need evidence (accuracy numbers, legal validity). Dry run started.
- **All 16 safeguards built in one go** (Divit): capability ledger, facts ledger, approval fingerprint, slug check before create, file locks and per-page history, near-duplicate detection, SERP freshness, live verification, risk-based sampling, quality metrics with a reviewer-leniency alert, rules version and ratchet re-check, image regression, library look-ahead, DataForSEO budget, ranking feedback loop, internal link graph. Each tested on throwaway pages (RUNBOOK 3c). The capability ledger's pending items need Divit's ruling; the first run caught unapproved money-movement and tax claims in the AP sample.
- **Who reviews** (Divit asked): the reviewer is an independent Claude agent, not the writer and not a person; Divit is the only human gate. To remove single-agent judgment from the gate: (1) the two judgment calls became code: a declared image "fact" that other drawn numbers produce is blocked, and an H1 that leans on a sibling's topic is blocked (Q3 now P1); (2) writer, reviewer and challenger must be three different agents (hubctl and QC R1/R2 enforce it); (3) a second, adversarial pass (`page-challenger`) must find zero defects after the rubric passes. Images now render before review so both agents judge copy and images together. Order: qc_pass -> images -> reviewed -> challenged -> approved (Divit) -> cms_draft -> published.
- **Airtight pass before the dry run** (Divit): field limits now measured in rendered pixels in the template's real typography (Brockmann headings, Inter body, sizes from the Webflow variables), against the widest approved rendering of each field (QC T1, `config/typography.json`); meta descriptions within about 920px; rich-text HTML shape identical to the live pages (S9); every quantity in every image declared and true, shared values matched across images, glyph coverage checked (engine `checks`); deliberate-error tests block all six error types. A canary draft is checked in the real template before the other dry-run pages are created; approved renders widen the calibration (`hubctl verified`).
- **Quality bar made explicit and enforced** (Divit asked on what basis the first draft was not the best). The basis was five criteria (scope, openers, specificity, craft, image balance); they are now a 10-criterion rubric (`rules/rubric.json`), a defect catalogue (`rules/CONTENT_DEFECTS.md`), QC checks Q1-Q4, A1 additions and the engine balance gate (calibrated: approved scenes pool at most 16% empty space; the first sample's weak panels 17-25%). Proven: the first draft rebuilt as written is blocked on all five defects. The reviewer must record 10/10 (`hubctl review`, QC R1) before a page moves on; the writer self-scores before QC.
- **FAQ standard** (Divit): exactly 15 items; carry as many secondaries as possible (QC: at least 10 verbatim); links like the AI website and app builder pages, extended: the hub link in item 2 plus 2-3 links to related Emergent pages with exact-match anchors; never a link to a page that is not live (publish gate). Keyword ideas from DataForSEO fill any slots left after PAA and secondaries.
- **Images stay vector**: use-case images and covers are outlined SVG with motion (caret, pulse, press, ripple, scan, ring, glow, and now a gentle float on every hero); only the share image is PNG because social platforms reject SVG.
- **Sample page v2**: H1 "Build Accounts Payable Automation From Inbox to Paid"; tab 1 and feature 4 rewritten; AP-specific Emergent column in the table (library variant `ap`); 15 FAQs with 17/17 secondaries and 4 links; image balance fixed. Preview: https://claude.ai/artifact/JudvZGyAtTNuC2C7qcGt51
- **Comparison tables: vetted competitor library + per-page selection** (Divit). `rules/competitors/<dir>.json` per hub, seeded from the 4 approved tables (regenerated byte-identically) plus Tipalti, BILL and Stampli (sourced 2026-10-07). Tables are generated with `hubctl table`; QC V2 rejects hand edits, V3 expires facts (numeric 90 days, other 180).
- **Image style** (Divit and the Webflow developer): neutral grey canvas; the artifact carries colour, one accent per image, rotating across the four tabs so no page is only purple. Applied in the engine; image hold lifted. The 24 live images keep the old style until their re-render is approved.
- **PAA relevance filter:** deeper PAA expansions drift off topic (the AP SERP drifted into "jobs AI will replace"); only questions sharing the page's topic are required (QC F4).
- **Sample page** written end to end for Divit's review: /ai-automation-builder/accounts-payable-automation (QC 0, images rendered).
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
