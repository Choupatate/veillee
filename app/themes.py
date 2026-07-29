"""Theme packs (FEATURES.md F46) — the app's art direction as a folder.

A pack is `app/static/themes/<name>/`: a `theme.css` re-declaring whichever
of main.css's colour variables it wants, and an `img/` folder of the
illustrations and icons. Templates never name a pack; they call
`theme_img("help-lantern.jpg")`, and this module answers with the current
pack's copy when it has one and the default pack's otherwise.

That fallback is the whole design. A pack of 35 pictures is a wall nobody
starts climbing; a pack that works the day its palette is written, and
takes its artwork one picture at a time, is a ramp. It also means a pack
only ever has to draw what it wants to change.

Two conventions hold it together:

- **A pack is a skin, not a rename.** The same filename means the same
  picture in every pack — `icon-save.png` is whatever that pack thinks a
  save button looks like. Rename a file in one pack and it silently falls
  back to the default's, forever.
- **Which pack a book uses is the book's own decision**, set once with
  `STORYBOOK_THEME`, not a per-reader toggle. The art direction is the
  book's identity; light/dark/manuscript stays the per-reader choice, and
  a pack is expected to look right in all three.
"""

import re
from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent / "static" / "themes"

#: The pack every other pack falls back to, and the one a book gets when
#: `STORYBOOK_THEME` is unset. It is the only pack guaranteed to be
#: complete.
DEFAULT_THEME = "ranch"

_THEME_NAME_RE = re.compile(r"^[a-z0-9-]{1,32}$")
_ASSET_NAME_RE = re.compile(r"^[a-z0-9._-]+$")


def available_themes() -> list[str]:
    """Every pack shipped with the app, alphabetically."""
    if not THEMES_DIR.is_dir():
        return []
    return sorted(p.name for p in THEMES_DIR.iterdir() if p.is_dir())


def is_valid_theme(name: str) -> bool:
    """A real pack, named safely. The regex matters as much as the
    directory check: this name is pasted into URLs and filesystem paths."""
    return bool(
        name
        and ".." not in name
        and _THEME_NAME_RE.match(name)
        and (THEMES_DIR / name).is_dir()
    )


def image_url_path(theme: str, filename: str) -> str:
    """The `static`-relative path of `filename` for `theme`, falling back to
    the default pack when this one doesn't draw it — e.g.
    "themes/orbit/img/icon-save.png" or "themes/ranch/img/icon-save.png".

    Returns the default pack's path for an unknown filename too. A missing
    picture is a missing picture either way, and inventing a path inside an
    unvalidated name is how a traversal starts.
    """
    if _ASSET_NAME_RE.match(filename or "") and ".." not in filename:
        if theme != DEFAULT_THEME and is_valid_theme(theme):
            if (THEMES_DIR / theme / "img" / filename).is_file():
                return f"themes/{theme}/img/{filename}"
    return f"themes/{DEFAULT_THEME}/img/{filename}"


def stylesheet_url_path(theme: str) -> str | None:
    """The pack's own stylesheet, or None when it doesn't have one (the
    default pack doesn't need one — its colours are main.css's own)."""
    if not is_valid_theme(theme):
        return None
    if (THEMES_DIR / theme / "theme.css").is_file():
        return f"themes/{theme}/theme.css"
    return None
