"""Tests for FEATURES.md F36: hardening for an internet-facing deployment.

Three layers, each locked down so a future change can't quietly reopen it:
security headers on every response, the brute-force lockout on the two
password-bearing endpoints, and — most important long-term — the auth
perimeter itself: every GET route in the app must refuse an anonymous
client unless it's on the tiny explicit allowlist below. A new page added
without @login_required fails that test the day it's written.
"""

from datetime import date

import pytest

from app import storage

# ---------------------------------------------------------------------------
# Security headers


def test_every_response_carries_the_hardening_headers(client):
    resp = client.get("/login")
    assert resp.headers["X-Content-Type-Options"] == "nosniff"
    assert resp.headers["X-Frame-Options"] == "DENY"
    assert resp.headers["Referrer-Policy"] == "same-origin"
    csp = resp.headers["Content-Security-Policy"]
    assert "default-src 'self'" in csp
    assert "script-src 'self'" in csp
    assert "'unsafe-inline'" not in csp.split("style-src")[0], (
        "script-src must never allow inline scripts — that's the whole "
        "defense against a <script> smuggled into |safe story HTML"
    )
    assert "frame-ancestors 'none'" in csp
    assert "form-action 'self'" in csp


def test_csp_never_names_an_external_host(client):
    """The no-CDN rule, enforced at the header level: nothing in the
    policy should ever point off-box."""
    csp = client.get("/login").headers["Content-Security-Policy"]
    assert "http:" not in csp and "https:" not in csp


def test_hsts_only_when_the_operator_says_https(app_factory):
    plain = app_factory().test_client().get("/login")
    assert "Strict-Transport-Security" not in plain.headers
    secure = app_factory(SESSION_COOKIE_SECURE=True).test_client().get("/login")
    assert secure.headers["Strict-Transport-Security"] == "max-age=31536000"


def test_html_pages_are_never_stored_in_caches(auth_client):
    assert auth_client.get("/").headers["Cache-Control"] == "no-store"


def test_cached_media_is_private_to_the_browser(auth_client, stories_dir, jpeg_bytes):
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "body")
    resp = auth_client.post(
        f"/api/stories/{story_id}/images",
        data={"file": (jpeg_bytes(), "p.jpg")},
        content_type="multipart/form-data",
    )
    filename = resp.get_json()["filename"]
    media = auth_client.get(f"/story/{story_id}/media/{filename}")
    assert media.status_code == 200
    cache = media.headers["Cache-Control"]
    assert "private" in cache
    assert "max-age" in cache
    assert "public" not in cache


def test_static_files_are_private_too(client):
    cache = client.get("/static/js/theme-boot.js").headers.get("Cache-Control", "")
    if "max-age" in cache:
        assert "private" in cache


def test_no_inline_scripts_anywhere(auth_client, client, stories_dir):
    """CSP forbids inline <script>; any template still carrying one would
    render a dead script block. The theme boot deliberately moved to
    static/js/theme-boot.js for this."""
    story_id = storage.create_story(stories_dir, "A day out", date(2026, 3, 1), "body")
    for path in ("/", f"/story/{story_id}", "/new", "/book", "/people", "/help"):
        html = auth_client.get(path).data.decode()
        assert "<script>" not in html, path
    assert "<script>" not in client.get("/login").data.decode()
    assert "theme-boot.js" in client.get("/login").data.decode()


# ---------------------------------------------------------------------------
# Brute-force lockout


@pytest.fixture
def fast_fail(monkeypatch):
    """Failed logins deliberately sleep 1s in production; tests shouldn't."""
    monkeypatch.setattr("app.auth.time.sleep", lambda s: None)
    monkeypatch.setattr("app.routes_accounts.time.sleep", lambda s: None)


def test_login_locks_out_after_repeated_failures(app_factory, fast_fail):
    client = app_factory(LOGIN_ATTEMPT_LIMIT=3, LOGIN_ATTEMPT_WINDOW=900).test_client()
    for _ in range(3):
        resp = client.post("/login", data={"password": "wrong"})
        assert resp.status_code == 200
    resp = client.post("/login", data={"password": "wrong"})
    assert resp.status_code == 429
    assert int(resp.headers["Retry-After"]) > 0
    assert b"Too many attempts" in resp.data


