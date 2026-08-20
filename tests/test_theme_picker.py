"""Tests for FEATURES.md F48: choosing a theme pack from the interface.

F46 made the art direction a folder and `STORYBOOK_THEME` chose it once,
at startup. This adds a picker in the nav — a cookie, so it dresses one
browser and reaches no one else's. The two rules worth guarding are that
the cookie really is scoped to its own browser, and that a bad cookie
never takes the book down: an install whose pack was deleted, or whose
cookie was hand-edited, still renders.
"""

from app import themes


# --- resolving the two sources of a pack name ---------------------------------


def test_a_readers_choice_wins_over_the_books_default():
    assert themes.pick_theme("orbit", "ranch") == "orbit"


def test_no_choice_leaves_the_books_own_pack():
    assert themes.pick_theme(None, "orbit") == "orbit"
    assert themes.pick_theme("", "orbit") == "orbit"


def test_a_pack_that_no_longer_exists_falls_back_rather_than_failing():
    """An install that dropped a pack folder must not 500 for every reader
    still carrying its cookie."""
    assert themes.pick_theme("packed-up-and-left", "orbit") == "orbit"


def test_a_hand_edited_cookie_cannot_name_a_path():
    for hostile in ("../../etc", "..", "/etc/passwd", "ranch/../orbit", "RANCH"):
        assert themes.pick_theme(hostile, "ranch") == "ranch"


def test_everything_missing_still_yields_the_default_pack():
    assert themes.pick_theme(None, None) == themes.DEFAULT_THEME
    assert themes.pick_theme("nope", "also-nope") == themes.DEFAULT_THEME


# --- what the picker shows ----------------------------------------------------


def test_every_shipped_pack_names_itself_and_shows_its_colours():
    """A pack is picked before it is applied, so it has to be recognisable
    from the picker alone."""
    for name in themes.available_themes():
        assert themes.label(name)
        swatch = themes.swatch(name)
        assert 2 <= len(swatch) <= 3, name


def test_a_pack_without_a_manifest_still_has_a_name():
    assert themes.label("wild-west") == "Wild West"


def test_only_real_colours_reach_the_style_attribute():
    """The swatch is pasted into `style="background: ..."`, so the
    allowlist is what stands between a manifest and the page."""
    assert themes.swatch("nonexistent-pack") == []


def test_the_picker_is_in_the_nav(auth_client):
    html = auth_client.get("/").data.decode()
    assert 'class="pack-picker"' in html
    for name in themes.available_themes():
        assert f"/theme/{name}" in html
        assert themes.label(name) in html


def test_the_current_pack_is_marked_not_removed(auth_client):
    """Same reasoning as the language picker: the row must not reflow when
    you switch, and a screen reader needs to know where it is."""
    html = auth_client.get("/").data.decode()
    current = html.split('action="/theme/ranch"')[1].split("</form>")[0]
    assert 'aria-current="true"' in current
    assert "pack-picker__btn--active" in current


def test_a_one_pack_install_shows_no_picker(auth_client, monkeypatch, tmp_path):
    """A picker offering one choice is a button that does nothing."""
    solo = tmp_path / "themes"
    (solo / "ranch").mkdir(parents=True)
    monkeypatch.setattr(themes, "THEMES_DIR", solo)
    html = auth_client.get("/").data.decode()
    assert 'class="pack-picker"' not in html


# --- setting it ---------------------------------------------------------------


def test_choosing_a_pack_sets_a_cookie_and_returns_you_to_the_page(auth_client):
    resp = auth_client.post(
        "/theme/orbit", data={"next": "/book"}, follow_redirects=False
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/book")
    cookie = resp.headers["Set-Cookie"]
    assert f"{themes.COOKIE_NAME}=orbit" in cookie
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie


def test_the_cookie_actually_changes_what_is_served(auth_client):
    before = auth_client.get("/").data.decode()
    assert "/static/themes/orbit/" not in before

    auth_client.post("/theme/orbit", data={"next": "/"})
    after = auth_client.get("/").data.decode()
    assert "/static/themes/orbit/theme.css" in after
    assert "/static/themes/orbit/img/" in after


def test_the_pack_decides_which_schemes_the_toggle_offers(auth_client):
    """orbit has no aged paper in it, and the nav toggle has to follow the
    pack a reader is actually looking at (F46)."""
    assert 'data-schemes="dark light manuscript"' in auth_client.get("/").data.decode()
    auth_client.post("/theme/orbit", data={"next": "/"})
    assert 'data-schemes="dark light"' in auth_client.get("/").data.decode()


def test_an_unknown_pack_is_a_404_not_a_cookie(auth_client):
    resp = auth_client.post("/theme/vaporwave", data={"next": "/"})
    assert resp.status_code == 404
    assert themes.COOKIE_NAME not in resp.headers.get("Set-Cookie", "")


def test_a_traversal_in_the_url_never_reaches_the_route(auth_client):
    assert auth_client.post("/theme/..", data={"next": "/"}).status_code in (404, 405)


def test_it_cannot_be_turned_into_an_open_redirect(auth_client):
    resp = auth_client.post(
        "/theme/orbit", data={"next": "https://example.com/"}, follow_redirects=False
    )
    assert "example.com" not in resp.headers["Location"]


def test_get_is_not_a_way_to_change_it(auth_client):
    assert auth_client.get("/theme/orbit").status_code == 405


def test_choosing_a_pack_needs_the_csrf_token(app_factory):
    """Every other state change is CSRF-protected; a preference someone
    else can flip for you is still someone else writing to your browser."""
    app = app_factory(WTF_CSRF_ENABLED=True)
    client = app.test_client()
    assert client.post("/theme/orbit", data={"next": "/"}).status_code == 400


def test_it_works_before_logging_in(client):
    """The login page is drawn by the pack too, so the choice has to be
    reachable from it — same reasoning as the language picker."""
    resp = client.post("/theme/orbit", data={"next": "/login"}, follow_redirects=False)
    assert resp.status_code == 302
    assert f"{themes.COOKIE_NAME}=orbit" in resp.headers["Set-Cookie"]
    assert "/static/themes/orbit/theme.css" in client.get("/login").data.decode()


def test_the_choice_survives_logging_out(auth_client):
    auth_client.post("/theme/orbit", data={"next": "/"})
    auth_client.post("/logout")
    assert "/static/themes/orbit/theme.css" in auth_client.get("/login").data.decode()


def test_one_browsers_choice_is_not_another_browsers(app):
    """The whole point of the cookie: the book's art direction is still
    whatever STORYBOOK_THEME says for everyone who hasn't chosen."""
    mine = app.test_client()
    mine.post("/login", data={"password": "test-password"})
    mine.post("/theme/orbit", data={"next": "/"})
    assert "/static/themes/orbit/theme.css" in mine.get("/").data.decode()

    yours = app.test_client()
    yours.post("/login", data={"password": "test-password"})
    assert "/static/themes/orbit/theme.css" not in yours.get("/").data.decode()


def test_a_stale_cookie_renders_the_books_pack_instead_of_failing(auth_client):
    auth_client.set_cookie(themes.COOKIE_NAME, "a-pack-since-deleted")
    resp = auth_client.get("/")
    assert resp.status_code == 200
    assert "/static/themes/ranch/img/" in resp.data.decode()
