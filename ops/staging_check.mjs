// staging_check.mjs: the browser half of ops/staging_check.py (Divit's full staging check, 2026-10-14). Read-only: a headless
// Chromium (Playwright, pinned in ops/package.json) loads public pages; nothing here writes to Webflow or publishes anything.
//   node ops/staging_check.mjs JOB.json          (JOB is written by staging_check.py; results land in JOB.out/pages/*.json)
//   node ops/staging_check.mjs --fixture FILE.html --width W [--hub /ai-form-builder]   one carousel measurement on a local file
//                                                 (golden cases: tests/golden/fixtures/staging_check), JSON on stdout
//   node ops/staging_check.mjs --quiz-fixture .cache/quiz/page-knowledge-min.html --width 390   playthrough self-test
// Per page and width it measures; staging_check.py judges. Measured: HTTP status, console errors, the header (exists, visible,
// bounding box), the rendered DOM (for the internal-link check), og:image, JSON-LD blocks, visible FAQ questions, FAQ clipping
// (every accordion opened on hubs, the first on child pages), empty <p>, section boxes and a full-page screenshot (pixel diff),
// and on the carousel pages the card geometry, hover, Load more and classes; on the template pages the Learn cards; on quiz pages
// a playthrough with the checks of ops/quiz/test_embed.mjs.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
import { captureErrors } from "./console_capture.mjs";

const argv = process.argv.slice(2);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const CAROUSEL_CLASSES = ["section_build", "build_list-wrapper", "build_list", "build_item", "build_link", "build_cover", "build_content_wrapper", "build_title"];

// ---------------------------------------------------------------- in-page measurements (run inside the browser)
function measureCarousel(arg) {
  const { hub } = arg;
  const sec = document.querySelector(".section_build");
  const out = { present: !!sec, displayed: !!(sec && sec.offsetHeight > 0 && getComputedStyle(sec).display !== "none") };
  if (!out.displayed) return out;
  const has = (c) => !!sec.querySelector(`[class~="${c}"], [class^="${c}"]`) || sec.classList.contains(c);
  out.classes = Object.fromEntries(arg.classes.map((c) => [c, c === "section_build" ? true : has(c)]));
  const list = sec.querySelector(".build_list") || sec;
  out.fs_list = list.getAttribute("fs-list-element") || list.getAttribute("fs-cmsload-element") || "";
  out.no_items_text = /No items found/i.test(sec.innerText);
  const items = [...sec.querySelectorAll(".build_item")].filter((i) => i.offsetHeight > 0 && getComputedStyle(i).display !== "none");
  const r = (e) => { const b = e.getBoundingClientRect(); return { x: b.left + scrollX, y: b.top + scrollY, w: b.width, h: b.height }; };
  out.cards = items.map((it) => {
    const as = [...it.querySelectorAll("a[href]")], a = as[0] || null;
    const cover = it.querySelector("img[class*='build_cover']") || it.querySelector("img");
    const title = it.querySelector("[class*='build_title']");
    const cs = cover ? getComputedStyle(cover) : null;
    return {
      n_links: as.length, link_class: a ? a.className : "", href: a ? a.getAttribute("href") : null, abs: a ? a.href : null,
      link_wraps: !!a && (!cover || a.contains(cover)) && (!title || a.contains(title)),
      item: r(it), link: a ? r(a) : null,
      cover: cover ? { box: r(cover), complete: cover.complete, nw: cover.naturalWidth, nh: cover.naturalHeight, fit: cs.objectFit,
        alt: cover.getAttribute("alt"), src: cover.currentSrc || cover.src, cls: cover.className } : null,
      title: title ? { text: title.textContent.trim(), box: r(title), sw: title.scrollWidth, cw: title.clientWidth, sh: title.scrollHeight, ch: title.clientHeight } : null,
    };
  });
  const lm = [...sec.querySelectorAll(".w-pagination-next, [fs-list-element='load-more'], [fs-cmsload-element='load-more'], a, button")]
    .find((e) => (e.matches(".w-pagination-next, [fs-list-element='load-more'], [fs-cmsload-element='load-more']") || /load more/i.test(e.textContent)) && e.offsetHeight > 0 && getComputedStyle(e).visibility !== "hidden");
  out.load_more_visible = !!lm;
  return out;
}

