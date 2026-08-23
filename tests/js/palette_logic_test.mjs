// Plain-Node tests for app/static/js/palette-logic.js — no framework, no npm
// dependency, run via `node tests/js/palette_logic_test.mjs`. Wired into the
// pytest suite by test_tree_logic_js.py, which skips gracefully if node
// isn't on PATH.
//
// These cover the *shape* of the maths. Whether it agrees with the server
// is a different question and a different test: tests/test_palette_preview.py
// runs the same seeds through app/palette.py and this file and compares the
// hexes. Neither test replaces the other — this one can pass on a port that
// is internally consistent and wrong.
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const Palette = require("../../app/static/js/palette-logic.js");

let passed = 0;

function check(name, fn) {
  fn();
  passed++;
  console.log("ok -", name);
}

check("isHex accepts both lengths and rejects everything else", () => {
  assert.equal(Palette.isHex("#abc"), true);
  assert.equal(Palette.isHex("#AABBCC"), true);
  assert.equal(Palette.isHex("  #123456  "), true);
  assert.equal(Palette.isHex("#abcd"), false);
  assert.equal(Palette.isHex("abcdef"), false);
  assert.equal(Palette.isHex("rebeccapurple"), false);
  assert.equal(Palette.isHex(""), false);
  assert.equal(Palette.isHex(null), false);
  assert.equal(Palette.isHex(0x123456), false);
});

check("parseHex expands the short form the way the server does", () => {
  assert.deepEqual(Palette.parseHex("#abc"), [0xaa, 0xbb, 0xcc]);
  assert.deepEqual(Palette.parseHex("#0f0d14"), [15, 13, 20]);
  assert.throws(() => Palette.parseHex("nope"));
});

check("pyRound is half-to-even, not half-up", () => {
  // The whole reason this function exists. Math.round would give 127 and
  // 129 here, and the preview would render a shade the server never will.
  assert.equal(Palette.pyRound(126.5), 126);
  assert.equal(Palette.pyRound(127.5), 128);
  assert.equal(Palette.pyRound(128.5), 128);
  assert.equal(Palette.pyRound(0.5), 0);
  assert.equal(Palette.pyRound(1.5), 2);
  // Away from the boundary it is ordinary rounding.
  assert.equal(Palette.pyRound(126.4), 126);
  assert.equal(Palette.pyRound(126.6), 127);
  assert.equal(Palette.pyRound(9), 9);
});

check("toHex pads single digits and clamps out-of-range channels", () => {
  assert.equal(Palette.toHex([0, 0, 0]), "#000000");
  assert.equal(Palette.toHex([255, 255, 255]), "#ffffff");
  assert.equal(Palette.toHex([15, 13, 20]), "#0f0d14");
  assert.equal(Palette.toHex([-8, 300, 20]), "#00ff14");
});

check("mix clamps its amount and lands on the endpoints", () => {
  const a = [0, 0, 0];
  const b = [255, 255, 255];
  assert.deepEqual(Palette.mix(a, b, 0), a);
  assert.deepEqual(Palette.mix(a, b, 1), b);
  assert.deepEqual(Palette.mix(a, b, 2), b);
  assert.deepEqual(Palette.mix(a, b, -1), a);
  assert.deepEqual(Palette.mix(a, b, 0.5), [127.5, 127.5, 127.5]);
});

check("contrast is symmetric and spans the WCAG range", () => {
  const black = Palette.parseHex("#000000");
  const white = Palette.parseHex("#ffffff");
  assert.equal(Palette.contrast(black, white).toFixed(2), "21.00");
  assert.equal(Palette.contrast(white, black).toFixed(2), "21.00");
  assert.equal(Palette.contrast(black, black), 1);
});

check("isDark reads the background, not the scheme's name", () => {
  assert.equal(Palette.isDark("#0f0d14"), true);
  assert.equal(Palette.isDark("#e6d9b4"), false);
  // A "manuscript" that is actually a candlelit study is dark.
  assert.equal(Palette.isDark("#241c10"), true);
});

check("derive: a dark seed sets every variable main.css reads", () => {
  const vars = Palette.derive({ bg: "#0f0d14", text: "#ece0c8", accent: "#c9a227" });
  assert.equal(vars["--color-bg"], "#0f0d14");
  assert.equal(vars["--color-text"], "#ece0c8");
  assert.equal(vars["--color-accent"], "#c9a227");
  assert.equal(vars["color-scheme"], "dark");
  assert.equal(vars["--firelight-strength"], "1");
  assert.equal(vars["--surface-texture"], "none");
  // The border and the mount's edge are the same computation, so they must
  // never disagree.
  assert.equal(vars["--color-border"], vars["--illo-mount-edge"]);
  ["--color-bg-raised", "--color-text-dim", "--color-accent-text",
   "--color-border", "--illo-mount"].forEach((key) => {
    assert.ok(Palette.isHex(vars[key]), key + " should be a hex colour");
  });
  assert.match(vars["--color-highlight-bg"], /^rgba\(\d+, \d+, \d+, 0\.18\)$/);
  assert.match(vars["--ambience-shade"], /^\d+, \d+, \d+$/);
});

