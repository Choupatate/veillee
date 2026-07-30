"""Process the orbit theme pack's generated icons (FEATURES.md F46).

The illustrations go through `process_orbit_plates.py`; icons are a
different shape of problem and follow F22's rules instead — transparent
PNG, no plate, 160x160, bold enough to survive 20px.

Four passes per file:
  1. cover the generator's corner sparkle, which sits at the same fixed
     inset as on the plates and would otherwise survive the keying as a
     little opaque ghost floating beside the icon;
  2. key the flat mid-grey background to transparent by flooding in from
     the corners, so an enclosed grey area *inside* the artwork (the hole
     in a ring, the gap in a dashed circle) stays part of the icon rather
     than being punched out with it;
  3. trim to the drawn content and pad to a square with a small margin;
  4. downscale to 160x160.

Point `ORBIT_ICONS` at the folder of generations and run it.
"""

import os
import sys
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

UPLOADS = Path(os.environ.get("ORBIT_ICONS", "."))
OUT = Path(__file__).resolve().parent.parent / "app" / "static" / "themes" / "orbit" / "img"

#: Only the generations that passed review are listed. Add a line when a
#: new icon lands; see IMAGE-PROMPTS-ORBIT.md for what "passed" means here.
ICONS = {
    "fb0dc132-3916": "icon-new-story.png",
    "acb1dce3-3917": "icon-instant.png",
}

#: How far a pixel may sit from the sampled background before it counts as
#: artwork. The generations' "plain" grey has a faint vignette, so this has
#: to tolerate more than a flat fill would need.
TOLERANCE = 38
#: Square margin around the trimmed artwork, as a fraction of the long edge.
MARGIN = 0.02
SIZE = 160


def cover_corner_mark(im):
    """Paint the generator's sparkle out with the background colour before
    keying — it is lighter than the background, so the flood would stop at
    it and leave it behind as an opaque speck."""
    w, h = im.size
    pad = 12
    box = (w - 144 - pad, h - 144 - pad, w - 97 + pad, h - 97 + pad)
    if box[0] < 0 or box[1] < 0:
        return im
    out = im.copy()
    out.paste(im.getpixel((4, h // 2)), box)
    return out


def background_mask(im):
    """Flood from every corner, so only background *connected to the edge*
    is keyed out."""
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    queue = deque()
    for start in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
        queue.append(start)
        seen[start[1] * w + start[0]] = 1
    seeds = [im.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    ref = tuple(sum(c[i] for c in seeds) // len(seeds) for i in range(3))

    mask = Image.new("L", (w, h), 0)
    mpx = mask.load()
    while queue:
        x, y = queue.popleft()
        r, g, b = px[x, y][:3]
        if abs(r - ref[0]) + abs(g - ref[1]) + abs(b - ref[2]) > TOLERANCE * 3:
            continue
        mpx[x, y] = 255
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                seen[ny * w + nx] = 1
                queue.append((nx, ny))
    # Close pinholes the tolerance left along soft edges.
    mask = mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))
    return mask


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, name in ICONS.items():
        im = Image.open(UPLOADS / f"{stem}.png").convert("RGB")
        before = im.size
        im = cover_corner_mark(im)

        alpha = background_mask(im).point(lambda v: 255 - v)
        rgba = im.convert("RGBA")
        rgba.putalpha(alpha)

        bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
        rgba = rgba.crop(bbox)
        w, h = rgba.size
        side = round(max(w, h) * (1 + MARGIN * 2))
        square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        square.paste(rgba, ((side - w) // 2, (side - h) // 2), rgba)
        square = square.resize((SIZE, SIZE), Image.LANCZOS)
        square.save(OUT / name, format="PNG", optimize=True)
        kb = (OUT / name).stat().st_size // 1024
        print(f"{name:22} {before} -> content {w}x{h} -> {SIZE}x{SIZE}  {kb}KB")


if __name__ == "__main__":
    sys.exit(main())