function transforms() {   // computed transform of every card and the elements that carry the hover (link, cover, content)
  const sec = document.querySelector(".section_build"); if (!sec) return [];
  return [...sec.querySelectorAll(".build_item")].filter((i) => i.offsetHeight > 0).map((it) =>
    [it, ...it.querySelectorAll("a, img, [class*='build_content'], [class*='build_cover']")].map((e) => getComputedStyle(e).transform + "|" + getComputedStyle(e).scale + "|" + getComputedStyle(e).translate).join(";"));
}

function measureLearn() {
  const sec = document.querySelector(".section_blog-related");
  const out = { present: !!sec, displayed: !!(sec && sec.offsetHeight > 0 && getComputedStyle(sec).display !== "none") };
  if (!out.displayed) return out;
  out.no_items_text = /No items found/i.test(sec.innerText);
  const items = [...sec.querySelectorAll(".blog_item, .w-dyn-item")].filter((i, k, a) => i.offsetHeight > 0 && a.indexOf(i.closest(".blog_item") || i) === k);
  out.cards = items.map((it) => {
    const a = it.querySelector("a[href]"), img = it.querySelector("img"), t = it.querySelector("[class*='blog_title'], h2, h3");
    return { href: a ? a.getAttribute("href") : null, abs: a ? a.href : null, title: t ? t.textContent.trim() : "",
      img: img ? { complete: img.complete, nw: img.naturalWidth, alt: img.getAttribute("alt"), src: img.currentSrc || img.src } : null,
      date: (it.querySelector("[fs-list-field='date']") || {}).textContent || "" };
  });
  return out;
}

function pageFacts() {
  const q = (s) => document.querySelector(s);
  const vis = (e) => !!e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== "hidden" && getComputedStyle(e).display !== "none";
  const hdrs = [...document.querySelectorAll(".navbar-wrapper, .navbar, header, [role='banner'], nav.w-nav, .w-nav")];
  const h = hdrs.find((e) => vis(e) && e.getBoundingClientRect().height > 0) || null;
  // the masked header region: the union of every header-like element at the top of the page (KS's header work is not judged)
  let hb = null;
  for (const e of hdrs) { const b = e.getBoundingClientRect(); if (!vis(e) || b.height === 0 || b.top + scrollY > 400) continue;
    const x = { y0: b.top + scrollY, y1: b.bottom + scrollY }; hb = hb ? { y0: Math.min(hb.y0, x.y0), y1: Math.max(hb.y1, x.y1) } : x; }
  const faqSec = [...document.querySelectorAll("section")].find((s) => /faq/i.test(s.className) && s.querySelector(".faq_question"));
  const empty = [...document.querySelectorAll("p")].filter((p) => !p.closest(".navbar-wrapper, .navbar, header, nav, .section_footer, footer, script, template, .hide, .w-condition-invisible")
      && !p.querySelector("img, svg, video, iframe, input, button, br + *") && !p.textContent.replace(/[\s ​‌‍⁠﻿]/g, "") && vis(p))
    .map((p) => { const prev = p.previousElementSibling; return { section: (p.closest("section")?.className || "").split(" ")[0], parent: p.parentElement.className.slice(0, 60),
      after: prev ? prev.textContent.trim().slice(0, 60) : "", raw: JSON.stringify(p.innerHTML.slice(0, 40)), w: p.offsetWidth, h: p.offsetHeight }; });
  const sections = [...document.querySelectorAll("body section, body .section_footer")].filter((s) => !s.parentElement.closest("section") && s.offsetHeight > 0)
    .map((s) => { const b = s.getBoundingClientRect(); return { cls: (s.className || "section").split(" ")[0], y: Math.round(b.top + scrollY), h: Math.round(b.height) }; });
  return {
    title: document.title, og_image: q('meta[property="og:image"]')?.getAttribute("content") || "",
    header: h ? { cls: h.className.split(" ")[0], tag: h.tagName.toLowerCase(), h: Math.round(h.getBoundingClientRect().height) } : null, header_box: hb,
    jsonld: [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent),
    faq_questions: faqSec ? [...faqSec.querySelectorAll(".faq_question")].map((e) => e.innerText.trim()).filter(Boolean) : [],
    faq_section: faqSec ? faqSec.className.split(" ")[0] : "",
    empty_p: empty, sections, doc_h: document.documentElement.scrollHeight, doc_w: document.documentElement.scrollWidth,
    quiz: { data: typeof window.awbQuiz === "object" && window.awbQuiz ? window.awbQuiz : null, mounts: document.querySelectorAll(".emgq-mount").length,
      rendered: document.querySelectorAll(".emgq-mount .emgq").length },
  };
}

