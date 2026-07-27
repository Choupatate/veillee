"""Tests for FEATURES.md F40 Phase 1: audience groups.

Three layers, and the middle one is the point of the file: the pure rule
(`groups.can_see`), then the leak perimeter — a scoped story must be
invisible from *every* route that reaches a story, walked mechanically so
a new route can't quietly skip the gate — then the group-management
screens.
"""

from datetime import date

import pytest

from app import accounts, groups, people, storage
from tests.conftest import _bootstrap_admin, _login, _people_dir


# ---------------------------------------------------------------------------
# The rule itself — pure, no Flask


def test_a_story_with_no_audience_is_for_everyone(make_story):
    story = make_story("s", date(2026, 1, 1))
    assert groups.can_see(story, set())


def test_a_scoped_story_needs_membership(make_story):
    story = make_story("s", date(2026, 1, 1), audience=["just-us"])
    assert groups.can_see(story, {"just-us"})
    assert not groups.can_see(story, {"godparents"})
    assert not groups.can_see(story, set())


def test_membership_of_any_listed_group_is_enough(make_story):
    """Union, not intersection — "close family and the godparents"."""
    story = make_story("s", date(2026, 1, 1), audience=["just-us", "godparents"])
    assert groups.can_see(story, {"godparents"})


def test_the_author_always_sees_their_own_story(make_story):
    """A mis-tap in the editor must not make a story vanish from the
    person who wrote it."""
    story = make_story("s", date(2026, 1, 1), audience=["just-us"], author="Papa")
    assert groups.can_see(story, set(), viewer_author_name="Papa")
    assert not groups.can_see(story, set(), viewer_author_name="Mamie")


def test_visible_stories_preserves_order(make_story):
    a = make_story("a", date(2026, 1, 1))
    b = make_story("b", date(2026, 1, 2), audience=["just-us"])
    c = make_story("c", date(2026, 1, 3))
    assert [s.id for s in groups.visible_stories([a, b, c], set())] == ["a", "c"]


# ---------------------------------------------------------------------------
# Storage round-trip


def test_audience_survives_a_save(stories_dir):
    story_id = storage.create_story(
        stories_dir, "Scoped", date(2026, 1, 1), "body", audience=["just-us"]
    )
    assert storage.get_story(stories_dir, story_id).audience == ["just-us"]


def test_audience_is_carried_over_when_a_save_omits_it(stories_dir):
    story_id = storage.create_story(
        stories_dir, "Scoped", date(2026, 1, 1), "body", audience=["just-us"]
    )
    storage.save_story(stories_dir, story_id, "Scoped", date(2026, 1, 1), "new body")
    assert storage.get_story(stories_dir, story_id).audience == ["just-us"]


def test_audience_can_be_cleared(stories_dir):
    story_id = storage.create_story(
        stories_dir, "Scoped", date(2026, 1, 1), "body", audience=["just-us"]
    )
    storage.save_story(stories_dir, story_id, "Scoped", date(2026, 1, 1), "b", audience=[])
    assert storage.get_story(stories_dir, story_id).audience == []


def test_restoring_an_old_version_keeps_the_current_audience(stories_dir):
    """The trap F40's spec called out. Restoring is about getting old
    *words* back; pulling up a version from before a story was scoped must
    not quietly republish it to the whole family."""
    story_id = storage.create_story(stories_dir, "Open", date(2026, 1, 1), "first")
    storage.save_story(
        stories_dir, story_id, "Now scoped", date(2026, 1, 1), "second", audience=["just-us"]
    )
    version_id = storage.list_versions(stories_dir, story_id)[0]["id"]

    storage.restore_version(stories_dir, story_id, version_id)

    restored = storage.get_story(stories_dir, story_id)
    assert restored.body.strip() == "first"      # the words came back
    assert restored.audience == ["just-us"]      # the audience did not move


def test_a_malformed_audience_key_is_ignored_not_fatal(stories_dir):
    story_id = storage.create_story(stories_dir, "Odd", date(2026, 1, 1), "body")
    path = stories_dir / story_id / "index.md"
    path.write_text(path.read_text().replace("title:", "audience: 17\ntitle:", 1))
    assert storage.get_story(stories_dir, story_id).audience == []


# ---------------------------------------------------------------------------
# The leak perimeter


