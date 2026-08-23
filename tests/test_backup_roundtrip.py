"""What `/export` writes, `import_backup` reads back (FEATURES.md F8).

These are the tests the old layout could not have. Export lived in a route
and import in `storage.py`, so nothing could exercise the two ends of one
contract together — and the import tests compensated by growing their own
export, a hand-rolled directory walk that applied neither the `.tmp` skip
nor the credential filter the real one applies. Every restore they checked
was a restore of a zip this app would never have produced.

With both halves in `backup.py` a round trip is one line, so these check
the property that actually matters to a family: **the backup you took is
the book you get back** — and, for a viewer who cannot see everything,
exactly the part of it they could see and no more.
"""

import zipfile
from datetime import date

import pytest

from app import accounts, backup, groups, people, storage
from tests.conftest import _login

ADMIN = ("papa", "adminpass1")
MEMBER = ("mamie", "mamiepass1")
OUTSIDER = ("tonton", "tontonpass1")


@pytest.fixture
def accounts_app(app_factory):
    return app_factory(ACCOUNTS_ENABLED=True)


@pytest.fixture
def book(accounts_app, stories_dir):
    """An admin, a member inside the group, a member outside it, one story
    everyone may read and one only the group may."""
    people_dir = storage.people_dir(stories_dir)
    for name, (username, password), role in [
        ("Papa", ADMIN, "admin"), ("Mamie", MEMBER, "family"),
        ("Tonton", OUTSIDER, "family"),
    ]:
        slug = people.create_person(people_dir, name)
        accounts.create_account(people_dir, slug, username, password, role)
    groups.create_group(stories_dir, "Just Us", members=["mamie"], created_by="papa")
    return {
        "public": storage.create_story(stories_dir, "Public", date(2026, 1, 1), "everyone"),
        "scoped": storage.create_story(
            stories_dir, "Secret", date(2026, 1, 2), "hush", audience=["just-us"]
        ),
    }


def _export_as(accounts_app, credentials):
    client = accounts_app.test_client()
    _login(client, *credentials)
    resp = client.get("/export")
    assert resp.status_code == 200
    from io import BytesIO
    return BytesIO(resp.data)


def _restore_into(tmp_path, name, zip_file):
    fresh = tmp_path / name
    fresh.mkdir()
    count = backup.import_backup(fresh, zip_file)
    return fresh, count


# --- the round trip, per tier -----------------------------------------------


def test_an_admin_backup_restores_the_whole_book(accounts_app, book, tmp_path):
    fresh, count = _restore_into(tmp_path, "admin-restore", _export_as(accounts_app, ADMIN))
    assert count == 2
    restored = {s.id for s in storage.list_stories(fresh)}
    assert restored == {book["public"], book["scoped"]}
    assert {p.slug for p in people.list_people(storage.people_dir(fresh))} == {
        "papa", "mamie", "tonton"
    }


def test_a_member_backup_restores_exactly_what_they_could_see(accounts_app, book, tmp_path):
    """The member outside the group took a partial backup. It restores as
    the part of the book they could read — not the whole thing, and not
    nothing."""
    fresh, count = _restore_into(tmp_path, "outsider-restore", _export_as(accounts_app, OUTSIDER))
    assert count == 1
    assert {s.id for s in storage.list_stories(fresh)} == {book["public"]}


def test_a_member_inside_the_group_gets_the_scoped_story_back(accounts_app, book, tmp_path):
    fresh, count = _restore_into(tmp_path, "member-restore", _export_as(accounts_app, MEMBER))
    assert count == 2
    assert {s.id for s in storage.list_stories(fresh)} == {book["public"], book["scoped"]}


@pytest.mark.parametrize("who", [ADMIN, MEMBER, OUTSIDER], ids=["admin", "member", "outsider"])
def test_no_restore_ever_installs_an_account(accounts_app, book, tmp_path, who):
    """The rule that must hold on every tier at once (F43). An admin's zip
    legitimately *contains* credential files; a restore still must not put
    them back, or a zip becomes a way to install your admins into somebody
    else's book."""
    fresh, _count = _restore_into(tmp_path, f"restore-{who[0]}", _export_as(accounts_app, who))
    people_dir = storage.people_dir(fresh)
    assert accounts.list_accounts(people_dir) == []
    leftovers = [
        path.name for path in fresh.rglob("*")
        if path.name in backup.CREDENTIAL_FILENAMES
    ]
    assert leftovers == []


