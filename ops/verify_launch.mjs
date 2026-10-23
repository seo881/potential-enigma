// verify_launch.mjs: live checks for the launch set, after a site publish (staging first, then emergent.sh; DECISIONS 2026-10-09).
// Read-only (HTTP GET/HEAD only).
//   npm install --prefix ops jsdom@24.1.0      (once)
//   node ops/verify_launch.mjs [manifest.json] [--base https://<site>.webflow.io]   -> ops/out/launch/verify-live[-staging].json, exit 1 on any failure
// --base defaults to https://emergent.sh. Content links are written as https://emergent.sh/...; on staging they are checked on --base.
// Per page: HTTP 200; H1, <title>, meta description, canonical (always the emergent.sh URL), og:image (resolves; a .webp URL serving
// image/webp, exactly 1200x630, at most 300 KB); FAQ rendered with
// all 10 questions and no placeholder; hero prompt prefilled and chips switching it, still switched 1.2 s later (the older chip script
// does not fight T1; page scripts run in jsdom); first use-case tab
// active on load (T10); 4 use-case images load; comparison table present; Learn section shown with 3 cards whose links return 200
// and not showing "No items found"; hub link present; no link to a child page that is not live; carousel (section_build) shown,
// its cover images with a non-empty alt (T5) and every card link 200 (Divit 2026-10-23).
// Per hub: the carousel is shown, links to every launched page of that hub, every card resolves (200), and covers have alt (T5).
import fs from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { JSDOM, VirtualConsole } = require("jsdom");
// Also a module: ops/live_audit.mjs imports checkPage / checkHub (Layer A reuses these checks).
import { fileURLToPath } from "node:url";
const MAIN = process.argv[1] && fileURLToPath(import.meta.url) === (await import("node:path")).resolve(process.argv[1]);
let BASE = "https://emergent.sh";
const CANON = "https://emergent.sh";
// a page script's rejected promise must not end the run; it is recorded with the page's console errors instead
const strayErrors = []; process.on("unhandledRejection", (e) => strayErrors.push(String(e && (e.stack || e.message || e)).slice(0, 300)));
export const setBase = (b) => { BASE = b.replace(/\/$/, ""); };
export const norm = (s) => (s || "").replace(/\s+/g, " ").trim();
// every request has a 30 s ceiling (2026-10-23: a full serial run hung for 6 hours on requests and jsdom loads that never ended)
export const FETCH_MS = 30000;
export const status = async (u, method = "HEAD") => { try { const r = await fetch(u, { method, redirect: "follow", signal: AbortSignal.timeout(FETCH_MS) }); return r.status; } catch { return 0; } };
// card links (Learn and carousel) repeat on every page of a hub: one probe per URL per run; a transport error (0) gets one GET retry
// and is not cached
const cardCache = new Map();
export async function cardStatus(u) {
  if (cardCache.has(u)) return cardCache.get(u);
  let s = await status(u, "HEAD"); if (s === 405 || s === 403 || s === 0) s = await status(u, "GET");
  if (s === 0) { await sleep(2000); s = await status(u, "GET"); }
  if (s !== 0) cardCache.set(u, s);
  return s;
}
// Divit 2026-10-23: Learn cards and the carousel are shown, and every card carries a real per-item link that resolves (200; Webflow
// serves only published items). Per card (w-dyn-item / role=listitem): its first link must not be empty, "#", the hub root, "/" or a
// template slug (detail_*), must match the expected path (want), and must return 200. Same rules as ops/verify_live.py learn_section.
const TEMPLATE_SLUG = /(^|\/)detail_[^/]*$/;
export const HUB_ROOTS = ["/ai-landing-page-builder", "/ai-form-builder", "/ai-automation-builder", "/ai-survey-and-quiz-builder"];
async function cardLinks(root, want) {
  const items = [...root.querySelectorAll(".w-dyn-item, [role=listitem]")].filter((e, i, A) => !A.some((o) => o !== e && o.contains(e)));
  const hrefs = [], bad = [];
  for (const it of items) {
    const a = it.querySelector("a[href]"), raw = (a?.getAttribute("href") || "").trim();
    const pth = a ? pathOf(a.href.split("#")[0]) : "";
    if (!raw || raw.startsWith("#")) { bad.push(`card without a link (${raw || "empty"})`); continue; }
    if (!pth || pth === "/" || HUB_ROOTS.includes(pth) || TEMPLATE_SLUG.test(pth) || !want.test(pth)) { bad.push(`${raw} (not a per-item link)`); continue; }
    hrefs.push(pth);
  }
  for (const h of [...new Set(hrefs)]) { const st = await cardStatus(BASE + h); if (st !== 200) bad.push(`${h} (${st})`); }
  return { n: items.length, hrefs, bad };
}
const LEARN_PATH = /^\/learn\/[a-z0-9][a-z0-9-]*$/, CHILD_PATH = /^\/ai-[a-z-]+\/[a-z0-9-]+$/;
const shown = (w, el) => !!el && !el.classList.contains("w-condition-invisible") && (!w || w.getComputedStyle(el).display !== "none");
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const PLACEHOLDER = /lorem ipsum|placeholder|question goes here|answer goes here|add your faq/i;
// a link on either host -> its path on this site ("" when it points elsewhere)
export const pathOf = (href) => { try { const u = new URL(href); return [new URL(BASE).host, new URL(CANON).host].includes(u.host) ? u.pathname.replace(/\/$/, "") : ""; } catch { return ""; } };
export const altOk = (img) => norm(img.getAttribute("alt")).length > 0;
// WebP dimensions from the RIFF header (VP8, VP8L or VP8X chunk)
export const webpSize = (b) => {
  if (b.length < 30 || b.toString("ascii", 0, 4) !== "RIFF" || b.toString("ascii", 8, 12) !== "WEBP") return null;
  const c = b.toString("ascii", 12, 16);
  if (c === "VP8 ") return [b.readUInt16LE(26) & 0x3fff, b.readUInt16LE(28) & 0x3fff];
  if (c === "VP8L") { const n = b.readUInt32LE(21); return [(n & 0x3fff) + 1, ((n >> 14) & 0x3fff) + 1]; }
  if (c === "VP8X") return [1 + b.readUIntLE(24, 3), 1 + b.readUIntLE(27, 3)];
  return null;
};
// share image (DECISIONS 2026-10-09): WebP, 200 with content-type image/webp, exactly 1200x630, at most 300 KB
export async function ogWebp(u) {
  const o = { url: u };
  try {
    const r = await fetch(u, { redirect: "follow" }); const b = Buffer.from(await r.arrayBuffer());
    Object.assign(o, { status: r.status, type: (r.headers.get("content-type") || "").split(";")[0].trim(), bytes: b.length, size: webpSize(b) });
  } catch (e) { o.error = String(e); }
  o.ok = /\.webp(\?|$)/i.test(new URL(u).pathname) && o.status === 200 && o.type === "image/webp"
    && !!o.size && o.size[0] === 1200 && o.size[1] === 630 && o.bytes <= 300 * 1024;
  return o;
}
const coverImgs = (root) => [...root.querySelectorAll("img")].filter((i) => /cover/.test(i.className));

