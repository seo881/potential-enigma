# Playable quiz (SurveyQuiz quiz pages)

Divit ordered this on 2026-10-14 (DECISIONS, "The day's steps" item 5). Quiz pages are SurveyQuiz pages whose slug contains `quiz`. Each one carries a quiz that visitors can play on the page, with one question per screen, a progress bar, a result screen and a restart.

Until the template is live, quiz pages can be written and reviewed but not shipped. Code enforces this: `quiz_template_live` must be `true` in `config/collections.json`.

## 1. Where the data lives

There is **no new field**. The 4 child collections are at Webflow's 60-field cap. The 2026-10-14 read-back of the SurveyQuiz collection shows:
- All 60 custom fields are mapped in `config/collections.json`.
- Every PlainText and RichText field holds a value on all 16 items.
- The only empty fields are the MultiReference fields `acrm---tutorials`, `acrm---case-study` and `acrm---integration`, which cannot hold text.

**Carrier (Divit approved, 2026-10-14):** `alpb---prompt`, the hero prompt RichText. The exporter appends the quiz as its **own** rich-text embed block after the hero prompt's `<p>` and its `window.awbPrompt` block:

```
<p>Build a vocabulary quiz ...</p><div data-rt-embed-type='true'><div data-rt-embed-type='true'><script> window.awbPrompt = {...}; </script></div></div><div data-rt-embed-type='true'><div data-rt-embed-type='true'><script id='awb-quiz-data'> window.awbQuiz = {...}; </script></div></div>
```

How the export behaves:
- **Separate data.** The block is `window.awbQuiz` inside `<script id='awb-quiz-data'>`. `window.awbPrompt` and the visible `<p>` are byte-for-byte what they would be without a quiz. Readers of `window.awbPrompt` (hero-chips.html, t1-hero-prompt.html, verify_launch.mjs, launch.py, live_audit.py) never see quiz text.
- **Only quiz pages carry it.** A spec without `quiz` exports exactly as before. Golden case `quiz-carrier-noquiz-identical` checks every SurveyQuiz spec this way.
- **Safe escaping.** The JSON is compact, with `<`, `>`, `&`, U+2028 and U+2029 written as `\u` escapes, so the value can never close the script or open a tag. Escaping is done by `qc/quiz.py embed_block`.
- **Size.** Rich-text code is capped at 50,000 characters. QC Z9 fails a carrier value over 45,000. A 10-question quiz is about 3-6k, and the hero prompt about 0.9k.
- **Checked.** `bulk-verify`, `ship-update` and `api-*` compare the composed value like any other field, since it comes from `export_fields`. QC Z9 re-composes the field and checks three things: the `<p>` and `awbPrompt` are unchanged, there is exactly one extra block, and that block decodes to `spec.quiz`.
- **Verified live.** For quiz pages, `verify-live` also checks:
  - `window.awbPrompt` on the page equals the approved default and chips;
  - the hero `<p>` text is on the page;
  - `window.awbQuiz` equals `spec.quiz`;
  - the template's quiz embed is present.
- **Comments are skipped.** Every parser uses `qc/quiz.py js_object`, which tries each `window.<name> =` and keeps only the one that decodes as JSON and ends in `; </script>`. Comments that mention the names are never misread.

**Ship guard.** `hubctl quiz_ship_block` refuses every quiz page in `_field_data`, `payload`, `bulk-payload`, `api-create` and `ship.py build_payloads` until `quiz_template_live` is `true` and a carrier is set. This also covers a quiz-slug page that has no quiz.

## 2. The JSON (spec.quiz)

```json
{
 "version": 1,
 "type": "knowledge",
 "title": "How Well Do You Know Metric Units?",
 "intro": "Eight questions on SI units and conversions. ...",
 "questions": [
  {"text": "How many base units make up the International System of Units (SI)?",
   "options": [{"text": "5"}, {"text": "7", "correct": true}, {"text": "9"}, {"text": "12"}],
   "explanation": "Every other SI unit ... is built from these base units.",
   "source": {"url": "https://www.nist.gov/pml/owm/metric-si/si-units", "quote": "The SI is made up of 7 base units that define ..."}},
  {"text": "How many centimeters are in 2.5 meters?", "options": [...], "explanation": "One meter is 100 centimeters, so 2.5 x 100 = 250.", "derivable": true}
 ],
 "results": [
  {"key": "keep-practicing", "title": "Keep Practicing", "description": "...", "min": 0, "max": 3},
  {"key": "solid-basics", "title": "Solid Basics", "description": "...", "min": 4, "max": 6},
  {"key": "metric-pro", "title": "Metric Pro", "description": "...", "min": 7, "max": 8}
 ]
}
```

