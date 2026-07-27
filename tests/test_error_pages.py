"""Tests for FEATURES.md F37: every error renders as a real page.

A bare Werkzeug error page carries no viewport meta and no stylesheet, so
on a phone it lays out at 980px and reads as "the whole site is broken".
That mattered little while 400s were near-unreachable; F36's ProxyFix made
Flask-WTF's HTTPS referer check active behind a reverse proxy, so a
misconfigured proxy now turns *every* form submission into one. These
tests pin the shape of the fix: HTML errors extend base.html, API errors
stay JSON.
"""

from datetime import date

import pytest
from flask import abort

from app import storage

# Anything rendered through base.html carries these; a bare Werkzeug page
# carries neither, which is exactly the mobile-layout bug.
VIEWPORT = 'name="viewport"'
STYLESHEET = "css/main.css"


@pytest.fixture
def erroring_app(app_factory):
    """An app with routes that raise each error we handle, so the handlers
    are exercised through a real request rather than called directly."""
    app = app_factory()

    @app.route("/boom/<int:code>")
    def boom(code):
        abort(code)

    @app.route("/api/boom/<int:code>")
    def api_boom(code):
        abort(code)

    return app


@pytest.mark.parametrize("code", [400, 403, 413, 429])
def test_error_pages_are_real_pages(erroring_app, code):
    resp = erroring_app.test_client().get(f"/boom/{code}")
    assert resp.status_code == code
    html = resp.data.decode()
    assert VIEWPORT in html, f"{code} page has no viewport meta — 980px on a phone"
    assert STYLESHEET in html, f"{code} page has no stylesheet"


def test_404_is_still_its_own_illustrated_page(client):
    html = client.get("/no-such-page").data.decode()
    assert VIEWPORT in html
    assert "never did" in html


@pytest.mark.parametrize("code", [400, 403, 413, 429])
def test_api_errors_stay_json(erroring_app, code):
    resp = erroring_app.test_client().get(f"/api/boom/{code}")
    assert resp.status_code == code
    assert resp.is_json
    assert "error" in resp.get_json()


def test_api_404_is_json_not_html(client):
    resp = client.get("/api/nothing-here")
    assert resp.status_code == 404
    assert resp.is_json


def test_upload_too_large_still_says_the_limit(erroring_app):
    """The 413 message carried the 128 MB number before F37; keep it."""
    resp = erroring_app.test_client().get("/api/boom/413")
    assert "128 MB" in resp.get_json()["error"]


# --- CSRF failures ----------------------------------------------------------


@pytest.fixture
def csrf_app(app_factory):
    return app_factory(WTF_CSRF_ENABLED=True)


def test_csrf_failure_is_a_readable_page_not_bad_request(csrf_app):
    resp = csrf_app.test_client().post("/login", data={"password": "test-password"})
    assert resp.status_code == 400
    html = resp.data.decode()
    assert VIEWPORT in html
    assert STYLESHEET in html
    assert "gone stale" in html
    assert "Bad Request" not in html
    assert "nothing was saved or lost" in html


def test_csrf_failure_on_the_api_is_json(csrf_app, stories_dir):
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "b")
    resp = csrf_app.test_client().put(
        f"/api/stories/{story_id}",
        json={"title": "x", "date": "2026-03-01", "markdown": "y"},
    )
    assert resp.status_code == 400
    assert resp.is_json
    assert "expired" in resp.get_json()["error"].lower()


def test_referrer_mismatch_names_the_reverse_proxy(csrf_app):
    """The failure a misconfigured reverse proxy produces should point at
    the proxy, not leave the family staring at "Bad Request"."""
    client = csrf_app.test_client()
    # Fetch the token from the same origin we post to, so the *token* is
    # valid and the referrer check is what actually fails.
    page = client.get("/login", base_url="https://potage.example").data.decode()
    token = page.split('name="csrf_token" value="')[1].split('"')[0]
    resp = client.post(
        "/login",
        data={"csrf_token": token, "password": "test-password"},
        headers={"Referer": "https://somewhere-else.example/login"},
        base_url="https://potage.example",
    )
    assert resp.status_code == 400
    html = resp.data.decode()
    assert "reverse proxy" in html
    assert "X-Forwarded-Host" in html


def test_a_matching_referrer_over_https_still_logs_in(csrf_app):
    """The guard must not fire on the correctly configured setup."""
    client = csrf_app.test_client()
    page = client.get("/login", base_url="https://potage.example").data.decode()
    token = page.split('name="csrf_token" value="')[1].split('"')[0]
    resp = client.post(
        "/login",
        data={"csrf_token": token, "password": "test-password"},
        headers={"Referer": "https://potage.example/login"},
        base_url="https://potage.example",
    )
    assert resp.status_code == 302