@pytest.fixture
def scoped_app(app_factory):
    """A book with one public story, one scoped to "just us", an admin who
    is NOT in that group, and a family member who is."""
    app = app_factory(ACCOUNTS_ENABLED=True)
    stories_dir = app.config["STORIES_DIR"]
    people_dir = storage.people_dir(stories_dir)
    people_dir.mkdir(parents=True, exist_ok=True)

    admin_slug = people.create_person(people_dir, "Papa")
    member_slug = people.create_person(people_dir, "Maman")
    accounts.create_account(people_dir, admin_slug, "papa", "hunter22", "admin")
    accounts.create_account(people_dir, member_slug, "maman", "hunter22", "family")

    groups.create_group(stories_dir, "Just us", members=[member_slug])

    app.config["PUBLIC_ID"] = storage.create_story(
        stories_dir, "A day out", date(2026, 1, 1), "public body", author="Papa"
    )
    app.config["SCOPED_ID"] = storage.create_story(
        stories_dir, "The secret", date(2026, 2, 1), "scoped body",
        author="Maman", audience=["just-us"], milestone="First word",
    )
    return app


@pytest.fixture
def outsider(scoped_app):
    """The admin, who is deliberately not in the group — F40's values call
    is that managing groups grants no reading privilege."""
    client = scoped_app.test_client()
    _login(client, "papa", "hunter22")
    return client


@pytest.fixture
def insider(scoped_app):
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")
    return client


# Every page that lists or renders stories without naming one in its URL.
# A scoped story's title must appear on none of them for an outsider.
LISTING_URLS = ("/", "/book", "/firsts", "/growth", "/drafts", "/archived", "/people/maman")


def test_no_listing_page_leaks_a_scoped_title(outsider, scoped_app):
    """The whole feature in one test: walk every surface that renders the
    story list and assert the scoped story's title appears on none of
    them, while the public one still does."""
    for url in LISTING_URLS:
        html = outsider.get(url).data.decode()
        assert "The secret" not in html, f"{url} leaked the scoped title"
    assert "A day out" in outsider.get("/").data.decode()


def test_no_listing_page_leaks_a_scoped_story_body(outsider, scoped_app):
    """/book renders full bodies, not just titles — a separate failure
    mode from the title leak above."""
    assert "scoped body" not in outsider.get("/book").data.decode()
    assert "public body" in outsider.get("/book").data.decode()


def test_the_epub_leaves_a_scoped_story_out(outsider, scoped_app):
    assert b"The secret" not in outsider.get("/book.epub").data


def test_scoped_story_urls_404_for_an_outsider(outsider, scoped_app):
    scoped = scoped_app.config["SCOPED_ID"]
    for url in (
        f"/story/{scoped}",
        f"/edit/{scoped}",
        f"/story/{scoped}/history",
        f"/story/{scoped}/media/photo-001.jpg",
    ):
        assert outsider.get(url).status_code == 404, url


def test_an_insider_sees_the_scoped_story_everywhere(insider, scoped_app):
    scoped = scoped_app.config["SCOPED_ID"]
    assert "The secret" in insider.get("/").data.decode()
    assert insider.get(f"/story/{scoped}").status_code == 200
    assert insider.get(f"/edit/{scoped}").status_code == 200
    assert "The secret" in insider.get("/book").data.decode()
    assert "The secret" in insider.get("/firsts").data.decode()


def test_the_public_story_is_unaffected(outsider, scoped_app):
    public = scoped_app.config["PUBLIC_ID"]
    assert outsider.get(f"/story/{public}").status_code == 200
    assert "A day out" in outsider.get("/").data.decode()


def test_random_never_lands_on_a_scoped_story(outsider, scoped_app):
    scoped = scoped_app.config["SCOPED_ID"]
    for _ in range(15):
        resp = outsider.get("/random")
        assert scoped not in resp.headers.get("Location", "")


def test_reading_order_skips_a_scoped_story(outsider, scoped_app):
    """Page-turn arrows must not hand out a scoped story's id."""
    public = scoped_app.config["PUBLIC_ID"]
    scoped = scoped_app.config["SCOPED_ID"]
    assert scoped not in outsider.get(f"/story/{public}").data.decode()


def test_an_outsider_cannot_write_to_a_scoped_story(outsider, scoped_app):
    scoped = scoped_app.config["SCOPED_ID"]
    resp = outsider.put(
        f"/api/stories/{scoped}",
        json={"title": "Overwritten", "date": "2026-02-01", "markdown": "gotcha"},
    )
    assert resp.status_code == 404
    stories_dir = scoped_app.config["STORIES_DIR"]
    assert storage.get_story(stories_dir, scoped).title == "The secret"


def test_an_outsider_cannot_reach_the_other_mutating_endpoints(outsider, scoped_app):
    scoped = scoped_app.config["SCOPED_ID"]
    assert outsider.post(f"/api/stories/{scoped}/images").status_code == 404
    assert outsider.post(f"/api/stories/{scoped}/memos").status_code == 404
    assert outsider.delete(f"/api/stories/{scoped}/memos/memo-001.webm").status_code == 404
    assert outsider.post(
        f"/api/stories/{scoped}/versions/20260101T000000000000/restore"
    ).status_code == 404


