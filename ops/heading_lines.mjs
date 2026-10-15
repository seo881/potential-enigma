// heading_lines.mjs: read-only proof for the carousel heading orphan fix (B-dev-14, 2026-10-15).
// Loads each staging page, measures the rendered lines of the carousel heading `.section_build h2.text-align-center` at 390, 768 and 1440 px in Chromium and
// WebKit, and exits 1 when any heading ends on a single-word line. No Webflow API or MCP call.
//   node ops/heading_lines.mjs                                  the Form hub and one Form template page on staging
//   node ops/heading_lines.mjs --base https://emergent-sh.webflow.io /ai-form-builder /ai-landing-page-builder
//   --css '<rules>' injects candidate CSS into every page after load (local test of a head-code change, nothing written)
//   node ops/heading_lines.mjs --all [--json out.json]           every visible h1/h2/h3 on the 4 hubs and one child per
//       template (or the paths given), each tagged by owner: run (carousel, Learn, hub FAQ: set in logs/templates.md),
//       cms (template heading whose text differs on a second child page: our CMS fields), static (template/shared text)
// WebKit needs `npx playwright install webkit` once (run from ops/).
import { chromium, webkit } from 'playwright';

const args = process.argv.slice(2);
let base = 'https://emergent-sh.webflow.io';
const bi = args.indexOf('--base');
if (bi >= 0) { base = args[bi + 1].replace(/\/$/, ''); args.splice(bi, 2); }
const ALL = args.includes('--all'); if (ALL) args.splice(args.indexOf('--all'), 1);
let css = null; const ci = args.indexOf('--css'); if (ci >= 0) { css = args[ci + 1]; args.splice(ci, 2); }
let jsonOut = null; const ji = args.indexOf('--json'); if (ji >= 0) { jsonOut = args[ji + 1]; args.splice(ji, 2); }
// representative child per template, and a second child used only to tell CMS-bound headings from static text
const SECOND = { '/ai-form-builder/contact-form': '/ai-form-builder/ach-form',
  '/ai-landing-page-builder/affiliate-landing-page': '/ai-landing-page-builder/app-landing-page',
  '/ai-automation-builder/accounting-automation': '/ai-automation-builder/accounts-payable-automation',
  '/ai-survey-and-quiz-builder/360-survey': '/ai-survey-and-quiz-builder/brand-awareness-survey' };
const paths = args.length ? args : ALL
  ? ['/ai-form-builder', '/ai-landing-page-builder', '/ai-automation-builder', '/ai-survey-and-quiz-builder', ...Object.keys(SECOND)]
  : ['/ai-form-builder', '/ai-form-builder/contact-form'];
const SEL = ALL ? 'h1, h2, h3' : '.section_build h2.text-align-center';
const RUN_SECTIONS = ['section_build', 'section_blog-related', 'section_faq2'];
const WIDTHS = [390, 768, 1440];

const measure = (sel) => [...document.querySelectorAll(sel)].filter(h => h.getClientRects().length && h.offsetWidth > 0
    && getComputedStyle(h).visibility !== 'hidden').map((h, i, all) => {
  const sec = h.closest('section, nav, header, footer, .w-nav');
  const section = sec ? (sec.className && String(sec.className).split(' ')[0]) || sec.tagName.toLowerCase() : 'none';
  const lines = [];
  const tw = document.createTreeWalker(h, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = tw.nextNode())) {
    const re = /\S+/g; let m;
    while ((m = re.exec(n.data))) {
      const r = document.createRange(); r.setStart(n, m.index); r.setEnd(n, m.index + m[0].length);
      // WebKit puts a zero-width rect on the previous line for a word right after a pre-line newline: use the widest rect
      const rc = [...r.getClientRects()].filter(x => x.width > 0).sort((a, b) => b.width - a.width); if (!rc.length) continue;
      const top = Math.round(rc[0].top);
      let L = lines.find(l => Math.abs(l.top - top) < 4);
      if (!L) lines.push(L = { top, w: [] });
      L.w.push(m[0]);
    }
  }
  const idx = all.filter(x => x.closest('section, nav, header, footer, .w-nav') === sec).indexOf(h);
  return { tag: h.tagName.toLowerCase(), section, idx, text: h.textContent.replace(/\s+/g, ' ').trim(),
    lines: lines.sort((a, b) => a.top - b.top).map(l => l.w.join(' ')) };
});
const isTemplate = (p) => p.split('/').filter(Boolean).length > 1;

let fail = 0;
const rows = [];
const second = {};
for (const [name, type] of [['chromium', chromium], ['webkit', webkit]]) {
  let browser;
  try { browser = await type.launch(); } catch (e) { console.log(`${name}: not installed, skipped`); continue; }
  for (const p of paths) {
    if (ALL && isTemplate(p) && SECOND[p] && !second[p]) {
      const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
      const page = await ctx.newPage();
      await page.goto(base + SECOND[p], { waitUntil: 'load', timeout: 60000 });
      second[p] = new Set((await page.evaluate(measure, SEL)).map(h => `${h.section}|${h.idx}|${h.text}`));
      await ctx.close();
    }
    for (const w of WIDTHS) {
      const ctx = await browser.newContext({ viewport: { width: w, height: 900 } });
      const page = await ctx.newPage();
      let res;
      try { res = await page.goto(base + p, { waitUntil: 'load', timeout: 60000 }); }
      catch (e) { console.log(`FAIL ${name} ${p} ${w}: load error ${e.message.split('\n')[0]}`); fail++; await ctx.close(); continue; }
      await page.evaluate(() => document.fonts.ready);
      if (ALL) await page.waitForTimeout(3000);   // hero H1s reveal word by word; measure after the animation settles
      if (css) { await page.addStyleTag({ content: css }); await page.waitForTimeout(100); }
      const heads = await page.evaluate(measure, SEL);
      if (!heads.length) { console.log(`FAIL ${name} ${p} ${w}: no ${SEL} (HTTP ${res && res.status()})`); fail++; }
      for (const h of heads) {
        const { lines } = h;
        const orphan = lines.length > 1 && lines[lines.length - 1].split(' ').length === 1;
        const owner = RUN_SECTIONS.includes(h.section) ? 'run'
          : (second[p] && !second[p].has(`${h.section}|${h.idx}|${h.text}`)) ? 'cms' : 'static';
        rows.push({ browser: name, path: p, width: w, owner, ...h, orphan });
        if (orphan) fail++;
        if (ALL && !orphan) continue;
        console.log(`${orphan ? 'FAIL' : 'ok  '} ${name} ${p} ${w}${ALL ? ` ${owner} ${h.tag} ${h.section}` : ''}: ${lines.map(l => `"${l}"`).join(' / ')}`);
      }
      await ctx.close();
    }
  }
  await browser.close();
}
if (jsonOut) { const fs = await import('fs'); fs.writeFileSync(jsonOut, JSON.stringify(rows, null, 1)); }
console.log(fail ? `${fail} failure(s): single-word last line or load error` : 'no single-word last line');
process.exit(fail ? 1 : 0);
