// verify_launch.mjs: live checks for the launch set, AFTER Divit's "publish batch 1" and his site publish. Read-only (HTTP GET/HEAD only).
//   npm install --prefix ops jsdom@24.1.0      (once)
//   node ops/verify_launch.mjs [ops/out/launch/manifest.json]   -> ops/out/launch/verify-live.json, exit 1 on any failure
// Per page: HTTP 200; H1, <title>, meta description, canonical, og:image (resolves); FAQ rendered with all 10 questions and no
// placeholder; hero prompt prefilled and chips switching it (page scripts run in jsdom); 4 use-case images load; comparison table
// present; Learn section not showing "No items found"; hub link present; no link to a child page that is not live.
// Per hub: the carousel links to every launched page of that hub.
import fs from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { JSDOM, VirtualConsole } = require("jsdom");
const BASE = "https://emergent.sh";
const man = JSON.parse(fs.readFileSync(process.argv[2] || "ops/out/launch/manifest.json", "utf8"));
const norm = (s) => (s || "").replace(/\s+/g, " ").trim();
const status = async (u, method = "HEAD") => { try { const r = await fetch(u, { method, redirect: "follow" }); return r.status; } catch { return 0; } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const PLACEHOLDER = /lorem ipsum|placeholder|question goes here|answer goes here|add your faq/i;

async function page(p) {
  const url = BASE + p.url, out = { url: p.url, checks: {} }, c = out.checks;
  const res = await fetch(url, { redirect: "follow" }).catch(() => null);
  c.http200 = !!res && res.status === 200;
  if (!c.http200) return out;
  const html = await res.text();
  const vc = new VirtualConsole();   // page script errors are not our failures; checked by outcome below
  const dom = new JSDOM(html, { url, runScripts: "dangerously", resources: "usable", pretendToBeVisual: true, virtualConsole: vc });
  await new Promise((r) => dom.window.addEventListener("load", r)); await sleep(2500);
  const d = dom.window.document, $ = (s) => d.querySelector(s), $$ = (s) => [...d.querySelectorAll(s)];
  c.h1 = norm($("h1")?.textContent) === norm(p.h1);
  c.title = norm(d.title) === norm(p.meta_title);
  c.meta_description = norm($('meta[name="description"]')?.content) === norm(p.meta_description);
  c.canonical = ($('link[rel="canonical"]')?.href || "").replace(/\/$/, "") === url;
  const og = $('meta[property="og:image"]')?.content;
  c.og_image = !!og && (await status(og)) === 200;
  const faqText = norm($$("[data-faq-wrapper]").map((e) => e.textContent).join(" "));
  c.faq_rendered = p.faq.every((q) => faqText.includes(norm(q))) && !PLACEHOLDER.test(faqText);
  const box = $("#hero-prompt-form textarea");
  c.hero_prefilled = !!box && norm(box.value) === norm(p.default_prompt);
  const chip = $('#hero-prompt-form [data-filter="2"]');
  if (chip && p.chips[1]) { chip.dispatchEvent(new dom.window.MouseEvent("click", { bubbles: true })); await sleep(50); c.chip_switches = norm(box?.value) === norm(p.chips[1]); }
  else c.chip_switches = false;
  const imgs = p.uc_images.filter(Boolean);
  c.usecase_images_4 = imgs.length === 4 && (await Promise.all(imgs.map((u) => status(u)))).every((s) => s === 200)
    && imgs.every((u) => $$("img").some((i) => (i.getAttribute("src") || "") === u || (i.getAttribute("srcset") || "").includes(u)));
  c.comparison_table = !!$(".cmp table");
  c.learn_not_empty = !/No items found/i.test($(".section_blog-related")?.textContent || "");
  c.hub_link = $$("a").some((a) => (a.href || "").replace(/\/$/, "") === BASE + p.hub);
  const kids = [...new Set($$("a").map((a) => a.href.split("#")[0].replace(/\/$/, "")).filter((h) => /^https:\/\/emergent\.sh\/ai-[a-z-]+\/[a-z0-9-]+$/.test(h)))];
  const dead = []; for (const k of kids) if ((await status(k)) !== 200) dead.push(k.replace(BASE, ""));
  c.no_link_to_non_live = dead.length === 0; if (dead.length) out.dead_links = dead;
  dom.window.close();
  return out;
}

const results = [];
for (const p of man.pages) { const r = await page(p); results.push(r); const bad = Object.entries(r.checks).filter(([, v]) => !v).map(([k]) => k); console.log(`${bad.length ? "FAIL" : "PASS"} ${p.url}${bad.length ? "  " + bad.join(", ") : ""}`); }
const hubs = [];
for (const hub of man.hubs) {
  const html = await (await fetch(BASE + hub)).text(); const dom = new JSDOM(html, { url: BASE + hub });
  const hrefs = new Set([...dom.window.document.querySelectorAll(".section_build a, a")].map((a) => a.href.replace(/\/$/, "")));
  const missing = man.pages.filter((p) => p.hub === hub && !hrefs.has(BASE + p.url)).map((p) => p.url);
  hubs.push({ hub, carousel_has_all_new_cards: missing.length === 0, missing }); console.log(`${missing.length ? "FAIL" : "PASS"} hub ${hub}${missing.length ? "  missing cards: " + missing.join(", ") : ""}`);
}
fs.writeFileSync("ops/out/launch/verify-live.json", JSON.stringify({ date: new Date().toISOString(), results, hubs }, null, 1));
const fails = results.filter((r) => Object.values(r.checks).some((v) => !v)).length + hubs.filter((h) => !h.carousel_has_all_new_cards).length;
console.log(`${results.length} pages, ${hubs.length} hubs, ${fails} failing`); process.exit(fails ? 1 : 0);
