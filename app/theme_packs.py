"""Making, changing and deleting a family's own theme pack (F50).

The read side lives in `themes.py`, which treats a made pack exactly like
a shipped one. This is everything that writes, and it lives under
`<stories>/themes/<name>/` — in the data folder, with the memories,
because artwork someone drew for their own book has to survive an app
update and travel in the backup zip like everything else they made.

A pack on disk is the same three things a shipped pack is: a `theme.json`,
an `img/` folder, and nothing else. Which means a family that stops using
this app still has a folder of their pictures and a readable file saying
what colours they chose.

Three rules the rest of the app already lives by, applied here:

- **The filename allowlist is the catalogue.** Only the 37 names in
  `theme_catalog` can ever be written into a pack, so no upload can invent
  a path — the strongest form of the "never build a path from user input"
  rule this codebase has, because the input isn't used to build the path
  at all, only to choose from a fixed list.
- **Uploaded images are re-encoded**, never written verbatim (`storage.py`
  does the same for photos).
- **`theme.json` is written tmp-then-replace**, so a save that dies
  halfway leaves the previous palette intact rather than a half-written
  file the pack can't be read from.
"""

import json
import os
import re
import unicodedata
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter

from . import palette as palette_mod
from . import themes
from .theme_catalog import BY_FILENAME, ICON, ORNAMENT, TILE

#: How far a pixel may sit from the sampled background before it counts as
#: artwork. Generated backgrounds are rarely perfectly flat — a faint
#: vignette is normal — so this tolerates more than a true flat fill needs.
KEY_TOLERANCE = 38
#: Margin left around a cut-out icon, as a fraction of its long edge.
ICON_MARGIN = 0.02
JPEG_QUALITY = 82
#: Names that would collide with a page of the theme editor itself, since
#: `/themes/new` has to keep meaning the new-theme form.
RESERVED_NAMES = frozenset({"new"})


class PackError(Exception):
    """Something the person filling in the form can fix."""


def slugify(label: str) -> str:
    """A folder name from what someone typed. ASCII, lowercase, hyphens —
    the same shape `themes.is_valid_theme` accepts, since this name ends up
    in URLs and on disk."""
    text = unicodedata.normalize("NFKD", label or "")
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:32].strip("-")


def pack_dir(user_dir, name) -> Path:
    """The folder for a made pack. Validated by the caller — every public
    function here checks the name before touching the filesystem."""
    return Path(user_dir) / name


def _check_name(user_dir, name):
    if not name or not themes._named_safely(name):
        raise PackError(
            "A theme name needs at least one letter or number, and can only "
            "contain letters, numbers and hyphens."
        )
    if themes.is_builtin_theme(name):
        raise PackError(f"“{name}” is the name of a theme that came with the app.")
    if name in RESERVED_NAMES:
        raise PackError(f"“{name}” is a word the app uses for its own pages.")
    return name


def list_packs(user_dir) -> list[dict]:
    """Every made pack, with what the admin page needs to list them."""
    out = []
    for name in themes.user_themes(user_dir):
        manifest = read_pack(user_dir, name)
        out.append(
            {
                "name": name,
                "label": manifest.get("label") or name,
                "description": manifest.get("description") or "",
                "schemes": manifest.get("schemes") or [],
                "drawn": len(drawn_assets(user_dir, name)),
                "total": len(BY_FILENAME),
            }
        )
    return out


def read_pack(user_dir, name) -> dict:
    try:
        raw = (pack_dir(user_dir, name) / "theme.json").read_text(encoding="utf-8")
        data = json.loads(raw)
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def drawn_assets(user_dir, name) -> set:
    """Which of the catalogue this pack has drawn for itself. Everything
    else is borrowed from the default pack, which is what lets a pack be
    used from its first picture."""
    img_dir = pack_dir(user_dir, name) / "img"
    if not img_dir.is_dir():
        return set()
    return {p.name for p in img_dir.iterdir() if p.is_file() and p.name in BY_FILENAME}


def _validate_palette(scheme_colors) -> dict:
    """Three hex colours per scheme, and nothing else gets through. These
    end up inside a stylesheet, so the allowlist is the whole defence."""
    clean = {}
    for scheme, seed in (scheme_colors or {}).items():
        if scheme not in themes.DEFAULT_COLOR_SCHEMES:
            raise PackError(f"There is no “{scheme}” colour scheme.")
        if not isinstance(seed, dict):
            raise PackError(f"The {scheme} scheme is missing its colours.")
        picked = {}
        for key in palette_mod.SEEDS:
            value = (seed.get(key) or "").strip()
            if not palette_mod.is_hex(value):
                raise PackError(
                    f"The {scheme} scheme's {key} colour needs to be a hex "
                    "colour like #1a2b3c."
                )
            picked[key] = value.lower()
        clean[scheme] = picked
    if not clean:
        raise PackError("A theme needs at least one colour scheme.")
    return clean


