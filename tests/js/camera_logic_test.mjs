// Plain-Node tests for app/static/js/camera-logic.js — no framework, no
// npm dependency, run via `node tests/js/camera_logic_test.mjs`. Wired
// into the pytest suite by test_tree_logic_js.py, which skips gracefully
// if node isn't on PATH.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const CameraLogic = require("../../app/static/js/camera-logic.js");

let passed = 0;

function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

check("captureSize: a frame within the limit is kept at its own size", () => {
  assert.deepEqual(CameraLogic.captureSize(1280, 720), { width: 1280, height: 720 });
});

check("captureSize: a frame exactly at the limit is not touched", () => {
  const size = CameraLogic.captureSize(CameraLogic.MAX_EDGE, 1000);
  assert.deepEqual(size, { width: CameraLogic.MAX_EDGE, height: 1000 });
});

check("captureSize: a wide frame is scaled by its longest edge", () => {
  assert.deepEqual(CameraLogic.captureSize(4000, 3000, 2000), { width: 2000, height: 1500 });
});

check("captureSize: a tall (portrait) frame is scaled by its height", () => {
  assert.deepEqual(CameraLogic.captureSize(3000, 4000, 2000), { width: 1500, height: 2000 });
});

check("captureSize: the aspect ratio survives an awkward ratio", () => {
  const size = CameraLogic.captureSize(4032, 2268, 2000);
  assert.equal(size.width, 2000);
  assert.equal(size.height, 1125);
  assert.ok(Math.abs(size.width / size.height - 4032 / 2268) < 0.01);
});

check("captureSize: an extreme ratio never rounds an edge down to zero", () => {
  assert.deepEqual(CameraLogic.captureSize(4000, 1, 100), { width: 100, height: 1 });
});

check("captureSize: a not-yet-ready video (0x0) is null, not a blank frame", () => {
  assert.equal(CameraLogic.captureSize(0, 0), null);
  assert.equal(CameraLogic.captureSize(640, 0), null);
  assert.equal(CameraLogic.captureSize(undefined, undefined), null);
});

check("captureSize: fractional dimensions are rounded to whole pixels", () => {
  assert.deepEqual(CameraLogic.captureSize(640.4, 480.6), { width: 640, height: 481 });
});

check("nextFacingMode: flips back and front, and back again", () => {
  assert.equal(CameraLogic.nextFacingMode("environment"), "user");
  assert.equal(CameraLogic.nextFacingMode("user"), "environment");
});

check("nextFacingMode: anything unknown flips to the back camera", () => {
  assert.equal(CameraLogic.nextFacingMode(undefined), "environment");
  assert.equal(CameraLogic.nextFacingMode(""), "environment");
});

check("isMirrored: only the selfie camera previews mirrored", () => {
  assert.equal(CameraLogic.isMirrored("user"), true);
  assert.equal(CameraLogic.isMirrored("environment"), false);
  assert.equal(CameraLogic.isMirrored(undefined), false);
});

check("captureFilename: local timestamp, zero-padded, .jpg", () => {
  assert.equal(
    CameraLogic.captureFilename(new Date(2026, 6, 4, 9, 5, 3)),
    "camera-20260704-090503.jpg"
  );
});

check("captureFilename: two-digit parts are left alone", () => {
  assert.equal(
    CameraLogic.captureFilename(new Date(2026, 11, 25, 18, 42, 59)),
    "camera-20261225-184259.jpg"
  );
});

console.log(`\n${passed} passed`);
