"""The book's own settings, set from inside the book (FEATURES.md F51).

Everything used to come from `STORYBOOK_*` environment variables, which is
right for the half that describes the *machine* — the password, the session
key, where the stories live, whether there is a proxy in front. It was
wrong for the other half, which describes the *family*: what the book is
called, whose childhood it is, who writes in it. Those are decisions a
parent makes, and asking them to edit a dotfile and restart a container to
change the title of their own book is asking the wrong person.

So the six family-facing settings live here, in `settings.json` in the
stories folder — beside `groups.json`, inside the backup, plain text, and
readable long after this app is gone.

**The environment is the default; the app wins.** A `STORYBOOK_*` variable
is what a fresh install starts with, and anything set from inside the book
overrides it from the next request onward, with no restart. That order is
deliberate: the person clicking Save in the app is making the more recent
decision, and a setting that silently reverted to a variable they have
never seen would be indefensible.

Read once per request into `g` (see `create_app`), so a save takes effect
immediately and a page render never reads the file twice.
"""

import json
import os
import re
from datetime import date
from pathlib import Path

SETTINGS_FILENAME = "settings.json"

#: What the app may be told about itself, and the config key each one
#: overrides. Anything not in here stays an environment variable, on
#: purpose: those are properties of the server, not of the family.
KEYS = {
    "title": "TITLE",
    "birthdate": "BIRTHDATE",
    "child": "CHILD_SLUG",
    "authors": "AUTHORS",
    "language": "DEFAULT_LANGUAGE",
    "theme": "THEME",
}

MAX_TITLE = 60
MAX_AUTHORS = 8
_HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
_SLUG_RE = re.compile(r"^[a-z0-9-]{1,64}$")


class SettingsError(Exception):
    """Something the person filling in the form can fix."""


def settings_path(stories_dir) -> Path:
    return Path(stories_dir) / SETTINGS_FILENAME


