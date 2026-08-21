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
- **A pack is expected to look right in every scheme it offers.** The
  reader picks light/dark/manuscript independently of the pack, so a pack
  that only works in the dark should say so in its `theme.json` rather
  than hope.

`STORYBOOK_THEME` names the book's pack. A reader can put a different one
on their own screen from the nav picker (F48), which is a cookie and so
reaches nothing but their browser; `pick_theme` is where the two meet, and
every request resolves through it.
"""

import json
import re
from pathlib import Path

THEMES_DIR = Path(__file__).resolve().parent / "static" / "themes"

#: What each scheme is called in the menu (F49). English source strings,
#: translated the way every other bit of chrome is — the scheme names
#: themselves are internal and never shown.
SCHEME_LABELS = {
    "dark": "Dark",
    "light": "Light",
    "manuscript": "Manuscript",
}

#: The colour schemes main.css itself declares. A pack that says nothing
#: offers all three; a pack whose world has no aged paper in it says so in
#: its `theme.json` and the nav toggle stops offering one.
DEFAULT_COLOR_SCHEMES = ("dark", "light", "manuscript")

#: The pack every other pack falls back to, and the one a book gets when
#: `STORYBOOK_THEME` is unset. It is the only pack guaranteed to be
#: complete.
DEFAULT_THEME = "ranch"

#: A reader's own choice of pack (F48), remembered in a cookie rather than
#: the session because it has to survive logging out — and because it is a
#: preference, not a permission. A year, like the language cookie.
COOKIE_NAME = "storybook-theme-pack"
COOKIE_MAX_AGE = 365 * 24 * 60 * 60

_THEME_NAME_RE = re.compile(r"^[a-z0-9-]{1,32}$")
_ASSET_NAME_RE = re.compile(r"^[a-z0-9._-]+$")
#: Swatch colours are pasted into a style attribute, so nothing but a plain
#: hex colour is ever let through.
_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


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


def _manifest(theme: str) -> dict:
    """A pack's optional `theme.json`, or an empty dict — a pack is allowed
    to have none, and a broken one must not take the book down with it."""
    if not is_valid_theme(theme):
        return {}
    try:
        data = json.loads((THEMES_DIR / theme / "theme.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def pick_theme(chosen: str | None, configured: str | None = None) -> str:
    """Which pack a request renders in: the reader's own choice if they
    have made one and it still exists, otherwise the book's.

    Every way a name can be wrong ends in the same place — a cookie from
    an older install naming a pack since deleted, a hand-edited one, a
    `STORYBOOK_THEME` that somehow got through — because a book that
    renders is worth more than a book that argues. (Startup does argue:
    `_parse_theme` refuses an unknown `STORYBOOK_THEME` outright, where
    there is someone to read the error.)
    """
    if chosen and is_valid_theme(chosen):
        return chosen
    if configured and is_valid_theme(configured):
        return configured
    return DEFAULT_THEME


def label(theme: str) -> str:
    """The pack's name for a human: its `theme.json` label, or the folder
    name tidied up. Not translated — a pack's name is a proper noun, the
    way "Storybook" is when a family has set STORYBOOK_TITLE."""
    declared = _manifest(theme).get("label")
    if isinstance(declared, str) and declared.strip():
        return declared.strip()[:32]
    return (theme or DEFAULT_THEME).replace("-", " ").title()


def swatch(theme: str) -> list[str]:
    """Up to three hex colours a picker can show as dots, so a pack is
    recognisable before it is applied. Empty when the pack declares none,
    which the picker renders as a name on its own rather than inventing
    colours it would have to guess."""
    declared = _manifest(theme).get("swatch")
    if not isinstance(declared, list):
        return []
    return [c for c in declared if isinstance(c, str) and _COLOR_RE.match(c)][:3]


def color_schemes(theme: str) -> list[str]:
    """The colour schemes this pack offers, in the order the nav toggle
    cycles them. From the pack's optional `theme.json`; the full built-in
    set when it has none, an unreadable one, or one that names no scheme
    main.css actually declares.

    A pack narrowing this is not cosmetic. The ranch's third scheme is aged
    paper, which in a book set in orbit is simply the wrong world — and a
    toggle that cycles to a scheme the pack never designed is worse than a
    toggle with one fewer stop.
    """
    if not is_valid_theme(theme):
        return list(DEFAULT_COLOR_SCHEMES)
    declared = _manifest(theme).get("schemes")
    if not isinstance(declared, list):
        return list(DEFAULT_COLOR_SCHEMES)
    # Only names main.css knows: an unknown one would be a toggle stop that
    # changes nothing, which reads as a broken button.
    schemes = [s for s in declared if s in DEFAULT_COLOR_SCHEMES]
    return schemes or list(DEFAULT_COLOR_SCHEMES)


def stylesheet_url_path(theme: str) -> str | None:
    """The pack's own stylesheet, or None when it doesn't have one (the
    default pack doesn't need one — its colours are main.css's own)."""
    if not is_valid_theme(theme):
        return None
    if (THEMES_DIR / theme / "theme.css").is_file():
        return f"themes/{theme}/theme.css"
    return None
