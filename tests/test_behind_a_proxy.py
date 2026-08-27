"""What `compose.https.yml` sets, and why both settings must be right.

Running Veillée behind Caddy on a domain (F62) means two environment
variables that are easy to omit, silently wrong when omitted, and
impossible to notice from the browser:

- `STORYBOOK_TRUSTED_PROXIES=1`, without which every visitor arrives as
  the proxy's IP and the login throttle (F36) counts the whole internet on
  one counter — so one attacker guessing passwords locks out the family.
- `STORYBOOK_COOKIE_SECURE=1`, without which the session cookie is not
  marked `Secure` and will happily travel over plain HTTP.

The compose file ships them set. These are the tests that say what "set"
has to mean, so that a future edit to that file which drops one fails here
rather than in somebody's house.
"""

import pytest

from app import create_app

from tests.conftest import BASE_TEST_CONFIG


@pytest.fixture
def behind_caddy(monkeypatch, stories_dir):
    """The app as `compose.https.yml` runs it."""
    monkeypatch.setenv("STORYBOOK_TRUSTED_PROXIES", "1")
    monkeypatch.setenv("STORYBOOK_COOKIE_SECURE", "1")
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(stories_dir))
    monkeypatch.setenv("STORYBOOK_PASSWORD", "test-password")
    monkeypatch.setenv("STORYBOOK_SECRET_KEY", "test-secret-key")
    return create_app(test_config={"TESTING": True, "WTF_CSRF_ENABLED": False})


@pytest.fixture
def no_proxy(monkeypatch, stories_dir):
    """The default: nothing in front, and forwarded headers are lies."""
    monkeypatch.delenv("STORYBOOK_TRUSTED_PROXIES", raising=False)
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(stories_dir))
    return create_app(test_config={"STORIES_DIR": stories_dir, **BASE_TEST_CONFIG})


VISITOR = "203.0.113.9"


def _exhaust(client, forwarded_for, limit):
    for _ in range(limit + 1):
        client.post("/login", data={"password": "wrong"},
                    headers={"X-Forwarded-For": forwarded_for})


def test_without_a_proxy_the_header_is_ignored(no_proxy):
    """The default has to fail the other way round.

    Trusting `X-Forwarded-For` when nothing sets it lets any client claim
    any IP and walk straight past the throttle by inventing a new one each
    time. So with no proxy configured, two different forwarded addresses
    must still share a counter — the header is not consulted at all.
    """
    client = no_proxy.test_client()
    _exhaust(client, "198.51.100.66", no_proxy.config["LOGIN_ATTEMPT_LIMIT"])

    pretending = client.post("/login", data={"password": "wrong"},
                             headers={"X-Forwarded-For": VISITOR})
    assert pretending.status_code == 429


def test_one_attacker_cannot_lock_out_the_family(behind_caddy):
    """The consequence, end to end: a run of failures from one address must
    not block a different one. Behind a proxy with the setting missing,
    both would key on Caddy's IP and the second visitor would be locked out
    by the first."""
    client = behind_caddy.test_client()
    _exhaust(client, "198.51.100.66", behind_caddy.config["LOGIN_ATTEMPT_LIMIT"])

    blocked = client.post("/login", data={"password": "wrong"},
                          headers={"X-Forwarded-For": "198.51.100.66"})
    innocent = client.post("/login", data={"password": "test-password"},
                           headers={"X-Forwarded-For": VISITOR})

    assert blocked.status_code == 429
    assert innocent.status_code == 302


def test_the_session_cookie_is_marked_secure(behind_caddy):
    client = behind_caddy.test_client()
    resp = client.post("/login", data={"password": "test-password"},
                       headers={"X-Forwarded-For": VISITOR, "X-Forwarded-Proto": "https"},
                       base_url="https://livre.example.com")

    cookie = resp.headers.get("Set-Cookie", "")
    assert "Secure" in cookie
    assert "HttpOnly" in cookie
    assert "SameSite=Lax" in cookie


def test_hsts_is_sent_when_cookies_are_secure(behind_caddy):
    resp = behind_caddy.test_client().get("/login", base_url="https://livre.example.com")
    assert "Strict-Transport-Security" in resp.headers


def test_no_hsts_on_a_plain_lan_install(no_proxy):
    """A LAN install over HTTP must not send HSTS: a browser that caches it
    will refuse to reach the book over http:// afterwards, and there is no
    certificate for it to use instead."""
    resp = no_proxy.test_client().get("/login")
    assert "Strict-Transport-Security" not in resp.headers