// open each FAQ item (all on hubs, the first on child pages) and measure whether its answer is cut (overflow hidden or an inner scroll)
async function faqClip(pg, all) {
  const n = await pg.evaluate(() => { const s = [...document.querySelectorAll("section")].find((x) => /faq/i.test(x.className) && x.querySelector(".faq_question")); return s ? s.querySelectorAll(".faq_question").length : 0; });
  const out = [];
  for (let i = 0; i < (all ? n : Math.min(1, n)); i++) {
    const exp = await pg.evaluate((i) => { const s = [...document.querySelectorAll("section")].find((x) => /faq/i.test(x.className) && x.querySelector(".faq_question"));
      const qq = s.querySelectorAll(".faq_question")[i]; qq.scrollIntoView({ block: "center" }); return qq.getAttribute("aria-expanded"); }, i);
    if (exp !== "true") { await pg.evaluate((i) => { const s = [...document.querySelectorAll("section")].find((x) => /faq/i.test(x.className) && x.querySelector(".faq_question")); s.querySelectorAll(".faq_question")[i].click(); }, i); await pg.waitForTimeout(700); }
    out.push(await pg.evaluate((i) => {
      const s = [...document.querySelectorAll("section")].find((x) => /faq/i.test(x.className) && x.querySelector(".faq_question"));
      const qq = s.querySelectorAll(".faq_question")[i], acc = qq.parentElement;
      const cands = [acc, ...acc.querySelectorAll("*")].filter((e) => e !== qq && !qq.contains(e));
      let worst = { cut: 0, scroll: false, cls: "" };
      for (const e of cands) {
        const cs = getComputedStyle(e); if (!/hidden|clip|auto|scroll/.test(cs.overflowY + cs.overflowX)) continue;
        if (!e.textContent.trim()) continue;
        const cut = e.scrollHeight - e.clientHeight, cutx = e.scrollWidth - e.clientWidth;
        const scroll = /auto|scroll/.test(cs.overflowY) && cut > 1;
        if (Math.max(cut, cutx) > worst.cut) worst = { cut: Math.max(cut, cutx), scroll, cls: e.className.split(" ")[0] };
      }
      return { i: i + 1, q: qq.innerText.trim().slice(0, 80), expanded: qq.getAttribute("aria-expanded"), ...worst };
    }, i));
  }
  return out;
}

async function hoverTest(pg) {
  const n = await pg.evaluate(() => document.querySelectorAll(".section_build .build_item").length);
  if (!n) return { done: false };
  const k = Math.min(1, n - 1);
  await pg.mouse.move(1, 1); await pg.waitForTimeout(400);
  const loc = pg.locator(".section_build .build_item").nth(k); await loc.scrollIntoViewIfNeeded(); await pg.waitForTimeout(500);
  const before = await pg.evaluate(transforms);
  await loc.hover(); await pg.waitForTimeout(900);
  const after = await pg.evaluate(transforms);
  await pg.mouse.move(1, 1); await pg.waitForTimeout(300);
  const changed = before.map((b, i) => (b !== after[i] ? i : -1)).filter((i) => i >= 0);
  return { done: true, hovered: k, changed };
}

