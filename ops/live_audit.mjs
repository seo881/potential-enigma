// live_audit.mjs: Layer A of the live audit (docs/LIVE_AUDIT.md), the browser half. Read-only (HTTP GET/HEAD and a headless browser).
//   node ops/live_audit.mjs MANIFEST.json OUT.json [--base https://emergent-sh.webflow.io] [--shots DIR] [--external]
// MANIFEST is written by `hubctl live-audit` (ops/live_audit.py) from the specs. First, every held page (status/ship/*.json) is
// fetched on every held host: a 200 anywhere is a P0 (A0-held-live). Per page this script records:
//   - the verify_launch checks (ops/verify_launch.mjs checkPage: H1, title, meta, canonical, WebP og:image, FAQ, hero prompt and chips
//     (T1), first tab (T10), use-case images, table, Learn list, hub link, links to non-live pages, carousel cover alt (T5));
//   - from a real Chromium render (Playwright, pinned in ops/package.json): visible text, all text, robots, every link with its HTTP
//     status, every image (src, alt, loaded, natural size), JSON-LD blocks, and 1440 px and 390 px full-page screenshots.
// Python (ops/live_audit.py) turns this into findings, severities and drift. Hubs (manifest.hubs) get the carousel check and the
// same extraction. Nothing here writes to Webflow.
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { checkPage, checkHub, setBase, status, statusRetry, transient, RETRY_MS, sleep, ogWebp } from "./verify_launch.mjs";
import { captureErrors, tieElements } from "./console_capture.mjs";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf(k); if (i < 0) return d; const v = argv[i + 1]; argv.splice(i, 2); return v; };
const flag = (k) => { const i = argv.indexOf(k); if (i < 0) return false; argv.splice(i, 1); return true; };
const BASE = (opt("--base", "https://emergent.sh")).replace(/\/$/, ""), SHOTS = opt("--shots", ""), EXTERNAL = flag("--external");
// --page-timeout S: one page's checks + render + link probes get S seconds (default 300); past that the page is recorded as a transport
// error (http 0, timeout) and the run goes on (2026-10-23: a serial full run hung for 6 hours). --hubs-only: shard for the hub checks
// (ops/schedule/live_audit_checks.sh); the carousel is compared with every manifest page of that hub.
const PAGE_MS = 1000 * +opt("--page-timeout", "300"), HUBS_ONLY = flag("--hubs-only");
const withTimeout = (p, ms, what) => Promise.race([p, new Promise((_, rej) => setTimeout(() => rej(new Error(`timeout after ${ms / 1000} s: ${what}`)), ms))]);
setBase(BASE);
const [MAN, OUT] = argv;
const man = JSON.parse(fs.readFileSync(MAN, "utf8"));
const hosts = [new URL(BASE).host, "emergent.sh", "www.emergent.sh"];
const statusCache = new Map();
const headStatus = async (u) => {
  // a transient answer (0, 5xx, 429) is re-tried with backoff (statusRetry, Divit 2026-11-03): a crawl of many links trips rate limits
  if (!statusCache.has(u)) statusCache.set(u, statusRetry(u, "HEAD"));
  const s = await statusCache.get(u);
  if (transient(s)) statusCache.delete(u);   // a transient answer is not cached: the next page probes again (one bad probe made 40 P0s, 2026-10-12)
  return s;
};
// /sitemap.xml may be a sitemap index (2026-10-12: post-, page-, news- and archive-news-sitemap.xml): read every child sitemap it lists
const sitemap = await (async () => { const get = async (u) => { try { const r = await fetch(u, { signal: AbortSignal.timeout(60000) }); return r.ok ? await r.text() : ""; } catch { return ""; } };
  const top = await get(BASE + "/sitemap.xml"); if (!/<sitemapindex/i.test(top)) return top;
  const kids = [...top.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(/^https?:\/\/[^/]+/, BASE));
  return (await Promise.all(kids.map(get))).join("\n"); })();