| Key | Rule |
|---|---|
| `version` | `1` |
| `type` | `knowledge`: one option per question has `"correct": true`; the score is the number of correct answers; each result has a score band `min`-`max`, and the bands cover 0..N exactly once. `matching`: each option has `"result": <result key>`; the most points wins, and a tie goes to the result listed first. Use `matching` for personality-style quizzes, with results framed as preferences. |
| `title`, `intro` | At most 70 and 200 characters; `intro` is optional. |
| `questions` | 6-10. Each has `text` (at most 140), 2-6 `options` (`text` at most 80), an optional `explanation` (at most 240), an optional `source` `{url (https), quote (exact span, 6+ words)}` and an optional `derivable: true`. |
| `results` | 2-6. Each has `key` (lowercase, digits and hyphens, at most 24), `title` (at most 60), `description` (at most 320), plus `min` and `max` for knowledge quizzes. |

Two complete examples, both QC-clean, are in `ops/quiz/fixtures/knowledge.json` and `ops/quiz/fixtures/matching.json`.

## 3. Writing rules (pack, QC and reviewer)

- **Promise.** The quiz plays the page's promise: a vocabulary quiz tests vocabulary, and a style quiz names a style. The results answer what the H1 says Emergent builds. QC Z0 at P2 flags a title that names none of the primary's words; the reviewer judges the rest.
- **Sources.** A knowledge question states a fact (its answer), so it carries `source` with the exact quoted span.
  - A question answered by calculation or logic may be `"derivable": true`, with the working in `explanation`.
  - In any quiz, an explanation that states a fact needs a source. That covers numbers, studies, "the largest" and "means" (`rules/quiz.json fact_rx`).
  - QC Z4 checks this. `hubctl sources-check URL` link-checks quiz sources, and Z4 fails sources that are dead, moved or unchecked for more than 7 days.
- **Never a diagnosis.** QC Z5 is P0 and uses the patterns in `rules/quiz.json` (`diagnosis`). It catches:
  - "you have X", "you are depressed/ADHD/...", "signs of", "a test for", "your IQ is", "diagnose", "clinically";
  - a disclaimer ("this is not a diagnosis") is allowed.
  - Results are preferences ("your answers lean toward ..."), never conditions or fixed traits.
- **No franchises.** No trademarked characters, franchises or branded tests as results (QC Z8), unless the page's primary keyword names them. Keep everything suitable for a school-age reader (reviewer).
- **Plain text and house style** (QC Z7):
  - no HTML or angle brackets;
  - straight quotes, no dashes, no exclamation marks, no emoji;
  - serial comma, US spelling, no we/our, no AI-tell words.
- **Mobile at 390 px.** The length limits above are QC Z6.

| QC | Severity | What |
|---|---|---|
| Z0 | P1 | Quiz page without `spec.quiz`, or `spec.quiz` on a page that is not a quiz page. P2: the title names none of the primary's words. |
| Z1 | P0 / P1 | P0: what the embed's runtime validation rejects (it would render nothing): version, type, title, result fields, exactly one correct option. P1: unknown keys, key shape, duplicate texts. |
| Z2 | P0 | Counts: 6-10 questions, 2-6 options, 2-6 results. |
| Z3 | P0 / P1 | P0: knowledge bands with a gap, an overlap or out of range; an option mapped to no result. P1: a result mapped in fewer than 2 questions, or one no set of answers can reach (exact check: capacity assignment with the first-listed tie rule). |
| Z4 | P1 | Sources as above. P2: the quote does not contain the correct answer. |
| Z5 | P0 | Diagnosis claim. |
| Z6 | P1 | Length limits. |
| Z7 | P1 | Hygiene and house style. |
| Z8 | P1 | Franchise or branded test. |
| Z9 | P0 / P1 | Carrier composition (section 1). |

## 4. Writer flow (skeleton and pack)

