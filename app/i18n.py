"""Interface translation (FEATURES.md F38).

Deliberately tiny and dependency-free: a dict lookup, a plural rule, and a
date formatter. Flask-Babel was the obvious alternative and was rejected —
it needs `.po`/`.mo` files compiled by `pybabel`, i.e. a build step, which
this project doesn't have and doesn't want (CLAUDE.md).

Only the *interface* is translated. Story text, titles, people's names —
everything a family actually writes — is stored and shown exactly as
typed. A French speaker and an English speaker looking at the same book
see the same memories, with different furniture around them.

Keys are the English source strings, so templates stay readable
(`{{ _("Back to the timeline") }}`) and a missing translation degrades to
English rather than to a raw key. `tests/test_i18n.py` fails if any string
used in a template is missing from the French dict, so "degrades to
English" never quietly becomes the normal case.
"""

from datetime import date, datetime

from .translations_fr import TRANSLATIONS_FR

DEFAULT_LANGUAGE = "en"
COOKIE_NAME = "storybook-lang"
COOKIE_MAX_AGE = 365 * 24 * 60 * 60

# Order here is the order the picker renders in.
LANGUAGES = {
    "en": {"label": "English", "short": "EN"},
    "fr": {"label": "Français", "short": "FR"},
}

TRANSLATIONS = {"fr": TRANSLATIONS_FR}

_MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
           "août", "septembre", "octobre", "novembre", "décembre"],
}

_MONTHS_SHORT = {
    "en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
    "fr": ["janv.", "févr.", "mars", "avr.", "mai", "juin",
           "juil.", "août", "sept.", "oct.", "nov.", "déc."],
}


def is_supported(lang) -> bool:
    return lang in LANGUAGES


def parse_accept_language(header: str):
    """First supported language from an Accept-Language header, or None.

    Quality values are honoured, and a regional tag matches its base
    language ("fr-CA" -> "fr") so a Quebecois phone isn't handed English.
    """
    if not header:
        return None
    entries = []
    for i, part in enumerate(header.split(",")):
        part = part.strip()
        if not part:
            continue
        tag, _, params = part.partition(";")
        tag = tag.strip().lower()
        quality = 1.0
        for param in params.split(";"):
            key, _, value = param.partition("=")
            if key.strip() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0.0
        # `i` keeps the header's own order as the tie-break, since equal-q
        # tags are ranked by appearance.
        entries.append((-quality, i, tag))
    for _, _, tag in sorted(entries):
        base = tag.split("-")[0]
        if is_supported(tag):
            return tag
        if is_supported(base):
            return base
    return None


def pick_language(cookie_value=None, accept_language=None, book_default=None) -> str:
    """Resolution order: the reader's own explicit choice, then the
    browser's preference, then the book's own default, then English.

    `book_default` (STORYBOOK_LANGUAGE) matters because this app is one
    family's book, not a public site: if the book is French, a visitor
    arriving with no stored choice should get French, not English."""
    if is_supported(cookie_value):
        return cookie_value
    from_header = parse_accept_language(accept_language)
    if from_header:
        return from_header
    if is_supported(book_default):
        return book_default
    return DEFAULT_LANGUAGE


def _plural_index(n: int, lang: str) -> int:
    """0 = singular form, 1 = plural form. French keeps the singular for
    zero ("0 jour"), English doesn't ("0 days")."""
    if lang == "fr":
        return 0 if abs(n) < 2 else 1
    return 0 if n == 1 else 1


def translate(text: str, lang: str) -> str:
    if lang == DEFAULT_LANGUAGE:
        return text
    return TRANSLATIONS.get(lang, {}).get(text, text)


def gettext(text: str, lang: str, **kwargs) -> str:
    """Translate, then interpolate. Interpolation happens after lookup so a
    translated string can reorder its placeholders."""
    result = translate(text, lang)
    if kwargs:
        try:
            return result.format(**kwargs)
        except (KeyError, IndexError):
            # A malformed translation must never 500 a page; fall back to
            # the English source, which is known to match the placeholders.
            return text.format(**kwargs)
    return result


def ngettext(singular: str, plural: str, n: int, lang: str, **kwargs) -> str:
    """Pick the singular or plural source string, then translate it. The
    French dict stores both forms under their own English keys."""
    source = singular if _plural_index(n, lang) == 0 else plural
    return gettext(source, lang, n=n, **kwargs)


# --- dates ------------------------------------------------------------------
#
# strftime("%B") is locale-dependent and needs the right locale generated on
# the host, which a Docker image typically doesn't have; strftime("%-d") is
# glibc-only besides. A lookup table is smaller, deterministic, and works
# identically everywhere.


