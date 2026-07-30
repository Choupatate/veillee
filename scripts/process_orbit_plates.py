"""Process the orbit theme pack's generated illustrations (FEATURES.md F46).

Kept in the repo rather than thrown away because the next batch of plates
needs the same three passes, and two of them are not obvious. Point
`UPLOADS` at the folder of generations and run it.

Three things per file:
  1. strip the cream paper border some generations came back with — it would
     fight the pack's dark `--illo-mount` and read as a double frame;
  2. paint out the generator's sparkle watermark in the bottom-right corner;
  3. downscale to roughly 2x display size and save JPEG q82.
"""
import os
import sys
from pathlib import Path

from PIL import Image, ImageStat

UPLOADS = Path(os.environ.get("ORBIT_PLATES", "."))
OUT = Path(__file__).resolve().parent.parent / "app" / "static" / "themes" / "orbit" / "img"

# source stem -> (output name, long edge)
ASSETS = {
    "26cf2215-3914": ("login-campfire.jpg", 856),
    "646b6b20-3887": ("person-oval.jpg", 732),
    "1534805c-3888": ("empty-chest.jpg", 729),
    "802471b4-3915": ("group-circle.jpg", 860),
    "42b94658-3890": ("sealed-letter.jpg", 620),
    "bd2bee74-3891": ("firsts-boots.jpg", 760),
    "6a8e7374-3892": ("growth-doorpost.jpg", 760),
    "442fc70f-3893": ("almanac-book.jpg", 700),
    "103594f6-3894": ("history-pages.jpg", 720),
    "0e0d5316-3895": ("accounts-keys.jpg", 760),
    "5376ad86-3896": ("invite-card.jpg", 700),
    "01e7b288-3908": ("write-link-pass.jpg", 700),
    "1e9aa30b-3909": ("help-lantern.jpg", 700),
    "ec5ca068-3910": ("book-frame.jpg", 897),
    "35c1ce6a-3911": ("instant-camera.jpg", 652),
    "d9839ca4-3912": ("tree-sapling.jpg", 760),
    "61897a88-3913": ("tumbleweed.jpg", 900),
}


def trim_paper_border(im):
    """Crop a uniformly light margin, if there is one. Only strips lines that
    are both bright and flat, so an illustration whose own artwork reaches
    the edge (a lit horizon, a pale regolith floor) is never cut into."""
    w, h = im.size

    def line_is_border(box):
        stat = ImageStat.Stat(im.crop(box).convert("L"))
        return stat.mean[0] > 195 and stat.stddev[0] < 34

    top = 0
    while top < h // 4 and line_is_border((0, top, w, top + 1)):
        top += 1
    bottom = h
    while bottom > h * 3 // 4 and line_is_border((0, bottom - 1, w, bottom)):
        bottom -= 1
    left = 0
    while left < w // 4 and line_is_border((left, top, left + 1, bottom)):
        left += 1
    right = w
    while right > w * 3 // 4 and line_is_border((right - 1, top, right, bottom)):
        right -= 1

    if (left, top, right, bottom) == (0, 0, w, h):
        return im, 0
    return im.crop((left, top, right, bottom)), max(top, left, w - right, h - bottom)


def remove_watermark(im):
    """Paint out the sparkle the generator stamps into the bottom-right.

    It sits at a fixed inset — measured across these generations at 97 to
    144 pixels from both the right and the bottom edge, about 47 pixels
    across — so it is covered by geometry rather than by detection, which
    is the only thing that works on the plates where it is a pale mark on
    pale regolith. The cover is the same box copied from directly above:
    backgrounds here are locally uniform vertically, and whatever seam is
    left lands well under what survives the downscale.
    """
    w, h = im.size
    pad = 10
    box = (w - 144 - pad, h - 144 - pad, w - 97 + pad, h - 97 + pad)
    ph = box[3] - box[1]
    src_top = box[1] - ph - 6
    if src_top < 0:
        return im, False
    patch = im.crop((box[0], src_top, box[2], src_top + ph))
    out = im.copy()
    out.paste(patch, (box[0], box[1]))
    return out, True


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for stem, (name, long_edge) in ASSETS.items():
        src = UPLOADS / f"{stem}.png"
        im = Image.open(src).convert("RGB")
        before = im.size
        im, marked = remove_watermark(im)
        im, trimmed = trim_paper_border(im)
        w, h = im.size
        scale = long_edge / max(w, h)
        if scale < 1:
            im = im.resize((round(w * scale), round(h * scale)), Image.LANCZOS)
        im.save(OUT / name, format="JPEG", quality=82, optimize=True)
        size_kb = (OUT / name).stat().st_size // 1024
        print(f"{name:22} {before} -> {im.size}  border:{trimmed:>3}px  "
              f"mark:{'removed' if marked else 'none':7}  {size_kb}KB")


if __name__ == "__main__":
    sys.exit(main())
