# Writer brief (adopted from account A's setup, Divit 2026-10-23 item 5)

READ FIRST (before any prose): rules/rework-checklist.md (clear EVERY line before finishing), DECISIONS.md entries for 2026-10-16, 2026-10-21 and 2026-10-23, docs/PREVENTION.md, rules/HUB_RULES.md.

TRUTH
- Every Emergent sentence maps to a claim id in claims_used.
- Every third-party, law, standard or software-category fact has a domain_sources quote span (6+ words), or it becomes plain advice.
- No flat yes or no about what a category of software or a law does without a span. No unsourced taxonomy ("N kinds"). Keep each source's own limits.
- No state-specific, legal, medical or financial advice. No compliance claims beyond SOC 2 Type I and ISO 27001. E-signatures: capture only. SCIM only as the named standard, never as an Emergent feature.
- Rename people and companies reused from other pages. Builder intent only; brand pages imply no partnership.

FINISH GATE (all required, in order)
1. `skeleton.py check URL all` = 0
2. `hubctl qc URL --stamp` TOTAL 0
3. `hubctl paa URL --spec`: 0 rejects AND 0 flags
4. `hubctl learn-check URL` ok
5. Hero prompt rule (QC L10) clean, and the prompt reads right (article, casing, a word that fits the business; never "signup" for a service call)
6. `hubctl verbatim URL` ok
7. `hubctl state URL qc_pass --by ID`, then `hubctl images URL --by ID`
8. READ the contact sheet: one hero, readable text, numbers add up across images and copy, images match the tab copy, and a person-addressed message is a card to that person, not a # channel. If not, fix the brief and re-render.
9. `ops/render_changed.py <sha> <sha> --pages <slug> --no-commit`
10. Commit your spec, your images and status/<hub>.json with `bash ops/sync.sh` (retry after a minute if it refuses)

REWORK: fix only the blocking findings and keep every other field byte-identical. Never run `hubctl ready`: a different agent slim-reviews the fix.
BLOCKER: if the page can't reach 10 gate-clean questions, or a source can't be found, stop and report the blocker in one line. If it can't be written as builder intent, park it.
RETURN in under 6 lines: final state, QC and gate, first-run P0/P1 per section, H1, flag count, anything for the coordinator. No Webflow calls.

SLUG: **PERMANENT SLUG RULE (Divit, 2026-10-23; final wording, supersedes every earlier slug note).** The target keyword is the one the page H1 is built around. The slug is that target keyword STANDALONE: no prefixes (custom, best, top, free, online, AI), no suffixes (generator, maker, builder, template, app, website, examples), singular not plural. Then remove ONLY the hub category word (LP "landing page"; Form "form"; Automation "automation"; SurveyQuiz "survey" and "quiz"). Lowercase and hyphenated, nothing else changed. Examples: "Build a Custom Thank You Page" -> thank-you-page; "Employment Verification Letter Generator" -> employment-verification-letter; "NDA Form Generator and Signing App" -> nda; "best startup landing pages" -> startup; "HIPAA Release Forms" -> hipaa-release; "Build a Church App" -> church; "Construction Inventory Management App" -> construction-inventory-management. Only exception: safety-quiz, team-quiz, wellness-quiz (collisions with live surveys). One slug function (ops/slugs.py) is used everywhere, and a mismatch BLOCKS create and ship. Check it with `hubctl slug-check URL`; a mismatch blocks qc_pass.
