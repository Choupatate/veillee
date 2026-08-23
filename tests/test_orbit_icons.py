"""The orbit pack's icons, and the properties drawing them is supposed to
guarantee (FEATURES.md F46).

`scripts/draw_orbit_icons.py` exists because an icon here is geometry
rather than illustration — so the things that make one usable are
measurable, and this file measures them instead of trusting a look at a
contact sheet. That distinction is not academic: the keyline bug these
tests now pin was invisible at 160 pixels, survived a review of a contact
sheet and a screenshot of the running app, and took a radial profile
through a single dash to find.

Three properties, each of which was violated at some point by artwork that
looked fine:

  * a stroke's light core sits *inside* its dark keyline, not on top of
    its outer half;
  * nothing is drawn past the edge of the grid, where the crop-and-pad
    step hides the flat cut inside the padded frame;
  * every icon still has ink on it at the twenty pixels the app actually
    draws it, on every scheme the pack offers.
"""

import importlib.util
import math
from pathlib import Path

import pytest
from PIL import Image

from app.palette import contrast

REPO_ROOT = Path(__file__).resolve().parent.parent
THEMES = REPO_ROOT / "app" / "static" / "themes"


def _load_script():
    path = REPO_ROOT / "scripts" / "draw_orbit_icons.py"
    spec = importlib.util.spec_from_file_location("draw_orbit_icons", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


draw = _load_script()

#: The raised surface each icon is actually drawn on, per scheme, from
#: `orbit/theme.css`. A button's background, not the page's — that is the
#: colour an icon has to survive.
ORBIT_GROUNDS = {
    "dark": (0x0C, 0x15, 0x26),
    "light": (0xC9, 0xDC, 0xF1),
}

#: What "you can see something" means, as a fraction of a 20x20 icon whose
#: pixels clear 3:1 against the ground behind them. Eight per cent is 32
#: pixels. Chosen from measurement rather than taste: every icon this
#: script draws clears it, the weakest by a little (`icon-new-person` on
#: the night side, which is mostly opaque visor), and an icon that lost its
#: keyline or half its ink would drop straight through.
INK_FLOOR = 0.08


def _ink(png, ground, size=20):
    """The fraction of an icon's pixels that stand out from the ground at
    the size the app draws it."""
    icon = Image.open(png).convert("RGBA").resize((size, size), Image.LANCZOS)
    plate = Image.new("RGB", (size, size), ground)
    plate.paste(icon, (0, 0), icon)
    pixels = plate.load()
    lit = sum(
        1
        for y in range(size)
        for x in range(size)
        if contrast(pixels[x, y], ground) >= 3.0
    )
    return lit / (size * size)


@pytest.mark.parametrize("name", sorted(draw.ICONS))
@pytest.mark.parametrize("scheme", sorted(ORBIT_GROUNDS))
def test_every_icon_has_ink_on_every_scheme_the_pack_offers(name, scheme):
    """The rule the whole pack is built on, measured rather than admired.

    No single colour in orbit's palette reads on both the night side and
    the day side, so an icon has to be a light shape inside a dark outline
    — and this is what checks that it still is once it has been shrunk to
    the size a button draws it at.
    """
    png = THEMES / "orbit" / "img" / f"{name}.png"
    assert png.is_file(), f"{name} has not been drawn"
    ink = _ink(png, ORBIT_GROUNDS[scheme])
    assert ink >= INK_FLOOR, (
        f"{name} covers only {ink:.1%} of a 20px square on the {scheme} "
        f"scheme (floor {INK_FLOOR:.0%}) — it has lost its keyline or its fill"
    )


@pytest.mark.parametrize("name", sorted(draw.ICONS))
def test_nothing_is_drawn_past_the_edge_of_the_grid(name):
    """A shape drawn off the grid is cut flat, and the cut has no keyline
    on it.

    The reason this needs a test rather than an eye: `render` trims to
    content and *then* pads, so the flat edge lands inside the padded
    frame rather than on the image border. The icon comes back looking
    framed and fine. `icon-new-person`'s plus reached x=65.7 on a 64-wide
    grid and nobody saw it for two rounds of review.
    """
    alpha = draw.draw_raw(name).getchannel("A")
    width, height = alpha.size
    edges = {
        "left": sum(alpha.getpixel((0, y)) > 8 for y in range(height)),
        "right": sum(alpha.getpixel((width - 1, y)) > 8 for y in range(height)),
        "top": sum(alpha.getpixel((x, 0)) > 8 for x in range(width)),
        "bottom": sum(alpha.getpixel((x, height - 1)) > 8 for x in range(width)),
    }
    touching = {side: n for side, n in edges.items() if n}
    assert not touching, (
        f"{name} is drawn past the grid on {touching} — move the shape in, "
        "or the cut edge ships without a keyline"
    )


def _radial(image, cx, cy, angle_deg, radii):
    """Colours sampled outward along one ray, in grid units."""
    rad = math.radians(angle_deg)
    out = []
    for r in radii:
        x = round(draw._s(cx + r * math.cos(rad)))
        y = round(draw._s(cy + r * math.sin(rad)))
        out.append(image.getpixel((x, y)))
    return out


def _bands(samples):
    """The run-length sequence of colours along a ray, ignoring the
    antialiased pixels between two bands."""
    known = {draw.NAVY: "navy", draw.CYAN: "cyan", draw.STAR: "star",
             draw.RUST: "rust", (0, 0, 0, 0): "empty"}
    out = []
    for sample in samples:
        label = known.get(sample)
        if label and (not out or out[-1] != label):
            out.append(label)
    return out


def test_an_arc_keyline_encloses_its_core():
    """The bug this file was written for.

    Pillow draws an arc's stroke inward from its bounding box, so a
    keyline and a core sharing one box both hug the outer edge and the
    core covers the keyline's outer half — the light on the outside, the
    dark within, which is the exact inverse of the rule. On the pale page
    the shape loses its outer edge entirely.

    Measured as bands along a ray: navy, then the core, then navy.
    """
    image, pen = draw._canvas()
    draw.arc(pen, 32, 32, 20, 0, 90, draw.STAR, key=12, core=5, caps=False)
    bands = _bands(_radial(image, 32, 32, 45, [r / 4 for r in range(4, 108)]))
    assert bands == ["empty", "navy", "star", "navy", "empty"], bands


def test_a_ring_keyline_encloses_its_core():
    """Same shape of bug in the same place: `ring` strokes an ellipse,
    which Pillow also draws inward from the box."""
    image, _pen = draw._canvas()
    draw.ring(image, 32, 32, 22, 22, 0, colour=draw.CYAN, key=12, core=5)
    bands = _bands(_radial(image, 32, 32, 0, [r / 4 for r in range(4, 116)]))
    assert bands == ["empty", "navy", "cyan", "navy", "empty"], bands


def test_a_stroke_keyline_encloses_its_core():
    """`stroke` never had the bug — `line()` is centred on its path — and
    this is here so that stays true if anyone rewrites it in terms of the
    other two."""
    image, pen = draw._canvas()
    draw.stroke(pen, [(10, 32), (54, 32)], draw.STAR, key=12, core=5)
    bands = _bands([image.getpixel((draw._s(32), draw._s(y)))
                    for y in [v / 4 for v in range(100, 156)]])
    assert bands == ["empty", "navy", "star", "navy", "empty"], bands


@pytest.mark.parametrize("name", sorted(draw.ICONS))
def test_each_icon_is_committed_at_the_size_the_app_expects(name):
    """160x160 with an alpha channel, the same box the generated icons
    were processed into — a pack is a skin, so the same filename has to be
    the same picture at the same size in every pack."""
    with Image.open(THEMES / "orbit" / "img" / f"{name}.png") as icon:
        assert icon.size == (draw.SIZE, draw.SIZE)
        assert icon.mode == "RGBA"


def test_the_committed_icons_match_what_the_script_draws_today():
    """The script is the artwork's source, so a hand-edited PNG is a lie
    about where the picture came from. Compared loosely — a re-encode can
    shift a pixel — but a redrawn shape moves far more than this allows.
    """
    for name in sorted(draw.ICONS):
        committed = Image.open(THEMES / "orbit" / "img" / f"{name}.png").convert("RGBA")
        fresh = draw.render(name).convert("RGBA")
        here, now = committed.tobytes(), fresh.tobytes()
        diff = sum(abs(a - b) for a, b in zip(here, now)) / len(here)
        assert diff < 2.0, (
            f"{name}.png differs from what draw_orbit_icons.py draws "
            f"(mean channel difference {diff:.2f}) — redraw it rather than "
            "editing the PNG"
        )
