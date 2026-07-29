"""Tests for FEATURES.md F44: the writing surface wearing the app's colours.

The look itself is CSS and was checked in a browser. What is testable — and
what silently breaks a whole theme when someone gets it wrong — is the two
mechanical contracts `editor-theme.css` depends on: it must load *after* the
vendored Toast UI sheets, and every one of its selectors must out-specify
the vendored dark theme's two-class rules.
"""

import re
from datetime import date
from pathlib import Path

from app import storage

STATIC = Path(__file__).resolve().parent.parent / "app" / "static"
EDITOR_CSS = STATIC / "css" / "editor-theme.css"


def _rules(css):
    """Selector lists in the sheet, at-rule preludes dropped."""
    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [
        sel.strip() for sel in re.findall(r"([^{}]+)\{", stripped)
        if not sel.strip().startswith("@")
    ]


# --- load order --------------------------------------------------------------


def _stylesheets(html):
    return re.findall(r'<link rel="stylesheet" href="([^"]+)"', html)


def test_editor_theme_loads_after_the_vendored_sheets(auth_client):
    """Toast UI's own CSS is one class deep in most places, so this file
    wins those by coming last. Move the link up and the editor goes back to
    a white box on aged paper."""
    sheets = _stylesheets(auth_client.get("/new").data.decode())
    theme = sheets.index("/static/css/editor-theme.css")
    assert theme > sheets.index("/static/vendor/toastui/toastui-editor.min.css")
    assert theme > sheets.index("/static/vendor/toastui/theme/toastui-editor-dark.css")


def test_the_person_editor_is_dressed_the_same_way(auth_client):
    """One editor, one theme — `_editor_head.html` is shared, and this
    fails if someone forks it."""
    sheets = _stylesheets(auth_client.get("/new-person").data.decode())
    assert "/static/css/editor-theme.css" in sheets


def test_the_story_editor_of_an_existing_story_gets_it_too(auth_client, stories_dir):
    story_id = storage.create_story(stories_dir, "A day", date(2026, 1, 1), "body")
    sheets = _stylesheets(auth_client.get(f"/edit/{story_id}").data.decode())
    assert "/static/css/editor-theme.css" in sheets


def test_no_other_page_pays_for_it(auth_client):
    """It only re-styles a widget the timeline never mounts."""
    assert "/static/css/editor-theme.css" not in _stylesheets(
        auth_client.get("/").data.decode()
    )


# --- specificity -------------------------------------------------------------


def test_every_selector_is_prefixed_with_root():
    """The vendored dark theme selects with two classes
    (`.toastui-editor-dark .toastui-editor-defaultUI-toolbar`). A one-class
    rule here loses to it whatever the load order, so the whole file buys a
    class-worth of specificity with `:root`. Drop the prefix on one rule and
    that rule quietly stops applying — in dark theme only."""
    unprefixed = [
        part.strip()
        for rule in _rules(EDITOR_CSS.read_text())
        for part in rule.split(",")
        if not part.strip().startswith(":root")
    ]
    assert not unprefixed, "selectors that will lose to the dark theme:\n" + "\n".join(
        f"  {s}" for s in unprefixed
    )


def test_colours_come_from_theme_variables_only():
    """A hex here would be right in one theme and wrong in the other three,
    which is the exact bug this file exists to fix."""
    css = re.sub(r"/\*.*?\*/", "", EDITOR_CSS.read_text(), flags=re.S)
    assert not re.findall(r"#[0-9a-fA-F]{3,8}\b", css)


def test_the_icon_sprite_is_never_touched_with_the_background_shorthand():
    """Toast UI's toolbar icons are one image positioned by
    `background-position-y`; `background: transparent` would erase it and
    every glyph with it. Only the longhand may be used."""
    css = re.sub(r"/\*.*?\*/", "", EDITOR_CSS.read_text(), flags=re.S)
    for block in re.findall(r"([^{}]*)\{([^{}]*)\}", css):
        if "toolbar-icons" in block[0]:
            assert not re.search(r"(^|[;\s])background\s*:", block[1]), block
