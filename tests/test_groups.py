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


ROUTE_FILES = (
    "routes_pages.py", "routes_people.py", "routes_groups.py",
    "routes_accounts.py", "routes_api.py", "routes_api_people.py",
)

# Anything in storage.py that hands back stories without a viewer in hand.
# A route calling one of these bypasses audience scoping entirely, which is
# how a scoped story leaks — so they're counted, not merely discouraged.
UNSCOPED_ENTRY_POINTS = ("storage.list_stories(", "storage.get_story(")

# The sanctioned exceptions, each with a reason:
#   routes_pages   — inside _visible_stories/_get_story_or_404/_exportable_story_ids
#                    and _export_is_scoped (the gate itself), plus book/book_epub
#                    re-reading a story already filtered to visible ones.
#   routes_groups  — two per-group story counts on an admin screen; they
#                    count, and never render a title or body.
#   routes_api     — inside _readable_story_or_error (the gate itself).
ALLOWED_UNSCOPED = {
    "routes_pages.py": 6,
    "routes_groups.py": 2,
    "routes_api.py": 1,
    "routes_people.py": 0,
    "routes_accounts.py": 0,
    "routes_api_people.py": 0,
}


def test_no_route_file_reaches_stories_unscoped():
    """`_visible_stories()` / `_get_story_or_404()` / `_readable_story_or_error()`
    are the only sanctioned ways into a story from a route. This counts the
    unscoped alternatives per file and fails when one appears, so a new route
    that forgets the gate is caught the day it's written rather than the day
    someone notices a private story on a relative's screen.

    If a legitimate new use lands here, raise the count *and* extend the
    comment above with why — the number is a ratchet, not a formality.
    """
    from pathlib import Path

    app_dir = Path(__file__).resolve().parent.parent / "app"
    for filename in ROUTE_FILES:
        text = (app_dir / filename).read_text()
        count = sum(text.count(entry) for entry in UNSCOPED_ENTRY_POINTS)
        assert count <= ALLOWED_UNSCOPED[filename], (
            f"{filename} reaches stories unscoped {count} times (allowed "
            f"{ALLOWED_UNSCOPED[filename]}); routes must go through the "
            "audience gate so scoping applies"
        )


def test_storage_exposes_no_unscoped_story_finder():
    """`stories_featuring` and `readable_page_stories` were removed when
    F40 landed: both read every story straight off disk, both had no
    caller left, and both looked exactly like the helper a future person
    page or page-turn feature would reach for. Keeping a convenient
    unscoped finder around is how the gate gets walked past.
    """
    assert not hasattr(storage, "stories_featuring")
    assert not hasattr(storage, "readable_page_stories")


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


def test_a_story_naming_a_missing_group_stays_private(make_story):
    """Restore a backup into a fresh book and the stories come back while
    groups.json doesn't. That must fail private, not public."""
    story = make_story("s", date(2026, 1, 1), audience=["gone"])
    assert not groups.can_see(story, set())
    assert not groups.can_see(story, {"just-us"})