def format_date(value, lang: str, style: str = "long") -> str:
    """`style`: "long" (June 18, 2026 / 18 juin 2026), "short" (Jun 18 /
    18 juin), "short_year" (Jun 18, 2026 / 18 juin 2026), "month_year"
    (June 2026 / juin 2026), or "month" (June / juin)."""
    if value is None:
        return ""
    if isinstance(value, datetime):
        value = value.date()
    lang = lang if lang in _MONTHS else DEFAULT_LANGUAGE
    month_long = _MONTHS[lang][value.month - 1]
    month_short = _MONTHS_SHORT[lang][value.month - 1]

    if lang == "fr":
        # French writes the day first and never puts a comma before the
        # year; "1" takes the ordinal "1er".
        day = "1er" if value.day == 1 else str(value.day)
        return {
            "long": f"{day} {month_long} {value.year}",
            "short": f"{day} {month_short}",
            "short_year": f"{day} {month_short} {value.year}",
            "month_year": f"{month_long} {value.year}",
            "month": month_long,
        }[style]

    return {
        "long": f"{month_long} {value.day}, {value.year}",
        "short": f"{month_short} {value.day}",
        "short_year": f"{month_short} {value.day}, {value.year}",
        "month_year": f"{month_long} {value.year}",
        "month": month_long,
    }[style]


def format_datetime(value, lang: str) -> str:
    """A saved-version timestamp: "Jun 18, 2026 14:05" / "18 juin 2026 à 14:05"."""
    if value is None:
        return ""
    stamp = value.strftime("%H:%M")
    day = format_date(value, lang, "short_year")
    return f"{day} à {stamp}" if lang == "fr" else f"{day} {stamp}"


# --- request-scoped shorthands ----------------------------------------------
#
# Everything above is pure and takes `lang` explicitly, so it can be tested
# without a request. These wrappers read the language the before_request
# hook resolved, and are what templates and route code actually call.


def current_language() -> str:
    from flask import g

    return getattr(g, "lang", DEFAULT_LANGUAGE)


def _(text: str, **kwargs) -> str:
    return gettext(text, current_language(), **kwargs)


def _n(singular: str, plural: str, n: int, **kwargs) -> str:
    return ngettext(singular, plural, n, current_language(), **kwargs)


def age_label(birthdate: date, on_date: date, lang: str = DEFAULT_LANGUAGE) -> str:
    """Localized version of the F3 age phrase. The month/day/year arithmetic
    lives in dates.py; this only chooses the words."""
    from . import dates

    parts = dates.age_parts(birthdate, on_date)
    if parts is None:
        return gettext("before you were born", lang)
    unit, amount = parts
    if unit == "day":
        return ngettext("{n} day old", "{n} days old", amount, lang)
    if unit == "month":
        return ngettext("{n} month old", "{n} months old", amount, lang)
    return ngettext("{n} year old", "{n} years old", amount, lang)


# --- strings a handful of JS files need at runtime --------------------------
#
# The static text templates render is translated at request time (this
# file); the few files below render text *after* the page loads (a save
# button's state, an in-browser camera's controls, the tree's view
# buttons) and can't go through Jinja. Rather than a second, JS-side
# translation table, they read the exact same English-source-keyed
# strings from here via a small JSON blob base.html embeds (see
# static/js/i18n.js) — one dictionary, one place a translator edits.
JS_STRINGS = (
    "Close", "Cancel", "Flip", "Switch camera", "Take photo", "Take a photo",
    "Retake", "Use photo", "Camera access was denied. You can still add a "
    "photo from your files.", "No camera found on this device.",
    "The camera is busy in another app. Close it and try again.",
    "Could not start the camera.",
    "The camera isn't ready yet — try again in a moment.",
    "Could not take that photo. Try again.",
    "Microphone access was denied.", "Could not save the recording.",
    "Could not delete the recording.", "Adding the photo…",
    "Could not add that photo.", "Delete", "Pause", "Resume", "Saving…",
    "Change photo", "Note (optional)", "https://...", "Since",
    "Until (optional)", "Remove source", "Remove union", "Wedding", "PACS",
    "Union", "Recenter", "Recenter the family tree",
    "Could not load the family tree.", "Everyone", "Import failed.",
    "Could not import. Please check your connection and try again.",
    "Imported {n} story. Reloading…", "Imported {n} stories. Reloading…",
    "Add a partner above first.", "Only {names}",
)


def js_strings(lang: str) -> dict:
    return {text: gettext(text, lang) for text in JS_STRINGS}
