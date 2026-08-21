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

Packs come from two places (F50). The ones that ship with the app live
under `app/static/themes/`; the ones a family makes live under
`<stories>/themes/`, in the data folder, because artwork someone drew for
their own book must survive an app update and travel in the backup zip
like everything else they made. Every lookup here checks the built-in
folder first, so a made pack can never shadow `ranch` and quietly break
the fallback everything else depends on.
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


#: Where a family's own packs live, relative to the stories directory.
USER_THEMES_DIRNAME = "themes"


def user_themes_dir(stories_dir) -> Path:
    """The data folder's pack directory. Not created here — a book with no
    made packs simply has no such folder."""
    return Path(stories_dir) / USER_THEMES_DIRNAME


def _named_safely(name: str) -> bool:
    """The name is pasted into URLs and filesystem paths, so the regex
    matters as much as any directory check that follows it."""
    return bool(name and ".." not in name and _THEME_NAME_RE.match(name))


def builtin_themes() -> list[str]:
    """Every pack shipped with the app, alphabetically."""
    if not THEMES_DIR.is_dir():
        return []
    return sorted(p.name for p in THEMES_DIR.iterdir() if p.is_dir())


def user_themes(user_dir=None) -> list[str]:
    """Every pack this book's family made, alphabetically. A folder whose
    name a shipped pack already uses is ignored rather than obeyed: the
    built-in one wins everywhere else, so honouring it here would only
    produce a pack that half-exists."""
    if user_dir is None:
        return []
    user_dir = Path(user_dir)
    if not user_dir.is_dir():
        return []
    shipped = set(builtin_themes())
    return sorted(
        p.name
        for p in user_dir.iterdir()
        if p.is_dir() and _named_safely(p.name) and p.name not in shipped
    )


def available_themes(user_dir=None) -> list[str]:
    """Every pack this book can render, shipped and made alike."""
    return sorted(set(builtin_themes()) | set(user_themes(user_dir)))


def is_builtin_theme(name: str) -> bool:
    return bool(_named_safely(name) and (THEMES_DIR / name).is_dir())


def pack_root(name: str, user_dir=None) -> Path | None:
    """The folder a pack's files are in, or None if there is no such pack.

    Built-in first, always. That order is what stops a made pack called
    `ranch` from shadowing the one every other pack falls back to.
    """
    if not _named_safely(name):
        return None
    if (THEMES_DIR / name).is_dir():
        return THEMES_DIR / name
    if user_dir is not None:
        made = Path(user_dir) / name
        if made.is_dir():
            return made
    return None


def is_valid_theme(name: str, user_dir=None) -> bool:
    """A real pack, named safely."""
    return pack_root(name, user_dir) is not None


def is_user_theme(name: str, user_dir=None) -> bool:
    """A pack that lives in the data folder rather than in the app. Only
    these can be edited or deleted from the interface (F50)."""
    root = pack_root(name, user_dir)
    return root is not None and not is_builtin_theme(name)


def image_ref(theme: str, filename: str, user_dir=None) -> tuple[str, str, str]:
    """Where a picture actually comes from, as `(kind, pack, filename)` —
    kind being "builtin" or "user". The fallback is already applied, so a
    caller only has to know how to turn each kind into a URL: shipped packs
    are static files, made ones are served by a route out of the data
    folder.

    Falls back to the default pack for a filename this pack doesn't draw,
    and for an unknown or unsafe filename too. A missing picture is a
    missing picture either way, and inventing a path inside an unvalidated
    name is how a traversal starts.
    """
    if _ASSET_NAME_RE.match(filename or "") and ".." not in filename:
        if theme != DEFAULT_THEME:
            root = pack_root(theme, user_dir)
            if root is not None and (root / "img" / filename).is_file():
                kind = "builtin" if is_builtin_theme(theme) else "user"
                return (kind, theme, filename)
    return ("builtin", DEFAULT_THEME, filename)