const browser = await chromium.launch();
async function render(url, slug) {
  const out = {};
  for (const [w, h] of [[1440, 900], [390, 844]]) {
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
    const pg = await ctx.newPage(); let resp = null; const perr = [];
    // errors with their source (script URL, stack) through CDP: Divit's 2026-10-14 console exception is source-based (ops/console_filter.py)
    await captureErrors(ctx, pg, perr);
    for (let a = 0; a < 2 && !resp; a++) {   // a navigation error is retried once (capped: the page timeout bounds the whole page)
      try { resp = await pg.goto(url, { waitUntil: "load", timeout: 45000 }); } catch (e) { out.error = String(e).slice(0, 200); await pg.waitForTimeout(3000 * (a + 1)); }
    }
    await pg.waitForTimeout(1500);
    // scroll through the page so lazy-loaded images load before they are checked, then back to the top
    await pg.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 120)); } window.scrollTo(0, 0); }).catch(() => {});
    await pg.waitForTimeout(1500);
    if (w === 1440) {
      out.http = resp ? resp.status() : 0;
      Object.assign(out, await pg.evaluate(() => {
        const q = (s) => document.querySelector(s), meta = (n) => q(`meta[name="${n}"]`)?.getAttribute("content") ?? null;
        const clone = document.body.cloneNode(true); clone.querySelectorAll("script,style,noscript,template").forEach((e) => e.remove());
        return {
          title: document.title, description: meta("description"), robots: meta("robots"),
          canonical: q('link[rel="canonical"]')?.getAttribute("href") || "", og_image: q('meta[property="og:image"]')?.getAttribute("content") || "",
          h1s: [...document.querySelectorAll("h1")].map((e) => e.textContent.trim()),
          text_visible: document.body.innerText, text_all: clone.textContent,
          links: [...document.querySelectorAll("a[href]")].map((a) => ({ href: a.href, text: a.textContent.trim().slice(0, 120), in_faq: !!a.closest("[data-faq-wrapper]"), visible: !!(a.offsetWidth || a.offsetHeight) })),
          images: [...document.querySelectorAll("img")].map((i) => ({ src: i.currentSrc || i.src, alt: i.getAttribute("alt"), cls: i.className, loaded: i.complete && i.naturalWidth > 0, w: i.naturalWidth, h: i.naturalHeight, visible: !!(i.offsetWidth || i.offsetHeight) })),
          jsonld: [...document.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent),
          faq_visible: [...document.querySelectorAll("[data-faq-wrapper]")].map((e) => e.innerText).join("\n"),
          empty_sections: [...document.querySelectorAll("section")].filter((s) => (s.offsetHeight > 0) && !s.innerText.trim() && !s.querySelector("img,svg,video,iframe,canvas")).map((s) => s.className).slice(0, 10),
        };
      }));
    }
    await tieElements(pg, perr).catch(() => {});   // ties markup errors to their element (the navbar svg exception, Divit 2026-10-15)
    if (w === 1440) out.console_errors = perr;
    if (SHOTS) { fs.mkdirSync(SHOTS, { recursive: true }); await pg.screenshot({ path: path.join(SHOTS, `${slug}-${w}.png`), fullPage: true }).catch(() => {}); }
    await ctx.close();
  }
  await retryFailedLoads(out);
  return out;
}

// Divit 2026-11-03 (B-dev-21): the Mac run found 44 A8-load and an A9-console net::ERR_SOCKET_NOT_CONNECTED on shared CDN assets that
// all returned 200 on re-check (11 shards' browsers on one home network). A failed resource load is re-fetched (the same URL) before it
// counts, on both runners: up to RETRY_MS.length re-tries with backoff. The finding is still scored when the failure persists.
//  - an image that did not load (visible, not complete or naturalWidth 0): decoded again in a fresh browser context (a new connection);
//    images[i].retry = {ok, attempts, status, w, h}. Python counts A8-load unless retry.ok. A real 404 stops at once (never ok); an
//    image that answers 200 but does not decode (broken file) is never ok.
//  - a console entry that is purely a network failure (rules/live_audit.json console_network_retry, kind "log", with the resource URL
//    as its source): the URL is fetched again (statusRetry); retry = {ok, status}. Python drops it only when retry.ok (2xx). Script
//    errors, page errors and any other console text are never re-tried and still count.
const NET_RX = new RegExp(JSON.parse(fs.readFileSync(new URL("../rules/live_audit.json", import.meta.url), "utf8")).console_network_retry);
const loadedOnce = new Map();   // src -> retry result, only for a success (a failure is never cached: each page re-tries)
async function decodeOnce(src) {
  const ctx = await browser.newContext(); const pg = await ctx.newPage();
  try {
    return await withTimeout(pg.evaluate(async (u) => { const i = new Image(); i.src = u; try { await i.decode(); } catch {}
      return { loaded: i.complete && i.naturalWidth > 0, w: i.naturalWidth, h: i.naturalHeight }; }, src), 45000, "image " + src);
  } catch (e) { return { loaded: false, error: String(e).slice(0, 120) }; } finally { await ctx.close().catch(() => {}); }
}
async function retryImage(src) {
  if (loadedOnce.has(src)) return loadedOnce.get(src);
  let r = { ok: false, attempts: 0 };
  for (let a = 0; a < RETRY_MS.length; a++) {
    await sleep(RETRY_MS[a]);
    const d = await decodeOnce(src), st = await status(src, "GET");
    r = { ok: !!d.loaded, attempts: a + 1, status: st, w: d.w, h: d.h, ...(d.error ? { error: d.error } : {}) };
    if (r.ok) { loadedOnce.set(src, r); break; }
    if (!transient(st) && st !== 200) break;   // 404, 410, 403: final, the image is broken; no more re-tries
  }
  return r;
}
async function retryFailedLoads(out) {   // in parallel per page (one probe per distinct URL), so a flaky network cannot run into the page timeout
  const imgs = (out.images || []).filter((i) => i.visible && !i.loaded && i.src && /^https?:/.test(i.src));
  const nets = (out.console_errors || []).filter((e) => e.kind === "log" && NET_RX.test(e.t || "") && /^https?:/.test(e.src || ""));
  const ir = new Map(), nr = new Map();
  for (const i of imgs) if (!ir.has(i.src)) ir.set(i.src, retryImage(i.src));
  for (const e of nets) if (!nr.has(e.src)) nr.set(e.src, statusRetry(e.src, "GET"));
  for (const i of imgs) i.retry = await ir.get(i.src);
  for (const e of nets) { const s = await nr.get(e.src); e.retry = { ok: s >= 200 && s < 300, status: s }; }
}

