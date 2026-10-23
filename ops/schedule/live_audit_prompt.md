Write the prose digest of today's live audit (Divit 2026-10-23). The checks already ran without you (ops/schedule/live_audit_checks.sh); you only read and summarise. Do not run commands, edit files or call Webflow.

Read `audits/live/{{DATE}}/digest.txt` (counts and failing URLs) and, if you need a message, `audits/live/{{DATE}}/findings.json`. Then reply with plain text only:
- Line 1 starts exactly with "Live audit {{DATE}}:" and gives pages checked, pages passed, and P0/P1/P2 counts (copy the numbers from digest.txt; never estimate).
- Then up to 8 lines: each P0 and P1 code with its count and up to 3 URLs, the template-level ones (carousel, Learn, console) first. Say which look like one template cause.
If digest.txt is missing or not dated {{DATE}}, reply exactly "digest unavailable: no checks for {{DATE}}".
