// Pure, DOM-free geometry behind the editor's pan/zoom photo cropper
// (FEATURES.md F33). Kept out of editor.js so it can be unit-tested under
// plain Node (tests/js/crop_logic_test.mjs), and — the reason it exists at
// all — so the preview and the finished JPEG are computed by the *same*
// function.
//
// editor.js used to work out where the photo sits twice: once in
// `updateCropTransform`, in CSS pixels against the on-screen stage, and
// again in `rasterizeCrop`, in canvas pixels against a 900px square. Two
// copies of one piece of arithmetic, and the failure mode if they ever
// disagreed is the worst kind for this app — the photo a parent framed is
// not the photo their book keeps, and nothing on screen would say so.
// `placement()` is that arithmetic, and the canvas just asks for it at a
// different scale.
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.CropLogic = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // How far past "fills the frame" the slider can go, and the resolution
  // the square crop is written at.
  var MAX_ZOOM_MULT = 3;
  var OUTPUT_SIZE = 900;

  // The scale at which the photo exactly fills the square stage: the
  // *larger* of the two ratios, so the short edge covers the frame and the
  // long edge overflows. `min` here would letterbox, which is the one
  // thing a square crop must never do.
  function fitScale(naturalW, naturalH, stageSize) {
    if (!naturalW || !naturalH || !stageSize) return 0;
    return Math.max(stageSize / naturalW, stageSize / naturalH);
  }

  // zoomPct runs 0..100 across the whole slider, mapping to 1x..MAX_ZOOM_MULT
  // of the fitting scale.
  function scaleAt(fit, zoomPct) {
    return fit * (1 + (MAX_ZOOM_MULT - 1) * (clampZoom(zoomPct) / 100));
  }

  function clampZoom(zoomPct) {
    if (!isFinite(zoomPct)) return 0;
    return Math.max(0, Math.min(100, zoomPct));
  }

  // How far the photo may be dragged before an edge would come inside the
  // frame. Zero on an axis the photo only just covers, which is why a
  // photo at zoom 0 cannot be panned along its short edge — there is no
  // slack there, and offering some would expose the background.
  function panLimits(state) {
    var scale = scaleAt(
      fitScale(state.naturalW, state.naturalH, state.stageSize), state.zoomPct
    );
    return {
      x: Math.max(0, (state.naturalW * scale - state.stageSize) / 2),
      y: Math.max(0, (state.naturalH * scale - state.stageSize) / 2),
    };
  }

  // The `+ 0` is not decoration: clamping a negative drag against a limit
  // of zero yields -0 in JavaScript, and -0 survives JSON, comparison
  // helpers and anything that renders the number back out. Adding zero
  // makes it 0 and leaves every other value alone.
  function clampPan(state) {
    var limit = panLimits(state);
    return {
      panX: Math.max(-limit.x, Math.min(limit.x, state.panX || 0)) + 0,
      panY: Math.max(-limit.y, Math.min(limit.y, state.panY || 0)) + 0,
    };
  }

  // Where the photo sits and how big it is, in units of the stage. `k`
  // rescales the whole answer: 1 for the CSS preview, OUTPUT_SIZE/stageSize
  // for the canvas. That single argument is the entire difference between
  // what the parent sees and what gets saved.
  function placement(state, k) {
    var factor = k === undefined ? 1 : k;
    var scale = scaleAt(
      fitScale(state.naturalW, state.naturalH, state.stageSize), state.zoomPct
    );
    var clamped = clampPan(state);
    var width = state.naturalW * scale;
    var height = state.naturalH * scale;
    return {
      left: (state.stageSize / 2 - width / 2 + clamped.panX) * factor,
      top: (state.stageSize / 2 - height / 2 + clamped.panY) * factor,
      width: width * factor,
      height: height * factor,
    };
  }

  // The canvas scale factor: how many output pixels one stage pixel is
  // worth. A stage of zero would make every placement NaN, so it is
  // treated as "no photo to draw" rather than allowed through.
  function outputScale(stageSize) {
    if (!stageSize) return 0;
    return OUTPUT_SIZE / stageSize;
  }

  function distance(a, b) {
    var dx = a.x - b.x;
    var dy = a.y - b.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  // A pinch that doubles the distance between two fingers adds 100 to the
  // zoom — the full slider. Clamped, so a hard pinch stops at the ends
  // rather than storing a zoom the slider cannot show.
  function pinchZoom(startZoom, startDistance, currentDistance) {
    if (!startDistance) return clampZoom(startZoom);
    return clampZoom(startZoom + (currentDistance / startDistance - 1) * 100);
  }

  // A drag moves the photo one-to-one with the finger, from where the pan
  // was when the finger went down — not from where it is now, which is
  // what makes a drag that hits a limit and comes back retrace its steps
  // instead of sticking.
  function dragPan(panStart, dragStart, current) {
    return {
      panX: panStart.panX + (current.x - dragStart.x),
      panY: panStart.panY + (current.y - dragStart.y),
    };
  }

  return {
    MAX_ZOOM_MULT: MAX_ZOOM_MULT,
    OUTPUT_SIZE: OUTPUT_SIZE,
    fitScale: fitScale,
    scaleAt: scaleAt,
    clampZoom: clampZoom,
    panLimits: panLimits,
    clampPan: clampPan,
    placement: placement,
    outputScale: outputScale,
    distance: distance,
    pinchZoom: pinchZoom,
    dragPan: dragPan,
  };
});
