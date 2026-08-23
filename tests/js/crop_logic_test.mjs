// Plain-Node tests for app/static/js/crop-logic.js — no framework, no npm
// dependency, run via `node tests/js/crop_logic_test.mjs`. Wired into the
// pytest suite by test_tree_logic_js.py, which skips gracefully if node
// isn't on PATH.
//
// The cropper is the one place in this app where a parent frames something
// by hand and gets back a file. Nothing on screen would tell them if the
// JPEG disagreed with the preview, so the last section here is the point
// of the module existing: preview and canvas are the same call.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const Crop = require("../../app/static/js/crop-logic.js");

let passed = 0;

function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

function near(actual, expected, message, tolerance = 1e-9) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `${message}: ${actual} !== ${expected}`
  );
}

// A landscape photo on a 300px square stage: 1200x800 needs 0.375 to fit
// its *height*, so the width overflows to 450.
const LANDSCAPE = { naturalW: 1200, naturalH: 800, stageSize: 300, zoomPct: 0, panX: 0, panY: 0 };
const PORTRAIT = { naturalW: 800, naturalH: 1200, stageSize: 300, zoomPct: 0, panX: 0, panY: 0 };

// --- fitting -----------------------------------------------------------------

check("fitScale covers the frame rather than fitting inside it", () => {
  near(Crop.fitScale(1200, 800, 300), 0.375, "landscape covers by height");
  near(Crop.fitScale(800, 1200, 300), 0.375, "portrait covers by width");
  const box = Crop.placement(LANDSCAPE);
  assert.ok(box.width >= 300 && box.height >= 300, "no letterboxing on either axis");
});

check("fitScale is zero for a photo or stage that has no size yet", () => {
  // The <img> fires load before layout in some browsers; a NaN placement
  // would put the photo at `left: NaNpx` and it would simply vanish.
  assert.equal(Crop.fitScale(0, 800, 300), 0);
  assert.equal(Crop.fitScale(1200, 0, 300), 0);
  assert.equal(Crop.fitScale(1200, 800, 0), 0);
});

check("a square photo on a square stage fits exactly, with no slack", () => {
  const square = { naturalW: 600, naturalH: 600, stageSize: 300, zoomPct: 0, panX: 0, panY: 0 };
  const box = Crop.placement(square);
  near(box.width, 300, "width");
  near(box.height, 300, "height");
  near(box.left, 0, "left");
  near(box.top, 0, "top");
  assert.deepEqual(Crop.panLimits(square), { x: 0, y: 0 });
});

// --- zoom --------------------------------------------------------------------

check("zoom runs from just-covering to MAX_ZOOM_MULT across the slider", () => {
  const fit = Crop.fitScale(1200, 800, 300);
  near(Crop.scaleAt(fit, 0), fit, "zero is the fitting scale");
  near(Crop.scaleAt(fit, 100), fit * Crop.MAX_ZOOM_MULT, "full is the multiple");
  near(Crop.scaleAt(fit, 50), fit * 2, "halfway is halfway between");
});

check("zoom outside the slider is clamped, not stored", () => {
  assert.equal(Crop.clampZoom(-30), 0);
  assert.equal(Crop.clampZoom(160), 100);
  assert.equal(Crop.clampZoom(NaN), 0);
  assert.equal(Crop.clampZoom(42), 42);
});

// --- panning -----------------------------------------------------------------

check("the short edge has no pan slack until you zoom in", () => {
  // 1200x800 at fit: 450x300. The height only just covers, so vertical
  // panning would show background.
  assert.deepEqual(Crop.panLimits(LANDSCAPE), { x: 75, y: 0 });
  assert.deepEqual(Crop.panLimits(PORTRAIT), { x: 0, y: 75 });
});

check("zooming in opens up slack on both axes", () => {
  const limits = Crop.panLimits({ ...LANDSCAPE, zoomPct: 100 });
  assert.ok(limits.x > 75, "wider");
  assert.ok(limits.y > 0, "and now vertical too");
});

check("a pan past the edge is pulled back to it", () => {
  const dragged = { ...LANDSCAPE, panX: 5000, panY: 5000 };
  assert.deepEqual(Crop.clampPan(dragged), { panX: 75, panY: 0 });
  const other = { ...LANDSCAPE, panX: -5000, panY: -5000 };
  assert.deepEqual(Crop.clampPan(other), { panX: -75, panY: 0 });
});

