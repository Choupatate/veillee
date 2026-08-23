// Plain-Node tests for app/static/js/draft-logic.js — no framework, no npm
// dependency, run via `node tests/js/draft_logic_test.mjs`. Wired into the
// pytest suite by test_tree_logic_js.py, which skips gracefully if node
// isn't on PATH.
//
// The first section is the defect this module was extracted to fix: the
// recovery banner used to compare two fields while the restore wrote
// fourteen, so a crash after any other kind of edit threw the draft away.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const Draft = require("../../app/static/js/draft-logic.js");

let passed = 0;

function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

const PAGE = {
  title: "First bike ride",
  markdown: "She wobbled, then she didn't.",
  date: "2026-06-18",
  author: "Papa",
  draft: false,
  archived: false,
  unlock: "",
  people: ["mamie"],
  tags: ["summer"],
  audience: [],
  sources: [],
};

const stored = (changes) => ({ ...PAGE, ...changes, savedAt: 1780000000000 });

// --- the bug ----------------------------------------------------------------

check("an edit to anything but the title or body is still recoverable", () => {
  // Each of these used to be discarded silently: the autosave had run, the
  // banner never appeared, and clearAutosave() deleted it on the way past.
  const onlyChanges = [
    ["the date", { date: "2026-06-19" }],
    ["who it is for", { audience: ["just-us"] }],
    ["the tags", { tags: ["summer", "bikes"] }],
    ["the people in it", { people: ["mamie", "papi"] }],
    ["the draft toggle", { draft: true }],
    ["the archive toggle", { archived: true }],
    ["the sealed-until date", { unlock: "2044-06-18" }],
    ["the author", { author: "Maman" }],
    ["a source", { sources: [{ url: "https://x", note: "n" }] }],
  ];
  for (const [what, change] of onlyChanges) {
    assert.equal(
      Draft.hasRecoverableChanges(stored(change), PAGE), true,
      `a draft differing only in ${what} must still be offered back`
    );
  }
});

check("the two it always did notice, it still notices", () => {
  assert.equal(Draft.hasRecoverableChanges(stored({ title: "Other" }), PAGE), true);
  assert.equal(Draft.hasRecoverableChanges(stored({ markdown: "More" }), PAGE), true);
});

check("a draft identical to the page is not offered", () => {
  // Otherwise every reopened editor greets you with a banner about a draft
  // that would change nothing.
  assert.equal(Draft.hasRecoverableChanges(stored({}), PAGE), false);
});

check("savedAt alone is never a change", () => {
  assert.equal(Draft.hasRecoverableChanges(stored({}), { ...PAGE }), false);
  assert.ok(!Draft.comparedKeys(stored({}), PAGE).includes("savedAt"));
});

// --- falsy values are values -------------------------------------------------

check("toggling a flag off is a change, not an absence", () => {
  const on = { ...PAGE, draft: true };
  assert.equal(Draft.hasRecoverableChanges(stored({ draft: false }), on), true);
});

check("clearing a field is a change", () => {
  assert.equal(Draft.hasRecoverableChanges(stored({ title: "" }), PAGE), true);
  assert.equal(Draft.hasRecoverableChanges(stored({ tags: [] }), PAGE), true);
});

check("null, undefined and a missing key all read as empty, and agree", () => {
  assert.equal(Draft.canonical(null), Draft.canonical(undefined));
  assert.equal(
    Draft.hasRecoverableChanges({ title: "t", markdown: "m", unlock: null },
                                { title: "t", markdown: "m" }),
    false
  );
});

check("a field the page does not have is still compared", () => {
  // An autosave from before a field existed, or from the person editor
  // rather than the story editor. It differs, so it counts.
  assert.equal(
    Draft.hasRecoverableChanges({ title: "t", markdown: "m", relation: "aunt" },
                                { title: "t", markdown: "m" }),
    true
  );
});

// --- ordering ---------------------------------------------------------------

check("reordering people or sources counts as a change", () => {
  // Their order is meaningful and editable, so it is not noise.
  assert.equal(
    Draft.hasRecoverableChanges(stored({ people: ["papi", "mamie"] }),
                                { ...PAGE, people: ["mamie", "papi"] }),
    true
  );
});

check("key order in an object never counts as a change", () => {
  assert.equal(
    Draft.canonical({ url: "u", note: "n" }),
    Draft.canonical({ note: "n", url: "u" })
  );
});

// --- what came out of storage ------------------------------------------------

check("junk in localStorage is not a draft", () => {
  for (const junk of [null, undefined, "", "a string", 42, [], [1, 2],
                      { nope: true }, { title: "t" }, { markdown: "m" },
                      { title: 1, markdown: 2 }]) {
    assert.equal(Draft.isRestorable(junk), false, JSON.stringify(junk));
    assert.equal(Draft.hasRecoverableChanges(junk, PAGE), false);
  }
});

check("an empty new-story draft is a draft", () => {
  // Empty strings are the correct shape; the page just has nothing in it.
  assert.equal(Draft.isRestorable({ title: "", markdown: "" }), true);
});

// --- the timestamp -----------------------------------------------------------

check("savedAtLabel formats through whatever the caller passes", () => {
  const label = Draft.savedAtLabel({ savedAt: 0 }, (d) => d.getUTCFullYear());
  assert.equal(label, 1970);
});

check("a missing or nonsense timestamp costs the label, not the draft", () => {
  // `new Date(undefined).toLocaleString()` is "Invalid Date" on the banner.
  for (const bad of [undefined, null, "yesterday", NaN, Infinity]) {
    assert.equal(Draft.savedAtLabel({ savedAt: bad }, (d) => d.toISOString()), "");
  }
  assert.equal(Draft.savedAtLabel(null), "");
});

check("the module touches no DOM", () => {
  // Comments stripped first: this file's own header explains what
  // localStorage held and why the comparison was wrong, and a guard that
  // cannot tell prose from code would forbid saying so.
  const source = require("node:fs")
    .readFileSync(new URL("../../app/static/js/draft-logic.js", import.meta.url), "utf8")
    .replace(/\/\*[\s\S]*?\*\//g, "")
    .replace(/(^|[^:])\/\/.*$/gm, "$1");
  for (const forbidden of ["document.", "window.", "localStorage", "fetch("]) {
    assert.ok(!source.includes(forbidden), `draft-logic.js must not use ${forbidden}`);
  }
});

console.log(`\n${passed} checks passed`);