// One page. opts.keepDom: return the live jsdom window as out.dom (caller closes it).
export async function checkPage(p, opts = {}) {
  const url = BASE + p.url, out = { url: p.url, checks: {} }, c = out.checks;
  const res = await fetch(url, { redirect: "follow", signal: AbortSignal.timeout(FETCH_MS) }).catch(() => null);
  out.http = res ? res.status : 0;   // 0 = transport error (timeout, DNS, reset): the run re-checks the page
  c.http200 = !!res && res.status === 200;
  if (!c.http200) return out;
  const html = await res.text().catch(() => null);
  if (html === null) { c.http200 = false; out.http = 0; return out; }
  out.html = html;
  const vc = new VirtualConsole(), errs = [];   // console errors: the site's own known noise is ignored (rules/live_audit.json verify_launch_console_ignore: jsdom only, no error sources)
  vc.on("jsdomError", (e) => errs.push(String(e && (e.message || e)))); vc.on("error", (...a) => errs.push(a.map(String).join(" ")));
  const dom = new JSDOM(html, { url, runScripts: "dangerously", resources: "usable", pretendToBeVisual: true, virtualConsole: vc,
    beforeParse(w) {   // jsdom has no CSS global; Webflow's interactions script calls CSS.escape (a jsdom gap, not a page error)
      if (!w.CSS) w.CSS = { escape: (s) => String(s).replace(/[^a-zA-Z0-9_\u00A0-\uFFFF-]/g, (ch) => "\\" + ch), supports: () => false };
    } });
  // a page resource that never finishes would keep "load" from firing forever: wait at most 45 s, then check what rendered
  await Promise.race([new Promise((r) => dom.window.addEventListener("load", r)), sleep(45000)]); await sleep(2500);
  const d = dom.window.document, $ = (s) => d.querySelector(s), $$ = (s) => [...d.querySelectorAll(s)];
  c.h1 = norm($("h1")?.textContent) === norm(p.h1);
  c.title = norm(d.title) === norm(p.meta_title);
  c.meta_description = norm($('meta[name="description"]')?.content) === norm(p.meta_description);
  c.canonical = ($('link[rel="canonical"]')?.getAttribute("href") || "").replace(/\/$/, "") === CANON + p.url;
  const og = $('meta[property="og:image"]')?.content;
  c.og_image = !!og && (await status(og)) === 200;
  if (og) { out.og = await ogWebp(new URL(og, url).href); c.og_webp = out.og.ok; } else c.og_webp = false;
  const faqText = norm($$("[data-faq-wrapper]").map((e) => e.textContent).join(" "));
  c.faq_rendered = p.faq.every((q) => faqText.includes(norm(q))) && !PLACEHOLDER.test(faqText);
  const box = $("#hero-prompt-form textarea");
  c.hero_prefilled = !!box && norm(box.value) === norm(p.default_prompt);
  // hero chips (Divit 2026-10-09): each chip appends its "add" clause in chip order and removes it on a second click; typed text survives;
  // aria-pressed and hubchip--on follow the state; the older chip script does not overwrite the box afterwards
  const adds = (p.chips || []).map((x) => (x && typeof x === "object" ? x.add : x));
  const chipEl = (n) => $(`#hero-prompt-form [data-hubchip="${n}"]`) || $(`#hero-prompt-form [data-filter="${n}"]`);
  const click = async (n) => { chipEl(n)?.dispatchEvent(new dom.window.MouseEvent("click", { bubbles: true, cancelable: true })); await sleep(60); };
  if (box && adds.length === 4 && [1, 2, 3, 4].every((n) => chipEl(n))) {
    let ok = true;
    for (let n = 1; n <= 4; n++) { await click(n); ok = ok && norm(box.value) === norm([p.default_prompt, ...adds.slice(0, n)].join(" ")); }
    c.chip_adds_in_order = ok;
    c.chip_state = [1, 2, 3, 4].every((n) => chipEl(n).getAttribute("aria-pressed") === "true" && chipEl(n).classList.contains("hubchip--on"))
      && !!$("#hero-prompt-form [data-hubchip]");
    await sleep(1200); c.chip_stable = norm(box.value) === norm([p.default_prompt, ...adds].join(" "));
    ok = true;
    for (let n = 1; n <= 4; n++) { await click(n); ok = ok && norm(box.value) === norm([p.default_prompt, ...adds.slice(n)].join(" ")) && chipEl(n).getAttribute("aria-pressed") === "false" && !chipEl(n).classList.contains("hubchip--on"); }
    c.chip_removes = ok;
    box.value = "My own words."; await click(2); const kept = norm(box.value) === norm("My own words. " + adds[1]); await click(2);
    c.typed_text_survives = kept && norm(box.value) === "My own words.";
    out.chip_after = norm(box.value).slice(0, 80);
  } else { c.chip_adds_in_order = c.chip_state = c.chip_stable = c.chip_removes = c.typed_text_survives = false; }
  // T10: the use-case tab whose label is tab_label_1 is the current tab, and its pane is the active one
  const links = $$(".w-tab-link"), first = links.find((a) => norm(a.textContent) === norm(p.tab_labels?.[0]));
  const pane = first && $$(".w-tab-pane").find((x) => x.getAttribute("data-w-tab") === first.getAttribute("data-w-tab"));
  c.first_tab_active = !!first && first.classList.contains("w--current") && !!pane && pane.classList.contains("w--tab-active")
    && !links.some((a) => a !== first && a.parentElement === first.parentElement && a.classList.contains("w--current"));
  const imgs = p.uc_images.filter(Boolean);
  c.usecase_images_4 = imgs.length === 4 && (await Promise.all(imgs.map((u) => status(u)))).every((s) => s === 200)
    && imgs.every((u) => $$("img").some((i) => (i.getAttribute("src") || "") === u || (i.getAttribute("srcset") || "").includes(u)));
  c.comparison_table = !!$(".cmp table");
  c.learn_not_empty = !/No items found/i.test($(".section_blog-related")?.textContent || "");
  // Learn list (Divit 2026-10-23; supersedes the 2026-10-09 launch state): shown on every child page with 3 published Learn
  // references (DECISIONS 2026-10-15/16), and every card link resolves
  const learn = $(".section_blog-related"), nLearn = learn ? learn.querySelectorAll(".w-dyn-item").length : 0;
  // learn_cards_3: the section is shown with exactly 3 cards and no "No items found"; learn_cards_resolve: each card links to its own
  // /learn/<slug> article and that link returns 200
  const L = learn ? await cardLinks(learn, LEARN_PATH) : { n: 0, hrefs: [], bad: ["Learn section not on the page"] };
  c.learn_cards_3 = shown(dom.window, learn) && L.n === 3 && !/No items found/i.test(learn.textContent);
  c.learn_cards_resolve = L.n > 0 && L.bad.length === 0;
  out.learn_items = L.n; out.learn_links = L.hrefs; if (L.bad.length) out.learn_bad = L.bad;
  // D1/D2 copy live
  const bodyText = norm(d.body.textContent);
  if (p.hero_description) c.hero_description_live = bodyText.includes(norm(p.hero_description));
  if (p.howto_description) c.howto_description_live = bodyText.includes(norm(p.howto_description));
  c.hub_link = $$("a").some((a) => pathOf(a.href) === p.hub);
  const kids = [...new Set($$("a").map((a) => pathOf(a.href.split("#")[0])).filter((h) => /^\/ai-[a-z-]+\/[a-z0-9-]+$/.test(h)))];
  const dead = []; for (const k of kids) if ((await status(BASE + k)) !== 200) dead.push(k);
  c.no_link_to_non_live = dead.length === 0; if (dead.length) out.dead_links = dead;
  // T5: the carousel on the child template (section_build, made visible by T6) shows covers with alt text
  const build = $(".section_build"), covers = build ? coverImgs(build) : [];
  if (build) {   // only while the carousel is shown (hidden until Monday's rework, Divit 2026-10-09)
    c.carousel_cover_alt = covers.length > 0 && covers.every(altOk);
    if (!c.carousel_cover_alt) out.cover_alt = `${covers.filter((i) => !altOk(i)).length} of ${covers.length} cover images without alt`;
  }
  // carousel shown (Divit 2026-10-23; supersedes the 2026-10-09 "carousel hidden" check), and every card links to a page that returns 200
  // carousel_visible: section_build is rendered and displayed; carousel_cards_resolve: every carousel card has a per-item child-page link
  // (not "#", empty or the hub root) that returns 200
  const sb = $(".section_build"); c.carousel_visible = shown(dom.window, sb);
  const K = sb ? await cardLinks(sb, CHILD_PATH) : { n: 0, hrefs: [], bad: ["carousel not on the page"] };
  c.carousel_cards_resolve = K.n > 0 && K.bad.length === 0; out.carousel_cards = K.n; if (K.bad.length) out.carousel_bad = K.bad;
  const IGN = JSON.parse(fs.readFileSync(new URL("../rules/live_audit.json", import.meta.url), "utf8")).verify_launch_console_ignore || [];
  out.console_errors = errs.filter((e) => !IGN.some((s) => e.includes(s))).slice(0, 10); c.no_console_errors = out.console_errors.length === 0;
  if (opts.keepDom) out.dom = dom; else dom.window.close();
  return out;
}