1. `skeleton.py build URL --by A-w-n` on a quiz page also writes `spec.quiz: null` and `spec.quiz_plan`, which holds the suggested type (from `rules/quiz.json type_hints`), the counts and the limits.
2. `skeleton.py pack URL` adds section 7 and a **Quiz** section with the rules above, GOOD/BAD examples, and the path to the fixtures.
3. `skeleton.py set URL quiz @/path/quiz.json`, then `skeleton.py check URL quiz` until 0 (`check URL all` includes the quiz).
4. `ops/review.py URL` prints the quiz for review, with the correct options, the result each option maps to, and the sources. `hubctl export-csv SurveyQuiz` has a `quiz` column.

`spec.quiz` is part of the approval fingerprint and the review hash (only when present, so existing pages' hashes are unchanged).

## 5. The template (coordinator, staging only)

Paste **`ops/quiz/embed.min.html`** (15.1k characters; the Code Embed limit is 50,000) into **one new HTML Embed element** on the SurveyQuiz Collection template:
- Place it between the hero section and the next section (features), at body level, not inside any component or symbol.
- Optional: wrap it in a Div Block with a new class `emgq-section` and conditional visibility "Name contains quiz" (or leave it unconditional, since without data it renders nothing and takes no space).
- Nothing is bound in the embed. The data arrives through the hero prompt RichText that is already on the template.
- No existing element, class or component is edited.
- `ops/quiz/embed.html` is the readable source; `python3 ops/quiz/build.py` regenerates the minified copy and refuses any CSS selector outside `.emgq` classes.

Space reservation (Divit 2026-10-23, CLS): on a page whose hero carries `#awb-quiz-data`, the mount keeps `min-height` 438 px (435 px at 479 px and below), the larger measured start screen of style-quiz and vocabulary-quiz, so rendering at DOMContentLoaded does not push the sections below. The gate `body:has(#awb-quiz-data)` is the one selector prefix build.py allows; pages without quiz data take no space.

What the embed does:
- **Reads the data** from `window.awbQuiz`, falling back to `<script type="application/json" id="emgq-data">` or a `.emgq-data` element.
- **Validates it** with the same rules as Z1-Z3. Invalid or missing data renders nothing; invalid data logs one console warning.
- **Renders** a start screen, one question per screen and a result screen:
  - each question is a `fieldset` with a `legend` holding the `h3`, and the options are native radio inputs;
  - "Question n of N" sits above a progress bar with `role=progressbar`, `aria-valuenow`, `aria-valuemax` and `aria-valuetext`;
  - an empty answer shows a `role=alert` error and moves focus to the first option;
  - Back keeps the chosen answer;
  - the result screen shows the title, the score line (knowledge), the description, a `details` list of answers with explanations and source links (https only, `noopener noreferrer nofollow`), and a restart button.
- **Focus.** Focus moves to the new question heading or the result heading. A polite status live region announces progress and the result.
- **No outside access.** Text is set with `textContent` only. There are no external requests and no libraries.
- **Respects user settings.** It honors `prefers-reduced-motion` and fits 390 px.

**Staging canary (Divit's condition 4):**
1. Write and review 2 quiz pages.
2. Create them as drafts on staging and publish the items to staging.
3. Run `verify-live` (hero prompt and quiz checks) and play both quizzes at 390 px and 1280 px.
4. Only then set `quiz_template_live: true` (with Divit's go).

## 6. Tests

- **Browser.** Run `python3 ops/quiz/build.py`, then `node ops/quiz/test_embed.mjs` (from `ops/`). This uses headless Chromium (Playwright 1.48.2) at 390 px and 1280 px, on the full and the minified embed, under hostile global CSS, with the carrier composed exactly as exported for a real SurveyQuiz spec, plus the template's hero-chips script. It covers:
  - every result path and every option, Back, the empty-answer error and restart;
  - a keyboard-only run;
  - progressbar aria, focus, the live region, tap targets of at least 44 px, no horizontal overflow, and WCAG AA contrast on every text element;
  - reduced motion and CSS isolation;
  - the hero prompt prefill and chips behaving identically with and without the quiz block;
  - fail-closed cases (no data, bad JSON, bad schema), escaping (markup in the data, `javascript:` sources) and zero network requests.
  - Screenshots land in `.cache/quiz/`.
- **Golden** (`tests/golden/run.py`):
  - `quiz-qc`: every Z check, positive and negative;
  - `quiz-js`: the shipped minified embed's own validate and score in node (`ops/quiz/logic.mjs`), mirrored by Python;
  - `quiz-agree`: the runtime validation and QC P0 agree;
  - `quiz-carrier`: non-quiz byte identity, composition, Z9, verify-live with and without the block, the ship guard, CSS scope and type hints.