def image_url_path(theme: str, filename: str, user_dir=None) -> str | None:
    """The `static`-relative path of `filename` for `theme` — e.g.
    "themes/orbit/img/icon-save.png". None when the answer is a made pack's
    file, which `static` knows nothing about; those go through the media
    route instead."""
    kind, pack, name = image_ref(theme, filename, user_dir)
    if kind != "builtin":
        return None
    return f"themes/{pack}/img/{name}"


def _manifest(theme: str, user_dir=None) -> dict:
    """A pack's `theme.json`, or an empty dict — a shipped pack is allowed
    to have none, and a broken one must not take the book down with it."""
    root = pack_root(theme, user_dir)
    if root is None:
        return {}
    try:
        data = json.loads((root / "theme.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def pick_theme(chosen: str | None, configured: str | None = None, user_dir=None) -> str:
    """Which pack a request renders in: the reader's own choice if they
    have made one and it still exists, otherwise the book's.

    Every way a name can be wrong ends in the same place — a cookie from
    an older install naming a pack since deleted, a hand-edited one, a
    `STORYBOOK_THEME` that somehow got through — because a book that
    renders is worth more than a book that argues. (Startup does argue:
    `_parse_theme` refuses an unknown `STORYBOOK_THEME` outright, where
    there is someone to read the error.)
    """
    if chosen and is_valid_theme(chosen, user_dir):
        return chosen
    if configured and is_valid_theme(configured, user_dir):
        return configured
    return DEFAULT_THEME


def label(theme: str, user_dir=None) -> str:
    """The pack's name for a human: its `theme.json` label, or the folder
    name tidied up. Not translated — a pack's name is a proper noun, the
    way "Storybook" is when a family has set STORYBOOK_TITLE."""
    declared = _manifest(theme, user_dir).get("label")
    if isinstance(declared, str) and declared.strip():
        return declared.strip()[:32]
    return (theme or DEFAULT_THEME).replace("-", " ").title()


def swatch(theme: str, user_dir=None) -> list[str]:
    """Up to three hex colours a picker can show as dots, so a pack is
    recognisable before it is applied. Empty when the pack declares none,
    which the picker renders as a name on its own rather than inventing
    colours it would have to guess."""
    declared = _manifest(theme, user_dir).get("swatch")
    if not isinstance(declared, list):
        return []
    return [c for c in declared if isinstance(c, str) and _COLOR_RE.match(c)][:3]


def color_schemes(theme: str, user_dir=None) -> list[str]:
    """The colour schemes this pack offers, in the order the nav toggle
    cycles them. From the pack's optional `theme.json`; the full built-in
    set when it has none, an unreadable one, or one that names no scheme
    main.css actually declares.

    A pack narrowing this is not cosmetic. The ranch's third scheme is aged
    paper, which in a book set in orbit is simply the wrong world — and a
    toggle that cycles to a scheme the pack never designed is worse than a
    toggle with one fewer stop.
    """
    if not is_valid_theme(theme, user_dir):
        return list(DEFAULT_COLOR_SCHEMES)
    declared = _manifest(theme, user_dir).get("schemes")
    if not isinstance(declared, list):
        return list(DEFAULT_COLOR_SCHEMES)
    # Only names main.css knows: an unknown one would be a toggle stop that
    # changes nothing, which reads as a broken button.
    schemes = [s for s in declared if s in DEFAULT_COLOR_SCHEMES]
    return schemes or list(DEFAULT_COLOR_SCHEMES)


def stylesheet_url_path(theme: str, user_dir=None) -> str | None:
    """The pack's own stylesheet as a static file, or None — either because
    the pack has none (the default pack doesn't need one; its colours are
    main.css's own) or because it is a made pack, whose colours are data
    and are rendered by a route rather than shipped as a file."""
    if not is_builtin_theme(theme):
        return None
    if (THEMES_DIR / theme / "theme.css").is_file():
        return f"themes/{theme}/theme.css"
    return None