async function linkStatuses(links) {
  const out = {};
  for (const l of links) {
    let u; try { u = new URL(l.href); } catch { continue; }
    if (!/^https?:$/.test(u.protocol)) continue;
    const internal = hosts.includes(u.host);
    if (!internal && !EXTERNAL) continue;
    const target = internal ? BASE + u.pathname : u.href.split("#")[0];
    out[l.href] = { internal, status: await headStatus(target) };
  }
  return out;
}

async function svgRatio(u) {
  try { const t = await (await fetch(u, { signal: AbortSignal.timeout(30000) })).text(); const vb = t.match(/viewBox="\s*[-\d.]+\s+[-\d.]+\s+([\d.]+)\s+([\d.]+)"/);
    return vb ? +(vb[1] / vb[2]).toFixed(4) : null; } catch { return null; }
}

const result = { base: BASE, date: new Date().toISOString(), sitemap_ok: !!sitemap, pages: [], hubs: [], held: [] };
// A0: pages held in status/ship/*.json must not be live on any host (GET, no cache; 200 = live)
for (const hp of man.held || []) {
  const st = {};
  for (const host of man.held_hosts || [BASE]) st[host] = await statusRetry(`${host.replace(/\/$/, "")}${hp.url}?la=${Date.now()}`, "GET");   // a transport error is re-tried, so a live held page is not missed
  result.held.push({ ...hp, status: st });
  const live = Object.entries(st).filter(([, c]) => c === 200).map(([h]) => h);
  console.log(`${live.length ? "P0 HELD PAGE LIVE" : "held ok "} ${hp.url}${live.length ? "  on " + live.join(", ") : ""}`);
}
for (const p of HUBS_ONLY ? [] : man.pages) {
  const slug = p.url.split("/").pop(); let r = { url: p.url };
  const one = async () => {
    const v = await checkPage(p, { keepDom: false }); delete v.html; r.checks = v.checks; r.verify = v;
    if (v.checks.http200) {
      r.render = await render(BASE + p.url, slug);
      r.link_status = await linkStatuses(r.render.links || []);
      r.in_sitemap = !!sitemap && (sitemap.includes(`emergent.sh${p.url}<`) || sitemap.includes(`${new URL(BASE).host}${p.url}<`));
      r.uc_ratio = {}; for (const u of p.uc_images.filter(Boolean)) r.uc_ratio[u] = await svgRatio(u);
      r.og = v.og || (r.render.og_image ? await ogWebp(new URL(r.render.og_image, BASE).href) : null);
    }
  };
  // transport: a page fetch that never answered (http 0), a browser navigation error (net::ERR_*), or the page timeout
  try { await withTimeout(one(), PAGE_MS, p.url); } catch (e) { r = { url: p.url, checks: { http200: false }, verify: { http: 0 }, transport_error: String(e).slice(0, 200) }; }
  if (!r.transport_error && r.verify?.http === 0) r.transport_error = "page fetch failed (http 0)";
  if (!r.transport_error && r.render && (r.render.http === 0 || /net::ERR_|Timeout/i.test(r.render.error || ""))) r.transport_error = "browser: " + (r.render.error || "http 0");
  result.pages.push(r);
  const bad = Object.entries(r.checks).filter(([, x]) => !x).map(([k]) => k);
  console.log(`${bad.length ? "FAIL" : "ok  "} ${p.url}${bad.length ? "  " + bad.join(", ") : ""}`);
}
for (const hub of man.hubs || []) {
  const h = await checkHub(hub, man.pages.filter((p) => p.hub === hub && (HUBS_ONLY || result.pages.find((r) => r.url === p.url)?.checks.http200)));
  if (h.http200) { try { await withTimeout((async () => { h.render = await render(BASE + hub, "hub" + hub.replace(/\//g, "-")); h.link_status = await linkStatuses(h.render.links || []); })(), PAGE_MS * 2, hub); } catch (e) { h.transport_error = String(e).slice(0, 200); } }
  result.hubs.push(h); console.log(`${h.http200 && h.carousel_has_all_new_cards && h.hub_card_cover_alt ? "ok  " : "FAIL"} hub ${hub}`);
}
await browser.close();
fs.mkdirSync(path.dirname(OUT), { recursive: true }); fs.writeFileSync(OUT, JSON.stringify(result));
console.log(`wrote ${OUT}: ${result.pages.length} pages, ${result.hubs.length} hubs`);
process.exit(0);   // the per-page timeout timers (withTimeout) would keep node alive up to --page-timeout after the last page
