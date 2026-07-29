"""Tests for FEATURES.md F46: theme packs.

A pack is a folder — a `theme.css` of colour variables and an `img/` folder
— and the whole design rests on one behaviour: **a pack only has to draw
what it wants to change.** Everything it hasn't drawn falls back to the
default pack's copy, which is what makes a new art direction shippable on
day one and finishable over months.

These tests pin that fallback, the validation around a name that reaches
both URLs and the filesystem, and the two conventions that keep packs
interchangeable (same filenames, complete default).
"""

import re
from pathlib import Path

import pytest

from app import themes

TEMPLATES = Path(__file__).resolve().parent.parent / "app" / "templates"
STATIC = Path(__file__).resolve().parent.parent / "app" / "static"
MAIN_CSS = (STATIC / "css" / "main.css").read_text()
THEME_BOOT = (STATIC / "js" / "theme-boot.js").read_text()
THEME_JS = (STATIC / "js" / "theme.js").read_text()


# --- resolution and fallback -------------------------------------------------


def test_the_default_pack_answers_for_itself():
    assert themes.image_url_path("ranch", "icon-save.png") == "themes/ranch/img/icon-save.png"


def test_a_pack_serves_the_pictures_it_has(tmp_path, monkeypatch):
    monkeypatch.setattr(themes, "THEMES_DIR", tmp_path)
    (tmp_path / "ranch" / "img").mkdir(parents=True)
    (tmp_path / "moon" / "img").mkdir(parents=True)
    (tmp_path / "ranch" / "img" / "icon-save.png").write_bytes(b"x")
    (tmp_path / "moon" / "img" / "icon-save.png").write_bytes(b"y")

    assert themes.image_url_path("moon", "icon-save.png") == "themes/moon/img/icon-save.png"


def test_a_pack_inherits_every_picture_it_has_not_drawn(tmp_path, monkeypatch):
    """The point of the whole design: a pack with an empty `img/` is still a
    working theme. Break this and a new pack has to ship 37 pictures before
    it can ship at all."""
    monkeypatch.setattr(themes, "THEMES_DIR", tmp_path)
    (tmp_path / "ranch" / "img").mkdir(parents=True)
    (tmp_path / "moon" / "img").mkdir(parents=True)
    (tmp_path / "ranch" / "img" / "icon-save.png").write_bytes(b"x")

    assert themes.image_url_path("moon", "icon-save.png") == "themes/ranch/img/icon-save.png"


def test_an_unknown_pack_falls_back_rather_than_inventing_a_path(tmp_path, monkeypatch):
    monkeypatch.setattr(themes, "THEMES_DIR", tmp_path)
    (tmp_path / "ranch" / "img").mkdir(parents=True)
    assert themes.image_url_path("nope", "icon-save.png") == "themes/ranch/img/icon-save.png"


@pytest.mark.parametrize("filename", [
    "../../../etc/passwd", "../secret.png", "a/b.png", "", "Icon.PNG", "x;y.png",
])
def test_a_filename_that_is_not_a_plain_asset_name_never_reaches_a_pack(filename):
    """This value comes from a template today, but it builds both a URL and
    a filesystem path — it is validated like one either way."""
    assert themes.image_url_path("orbit", filename).startswith("themes/ranch/img/")


@pytest.mark.parametrize("name", ["../ranch", "ran ch", "RANCH", "", "x" * 33, "no-such-pack"])
def test_a_pack_name_that_is_not_a_pack_is_rejected(name):
    assert not themes.is_valid_theme(name)


def test_the_shipped_packs_are_all_valid_names():
    packs = themes.available_themes()
    assert themes.DEFAULT_THEME in packs
    for name in packs:
        assert themes.is_valid_theme(name)


# --- the two conventions -----------------------------------------------------


def test_the_default_pack_is_the_complete_one():
    """Every other pack falls back to this one, so it is the only pack that
    is not allowed a hole. Every picture any template asks for has to exist
    here."""
    asked = set()
    for path in TEMPLATES.glob("*.html"):
        asked.update(re.findall(r"theme_img\('([^']+)'\)", path.read_text()))
    assert len(asked) > 20, "the scanner stopped finding calls — check the regex"

    default_img = themes.THEMES_DIR / themes.DEFAULT_THEME / "img"
    missing = sorted(name for name in asked if not (default_img / name).is_file())
    assert not missing, f"the default pack is missing: {missing}"


def test_a_pack_is_a_skin_and_not_a_rename():
    """Same filename, same picture, in every pack. A pack that renames a
    file doesn't override it — it silently inherits the default's forever,
    and ships a file nothing ever loads."""
    default_img = themes.THEMES_DIR / themes.DEFAULT_THEME / "img"
    known = {p.name for p in default_img.iterdir() if p.is_file()}
    for name in themes.available_themes():
        if name == themes.DEFAULT_THEME:
            continue
        pack_img = themes.THEMES_DIR / name / "img"
        if not pack_img.is_dir():
            continue
        stray = sorted({p.name for p in pack_img.iterdir() if p.is_file()} - known)
        assert not stray, f"{name} ships files the default pack has no name for: {stray}"


def test_no_template_names_an_image_folder_directly():
    """Every picture goes through the resolver. A stray
    `url_for('static', filename='img/...')` would pin one pack's art into a
    page and quietly ignore every other pack."""
    offenders = [
        path.name for path in TEMPLATES.glob("*.html")
        if "filename='img/" in path.read_text() or "filename='themes/" in path.read_text()
    ]
    assert not offenders