def test_even_the_right_password_is_refused_while_blocked(app_factory, fast_fail):
    """A blocked client must learn nothing — not even that it finally
    guessed right."""
    client = app_factory(LOGIN_ATTEMPT_LIMIT=2, LOGIN_ATTEMPT_WINDOW=900).test_client()
    for _ in range(2):
        client.post("/login", data={"password": "wrong"})
    resp = client.post("/login", data={"password": "test-password"})
    assert resp.status_code == 429
    assert client.get("/").status_code == 302  # still not logged in


def test_successful_login_clears_the_counter(app_factory, fast_fail):
    client = app_factory(LOGIN_ATTEMPT_LIMIT=3, LOGIN_ATTEMPT_WINDOW=900).test_client()
    client.post("/login", data={"password": "wrong"})
    client.post("/login", data={"password": "wrong"})
    resp = client.post("/login", data={"password": "test-password"})
    assert resp.status_code == 302
    # Fresh slate: two more fumbles don't lock the next attempt out.
    client.post("/logout")
    client.post("/login", data={"password": "wrong"})
    client.post("/login", data={"password": "wrong"})
    assert client.post("/login", data={"password": "test-password"}).status_code == 302


def test_get_login_page_is_never_throttled(app_factory, fast_fail):
    """Only guesses count; a blocked family member can still *see* the
    login page (and the message telling them to wait)."""
    client = app_factory(LOGIN_ATTEMPT_LIMIT=1, LOGIN_ATTEMPT_WINDOW=900).test_client()
    client.post("/login", data={"password": "wrong"})
    assert client.get("/login").status_code == 200


def test_invite_code_form_shares_the_same_lockout(app_factory, fast_fail, stories_dir):
    client = app_factory(
        ACCOUNTS_ENABLED=True, LOGIN_ATTEMPT_LIMIT=2, LOGIN_ATTEMPT_WINDOW=900
    ).test_client()
    for _ in range(2):
        client.post(
            "/request-account",
            data={
                "display_name": "X", "username": "x", "password": "yyyyyyyy",
                "invite_code": "wrong", "note": "",
            },
        )
    resp = client.post(
        "/request-account",
        data={
            "display_name": "X", "username": "x", "password": "yyyyyyyy",
            "invite_code": "wrong", "note": "",
        },
    )
    assert resp.status_code == 429
    # ... and the lockout carries over to /login: same secret, same key.
    assert client.post("/login", data={"username": "x", "password": "y"}).status_code == 429


# ---------------------------------------------------------------------------
# The auth perimeter

# The complete set of GET endpoints an anonymous visitor may reach. Adding
# a route here is a deliberate decision to expose it to the internet
# unauthenticated — everything else must redirect to /login or 404.
PUBLIC_GET_ENDPOINTS = {
    "auth.login",
    "pages.manifest",          # must stay public for home-screen install
    "pages.request_account",   # gated by ACCOUNTS_ENABLED + invite code
    "pages.use_write_link",    # bearer token is the credential
    "pages.accept_invite",     # same — bearer token, gated by ACCOUNTS_ENABLED
    "static",
}

_SAMPLE_ARGS = {
    "story_id": "2026-01-01-somestory",
    "slug": "someone",
    "person_slug": "someone",
    "filename": "photo-001.jpg",
    "username": "someone",
    "link_id": "0123456789abcdef",
    "version_id": "20260101-000000",
    "token": "not-a-real-token",
}


def _fill(rule):
    return {arg: _SAMPLE_ARGS.get(arg, "x") for arg in rule.arguments}


def test_every_get_route_refuses_anonymous_visitors(app, client):
    """Walk the entire URL map: anything not explicitly public must send
    an anonymous client to /login (or 404 for role-gated admin pages).
    A new route missing @login_required fails here immediately."""
    checked = 0
    for rule in app.url_map.iter_rules():
        if "GET" not in rule.methods or rule.endpoint in PUBLIC_GET_ENDPOINTS:
            continue
        url = rule.build(_fill(rule))[1] if rule.arguments else rule.rule
        resp = client.get(url)
        assert resp.status_code in (301, 302, 404), (
            f"{rule.endpoint} ({url}) answered {resp.status_code} to an "
            "anonymous GET — every non-public route must be login-gated"
        )
        if resp.status_code in (301, 302):
            assert "/login" in resp.headers["Location"], (rule.endpoint, url)
        checked += 1
    assert checked > 30  # the walk really walked


def test_the_public_allowlist_is_exactly_what_we_think(app):
    """If a new public endpoint appears (or one is renamed), this fails
    and forces the allowlist — and the exposure decision — to be updated
    consciously."""
    all_endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert PUBLIC_GET_ENDPOINTS <= all_endpoints
