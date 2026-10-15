// console_capture.mjs: error-level console messages and page errors WITH their source (script URL and stack), through a CDP
// session on a Playwright page. Divit 2026-10-14: the console exception (rules/live_audit.json console_ignore_sources) is
// decided on where an error comes from, never on its message text; ops/console_filter.py applies it.
// Used by ops/staging_check.mjs and ops/live_audit.mjs. Read-only.
//   await captureErrors(ctx, pg, sink, { w: 1440 })   before navigation; sink gets {t, src, stack: [urls], kind, ...extra}
//   await tieElements(pg, sink, from)                 at the end (each document is also tied on its own load): marks errors the page document itself reported (doc: true) and
//                                                      ties a markup error (e.g. <svg> attribute width) to its element (element:
//                                                      {tag, attr, value, nav, href, link_class}); the navbar <svg width="2o"> exception
//                                                      (Divit 2026-10-15) is decided on that element, never on the message.
const frames = (st) => ((st && st.callFrames) || []).map((f) => f.url).filter(Boolean);
const argText = (a) => (a.value !== undefined ? String(a.value) : a.description || a.unserializableValue || a.type || "");

export async function captureErrors(ctx, pg, sink, extra = {}) {
  const cdp = await ctx.newCDPSession(pg);
  cdp.on("Runtime.consoleAPICalled", (e) => {
    if (e.type !== "error" && e.type !== "assert") return;
    const st = frames(e.stackTrace);
    sink.push({ ...extra, kind: "console", t: e.args.map(argText).join(" ").slice(0, 300), src: st[0] || "", stack: st.slice(0, 12) });
  });
  cdp.on("Runtime.exceptionThrown", (e) => {
    const d = e.exceptionDetails || {}, st = frames(d.stackTrace);
    const text = (d.exception && (d.exception.description || d.exception.value)) || d.text || "exception";
    sink.push({ ...extra, kind: "pageerror", t: ("pageerror: " + text).slice(0, 300), src: d.url || st[0] || "", stack: [d.url, ...st].filter(Boolean).slice(0, 12) });
  });
  cdp.on("Log.entryAdded", (e) => {   // browser-side errors (failed resource loads, CSP, intervention): the URL is the source
    const x = e.entry || {}; if (x.level !== "error") return;
    const st = frames(x.stackTrace);
    sink.push({ ...extra, kind: "log", source: x.source || "", line: x.lineNumber ?? null, t: (x.text || "").slice(0, 300), src: x.url || st[0] || "", stack: [x.url, ...st].filter(Boolean).slice(0, 12) });
  });
  await cdp.send("Runtime.enable"); await cdp.send("Log.enable");
  autoTie(pg, sink);
  return cdp;
}

// Elements carrying an attribute value, in DOM order, with where they sit (navbar or not, the link around them), plus the
// document they were read from (the caller checks it is the one that reported the error).
function elementsWith(q) {
  const els = [...document.getElementsByTagName(q.tag)].filter((e) => e.getAttribute(q.attr) === q.value).map((e) => {
    const a = e.closest("a[href]");
    return { tag: e.localName, attr: q.attr, value: q.value, href: a ? a.getAttribute("href") : null, link_class: a ? a.className : null,
      nav: !!e.closest('nav, [role="navigation"], .w-nav, [class^="nav_"], [class*=" nav_"], [class^="navbar"], [class*=" navbar"]') };
  });
  return { doc: location.href, els };
}
const strip = (u) => String(u || "").split("#")[0];
const isScript = (u) => /\.m?js([?#]|$)/.test(u || "");
const MARKUP = /<([a-zA-Z][\w-]*)> attribute ([\w:-]+): [^"]*"([^"]*)"/;
const pending = new WeakMap();   // pg -> the tie running for the document that just loaded

// Ties the errors the CURRENT document reported (B-dev-9, 2026-10-15): a markup error can only be tied while its document is
// still open. Run on every main-frame load (captureErrors) so the first load is tied before a later navigation (load more ->
// ?xxxx_page=2, a css reload) replaces it; a lookup that lands in another document ties nothing.
async function tieDoc(pg, sink, from) {
  const doc = strip(pg.url()), todo = [];
  for (const e of sink.slice(from)) {
    if (e.kind !== "log" || e.doc !== undefined || strip(e.src) !== doc) continue;
    e.doc = !(e.stack || []).some(isScript);
    // the message only says which element to look up (tag, attribute, value); whether the error is excepted is decided on that element
    const m = e.doc && !e.element && MARKUP.exec(e.t || "");
    if (m) todo.push([e, { tag: m[1], attr: m[2], value: m[3] }]);
  }
  const used = new Map();   // the i-th error of a kind from this document load goes to the i-th such element
  for (const [e, q] of todo) {
    const key = JSON.stringify(q);
    const r = await pg.evaluate(elementsWith, q).catch(() => null);
    if (!r || strip(r.doc) !== doc) { e.doc = false; continue; }   // the document went away: not tied, so it counts
    const i = used.get(key) || 0;
    if (r.els.length) { e.element = r.els[Math.min(i, r.els.length - 1)]; used.set(key, i + 1); }
  }
}

export function autoTie(pg, sink) {   // called by captureErrors: tie each document as soon as it has loaded
  pg.on("load", () => {
    const prev = pending.get(pg) || Promise.resolve();
    pending.set(pg, prev.then(() => new Promise((r) => setTimeout(r, 250))).then(() => tieDoc(pg, sink, 0)).catch(() => {}));
  });
}

export async function tieElements(pg, sink, from = 0) {
  await (pending.get(pg) || Promise.resolve());
  await tieDoc(pg, sink, from).catch(() => {});
  for (const e of sink.slice(from)) if (e.kind === "log" && e.doc === undefined) e.doc = false;   // a document never tied: counts
}