def test_a_scoped_story_the_exporter_could_not_see_is_simply_absent(
    accounts_app, book, tmp_path
):
    """Not "restored and then hidden" — absent from the zip, so absent from
    disk. The photos and `.versions/` go with it, which is the reason
    export is scoped at all: they would otherwise be the way around the
    group."""
    zip_file = _export_as(accounts_app, OUTSIDER)
    names = zipfile.ZipFile(zip_file).namelist()
    assert not [n for n in names if n.startswith(book["scoped"])]
    zip_file.seek(0)
    fresh, _count = _restore_into(tmp_path, "no-trace", zip_file)
    assert not (fresh / book["scoped"]).exists()


# --- what write_backup itself guarantees ------------------------------------


def test_a_half_written_file_never_travels(stories_dir):
    """`.tmp` files are what an interrupted atomic write leaves behind. The
    hand-rolled export in the tests did not skip them; the real one does,
    and this is why the tests now use the real one."""
    storage.create_story(stories_dir, "A story", date(2026, 1, 1), "body")
    (stories_dir / "settings.json.tmp").write_text("{}", encoding="utf-8")
    names = zipfile.ZipFile(backup.write_backup(stories_dir)).namelist()
    assert not [n for n in names if n.endswith(".tmp")], names


def test_the_things_that_are_not_stories_are_never_audience_filtered(stories_dir):
    """`people/`, `themes/` and `groups.json` sit at the top of the stories
    directory beside story folders, and a scoped export must not mistake
    them for stories nobody may see — a backup that lost its cast would be
    worse than one that lost a story."""
    people_dir = storage.people_dir(stories_dir)
    people.create_person(people_dir, "Mamie")
    groups.create_group(stories_dir, "Just Us", members=["mamie"])
    kept = storage.create_story(stories_dir, "Kept", date(2026, 1, 1), "yes")
    storage.create_story(stories_dir, "Dropped", date(2026, 1, 2), "no")

    names = zipfile.ZipFile(
        backup.write_backup(stories_dir, allowed_ids={kept})
    ).namelist()
    tops = {n.split("/")[0] for n in names}
    assert storage.PEOPLE_DIRNAME in tops
    assert groups.GROUPS_FILENAME in tops
    assert kept in tops
    assert "2026-01-02-dropped" not in tops


def test_write_backup_hands_back_a_stream_ready_to_read(stories_dir):
    """`send_file` streams whatever this returns, so it has to come back
    rewound — a zip served from its own end is a zero-byte download."""
    storage.create_story(stories_dir, "A story", date(2026, 1, 1), "body")
    handle = backup.write_backup(stories_dir)
    assert handle.tell() == 0
    assert handle.read(2) == b"PK"


# --- the two halves agree ---------------------------------------------------


def test_both_halves_of_the_round_trip_live_in_one_module():
    """The reason `backup.py` exists. Export was thirty lines in a route
    and import a hundred and fifty in `storage.py`; nothing held them to
    each other, and the tests had written their own export twice to cope.
    """
    assert hasattr(backup, "write_backup")
    assert hasattr(backup, "import_backup")
    assert not hasattr(storage, "import_backup"), (
        "import_backup moved to backup.py — storage.py is the story "
        "filesystem, not the backup format"
    )


def test_storage_no_longer_reaches_up_into_settings_and_themes():
    """Those three imports lived inside `import_backup`'s body, with a
    comment explaining that keeping them local kept the dependency arrow
    presentable. Moving the function moved the reason for them."""
    source = (
        storage.__file__ and __import__("pathlib").Path(storage.__file__).read_text()
    )
    for upward in ("from . import settings", "from .theme_catalog", "from .themes"):
        assert upward not in source, (
            f"storage.py imports {upward!r} again — the data layer every "
            "other module leans on should not lean back"
        )