def test_the_editor_round_trips_a_missing_groups_slug(scoped_app):
    """The silent un-scoping this feature is most likely to suffer: the
    picker shows nothing lit for an orphaned slug, an ordinary save sends
    an empty audience, and a private story quietly goes public."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    orphan = storage.create_story(
        stories_dir, "Restored", date(2026, 4, 1), "body",
        author="Maman", audience=["gone"],
    )
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")

    html = client.get(f"/edit/{orphan}").data.decode()
    assert _chip_pressed(html, "gone"), "orphaned slug must render as a lit chip"

    # And saving it back must be accepted rather than 400ing on the slug.
    resp = client.put(
        f"/api/stories/{orphan}",
        json={"title": "Restored", "date": "2026-04-01", "markdown": "body",
              "audience": ["gone"]},
    )
    assert resp.status_code == 200
    assert storage.get_story(stories_dir, orphan).audience == ["gone"]


def test_an_unknown_group_is_still_refused_when_it_is_new(scoped_app):
    """Preserving an orphaned slug must not become a way to invent one."""
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")
    resp = client.put(
        f"/api/stories/{scoped_app.config['PUBLIC_ID']}",
        json={"title": "A day out", "date": "2026-01-01", "markdown": "b",
              "audience": ["invented"]},
    )
    assert resp.status_code == 400


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
    resp = admin_client.post("/groups", data={"name": "Just us"})
    assert resp.status_code == 302
    stories_dir = admin_client.application.config["STORIES_DIR"]
    assert [g.slug for g in groups.list_groups(stories_dir)] == ["just-us"]


def test_a_duplicate_group_name_is_refused(admin_client):
    admin_client.post("/groups", data={"name": "Just us"})
    resp = admin_client.post("/groups", data={"name": "Just us"}, follow_redirects=True)
    assert "already a group" in resp.data.decode()


def test_a_blank_group_name_is_refused(admin_client):
    resp = admin_client.post("/groups", data={"name": "  "})
    assert "Give the group a name." in resp.data.decode()
    assert groups.list_groups(admin_client.application.config["STORIES_DIR"]) == []


def test_admin_sets_membership(admin_client):
    stories_dir = admin_client.application.config["STORIES_DIR"]
    slug = people.create_person(_people_dir(admin_client.application), "Mamie Rose")
    groups.create_group(stories_dir, "Just us")

    admin_client.post("/groups/just-us", data={"name": "Just us", "members": [slug]})
    assert groups.get_group(stories_dir, "just-us").members == [slug]


def test_membership_rejects_an_unknown_person(admin_client):
    stories_dir = admin_client.application.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Just us")
    resp = admin_client.post(
        "/groups/just-us", data={"name": "Just us", "members": ["nobody"]}
    )
    assert "Unknown person" in resp.data.decode()
    assert groups.get_group(stories_dir, "just-us").members == []


def test_renaming_keeps_the_slug(admin_client):
    """Stories reference a group by slug; a rename that changed it would
    silently un-scope every story pointing at the old one."""
    stories_dir = admin_client.application.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Just us")
    admin_client.post("/groups/just-us", data={"name": "The four of us"})
    group = groups.get_group(stories_dir, "just-us")
    assert group.name == "The four of us"
    assert group.slug == "just-us"


def test_the_groups_pages_need_a_login(scoped_app):
    client = scoped_app.test_client()
    assert client.get("/groups").status_code == 302
    assert client.get("/groups/just-us").status_code == 302


def test_unknown_group_404s(admin_client):
    assert admin_client.get("/groups/nope").status_code == 404


# ---------------------------------------------------------------------------
# F41: anyone can make a group; the people in it are the ones who change it


@pytest.fixture
def outsider_client(scoped_app):
    """A family account belonging to no group at all — the viewer every
    permission rule here has to hold against."""
    people_dir = storage.people_dir(scoped_app.config["STORIES_DIR"])
    slug = people.create_person(people_dir, "Mamie Rose")
    accounts.create_account(people_dir, slug, "mamie", "hunter22", "family")
    client = scoped_app.test_client()
    _login(client, "mamie", "hunter22")
    return client


def test_a_family_member_can_make_a_group(scoped_app):
    """The point of F41 — group-making was admin-only, which made scoping
    a story something you had to ask permission for."""
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")
    resp = client.post("/groups", data={"name": "Weekend crew"})
    assert resp.status_code == 302

    group = groups.get_group(scoped_app.config["STORIES_DIR"], "weekend-crew")
    assert group is not None
    assert group.created_by == "maman"   # recorded, for provenance


def test_making_a_group_puts_you_in_it(scoped_app):
    """Rights follow membership, so a creator left outside would be locked
    out of the group they just made with nothing on screen saying why."""
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")
    client.post("/groups", data={"name": "Weekend crew"})
    assert groups.get_group(scoped_app.config["STORIES_DIR"], "weekend-crew").members == ["maman"]


def test_a_member_can_edit_the_group(scoped_app):
    """Maman is in "Just us" and didn't make it — membership is what
    counts."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")

    resp = client.post("/groups/just-us", data={"name": "The two of us", "members": ["maman", "papa"]})
    assert resp.status_code == 302
    group = groups.get_group(stories_dir, "just-us")
    assert group.name == "The two of us"
    assert set(group.members) == {"maman", "papa"}


