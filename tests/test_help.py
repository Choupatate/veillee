"""Tests for FEATURES.md F33: the in-app Help page (/help), a plain-language
guide for the family using the app rather than a developer reading
README.md/FEATURES.md."""

from tests.conftest import _bootstrap_admin, _login


def test_help_requires_auth(client):
    resp = client.get("/help")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_help_page_renders_core_sections(auth_client):
    resp = auth_client.get("/help")
    assert resp.status_code == 200
    html = resp.data.decode()
    assert "Writing a memory" in html
    assert "family tree" in html
    assert "Growing up" in html
    assert "Reading it back" in html
    assert "Voice memos" in html
    assert "Keeping it safe" in html


def test_help_page_hides_accounts_section_by_default(auth_client):
    html = auth_client.get("/help").data.decode()
    assert "Family accounts" not in html


def test_help_page_shows_accounts_section_when_enabled(app_factory):
    accounts_app = app_factory(ACCOUNTS_ENABLED=True)
    client = accounts_app.test_client()
    _bootstrap_admin(client, username="papa", password="hunter22")
    _login(client, "papa", "hunter22")
    html = client.get("/help").data.decode()
    assert "Family accounts" in html


def test_nav_links_to_help_when_authed(auth_client):
    html = auth_client.get("/").data.decode()
    assert 'href="/help"' in html
    assert ">Help<" in html


def test_nav_hides_help_link_when_logged_out(client):
    html = client.get("/login").data.decode()
    assert 'href="/help"' not in html
