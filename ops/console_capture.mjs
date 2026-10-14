// console_capture.mjs: error-level console messages and page errors WITH their source (script URL and stack), through a CDP
// session on a Playwright page. Divit 2026-10-14: the console exception (rules/live_audit.json console_ignore_sources) is
// decided on where an error comes from, never on its message text; ops/console_filter.py applies it.
// Used by ops/staging_check.mjs and ops/live_audit.mjs. Read-only.
//   await captureErrors(ctx, pg, sink, { w: 1440 })   before navigation; sink gets {t, src, stack: [urls], kind, ...extra}
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
    sink.push({ ...extra, kind: "log", t: (x.text || "").slice(0, 300), src: x.url || st[0] || "", stack: [x.url, ...st].filter(Boolean).slice(0, 12) });
  });
  await cdp.send("Runtime.enable"); await cdp.send("Log.enable");
  return cdp;
}
