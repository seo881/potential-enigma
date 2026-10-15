# Post-domain-publish plan (template run, 2026-10-15)

Owner: B-c-1 (coordinator, the only Webflow writer). Trigger: KS publishes to the domain after Divit clears the pre-publish gate. Claude never publishes the site (CLAUDE.md). Every step below is read-only against production except step 4, which publishes one CMS item.

Order: 1 → 2 → 3 run back to back within the first hour. 4 only after 1–3 pass. Report to Divit after each step with a pass/fail row.

## 1. Live audit (templates and hubs)
- Run: `.venv/bin/python3 ops/hubctl.py live-audit --since-publish`, then `live-audit report <date>`. It covers the 4 hubs, the 4 templates (one child each) and every changed page.
- Pass: no new failure class against the staging check baseline (the named exceptions are the navbar SVG and Clarity). Headings have no orphan at 390, 768 or 1440 on our headings. The Learn section shows the 3 newest real articles, and there is no "No items found".
- Rollback: send any template failure to Divit and KS with the element ID. The rollback we stage in the Designer is set_visibility false on the 12 sections of `childedits/2026-10-14/template-run/unhide-batch.json` and remove_element on quiz embed 117b49c2. It reaches production only when Divit or KS publishes, so they get the exact list and decide. Claude never publishes it.

## 2. verify-live on every live page
- Run `.venv/bin/python3 ops/hubctl.py verify-live <url>` for every URL with `live: true` in `status/live.json` (157 at the time of writing). The check covers title, meta, H1, FAQ, images, share image and every internal link returning 200.
- Pass: every page passes.
- Rollback: a CMS field failure goes through the normal live-fix path (`hubctl live-fix`, before-value committed, API PATCH, item publish, verify-live). If a template change caused it (for example a broken binding), the step 1 rollback list goes to Divit and KS.

## 3. Production carousel click test
- Reuse the B-qa-3 tooling (857cd609) against production: on the 4 hubs and 4 templates, click 3 cards per page and the 12 Learn cards; load every Load more batch and check that every card href returns 200 with a matching H1; check self-exclusion and hover at 1440, 768 and 390. Screenshots go to `divit/prod-<date>/`.
- Pass: the same as staging run 3 (0 "#", 0 hub-root or /detail_ links, 0 404s, the current page never listed).
- Rollback: as in step 1, the hide list goes to Divit and KS.

## 4. Quiz canary: style-quiz
- Precondition: steps 1–3 pass. style-quiz is `reviewed` (flags Q3 and Q6 kept, approved by Divit 2026-10-15).
- Steps:
  1. The approve step runs in the foreground so Divit sees the prompt: `hubctl state /ai-survey-and-quiz-builder/style-quiz approved --by divit`.
  2. `hubctl cms-check SurveyQuiz <fresh readback>`.
  3. `hubctl api-create SurveyQuiz --sha <sha> --limit 1`, run as `--before-only`, then commit and run `--live`. The item is created as a draft, read back and checked with bulk-verify (`cms_draft`).
  4. `hubctl api-publish SurveyQuiz --before-only`, then commit, then `--live --verify-live`. This is an item publish of style-quiz only.
- Playthrough on production at 1440 and 390: start the quiz, answer every question, reach a result, restart, and check keyboard navigation. Record console errors, layout shift and screenshots.
- Pass: the quiz completes at both widths, with 0 console errors and no layout shift outside the quiz block.
- Rollback on any failure: unpublish style-quiz at once through the API script (the item goes back to draft; the before-value is in childedits), read it back, confirm the URL returns 404, then report. Nothing else changes.

## 5. Afterwards
- Update logs/templates.md (production state), status/live.json (refreshed by `api-read`), and write a work report in reports/.
