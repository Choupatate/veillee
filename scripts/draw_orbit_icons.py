"""Draw the orbit pack's thirteen icons (FEATURES.md F46).

The plates in `app/static/themes/orbit/img/*.jpg` were generated and then
processed by `process_orbit_plates.py`. The icons are a different problem
and this script solves it a different way: it *draws* them, in Pillow,
from the subject list in IMAGE-PROMPTS-ORBIT.md.

Why drawn rather than generated. An icon here is four flat colours, a
dark keyline and one silhouette that has to survive being shown at twenty
pixels — that is geometry, not illustration, and it is precisely what a
generator is worst at: it softens small shapes, forgets the outline
between one image and the next, and will not hold thirteen drawings to one
style. Drawing them also makes the set *reproducible*: this file is the
artwork's source, so a colour can be changed and all thirteen redrawn,
which was never true of the generated plates.

The house rules it follows, all from IMAGE-PROMPTS-ORBIT.md:

  * **Every shape carries the dark navy keyline**, about a tenth of the
    icon's width. This is the rule the pack's first icon batch taught, and
    the table in that file is the argument: pale starlight is 14.5:1 on
    the night side and 1.11:1 on the day side, cyan is 9.6:1 and 1.36:1,
    navy is the other way round. No single colour in the palette reads on
    both schemes, so an icon has to be a light shape inside a dark outline
    — then whichever scheme you are in, one half of it carries.
  * **A line needs the keyline too**, and cannot simply *be* the keyline:
    a navy stroke vanishes at night. So every stroke here is drawn twice,
    a fat navy keyline under a narrower light core. `stroke` does that.
  * **The ring is the pack's signature shape** — the one silhouette that
    stays legible at 20px — so it recurs deliberately.
  * **No lettering, no faces.** Visors are opaque navy: an empty visor
    lets any reader be the cosmonaut.

Everything is drawn on a 64x64 grid at 10x and downsampled, which is how
the edges get their antialiasing without any of the shapes being blurry.
Output framing (trim to content, pad 2%, square, 160x160) is copied from
`process_orbit_icons.py` so these sit in the same box as the two icons
that came from the generator.

    python scripts/draw_orbit_icons.py            # writes all thirteen
    python scripts/draw_orbit_icons.py icon-tree  # or just one
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw

OUT = (Path(__file__).resolve().parent.parent
       / "app" / "static" / "themes" / "orbit" / "img")

#: The pack's palette, from IMAGE-PROMPTS-ORBIT.md's house style.
NAVY = (23, 37, 63, 255)      # #17253f — the keyline, and opaque visors
CYAN = (92, 200, 245, 255)    # #5cc8f5 — instrument cyan
STAR = (220, 230, 245, 255)   # #dce6f5 — pale starlight
RUST = (200, 98, 47, 255)     # #c8622f — life and danger, used sparingly

GRID = 64          # the coordinate space every icon is drawn in
SCALE = 10         # ...at ten times the size, for antialiasing
SIZE = 160         # ...and downsampled to this
MARGIN = 0.02      # square padding around the trimmed artwork

#: A tenth of the icon's width, which is what the prompt asks for. Every
#: keyline is this or thicker; a light core is roughly half of it.
KEY = 6.4
CORE = 3.0


def _canvas():
    px = GRID * SCALE
    im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def _s(value):
    return value * SCALE


def _inset(box, amount):
    """A bounding box pulled in on every side.

    Pillow draws an arc's or an ellipse's stroke *inward* from its
    bounding box, not centred on it. So a keyline and a light core sharing
    one box both hug the box's outer edge, and the core ends up drawn on
    top of the outer half of the keyline — the light on the outside, the
    dark within. That is the exact inverse of the rule this pack is built
    on, and it is invisible at 160px and fatal at 20: on the pale page the
    shape loses its outer edge entirely.

    Insetting the core's box by half the difference puts the two bands
    concentric, which is what "a keyline with a core" was supposed to mean
    all along. `line()` is already centred on its path, so `stroke()` never
    had this problem — which is why it took a radial measurement rather
    than a look to find.
    """
    return [box[0] + _s(amount), box[1] + _s(amount),
            box[2] - _s(amount), box[3] - _s(amount)]


def disc(draw, cx, cy, r, fill, key=KEY):
    """A filled circle inside the keyline."""
    half = key / 2
    draw.ellipse([_s(cx - r - half), _s(cy - r - half),
                  _s(cx + r + half), _s(cy + r + half)], fill=NAVY)
    draw.ellipse([_s(cx - r + half), _s(cy - r + half),
                  _s(cx + r - half), _s(cy + r - half)], fill=fill)


def _round_line(draw, points, width, colour):
    """Pillow's lines have no round caps or joints; the dots supply both.
    Without them every stroke here would end in a square corner, which
    reads as a different drawing style at 160px and as grit at 20."""
    draw.line([(_s(x), _s(y)) for x, y in points],
              fill=colour, width=round(_s(width)), joint="curve")
    for x, y in points:
        draw.ellipse([_s(x - width / 2), _s(y - width / 2),
                      _s(x + width / 2), _s(y + width / 2)], fill=colour)


def stroke(draw, points, colour, key=KEY + 3.4, core=CORE + 1.4):
    """A line, drawn twice: a navy keyline with a light core on top.

    The whole reason the pack's icons work on both schemes. Drawing the
    core alone gives a line that disappears on the day side; drawing the
    keyline alone gives one that disappears at night.
    """
    _round_line(draw, points, key, NAVY)
    _round_line(draw, points, core, colour)


def ring(im, cx, cy, rx, ry, angle, colour=STAR, key=KEY + 3.6, core=CORE + 1.0,
         fill=None):
    """The pack's signature shape: a tilted ellipse, keylined like
    everything else. With `fill`, a solid tilted disc instead — the
    antenna dish.

    Drawn into its own layer and rotated, because Pillow cannot draw a
    rotated ellipse directly. Rotating the layer rather than approximating
    the ellipse with a polygon keeps the curve clean at 10x.
    """
    px = GRID * SCALE
    layer = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    pen = ImageDraw.Draw(layer)
    box = [_s(cx - rx), _s(cy - ry), _s(cx + rx), _s(cy + ry)]
    if fill is not None:
        pen.ellipse(box, fill=fill)
    pen.ellipse(box, outline=NAVY, width=round(_s(key)))
    if fill is None:
        pen.ellipse(_inset(box, (key - core) / 2), outline=colour,
                    width=round(_s(core)))
    layer = layer.rotate(angle, resample=Image.BICUBIC, center=(_s(cx), _s(cy)))
    im.alpha_composite(layer)


def bowl(im, cx, cy, r, angle, fill=CYAN, key=KEY):
    """A half-disc, tilted — the antenna dish.

    A dish drawn as a flat filled ellipse reads as a microphone head: the
    silhouette that says "dish" is a bowl with a straight rim, not an oval.
    """
    px = GRID * SCALE
    layer = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    pen = ImageDraw.Draw(layer)
    half = key / 2
    box_out = [_s(cx - r - half), _s(cy - r - half),
               _s(cx + r + half), _s(cy + r + half)]
    box_in = [_s(cx - r + half), _s(cy - r + half),
              _s(cx + r - half), _s(cy + r - half)]
    pen.pieslice(box_out, 180, 360, fill=NAVY)
    pen.pieslice(box_in, 180, 360, fill=fill)
    layer = layer.rotate(angle, resample=Image.BICUBIC, center=(_s(cx), _s(cy)))
    im.alpha_composite(layer)


def arc(draw, cx, cy, r, start, end, colour, key=KEY + 3.4, core=CORE + 1.4,
        caps=True):
    """A keylined arc — the sound waves beside the microphone, the dashes
    of the draft planet, the open hatch.

    Pillow's arc has no caps. Rounding them is right for a short stroke
    that reads as a mark; on a long arc that reads as a *rim* the caps
    stand out as bolts, so `caps=False` leaves them square.
    """
    import math

    box = [_s(cx - r), _s(cy - r), _s(cx + r), _s(cy + r)]
    draw.arc(box, start, end, fill=NAVY, width=round(_s(key)))
    draw.arc(_inset(box, (key - core) / 2), start, end, fill=colour,
             width=round(_s(core)))
    if not caps:
        return
    # The caps sit on the keyline's mid-radius, which is where the core
    # now runs — not on the bounding box's radius.
    mid = r - key / 2
    for angle in (start, end):
        ex = cx + mid * math.cos(math.radians(angle))
        ey = cy + mid * math.sin(math.radians(angle))
        draw.ellipse([_s(ex - key / 2), _s(ey - key / 2),
                      _s(ex + key / 2), _s(ey + key / 2)], fill=NAVY)
        draw.ellipse([_s(ex - core / 2), _s(ey - core / 2),
                      _s(ex + core / 2), _s(ey + core / 2)], fill=colour)


def polygon(draw, points, fill, key=KEY):
    """A filled polygon inside the keyline — the arrowheads."""
    scaled = [(_s(x), _s(y)) for x, y in points]
    draw.line(scaled + [scaled[0]], fill=NAVY, width=round(_s(key)), joint="curve")
    for x, y in points:
        draw.ellipse([_s(x - key / 2), _s(y - key / 2),
                      _s(x + key / 2), _s(y + key / 2)], fill=NAVY)
    draw.polygon(scaled, fill=fill)
    draw.line(scaled + [scaled[0]], fill=NAVY, width=round(_s(key * 0.6)),
              joint="curve")


def box(draw, x0, y0, x1, y1, fill, radius=3, key=KEY):
    half = key / 2
    draw.rounded_rectangle(
        [_s(x0 - half), _s(y0 - half), _s(x1 + half), _s(y1 + half)],
        radius=_s(radius + half), fill=NAVY)
    draw.rounded_rectangle(
        [_s(x0 + half), _s(y0 + half), _s(x1 - half), _s(y1 - half)],
        radius=_s(max(radius - half, 1)), fill=fill)


# --- the thirteen -----------------------------------------------------------
# One function each, named for its file. The docstring is the subject line
# from IMAGE-PROMPTS-ORBIT.md's table, so a drawing that has drifted from
# what the catalogue promises is visible right here.


def icon_new_story(im, draw):
    """A ringed planet with a stylus arcing over it like an orbit."""
    disc(draw, 28, 35, 17, CYAN)
    # A thinner ring than the planet's outline, so the planet stays the
    # subject and the orbit stays a line drawn over it.
    ring(im, 28, 35, 27, 8, 22, key=KEY + 1.6, core=CORE - 0.4)
    pen = ImageDraw.Draw(im)
    stroke(pen, [(41, 21), (52, 10)], STAR, key=KEY + 4.6, core=CORE + 2.6)
    disc(pen, 53, 9, 3.4, RUST, key=KEY - 1.6)


def icon_instant(im, draw):
    """A chunky survey camera seen head-on, one round lens."""
    box(draw, 21, 10, 39, 21, CYAN, radius=3)
    box(draw, 6, 19, 58, 54, CYAN, radius=6)
    disc(draw, 32, 37, 13, STAR)
    disc(draw, 32, 37, 6, CYAN, key=KEY - 2)
    disc(draw, 49, 27, 3.2, RUST, key=KEY - 2.4)


def icon_save(im, draw):
    """A thick downward arrow, its shaft crossed by a tilted planet's ring
    seen edge-on, the arrowhead resting on a short horizontal bar."""
    stroke(draw, [(32, 8), (32, 26)], CYAN, key=KEY + 9, core=CORE + 5)
    polygon(draw, [(16, 25), (32, 46), (48, 25)], CYAN)
    # Edge-on: nearly flat, and thin, or it reads as a knot in the shaft.
    ring(im, 32, 16, 15, 3.4, 16, key=KEY + 1.2, core=CORE - 0.6)
    pen = ImageDraw.Draw(im)
    stroke(pen, [(15, 55), (49, 55)], STAR, key=KEY + 5, core=CORE + 2.6)


def icon_draft(im, draw):
    """A whole planet inside an unfinished orbit: the ring drawn as four
    thick dashes with wide gaps, the body solid.

    The catalogue asks for this the other way round — a dashed body inside
    a solid ring — and two attempts at that came back as a solid rim once
    the dashes' keylines closed up. Dashing the orbit says "not finished
    yet" just as plainly and survives 20px, so the drawing won and this
    line was corrected to match it rather than the other way about.
    """
    # Four thick dashes with wide gaps — at r=15 they came out as beads,
    # so the radius is bigger and each dash is a 58-degree run.
    # Two attempts at a dashed *body* both read as a solid rim once the
    # keylines closed up. The unfinished thing is the orbit instead: a
    # whole planet, and a ring still being drawn round it.
    disc(draw, 32, 32, 11, CYAN)
    for start in (188, 278, 8, 98):
        arc(draw, 32, 32, 23, start, start + 46, STAR,
            key=KEY + 4.6, core=CORE + 2.6, caps=False)


def icon_archive(im, draw):
    """A wide storage crate seen square-on, wider than it is tall, with a
    separate lid bar across the top and one rust band across the middle."""
    box(draw, 8, 27, 56, 53, CYAN, radius=3)
    draw.rectangle([_s(12), _s(35), _s(52), _s(44)], fill=RUST)
    box(draw, 5, 13, 59, 27, STAR, radius=3)


def icon_seal(im, draw):
    """A capsule with a single wax seal disc on its seam."""
    box(draw, 10, 12, 54, 52, CYAN, radius=10)
    # The seam has to be visible or the capsule is just a rounded square:
    # a plain navy line, no light core, because it is a join and not a
    # drawn stroke.
    # A visible band, not a hairline: the seal has to be sitting *on* a
    # join, or the icon is a round button on a rounded square.
    draw.rectangle([_s(11), _s(29.6), _s(53), _s(34.4)], fill=NAVY)
    disc(draw, 32, 32, 8.5, RUST)


def icon_source(im, draw):
    """A small antenna dish pointing up and to the right."""
    stroke(draw, [(24, 40), (14, 54)], STAR, key=KEY + 4.4, core=CORE + 2.2)
    bowl(im, 31, 30, 20, 38)
    pen = ImageDraw.Draw(im)
    stroke(pen, [(31, 30), (47, 13)], STAR, key=KEY + 3.4, core=CORE + 1.4)
    disc(pen, 48, 12, 4.0, RUST, key=KEY - 1.4)


def icon_record(im, draw):
    """A round microphone grille with two sound arcs."""
    arc(draw, 32, 32, 22, -52, 52, CYAN, key=KEY + 5, core=CORE + 2.4, caps=False)
    arc(draw, 32, 32, 22, 128, 232, CYAN, key=KEY + 5, core=CORE + 2.4, caps=False)
    disc(draw, 32, 32, 14, CYAN)
    disc(draw, 32, 32, 6.5, STAR, key=KEY - 2)


def icon_print(im, draw):
    """A flat plate emerging from a slot."""
    box(draw, 17, 6, 47, 37, STAR, radius=2)
    box(draw, 6, 36, 58, 56, CYAN, radius=4)
    draw.rectangle([_s(42), _s(45), _s(52), _s(49)], fill=RUST)


def icon_import(im, draw):
    """An arrow entering an open hatch."""
    # An open hatch: a rim with a gap on the left for the arrow to enter.
    # No caps — on a rim they read as bolts.
    arc(draw, 35, 33, 20, -56, 56, CYAN, key=KEY + 5, core=CORE + 2.8, caps=False)
    arc(draw, 35, 33, 20, 124, 236, CYAN, key=KEY + 5, core=CORE + 2.8, caps=False)
    stroke(draw, [(7, 33), (26, 33)], STAR, key=KEY + 5, core=CORE + 2.8)
    polygon(draw, [(25, 23), (44, 33), (25, 43)], CYAN)


def icon_tree(im, draw):
    """Three small moons linked by two straight struts."""
    stroke(draw, [(32, 19), (14, 47)], STAR, key=KEY + 5, core=CORE + 2.6)
    stroke(draw, [(32, 19), (50, 47)], STAR, key=KEY + 5, core=CORE + 2.6)
    disc(draw, 32, 14, 9, CYAN)
    disc(draw, 13, 50, 9, STAR)
    disc(draw, 51, 50, 9, STAR)


def icon_new_person(im, draw):
    """A helmet silhouette with a small plus beside it."""
    # Starlight rather than cyan, so the opaque navy visor reads against
    # the helmet instead of merging into its own keyline.
    disc(draw, 24, 34, 17, STAR)
    # The visor is opaque on purpose: no eyes, no face, so any reader can
    # be the cosmonaut (IMAGE-PROMPTS-ORBIT.md). Drawn as the dark D across
    # the front of the helmet rather than a centred oval — an oval in the
    # middle of a pale disc reads as an eye, which is the opposite of what
    # an empty visor is for.
    draw.rounded_rectangle([_s(11), _s(29), _s(37), _s(43)],
                           radius=_s(6), fill=NAVY)
    stroke(draw, [(51, 8), (51, 22)], RUST, key=KEY + 5, core=CORE + 2.6)
    stroke(draw, [(44, 15), (58, 15)], RUST, key=KEY + 5, core=CORE + 2.6)


def icon_group(im, draw):
    """Three helmet silhouettes inside one tilted ring."""
    # Three helmets that stay three at 20px: spread wider, drawn smaller
    # than the ring that gathers them, and starlight so the visors show.
    # No visors here: at 20px three dark ovals inside three pale discs
    # inside a ring collapse into one face. Three plain heads gathered by
    # the ring is the shape that survives.
    # Five compositions in, the thing that works is inverting it. Giving
    # each figure its own dark keyline packs three outlines into one oval
    # and they merge into a mass; making the *enclosure* the dark shape
    # and the figures light silhouettes inside it needs no per-figure
    # outline at all, and it is what the catalogue asks for anyway —
    # "three figures' silhouettes gathered inside one enclosing shape".
    # The cyan rim is what keeps the enclosure visible on the night side,
    # where a navy fill is the background.
    ring(im, 32, 33, 30, 18, 12, colour=CYAN, fill=NAVY)
    ring(im, 32, 33, 30, 18, 12, colour=CYAN, key=0.1, core=CORE - 0.4)
    pen = ImageDraw.Draw(im)
    for cx, top in ((16, 36), (32, 32), (48, 36)):
        pen.rounded_rectangle([_s(cx - 6.2), _s(top), _s(cx + 6.2), _s(top + 12)],
                              radius=_s(5), fill=STAR)
        # A hair of navy between head and shoulders, or each figure reads
        # as one pill rather than as a person.
        pen.ellipse([_s(cx - 5.0), _s(top - 12.4), _s(cx + 5.0), _s(top - 2.4)],
                    fill=STAR)


ICONS = {
    "icon-new-story": icon_new_story,
    "icon-instant": icon_instant,
    "icon-save": icon_save,
    "icon-draft": icon_draft,
    "icon-archive": icon_archive,
    "icon-seal": icon_seal,
    "icon-source": icon_source,
    "icon-record": icon_record,
    "icon-print": icon_print,
    "icon-import": icon_import,
    "icon-tree": icon_tree,
    "icon-new-person": icon_new_person,
    "icon-group": icon_group,
}


def draw_raw(name):
    """The icon on its full 64x64 grid, before any cropping.

    Separate from `render` so a test can see what `render` would throw
    away. The crop-and-pad below trims to content and then adds a margin,
    which means a shape drawn past the edge of the grid comes back
    *looking* fine — its flat, un-keylined cut sits inside the padded
    frame rather than on the image border, where anyone would notice it.
    `icon-new-person`'s plus arm reached x=65.7 on a 64-wide grid for
    exactly that reason.
    """
    im, draw = _canvas()
    ICONS[name](im, draw)
    return im


def render(name):
    im = draw_raw(name)

    # Same framing as process_orbit_icons.py, so a drawn icon and a
    # generated one sit in the same box.
    bbox = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox is None:
        raise SystemExit(f"{name}: nothing was drawn")
    art = im.crop(bbox)
    w, h = art.size
    side = round(max(w, h) * (1 + MARGIN * 2))
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(art, ((side - w) // 2, (side - h) // 2), art)
    return square.resize((SIZE, SIZE), Image.LANCZOS)


def main(argv):
    names = argv[1:] or list(ICONS)
    unknown = [n for n in names if n not in ICONS]
    if unknown:
        raise SystemExit(f"unknown icon(s): {', '.join(unknown)}")
    OUT.mkdir(parents=True, exist_ok=True)
    for name in names:
        path = OUT / f"{name}.png"
        render(name).save(path, format="PNG", optimize=True)
        print(f"{name:18} -> {path.relative_to(OUT.parents[4])}  "
              f"{path.stat().st_size // 1024}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
