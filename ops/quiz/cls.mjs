// ops/quiz/cls.mjs: the quiz CLS proof (Divit 2026-11-03: "5 runs at 1440 and 390, under 0.01"). Read-only HTTP + headless Chromium.
// It rebuilds the cls.mjs method of the 2026-10-23 report (reports/2026-10-23/1504-quiz-embed-cls-reservation.md), now kept in git.
//
// Why a stand-in: the canary quizzes (style, vocabulary) are CMS drafts, and neither webflow.io nor emergent.sh renders a draft
// (both 404). So, as on 2026-10-23, the script loads a LIVE SurveyQuiz page served by the target host (the control, default
// /ai-survey-and-quiz-builder/team), intercepts that one document request, and injects the canary's quiz carrier block exactly as
// hubctl exports it (qc/quiz.py embed_block, appended after the awbPrompt block in the hero's alpb---prompt rich text). Every other
// request (CSS, JS, fonts, images, the template's quiz embed 117b49c2) is the host's real response, so the template under test is
// the one the host serves. After the canaries are item-published, run with --direct to measure the real pages instead.
//
// Usage (from the repo root):
//   node ops/quiz/cls.mjs [--base https://emergent-sh.webflow.io] [--runs 5] [--widths 1440,390] [--threshold 0.01]
//                         [--negative] [--stand style,vocabulary] [--control /ai-survey-and-quiz-builder/team] [--direct URL,URL] [--out FILE]
// Exit 0 = every run of every page under the threshold AND the control takes no space; 3 = a failure; 1 = could not run.
// CLS = the largest session window (gap < 1 s, window <= 5 s) of layout shifts without recent input, buffered from navigation,
// over: load + 3 s settle + scroll to the quiz + a full playthrough (start, every question, result, restart). Shifts that follow a
// click have recent input and do not count (the web-vitals definition).
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..", "..");
const { chromium } = require(path.join(ROOT, "ops", "node_modules", "playwright"));

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf("--" + k); return i >= 0 ? argv[i + 1] : d; };
const BASE = opt("base", "https://emergent-sh.webflow.io").replace(/\/$/, "");
const RUNS = parseInt(opt("runs", "5"), 10);
const WIDTHS = opt("widths", "1440,390").split(",").map(Number);
const THRESH = parseFloat(opt("threshold", "0.01"));
const CONTROL = opt("control", "/ai-survey-and-quiz-builder/team");
const DIRECT = (opt("direct", "") || "").split(",").filter(Boolean);
const STAND = DIRECT.length ? [] : opt("stand", "style,vocabulary").split(",").filter(Boolean);
const stamp = new Date().toISOString().replace(/[-:]/g, "").slice(0, 15);
const OUT = opt("out", path.join(ROOT, ".cache", "quiz", `cls-${stamp}-${new URL(BASE).hostname}.json`));
const PY = fs.existsSync(path.join(ROOT, ".venv", "bin", "python3")) ? path.join(ROOT, ".venv", "bin", "python3") : "python3";
// --negative: the stand-in also cancels the reservation (min-height 0), to prove the measure catches the 2026-10-16 shift (expect FAIL)
const NEG = argv.includes("--negative");
const NEG_CSS = "<style>body:has(#awb-quiz-data) .emgq-mount{min-height:0 !important}</style>";
const HEIGHT = { 1440: 900, 768: 1024, 390: 844 };

function carrier(slug) {
  const spec = path.join(ROOT, "specs", "sqb", slug + ".json");
  if (!fs.existsSync(spec)) throw new Error("no spec " + spec);
  return execFileSync(PY, ["-I", "-c",
    "import sys,json;sys.path.insert(0,sys.argv[1]);import quiz;print(quiz.embed_block(json.load(open(sys.argv[2]))['quiz']),end='')",
    path.join(ROOT, "qc"), spec], { encoding: "utf8" });
}

// inject the carrier where the export puts it: after the awbPrompt block inside the hero's hidden prompt rich text
function inject(html, block) {
  const i = html.indexOf('<div class="hide w-richtext">');
  if (i < 0) throw new Error("hero prompt rich text not found on the control page");
  const j = html.indexOf("window.awbPrompt", i);
  const close = "</script></div></div>";
  const k = j < 0 ? -1 : html.indexOf(close, j);
  if (k < 0) throw new Error("awbPrompt block not found in the hero prompt rich text");
  return html.slice(0, k + close.length) + block + html.slice(k + close.length);
}

const OBSERVER = () => {
  window.__ls = [];
  try {
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) window.__ls.push({ v: e.value, t: Math.round(e.startTime), input: e.hadRecentInput,
        src: (e.sources || []).map((s) => (s.node && (s.node.className || s.node.nodeName)) || "?").map(String).slice(0, 3) });
    }).observe({ type: "layout-shift", buffered: true });
  } catch (e) { window.__lsErr = String(e); }
};

function sessionCLS(entries) {
  let best = 0, cur = 0, first = -1, prev = -1;
  for (const e of entries.filter((x) => !x.input)) {
    if (first < 0 || e.t - prev >= 1000 || e.t - first >= 5000) { cur = 0; first = e.t; }
    cur += e.v; prev = e.t; best = Math.max(best, cur);
  }
  return Math.round(best * 1e5) / 1e5;
}