// One hub page: its carousel links to every given page and those cards' covers have alt text.
export async function checkHub(hub, mine) {
  let res = null; for (let a = 0; a < 3 && !(res && res.ok); a++) { res = await fetch(BASE + hub, { signal: AbortSignal.timeout(FETCH_MS) }).catch(() => null); if (!(res && res.ok)) await sleep(2000 * (a + 1)); }
  const html = res && res.ok ? await res.text().catch(() => "") : "";
  const d = new JSDOM(html, { url: BASE + hub }).window.document;
  const anchors = [...d.querySelectorAll("a")];
  const missing = mine.filter((p) => !anchors.some((a) => pathOf(a.href) === p.url)).map((p) => p.url);
  const noAlt = [];
  for (const p of mine) for (const a of anchors.filter((a) => pathOf(a.href) === p.url)) {
    let card = a; for (let i = 0; i < 6 && card && !card.querySelector("img"); i++) card = card.parentElement;   // the card around the link
    const im = card ? [...card.querySelectorAll("img")] : [], cov = im.filter((i) => /cover/.test(i.className));
    if (!(cov.length ? cov : im).every(altOk) || !im.length) noAlt.push(p.url);
  }
  // hub carousel (Divit 2026-10-23): shown, and every card resolves (200)
  const sb = d.querySelector(".section_build");
  const K = sb ? await cardLinks(sb, CHILD_PATH) : { n: 0, hrefs: [], bad: ["carousel not on the hub"] };
  return { hub, http200: !!res && res.status === 200, carousel_visible: shown(null, sb), carousel_cards: K.n, carousel_cards_resolve: K.n > 0 && K.bad.length === 0, carousel_bad: K.bad, carousel_has_all_new_cards: missing.length === 0, missing, hub_card_cover_alt: noAlt.length === 0, cover_alt_missing: [...new Set(noAlt)] };
}

