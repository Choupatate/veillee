"""Tests for FEATURES.md F50: making a theme pack from inside the book.

Three things carry the weight here and are tested hardest. A made pack
lives in the *data* folder, so it survives an app update and rides along in
the backup zip. Only an admin can touch one. And nothing a person types or
uploads is ever trusted: the filename allowlist is the catalogue itself,
every colour is a validated hex before it reaches a stylesheet, and every
picture is decoded and re-encoded rather than written through.
"""

import io
import json
import zipfile
from datetime import date

import pytest
from PIL import Image

from app import palette, storage, theme_catalog, theme_packs, themes

DARK = {"bg": "#101822", "text": "#e8e2d9", "accent": "#d9a441"}
LIGHT = {"bg": "#faf6ef", "text": "#2a2520", "accent": "#a9701c"}


@pytest.fixture
def user_dir(stories_dir):
    return themes.user_themes_dir(stories_dir)


@pytest.fixture
def made(user_dir):
    theme_packs.save_pack(
        user_dir, "woodblock", label="Woodblock", description="indigo and rust",
        scheme_colors={"dark": DARK, "light": LIGHT},
    )
    return "woodblock"


def _png(size=(400, 400), color=(200, 40, 40), background=(128, 128, 128)):
    im = Image.new("RGB", size, background)
    im.paste(Image.new("RGB", (size[0] // 2, size[1] // 2), color), (size[0] // 4, size[1] // 4))
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    return buf


# --- where a made pack lives --------------------------------------------------


def test_a_made_pack_lives_in_the_data_folder(stories_dir, made):
    """Not in the app: an update or a container rebuild would delete
    artwork someone drew, and the backup only covers the data folder."""
    assert (stories_dir / "themes" / "woodblock" / "theme.json").is_file()


def test_the_app_can_render_it_like_any_other_pack(user_dir, made):
    assert made in themes.available_themes(user_dir)
    assert themes.label(made, user_dir) == "Woodblock"
    assert themes.color_schemes(made, user_dir) == ["dark", "light"]
    assert len(themes.swatch(made, user_dir)) >= 2


def test_it_is_known_as_a_made_pack_and_the_shipped_ones_are_not(user_dir, made):
    assert themes.is_user_theme(made, user_dir)
    assert not themes.is_user_theme("ranch", user_dir)
    assert not themes.is_user_theme("orbit", user_dir)


def test_a_made_pack_can_never_shadow_a_shipped_one(user_dir):
    """The fallback everything else depends on runs through `ranch`; a
    folder of that name in the data directory must be ignored, not
    obeyed."""
    (user_dir / "ranch").mkdir(parents=True)
    (user_dir / "ranch" / "theme.json").write_text('{"label": "Not the ranch"}')
    assert themes.label("ranch", user_dir) == "Ranch"
    assert "ranch" not in themes.user_themes(user_dir)
    assert themes.pack_root("ranch", user_dir) == themes.THEMES_DIR / "ranch"


def test_a_shipped_name_is_refused_before_anything_is_written(user_dir):
    with pytest.raises(theme_packs.PackError):
        theme_packs.save_pack(user_dir, "orbit", label="Mine", description="",
                              scheme_colors={"dark": DARK})
    assert not (user_dir / "orbit").exists()


def test_a_name_the_editor_needs_for_itself_is_refused(user_dir):
    """`/themes/new` has to keep meaning the new-theme form."""
    with pytest.raises(theme_packs.PackError):
        theme_packs.save_pack(user_dir, "new", label="New", description="",
                              scheme_colors={"dark": DARK})


def test_a_name_that_could_leave_the_folder_is_refused(user_dir):
    for hostile in ("../evil", "..", "/etc", "Woodblock", ""):
        with pytest.raises(theme_packs.PackError):
            theme_packs.save_pack(user_dir, hostile, label="x", description="",
                                  scheme_colors={"dark": DARK})


def test_slugify_makes_a_safe_name_out_of_what_someone_typed():
    assert theme_packs.slugify("Estampe Japonaise") == "estampe-japonaise"
    assert theme_packs.slugify("Café  du  Marché!") == "cafe-du-marche"
    assert theme_packs.slugify("../../etc/passwd") == "etc-passwd"
    assert theme_packs.slugify("") == ""


# --- the palette --------------------------------------------------------------


def test_only_hex_colours_ever_reach_a_stylesheet(user_dir):
    for bad in ("red", "javascript:alert(1)", "#12", "url(x)", "#1234ff; }"):
        with pytest.raises(theme_packs.PackError):
            theme_packs.save_pack(user_dir, "bad", label="Bad", description="",
                                  scheme_colors={"dark": dict(DARK, accent=bad)})


def test_a_scheme_the_app_does_not_have_is_refused(user_dir):
    with pytest.raises(theme_packs.PackError):
        theme_packs.save_pack(user_dir, "bad", label="Bad", description="",
                              scheme_colors={"neon": DARK})


def test_three_colours_become_a_whole_theme(user_dir, made):
    css = theme_packs.render_stylesheet(user_dir, made)
    for variable in (
        "--color-bg", "--color-bg-raised", "--color-text", "--color-text-dim",
        "--color-accent", "--color-accent-text", "--color-highlight-bg",
        "--color-border", "--illo-mount", "--ambience-glow",
        "--firelight-strength",
    ):
        assert variable in css


def test_the_stylesheet_has_the_shape_a_shipped_pack_is_written_in(user_dir, made):
    """A default block, the system-preference answer, and one block per
    scheme so the nav toggle wins over both (F46's contract)."""
    css = theme_packs.render_stylesheet(user_dir, made)
    assert css.startswith("/*")
    assert ":root {" in css
    assert "@media (prefers-color-scheme: light) {" in css
    assert ':root:not([data-theme])' in css
    assert ':root[data-theme="dark"] {' in css
    assert ':root[data-theme="light"] {' in css


def test_a_pack_with_no_pale_scheme_makes_no_promise_about_daylight(user_dir):
    theme_packs.save_pack(user_dir, "night", label="Night", description="",
                          scheme_colors={"dark": DARK})
    css = theme_packs.render_stylesheet(user_dir, "night")
    assert "prefers-color-scheme" not in css


def test_a_broken_palette_costs_a_scheme_not_the_book():
    """theme.json can come back from a backup saying anything at all."""
    css = palette.render_css(
        {"dark": {"bg": "#000000", "text": "red", "accent": "#ffffff"},
         "light": LIGHT},
        ["dark", "light"],
    )
    assert ':root[data-theme="light"]' in css
    assert ':root[data-theme="dark"]' not in css


def test_colour_scheme_follows_the_background_not_the_name():
    """A browser draws its own scrollbars from `color-scheme`, so it has to
    match what is on screen — and someone's "manuscript" may be candlelit."""
    dark = palette.derive({"bg": "#0a0a0a", "text": "#eeeeee", "accent": "#cc8844"})
    pale = palette.derive({"bg": "#f4efe4", "text": "#222222", "accent": "#8a5a1c"})
    assert dark["color-scheme"] == "dark"
    assert pale["color-scheme"] == "light"


def test_the_label_on_the_accent_is_the_one_that_can_be_read():
    """Whichever of the reader's own two colours contrasts with it."""
    derived = palette.derive({"bg": "#101822", "text": "#e8e2d9", "accent": "#d9a441"})
    on_accent = palette.parse_hex(derived["--color-accent-text"])
    accent = palette.parse_hex("#d9a441")
    assert palette.contrast(on_accent, accent) >= 3


# --- the pictures -------------------------------------------------------------


def test_the_catalogue_is_exactly_the_default_packs_pictures():
    """A name in one and not the other is a picture that can never be
    replaced, or a prompt for a picture nothing draws."""
    shipped = {
        p.name for p in (themes.THEMES_DIR / themes.DEFAULT_THEME / "img").iterdir()
        if p.is_file()
    }
    assert {a.filename for a in theme_catalog.CATALOG} == shipped


def test_every_asset_says_where_it_goes_and_what_it_shows():
    for asset in theme_catalog.CATALOG:
        assert asset.where and asset.subject
        assert asset.width > 0 and asset.height > 0


def test_a_prompt_carries_the_world_the_subject_and_the_rules():
    asset = theme_catalog.BY_FILENAME["icon-save.png"]
    prompt = theme_catalog.prompt_for(asset, "A woodblock world, indigo and rust.")
    assert "woodblock world" in prompt
    assert asset.subject in prompt
    # The lessons of F42 and F46, restated on every icon because a
    # generator forgets them between images.
    assert "20 pixels" in prompt
    assert "Outline every shape" in prompt
    assert "160 by 160" in prompt


def test_a_plate_prompt_forbids_the_things_that_had_to_be_undone_by_hand():
    prompt = theme_catalog.prompt_for(theme_catalog.BY_FILENAME["help-lantern.jpg"], "x")
    assert "No lettering" in prompt
    assert "No watermark" in prompt
    assert "No paper border" in prompt


def test_a_prompt_still_reads_when_nobody_described_anything():
    prompt = theme_catalog.prompt_for(theme_catalog.CATALOG[0], "")
    assert "Draw one picture" in prompt


def test_an_uploaded_icon_is_cut_out_and_resized(user_dir, made):
    theme_packs.save_asset(user_dir, made, "icon-save.png", _png((512, 512)))
    saved = Image.open(user_dir / made / "img" / "icon-save.png")
    assert saved.format == "PNG"
    assert saved.mode == "RGBA"
    assert max(saved.size) <= 160
    # The flat background it was asked for is gone: the corner is see-through.
    assert saved.getpixel((1, 1))[3] == 0


def test_an_uploaded_illustration_becomes_a_capped_jpeg(user_dir, made):
    theme_packs.save_asset(user_dir, made, "help-lantern.jpg", _png((2000, 2000)))
    saved = Image.open(user_dir / made / "img" / "help-lantern.jpg")
    assert saved.format == "JPEG"
    assert max(saved.size) <= 700


def test_an_uploaded_tile_keeps_the_shape_it_tiles_at(user_dir, made):
    theme_packs.save_asset(user_dir, made, "tree-map-tile.jpg", _png((900, 600)))
    saved = Image.open(user_dir / made / "img" / "tree-map-tile.jpg")
    assert saved.size == (1024, 1024)


def test_an_upload_is_never_written_through(user_dir, made):
    """Re-encoded like every other image in this app, so nothing rides in
    inside a file that merely claims to be a picture."""
    original = _png((300, 300)).getvalue()
    theme_packs.save_asset(user_dir, made, "help-lantern.jpg", io.BytesIO(original))
    assert (user_dir / made / "img" / "help-lantern.jpg").read_bytes() != original


def test_a_picture_that_is_not_in_the_catalogue_is_refused(user_dir, made):
    for hostile in ("../../index.md", "evil.php", "theme.json", "icon-save.svg"):
        with pytest.raises(theme_packs.PackError):
            theme_packs.save_asset(user_dir, made, hostile, _png())
    assert theme_packs.drawn_assets(user_dir, made) == set()


def test_a_file_that_is_not_an_image_is_refused(user_dir, made):
    with pytest.raises(theme_packs.PackError):
        theme_packs.save_asset(user_dir, made, "icon-save.png", io.BytesIO(b"not a png"))


def test_a_picture_can_be_put_back_to_the_borrowed_one(user_dir, made):
    theme_packs.save_asset(user_dir, made, "icon-save.png", _png())
    assert theme_packs.remove_asset(user_dir, made, "icon-save.png")
    assert theme_packs.drawn_assets(user_dir, made) == set()
    # And the app is back to serving the default pack's.
    assert themes.image_ref(made, "icon-save.png", user_dir)[1] == themes.DEFAULT_THEME


def test_a_pack_serves_its_own_pictures_and_borrows_the_rest(user_dir, made):
    theme_packs.save_asset(user_dir, made, "icon-save.png", _png())
    assert themes.image_ref(made, "icon-save.png", user_dir) == ("user", made, "icon-save.png")
    assert themes.image_ref(made, "icon-draft.png", user_dir)[0:2] == ("builtin", "ranch")


# --- deleting -----------------------------------------------------------------


def test_deleting_a_pack_takes_its_pictures_with_it(user_dir, made):
    theme_packs.save_asset(user_dir, made, "icon-save.png", _png())
    assert theme_packs.delete_pack(user_dir, made)
    assert not (user_dir / made).exists()
    assert made not in themes.available_themes(user_dir)


def test_deleting_leaves_a_folder_someone_put_something_else_in(user_dir, made):
    """This app deletes almost nothing; a folder with a stranger in it is
    left standing rather than taken along."""
    (user_dir / made / "notes.txt").write_text("my sketches")
    assert not theme_packs.delete_pack(user_dir, made)
    assert (user_dir / made / "notes.txt").is_file()


# --- the backup ---------------------------------------------------------------


def test_a_made_theme_travels_in_the_backup(auth_client, stories_dir, user_dir, made):
    storage.create_story(stories_dir, "A story", date(2026, 1, 1), "body")
    theme_packs.save_asset(user_dir, made, "icon-save.png", _png())
    data = auth_client.get("/export").data
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        names = zf.namelist()
    assert "themes/woodblock/theme.json" in names
    assert "themes/woodblock/img/icon-save.png" in names


def test_a_made_theme_comes_back_from_a_backup(stories_dir, user_dir):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-01-01-a-story/index.md", "---\ntitle: A story\n---\nbody\n")
        zf.writestr("themes/woodblock/theme.json", json.dumps({"label": "Woodblock"}))
        zf.writestr("themes/woodblock/img/icon-save.png", _png().getvalue())
        # Not a shape this app writes: a theme folder is not a way to drop
        # arbitrary files into the stories directory.
        zf.writestr("themes/woodblock/img/evil.svg", "<svg/>")
        zf.writestr("themes/woodblock/notes.txt", "nope")
    buf.seek(0)
    storage.import_backup(stories_dir, buf)
    assert (user_dir / "woodblock" / "theme.json").is_file()
    assert (user_dir / "woodblock" / "img" / "icon-save.png").is_file()
    assert not (user_dir / "woodblock" / "img" / "evil.svg").exists()
    assert not (user_dir / "woodblock" / "notes.txt").exists()


def test_a_restored_theme_never_overwrites_one_of_the_same_name(stories_dir, user_dir, made):
    before = (user_dir / made / "theme.json").read_text()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-01-01-a-story/index.md", "---\ntitle: A story\n---\nbody\n")
        zf.writestr("themes/woodblock/theme.json", json.dumps({"label": "Theirs"}))
    buf.seek(0)
    storage.import_backup(stories_dir, buf)
    assert (user_dir / made / "theme.json").read_text() == before


# --- what a strongly-styled world needs from a prompt (F50 follow-up) ---------


CYBERPUNK = {
    "dark": {"bg": "#050508", "text": "#e8faff", "accent": "#fcee0a"},
    "light": {"bg": "#d8e6f0", "text": "#0a1420", "accent": "#00a8b5"},
}


def test_a_prompt_names_the_packs_own_colours():
    """A generator left to pick its own "cyan" picks a different one every
    time, which is most of why a set of thirty-seven drifts apart."""
    prompt = theme_catalog.prompt_for(
        theme_catalog.BY_FILENAME["empty-chest.jpg"], "Neon and chrome.", CYBERPUNK
    )
    assert "#050508" in prompt
    assert "#fcee0a" in prompt
    assert "Nothing outside them" in prompt


def test_a_prompt_names_one_background_not_one_per_scheme():
    """Two backgrounds in one prompt is no background at all."""
    line = theme_catalog.palette_line(CYBERPUNK)
    assert line.count("background") == 1
    # The other scheme still contributes its accent.
    assert "#00a8b5" in line


def test_a_pack_with_no_palette_yet_still_gets_a_usable_prompt():
    for palette_arg in (None, {}, {"dark": "not a palette"}):
        prompt = theme_catalog.prompt_for(theme_catalog.CATALOG[0], "x", palette_arg)
        assert "Palette:" not in prompt
        assert "Subject:" in prompt


def test_a_plate_prompt_forbids_a_scene():
    """The failure a style described as a place produces: thirty-seven
    views of that place with the subject lost inside each one."""
    prompt = theme_catalog.prompt_for(
        theme_catalog.BY_FILENAME["empty-chest.jpg"], "A neon city at night.", CYBERPUNK
    )
    assert "not a view of the world" in prompt
    for absent in ("street", "landscape", "crowd"):
        assert absent in prompt


def test_a_style_built_on_signage_is_given_a_legal_way_to_keep_it():
    """"No lettering" against a genre made of neon signs is a rule that
    gets ignored; this gives the generator somewhere to go instead."""
    prompt = theme_catalog.prompt_for(
        theme_catalog.BY_FILENAME["help-lantern.jpg"], "Neon signs everywhere.", CYBERPUNK
    )
    assert "abstract glowing marks" in prompt
    assert "nothing readable" in prompt


def test_a_plate_is_told_it_hangs_on_both_schemes():
    prompt = theme_catalog.prompt_for(theme_catalog.CATALOG[0], "x", CYBERPUNK)
    assert "both the dark and the pale version" in prompt


def test_an_icon_prompt_forbids_the_glow_that_defeats_the_cutout():
    """A glow is a gradient, and a gradient is what stops the flood fill —
    it comes back as a halo or a box around the icon."""
    prompt = theme_catalog.prompt_for(theme_catalog.BY_FILENAME["icon-save.png"], "Neon.")
    assert "no glow" in prompt
    assert "mid-grey background" in prompt


# --- derivations that survive a saturated palette -----------------------------


def test_a_neon_text_colour_still_leaves_a_readable_dimmed_one():
    """Mixing a saturated text colour toward the background is what a
    plain mix does and what makes it unreadable; the contrast floor is the
    constraint that matters."""
    derived = palette.derive({"bg": "#0d0221", "text": "#ff2a6d", "accent": "#05d9e8"})
    ratio = palette.contrast(
        palette.parse_hex(derived["--color-text-dim"]), palette.parse_hex("#0d0221")
    )
    assert ratio >= palette.DIM_FLOOR - 0.1


def test_a_border_is_pushed_until_it_is_visible():
    derived = palette.derive({"bg": "#0d0221", "text": "#ff2a6d", "accent": "#05d9e8"})
    ratio = palette.contrast(
        palette.parse_hex(derived["--color-border"]), palette.parse_hex("#0d0221")
    )
    assert ratio >= palette.EDGE_FLOOR - 0.1


def test_an_ordinary_palette_is_left_where_it_was():
    """The floors are a rescue for saturated colours, not a redesign of
    the books that were already fine."""
    derived = palette.derive(DARK)
    assert derived["--color-text-dim"] == palette.to_hex(
        palette.mix(palette.parse_hex(DARK["text"]), palette.parse_hex(DARK["bg"]), 0.42)
    )


def test_two_colours_nobody_could_tell_apart_are_reported_not_silently_kept():
    """No derivation can rescue a text colour that is invisible on its own
    background, so the app says so instead of pretending."""
    warnings = theme_packs.palette_warnings(
        {"dark": {"bg": "#2b2f1f", "text": "#4a5236", "accent": "#a8b56b"}}
    )
    assert len(warnings) == 1
    assert "hard to read" in warnings[0]
    assert "saved either way" in warnings[0]


def test_a_readable_palette_is_not_nagged_about():
    assert theme_packs.palette_warnings({"dark": DARK, "light": LIGHT}) == []


def test_the_warning_does_not_stop_the_save(auth_client):
    resp = auth_client.post("/themes/new", data={
        "label": "Olive", "description": "", "schemes": ["dark"],
        "dark-bg": "#2b2f1f", "dark-text": "#4a5236", "dark-accent": "#a8b56b",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert "hard to read" in resp.data.decode()
    user_dir = themes.user_themes_dir(auth_client.application.config["STORIES_DIR"])
    assert "olive" in themes.available_themes(user_dir)
