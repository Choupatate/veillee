"""Tests for the /licences page (F35).

The point of the page is compliance, so the tests check the thing that would
actually break compliance: that the notices rendered are the ones really
shipped in `app/static/vendor/`, not a copy that has drifted from them.
"""

from pathlib import Path

import pytest

VENDOR_LICENCE_FILES = [
    "vendor/toastui/LICENSE",
    "vendor/familychart/LICENSE",
    "vendor/d3/LICENSE",
]


def _static_dir(app):
    return Path(app.static_folder)


def test_licences_page_requires_login(client):
    resp = client.get("/licences")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_licences_page_renders(auth_client):
    resp = auth_client.get("/licences")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Licences" in body
    assert "Apache License 2.0" in body


@pytest.mark.parametrize("name", ["Toast UI Editor", "family-chart", "D3"])
def test_every_vendored_library_is_named(auth_client, name):
    body = auth_client.get("/licences").get_data(as_text=True)
    assert name in body


def test_page_reproduces_the_real_licence_files(app, auth_client):
    """Each vendored licence must appear on the page as it is on disk.

    Substantive line-by-line rather than a token check: this is the assertion
    that fails if someone edits the page text, or upgrades a vendored bundle
    and forgets its licence changed.
    """
    body = auth_client.get("/licences").get_data(as_text=True)
    for rel in VENDOR_LICENCE_FILES:
        text = (_static_dir(app) / rel).read_text(encoding="utf-8").strip()
        assert text, f"{rel} is empty"
        for line in text.splitlines():
            line = line.strip()
            if len(line) < 20:
                continue
            # The template escapes nothing else in these files, but quotes in
            # "AS IS" become &#34; once Jinja autoescapes them.
            assert line.replace('"', "&#34;") in body, f"{rel}: missing {line!r}"


def test_copyright_holders_are_present(auth_client):
    body = auth_client.get("/licences").get_data(as_text=True)
    for holder in ["NHN Cloud Corp.", "Donat Soric", "Mike Bostock"]:
        assert holder in body


def test_server_side_packages_are_listed(auth_client):
    body = auth_client.get("/licences").get_data(as_text=True)
    assert "Flask" in body
    assert "ZPL 2.1" in body
    assert "MIT-CMU" in body


def test_missing_licence_file_does_not_break_the_page(app, auth_client, monkeypatch):
    """A packaging slip should degrade to a pointer, not a 500."""
    from app import routes_pages

    app.extensions.pop("vendored_licences", None)
    monkeypatch.setattr(routes_pages, "_VENDORED_LICENCES", (
        {
            "name": "Nonexistent",
            "version": "0.0.0",
            "purpose": "test",
            "url": "https://example.invalid",
            "path": "vendor/nope/LICENSE",
        },
    ))
    resp = auth_client.get("/licences")
    assert resp.status_code == 200
    assert "Licence text unavailable" in resp.get_data(as_text=True)


def test_help_page_links_to_licences(auth_client):
    body = auth_client.get("/help").get_data(as_text=True)
    assert "/licences" in body


def test_served_css_carries_a_copyright_banner(app):
    """The two vendored CSS files upstream ships without a banner must keep the
    one added locally — they are served to browsers, so the notice has to be in
    the copy that goes out."""
    for rel, holder in [
        ("vendor/familychart/family-chart.css", "Donat Soric"),
        ("vendor/toastui/theme/toastui-editor-dark.css", "NHN Cloud Corp."),
    ]:
        head = (_static_dir(app) / rel).read_text(encoding="utf-8")[:600]
        assert "Copyright" in head, f"{rel} lost its banner"
        assert holder in head, f"{rel} banner lost its copyright holder"


def test_minified_bundles_keep_their_upstream_banners(app):
    """Same requirement for the bundles that already shipped with a banner."""
    for rel, holder in [
        ("vendor/d3/d3.min.js", "Mike Bostock"),
        ("vendor/familychart/family-chart.min.js", "donatso"),
        ("vendor/toastui/toastui-editor-all.min.js", "NHN Cloud"),
        ("vendor/toastui/toastui-editor.min.css", "NHN Cloud"),
    ]:
        head = (_static_dir(app) / rel).read_text(encoding="utf-8", errors="replace")[:600]
        assert holder in head, f"{rel} lost its upstream banner"
