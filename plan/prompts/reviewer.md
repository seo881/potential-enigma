# A-r-<n>: the one review of up to 4 pages (CLAUDE.md step 5)

Read plan/prompts/README.md, then follow .claude/agents/page-reviewer.md exactly. Pages: <URLS>.

For each page:
1. `hubctl review-claim <url> --by A-r-<n>` first (review lock, DECISIONS 2026-11-03). If refused (claimed/held by another agent or you are one of its writers), skip it and say so.
2. Review copy AND rendered images (contact sheet in .cache/review/; render with `hubctl images <url>` only if missing) against the keyword brief, HUB_RULES, rules/rework-checklist.md and rules/SEVERITY.md only.
3. Standards gate: slug == ops/slugs.py slug_for; hero prompt passes L13/L14 and the HERO PROMPT FIX bar. A failure is blocking.
4. Record with `hubctl review` -> `reviewed` (no blocking) or `rework` (blocking findings listed precisely, field by field). Flags that need Divit (PA7 definitions, claims you cannot verify) go in the result for his packet.
5. Commit + push the spec/status paths you changed.
Return per page: verdict, blocking findings (one line each), flags for Divit, SHA.
