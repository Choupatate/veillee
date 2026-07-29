"""Tests for FEATURES.md F44: the firelight wash and its off switch.

The animation is CSS and was watched in a browser; what is worth pinning
here is the contract the three pieces share — the markup in `base.html`,
the `data-firelight` attribute `theme-boot.js` writes before first paint,
and the `--firelight-strength` every theme has to declare.
"""

import re
from pathlib import Path

APP = Path(__file__).resolve().parent.parent / "app"
MAIN_CSS = (APP / "static" / "css" / "main.css").read_text()
THEME_BOOT = (APP / "static" / "js" / "theme-boot.js").read_text()
FIRELIGHT_JS = (APP / "static" / "js" / "firelight.js").read_text()


# --- the markup --------------------------------------------------------------


def test_the_wash_and_its_switch_are_on_every_page(auth_client):
    html = auth_client.get("/").data.decode()
    assert '<div class="firelight" aria-hidden="true">' in html
    assert 'class="firelight__glow"' in html
    assert 'class="firelight__flicker"' in html
    assert 'id="firelight-toggle"' in html
    assert "/static/js/firelight.js" in html


def test_it_reaches_the_login_page_too(client):
    """base.html renders for everyone, logged in or not — the fire is lit
    in the room before you sit down."""
    html = client.get("/login").data.decode()
    assert 'class="firelight"' in html
    assert 'id="firelight-toggle"' in html


def test_the_wash_is_hidden_from_assistive_tech():
    """Decoration with nothing to announce. The button carries the label."""
    base = (APP / "templates" / "base.html").read_text()
    div = re.search(r"<div class=\"firelight\"[^>]*>", base).group(0)
    assert 'aria-hidden="true"' in div


def test_the_switch_is_labelled_and_translated():
    from app.translations_fr import TRANSLATIONS_FR

    base = (APP / "templates" / "base.html").read_text()
    assert "aria-label=\"{{ _('Firelight') }}\"" in base
    assert TRANSLATIONS_FR["Firelight"] != "Firelight"


# --- the off switch ----------------------------------------------------------


def test_only_off_is_ever_stored_and_it_is_applied_before_paint():
    """Firelight is on by default, so an empty storage slot must mean on —
    which is why theme-boot only ever looks for the string "off". It runs
    in <head> so the wash is never painted and then yanked away."""
    assert 'getString("storybook-firelight") === "off"' in THEME_BOOT
    assert 'setAttribute("data-firelight", "off")' in THEME_BOOT


def test_the_css_honours_that_attribute():
    assert re.search(
        r':root\[data-firelight="off"\]\s*\.firelight\s*\{[^}]*display:\s*none', MAIN_CSS
    )


def test_the_button_reports_its_state():
    assert 'setAttribute("aria-pressed"' in FIRELIGHT_JS


def test_the_button_is_not_offered_without_js():
    """It can't do anything without JS, so it isn't shown — `theme-boot.js`
    adds the `js` class in <head>, which is what un-hides it."""
    assert re.search(r"\.firelight-toggle\s*\{[^}]*display:\s*none", MAIN_CSS)
    assert re.search(r"\.js \.firelight-toggle\s*\{[^}]*display:\s*inline-flex", MAIN_CSS)


# --- the effect itself -------------------------------------------------------


def test_every_theme_declares_its_own_strength():
    """`.firelight` sets `opacity: var(--firelight-strength)` with no
    fallback on purpose: a theme that forgets to declare it should fail
    here rather than quietly wash a bright page with full-strength amber.
    Every block that defines the palette has to define the strength too.
    (Print is excluded: it repaints the palette white and hides the wash.)"""
    screen = MAIN_CSS[:MAIN_CSS.index("@media print")]
    palettes = screen.count("--color-bg:")
    assert palettes >= 4, "the theme blocks moved — check this test"
    assert screen.count("--firelight-strength:") == palettes


def test_the_animation_is_off_for_reduced_motion():
    """Under `prefers-reduced-motion: reduce` the layers keep their warm
    tint but stop moving — the same bargain `.lasso-spinner` makes."""
    guarded = re.findall(
        r"@media \(prefers-reduced-motion: no-preference\) \{(.*?)\n\}", MAIN_CSS, re.S
    )
    assert any("firelight-breathe" in block for block in guarded)
    outside = MAIN_CSS
    for block in guarded:
        outside = outside.replace(block, "")
    assert "animation: firelight-breathe" not in outside


def test_the_two_layers_run_on_mismatched_cycles():
    """Equal durations would beat in step and read as a pulse; the whole
    point is that a fire never repeats on time."""
    durations = re.findall(r"animation: firelight-breathe ([\d.]+)s", MAIN_CSS)
    assert len(durations) == 2
    assert durations[0] != durations[1]


def test_the_wash_cannot_swallow_a_click():
    assert re.search(r"\.firelight \{[^}]*pointer-events:\s*none", MAIN_CSS)


def test_it_stays_under_the_lightbox():
    """The wash sits over the page but must never cover the zoomed photo
    (z-index 200) or the skip link (100)."""
    z = re.search(r"\.firelight \{[^}]*z-index:\s*(\d+)", MAIN_CSS)
    assert z and int(z.group(1)) < 100


def test_it_does_not_print():
    printed = MAIN_CSS[MAIN_CSS.index("@media print"):]
    hidden = re.search(r"\.skip-link,\s*\.firelight,", printed)
    assert hidden
