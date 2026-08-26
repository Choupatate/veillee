// Plain-Node tests for app/static/js/share-logic.js — no framework, no npm
// dependency, run via `node tests/js/share_link_test.mjs`. Wired into the
// pytest suite by test_tree_logic_js.py, which skips gracefully if node
// isn't on PATH.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const ShareLogic = require("../../app/static/js/share-logic.js");

let passed = 0;

function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

// --- which way of handing the link over ------------------------------------

check("tier: a phone with a share sheet gets the share sheet", () => {
  assert.equal(ShareLogic.tier({ canShare: true, canCopy: true }), "share");
});

check("tier: a desktop browser with no share sheet copies", () => {
  assert.equal(ShareLogic.tier({ canShare: false, canCopy: true }), "copy");
});

check("tier: plain HTTP has neither, and falls back to selecting", () => {
  // The Clipboard API needs a secure context, and a self-hosted app on a
  // home network often is not one. This is the tier that keeps the button
  // from being dead there.
  assert.equal(ShareLogic.tier({ canShare: false, canCopy: false }), "select");
});

check("tier: a share sheet is preferred even when the clipboard works", () => {
  assert.equal(ShareLogic.tier({ canShare: true, canCopy: false }), "share");
});

check("tier: no capabilities object at all still returns a tier", () => {
  // Called before feature detection has run, or with a stale object. It
  // must degrade, not throw — this decides whether a button works.
  assert.equal(ShareLogic.tier(), "select");
  assert.equal(ShareLogic.tier(null), "select");
  assert.equal(ShareLogic.tier({}), "select");
});

// --- what a failed share means ---------------------------------------------

check("isDismissal: closing the share sheet is AbortError", () => {
  const dismissed = new Error("share canceled");
  dismissed.name = "AbortError";
  assert.equal(ShareLogic.isDismissal(dismissed), true);
});

check("isDismissal: a real failure is not a dismissal", () => {
  const broken = new Error("permission denied");
  broken.name = "NotAllowedError";
  assert.equal(ShareLogic.isDismissal(broken), false);
});

check("isDismissal: no error is not a dismissal", () => {
  assert.equal(ShareLogic.isDismissal(null), false);
  assert.equal(ShareLogic.isDismissal(undefined), false);
});

check("afterShareFailure: a dismissal does nothing at all", () => {
  // The rule this module exists for. Someone opened the share sheet and
  // changed their mind; silently putting a private write-link on their
  // clipboard is not a helpful consolation prize.
  const dismissed = new Error("share canceled");
  dismissed.name = "AbortError";
  assert.equal(ShareLogic.afterShareFailure(dismissed), "none");
});

check("afterShareFailure: a genuine failure falls down a tier", () => {
  const broken = new Error("no handler");
  broken.name = "NotAllowedError";
  assert.equal(ShareLogic.afterShareFailure(broken), "copy");
});

console.log(`\n${passed} checks passed`);
