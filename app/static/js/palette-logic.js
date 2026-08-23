// The colour maths behind the theme editor's live preview (F52) — a port
// of app/palette.py's `derive`, `contrast` and `palette_warnings`.
//
// **This file exists to be checked against the Python, not trusted on its
// own.** A preview that is merely *close* to what the app will render is
// worse than no preview: it teaches someone that their dim text is
// readable when the server is about to decide otherwise. So every number
// below mirrors palette.py operation for operation, in the same order, and
// `tests/test_palette_preview.py` feeds a long list of seeds through both
// and fails on the first hex that differs. If you change one, change both
// in the same commit.
//
// Two portability details that are easy to get wrong and impossible to see:
//
//   * Python's `round()` is half-to-even; JavaScript's `Math.round` is
//     half-up. They disagree on exactly the values a 50% mix produces
//     (126.5 -> 126 in Python, 127 here), so `pyRound` below does it
//     Python's way. This is not pedantry: `mix(bg, text, 0.5)` lands on a
//     .5 boundary for any pair of channels an even distance apart.
//   * Neither this file nor palette.py is allowed to shortcut the
//     back-off loops into a formula. They are iterative because contrast
//     is not linear in the mix amount, and a closed form would drift.
(function (root, factory) {
  if (typeof module === "object" && module.exports) {
    module.exports = factory();
  } else {
    root.PaletteLogic = factory();
  }
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var HEX_RE = /^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/;

  //: What a dimmed label still has to clear against its background.
  var DIM_FLOOR = 4.5;
  //: A border is not text; it only has to be visible as an edge.
  var EDGE_FLOOR = 1.5;
  //: What palette.py's `palette_warnings` measures text against.
  var TEXT_FLOOR = 4.5;

  //: The three colours a scheme is, and nothing else to fill in.
  var SEEDS = ["bg", "text", "accent"];

  function isHex(value) {
    return typeof value === "string" && HEX_RE.test(value.trim());
  }

  function parseHex(value) {
    if (!isHex(value)) throw new Error("not a hex colour: " + value);
    var digits = value.trim().replace(/^#/, "");
    if (digits.length === 3) {
      digits = digits.charAt(0) + digits.charAt(0)
             + digits.charAt(1) + digits.charAt(1)
             + digits.charAt(2) + digits.charAt(2);
    }
    return [
      parseInt(digits.slice(0, 2), 16),
      parseInt(digits.slice(2, 4), 16),
      parseInt(digits.slice(4, 6), 16),
    ];
  }

  // Python's round(): halves go to the even neighbour. Channels are never
  // negative here (they are clamped to 0..255 by the caller), so this only
  // has to be right for non-negative input.
  function pyRound(x) {
    var floor = Math.floor(x);
    var fraction = x - floor;
    if (fraction > 0.5) return floor + 1;
    if (fraction < 0.5) return floor;
    return floor % 2 === 0 ? floor : floor + 1;
  }

  function channelHex(value) {
    var clamped = Math.max(0, Math.min(255, pyRound(value)));
    return (clamped < 16 ? "0" : "") + clamped.toString(16);
  }

  function toHex(rgb) {
    return "#" + channelHex(rgb[0]) + channelHex(rgb[1]) + channelHex(rgb[2]);
  }

  // `amount` of `b` mixed into `a`, per channel, in plain sRGB — small
  // nudges between colours someone already chose to sit together.
  function mix(a, b, amount) {
    var ratio = Math.max(0, Math.min(1, amount));
    return [
      a[0] + (b[0] - a[0]) * ratio,
      a[1] + (b[1] - a[1]) * ratio,
      a[2] + (b[2] - a[2]) * ratio,
    ];
  }

  function relativeLuminance(rgb) {
    var channels = [];
    for (var i = 0; i < 3; i++) {
      var c = rgb[i] / 255;
      channels.push(c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
    }
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2];
  }

  function contrast(a, b) {
    var first = relativeLuminance(a);
    var second = relativeLuminance(b);
    var lighter = Math.max(first, second);
    var darker = Math.min(first, second);
    return (lighter + 0.05) / (darker + 0.05);
  }

  // Whether a scheme reads as dark, decided by its background rather than
  // by its name.
  function isDark(bg) {
    return relativeLuminance(parseHex(bg)) < 0.4;
  }

  function mixToFloor(base, target, amount, against, floor, step) {
    step = step === undefined ? 0.04 : step;
    amount = Math.max(0, Math.min(1, amount));
    while (amount > 0) {
      var candidate = mix(base, target, amount);
      if (contrast(candidate, against) >= floor) return candidate;
      amount -= step;
    }
    return base;
  }

  function mixUpToFloor(base, target, amount, against, floor, limit, step) {
    limit = limit === undefined ? 0.6 : limit;
    step = step === undefined ? 0.04 : step;
    amount = Math.max(0, Math.min(1, amount));
    var candidate = mix(base, target, amount);
    while (contrast(candidate, against) < floor && amount < limit) {
      amount += step;
      candidate = mix(base, target, amount);
    }
    return candidate;
  }

  function rgbTriple(rgb) {
    return [pyRound(rgb[0]), pyRound(rgb[1]), pyRound(rgb[2])].join(", ");
  }

  // Every variable one scheme sets, from {bg, text, accent}.
  function derive(seed, texture) {
    var bg = parseHex(seed.bg);
    var text = parseHex(seed.text);
    var accent = parseHex(seed.accent);
    var dark = relativeLuminance(bg) < 0.4;

    // The label drawn *on* the accent: whichever of the reader's own two
    // colours can be read against it.
    var accentText = contrast(accent, bg) >= contrast(accent, text) ? bg : text;
    var edge = toHex(mixUpToFloor(bg, text, 0.18, bg, EDGE_FLOOR));

    var variables = {
      "--color-bg": toHex(bg),
      "--color-bg-raised": toHex(mix(bg, text, 0.07)),
      "--color-text": toHex(text),
      "--color-text-dim": toHex(mixToFloor(text, bg, 0.42, bg, DIM_FLOOR)),
      "--color-accent": toHex(accent),
      "--color-accent-text": toHex(accentText),
      "--color-highlight-bg": "rgba(" + rgbTriple(accent) + ", 0.18)",
      "--color-border": edge,
      "--illo-mount": toHex(mix(bg, text, 0.04)),
      "--illo-mount-edge": edge,
      "--ambience-glow": rgbTriple(mix(accent, [255, 255, 255], 0.35)),
      "--ambience-glow-edge": rgbTriple(accent),
      "--ambience-shade": rgbTriple(bg),
      "--firelight-strength": dark ? "1" : "1.6",
      "--surface-texture": texture || "none",
      "color-scheme": dark ? "dark" : "light",
    };
    if (texture) variables["--surface-texture-size"] = "512px 512px";
    return variables;
  }

  function complete(seed) {
    if (!seed || typeof seed !== "object") return false;
    return SEEDS.every(function (key) {
      return isHex(seed[key]);
    });
  }

  // The one measurement palette.py refuses to save quietly. `template` is
  // the sentence, translated server-side, with {scheme} and {ratio} in it —
  // this file stays free of English.
  function warnings(schemeColors, template) {
    var out = [];
    Object.keys(schemeColors || {}).forEach(function (scheme) {
      var seed = schemeColors[scheme];
      if (!seed || !isHex(seed.text) || !isHex(seed.bg)) return;
      var ratio = contrast(parseHex(seed.text), parseHex(seed.bg));
      if (ratio < TEXT_FLOOR) {
        out.push({
          scheme: scheme,
          ratio: ratio,
          text: String(template || "")
            .replace("{scheme}", scheme)
            .replace("{ratio}", ratio.toFixed(1)),
        });
      }
    });
    return out;
  }

  // What the preview puts under the miniature: the three pairs a reader
  // actually has to be able to tell apart, each with the floor it is being
  // held to. `--color-border` is deliberately not here — an edge that is
  // hard to see is a design choice, not a fault.
  function checks(seed) {
    if (!complete(seed)) return [];
    var bg = parseHex(seed.bg);
    var vars = derive(seed);
    return [
      { key: "text", ratio: contrast(parseHex(seed.text), bg), floor: TEXT_FLOOR },
      { key: "accent", ratio: contrast(parseHex(seed.accent), bg), floor: DIM_FLOOR },
      { key: "dim", ratio: contrast(parseHex(vars["--color-text-dim"]), bg), floor: DIM_FLOOR },
    ];
  }

  return {
    DIM_FLOOR: DIM_FLOOR,
    EDGE_FLOOR: EDGE_FLOOR,
    TEXT_FLOOR: TEXT_FLOOR,
    SEEDS: SEEDS,
    isHex: isHex,
    parseHex: parseHex,
    toHex: toHex,
    pyRound: pyRound,
    mix: mix,
    relativeLuminance: relativeLuminance,
    contrast: contrast,
    isDark: isDark,
    derive: derive,
    complete: complete,
    warnings: warnings,
    checks: checks,
  };
});
