// logic.mjs: run the quiz embed's own validate() and score() in node (golden kinds quiz-js and quiz-agree, tests/golden/run.py).
//   node ops/quiz/logic.mjs CASE.json   CASE = {"quiz": {...}, "answers": [option index per question] (optional)}
// Prints {"error": "" | "<why the embed would render nothing>", "result": {key, points, of} | null}. The code is extracted from
// ops/quiz/embed.min.html (what ships), so the test runs exactly the shipped logic.
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..", "..");
const html = fs.readFileSync(path.join(ROOT, "ops", "quiz", "embed.min.html"), "utf8");
const src = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const sandbox = { module: { exports: null }, console };
vm.runInNewContext(src, sandbox);
const api = sandbox.module.exports;
const c = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const error = api.validate(c.quiz);
const result = !error && Array.isArray(c.answers) ? api.score(c.quiz, c.answers) : null;
process.stdout.write(JSON.stringify({ error, result: result && { key: result.key, points: result.points, of: result.of } }));
