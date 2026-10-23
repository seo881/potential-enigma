# Reviewer brief (Divit 2026-10-23 item 5)
- Check every line of rules/rework-checklist.md first.
- Run `hubctl verbatim URL` and `hubctl paa URL --spec` (0 rejects, 0 flags).
- Read the contact sheet.
- Severity comes from rules/SEVERITY.md only.
- Never edit the page. Never review a page you wrote any part of.
- No blocking finding: the page moves to reviewed; then run `hubctl ship-check URL`. Blocking finding: record it (the page goes to rework) and stop.
- Slim review (after a rework): `hubctl review-diff`, then `hubctl slim-review`, on the changed fields only.
- Commit your files plus status/<hub>.json with `bash ops/sync.sh`. No Webflow calls. Reply in under 6 lines.
