"""Who can reach F51's setup wizard and Settings — and what they can do to
a book that already exists.

This file exists because of one question: could anyone trigger the wizard
again on a book in use, and lose what is in it? The answers are all here
rather than in a reply, so they stay answers.

Two properties are load-bearing. **The wizard cannot be re-armed from
inside the app**: a book with stories in it is set up for good, and no
route in this app deletes a story. And **neither page can destroy
anything** even for the person allowed to use them: they write one small
JSON file and, at most, add one person to the cast.
"""

from datetime import date

import pytest

from app import create_app, people, settings, storage, write_links
from tests.conftest import _bootstrap_admin, _login, _request_account

BASE = {"PASSWORD": "test-password", "SECRET_KEY": "test-secret", "WTF_CSRF_ENABLED": False}


@pytest.fixture
def book_in_use(tmp_path):
    """A book someone has been writing in, with no settings file — the
    shape every install that predates F51 has on the day it upgrades."""
    d = tmp_path / "stories"
    d.mkdir()
    storage.create_story(d, "A real memory", date(2025, 3, 2), "body")
    people.create_person(storage.people_dir(d), "Milo")
    return d


def _contents(stories_dir):
    return (
        {s.id for s in storage.list_stories(stories_dir)},
        {p.slug for p in people.list_people(storage.people_dir(stories_dir))},
    )


def _app(stories_dir, **config):
    return create_app(test_config={"STORIES_DIR": stories_dir, **BASE, **config})


# --- nobody who is not logged in ---------------------------------------------


def test_a_stranger_cannot_reach_either_page(book_in_use):
    client = _app(book_in_use).test_client()
    before = _contents(book_in_use)
    for method, path in (("get", "/setup"), ("get", "/settings"),
                         ("post", "/setup"), ("post", "/settings")):
        resp = getattr(client, method)(path, data={"skip": "1", "title": "hijacked"})
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]
    assert _contents(book_in_use) == before
    assert not settings.settings_path(book_in_use).is_file()


def test_both_pages_need_the_csrf_token(book_in_use):
    app = _app(book_in_use, WTF_CSRF_ENABLED=True)
    client = app.test_client()
    client.post("/login", data={"password": "test-password"})
    for path in ("/setup", "/settings"):
        assert client.post(path, data={"title": "hijacked"}).status_code == 400


# --- nobody who is merely family ---------------------------------------------


@pytest.fixture
def accounts_book(book_in_use):
    app = _app(book_in_use, ACCOUNTS_ENABLED=True)
    admin = app.test_client()
    _bootstrap_admin(admin)
    _login(admin, "papa", "hunter22")
    member = app.test_client()
    _request_account(member, display_name="Mamie", username="mamie", password="hunter22")
    admin.post("/admin/accounts/pending/mamie",
               data={"new_person_name": "Mamie", "role": "family"})
    _login(member, "mamie", "hunter22")
    return app, admin, member


def test_a_family_member_gets_a_404_from_both_pages(accounts_book):
    _, _, member = accounts_book
    for method, path in (("get", "/setup"), ("get", "/settings"),
                         ("post", "/setup"), ("post", "/settings")):
        assert getattr(member, method)(path, data={"skip": "1"}).status_code == 404


def test_a_family_member_cannot_change_a_setting(accounts_book, book_in_use):
    _, _, member = accounts_book
    member.post("/settings", data={
        "title": "hijacked", "birthdate": "", "child": "", "authors": "",
        "language": "", "theme": "",
    })
    assert settings.read(book_in_use).get("title") != "hijacked"


def test_a_family_member_is_not_even_offered_the_link(accounts_book):
    _, admin, member = accounts_book
    assert 'href="/settings"' in admin.get("/").data.decode()
    assert 'href="/settings"' not in member.get("/").data.decode()


# --- and nobody holding a write link -----------------------------------------


