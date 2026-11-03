// Golden helper (Divit 2026-11-03, B-dev-21): ops/verify_launch.mjs statusRetry against a local HTTP server that answers a scripted
// sequence. Offline, read-only. Each answer is a status code, or "reset" (the socket is destroyed: a transport error, status 0).
//   EMG_RETRY_MS=10,20,40 node status_retry.mjs '["reset", 503, 200]'   -> {"status": 200, "requests": 3}
import http from "node:http";
const script = JSON.parse(process.argv[2]); let n = 0;
const srv = http.createServer((req, res) => {
  const a = script[Math.min(n, script.length - 1)]; n++;
  if (a === "reset") { req.socket.destroy(); return; }
  res.writeHead(a, { "content-type": "text/plain", connection: "close" }); res.end(String(a));
});
await new Promise((r) => srv.listen(0, "127.0.0.1", r));
const { statusRetry } = await import("../../../../ops/verify_launch.mjs");
const s = await statusRetry(`http://127.0.0.1:${srv.address().port}/x`, process.argv[3] || "HEAD");
srv.close(); console.log(JSON.stringify({ status: s, requests: n })); process.exit(0);