async function loadMore(pg, exhaust) {
  const count = () => pg.evaluate(() => [...document.querySelectorAll(".section_build .build_item")].filter((i) => i.offsetHeight > 0).length);
  const first = await count(); const steps = [];
  for (let s = 0; s < (exhaust ? 20 : 1); s++) {
    const btn = pg.locator(".section_build .w-pagination-next, .section_build [fs-list-element='load-more'], .section_build [fs-cmsload-element='load-more']").filter({ visible: true }).first();
    if (!(await btn.count())) break;
    const was = await count();
    try { await btn.scrollIntoViewIfNeeded(); await btn.click({ timeout: 5000 }); } catch { steps.push({ error: "click failed" }); break; }
    let now = was; for (let t = 0; t < 12 && now <= was; t++) { await pg.waitForTimeout(400); now = await count(); }
    steps.push({ before: was, after: now }); if (now <= was) break;
  }
  const hrefs = await pg.evaluate(() => [...document.querySelectorAll(".section_build .build_item")].filter((i) => i.offsetHeight > 0).map((i) => i.querySelector("a[href]")?.getAttribute("href") || null));
  return { first, steps, all_hrefs: hrefs };
}

// ---------------------------------------------------------------- quiz playthrough (ops/quiz/test_embed.mjs checks on the live DOM)
let quizLock = Promise.resolve();   // test_embed.mjs keeps module-level tallies: one playthrough at a time
function quizRun(pg, width, label) { const r = quizLock.then(() => quizRun1(pg, width, label)); quizLock = r.catch(() => {}); return r; }
async function quizRun1(pg, width, label) {
  const T = await import(pathToFileURL(path.join(path.dirname(fileURLToPath(import.meta.url)), "quiz", "test_embed.mjs")).href);
  const start = T.failLog.length, t0 = T.tally().passes + T.tally().fails;
  const q = await pg.evaluate(() => window.awbQuiz || null);
  if (!q) return { present: false, error: "window.awbQuiz missing" };
  const n = (await pg.$$(".emgq-mount .emgq")).length;
  if (n !== 1) return { present: true, rendered: n, error: `expected one rendered quiz, found ${n}` };
  try {
    await pg.locator(".emgq").first().scrollIntoViewIfNeeded();
    await T.a11y(pg, label + " start");
    const seen = new Set();
    for (const [pi, ans] of T.paths(q).entries()) {
      await pg.click(".emgq .emgq-primary");
      if (await pg.$(".emgq-meta")) await T.startQuiz(pg);
      for (let i = 0; i < ans.length; i++) await T.answer(pg, ans[i], q, i, `${label} path ${pi}`);
      seen.add(await T.checkResult(pg, q, ans, `${label} path ${pi}`));
      if (pi === 0) { await T.a11y(pg, label + " result"); await T.layout(pg, width, label + " result"); }
      await pg.click(".emgq-nav .emgq-primary"); await pg.click(".emgq-ghost");
    }
    const missing = q.results.filter((r) => !seen.has(r.key)).map((r) => r.key);
    if (missing.length) T.failLog.push(`${label}: results never reached in the UI: ${missing.join(", ")}`);
  } catch (e) { T.failLog.push(`${label}: playthrough error ${String(e).slice(0, 200)}`); }
  const fails = T.failLog.slice(start);
  return { present: true, rendered: 1, type: q.type, questions: q.questions.length, results: q.results.length, checks: T.tally().passes + T.tally().fails - t0, fails };
}

