"""Tests for FEATURES.md F50's routes: the theme-making pages themselves.

Who can reach them is the point of most of this. Making a theme is not
reading a story — it writes files into the book's own folder — so it sits
behind the same gate a backup restore does: the admin when accounts are on,
the single password-holder when they are not, and nobody else. The two
routes that *serve* a made pack are public on purpose, because the login
page is dressed by the pack too, and they are the ones tested hardest for
what they will refuse to serve.
"""

import io

import pytest
from PIL import Image

from app import theme_packs, themes
from tests.conftest import _bootstrap_admin, _login, _request_account

DARK = {"bg": "#101822", "text": "#e8e2d9", "accent": "#d9a441"}
LIGHT = {"bg": "#faf6ef", "text": "#2a2520", "accent": "#a9701c"}


def _png(size=(400, 400)):
    im = Image.new("RGB", size, (128, 128, 128))
    im.paste(Image.new("RGB", (size[0] // 2, size[1] // 2), (200, 40, 40)),
             (size[0] // 4, size[1] // 4))
    buf = io.BytesIO()
    im.save(buf, format="PNG")
    buf.seek(0)
    return buf


def _make(client, name="woodblock", label="Woodblock", description="indigo and rust"):
    stories_dir = client.application.config["STORIES_DIR"]
    theme_packs.save_pack(
        themes.user_themes_dir(stories_dir), name,
        label=label, description=description,
        scheme_colors={"dark": DARK, "light": LIGHT},
    )
    return name


# --- who can get in -----------------------------------------------------------


def test_a_single_password_book_can_make_themes(auth_client):
    """There is one trust level there, and it belongs to whoever set the
    book up — the same reasoning the backup restore is gated by."""
    assert auth_client.get("/themes").status_code == 200


def test_a_logged_out_visitor_cannot(client):
    for path in ("/themes", "/themes/new"):
        resp = client.get(path)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]


@pytest.fixture
def admin_client(app_factory):
    app = app_factory(ACCOUNTS_ENABLED=True)
    client = app.test_client()
    _bootstrap_admin(client)
    _login(client, "papa", "hunter22")
    return client


@pytest.fixture
def member_client(admin_client):
    """A second account in the same book, approved by the admin as
    ordinary family rather than as another admin."""
    app = admin_client.application
    client = app.test_client()
    _request_account(client, display_name="Mamie", username="mamie", password="hunter22")
    admin_client.post(
        "/admin/accounts/pending/mamie",
        data={"new_person_name": "Mamie", "role": "family"},
    )
    _login(client, "mamie", "hunter22")
    return client


def test_an_admin_can_make_themes(admin_client):
    assert admin_client.get("/themes").status_code == 200


def test_a_family_member_cannot(member_client):
    """404 rather than 403, like every other admin route here: the page's
    existence isn't news a guest needs."""
    assert member_client.get("/").status_code == 200
    for path in ("/themes", "/themes/new"):
        assert member_client.get(path).status_code == 404


def test_a_family_member_cannot_write_one_either(member_client, admin_client):
    name = _make(admin_client)
    resp = member_client.post(
        f"/themes/{name}/pictures/icon-save.png",
        data={"file": (_png(), "icon.png")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 404
    stories_dir = admin_client.application.config["STORIES_DIR"]
    assert theme_packs.drawn_assets(themes.user_themes_dir(stories_dir), name) == set()


def test_a_family_member_cannot_delete_one(member_client, admin_client):
    name = _make(admin_client)
    assert member_client.post(f"/themes/{name}/delete").status_code == 404
    stories_dir = admin_client.application.config["STORIES_DIR"]
    assert name in themes.available_themes(themes.user_themes_dir(stories_dir))


# --- making one ---------------------------------------------------------------


def test_making_a_theme_writes_it_and_goes_to_the_pictures(auth_client):
    resp = auth_client.post("/themes/new", data={
        "label": "Estampe Japonaise", "description": "indigo and rust",
        "schemes": ["dark", "light"],
        "dark-bg": "#101822", "dark-text": "#e8e2d9", "dark-accent": "#d9a441",
        "light-bg": "#faf6ef", "light-text": "#2a2520", "light-accent": "#a9701c",
    })
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/themes/estampe-japonaise/pictures")
    stories_dir = auth_client.application.config["STORIES_DIR"]
    user_dir = themes.user_themes_dir(stories_dir)
    assert themes.label("estampe-japonaise", user_dir) == "Estampe Japonaise"


def test_a_bad_colour_comes_back_as_a_message_not_a_stack_trace(auth_client):
    resp = auth_client.post("/themes/new", data={
        "label": "Bad", "description": "", "schemes": ["dark"],
        "dark-bg": "cornflower", "dark-text": "#ffffff", "dark-accent": "#d9a441",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert "hex colour" in resp.data.decode()


def test_only_the_ticked_schemes_are_saved(auth_client):
    auth_client.post("/themes/new", data={
        "label": "Night", "description": "", "schemes": ["dark"],
        "dark-bg": "#101822", "dark-text": "#e8e2d9", "dark-accent": "#d9a441",
        "light-bg": "#faf6ef", "light-text": "#2a2520", "light-accent": "#a9701c",
    })
    user_dir = themes.user_themes_dir(auth_client.application.config["STORIES_DIR"])
    assert themes.color_schemes("night", user_dir) == ["dark"]


def test_the_sheet_lists_every_picture_with_a_prompt(auth_client):
    name = _make(auth_client)
    html = auth_client.get(f"/themes/{name}/pictures").data.decode()
    from app import theme_catalog

    for asset in theme_catalog.CATALOG:
        assert asset.filename in html
    # The world someone described is in each prompt, which is what makes
    # thirty-seven drawings look like one book.
    assert "indigo and rust" in html
    assert "0 of 37" in html or "0 of {}".format(len(theme_catalog.CATALOG)) in html


def test_uploading_a_picture_puts_it_in_the_pack(auth_client):
    name = _make(auth_client)
    resp = auth_client.post(
        f"/themes/{name}/pictures/icon-save.png",
        data={"file": (_png(), "whatever-the-generator-called-it.png")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 302
    user_dir = themes.user_themes_dir(auth_client.application.config["STORIES_DIR"])
    assert theme_packs.drawn_assets(user_dir, name) == {"icon-save.png"}


def test_the_uploads_own_filename_is_never_used(auth_client):
    """The generator names files whatever it likes; the catalogue decides
    where each one goes, so the upload's name is not a path at all."""
    name = _make(auth_client)
    auth_client.post(
        f"/themes/{name}/pictures/icon-save.png",
        data={"file": (_png(), "../../../evil.png")},
        content_type="multipart/form-data",
    )
    stories_dir = auth_client.application.config["STORIES_DIR"]
    assert not (stories_dir / "evil.png").exists()
    assert theme_packs.drawn_assets(themes.user_themes_dir(stories_dir), name) == {
        "icon-save.png"
    }


def test_a_picture_that_is_not_in_the_catalogue_is_a_404(auth_client):
    name = _make(auth_client)
    resp = auth_client.post(
        f"/themes/{name}/pictures/evil.png",
        data={"file": (_png(), "evil.png")},
        content_type="multipart/form-data",
    )
    assert resp.status_code in (302, 404)
    user_dir = themes.user_themes_dir(auth_client.application.config["STORIES_DIR"])
    assert theme_packs.drawn_assets(user_dir, name) == set()


def test_deleting_a_theme_from_the_page(auth_client):
    name = _make(auth_client)
    resp = auth_client.post(f"/themes/{name}/delete")
    assert resp.status_code == 302
    user_dir = themes.user_themes_dir(auth_client.application.config["STORIES_DIR"])
    assert name not in themes.available_themes(user_dir)


def test_a_shipped_pack_cannot_be_edited_or_deleted(auth_client):
    for path in ("/themes/ranch/edit", "/themes/orbit/edit"):
        assert auth_client.get(path).status_code == 404
    assert auth_client.post("/themes/orbit/delete").status_code == 404
    assert "orbit" in themes.builtin_themes()


# --- serving one --------------------------------------------------------------


def test_a_made_theme_dresses_the_book(auth_client):
    name = _make(auth_client)
    auth_client.post(
        f"/themes/{name}/pictures/icon-new-story.png",
        data={"file": (_png(), "icon.png")}, content_type="multipart/form-data",
    )
    auth_client.post(f"/theme/{name}", data={"next": "/"})
    html = auth_client.get("/").data.decode()
    assert f"/themes/{name}/theme.css" in html
    assert f"/themes/{name}/img/icon-new-story.png" in html
    # ...and everything it hasn't drawn is still the default pack's.
    assert "/static/themes/ranch/img/" in html


def test_the_generated_stylesheet_is_served_as_css(auth_client):
    name = _make(auth_client)
    resp = auth_client.get(f"/themes/{name}/theme.css")
    assert resp.status_code == 200
    assert resp.mimetype == "text/css"
    assert "--color-bg: #101822" in resp.data.decode()


def test_a_made_packs_pictures_are_public_like_static_ones(client, auth_client):
    """The login page is dressed by the pack too, and a login screen with
    broken pictures would be the first thing a family saw."""
    name = _make(auth_client)
    auth_client.post(
        f"/themes/{name}/pictures/login-campfire.jpg",
        data={"file": (_png(), "x.png")}, content_type="multipart/form-data",
    )
    assert client.get(f"/themes/{name}/img/login-campfire.jpg").status_code == 200
    assert client.get(f"/themes/{name}/theme.css").status_code == 200


def test_the_media_route_serves_nothing_but_a_packs_own_pictures(auth_client):
    name = _make(auth_client)
    stories_dir = auth_client.application.config["STORIES_DIR"]
    (themes.user_themes_dir(stories_dir) / name / "img" / "secret.txt").write_text("no")
    for hostile in ("secret.txt", "..%2f..%2findex.md", "theme.json"):
        assert auth_client.get(f"/themes/{name}/img/{hostile}").status_code == 404


def test_no_route_reaches_outside_the_themes_folder(auth_client, stories_dir):
    (stories_dir / "private.md").write_text("secret")
    for path in (
        "/themes/../img/private.md",
        "/themes/..%2f..%2fprivate.md/theme.css",
        "/themes/people/img/icon-save.png",
    ):
        assert auth_client.get(path).status_code == 404


def test_a_pack_nobody_made_is_a_404(auth_client):
    assert auth_client.get("/themes/nothing-here/theme.css").status_code == 404
    assert auth_client.get("/themes/ranch/theme.css").status_code == 404


def test_a_made_theme_is_offered_in_the_nav_picker(auth_client):
    _make(auth_client, label="Woodblock")
    html = auth_client.get("/").data.decode()
    assert "/theme/woodblock" in html
    assert "Woodblock" in html


def test_the_way_in_is_only_shown_to_someone_who_can_use_it(admin_client, member_client):
    assert "/themes" in admin_client.get("/").data.decode()
    assert 'href="/themes"' not in member_client.get("/").data.decode()


def test_the_sheet_shows_the_pack_being_edited_not_the_one_being_worn(auth_client):
    """An admin wearing orbit while filling in their own theme must see
    their own pictures on the sheet, and orbit's nowhere on it."""
    name = _make(auth_client)
    auth_client.post(
        f"/themes/{name}/pictures/icon-save.png",
        data={"file": (_png(), "x.png")}, content_type="multipart/form-data",
    )
    auth_client.post("/theme/orbit", data={"next": "/"})
    sheet = auth_client.get(f"/themes/{name}/pictures").data.decode()
    rows = sheet.split('class="asset-sheet__shot"')[1:]
    assert any(f"/themes/{name}/img/icon-save.png" in row for row in rows)
    assert not any("/static/themes/orbit/img/" in row for row in rows)
