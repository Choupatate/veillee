"""The theme editor's live preview has to agree with the server (F52).

`app/static/js/palette-logic.js` is a port of `app/palette.py`, and a port
is a thing that drifts. The preview's whole claim is that what a family
sees while they type is what their book will look like once they save, so
this file runs the same seeds through both and fails on the first hex that
differs.

Two reasons this is a real risk rather than a theoretical one: Python's
`round()` is half-to-even and JavaScript's `Math.round` is half-up, and
both `_mix_to_floor` and `_mix_up_to_floor` are iterative back-offs whose
result depends on accumulating `amount -= 0.04` in exactly the same order.
Neither shows up in a spot check; both show up here.

Skipped, not failed, when node isn't on PATH — the app has no Node
dependency and never should.
"""
import json
import shutil
import subprocess
from pathlib import Path

import pytest

from app import palette

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULE = REPO_ROOT / "app" / "static" / "js" / "palette-logic.js"
NODE = shutil.which("node")

#: Reads seeds as JSON on the command line, prints what the browser would
#: derive from them. Kept here rather than in tests/js/ because it is a
#: fixture for this test, not a test of its own.
DRIVER = """
const Palette = require(process.argv[1]);
const seeds = JSON.parse(process.argv[2]);
console.log(JSON.stringify(seeds.map((seed) => Palette.derive(seed))));
"""

#: Palettes that exist, palettes someone might plausibly type, and
#: palettes chosen to be awkward: pure black and white, a pair too close
#: to dim, a saturated neon that forces the back-off loop to run, the
#: short hex form, and a background sitting either side of the
#: dark/light boundary.
NAMED_SEEDS = [
    {"bg": "#141210", "text": "#e8e2d9", "accent": "#d9a441"},  # ranch dark
    {"bg": "#faf6ef", "text": "#2a2520", "accent": "#a9701c"},  # ranch light
    {"bg": "#ece1c8", "text": "#3a2c1c", "accent": "#8a4a2a"},  # ranch manuscript
    {"bg": "#04060d", "text": "#dbe7f7", "accent": "#5cc8f5"},  # orbit dark
    {"bg": "#dbe9f8", "text": "#0d2740", "accent": "#14567f"},  # orbit light
    {"bg": "#0f0d14", "text": "#ece0c8", "accent": "#c9a227"},
    {"bg": "#e6d9b4", "text": "#2b2418", "accent": "#2f4c8f"},
    {"bg": "#000000", "text": "#ffffff", "accent": "#ff0000"},
    {"bg": "#ffffff", "text": "#000000", "accent": "#0000ff"},
    {"bg": "#000", "text": "#fff", "accent": "#f0a"},  # short form
    {"bg": "#808080", "text": "#8a8a8a", "accent": "#8a8a8a"},  # floor unreachable
    {"bg": "#1a0a24", "text": "#ff2bd1", "accent": "#39ff14"},  # neon
    {"bg": "#707070", "text": "#898989", "accent": "#00ffff"},
    {"bg": "#767676", "text": "#111111", "accent": "#ffffff"},  # either side of 0.4
    {"bg": "#757575", "text": "#eeeeee", "accent": "#000000"},
]


def _sweep():
    """A deterministic spread across the whole cube.

    Deliberately not random: a cross-language comparison that only fails
    on some runs is worse than one that never runs at all.
    """
    seeds = []
    for i in range(0, 256, 17):
        for j in range(0, 256, 51):
            bg = "#%02x%02x%02x" % (i, (i * 3) % 256, j)
            text = "#%02x%02x%02x" % (255 - i, (j * 7) % 256, (i + j) % 256)
            accent = "#%02x%02x%02x" % ((i * 5) % 256, j, (255 - j) % 256)
            seeds.append({"bg": bg, "text": text, "accent": accent})
    return seeds


ALL_SEEDS = NAMED_SEEDS + _sweep()