async function measure(browser, url, width, block) {
  const ctx = await browser.newContext({ viewport: { width, height: HEIGHT[width] || 900 }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  await page.addInitScript(OBSERVER);
  const target = url.split("?")[0];
  let status = null;
  if (block) {
    await page.route((u) => u.href.split("?")[0] === target, async (route) => {
      if (route.request().resourceType() !== "document" || route.request().frame() !== page.mainFrame()) return route.continue();
      const resp = await route.fetch();
      status = resp.status();
      await route.fulfill({ response: resp, body: inject(await resp.text(), block), headers: { ...resp.headers(), "content-type": "text/html; charset=utf-8" } });
    });
  }
  const r = { width, status: null, cls: null, cls_load: null, played: false, err: null, mount_h: null, mount_display: null, gap_hero_stats: null };
  try {
    const resp = await page.goto(url, { waitUntil: "load", timeout: 60000 });
    r.status = status ?? (resp && resp.status());
    await page.waitForTimeout(3000);
    const geo = await page.evaluate(() => {
      const m = document.querySelector(".emgq-mount"), s = document.querySelector(".section_stats");
      const hero = m && m.closest(".w-embed") ? m.closest(".w-embed").previousElementSibling : null;
      return { mount_h: m ? Math.round(m.getBoundingClientRect().height) : null, mount_display: m ? getComputedStyle(m).display : null,
        gap: hero && s ? Math.round(s.getBoundingClientRect().top - hero.getBoundingClientRect().bottom) : null,
        quiz: !!document.querySelector(".emgq"), data: !!document.getElementById("awb-quiz-data") };
    });
    Object.assign(r, { mount_h: geo.mount_h, mount_display: geo.mount_display, gap_hero_stats: geo.gap, quiz_rendered: geo.quiz, carrier: geo.data });
    r.cls_load = sessionCLS(await page.evaluate(() => window.__ls));
    if (geo.quiz) {
      await page.locator(".emgq").scrollIntoViewIfNeeded();
      await page.getByRole("button", { name: "Start the quiz" }).click();
      for (let n = 0; n < 12; n++) {
        if (await page.getByRole("button", { name: "Take the quiz again" }).count()) break;
        await page.locator(".emgq-opt").first().click();
        await page.locator(".emgq-form button[type=submit]").click();
        await page.waitForTimeout(150);
      }
      await page.getByRole("button", { name: "Take the quiz again" }).click();
      await page.waitForTimeout(500);
      r.played = true;
    }
    const all = await page.evaluate(() => window.__ls);
    r.cls = sessionCLS(all);
    r.shifts_no_input = all.filter((e) => !e.input).length;
    r.shifts_with_input = all.filter((e) => e.input).length;
    r.entries = all.filter((e) => !e.input);
  } catch (e) { r.err = String(e.message || e).slice(0, 300); }
  await page.unrouteAll({ behavior: "ignoreErrors" }).catch(() => {});
  await ctx.close();
  return r;
}

(async () => {
  let pages;
  try {
    pages = [
      ...STAND.map((slug) => ({ name: `stand-in ${slug} on ${CONTROL}`, url: `${BASE}${CONTROL}?stand=${slug}`, block: carrier(slug) + (NEG ? NEG_CSS : ""), quiz: true })),
      ...DIRECT.map((u) => ({ name: u, url: u.startsWith("http") ? u : BASE + u, block: null, quiz: true })),
      { name: `control ${CONTROL} (survey, no quiz data)`, url: BASE + CONTROL, block: null, quiz: false },
    ];
  } catch (e) { console.error("could not run: " + e.message); process.exit(1); }
  const browser = await chromium.launch();
  const out = { base: BASE, measured: new Date().toISOString(), runs: RUNS, widths: WIDTHS, threshold: THRESH,
    method: "Chromium (Playwright) PerformanceObserver layout-shift, buffered; CLS = max session window of shifts without recent input; load + 3s settle + scroll to quiz + full playthrough + restart",
    pages: {} };
  let fail = 0;
  for (const p of pages) {
    out.pages[p.name] = { url: p.url, runs: {} };
    for (const w of WIDTHS) {
      const rs = [];
      for (let i = 0; i < RUNS; i++) rs.push(await measure(browser, p.url, w, p.block));
      out.pages[p.name].runs[w] = rs;
      const bad = rs.filter((r) => r.err || r.status !== 200 || r.cls == null || r.cls >= THRESH
        || (p.quiz && (!r.played || !r.carrier))
        || (!p.quiz && (r.mount_display !== "none" || (r.gap_hero_stats != null && r.gap_hero_stats !== 0))));
      fail += bad.length;
      const cls = rs.map((r) => r.cls), mh = [...new Set(rs.map((r) => r.mount_h))];
      console.log(`${bad.length ? "FAIL" : "PASS"}  ${p.name} @${w}: cls max ${Math.max(...cls.map((c) => c ?? 1))} [${cls.join(", ")}]`
        + ` mount ${mh.join("/")}px${p.quiz ? ` played ${rs.filter((r) => r.played).length}/${RUNS}` : ` display ${[...new Set(rs.map((r) => r.mount_display))]} gap ${[...new Set(rs.map((r) => r.gap_hero_stats))]}`}`
        + (bad.length ? `  ${bad.map((r) => r.err || `status ${r.status} cls ${r.cls}`).join("; ")}` : ""));
    }
  }
  await browser.close();
  out.result = fail ? "FAIL" : "PASS";
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
  console.log(`${out.result}: ${pages.length} pages x ${WIDTHS.length} widths x ${RUNS} runs, threshold < ${THRESH}; data ${path.relative(ROOT, OUT)}`);
  process.exit(fail ? 3 : 0);
})();