if (MAIN) {
const argv = process.argv.slice(2), bi = argv.indexOf("--base");
if (bi >= 0) setBase(argv.splice(bi, 2)[1]);
const STAGING = BASE !== CANON;
const man = JSON.parse(fs.readFileSync(argv[0] || "ops/out/launch/manifest.json", "utf8"));
const results = [];
for (const p of man.pages) { const r = await checkPage(p); delete r.html; results.push(r); const bad = Object.entries(r.checks).filter(([, v]) => !v).map(([k]) => k); console.log(`${bad.length ? "FAIL" : "PASS"} ${p.url}${bad.length ? "  " + bad.join(", ") : ""}${r.cover_alt ? "  (" + r.cover_alt + ")" : ""}${r.og && !r.og.ok ? "  (og: " + [r.og.status, r.og.type, r.og.size && r.og.size.join("x"), r.og.bytes + " B"].join(", ") + ")" : ""}`); }
// one line per child template (the carousel is template markup, so every page of a hub shows the same result)
const templates = man.hubs.map((hub) => { const rs = results.filter((r) => man.pages.find((p) => p.url === r.url).hub === hub && r.checks.http200);
  return { hub, template_cover_alt: rs.length > 0 && rs.every((r) => r.checks.carousel_cover_alt !== false), pages_checked: rs.length }; });
for (const t of templates) console.log(`${t.template_cover_alt ? "PASS" : "FAIL"} template cards ${t.hub}: cover alt (${t.pages_checked} pages)`);
const hubs = [];
for (const hub of man.hubs) {
  const h = await checkHub(hub, man.pages.filter((p) => p.hub === hub));
  hubs.push(h);
  const bad = ["http200", "carousel_visible", "carousel_cards_resolve"].filter((k) => !h[k]);   // carousel shown, cards resolve (Divit 2026-10-23)
  console.log(`${bad.length ? "FAIL" : "PASS"} hub ${hub}${bad.length ? "  " + bad.join(", ") : ""}${h.missing.length ? "  missing cards: " + h.missing.join(", ") : ""}${h.cover_alt_missing.length ? "  no cover alt: " + h.cover_alt_missing.join(", ") : ""}`);
}
// one page outside our 4 collections must be unchanged on staging (same visible text as production, none of our code on it)
const OUT_URL = JSON.parse(fs.readFileSync(new URL("../rules/live_audit.json", import.meta.url), "utf8")).outside_check;
const outside = { url: OUT_URL };
if (OUT_URL && STAGING) {
  const get = async (b) => { const r = await fetch(b + OUT_URL).catch(() => null); return r && r.ok ? await r.text() : ""; };
  const [sh, ph] = [await get(BASE), await get(CANON)];
  // production sits behind Cloudflare email obfuscation ("[email protected]"); staging shows the address: both read as EMAIL (per text node)
  const txt = (h) => { const w = new JSDOM(h).window; const d = w.document; d.querySelectorAll("script,style,noscript").forEach((e) => e.remove());
    const it = d.createTreeWalker(d.body || d, w.NodeFilter.SHOW_TEXT); for (let n = it.nextNode(); n; n = it.nextNode()) n.nodeValue = n.nodeValue.replace(/\[email\s*protected\]|[\w.+-]+@[\w-]+(\.[\w-]+)+/g, "EMAIL");
    return norm(d.body?.textContent); };
  outside.ok = !!sh && !!ph && txt(sh) === txt(ph) && !/data-hubchip|hubchip--on|Hero prompt \(Divit/.test(sh);
  console.log(`${outside.ok ? "PASS" : "FAIL"} outside page ${OUT_URL} unchanged on staging`);
}
fs.writeFileSync(`ops/out/launch/verify-live${STAGING ? "-staging" : ""}.json`, JSON.stringify({ date: new Date().toISOString(), base: BASE, results, templates, hubs, outside }, null, 1));
const fails = results.filter((r) => Object.values(r.checks).some((v) => !v)).length + templates.filter((t) => !t.template_cover_alt).length
  + hubs.filter((h) => !h.http200 || !h.carousel_visible || !h.carousel_cards_resolve).length + (outside.ok === false ? 1 : 0);
console.log(`${BASE}: ${results.length} pages, ${templates.length} templates, ${hubs.length} hubs, ${fails} failing`); process.exit(fails ? 1 : 0);
}