def _derived_in_node(seeds):
    result = subprocess.run(
        [NODE, "-e", DRIVER, str(MODULE), json.dumps(seeds)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_palette_logic_js_matches_palette_py():
    ours = [palette.derive(seed) for seed in ALL_SEEDS]
    theirs = _derived_in_node(ALL_SEEDS)
    assert len(ours) == len(theirs) == len(ALL_SEEDS)

    for seed, mine, yours in zip(ALL_SEEDS, ours, theirs):
        # Compared key by key so a failure names the variable, not a wall
        # of JSON. Same keys, same values, same order.
        assert list(mine) == list(yours), f"different variables for {seed}"
        for name, value in mine.items():
            assert yours[name] == value, (
                f"{name} differs for {seed}: python {value!r}, browser "
                f"{yours[name]!r}"
            )


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_palette_logic_js_matches_on_a_texture():
    seed = {"bg": "#0f0d14", "text": "#ece0c8", "accent": "#c9a227"}
    texture = 'url("/themes/hall/img/tree-map-tile.jpg")'
    mine = palette.derive(seed, texture)
    result = subprocess.run(
        [NODE, "-e",
         "const P = require(process.argv[1]);"
         "console.log(JSON.stringify(P.derive(JSON.parse(process.argv[2]),"
         " process.argv[3])));",
         str(MODULE), json.dumps(seed), texture],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == mine


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_palette_logic_js_agrees_about_which_schemes_are_dark():
    """`is_dark` decides `color-scheme`, which decides how the browser
    draws form controls and scrollbars. A preview that disagrees about it
    is showing the wrong world, not a slightly wrong colour."""
    backgrounds = [seed["bg"] for seed in ALL_SEEDS]
    result = subprocess.run(
        [NODE, "-e",
         "const P = require(process.argv[1]);"
         "console.log(JSON.stringify(JSON.parse(process.argv[2])"
         ".map((bg) => P.isDark(bg))));",
         str(MODULE), json.dumps(backgrounds)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout) == [
        bool(palette.is_dark(bg)) for bg in backgrounds
    ]


@pytest.mark.skipif(NODE is None, reason="node not available on PATH")
def test_palette_logic_js_warns_where_theme_packs_would():
    """The live warning under the preview and the one `save_pack` returns
    have to fire on the same palettes, or the preview is either crying
    wolf or keeping quiet about a palette the server will complain
    about."""
    from app import theme_packs

    palettes = [
        {"dark": ALL_SEEDS[0], "light": ALL_SEEDS[1]},
        {"dark": {"bg": "#808080", "text": "#8a8a8a", "accent": "#8a8a8a"}},
        {"light": {"bg": "#dcdbd4", "text": "#c9c8c2", "accent": "#8f2f2a"}},
        {"dark": {"bg": "#000000", "text": "#ffffff", "accent": "#ff0000"}},
    ]
    result = subprocess.run(
        [NODE, "-e",
         "const P = require(process.argv[1]);"
         "console.log(JSON.stringify(JSON.parse(process.argv[2]).map("
         "(p) => P.warnings(p, '{scheme}|{ratio}').map((w) => w.scheme))));",
         str(MODULE), json.dumps(palettes)],
        cwd=REPO_ROOT, capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    theirs = json.loads(result.stdout)

    for scheme_colors, flagged in zip(palettes, theirs):
        server = theme_packs.palette_warnings(scheme_colors)
        assert len(server) == len(flagged), (
            f"{scheme_colors}: server warned {len(server)}, browser "
            f"{len(flagged)}"
        )
        for scheme in flagged:
            assert any(scheme in line for line in server)


def test_the_preview_module_is_not_wired_into_a_page_that_needs_it_absent():
    """A guard for the rule the file's own banner states: palette-logic.js
    is pure. If it ever grows a DOM reference it stops being testable
    under Node, and this test is where that shows up."""
    source = MODULE.read_text(encoding="utf-8")
    for forbidden in ("document.", "window.", "localStorage", "fetch("):
        assert forbidden not in source, (
            f"palette-logic.js must stay DOM-free; found {forbidden!r}"
        )
