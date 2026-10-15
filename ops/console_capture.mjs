// console_capture.mjs: error-level console messages and page errors WITH their source (script URL and stack), through a CDP
// session on a Playwright page. Divit 2026-10-14: the console exception (rules/live_audit.json console_ignore_sources) is
// decided on where an error comes from, never on its message text; ops/console_filter.py applies it.
// Used by ops/staging_check.mjs and ops/live_audit.mjs. Read-only.
//   await captureErrors(ctx, pg, sink, { w: 1440 })   before navigation; sink gets {t, src, stack: [urls], kind, ...extra}
//   await tieElements(pg, sink, from)                 after load: marks errors the page document itself reported (doc: true) and
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
  return cdp;
}

// Elements carrying an attribute value, in DOM order, with where they sit (navbar or not, the link around them).
function elementsWith(q) {
  return [...document.getElementsByTagName(q.tag)].filter((e) => e.getAttribute(q.attr) === q.value).map((e) => {
    const a = e.closest("a[href]");
    return { tag: e.localName, attr: q.attr, value: q.value, href: a ? a.getAttribute("href") : null, link_class: a ? a.className : null,
      nav: !!e.closest('nav, [role="navigation"], .w-nav, [class^="nav_"], [class*=" nav_"], [class^="navbar"], [class*=" navbar"]') };
  });
}
const strip = (u) => String(u || "").split("#")[0];
const isScript = (u) => /\.m?js([?#]|$)/.test(u || "");

export async function tieElements(pg, sink, from = 0) {
  const doc = strip(pg.url()), todo = [];
  for (const e of sink.slice(from)) {
    if (e.kind !== "log") continue;
    e.doc = strip(e.src) === doc && !(e.stack || []).some(isScript);
    // the message only says which element to look up (tag, attribute, value); whether the error is excepted is decided on that element
    const m = e.doc && !e.element && /<([a-zA-Z][\w-]*)> attribute ([\w:-]+): [^"]*"([^"]*)"/.exec(e.t || "");
    if (m) todo.push([e, { tag: m[1], attr: m[2], value: m[3] }]);
  }
  const used = new Map();
  for (const [e, q] of todo) {
    const key = JSON.stringify(q);
    const els = await pg.evaluate(elementsWith, q).catch(() => []);
    const i = used.get(key) || 0;
    if (els.length) { e.element = els[Math.min(i, els.length - 1)]; used.set(key, i + 1); }
  }
}