check("derive: a pale seed asks for more firelight, not less", () => {
  const pale = Palette.derive({ bg: "#e6d9b4", text: "#2b2418", accent: "#2f4c8f" });
  assert.equal(pale["color-scheme"], "light");
  assert.equal(pale["--firelight-strength"], "1.6");
});

check("derive: the short hex form normalises", () => {
  const short = Palette.derive({ bg: "#000", text: "#fff", accent: "#f00" });
  assert.equal(short["--color-bg"], "#000000");
  assert.equal(short["--color-text"], "#ffffff");
  assert.equal(short["--color-accent"], "#ff0000");
});

check("derive: dimmed text is held to the floor, however saturated", () => {
  // Neon magenta on dark purple: the plain 42% mix lands around 2.5:1, and
  // the back-off is what keeps the label readable.
  const seed = { bg: "#1a0a24", text: "#ff2bd1", accent: "#ff2bd1" };
  const dim = Palette.parseHex(Palette.derive(seed)["--color-text-dim"]);
  assert.ok(
    Palette.contrast(dim, Palette.parseHex(seed.bg)) >= Palette.DIM_FLOOR,
    "dimmed text must clear 4.5:1",
  );
});

check("derive: an unreachable floor falls back rather than looping", () => {
  // Text that cannot clear 4.5:1 against its own background at any mix —
  // the loop has to end at the undimmed colour, not spin.
  const vars = Palette.derive({ bg: "#808080", text: "#8a8a8a", accent: "#8a8a8a" });
  assert.equal(vars["--color-text-dim"], "#8a8a8a");
});

check("derive: the accent's label is whichever colour can be read on it", () => {
  // A pale accent needs the dark background as its label...
  const pale = Palette.derive({ bg: "#101010", text: "#f4f4f4", accent: "#f0e0a0" });
  assert.equal(pale["--color-accent-text"], "#101010");
  // ...and a dark accent on a pale page needs the pale text colour.
  const dark = Palette.derive({ bg: "#f6f2ea", text: "#141210", accent: "#2f2a55" });
  assert.equal(dark["--color-accent-text"], "#f6f2ea");
});

check("derive: a texture brings its tile size with it", () => {
  const bare = Palette.derive({ bg: "#0f0d14", text: "#ece0c8", accent: "#c9a227" });
  assert.equal(bare["--surface-texture-size"], undefined);
  const tiled = Palette.derive(
    { bg: "#0f0d14", text: "#ece0c8", accent: "#c9a227" },
    'url("/themes/hall/img/tile.jpg")',
  );
  assert.equal(tiled["--surface-texture"], 'url("/themes/hall/img/tile.jpg")');
  assert.equal(tiled["--surface-texture-size"], "512px 512px");
});

check("complete: three hexes, or it is not a scheme", () => {
  assert.equal(Palette.complete({ bg: "#000", text: "#fff", accent: "#f00" }), true);
  assert.equal(Palette.complete({ bg: "#000", text: "#fff" }), false);
  assert.equal(Palette.complete({ bg: "#000", text: "#fff", accent: "red" }), false);
  assert.equal(Palette.complete(null), false);
  assert.equal(Palette.complete("#000000"), false);
});

check("warnings: only the text-on-background pair, and only below the floor", () => {
  const template = "In {scheme}: {ratio} to 1.";
  const fine = Palette.warnings(
    { dark: { bg: "#0f0d14", text: "#ece0c8", accent: "#c9a227" } }, template);
  assert.deepEqual(fine, []);

  const bad = Palette.warnings(
    { light: { bg: "#dcdbd4", text: "#c9c8c2", accent: "#8f2f2a" } }, template);
  assert.equal(bad.length, 1);
  assert.equal(bad[0].scheme, "light");
  assert.ok(bad[0].ratio < Palette.TEXT_FLOOR);
  assert.equal(bad[0].text, "In light: " + bad[0].ratio.toFixed(1) + " to 1.");
});

check("warnings: an incomplete scheme is skipped, not raised on", () => {
  assert.deepEqual(Palette.warnings({ dark: { bg: "#000" } }, "x"), []);
  assert.deepEqual(Palette.warnings({ dark: null }, "x"), []);
  assert.deepEqual(Palette.warnings(null, "x"), []);
});

check("checks: three pairs, each with the floor it is held to", () => {
  const rows = Palette.checks({ bg: "#0f0d14", text: "#ece0c8", accent: "#c9a227" });
  assert.deepEqual(rows.map((r) => r.key), ["text", "accent", "dim"]);
  assert.equal(rows[0].ratio.toFixed(1), "14.8");
  assert.equal(rows[1].ratio.toFixed(1), "8.0");
  assert.equal(rows[2].ratio.toFixed(1), "5.4");
  rows.forEach((row) => assert.equal(row.floor, 4.5));
});

check("checks: nothing to show until all three colours are there", () => {
  assert.deepEqual(Palette.checks({ bg: "#0f0d14", text: "#ece0c8" }), []);
});

console.log("\n" + passed + " checks passed");