def test_an_outsiders_export_leaves_the_scoped_story_out(outsider, scoped_app):
    import io
    import zipfile

    data = outsider.get("/export").data
    names = zipfile.ZipFile(io.BytesIO(data)).namelist()
    scoped, public = scoped_app.config["SCOPED_ID"], scoped_app.config["PUBLIC_ID"]
    assert any(n.startswith(f"{public}/") for n in names)
    assert not any(n.startswith(f"{scoped}/") for n in names)
    # people/ and groups.json aren't stories and are never audience-scoped.
    assert any(n.startswith("people/") for n in names)


def test_an_insiders_export_is_complete(insider, scoped_app):
    import io
    import zipfile

    names = zipfile.ZipFile(io.BytesIO(insider.get("/export").data)).namelist()
    assert any(n.startswith(f"{scoped_app.config['SCOPED_ID']}/") for n in names)


def test_the_import_page_warns_about_a_partial_backup(outsider):
    assert "leaves them out" in outsider.get("/import").data.decode()


def test_import_is_admin_only_in_accounts_mode(insider):
    assert insider.get("/import").status_code == 404
    assert insider.post("/api/import").status_code == 404


def test_the_author_still_sees_a_story_they_scoped_away_from_themselves(scoped_app):
    """Maman wrote the scoped story and is in the group; make a third
    story she scoped to a group she is *not* in and check it still
    reaches her."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Godparents", members=[])
    oops = storage.create_story(
        stories_dir, "Mis-scoped", date(2026, 3, 1), "body",
        author="Maman", audience=["godparents"],
    )
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")
    assert client.get(f"/story/{oops}").status_code == 200


# --- the guard that keeps the perimeter honest ------------------------------


ROUTE_FILES = ("routes_pages.py", "routes_people.py", "routes_groups.py")


def test_no_page_route_reaches_the_story_list_directly():
    """`_visible_stories()` is the only sanctioned way into the story list
    from a page route. A new route calling `storage.list_stories` straight
    is how a scoped story leaks, so this fails the day one does.

    `routes_pages.py` gets one sanctioned use — inside `_visible_stories`
    itself — plus the two group-count helpers in `routes_groups.py`, which
    count stories per group for an admin screen and deliberately never
    render a title or body.
    """
    from pathlib import Path

    app_dir = Path(__file__).resolve().parent.parent / "app"
    allowed = {"routes_pages.py": 3, "routes_groups.py": 2, "routes_people.py": 0}
    for filename in ROUTE_FILES:
        text = (app_dir / filename).read_text()
        count = text.count("storage.list_stories(")
        assert count <= allowed[filename], (
            f"{filename} calls storage.list_stories {count} times; page routes "
            "must go through _visible_stories() so audience scoping applies"
        )


def test_accounts_mode_off_means_no_scoping_at_all(auth_client, stories_dir):
    """One shared password is one identity — there is nobody to scope a
    story away from, so an `audience` key must not hide anything."""
    story_id = storage.create_story(
        stories_dir, "Scoped", date(2026, 1, 1), "body", audience=["just-us"]
    )
    assert auth_client.get(f"/story/{story_id}").status_code == 200
    assert "Scoped" in auth_client.get("/").data.decode()


def test_the_groups_pages_do_not_exist_without_accounts(auth_client):
    assert auth_client.get("/admin/groups").status_code == 404


# ---------------------------------------------------------------------------
# Group management


@pytest.fixture
def admin_client(app_factory):
    app = app_factory(ACCOUNTS_ENABLED=True)
    client = app.test_client()
    _bootstrap_admin(client)
    _login(client, "papa", "hunter22")
    return client


def test_admin_creates_a_group(admin_client):
    resp = admin_client.post("/admin/groups", data={"name": "Just us"})
    assert resp.status_code == 302
    stories_dir = admin_client.application.config["STORIES_DIR"]
    assert [g.slug for g in groups.list_groups(stories_dir)] == ["just-us"]


def test_a_duplicate_group_name_is_refused(admin_client):
    admin_client.post("/admin/groups", data={"name": "Just us"})
    resp = admin_client.post("/admin/groups", data={"name": "Just us"}, follow_redirects=True)
    assert "already a group" in resp.data.decode()


def test_a_blank_group_name_is_refused(admin_client):
    resp = admin_client.post("/admin/groups", data={"name": "  "})
    assert "Give the group a name." in resp.data.decode()
    assert groups.list_groups(admin_client.application.config["STORIES_DIR"]) == []


def test_admin_sets_membership(admin_client):
    stories_dir = admin_client.application.config["STORIES_DIR"]
    slug = people.create_person(_people_dir(admin_client.application), "Mamie Rose")
    groups.create_group(stories_dir, "Just us")

    admin_client.post("/admin/groups/just-us", data={"name": "Just us", "members": [slug]})
    assert groups.get_group(stories_dir, "just-us").members == [slug]


def test_membership_rejects_an_unknown_person(admin_client):
    stories_dir = admin_client.application.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Just us")
    resp = admin_client.post(
        "/admin/groups/just-us", data={"name": "Just us", "members": ["nobody"]}
    )
    assert "Unknown person" in resp.data.decode()
    assert groups.get_group(stories_dir, "just-us").members == []


def test_renaming_keeps_the_slug(admin_client):
    """Stories reference a group by slug; a rename that changed it would
    silently un-scope every story pointing at the old one."""
    stories_dir = admin_client.application.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Just us")
    admin_client.post("/admin/groups/just-us", data={"name": "The four of us"})
    group = groups.get_group(stories_dir, "just-us")
    assert group.name == "The four of us"
    assert group.slug == "just-us"


def test_groups_pages_are_admin_only(scoped_app):
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")   # family, not admin
    assert client.get("/admin/groups").status_code == 404
    assert client.get("/admin/groups/just-us").status_code == 404


def test_unknown_group_404s(admin_client):
    assert admin_client.get("/admin/groups/nope").status_code == 404


def test_the_api_refuses_an_unknown_group(admin_client):
    """Silently dropping an unknown slug would turn a story the writer
    believed was scoped into a public one."""
    resp = admin_client.post(
        "/api/stories",
        json={"title": "T", "date": "2026-01-01", "markdown": "b", "audience": ["nope"]},
    )
    assert resp.status_code == 400
    assert "Unknown group" in resp.get_json()["error"]


# ---------------------------------------------------------------------------
# Phase 2: the audience picker and the "who can see this" markers


def test_the_editor_offers_every_group(insider, scoped_app):
    html = insider.get("/new").data.decode()
    assert 'data-group-slug="just-us"' in html
    assert "Who can see this" in html


def _chip_pressed(html, slug):
    """Whether the audience chip for `slug` is lit, read out of the markup
    rather than inferred from "some chip somewhere is pressed"."""
    import re

    match = re.search(
        r'data-group-slug="' + re.escape(slug) + r'"[^>]*aria-pressed="(\w+)"', html
    )
    assert match, f"no audience chip rendered for {slug}"
    return match.group(1) == "true"


def test_the_editor_preselects_a_scoped_storys_groups(insider, scoped_app):
    html = insider.get(f"/edit/{scoped_app.config['SCOPED_ID']}").data.decode()
    assert _chip_pressed(html, "just-us")


def test_the_editor_leaves_chips_unlit_for_a_public_story(insider, scoped_app):
    html = insider.get(f"/edit/{scoped_app.config['PUBLIC_ID']}").data.decode()
    assert not _chip_pressed(html, "just-us")


def test_the_instant_composer_offers_groups_too(insider):
    """The original ask was "stories or instants" — an instant you can't
    scope would be a hole you'd only find after posting one."""
    html = insider.get("/new-instant").data.decode()
    assert 'data-group-slug="just-us"' in html