def test_main_css_hardcodes_no_pack_art():
    """The two pictures CSS draws are variables, so a pack can replace them
    (or, like orbit, draw them with gradients and ship no file at all)."""
    assert "--flourish-image:" in MAIN_CSS
    assert "--brand-mark:" in MAIN_CSS
    for match in re.findall(r'url\("\.\./themes/([a-z0-9-]+)/', MAIN_CSS):
        assert match == themes.DEFAULT_THEME


# --- configuration -----------------------------------------------------------


def test_an_unknown_theme_fails_at_startup(monkeypatch):
    """Silently serving the default pack would be a puzzle to debug, and
    the fix is one word — so this fails loudly, like STORYBOOK_AUTHORS."""
    from app import create_app

    monkeypatch.setenv("STORYBOOK_THEME", "definitely-not-a-pack")
    with pytest.raises(RuntimeError, match="Unknown STORYBOOK_THEME"):
        create_app()


def test_the_default_is_the_default_pack(app):
    assert app.config["THEME"] == themes.DEFAULT_THEME


def test_pages_serve_the_configured_pack(app_factory):
    """End to end: set the pack, and the pictures on a real page come from
    it — or from the default when it hasn't drawn them."""
    app = app_factory(THEME="orbit")
    client = app.test_client()
    html = client.get("/login").data.decode()
    assert "/static/themes/orbit/theme.css" in html
    # orbit ships no artwork yet, so every picture is inherited
    assert "/static/themes/ranch/img/" in html


def test_the_default_pack_needs_no_stylesheet(app):
    """Its colours are main.css's own — a second sheet would be a copy to
    keep in sync."""
    assert themes.stylesheet_url_path(themes.DEFAULT_THEME) is None
    html = app.test_client().get("/login").data.decode()
    assert "themes/ranch/theme.css" not in html


# --- which colour schemes a pack offers --------------------------------------


def test_a_pack_that_says_nothing_offers_every_scheme():
    assert themes.color_schemes(themes.DEFAULT_THEME) == list(themes.DEFAULT_COLOR_SCHEMES)


def test_a_pack_can_narrow_the_schemes_it_offers():
    """Orbit has no aged paper in it, so it doesn't own a "manuscript"
    scheme — and the nav toggle stops offering one. A toggle that cycles to
    a scheme the pack never designed is worse than one stop fewer."""
    assert themes.color_schemes("orbit") == ["dark", "light"]


@pytest.mark.parametrize("body", [
    '{"schemes": []}',
    '{"schemes": ["chartreuse"]}',
    '{"schemes": "dark"}',
    '{"nope": 1}',
    '[]',
    'not json at all',
])
def test_a_theme_json_that_declares_nothing_usable_falls_back(tmp_path, monkeypatch, body):
    """Half a pack is still a pack: anything unreadable here means "all of
    them", never "none of them", because none of them is a toggle that
    does nothing."""
    monkeypatch.setattr(themes, "THEMES_DIR", tmp_path)
    (tmp_path / "moon").mkdir(parents=True)
    (tmp_path / "moon" / "theme.json").write_text(body)
    assert themes.color_schemes("moon") == list(themes.DEFAULT_COLOR_SCHEMES)


def test_an_unknown_pack_offers_every_scheme():
    assert themes.color_schemes("nope") == list(themes.DEFAULT_COLOR_SCHEMES)


def test_the_page_tells_the_scripts_which_schemes_exist(app_factory):
    """`data-schemes` is on <html> so theme-boot.js can read it in <head>,
    before first paint."""
    ranch = app_factory().test_client().get("/login").data.decode()
    assert 'data-schemes="dark light manuscript"' in ranch

    orbit = app_factory(THEME="orbit").test_client().get("/login").data.decode()
    assert 'data-schemes="dark light"' in orbit


def test_the_scripts_read_the_list_rather_than_hardcoding_it():
    """Both halves have to follow the pack: the boot script decides whether
    a stored scheme may be applied, and the toggle decides what it cycles
    through."""
    assert 'getAttribute("data-schemes")' in THEME_BOOT
    assert "window.StorybookSchemes" in THEME_BOOT
    assert "window.StorybookSchemes" in THEME_JS


def test_a_scheme_the_pack_does_not_offer_is_not_applied():
    """A reader who chose manuscript in a ranch book and then opens an orbit
    one must not be handed a scheme that pack never designed — theme-boot
    checks membership before applying."""
    assert "allowed.indexOf(stored) !== -1" in THEME_BOOT


# --- the data URIs a pack embeds ---------------------------------------------


def test_no_pack_embeds_a_raw_hash_in_a_data_uri():
    """A raw `#` inside `url("data:image/svg+xml,…")` starts a fragment
    identifier: the browser truncates the SVG at the first fill colour and
    the image silently disappears. It has to be `%23`. This cost an hour
    once — the CSS parses, the property computes, and nothing is drawn."""
    for theme in themes.available_themes():
        css_path = themes.THEMES_DIR / theme / "theme.css"
        if not css_path.is_file():
            continue
        for uri in re.findall(r'url\("(data:image/svg\+xml,[^"]*)"\)', css_path.read_text()):
            assert "#" not in uri, f"{theme}: raw # in a data URI truncates it"


def test_a_pack_can_lay_a_texture_over_its_background():
    """The hook orbit's starfield hangs on. Defaulted to `none` in main.css
    so a pack that says nothing gets a plain background."""
    assert "--surface-texture: none;" in MAIN_CSS
    assert "background-image: var(--surface-texture, none);" in MAIN_CSS


def test_orbit_puts_stars_in_the_night_and_not_in_the_day():
    css = (themes.THEMES_DIR / "orbit" / "theme.css").read_text()
    assert css.count("--surface-texture:") >= 2
    # the light scheme turns it off — you can't see stars in daylight
    light = re.search(r':root\[data-theme="light"\] \{([^}]*)\}', css).group(1)
    assert "--surface-texture: none;" in light
