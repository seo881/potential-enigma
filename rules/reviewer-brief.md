# Reviewer brief (Divit 2026-10-23 item 5)
- Check every line of rules/rework-checklist.md first.
- Run `hubctl verbatim URL` and `hubctl paa URL --spec` (0 rejects, 0 flags).
- Read the contact sheet.
- Severity comes from rules/SEVERITY.md only.
- Never edit the page. Never review a page you wrote any part of.
- No blocking finding: the page moves to reviewed; then run `hubctl ship-check URL`. Blocking finding: record it (the page goes to rework) and stop.
- Slim review (after a rework): `hubctl review-diff`, then `hubctl slim-review`, on the changed fields only.
- Commit your files plus status/<hub>.json with `bash ops/sync.sh`. No Webflow calls. Reply in under 6 lines.

SLUG: **PERMANENT SLUG RULE (Divit, 2026-10-23; final wording, supersedes every earlier slug note).** The target keyword is the one the page H1 is built around. The slug is that target keyword STANDALONE: no prefixes (custom, best, top, free, online, AI), no suffixes (generator, maker, builder, template, app, website, examples), singular not plural. Then remove ONLY the hub category word (LP "landing page"; Form "form"; Automation "automation"; SurveyQuiz "survey" and "quiz"). Lowercase and hyphenated, nothing else changed. Examples: "Build a Custom Thank You Page" -> thank-you-page; "Employment Verification Letter Generator" -> employment-verification-letter; "NDA Form Generator and Signing App" -> nda; "best startup landing pages" -> startup; "HIPAA Release Forms" -> hipaa-release; "Build a Church App" -> church; "Construction Inventory Management App" -> construction-inventory-management. Only exception: safety-quiz, team-quiz, wellness-quiz (collisions with live surveys). One slug function (ops/slugs.py) is used everywhere, and a mismatch BLOCKS create and ship. A slug that breaks the rule is a blocking finding.