def test_someone_outside_the_group_cannot_edit_it(scoped_app, outsider_client):
    """The whole reason there is a gate at all: if any logged-in person
    could edit any group, anyone could add themselves to "Just us" and read
    it, and a group would protect nothing."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    resp = outsider_client.post(
        "/groups/just-us", data={"name": "Mine now", "members": ["mamie-rose"]}
    )
    assert resp.status_code == 403
    group = groups.get_group(stories_dir, "just-us")
    assert group.name == "Just us"
    assert group.members == ["maman"]


def test_an_outsider_cannot_read_the_scoped_story_after_trying(scoped_app, outsider_client):
    """The 403 has to actually hold, not just refuse the form: the thing
    being protected is the story."""
    assert outsider_client.get(f"/story/{scoped_app.config['SCOPED_ID']}").status_code == 404


def test_an_admin_can_edit_a_group_they_are_not_in(scoped_app):
    stories_dir = scoped_app.config["STORIES_DIR"]
    client = scoped_app.test_client()
    _login(client, "papa", "hunter22")   # admin, not in "Just us"

    resp = client.post("/groups/just-us", data={"name": "Renamed", "members": ["maman"]})
    assert resp.status_code == 302
    assert groups.get_group(stories_dir, "just-us").name == "Renamed"


def test_a_group_with_nobody_in_it_is_admin_only(scoped_app, outsider_client):
    """Membership is the gate, so an empty group has no family editors —
    it must fail closed rather than fall open to everyone."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Empty")
    assert outsider_client.post(
        "/groups/empty", data={"name": "Mine", "members": ["mamie-rose"]}
    ).status_code == 403


def test_everyone_can_see_the_group_list_and_pages(scoped_app, outsider_client):
    """A group's name isn't a secret — it shows on every story kept to it —
    so the page renders read-only rather than 404ing."""
    assert outsider_client.get("/groups").status_code == 200
    html = outsider_client.get("/groups/just-us").data.decode()
    assert html.count('name="members"') == 0      # no form to edit with
    assert "changed by the people in it" in html


def test_an_outsider_is_not_told_how_many_stories_are_kept_here(scoped_app, outsider_client):
    """A count of stories you can't read is still a count of stories you
    can't read — the same thing F40 stops the timeline's "kept to a group"
    pill from leaking to an outsider."""
    for path in ("/groups", "/groups/just-us"):
        html = outsider_client.get(path).data.decode()
        assert "1 story" not in html
        assert "kept to this group" not in html


def test_a_member_is_told(scoped_app):
    member = scoped_app.test_client()
    _login(member, "maman", "hunter22")
    assert "1 story is kept to this group" in member.get("/groups/just-us").data.decode()
    assert "1 story" in member.get("/groups").data.decode()


def test_a_member_gets_a_form_and_an_outsider_does_not(scoped_app, outsider_client):
    member = scoped_app.test_client()
    _login(member, "maman", "hunter22")
    assert 'name="members"' in member.get("/groups/just-us").data.decode()
    assert 'name="members"' not in outsider_client.get("/groups/just-us").data.decode()


def test_the_page_warns_before_you_widen_someone_elses_writing(scoped_app):
    """Adding a person republishes whatever other people kept to the group,
    not only your own stories. The one place to say that is the page where
    you'd do it."""
    client = scoped_app.test_client()
    _login(client, "papa", "hunter22")   # admin; the scoped story is Maman's
    assert "written by someone else" in client.get("/groups/just-us").data.decode()


def test_no_warning_when_the_only_stories_kept_here_are_yours(scoped_app):
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")   # she wrote the scoped story
    assert "written by someone else" not in client.get("/groups/just-us").data.decode()


# --- the same-scope barrier -------------------------------------------------


def test_a_group_covering_exactly_the_same_people_is_refused(scoped_app):
    """Two groups with identical membership are one circle under two names:
    a story kept to one looks protected from people who can read it through
    the other."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    groups.set_members(stories_dir, "just-us", ["maman", "papa"])
    client = scoped_app.test_client()
    _login(client, "papa", "hunter22")
    client.post("/groups", data={"name": "Weekend crew"})   # -> members == ["papa"]

    resp = client.post(
        "/groups/weekend-crew", data={"name": "Weekend crew", "members": ["maman", "papa"]},
        follow_redirects=True,
    )
    assert "already covers exactly these people" in resp.data.decode()
    assert "Just us" in resp.data.decode()   # and says which group
    assert groups.get_group(stories_dir, "weekend-crew").members == ["papa"]


def test_a_second_group_of_one_person_is_allowed(scoped_app):
    """A group of one is a note to a single person, and refusing one would
    mean refusing a group the moment someone types its name — making a
    group puts you in it, so everyone's first group is {them}."""
    stories_dir = scoped_app.config["STORIES_DIR"]      # "Just us" is {maman}
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")
    assert client.post("/groups", data={"name": "Notes to self"}).status_code == 302
    assert groups.get_group(stories_dir, "notes-to-self").members == ["maman"]


