# Reworks and slim reviews (handover 2026-11-11)

Read plan/prompts/README.md. Writer and reviewer are always different agents (hubctl refuses otherwise). Unlock the fields named in a rework BEFORE fixing.

- Rework (A-w-<n>): fix the blocking findings ONLY (the review in the spec lists them), QC to 0, re-render (`hubctl images <url>`), read the contact sheet, commit, then `hubctl ready <url> --by A-w-<n>` -> reviewed. Never a second full review.
- Slim review (A-s-<n>, a different agent): `hubctl review-claim` first, review only the changed fields with rules/SEVERITY.md, record `hubctl slim-review`. Pass -> re-approval under the standing go item 5: `hubctl go-record 2026-11-11 --urls <url> --quote "standing go: Divit 2026-11-11 item 5 (slim review passed after a fix)" --by A-c-1`, then `hubctl state <url> approved --by divit`.
- Page flags that need Divit go into the result for his 2-hourly packet, never to him one at a time.
