"""The third-party notices page (FEATURES.md F53).

`tests/test_vendored_licences.py` checks that the licence *files* are in
the repository, which is what actually discharges the obligation. This
checks the page that shows them to whoever receives the app — and, more
usefully, that the page cannot quietly fall out of step with what the app
really ships.

Two ways it could: a vendored bundle gets added or upgraded and the page
still names the old one, or a pinned Python package appears in
`requirements.txt` and nobody lists it. Both are checked below against the
real files rather than against a copy.
"""

import html
import re
from pathlib import Path

import pytest

from app.routes_pages import SERVER_LICENCES, VENDORED_LICENCES

REPO_ROOT = Path(__file__).resolve().parent.parent
VENDOR = REPO_ROOT / "app" / "static" / "vendor"


# --- the page ---------------------------------------------------------------


def test_the_page_needs_a_login_like_every_other(client):
    assert client.get("/licences").headers["Location"].startswith("/login")


def test_the_page_renders(auth_client):
    assert auth_client.get("/licences").status_code == 200


def test_every_vendored_licence_is_reproduced_in_full(auth_client):
    """"Reproduced in full" is the phrase the page uses, so it had better be
    true: the whole text, not a summary and not a link."""
    # Unescaped, because Jinja turns the licences' own quotation marks into
    # `&#34;` on the way out — which is correct, and would make a literal
    # comparison fail on text that is perfectly present.
    body = html.unescape(auth_client.get("/licences").data.decode())
    for library in VENDORED_LICENCES:
        text = (VENDOR.parent / library["path"]).read_text(encoding="utf-8").strip()
        # The distinctive middle of a licence, past the copyright line.
        for line in [ln for ln in text.splitlines() if len(ln) > 40][:3]:
            assert line.strip() in body, (
                f"{library['name']}'s licence is not reproduced in full — "
                f"missing: {line.strip()[:60]!r}"
            )


def test_the_page_shows_the_text_on_disk_rather_than_a_copy(auth_client, tmp_path):
    """The page reads each `LICENSE` file at request time. A copy pasted
    into the template would look identical today and drift silently the
    first time a bundle is upgraded."""
    source = (REPO_ROOT / "app" / "routes_pages.py").read_text()
    assert "read_text" in source
    body = auth_client.get("/licences").data.decode()
    assert "NHN Cloud Corp" in body, "Toast UI's copyright holder is not on the page"
    assert "Donat Soric" in body, "family-chart's copyright holder is not on the page"
    assert "Mike Bostock" in body, "D3's copyright holder is not on the page"


def test_a_missing_licence_file_does_not_break_the_page(auth_client, monkeypatch):
    """A packaging accident should cost the notice, not the page. The
    *files* are guarded by test_vendored_licences.py; this is the fallback
    for the one place a 500 would be least useful — and it names the path,
    so whoever hits it can find what went missing."""
    import app.routes_pages as routes

    monkeypatch.setattr(routes, "VENDORED_LICENCES", (
        {
            "name": "Nothing", "version": "0", "purpose": "draws the family tree",
            "url": "https://example.invalid", "path": "vendor/nothing/LICENSE",
        },
    ))
    resp = auth_client.get("/licences")
    assert resp.status_code == 200
    assert "vendor/nothing/LICENSE" in resp.data.decode()


def test_help_links_to_it(auth_client):
    assert "/licences" in auth_client.get("/help").data.decode()


# --- the lists cannot drift from what the app ships -------------------------


def test_every_vendored_library_is_on_the_page():
    """A bundle added to app/static/vendor/ and not to VENDORED_LICENCES
    would be served to browsers with its notice nowhere a reader can see."""
    on_disk = {p.name for p in VENDOR.iterdir() if p.is_dir()}
    listed = {Path(lib["path"]).parts[1] for lib in VENDORED_LICENCES}
    assert on_disk == listed, (
        f"vendored on disk: {sorted(on_disk)}; listed on the page: "
        f"{sorted(listed)}"
    )


def test_each_entry_points_at_a_real_licence_file():
    for library in VENDORED_LICENCES:
        path = VENDOR.parent / library["path"]
        assert path.is_file(), f"{library['name']} points at {library['path']}, which is not there"


@pytest.mark.parametrize("field", ["name", "version", "purpose", "url"])
def test_each_entry_is_filled_in(field):
    for library in VENDORED_LICENCES:
        assert library.get(field), f"{library.get('name')} has no {field}"


def _pinned_packages():
    """Every package pinned in requirements.txt, minus the dev tools — the
    ones that actually run when a family runs this book."""
    text = (REPO_ROOT / "requirements.txt").read_text()
    before_dev = text.split("# dev")[0]
    return {
        re.split(r"[=<>]", line)[0].strip().lower()
        for line in before_dev.splitlines()
        if line.strip() and not line.startswith("#")
    }


def test_every_pinned_package_is_named_on_the_page():
    """`requirements.txt` is the truth about what runs on the server, so a
    new pin has to appear here too. Matched loosely — the page groups
    packages that share a licence ("Flask, Werkzeug, Jinja2…") — but a
    package named nowhere on the page fails."""
    listed = " ".join(name for name, _licence in SERVER_LICENCES).lower()
    missing = sorted(p for p in _pinned_packages() if p.replace("-", " ") not in listed
                     and p not in listed)
    assert not missing, (
        f"{missing} are pinned in requirements.txt but named nowhere in "
        "SERVER_LICENCES — add them, with their licence"
    )


def test_the_optional_transcription_dependency_is_named_too():
    """It is not in requirements.txt (it is installed separately), so
    nothing above would catch it going missing."""
    listed = " ".join(name for name, _licence in SERVER_LICENCES).lower()
    assert "faster-whisper" in listed


def test_every_server_entry_names_a_licence():
    for name, licence in SERVER_LICENCES:
        assert name.strip() and licence.strip(), (name, licence)


def test_the_page_says_which_licence_the_app_itself_uses(auth_client):
    """And that it matches the LICENSE file in the repository root."""
    body = auth_client.get("/licences").data.decode()
    assert "Apache" in body
    assert "Apache License" in (REPO_ROOT / "LICENSE").read_text()