def _swatch_from(clean_palette, schemes) -> list:
    """The dots the nav picker shows. Derived rather than asked for: the
    first scheme's background and accent, plus the palest background, which
    is what makes two packs tellable apart at a glance."""
    first = clean_palette[schemes[0]]
    dots = [first["bg"], first["accent"]]
    palest = max(
        clean_palette.values(),
        key=lambda seed: palette_mod.relative_luminance(palette_mod.parse_hex(seed["bg"])),
    )
    if palest["bg"] not in dots:
        dots.append(palest["bg"])
    return dots


#: What body text has to clear against its own background to be readable
#: (WCAG AA). Reported, never enforced: it is someone's book, and a
#: deliberate choice is allowed — but a choice nobody can read should be a
#: choice, not a surprise.
TEXT_FLOOR = 4.5


def palette_warnings(scheme_colors) -> list[str]:
    """Anything measurably wrong with a palette, in words.

    Only the text-on-background pair is checked, because it is the one no
    derivation downstream can rescue: everything else here is mixed *from*
    those two, so if they can't be told apart, nothing made from them can
    be either.
    """
    out = []
    for scheme, seed in (scheme_colors or {}).items():
        try:
            ratio = palette_mod.contrast(
                palette_mod.parse_hex(seed["text"]), palette_mod.parse_hex(seed["bg"])
            )
        except (KeyError, TypeError, ValueError):
            continue
        if ratio < TEXT_FLOOR:
            out.append(
                f"In the {scheme} scheme the text colour is hard to read on "
                f"that background ({ratio:.1f} to 1, where 4.5 is the usual "
                "floor). It is saved either way — but try a lighter or "
                "darker text colour."
            )
    return out


def save_pack(user_dir, name, *, label, description, scheme_colors) -> str:
    """Create or update a pack's `theme.json`. Returns the pack's name.

    Everything about a pack except its pictures is here, so this is the
    one write that has to be atomic: a reader loading the book while it
    happens sees either the old palette or the new one.
    """
    _check_name(user_dir, name)
    clean = _validate_palette(scheme_colors)
    # Ordered the way main.css declares them, so the nav toggle cycles in a
    # predictable direction rather than in dictionary order.
    schemes = [s for s in themes.DEFAULT_COLOR_SCHEMES if s in clean]
    label = (label or "").strip()[:32] or name.replace("-", " ").title()

    manifest = {
        "label": label,
        "description": (description or "").strip()[:2000],
        "schemes": schemes,
        "palette": {s: clean[s] for s in schemes},
        "swatch": _swatch_from(clean, schemes),
    }
    directory = pack_dir(user_dir, name)
    (directory / "img").mkdir(parents=True, exist_ok=True)
    target = directory / "theme.json"
    tmp = directory / "theme.json.tmp"
    tmp.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, target)
    return name


#: Pictures main.css reaches through a CSS variable rather than through an
#: `<img>`, so a template's `theme_img()` never sees them. A pack that
#: ships its own `theme.css` (orbit) redeclares these by hand; a made pack
#: has no such file, so its stylesheet has to declare them or its own
#: divider and brand mark are drawn and never shown.
CSS_ASSETS = {
    "rope-divider.png": "--flourish-image",
    "brand-star.png": "--brand-mark",
}


def render_stylesheet(user_dir, name) -> str:
    """The pack's CSS, generated from its palette every time it is asked
    for rather than written to disk: one source of truth, and no stale
    stylesheet to explain if a save is interrupted.

    The `url()`s are absolute, and that is not fussiness. These variables
    are *declared* here but *used* in main.css, and a relative URL inside a
    custom property is resolved against the stylesheet that uses it — so
    `img/x.png` was fetched from `/static/css/img/x.png` and 404ed, leaving
    the default pack's ornament on screen and no error anywhere to explain
    why. An absolute path cannot be misresolved.
    """
    manifest = read_pack(user_dir, name)
    drawn = drawn_assets(user_dir, name)
    extra = {
        variable: f'url("/themes/{name}/img/{filename}")'
        for filename, variable in CSS_ASSETS.items()
        if filename in drawn
    }
    return palette_mod.render_css(
        manifest.get("palette") or {},
        manifest.get("schemes") or [],
        extra=extra,
        name=manifest.get("label") or name,
    )


# --- pictures ----------------------------------------------------------------