def test_no_picker_without_accounts(auth_client):
    assert "Who can see this" not in auth_client.get("/new").data.decode()
    assert "Who can see this" not in auth_client.get("/new-instant").data.decode()


def test_no_picker_when_no_groups_exist(app_factory):
    app = app_factory(ACCOUNTS_ENABLED=True)
    client = app.test_client()
    _bootstrap_admin(client)
    _login(client, "papa", "hunter22")
    assert "Who can see this" not in client.get("/new").data.decode()


def test_the_story_page_says_who_it_is_kept_to(insider, scoped_app):
    html = insider.get(f"/story/{scoped_app.config['SCOPED_ID']}").data.decode()
    assert "Kept to Just us" in html


def test_a_public_story_says_nothing_about_audience(insider, scoped_app):
    html = insider.get(f"/story/{scoped_app.config['PUBLIC_ID']}").data.decode()
    assert "Kept to" not in html


def test_the_timeline_marks_a_scoped_story(insider):
    assert "kept to a group" in insider.get("/").data.decode()


def test_the_timeline_does_not_mark_anything_for_an_outsider(outsider):
    """An outsider can't see the scoped story at all, so there is nothing
    to mark — the pill must not leak its existence either."""
    assert "kept to a group" not in outsider.get("/").data.decode()


def test_the_api_accepts_a_real_group(admin_client):
    stories_dir = admin_client.application.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Just us")
    resp = admin_client.post(
        "/api/stories",
        json={"title": "T", "date": "2026-01-01", "markdown": "b", "audience": ["just-us"]},
    )
    assert resp.status_code == 200
    story_id = resp.get_json()["id"]
    assert storage.get_story(stories_dir, story_id).audience == ["just-us"]