def read(stories_dir) -> dict:
    """What has been set from inside the book, or an empty dict.

    Never raises. A settings file that has been hand-edited into nonsense
    costs the settings, not the book — every reader would otherwise meet an
    error page because someone mistyped a date.
    """
    try:
        data = json.loads(settings_path(stories_dir).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def is_configured(stories_dir) -> bool:
    """Whether this book has been set up.

    The settings file's *existence* is the flag, not its contents: someone
    who deliberately left every field blank has still decided, and must not
    be asked again.

    **A book with stories in it counts as set up**, settings file or not.
    That is the upgrade case, and getting it wrong would be the worst kind
    of bug this feature could have: a family who has been writing for a
    year installs a new version and is met by a setup wizard for a book
    that plainly already exists. Their settings came from environment
    variables and still work; there is nothing to ask them.

    **A book is more than its stories.** A family can spend an evening
    adding the cast, making a theme and setting up who can read what
    before anybody writes the first entry — and that book is plainly not
    new. Counting only stories meant the wizard could still be reached on
    it, and one submit with the fields cleared took away its title, its
    narrators, its birth date and its language. The content survived; the
    book's identity did not.

    Made themes and audience groups are counted for that reason: neither
    exists unless somebody deliberately made it.

    People are still *not* counted, and that exclusion is the reason this
    is not simply "is the folder empty" — in accounts mode the first
    account creates a Person before a single story is written, so people
    would make every genuinely new book look like an old one. The wizard's
    own refusal to clear a value it was not given (see
    `routes_settings._form_values`) is what covers a book that has only a
    cast, and what covers the case nothing here can detect: a stories
    volume that failed to mount looks exactly like a new book, and always
    will.
    """
    if settings_path(stories_dir).is_file():
        return True
    return has_stories(stories_dir) or has_made_content(stories_dir)


def has_made_content(stories_dir) -> bool:
    """Whether somebody has made a theme or an audience group here.

    Read off the filesystem rather than through `themes` and `groups`, to
    keep this module's habit of importing nothing from the rest of the app
    — it is the thing every request reads, and it stays a leaf.
    """
    stories_dir = Path(stories_dir)
    themes_root = stories_dir / "themes"
    if themes_root.is_dir() and any(e.is_dir() for e in themes_root.iterdir()):
        return True
    try:
        data = json.loads((stories_dir / "groups.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return bool(isinstance(data, list) and data)


def has_stories(stories_dir) -> bool:
    """Whether anything has been written here yet. Cheap on purpose: this
    runs on the way to the timeline, so it stops at the first story it
    finds rather than listing them all."""
    stories_dir = Path(stories_dir)
    if not stories_dir.is_dir():
        return False
    for entry in stories_dir.iterdir():
        if not entry.is_dir() or entry.name in ("people", "themes"):
            continue
        if (entry / "index.md").is_file():
            return True
    return False


# --- validation --------------------------------------------------------------


def clean_title(value) -> str:
    return (value or "").strip()[:MAX_TITLE]


def clean_birthdate(value):
    """An ISO date, or None for "don't show ages at all"."""
    value = (value or "").strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise SettingsError(
            "The birth date needs to look like 2023-06-18 (year-month-day)."
        )


def clean_child(value) -> str:
    value = (value or "").strip()
    if value and not _SLUG_RE.match(value):
        raise SettingsError("That doesn't look like a person's address.")
    return value


def clean_language(value, supported) -> str:
    value = (value or "").strip()
    if value and value not in supported:
        raise SettingsError("The app doesn't have that language.")
    return value


def clean_authors(value) -> list:
    """The narrators, as typed: one `Name #rrggbb` per line.

    Lenient about the separator — a colon, a comma or spaces all work,
    because this is a text box and people type what looks reasonable — and
    strict about the colour, which ends up in a style attribute.
    """
    if isinstance(value, list):
        lines = [
            f"{entry.get('name', '')} {entry.get('color', '')}"
            for entry in value
            if isinstance(entry, dict)
        ]
    else:
        lines = (value or "").splitlines()

    authors = []
    seen = set()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = re.match(r"^(.*?)[\s:,]+(#[0-9a-fA-F]{6})$", line)
        if not match:
            raise SettingsError(
                f"“{line}” should be a name and a colour, like: Papa #d9a441"
            )
        name = match.group(1).strip()
        if not name:
            raise SettingsError(f"“{line}” is missing a name.")
        if name.casefold() in seen:
            raise SettingsError(f"“{name}” is in the list twice.")
        seen.add(name.casefold())
        authors.append({"name": name, "color": match.group(2).lower()})
        if len(authors) > MAX_AUTHORS:
            raise SettingsError(f"That's more than {MAX_AUTHORS} narrators.")
    return authors


def authors_text(authors) -> str:
    """The list back as the text someone typed, for the form."""
    return "\n".join(
        f"{a.get('name', '')} {a.get('color', '')}"
        for a in (authors or [])
        if isinstance(a, dict)
    )


# --- reading and writing -----------------------------------------------------


def _stored_authors(value, fallback):
    """A narrator list read back off disk, or the environment's if it is
    not one.

    `read()` promises that a settings file someone edited by hand costs
    them the settings and not the book, and the birthdate branch below
    keeps that promise by catching a bad date. This is the same promise
    for the same reason: `_authors_and_colors` indexes every entry as
    `a["name"]`, so `{"authors": ["Papa", "Maman"]}` — which is exactly
    what a person would write by hand — turned every page of the book
    into a 500.

    Entries are filtered rather than the whole list rejected: one bad line
    should not cost the other three narrators their colours.
    """
    if not isinstance(value, list):
        return fallback
    clean = []
    for entry in value:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        color = entry.get("color")
        if (isinstance(name, str) and name.strip()
                and isinstance(color, str) and _HEX_RE.match(color.strip())):
            clean.append({"name": name.strip(), "color": color.strip().lower()})
    return clean


def effective(config, stories_dir) -> dict:
    """The settings this request should use: the environment's values, with
    anything set inside the book laid over the top.

    A key that is present but empty means "no value" — someone clearing the
    title in the form wants the app's own name back, not the environment's
    leftover. A key that is absent falls through to the environment, which
    is what makes an install that has never opened the page behave exactly
    as it always did.
    """
    stored = read(stories_dir)
    out = {}
    for key, config_key in KEYS.items():
        if key not in stored:
            out[config_key] = config.get(config_key)
            continue
        value = stored[key]
        if key == "birthdate":
            try:
                out[config_key] = date.fromisoformat(value) if value else None
            except (TypeError, ValueError):
                out[config_key] = config.get(config_key)
        elif key == "authors":
            out[config_key] = _stored_authors(value, config.get(config_key))
        else:
            out[config_key] = value or None
    return out


def book(key):
    """One effective setting for the current request.

    Everything that used to read `current_app.config["AUTHORS"]` reads this
    instead, so a value set in the app is picked up on the next request
    rather than the next restart. Falls back to the raw config outside a
    request (and before `before_request` has run), where the environment is
    all there is.
    """
    from flask import current_app, g

    values = getattr(g, "book", None)
    if values is None:
        return current_app.config.get(key)
    return values.get(key, current_app.config.get(key))


def save(stories_dir, values) -> None:
    """Write the settings, atomically — a save that dies halfway leaves the
    previous ones intact rather than a file the book can't be read from."""
    stories_dir = Path(stories_dir)
    stories_dir.mkdir(parents=True, exist_ok=True)
    existing = read(stories_dir)
    existing.update(values)
    target = settings_path(stories_dir)
    tmp = stories_dir / (SETTINGS_FILENAME + ".tmp")
    tmp.write_text(json.dumps(existing, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, target)
