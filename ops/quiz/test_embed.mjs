// test_embed.mjs: the playable-quiz embed in a real headless Chromium (docs/QUIZ.md). Run `python3 ops/quiz/build.py` first.
//   node ops/quiz/test_embed.mjs [--shots .cache/quiz]
// Pages come from .cache/quiz/page-*.html (the fixtures in ops/quiz/fixtures, carried exactly as the exporter writes them, under
// hostile global CSS). At 390 px and 1280 px, for the full and the minified embed, it clicks through every result path and every
// option, a keyboard-only run (Tab, Space, arrows, Enter), Back, the empty-answer error, restart; asserts progress, aria, focus,
// result mapping (expected results computed here independently), no network requests, no horizontal overflow, tap sizes, contrast,
// reduced motion, CSS isolation (probe elements outside the quiz keep their styles), escaping and fail-closed. Exit 1 on any failure.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..", "..");
const OUT = path.join(ROOT, ".cache", "quiz");
const fx = (n) => JSON.parse(fs.readFileSync(path.join(ROOT, "ops", "quiz", "fixtures", `${n}.json`), "utf8"));
const FX = { knowledge: fx("knowledge"), matching: fx("matching") };
let fails = 0, passes = 0;
const ok = (cond, msg) => { if (cond) passes++; else { fails++; console.log("FAIL " + msg); } };

// independent expectation (not the embed's code): knowledge = band of the correct count; matching = most picks, first listed on a tie
function expected(q, ans) {
  if (q.type === "knowledge") {
    const pts = ans.filter((a, i) => q.questions[i].options[a].correct === true).length;
    return { key: q.results.find((r) => pts >= r.min && pts <= r.max).key, pts };
  }
  const t = {}; ans.forEach((a, i) => { const k = q.questions[i].options[a].result; t[k] = (t[k] || 0) + 1; });
  let best = q.results[0].key; for (const r of q.results) if ((t[r.key] || 0) > (t[best] || 0)) best = r.key;
  return { key: best, pts: t[best] || 0 };
}
// answer paths: one per result (the band minimum, or every pick on that result where offered) plus option sweeps (option j everywhere)
function paths(q) {
  const out = [];
  for (const r of q.results) {
    if (q.type === "knowledge") {
      let need = r.min;
      out.push(q.questions.map((qq) => { const c = qq.options.findIndex((o) => o.correct === true); if (need > 0) { need--; return c; } return c === 0 ? 1 : 0; }));
    } else out.push(q.questions.map((qq) => { const i = qq.options.findIndex((o) => o.result === r.key); return i < 0 ? 0 : i; }));
  }
  const maxO = Math.max(...q.questions.map((qq) => qq.options.length));
  for (let j = 0; j < maxO; j++) out.push(q.questions.map((qq) => Math.min(j, qq.options.length - 1)));
  return out;
}

const lum = (rgb) => { const c = rgb.match(/\d+(\.\d+)?/g).slice(0, 3).map(Number).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; };
const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };

async function open(browser, name, width, opts = {}) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: opts.reduced ? "reduce" : "no-preference" });
  const page = await ctx.newPage(); const reqs = [], warns = [], errors = [];
  page.on("request", (r) => { if (!r.url().startsWith("data:") && !r.url().startsWith("about:")) reqs.push(r.url()); });
  page.on("console", (m) => { if (m.type() === "warning") warns.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.route("**/*", (r) => r.abort());
  await page.setContent(fs.readFileSync(path.join(OUT, `page-${name}.html`), "utf8"), { waitUntil: "load" });
  return { ctx, page, reqs, warns, errors };
}
const active = (page) => page.evaluate(() => { const a = document.activeElement; return a ? (a.className || a.tagName) + "|" + (a.textContent || "").slice(0, 80) : ""; });

async function startQuiz(page) { await page.click(".emgq .emgq-primary"); }
async function answer(page, idx, q, i, label) {
  const N = q.questions.length;
  ok(await page.textContent(".emgq-count") === `Question ${i + 1} of ${N}`, `${label}: count text q${i + 1}`);
  const bar = await page.$eval(".emgq-bar", (b) => [b.getAttribute("role"), b.getAttribute("aria-valuenow"), b.getAttribute("aria-valuemax"), b.getAttribute("aria-valuemin")]);
  ok(bar[0] === "progressbar" && bar[1] === String(i + 1) && bar[2] === String(N) && bar[3] === "0", `${label}: progressbar aria q${i + 1} ${bar}`);
  ok((await active(page)).startsWith("emgq-q|"), `${label}: focus on question heading q${i + 1}`);
  ok(await page.textContent(".emgq-q") === q.questions[i].text, `${label}: question text q${i + 1}`);
  await page.click(`.emgq-opt:nth-child(${idx + 1})`);
  await page.click(".emgq-primary");
}
async function checkResult(page, q, ans, label) {
  const exp = expected(q, ans), R = q.results.find((r) => r.key === exp.key);
  ok(await page.textContent(".emgq-title") === R.title, `${label}: result ${exp.key} (got "${await page.textContent(".emgq-title")}")`);
  ok(await page.textContent(".emgq-card .emgq-text") === R.description, `${label}: result description`);
  if (q.type === "knowledge") ok(await page.textContent(".emgq-score") === `You got ${exp.pts} of ${q.questions.length} right.`, `${label}: score line`);
  ok((await active(page)).startsWith("emgq-title|"), `${label}: focus on result heading`);
  await page.waitForTimeout(80);
  const live = await page.textContent(".emgq-sr");
  ok(live.startsWith("Your result: " + R.title), `${label}: live region announces the result (${live})`);
  return exp.key;
}

async function layout(page, width, label) {
  const m = await page.evaluate(() => {
    const opts = [...document.querySelectorAll(".emgq-opt, .emgq-btn")].map((e) => e.getBoundingClientRect());
    return { sw: document.documentElement.scrollWidth, minH: Math.min(...opts.map((r) => r.height)), maxR: Math.max(...opts.map((r) => r.right)), minL: Math.min(...opts.map((r) => r.left)) };
  });
  ok(m.sw <= width, `${label}: no horizontal overflow (scrollWidth ${m.sw} at ${width})`);
  ok(m.minH >= 44, `${label}: tap targets >= 44 px (min ${m.minH})`);
  ok(m.maxR <= width && m.minL >= 0, `${label}: controls inside the viewport`);
}

async function a11y(page, label) {
  const r = await page.evaluate(() => {
    const radios = [...document.querySelectorAll(".emgq-radio")];
    const labelled = radios.every((x) => x.labels && x.labels.length === 1 && x.labels[0].textContent.trim());
    const fs = document.querySelector(".emgq-fs"); const lg = fs && fs.querySelector(":scope > legend");
    const names = [...document.querySelectorAll(".emgq-btn")].every((b) => b.textContent.trim().length > 1);
    const live = document.querySelector(".emgq-sr[aria-live='polite'][role='status']");
    const pairs = [];
    const bgOf = (e) => { while (e) { const c = getComputedStyle(e).backgroundColor; if (c && !/rgba\(0, 0, 0, 0\)|transparent/.test(c)) return c; e = e.parentElement; } return "rgb(255, 255, 255)"; };
    for (const e of document.querySelectorAll(".emgq-q, .emgq-count, .emgq-opt, .emgq-btn, .emgq-title, .emgq-text, .emgq-meta, .emgq-err, .emgq-kicker, .emgq-score"))
      if (e.textContent.trim()) pairs.push([e.className, getComputedStyle(e).color, bgOf(e)]);
    return { labelled, legend: !!(lg && lg.textContent.trim()), names, live: !!live, pairs, radios: radios.length };
  });
  if (r.radios) { ok(r.labelled, `${label}: every radio has exactly one label with text`); ok(r.legend, `${label}: fieldset has a legend`); }
  ok(r.names, `${label}: every button has a name`); ok(r.live, `${label}: polite status live region`);
  for (const [cls, fg, bg] of r.pairs) { const c = contrast(fg, bg); ok(c >= 4.5, `${label}: contrast ${c.toFixed(2)} for .${cls.split(" ").join(".")} (${fg} on ${bg})`); }
}

async function isolation(page, label) {
  const s = await page.evaluate(() => {
    const g = (sel) => { const e = document.querySelector(sel); const c = getComputedStyle(e); return [c.color, c.fontSize, c.fontWeight, c.marginBottom, c.display].join(","); };
    return { h2: g(".probe-h2"), p: g(".probe-p"), label: g(".probe"), foot: g(".probe-foot") };
  });
  // values from the hostile sheet in build.py: if the embed's CSS leaked, these would differ
  ok(s.h2 === "rgb(225, 29, 72),40px,700,10px,block", `${label}: page h2 untouched (${s.h2})`);
  ok(s.p === "rgb(37, 99, 235),14px,400,10px,block", `${label}: page p untouched (${s.p})`);
  ok(s.label === "rgb(124, 58, 237),14px,700,5px,block", `${label}: page label untouched (${s.label})`);
  ok(s.foot === "rgb(37, 99, 235),14px,400,10px,block", `${label}: footer p untouched (${s.foot})`);
}

async function run() {
  const shots = (() => { const i = process.argv.indexOf("--shots"); return i > 0 ? process.argv[i + 1] : OUT; })();
  fs.mkdirSync(shots, { recursive: true });
  const browser = await chromium.launch();
  const shotList = [];
  for (const width of [390, 1280]) for (const variant of ["full", "min"]) for (const kind of ["knowledge", "matching"]) {
    const q = FX[kind], label = `${kind}-${variant}-${width}`;
    const { ctx, page, reqs, warns, errors } = await open(browser, `${kind}-${variant}`, width);
    ok(await page.textContent(".emgq-title") === q.title, `${label}: start screen title`);
    ok((await page.$$(".emgq-mount .emgq")).length === 1, `${label}: one quiz rendered`);
    await isolation(page, label); await a11y(page, label + " start");
    if (variant === "min") { const p = path.join(shots, `${kind}-${width}-start.png`); await page.screenshot({ path: p, fullPage: false, clip: await page.$eval(".emgq", (e) => { const r = e.getBoundingClientRect(); return { x: 0, y: r.top + window.scrollY, width: window.innerWidth, height: Math.min(r.height, 1400) }; }) }); shotList.push(p); }
    // empty answer: error shown, focus to the first option, no move
    await startQuiz(page);
    await page.click(".emgq-primary");
    ok((await page.textContent(".emgq-err")) === "Choose an answer to continue.", `${label}: empty answer error`);
    ok((await page.textContent(".emgq-count")) === `Question 1 of ${q.questions.length}`, `${label}: stays on question 1`);
    ok((await active(page)).startsWith("emgq-radio"), `${label}: focus to the first option after the error`);
    await a11y(page, label + " question"); await layout(page, width, label + " question");
    if (variant === "min") { const p = path.join(shots, `${kind}-${width}-question.png`); await page.screenshot({ path: p, clip: await page.$eval(".emgq", (e) => { const r = e.getBoundingClientRect(); return { x: 0, y: r.top + window.scrollY, width: window.innerWidth, height: r.height }; }) }); shotList.push(p); }
    // Back keeps the answer
    await page.click(".emgq-opt:nth-child(2)"); await page.click(".emgq-primary");
    await page.click(".emgq-ghost");
    ok((await page.textContent(".emgq-count")) === `Question 1 of ${q.questions.length}`, `${label}: Back returns to question 1`);
    ok(await page.$eval(".emgq-opt:nth-child(2) .emgq-radio", (r) => r.checked), `${label}: Back keeps the chosen answer`);
    await page.click(".emgq-ghost");
    ok((await active(page)).startsWith("emgq-title|"), `${label}: Back from question 1 returns to the start, focus on title`);
    // every result path and every option
    const seen = new Set();
    for (const [pi, ans] of paths(q).entries()) {
      await page.click(".emgq .emgq-primary");
      if (await page.$(".emgq-meta")) await startQuiz(page);
      for (let i = 0; i < ans.length; i++) await answer(page, ans[i], q, i, `${label} path ${pi}`);
      seen.add(await checkResult(page, q, ans, `${label} path ${pi}`));
      if (pi === 0) { await a11y(page, label + " result"); await layout(page, width, label + " result"); }
      if (pi === 0 && variant === "min") {
        if (await page.$(".emgq-sum")) await page.click(".emgq-sum");
        const p = path.join(shots, `${kind}-${width}-result.png`); await page.screenshot({ path: p, clip: await page.$eval(".emgq", (e) => { const r = e.getBoundingClientRect(); return { x: 0, y: r.top + window.scrollY, width: window.innerWidth, height: Math.min(r.height, 3000) }; }) }); shotList.push(p);
        if (kind === "knowledge") {
          const links = await page.$$eval(".emgq-link", (as) => as.map((a) => [a.href, a.rel, a.target, a.textContent]));
          ok(links.length === 2 && links.every((l) => l[0].startsWith("https://www.nist.gov/") && l[1].includes("noopener") && l[3].startsWith("Source: nist.gov")), `${label}: source links ${JSON.stringify(links)}`);
        }
      }
      await page.click(".emgq-nav .emgq-primary");   // restart
      ok((await page.textContent(".emgq-count")) === `Question 1 of ${q.questions.length}`, `${label}: restart goes to question 1`);
      ok(!(await page.$eval(".emgq-opt:nth-child(1) .emgq-radio", (r) => r.checked)), `${label}: restart clears answers`);
      await page.click(".emgq-ghost");   // back to start for the next path
    }
    ok(q.results.every((r) => seen.has(r.key)), `${label}: every result reached in the UI (${[...seen].join(", ")})`);
    ok(reqs.length === 0, `${label}: no network requests (${reqs.join(", ")})`);
    ok(errors.length === 0 && warns.length === 0, `${label}: no page errors or warnings (${errors.concat(warns).join(" | ")})`);
    await ctx.close();
  }
  // keyboard only: Tab to Start, Enter; per question Tab to the group, Space (first) or ArrowDown (second), Enter; restart by keyboard
  for (const kind of ["knowledge", "matching"]) {
    const q = FX[kind], label = `${kind}-keyboard`;
    const { ctx, page } = await open(browser, `${kind}-min`, 390);
    let found = false;
    for (let t = 0; t < 10 && !found; t++) { await page.keyboard.press("Tab"); found = (await active(page)).startsWith("emgq-btn emgq-primary|Start"); }
    ok(found, `${label}: Start reachable by Tab`);
    await page.keyboard.press("Enter");
    const ans = [];
    for (let i = 0; i < q.questions.length; i++) {
      ok((await active(page)).startsWith("emgq-q|"), `${label}: focus on heading q${i + 1}`);
      await page.keyboard.press("Tab");
      ok((await active(page)).startsWith("emgq-radio"), `${label}: Tab enters the options q${i + 1}`);
      if (i % 2 === 0) { await page.keyboard.press("Space"); ans.push(0); } else { await page.keyboard.press("ArrowDown"); ans.push(1); }
      ok(await page.$eval(`.emgq-opt:nth-child(${ans[i] + 1}) .emgq-radio`, (r) => r.checked), `${label}: option chosen by keyboard q${i + 1}`);
      ok(await page.$eval(`.emgq-opt:nth-child(${ans[i] + 1})`, (l) => l.classList.contains("emgq-on")), `${label}: chosen option styled q${i + 1}`);
      await page.keyboard.press("Enter");
    }
    await checkResult(page, q, ans, label);
    let restart = false;
    for (let t = 0; t < 8 && !restart; t++) { await page.keyboard.press("Tab"); restart = (await active(page)).includes("Take the quiz again"); }
    ok(restart, `${label}: restart reachable by Tab (through the review summary)`);
    await page.keyboard.press("Enter");
    ok((await active(page)).startsWith("emgq-q|"), `${label}: restart focuses question 1`);
    await ctx.close();
  }
  // the hero prompt shares its field with the quiz block: prefill and chips behave exactly as on a page without a quiz
  { const base = await open(browser, "hero-noquiz", 390); await base.page.waitForTimeout(50);
    const h0 = await base.page.evaluate(() => ({ v: document.querySelector("#hero-prompt-form textarea").value, p: JSON.stringify(window.awbPrompt), q: typeof window.awbQuiz }));
    await base.page.click("[data-hubchip='1']"); const h0c = await base.page.$eval("#hero-prompt-form textarea", (t) => t.value);
    ok(h0.v.length > 20 && h0.q === "undefined", `hero-noquiz: prompt prefilled, no quiz data (${h0.v.slice(0, 50)})`);
    ok((await base.page.$$(".emgq-mount .emgq")).length === 0, "hero-noquiz: no quiz rendered");
    await base.ctx.close();
    for (const name of ["knowledge-min", "matching-full", "knowledge-before"]) {
      const { ctx, page } = await open(browser, name, 390); await page.waitForTimeout(50);
      const h = await page.evaluate(() => ({ v: document.querySelector("#hero-prompt-form textarea").value, p: JSON.stringify(window.awbPrompt), q: !!window.awbQuiz, inbox: document.querySelector("#hero-prompt-form textarea").value.includes("awbQuiz") }));
      ok(h.v === h0.v, `${name}: hero prompt prefilled exactly as without a quiz`);
      ok(h.p === h0.p, `${name}: window.awbPrompt identical with the quiz block present`);
      ok(h.q && !h.inbox, `${name}: quiz data separate from the prompt`);
      await page.click("[data-hubchip='1']");
      ok((await page.$eval("#hero-prompt-form textarea", (t) => t.value)) === h0c, `${name}: chip 1 switches the prompt exactly as without a quiz`);
      ok((await page.$$(".emgq-mount .emgq")).length === 1, `${name}: quiz rendered from the hero prompt field`);
      await ctx.close();
    } }
  // reduced motion
  { const { ctx, page } = await open(browser, "knowledge-min", 390, { reduced: true }); await startQuiz(page);
    const d = await page.$eval(".emgq-fill", (e) => getComputedStyle(e).transitionDuration);
    ok(d === "0s", `reduced motion: progress transition ${d}`); await ctx.close();
    const n = await open(browser, "knowledge-min", 390); await startQuiz(n.page);
    ok((await n.page.$eval(".emgq-fill", (e) => getComputedStyle(e).transitionDuration)) !== "0s", "motion allowed: progress transition on"); await n.ctx.close(); }
  // data source variants and fail-closed
  for (const [name, expectQuiz, warnRx] of [["knowledge-before", true, null], ["json-tag", true, null], ["nodata", false, null], ["badjson", false, /invalid JSON/], ["badschema", false, /questions: 6 to 10/]]) {
    const { ctx, page, warns, reqs } = await open(browser, name, 390);
    const n = (await page.$$(".emgq-mount .emgq")).length;
    ok(n === (expectQuiz ? 1 : 0), `${name}: ${expectQuiz ? "renders" : "renders nothing"} (${n})`);
    ok(!(await page.$eval(".emgq-mount", (m) => m.offsetHeight)) === !expectQuiz, `${name}: mount ${expectQuiz ? "visible" : "takes no space"}`);
    ok(warnRx ? warns.some((w) => warnRx.test(w)) : warns.length === 0, `${name}: console warning ${warnRx || "none"} (${warns.join(" | ")})`);
    ok(reqs.length === 0, `${name}: no network requests`);
    await ctx.close();
  }
  // escaping: markup in the data is shown as text, never parsed; a javascript: source is not linked
  { const { ctx, page, reqs } = await open(browser, "escape", 390);
    const t = await page.textContent(".emgq-title");
    ok(t.startsWith("<img src=x onerror=alert(1)> & <b>bold</b>"), `escape: title shown as text (${t.slice(0, 40)})`);
    ok((await page.$$(".emgq img, .emgq b")).length === 0, "escape: no element created from data");
    ok(!(await page.evaluate(() => window.pwned)), "escape: no script injected");
    await startQuiz(page);
    ok((await page.$$(".emgq-q a")).length === 0, "escape: no link created from question text");
    for (let i = 0; i < FX.knowledge.questions.length; i++) { await page.click(".emgq-opt:nth-child(1)"); await page.click(".emgq-primary"); }
    await page.click(".emgq-sum");
    ok(!(await page.$$eval(".emgq-link", (as) => as.some((a) => a.href.startsWith("javascript")))), "escape: javascript: source not linked");
    ok(reqs.length === 0, "escape: no network requests (img src=x never loaded)");
    await ctx.close(); }
  await browser.close();
  fs.writeFileSync(path.join(OUT, "test-result.json"), JSON.stringify({ passes, fails, screenshots: shotList.map((p) => path.relative(ROOT, p)) }, null, 1));
  console.log(`quiz embed: ${passes} checks passed, ${fails} failed; screenshots: ${shotList.map((p) => path.relative(ROOT, p)).join(", ")}`);
  process.exit(fails ? 1 : 0);
}
run().catch((e) => { console.error(e); process.exit(2); });