def test_a_write_link_guest_cannot_reach_either_page(accounts_book, book_in_use):
    """A delegate's session is not an account session at all: it never sets
    `authed`, so `login_required` turns it away before any role is
    considered."""
    app, _, _ = accounts_book
    papa = next(p for p in people.list_people(storage.people_dir(book_in_use))
                if p.name == "Papa")
    _, token = write_links.create_link(storage.people_dir(book_in_use), papa.slug)

    guest = app.test_client()
    assert guest.get(f"/w/{token}").status_code == 302   # a real delegate session
    assert guest.get("/w/write").status_code == 200      # ...which works

    for path in ("/setup", "/settings"):
        resp = guest.get(path)
        assert resp.status_code == 302
        assert "/login" in resp.headers["Location"]
    guest.post("/settings", data={
        "title": "hijacked", "birthdate": "", "child": "", "authors": "",
        "language": "", "theme": "",
    })
    assert settings.read(book_in_use).get("title") != "hijacked"


# --- the wizard cannot be re-armed -------------------------------------------


def test_a_book_with_stories_never_shows_the_wizard_again(book_in_use):
    client = _app(book_in_use).test_client()
    client.post("/login", data={"password": "test-password"})
    assert client.get("/", follow_redirects=False).status_code == 200
    resp = client.post("/setup", data={"skip": "1"})
    assert resp.headers["Location"].endswith("/settings")
    assert not settings.settings_path(book_in_use).is_file()


def test_losing_the_settings_file_does_not_re_arm_it(book_in_use):
    """The file is a flag, not the only flag — the stories are the other
    one, which is what makes this safe against a lost or truncated file."""
    settings.save(book_in_use, {"title": "Milo's book"})
    settings.settings_path(book_in_use).unlink()
    assert settings.is_configured(book_in_use)
    client = _app(book_in_use).test_client()
    client.post("/login", data={"password": "test-password"})
    assert client.get("/", follow_redirects=False).status_code == 200


def test_no_route_in_this_app_can_empty_a_book(book_in_use):
    """The property the one above rests on: you cannot get back to an
    empty book from inside the app, so you cannot get back to the wizard.
    Stories are never deleted here — the deliberate omission from F12's
    'the one deletion this app supports'."""
    app = _app(book_in_use)
    deleting = [
        str(rule) for rule in app.url_map.iter_rules()
        if "DELETE" in rule.methods or "delete" in str(rule)
    ]
    assert sorted(deleting) == [
        "/api/stories/<story_id>/memos/<filename>",   # F12: a pocket recording
        "/themes/<theme>/delete",                     # F50: a theme someone made
    ]


def test_archiving_everything_does_not_empty_the_book(book_in_use):
    """Archived stories are still stories on disk; the closest thing to
    emptying a book from the interface leaves it set up."""
    for story in storage.list_stories(book_in_use):
        storage.save_story(book_in_use, story.id, story.title, story.date,
                           story.body or "", archived=True)
    assert settings.is_configured(book_in_use)


# --- what the pages can do at their very worst -------------------------------


def test_the_wizard_never_touches_a_story_or_a_photo(tmp_path):
    d = tmp_path / "stories"
    d.mkdir()
    client = _app(d).test_client()
    client.post("/login", data={"password": "test-password"})
    client.post("/setup", data={
        "title": "Milo's book", "child_name": "Milo", "birthdate": "2023-06-18",
        "authors": "", "language": "", "theme": "",
    })
    # One person added, by request. Nothing removed, nothing else written.
    assert {p.name for p in people.list_people(storage.people_dir(d))} == {"Milo"}
    assert sorted(p.name for p in d.iterdir()) == ["people", "settings.json"]


def test_the_worst_an_admin_can_do_is_undo_by_typing_it_again(book_in_use):
    """Settings are settings: clearing them changes what is shown, never
    what is stored. The stories are untouched either way."""
    client = _app(book_in_use).test_client()
    client.post("/login", data={"password": "test-password"})
    before = _contents(book_in_use)
    client.post("/settings", data={
        "title": "", "birthdate": "", "child": "", "authors": "",
        "language": "", "theme": "",
    })
    assert _contents(book_in_use) == before
    client.post("/settings", data={
        "title": "Milo's book", "birthdate": "2023-06-18", "child": "",
        "authors": "", "language": "", "theme": "",
    })
    assert settings.read(book_in_use)["title"] == "Milo's book"
    assert _contents(book_in_use) == before
