// Plain-Node tests for app/static/js/theme-logic.js — no framework, no npm
// dependency, run via `node tests/js/theme_logic_test.mjs`. Wired into the
// pytest suite by test_tree_logic_js.py, which skips gracefully if node
// isn't on PATH.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const ThemeLogic = require("../../app/static/js/theme-logic.js");

const RANCH = ["dark", "light", "manuscript"];
const ORBIT = ["dark", "light"];

let passed = 0;

function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

check("nextScheme: the cycle walks the pack's own list, in order", () => {
  assert.equal(ThemeLogic.nextScheme(RANCH, "dark"), "light");
  assert.equal(ThemeLogic.nextScheme(RANCH, "light"), "manuscript");
  assert.equal(ThemeLogic.nextScheme(RANCH, "manuscript"), "dark");
});

check("nextScheme: a pack with two stops has two stops", () => {
  assert.equal(ThemeLogic.nextScheme(ORBIT, "dark"), "light");
  assert.equal(ThemeLogic.nextScheme(ORBIT, "light"), "dark");
});

check("nextScheme: a scheme the pack doesn't offer lands on its first", () => {
  // What a reader carries over from a ranch book into an orbit one: they
  // are looking at their system's scheme, not a choice this pack knows.
  assert.equal(ThemeLogic.nextScheme(ORBIT, "manuscript"), "dark");
  assert.equal(ThemeLogic.nextScheme(RANCH, null), "dark");
  assert.equal(ThemeLogic.nextScheme(RANCH, ""), "dark");
});

check("nextScheme: a pack offering one scheme stays on it", () => {
  assert.equal(ThemeLogic.nextScheme(["dark"], "dark"), "dark");
});

check("nextScheme: no schemes at all is nothing to cycle to", () => {
  assert.equal(ThemeLogic.nextScheme([], "dark"), null);
  assert.equal(ThemeLogic.nextScheme(null, "dark"), null);
});

check("pressAction: a plain tap cycles, which is the whole point", () => {
  assert.equal(ThemeLogic.pressAction({}), "cycle");
  assert.equal(ThemeLogic.pressAction({ open: false, longPress: false }), "cycle");
});

check("pressAction: holding opens the menu", () => {
  assert.equal(ThemeLogic.pressAction({ longPress: true }), "open");
});

check("pressAction: a tap while the menu is open is the way out", () => {
  assert.equal(ThemeLogic.pressAction({ open: true }), "close");
});

check("pressAction: the click a long press leaves behind never cycles", () => {
  // The case this function exists for: without it, holding the button to
  // look at your options would change your colours on the way in.
  assert.equal(ThemeLogic.pressAction({ open: false, longPress: true }), "open");
  assert.equal(ThemeLogic.pressAction({ open: true, longPress: true }), "open");
});

console.log(`\n${passed} passed`);
