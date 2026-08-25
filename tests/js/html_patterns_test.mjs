// Every `pattern="..."` in every template must compile as a JavaScript
// regular expression under the `v` flag, because that is how browsers
// compile it (HTML spec: the pattern is compiled with `v` since the
// unicodeSets proposal landed).
//
// This exists because of a real one. Three account forms carried
// `pattern="[a-z0-9-]{3,32}"`, which is a perfectly good regex under `u`
// and throws under `v` — a lone `-` inside a character class is reserved
// there. A pattern that throws is not a pattern that rejects: the browser
// discards it and validates nothing, silently. The forms looked validated,
// logged "Invalid regular expression" to a console nobody had open, and
// let anything through to the server.
//
// It was only ever a UX bug — accounts.USERNAME_RE still rejects the same
// input server-side, so nothing invalid was ever stored — but it is the
// exact shape of mistake no Python test can see and no human notices,
// since the failure mode is a validation that quietly stops happening.
//
// Run via `node tests/js/html_patterns_test.mjs`; wired into pytest by
// test_tree_logic_js.py, which skips gracefully when node is absent.
import assert from "node:assert/strict";
import { readdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const TEMPLATES = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "app", "templates");

const PATTERN_RE = /\spattern="([^"]*)"/g;

function patternsInTemplates() {
  const found = [];
  for (const name of readdirSync(TEMPLATES).filter((f) => f.endsWith(".html"))) {
    const source = readFileSync(join(TEMPLATES, name), "utf8");
    for (const [, pattern] of source.matchAll(PATTERN_RE)) {
      found.push({ file: name, pattern });
    }
  }
  return found;
}

let passed = 0;
function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

const patterns = patternsInTemplates();

check("the scanner still finds the patterns at all", () => {
  // A guard on the guard: if the regex above stops matching, every test
  // below passes vacuously and the next broken pattern ships.
  assert.ok(patterns.length >= 4,
    `only found ${patterns.length} pattern attributes — has the scanner broken?`);
});

check("every pattern compiles the way a browser compiles it", () => {
  const broken = [];
  for (const { file, pattern } of patterns) {
    try {
      // Exactly what the HTML spec says to build: anchored, `v` flag.
      new RegExp(`^(?:${pattern})$`, "v");
    } catch (error) {
      broken.push(`${file}: pattern="${pattern}" -> ${error.message}`);
    }
  }
  assert.deepEqual(broken, [],
    "these patterns throw under `v`, so the browser ignores them and " +
    "validates nothing:\n  " + broken.join("\n  "));
});

check("the username pattern actually rejects a bad username", () => {
  // Compiling is necessary, not sufficient — check it still means what it
  // was written to mean.
  const username = patterns.find((p) => p.pattern.includes("3,32"));
  assert.ok(username, "no username pattern found");
  const re = new RegExp(`^(?:${username.pattern})$`, "v");
  assert.equal(re.test("mamie"), true, "a good username must pass");
  assert.equal(re.test("marie-jo"), true, "a hyphen must still be allowed");
  assert.equal(re.test("ab"), false, "too short must fail");
  assert.equal(re.test("Mamie"), false, "uppercase must fail");
  assert.equal(re.test("mamie!"), false, "punctuation must fail");
});

console.log(`\n${passed} checks passed (${patterns.length} pattern attributes)`);
