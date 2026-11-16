// Golden fixture (B-audit-1 2026-11-16): does a node process that imports ops/verify_launch.mjs survive the jsdom unbound-postMessage error?
// argv[2] = "unbound": a page script calls window.postMessage unbound, so jsdom's queued node timer throws on `this` = undefined
// (the live shard crash of 11-13..11-16);
// argv[2] = "other": an unrelated uncaught TypeError, which must still end the process with status 1.
// Prints {"survived": true} when the process is still alive 300 ms later.
import { createRequire } from "node:module";
import "../../../../ops/verify_launch.mjs";
const require = createRequire(new URL("../../../../ops/verify_launch.mjs", import.meta.url));   // jsdom lives in ops/node_modules
const { JSDOM, VirtualConsole } = require("jsdom");
const mode = process.argv[2] || "unbound";
if (mode === "unbound") {
  const dom = new JSDOM(`<script>var pm = window.postMessage; pm("x", "*");</script>`, { url: "https://example.test/", runScripts: "dangerously", virtualConsole: new VirtualConsole() });
} else {
  setTimeout(() => { null.boom; }, 10);
}
setTimeout(() => { console.log(JSON.stringify({ survived: true })); process.exit(0); }, 300);