// ---------------------------------------------------------------- one page
async function openPage(browser, url, width, errs) {
  const ctx = await browser.newContext({ viewport: { width, height: 900 }, deviceScaleFactor: 1 });
  const pg = await ctx.newPage();
  await captureErrors(ctx, pg, errs, { w: width });   // with source and stack (Divit's 2026-10-14 exception is source-based)
  let resp = null, error = null;
  for (let a = 0; a < 3 && !resp; a++) {
    try { resp = await pg.goto(url, { waitUntil: "load", timeout: 60000 }); } catch (e) { error = String(e).slice(0, 200); await sleep(3000 * (a + 1)); }
  }
  await pg.waitForTimeout(1200);
  // a stylesheet that failed to load renders the page unstyled (10x taller; seen once in calibration): reload, at most twice
  // (the site's own Webflow stylesheets only: a third-party sheet such as an ad tag's sa.css may fail without changing the page)
  const cssOk = () => pg.evaluate(() => [...document.querySelectorAll('link[rel="stylesheet"]')].filter((l) => /website-files\.com\/.*\.css|webflow.*\.css/.test(l.href) || new URL(l.href, location.href).host === location.host)
    .every((l) => { try { return !!l.sheet && l.sheet.cssRules.length > 0; } catch { return !!l.sheet; } })).catch(() => false);
  let cssRetries = 0;
  while (resp && !(await cssOk()) && cssRetries < 2) { cssRetries++; try { resp = await pg.reload({ waitUntil: "load", timeout: 60000 }); } catch {} await pg.waitForTimeout(1500); }
  const cssLoaded = await cssOk();
  // scroll through so lazy images and scroll-in animations run to their end state, then back to the top
  await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 400) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 150)); } }).catch(() => {});
  await pg.waitForTimeout(1500);
  await pg.evaluate(() => window.scrollTo(0, 0)).catch(() => {});
  await pg.waitForTimeout(1200);
  return { ctx, pg, status: resp ? resp.status() : 0, error: error || (cssLoaded ? null : "a stylesheet did not load (after 2 reloads)"), cssRetries };
}

// Boxes (page coordinates) that move on their own (JS marquees, sliders, counters) or always differ (video, canvas, iframe):
// two samples of every element's box 700 ms apart; for a moving element the nearest still ancestor (its viewport) is masked.
async function volatileBoxes(pg) {
  const snap = () => pg.evaluate(() => [...document.querySelectorAll("body *")].map((e) => { const b = e.getBoundingClientRect(); return [Math.round(b.left), Math.round(b.top + scrollY), Math.round(b.width), Math.round(b.height)].join(","); }));
  const a = await snap(); await pg.waitForTimeout(700); const b = await snap();
  return pg.evaluate(([a, b]) => {
    const els = [...document.querySelectorAll("body *")], moving = new Set(els.filter((e, i) => a[i] !== b[i] && els.length === a.length));
    const out = [], seen = new Set();
    const box = (e) => { const r = e.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height) }; };
    for (const e of moving) {
      let p = e.parentElement; while (p && moving.has(p)) p = p.parentElement;
      if (!p || p === document.body || p.tagName === "SECTION" || seen.has(p)) continue;
      seen.add(p); const r = box(p); if (r.w > 0 && r.h > 0) out.push({ ...r, why: "moving" });
    }
    for (const e of document.querySelectorAll("video, canvas, iframe")) { const r = box(e); if (r.w > 0 && r.h > 0) out.push({ ...r, why: e.tagName.toLowerCase() }); }
    for (const e of document.querySelectorAll("svg")) if (e.querySelector("animate, animateTransform, animateMotion, set")) { const r = box(e); if (r.w > 0 && r.h > 0) out.push({ ...r, why: "animated svg" }); }
    // the active use-case tab pill is sometimes captured unstyled for a frame on the live site (same page, same code, two loads):
    // the tab menu is state, not layout; its labels are checked by verify_launch (T10)
    for (const e of document.querySelectorAll(".w-tab-menu")) { const r = box(e); if (r.w > 0 && r.h > 0) out.push({ ...r, why: "tab state" }); }
    return out;
  }, [a, b]).then(async (out) => {
    // SVG images that animate themselves (SMIL or CSS keyframes inside the file: the use-case mockups); a screenshot catches any frame
    const svgs = await pg.evaluate(async () => {
      const res = [];
      for (const i of document.images) {
        const src = i.currentSrc || i.src; if (!/\.svg(\?|$)/i.test(src) || !i.offsetWidth) continue;
        try { const t = await (await fetch(src)).text(); if (/<animate|<set\b|@keyframes|animation\s*:/i.test(t)) { const r = i.getBoundingClientRect(); res.push({ x: Math.round(r.left), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height), why: "animated svg image" }); } } catch {}
      }
      return res;
    }).catch(() => []);
    return [...out, ...svgs].slice(0, 300);
  });
}

