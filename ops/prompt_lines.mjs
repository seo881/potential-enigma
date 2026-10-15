// prompt_lines.mjs: the browser half of ops/prompt_lines.py (hero prompt line rule, Divit 2026-10-15). Read-only: headless
// Chromium (Playwright, pinned in ops/package.json); nothing here writes to Webflow or publishes anything.
//   node ops/prompt_lines.mjs live JOB.json    JOB {urls:[...], widths:[1440,390]}: for each live page and viewport width, the
//        computed style of the hero prompt box (#hero-prompt-form textarea) and the rendered line count of the default prompt
//        and of each chip prompt, composed by the page's own hero-chips script (a real click on each chip, then a click back); optional
//        JOB.texts are typed into the live box one by one, line counts returned as `extra` (validates the local renderer)
//   node ops/prompt_lines.mjs local JOB.json   JOB {fonts:[{file, unicode_range}], items:[{id, style:{css prop: value}, text}]}:
//        renders each text into a <textarea> with exactly those computed styles (the page's own element type, so pre-wrap,
//        break-word and trailing spaces wrap the same way) on a blank page with the cached font files; no network.
// Line count, both modes: the box is measured at height 0 with overflow hidden, so scrollHeight is the text's own height;
// lines = round((scrollHeight - padding-top - padding-bottom) / line-height). JSON on stdout.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const [mode, jobPath] = process.argv.slice(2);
if (!["live", "local"].includes(mode) || !jobPath) { console.error("usage: node ops/prompt_lines.mjs live|local JOB.json"); process.exit(2); }
const job = JSON.parse(fs.readFileSync(jobPath, "utf8"));

// the computed properties that decide where a line breaks or how tall it is (recorded per hub in rules/prompt_box.json)
export const PROPS = ["width", "box-sizing", "font-family", "font-size", "font-weight", "font-style", "font-stretch", "font-kerning",
  "font-feature-settings", "font-variation-settings", "font-optical-sizing", "font-variant-ligatures", "text-rendering",
  "letter-spacing", "word-spacing", "line-height", "text-transform", "text-indent", "tab-size", "white-space", "overflow-wrap",
  "word-break", "hyphens", "direction", "padding-top", "padding-right", "padding-bottom", "padding-left",
  "border-top-width", "border-right-width", "border-bottom-width", "border-left-width", "border-top-style", "border-right-style",
  "border-bottom-style", "border-left-style"];

function linesOf(t) {   // runs in the page
  const cs = getComputedStyle(t);
  const keep = [t.style.height, t.style.minHeight, t.style.maxHeight, t.style.overflowY, t.style.overflow];
  t.style.minHeight = "0"; t.style.maxHeight = "none"; t.style.height = "0px"; t.style.overflow = "hidden";
  const sh = t.scrollHeight;
  [t.style.height, t.style.minHeight, t.style.maxHeight, t.style.overflowY, t.style.overflow] = keep;
  const lh = parseFloat(cs.lineHeight), pad = parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
  return { lines: Math.round((sh - pad) / lh), scroll_height: sh, line_height: lh };
}

const browser = await chromium.launch();
try {
  if (mode === "live") {
    const out = [];
    for (const url of job.urls) for (const W of job.widths || [1440, 390]) {
      const page = await browser.newPage({ viewport: { width: W, height: 900 } });
      const rec = { url, width: W };
      try {
        const resp = await page.goto(url, { waitUntil: "load", timeout: 60000 });
        rec.status = resp ? resp.status() : null;
        await page.waitForTimeout(800);
        if (job.texts) await page.evaluate((x) => { window.__plExtra = x; }, job.texts);
        Object.assign(rec, await page.evaluate(async ({ PROPS, linesSrc }) => {
          const linesOf = eval("(" + linesSrc + ")");
          await document.fonts.ready;
          const f = document.getElementById("hero-prompt-form");
          const t = f && f.querySelector('textarea, [data-name="prompt"]');
          if (!t) return { error: "no #hero-prompt-form textarea" };
          const cs = getComputedStyle(t), style = {};
          PROPS.forEach((p) => (style[p] = cs.getPropertyValue(p)));
          const fonts = []; document.fonts.forEach((x) => { if (x.status === "loaded") fonts.push([x.family, x.weight, x.style]); });
          const P = window.awbPrompt || null;
          const texts = [{ key: "default", text: t.value, ...linesOf(t) }];
          const chips = [...f.querySelectorAll("[data-hubchip]")].length ? [...f.querySelectorAll("[data-hubchip]")] : [...f.querySelectorAll("[data-filter]")];
          chips.forEach((c, i) => {
            c.click(); texts.push({ key: `chip ${i + 1}`, label: c.textContent.trim(), text: t.value, ...linesOf(t) }); c.click();
          });
          const back = t.value === texts[0].text;
          // extra texts (validation): typed into the live box itself, then the default is put back
          const extra = (window.__plExtra || []).map((x) => { t.value = x; return linesOf(t).lines; });
          t.value = texts[0].text;
          return { tag: t.tagName.toLowerCase(), style, fonts_loaded: fonts, awbPrompt: P, texts, back_to_default: back, extra };
        }, { PROPS, linesSrc: linesOf.toString() }));
      } catch (e) { rec.error = String(e); }
      out.push(rec); await page.close();
    }
    process.stdout.write(JSON.stringify(out));
  } else {
    const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
    const faces = (job.fonts || []).map((f) => {
      const b64 = fs.readFileSync(path.resolve(root, f.file)).toString("base64");
      return (f.weights || ["400", "500", "600", "700", "800", "900"]).map((w) =>
        `@font-face{font-family:'${f.family}';font-style:normal;font-weight:${w};src:url(data:font/woff2;base64,${b64}) format('woff2');unicode-range:${f.unicode_range};}`).join("\n");
    }).join("\n");
    const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
    await page.setContent(`<!doctype html><html><head><meta charset="utf-8"><style>${faces}\nbody{margin:0}textarea{display:block;resize:none;outline:0;background:none;margin:0}</style></head><body></body></html>`);
    const res = await page.evaluate(async ({ items, linesSrc }) => {
      const linesOf = eval("(" + linesSrc + ")");
      const out = {};
      // load every face the items use before measuring (a fallback font would wrap differently)
      const fams = new Set();
      for (const it of items) fams.add(`${it.style["font-style"] || "normal"} ${it.style["font-weight"] || "400"} ${it.style["font-size"] || "16px"} ${it.style["font-family"]}`);
      for (const f of fams) { await document.fonts.load(f, "Build a form ÄÉ"); }
      await document.fonts.ready;
      const missing = [...fams].filter((f) => !document.fonts.check(f, "Build"));
      for (const it of items) {
        const t = document.createElement("textarea");
        for (const [k, v] of Object.entries(it.style)) t.style.setProperty(k, v);
        document.body.appendChild(t);
        t.value = it.text;
        out[it.id] = linesOf(t);
        t.remove();
      }
      return { lines: out, missing_fonts: missing };
    }, { items: job.items, linesSrc: linesOf.toString() });
    process.stdout.write(JSON.stringify(res));
    await page.close();
  }
} finally { await browser.close(); }