def _key_background(im):
    """Cut a flat background away by flooding in from the corners, so an
    enclosed area *inside* the artwork — the hole in a ring, the gap in a
    dashed shape — stays part of the icon rather than being punched out
    with it."""
    w, h = im.size
    px = im.load()
    seen = bytearray(w * h)
    queue = deque()
    corners = ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))
    for corner in corners:
        queue.append(corner)
        seen[corner[1] * w + corner[0]] = 1
    seeds = [im.getpixel(c) for c in corners]
    ref = tuple(sum(s[i] for s in seeds) // len(seeds) for i in range(3))

    mask = Image.new("L", (w, h), 0)
    mpx = mask.load()
    while queue:
        x, y = queue.popleft()
        r, g, b = px[x, y][:3]
        if abs(r - ref[0]) + abs(g - ref[1]) + abs(b - ref[2]) > KEY_TOLERANCE * 3:
            continue
        mpx[x, y] = 255
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                seen[ny * w + nx] = 1
                queue.append((nx, ny))
    # Close the pinholes the tolerance leaves along a soft edge.
    return mask.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.MinFilter(5))


def _has_transparency(im) -> bool:
    return im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 250


def _prepare_cutout(im, asset):
    """An icon or ornament: transparent, trimmed to what was drawn, and
    centred in the shape the app draws it at.

    An upload that is already transparent is taken at its word; a flat
    background is cut away, which is what the prompt asks the generator
    for. Getting this wrong in the safe direction only costs a background
    the person can remove themselves.
    """
    if _has_transparency(im):
        rgba = im.convert("RGBA")
    else:
        flat = im.convert("RGB")
        alpha = _key_background(flat).point(lambda v: 255 - v)
        rgba = flat.convert("RGBA")
        rgba.putalpha(alpha)

    bbox = rgba.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox:
        rgba = rgba.crop(bbox)

    if asset.width == asset.height:
        w, h = rgba.size
        side = round(max(w, h) * (1 + ICON_MARGIN * 2))
        square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        square.paste(rgba, ((side - w) // 2, (side - h) // 2), rgba)
        rgba = square
    rgba.thumbnail((asset.width, asset.height), Image.LANCZOS)
    return rgba


def save_asset(user_dir, name, filename, fileobj) -> str:
    """Take one uploaded picture into a pack. Returns the filename written.

    Never writes the bytes it was given: everything is decoded, reshaped
    and re-encoded, so an upload cannot smuggle anything through as an
    image the way a verbatim copy could.
    """
    _check_name(user_dir, name)
    asset = BY_FILENAME.get(filename)
    if asset is None:
        raise PackError("That isn't one of this book's pictures.")
    try:
        im = Image.open(fileobj)
        im.load()
    except Exception:
        raise PackError("That file isn't an image the app can read.")

    img_dir = pack_dir(user_dir, name) / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    target = img_dir / asset.filename
    tmp = img_dir / (asset.filename + ".tmp")

    if asset.kind in (ICON, ORNAMENT):
        _prepare_cutout(im, asset).save(tmp, format="PNG", optimize=True)
    else:
        rgb = im.convert("RGB")
        if asset.kind == TILE:
            # A tile has to stay the shape it tiles at, so this is the one
            # place the picture is fitted rather than merely capped.
            rgb = rgb.resize((asset.width, asset.height), Image.LANCZOS)
        else:
            rgb.thumbnail((asset.width, asset.height), Image.LANCZOS)
        rgb.save(tmp, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    os.replace(tmp, target)
    return asset.filename


def remove_asset(user_dir, name, filename) -> bool:
    """Put one picture back to the default pack's. Returns whether there
    was one to remove."""
    _check_name(user_dir, name)
    if filename not in BY_FILENAME:
        return False
    path = pack_dir(user_dir, name) / "img" / filename
    if not path.is_file():
        return False
    path.unlink()
    return True


def delete_pack(user_dir, name) -> bool:
    """Delete a made pack and everything in it.

    Deliberately shallow: it unlinks the files it knows about and then asks
    the directories to go, so a folder someone put something else in is
    left standing rather than taken with it. This app deletes almost
    nothing (F12's memos are the other case), and a pack full of artwork
    someone drew deserves the same care.
    """
    _check_name(user_dir, name)
    directory = pack_dir(user_dir, name)
    if not directory.is_dir():
        return False
    img_dir = directory / "img"
    if img_dir.is_dir():
        for child in img_dir.iterdir():
            if child.is_file() and child.name in BY_FILENAME:
                child.unlink()
        try:
            img_dir.rmdir()
        except OSError:
            pass
    for leftover in ("theme.json", "theme.json.tmp"):
        path = directory / leftover
        if path.is_file():
            path.unlink()
    try:
        directory.rmdir()
    except OSError:
        return False
    return True