async function settleImages(pg) {   // every image loaded (a failed one is retried once), so a slow CDN is not a pixel change
  await pg.evaluate(async () => {
    const wait = (i) => (i.complete ? null : new Promise((r) => { i.addEventListener("load", r, { once: true }); i.addEventListener("error", r, { once: true }); setTimeout(r, 8000); }));
    await Promise.all([...document.images].map(wait));
    const broken = [...document.images].filter((i) => i.currentSrc && i.complete && i.naturalWidth === 0);
    for (const i of broken) { const s = i.src; i.src = ""; i.src = s; }
    await Promise.all(broken.map(wait));
  }).catch(() => {});
}

async function fullShot(pg, file) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await settleImages(pg);
  await pg.evaluate(() => window.scrollTo(0, 0)); await pg.mouse.move(0, 0); await pg.waitForTimeout(300);
  // no finite CSS transition or animation may be mid-flight (an active-tab pill caught at 0.1 s of its 0.2 s fade read as a change)
  await pg.evaluate(async () => { for (let t = 0; t < 30; t++) {
    const busy = document.getAnimations().filter((a) => a.playState === "running" && Number.isFinite(a.effect?.getComputedTiming?.().endTime ?? Infinity));
    if (!busy.length) return; await new Promise((r) => setTimeout(r, 100)); } }).catch(() => {});
  await pg.screenshot({ path: file, fullPage: true, animations: "disabled", caret: "hide" });
  return { volatile: await volatileBoxes(pg), broken_images: await pg.evaluate(() => [...document.images].filter((i) => i.currentSrc && i.complete && i.naturalWidth === 0 && i.offsetWidth > 0).map((i) => i.currentSrc.slice(0, 120))) };
}

async function sectionShot(pg, sel, file) {
  const el = pg.locator(sel).first();
  if (!(await el.count()) || !(await el.isVisible())) return false;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  await el.scrollIntoViewIfNeeded(); await pg.waitForTimeout(600); await pg.mouse.move(0, 0); await pg.waitForTimeout(300);
  await el.screenshot({ path: file, animations: "disabled" }); return true;
}

async function checkPage(browser, job, p) {
  const res = { url: p.url, kind: p.kind, widths: {}, console: [] };
  const want = (s) => job.sections.includes(s);
  const widths = job.baseline ? [1440, 390] : [...new Set([1440, 390, ...(p.carousel && want("carousel") ? [1024, 768] : []), ...(p.kind === "quiz" && want("quiz") ? [1280] : [])])];
  for (const w of widths) {
    const errs = [];
    const { ctx, pg, status, error } = await openPage(browser, job.base + p.url, w, errs);
    const W = (res.widths[w] = { status, error });
    try {
      if (status !== 200) { if (p.kind === "quiz") { res.not_present = true; break; } continue; }
      const general = w === 1440 || w === 390;
      if (general) {
        Object.assign(W, await pg.evaluate(pageFacts));
        if (w === 1440 && !job.baseline) fs.writeFileSync(path.join(job.out, "html", p.key + ".html"), await pg.content());
        if (job.shots && (w === 1440 || w === 390)) {
          const v = await fullShot(pg, path.join(job.shots, `${p.key}-${w}.png`)); W.shot = `${p.key}-${w}.png`;
          W.shot_sections = await pg.evaluate(pageFacts).then((f) => ({ sections: f.sections, header_box: f.header_box, doc_h: f.doc_h, ...v }));
        }
      }
      if (job.baseline) continue;
      if (general && want("faq")) W.faq_clip = await faqClip(pg, p.kind === "hub");
      if (p.carousel && want("carousel")) {
        await pg.evaluate(() => window.scrollTo(0, 0));
        W.carousel = await pg.evaluate(measureCarousel, { hub: p.hub, classes: CAROUSEL_CLASSES });
        if (W.carousel.displayed) { W.carousel.hover = await hoverTest(pg); W.carousel.load_more = await loadMore(pg, w === 1440); }
      }
      if (p.learn && want("learn") && general) W.learn = await pg.evaluate(measureLearn);
      if (p.kind === "quiz" && want("quiz") && (w === 390 || w === 1280)) W.quiz = await quizRun(pg, w, `${p.url.split("/").pop()}-${w}`);
    } catch (e) { W.error = (W.error ? W.error + "; " : "") + String(e).slice(0, 300); }
    finally { res.console.push(...errs); await ctx.close(); }
  }
  return res;
}

