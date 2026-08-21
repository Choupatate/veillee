"""Tests for FEATURES.md F49: one control in the nav for how the book looks.

The colour cycler and the pack picker were two neighbours doing related
things; this folds the second into a menu behind a press-and-hold on the
first. The hold itself can only be judged in a browser — what is testable
here is the contract underneath it: the menu is a real <details>, so it
still opens and still switches packs with JavaScript off, and the scheme
chips (which need localStorage to mean anything) are the only part that
depends on JavaScript being there.
"""

from pathlib import Path

from app import themes

REPO_ROOT = Path(__file__).resolve().parent.parent
MAIN_CSS = (REPO_ROOT / "app" / "static" / "css" / "main.css").read_text()


def _menu(html):
    return html.split('id="theme-menu"')[1].split("</details>")[0]


# --- the shape of it ----------------------------------------------------------


def test_the_toggle_is_a_disclosure_so_it_works_without_javascript(auth_client):
    html = auth_client.get("/").data.decode()
    assert '<details class="theme-menu"' in html
    menu = _menu(html)
    assert "<summary" in menu
    assert 'id="theme-toggle"' in menu


def test_the_button_says_that_holding_it_does_something_else(auth_client):
    """A disclosure whose activation doesn't disclose has to explain
    itself, or the only way to find the menu is by accident."""
    summary = _menu(auth_client.get("/").data.decode()).split("</summary>")[0]
    assert "aria-label=" in summary
    assert "Hold" in summary


def test_the_pack_picker_moved_inside_the_menu(auth_client):
    """The whole point: the nav carries one control, not one plus a row of
    swatches."""
    html = auth_client.get("/").data.decode()
    assert 'class="pack-picker"' in _menu(html)
    before_menu = html.split('id="theme-menu"')[0]
    assert "pack-picker" not in before_menu


def test_the_menu_offers_the_packs_schemes_and_a_way_back_to_the_system(auth_client):
    menu = _menu(auth_client.get("/").data.decode())
    for scheme in themes.color_schemes(themes.DEFAULT_THEME):
        assert f'data-scheme="{scheme}"' in menu
    # An explicit "no choice stored" chip, which is the only way to undo a
    # choice once one has been made.
    assert 'data-scheme=""' in menu


def test_a_pack_is_never_offered_a_scheme_it_did_not_design(auth_client):
    auth_client.post("/theme/orbit", data={"next": "/"})
    menu = _menu(auth_client.get("/").data.decode())
    assert 'data-scheme="dark"' in menu
    assert 'data-scheme="manuscript"' not in menu


def test_the_scheme_names_are_translated(auth_client_factory):
    from app.translations_fr import TRANSLATIONS_FR

    menu = _menu(auth_client_factory(DEFAULT_LANGUAGE="fr").get("/").data.decode())
    for label in themes.SCHEME_LABELS.values():
        assert TRANSLATIONS_FR[label] in menu
    assert TRANSLATIONS_FR["System"] in menu


def test_every_scheme_a_pack_can_offer_has_a_name(auth_client):
    """A scheme with no entry in SCHEME_LABELS would render an empty chip."""
    for scheme in themes.DEFAULT_COLOR_SCHEMES:
        assert themes.SCHEME_LABELS.get(scheme)


# --- what depends on JavaScript, and what doesn't -----------------------------


def test_the_scheme_chips_are_hidden_without_javascript():
    """They are remembered in localStorage, so with no JavaScript they
    could only lie about what is selected. The packs are a cookie and stay
    — which is what keeps the menu worth opening at all."""
    hidden = MAIN_CSS.split(".theme-menu__schemes {")[1].split("}")[0]
    assert "display: none" in hidden
    assert ".js .theme-menu__schemes {" in MAIN_CSS


def test_the_pack_forms_do_not_depend_on_javascript(auth_client):
    menu = _menu(auth_client.get("/").data.decode())
    assert 'method="post"' in menu
    assert 'action="/theme/orbit"' in menu
    assert "csrf_token" in menu


def test_the_press_logic_loads_before_the_script_that_uses_it(auth_client):
    html = auth_client.get("/").data.decode()
    assert html.index("js/theme-logic.js") < html.index("js/theme.js")


# --- details that would break the button quietly ------------------------------


def test_the_summary_marker_is_removed_in_every_engine():
    """A <summary> is a list item by default, and each engine draws its own
    marker — all of them have to go or the round button grows a triangle."""
    for selector in ("::-webkit-details-marker", "::marker"):
        assert f".theme-menu__summary{selector}" in MAIN_CSS
    assert "list-style: none" in MAIN_CSS.split(".theme-menu__summary {")[1].split("}")[0]


def test_holding_the_button_cannot_raise_the_phones_own_menu():
    """Without this, a long press on iOS selects the glyph or opens the
    callout on top of the menu it was meant to open."""
    summary = MAIN_CSS.split(".theme-menu__summary {")[1].split("}")[0]
    assert "-webkit-touch-callout: none" in summary
    assert "user-select: none" in summary


def test_the_chosen_chip_is_not_told_apart_by_colour_alone():
    """F45's rule: hover must never be able to imitate the pressed state."""
    pressed = MAIN_CSS.split('.theme-menu__chip[aria-pressed="true"] {')[1].split("}")[0]
    assert "font-weight" in pressed
    assert "background" in pressed
