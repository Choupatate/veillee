"""FEATURES.md F56: handing a link over.

Two halves, and only one of them is testable here. The button's *markup*
— that it exists, carries the URL it shares, and ships `hidden` so a
browser without JavaScript never shows a dead control — is checked below.
The three-tier behaviour behind it (share sheet, then clipboard, then
select the text) lives in `share-link.js` and is exercised by
`tests/js/share_link_test.mjs` in a real browser, because
`navigator.share` cannot be meaningfully faked in Python.
"""

import pytest

from tests.conftest import _bootstrap_admin, _login


@pytest.fixture
def accounts_app(app_factory):
    return app_factory(ACCOUNTS_ENABLED=True)


@pytest.fixture
def accounts_client(accounts_app):
    """A client logged in as the admin the first account request creates."""
    client = accounts_app.test_client()
    _bootstrap_admin(client)
    _login(client, "papa", "hunter22")
    return client


def _share_button(html):
    """The share button's tag, or None. Crude on purpose — a parser would
    hide exactly the kind of malformed-attribute mistake this is here to
    catch."""
    if "admin__share" not in html:
        return None
    start = html.index("<button", html.index("admin__share") - 400)
    return html[start:html.index(">", start) + 1]


def test_a_new_write_link_offers_a_share_button(accounts_client):
    resp = accounts_client.post("/account/write-links", data={"label": "for grandma"})
    button = _share_button(resp.data.decode())
    assert button is not None
    assert "/w/" in button


def test_a_new_invite_offers_a_share_button(accounts_client):
    resp = accounts_client.post("/admin/accounts/invite", data={
        "new_person_name": "Mamie", "role": "family",
    })
    button = _share_button(resp.data.decode())
    assert button is not None
    assert "/invite/" in button


def test_the_button_ships_hidden(accounts_client):
    """Without JavaScript the URL is still there as selectable text. A
    visible button that cannot do anything is worse than no button."""
    resp = accounts_client.post("/account/write-links", data={"label": "x"})
    assert "hidden" in _share_button(resp.data.decode())


def test_the_button_has_no_text_of_its_own(accounts_client):
    """It says "Share" or "Copy" depending on what the browser can do, and
    share-link.js decides which. Server-rendered text would be wrong half
    the time and would flicker on the way to being corrected."""
    resp = accounts_client.post("/account/write-links", data={"label": "x"})
    html = resp.data.decode()
    start = html.index("<button", html.index("admin__share") - 400)
    end = html.index("</button>", start)
    inner = html[html.index(">", start) + 1:end]
    assert inner.strip() == ""


def test_the_url_lives_in_the_page_as_text_too(accounts_client):
    """The share button is an enhancement, not the only way out. The
    fallback tier selects the <code> element, so it has to be addressable."""
    resp = accounts_client.post("/account/write-links", data={"label": "x"})
    html = resp.data.decode()
    assert 'id="new-link-url"' in html
    assert 'data-share-source="new-link-url"' in html
