// Pure, DOM-free helpers behind the in-app camera (FEATURES.md F34):
// frame-scaling math, the front/back toggle, and capture filenames. Kept
// out of camera.js so it can be unit-tested under plain Node
// (tests/js/camera_logic_test.mjs) without a browser or a webcam.
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.CameraLogic = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  // Mirrors storage.MAX_IMAGE_EDGE: the server re-encodes to this anyway,
  // so shrinking here only saves upload bytes, never quality.
  var MAX_EDGE = 2000;

  function captureSize(width, height, maxEdge) {
    var limit = maxEdge || MAX_EDGE;
    // A <video> reports 0x0 until the stream has a first frame; the caller
    // uses null to mean "not ready yet" rather than capturing a blank.
    if (!(width > 0) || !(height > 0)) return null;
    var longest = Math.max(width, height);
    if (longest <= limit) {
      return { width: Math.round(width), height: Math.round(height) };
    }
    var scale = limit / longest;
    return {
      width: Math.max(1, Math.round(width * scale)),
      height: Math.max(1, Math.round(height * scale)),
    };
  }

  function nextFacingMode(mode) {
    return mode === "environment" ? "user" : "environment";
  }

  // Phones show the selfie camera mirrored (you move left, the preview
  // moves left) but save the frame unmirrored. Only the preview asks.
  function isMirrored(mode) {
    return mode === "user";
  }

  function captureFilename(when) {
    var d = when || new Date();
    function pad(n) {
      return (n < 10 ? "0" : "") + n;
    }
    return (
      "camera-" +
      d.getFullYear() +
      pad(d.getMonth() + 1) +
      pad(d.getDate()) +
      "-" +
      pad(d.getHours()) +
      pad(d.getMinutes()) +
      pad(d.getSeconds()) +
      ".jpg"
    );
  }

  return {
    MAX_EDGE: MAX_EDGE,
    captureSize: captureSize,
    nextFacingMode: nextFacingMode,
    isMirrored: isMirrored,
    captureFilename: captureFilename,
  };
});
