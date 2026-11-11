# A-w-<n>: writer, one page (CLAUDE.md step 3)

Read plan/prompts/README.md, then follow .claude/agents/page-writer.md and the hub-content skill exactly. Page: <URL>.

1. `git status` and `git log -- specs/<dir>/<slug>.json`: if partial work exists (committed or uncommitted), continue from it; never discard it.
2. The page is claimed by B-c-1; you work it under the handover (DECISIONS 2026-11-11, A is coordinator). If hubctl refuses because of B's claim or hold, stop and report; do not force.
3. Write to QC TOTAL 0 (`hubctl qc`), hero prompt set by you per the HERO PROMPT FIX bar (one specific sentence in the user's voice, concrete realistic build, exact primary keyword, approved capabilities only, unique in the hub; L13/L14 clean). Slug must equal ops/slugs.py slug_for.
4. Render images (`hubctl images <url>`), read the contact sheet (one hero, readable text, numbers add up, story matches tab copy), fix until clean -> state `images`.
5. Commit + push spec, status and images/<dir>/<slug> with explicit paths.
Return: url, final state, QC total, anything a reviewer or Divit must know, SHA.