check("placement clamps the pan it is given", () => {
  // The overlay clamps as it drags, but rasterizeCrop reads the state
  // straight out — so placement has to clamp too, or a stale pan could
  // reach the canvas after a zoom change shrank the limits.
  const overshot = { ...LANDSCAPE, panX: 5000 };
  assert.deepEqual(Crop.placement(overshot), Crop.placement({ ...LANDSCAPE, panX: 75 }));
});

check("a drag moves the photo with the finger, from where the pan started", () => {
  const moved = Crop.dragPan({ panX: 10, panY: 20 }, { x: 100, y: 100 }, { x: 130, y: 60 });
  assert.deepEqual(moved, { panX: 40, panY: -20 });
});

check("a drag out and back returns to where it began", () => {
  const start = { panX: 12, panY: -4 };
  const out = Crop.dragPan(start, { x: 50, y: 50 }, { x: 400, y: 400 });
  const back = Crop.dragPan(start, { x: 50, y: 50 }, { x: 50, y: 50 });
  assert.notDeepEqual(out, back);
  assert.deepEqual(back, start);
});

// --- pinch -------------------------------------------------------------------

check("doubling the finger distance adds the whole slider", () => {
  assert.equal(Crop.pinchZoom(0, 100, 200), 100);
  assert.equal(Crop.pinchZoom(0, 100, 150), 50);
});

check("pinching closed comes back down, and stops at zero", () => {
  assert.equal(Crop.pinchZoom(50, 100, 50), 0);
  assert.equal(Crop.pinchZoom(50, 100, 10), 0);
});

check("a pinch that starts with no distance changes nothing", () => {
  // Two pointers reported at the same coordinates would otherwise divide
  // by zero and set the zoom to NaN, which the slider cannot come back from.
  assert.equal(Crop.pinchZoom(40, 0, 120), 40);
});

check("distance is symmetric and ordinary Pythagoras", () => {
  assert.equal(Crop.distance({ x: 0, y: 0 }, { x: 3, y: 4 }), 5);
  assert.equal(Crop.distance({ x: 3, y: 4 }, { x: 0, y: 0 }), 5);
});

// --- the reason this module exists -------------------------------------------

check("the canvas draws exactly what the preview shows, at output scale", () => {
  // editor.js computed this twice — once in CSS pixels for the preview and
  // once in canvas pixels for the JPEG. Same numbers, written out
  // separately. This is the property those two copies were supposed to
  // have and nothing checked.
  const states = [
    LANDSCAPE,
    PORTRAIT,
    { ...LANDSCAPE, zoomPct: 37, panX: 21, panY: -8 },
    { ...PORTRAIT, zoomPct: 100, panX: -60, panY: 140 },
    { naturalW: 4032, naturalH: 3024, stageSize: 320, zoomPct: 12, panX: -19, panY: 3 },
  ];
  for (const state of states) {
    const k = Crop.outputScale(state.stageSize);
    const preview = Crop.placement(state);
    const canvas = Crop.placement(state, k);
    for (const key of ["left", "top", "width", "height"]) {
      near(canvas[key], preview[key] * k, `${key} at zoom ${state.zoomPct}`, 1e-9);
    }
  }
});

check("the framed square is the square that gets saved", () => {
  // The stronger statement: whatever part of the photo sits under the
  // stage ends up filling the 900px output. Checked by mapping the output
  // square's corners back through the placement and landing on the stage.
  const state = { ...LANDSCAPE, zoomPct: 60, panX: -30, panY: 12 };
  const k = Crop.outputScale(state.stageSize);
  const canvas = Crop.placement(state, k);
  const preview = Crop.placement(state);

  // The output canvas is OUTPUT_SIZE across; the stage is stageSize. The
  // fraction of the photo covered has to be identical.
  near(
    (0 - canvas.left) / canvas.width,
    (0 - preview.left) / preview.width,
    "left edge of the visible strip"
  );
  near(
    (Crop.OUTPUT_SIZE - canvas.top) / canvas.height,
    (state.stageSize - preview.top) / preview.height,
    "bottom edge of the visible strip"
  );
});

check("a stage of zero produces no output scale rather than infinity", () => {
  assert.equal(Crop.outputScale(0), 0);
  assert.equal(Crop.outputScale(300), 3);
});

check("the module touches no DOM", () => {
  // It runs here at all, which is most of the proof; this catches a
  // `document.` slipped in behind a branch that these tests miss.
  const source = require("node:fs").readFileSync(
    new URL("../../app/static/js/crop-logic.js", import.meta.url), "utf8"
  );
  for (const forbidden of ["document.", "window.", "navigator.", "fetch("]) {
    assert.ok(!source.includes(forbidden), `crop-logic.js must not use ${forbidden}`);
  }
});

console.log(`\n${passed} checks passed`);
