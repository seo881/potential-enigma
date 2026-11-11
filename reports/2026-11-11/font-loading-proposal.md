# Font-loading fix: proposal for Divit's next site publish (off the critical path)

**Request:** Divit, 2026-11-11 (FULL THROTTLE item 1): "Propose a font-loading fix for my next site publish, off the critical path."

This is a proposal only. Claude makes no Designer, template or site change and no site publish. Quizzes ship meanwhile (vocabulary and the 47 quizzes); nothing waits on this.

## Problem
On a phone, the hero heading and subtitle first paint in the fallback font. Brockmann (`font-display: swap`) and Inter (loaded late by `WebFont.load`) then arrive and are wider, so a line can rewrap and push the page down. Style measured CLS 0.061 at 390 px (the limit is 0.01); the quiz itself never moves (reports/2026-11-06/quiz-cls-390-investigation.md, cc21e187). The same rewrap affects 18 of 64 live SurveyQuiz heroes at 390, and probably pages on the other hubs, which use the same fonts.

## The change: one site-wide head code edit (Site settings > Custom code > Head)
1. Preload the two Brockmann weights the hero uses:
```html
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://cdn.prod.website-files.com/6a0edf12ef1a8562ed56d806/6a16b08c92285082b1df5e71_Brockmann-Medium.woff2">
<link rel="preload" as="font" type="font/woff2" crossorigin href="https://cdn.prod.website-files.com/6a0edf12ef1a8562ed56d806/6a16b08c6a4f5c938bf2f2cf_Brockmann-SemiBold.woff2">
```
2. Load Inter from a static link with `display=optional`, in place of the `WebFont.load({google:{families:["Inter:400,500,600,700,800,900"]}})` call:
```html
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=optional">
```
The `WebFont.load` call is Webflow's own font setting (Site settings > Fonts / Google Fonts). Removing Inter there and adding the link above is the equivalent of the measured variant.

## Measured (browser-side rewrite on production, 2026-11-06)
| Variant | 360 | 390 | 414 |
|---|---|---|---|
| today | 0.0013 | 0.061 | 0.0003 |
| preload Brockmann only | 0.0013 | 0.0275 | 0.0003 |
| preload Brockmann + Inter link, display=block | 0.0003 | 0.0125 | 0.0003 |
| **preload Brockmann + Inter link, display=optional** | **0.0003** | **0.0003** | **0.0003** |

## Cost and risk
- With `display=optional`, a slow first visit may show the fallback for Inter during that page view (no shift; cached afterwards).
- Two extra preloads (about 2 x 30-40 KB woff2) on every page.
- Site-wide head code, so it touches every page. After your publish, B re-measures style at 360/390/414/1440 (5 runs each) and runs the full live audit.

## Rollback
Remove the added head lines and restore Inter in the Webflow font settings, then publish.