// a Divit screenshot must show the first page of the carousel (before Load more), so it is taken on a fresh load
async function divitShots(browser, job, p) {
  const out = {};
  for (const w of [1440, 390]) {
    const { ctx, pg, status } = await openPage(browser, job.base + p.url, w, []);
    try { if (status === 200) for (const [name, sel] of p.divit) out[`${name}-${w}`] = (await sectionShot(pg, sel, path.join(job.divit, `${name}-${w}.png`))) ? `${name}-${w}.png` : null;
      else for (const [name] of p.divit) out[`${name}-${w}`] = null; }
    finally { await ctx.close(); }
  }
  return out;
}

async function main() {
  if (argv[0] === "--fixture") {   // golden: one carousel measurement on a local file
    const file = path.resolve(argv[1]), w = +argv[argv.indexOf("--width") + 1] || 1440, hi = argv.indexOf("--hub");
    const browser = await chromium.launch();
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
    const pg = await ctx.newPage(); await pg.route(/^https?:/, (r) => r.abort());
    await pg.goto(pathToFileURL(file).href, { waitUntil: "load" }); await pg.waitForTimeout(200);
    const c = await pg.evaluate(measureCarousel, { hub: hi > 0 ? argv[hi + 1] : "", classes: CAROUSEL_CLASSES });
    console.log(JSON.stringify(c)); await browser.close(); return;
  }
  if (argv[0] === "--quiz-fixture") {   // self-test of the live playthrough on a local quiz page (.cache/quiz/page-*.html)
    const w = +argv[argv.indexOf("--width") + 1] || 390, browser = await chromium.launch();
    const ctx = await browser.newContext({ viewport: { width: w, height: 900 } }), pg = await ctx.newPage();
    await pg.goto(pathToFileURL(path.resolve(argv[1])).href, { waitUntil: "load" });
    console.log(JSON.stringify(await quizRun(pg, w, path.basename(argv[1]) + "-" + w))); await browser.close(); return;
  }
  const job = JSON.parse(fs.readFileSync(argv[0], "utf8"));
  fs.mkdirSync(path.join(job.out, "pages"), { recursive: true }); fs.mkdirSync(path.join(job.out, "html"), { recursive: true });
  // one browser per worker, relaunched every 12 pages and after a crash (a 131-page run once lost its shared browser at page 109)
  const queue = [...job.pages]; let done = 0;
  const worker = async () => {
    let browser = await chromium.launch(), used = 0;
    const fresh = async () => { try { await browser.close(); } catch {} browser = await chromium.launch(); used = 0; };
    while (queue.length) {
      const p = queue.shift(); const t = Date.now();
      if (used >= 12 || !browser.isConnected()) await fresh();
      let r;
      for (let attempt = 0; attempt < 2; attempt++) {
        try { r = await checkPage(browser, job, p); break; }
        catch (e) { r = { url: p.url, kind: p.kind, fatal: String(e).slice(0, 300), widths: {}, console: [] }; await fresh(); }
      }
      used++;
      if (!job.baseline && job.divit && p.divit) { try { if (!browser.isConnected()) await fresh(); r.divit = await divitShots(browser, job, p); } catch (e) { r.divit_error = String(e).slice(0, 200); } }
      r.secs = Math.round((Date.now() - t) / 100) / 10;
      fs.writeFileSync(path.join(job.out, "pages", p.key + ".json"), JSON.stringify(r));
      done++; console.log(`[${done}/${job.pages.length}] ${p.url} ${r.secs}s${r.fatal ? " FATAL " + r.fatal : ""}`);
    }
    try { await browser.close(); } catch {}
  };
  await Promise.all(Array.from({ length: Math.max(1, job.concurrency || 4) }, worker));
}
main().catch((e) => { console.error(e); process.exit(2); });