def test_the_same_scope_check_ignores_the_group_being_edited(scoped_app):
    """Saving a group without changing its members must not trip over
    itself."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Mine", members=["papa"])
    client = scoped_app.test_client()
    _login(client, "papa", "hunter22")
    resp = client.post("/groups/mine", data={"name": "Mine still", "members": ["papa"]})
    assert resp.status_code == 302
    assert groups.get_group(stories_dir, "mine").name == "Mine still"


def test_two_empty_groups_are_allowed(stories_dir):
    """Every group starts empty on the way to being filled in — "nobody
    yet" is a state, not a scope."""
    groups.create_group(stories_dir, "One")
    groups.create_group(stories_dir, "Two")
    assert len(groups.list_groups(stories_dir)) == 2


def test_same_scope_is_order_independent(scoped_app):
    stories_dir = scoped_app.config["STORIES_DIR"]
    papa, maman = "papa", "maman"
    groups.create_group(stories_dir, "A", members=[papa, maman])
    with pytest.raises(groups.GroupError, match="already covers"):
        groups.create_group(stories_dir, "B", members=[maman, papa])


def test_a_duplicated_member_is_collapsed_not_stored_twice(scoped_app):
    stories_dir = scoped_app.config["STORIES_DIR"]
    group = groups.create_group(stories_dir, "Dupes", members=["papa", "papa"])
    assert group.members == ["papa"]


def test_create_group_validates_its_members(stories_dir):
    with pytest.raises(groups.GroupError, match="Unknown person"):
        groups.create_group(stories_dir, "Ghosts", members=["nobody"])


def test_a_member_slug_cannot_escape_the_people_directory(stories_dir):
    with pytest.raises(groups.GroupError, match="Unknown person"):
        groups.create_group(stories_dir, "Sneaky", members=["../../etc"])


# --- the cap ----------------------------------------------------------------


def test_the_group_count_is_capped(stories_dir, monkeypatch):
    """Every group is a chip in the editor's audience row on a phone. Now
    that anyone can add one, something has to stop the row growing until
    it's unreadable."""
    monkeypatch.setattr(groups, "MAX_GROUPS", 3)
    for i in range(3):
        groups.create_group(stories_dir, f"Group {i}")
    with pytest.raises(groups.GroupError, match="as many as this book keeps"):
        groups.create_group(stories_dir, "One too many")


def test_the_create_form_disappears_at_the_cap(scoped_app, monkeypatch):
    monkeypatch.setattr(groups, "MAX_GROUPS", 1)
    client = scoped_app.test_client()
    _login(client, "maman", "hunter22")
    html = client.get("/groups").data.decode()
    assert "Create group" not in html
    assert "as many groups as it keeps" in html


# --- renaming ---------------------------------------------------------------


def test_a_rename_onto_another_groups_name_is_refused(scoped_app):
    """The slug can't change, so without this two groups could end up
    displaying the same name — and the audience chips would be two
    identical-looking buttons doing different things."""
    stories_dir = scoped_app.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Mine", created_by="papa")
    client = scoped_app.test_client()
    _login(client, "papa", "hunter22")
    resp = client.post("/groups/mine", data={"name": "just us"}, follow_redirects=True)
    assert "already a group" in resp.data.decode()
    assert groups.get_group(stories_dir, "mine").name == "Mine"


def test_created_by_survives_a_round_trip(scoped_app):
    stories_dir = scoped_app.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Mine", created_by="papa")
    assert groups.get_group(stories_dir, "mine").created_by == "papa"


def test_a_malformed_created_by_is_ignored_not_fatal(scoped_app):
    """`created_by` is provenance, not permission, so a garbled value costs
    a line of display text and nothing more — but it must not take the
    whole group down with it."""
    import json

    stories_dir = scoped_app.config["STORIES_DIR"]
    groups.create_group(stories_dir, "Mine", created_by="papa")
    path = stories_dir / "groups.json"
    data = json.loads(path.read_text())
    data[-1]["created_by"] = 17
    path.write_text(json.dumps(data))

    group = groups.get_group(stories_dir, "mine")
    assert group.created_by is None
    assert group.members == ["papa"]   # still editable by the people in it


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
