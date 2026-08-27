"""Tests for FEATURES.md F43: what a backup zip may and may not carry.

Two rules, from both directions. **Out**: only an admin's export contains
account files — everyone else's zip is memories and people, no password
hashes. **In**: an import never restores a credential file at all, and the
cast is additive rather than a collision that aborts the whole restore.
"""

import zipfile
from datetime import date
from io import BytesIO

import pytest

from app import (
    accounts, backup, groups, invites, people, secret_key, storage, write_links,
)
from tests.conftest import _login


@pytest.fixture
def accounts_app(app_factory):
    return app_factory(ACCOUNTS_ENABLED=True)


@pytest.fixture
def cast(accounts_app, stories_dir):
    """An admin (papa) and a plain family member (mamie), each with an
    account; a write link of papa's; an invite waiting for a third person
    who has no account yet; and a pending request. One of every credential
    file the app writes."""
    people_dir = stories_dir / "people"
    for name in ("Papa", "Mamie", "Tata"):
        people.create_person(people_dir, name)
    accounts.create_account(people_dir, "papa", "papa", "adminpass1", role="admin")
    accounts.create_account(people_dir, "mamie", "mamie", "mamiepass1", role="family")
    write_links.create_link(people_dir, "papa", label="for the recital")
    invites.create_invite(people_dir, "tata", "family", created_by="papa")
    accounts.create_pending_request(stories_dir, "cousin", "cousinpass1", "Cousin", "")
    return people_dir


def _zip_for(accounts_app, username, password):
    client = accounts_app.test_client()
    _login(client, username, password)
    resp = client.get("/export")
    assert resp.status_code == 200
    return zipfile.ZipFile(BytesIO(resp.data))


# --- the constant the two sides share ---------------------------------------


def test_credential_filenames_match_the_modules_that_write_them():
    """`backup.CREDENTIAL_FILENAMES` is the list both the export filter and
    the import filter read. Rename a file in the module that owns it without
    updating that set and password hashes start travelling again, silently,
    which is exactly the kind of drift a test has to catch."""
    assert accounts.ACCOUNT_FILENAME in backup.CREDENTIAL_FILENAMES
    assert accounts.PENDING_FILENAME in backup.CREDENTIAL_FILENAMES
    assert invites.INVITES_FILENAME in backup.CREDENTIAL_FILENAMES
    assert write_links.WRITE_LINKS_FILENAME in backup.CREDENTIAL_FILENAMES


# --- export ------------------------------------------------------------------


def test_family_member_export_has_no_credential_files(accounts_app, cast, stories_dir):
    storage.create_story(stories_dir, "Public", date(2026, 1, 2), "for everyone")
    zf = _zip_for(accounts_app, "mamie", "mamiepass1")
    names = zf.namelist()

    assert not [n for n in names if n.rsplit("/", 1)[-1] in backup.CREDENTIAL_FILENAMES]
    # ...and nothing that merely looks like one either
    blob = b"".join(zf.read(n) for n in names)
    assert b"password_hash" not in blob
    assert b"token_hash" not in blob
    # the memories themselves are untouched by this rule
    assert any(n.endswith("/index.md") and not n.startswith("people/") for n in names)
    assert "people/papa/index.md" in names


def test_admin_export_still_carries_everything(accounts_app, cast, stories_dir):
    storage.create_story(stories_dir, "Public", date(2026, 1, 2), "for everyone")
    names = _zip_for(accounts_app, "papa", "adminpass1").namelist()

    assert "people/papa/account.json" in names
    assert "people/mamie/account.json" in names
    assert "people/papa/write_links.json" in names
    assert "people/tata/invites.json" in names
    assert accounts.PENDING_FILENAME in names


def test_shared_password_mode_export_is_unchanged(auth_client, stories_dir):
    """Without accounts there is one identity and no account files to
    withhold — an existing install must see no difference."""
    story_id = storage.create_story(stories_dir, "Solo", date(2026, 1, 3), "body")
    zf = zipfile.ZipFile(BytesIO(auth_client.get("/export").data))
    assert f"{story_id}/index.md" in zf.namelist()


def test_a_write_link_guest_cannot_export_at_all(accounts_app, cast, stories_dir):
    """The third tier, and the one with no test until the view helpers were
    split out of routes_pages.py.

    A delegated write link (F19) hands somebody a way to add one story
    without an account. They are not a reader: `/export` is a way to take
    the whole book away, and `login_required` has to keep them out of it
    even while they are legitimately holding a session.
    """
    _link, token = write_links.create_link(cast, "papa", label="one page")
    guest = accounts_app.test_client()
    assert guest.get(f"/w/{token}").headers["Location"] == "/w/write"
    assert guest.get("/w/write").status_code == 200, "the guest can write"

    assert guest.get("/export").headers["Location"].startswith("/login")
    assert guest.get("/").headers["Location"].startswith("/login")


def test_family_member_export_still_omits_scoped_stories(accounts_app, cast, stories_dir):
    """F40's rule and F43's rule are independent, and both still hold."""
    group = groups.create_group(stories_dir, "Just us", created_by="papa")
    secret_id = storage.create_story(stories_dir, "Secret", date(2026, 1, 1), "private")
    secret = storage.get_story(stories_dir, secret_id)
    storage.save_story(stories_dir, secret_id, secret.title, secret.date, secret.body,
                       audience=[group.slug])
    storage.create_story(stories_dir, "Public", date(2026, 1, 2), "for everyone")

    names = _zip_for(accounts_app, "mamie", "mamiepass1").namelist()
    assert not [n for n in names if n.startswith(secret_id)]


# --- import ------------------------------------------------------------------


def _backup_of(source_dir):
    """The real export, with credentials in it — the widest zip an import
    ever has to refuse. Second of two byte-identical hand-rolled walks
    that both predated `backup.write_backup` existing."""
    return backup.write_backup(source_dir)


def test_import_restores_people_into_a_book_that_already_has_some(tmp_path, stories_dir):
    """The bug this fixes: `people` matches `is_valid_story_id`, so the
    collision check saw it on both sides and refused the whole restore."""
    source = tmp_path / "source"
    source.mkdir()
    people.create_person(source / "people", "Papa")
    people.create_person(source / "people", "Mamie")
    storage.create_story(source, "Restored", date(2026, 1, 1), "body")

    people.create_person(stories_dir / "people", "Mamie")

    count = backup.import_backup(stories_dir, _backup_of(source))

    assert count == 1
    assert sorted(p.slug for p in people.list_people(stories_dir / "people")) == ["mamie", "papa"]


def test_import_keeps_the_person_already_here(tmp_path, stories_dir):
    """The living folder is the newer truth — a person in both the zip and
    the book is left exactly as they are, not merged or overwritten."""
    source = tmp_path / "source"
    source.mkdir()
    people.create_person(source / "people", "Mamie", relation="stale copy")
    storage.create_story(source, "Restored", date(2026, 1, 1), "body")

    people.create_person(stories_dir / "people", "Mamie", relation="the current one")
    backup.import_backup(stories_dir, _backup_of(source))

    assert people.get_person(stories_dir / "people", "mamie").relation == "the current one"


def test_import_never_restores_credentials(tmp_path, stories_dir):
    """A zip is a portable file. Restoring one from another book must not
    install its accounts — least of all its admins — into this one."""
    source = tmp_path / "source"
    source.mkdir()
    people.create_person(source / "people", "Papa")
    accounts.create_account(source / "people", "papa", "papa", "adminpass1", role="admin")
    write_links.create_link(source / "people", "papa", label="recital")
    accounts.create_pending_request(source, "cousin", "cousinpass1", "Cousin", "")
    storage.create_story(source, "Restored", date(2026, 1, 1), "body")

    backup.import_backup(stories_dir, _backup_of(source))

    assert people.get_person(stories_dir / "people", "papa") is not None
    assert accounts.get_account(stories_dir / "people", "papa") is None
    assert not (stories_dir / "people" / "papa" / write_links.WRITE_LINKS_FILENAME).exists()
    assert not (stories_dir / accounts.PENDING_FILENAME).exists()


def test_import_still_aborts_wholly_on_a_story_collision(tmp_path, stories_dir):
    """People became additive; stories did not. A colliding story still
    writes nothing at all — including none of the zip's people."""
    source = tmp_path / "source"
    source.mkdir()
    people.create_person(source / "people", "Papa")
    story_id = storage.create_story(source, "Same day", date(2026, 1, 1), "theirs")
    storage.create_story(stories_dir, "Same day", date(2026, 1, 1), "ours")

    with pytest.raises(backup.ImportCollision):
        backup.import_backup(stories_dir, _backup_of(source))

    assert people.get_person(stories_dir / "people", "papa") is None
    assert storage.get_story(stories_dir, story_id).body.strip() == "ours"


def test_import_ignores_odd_shapes_under_people(tmp_path, stories_dir):
    """Anything under people/ this app never writes is skipped rather than
    extracted — a loose file at the root of people/, or a bad slug."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-01-01-ok/index.md", "---\ntitle: Ok\ndate: 2026-01-01\n---\nbody\n")
        zf.writestr("people/loose.md", "not a person")
        zf.writestr("people/Not A Slug/index.md", "nope")
    buf.seek(0)

    backup.import_backup(stories_dir, buf)

    assert not (stories_dir / "people" / "loose.md").exists()
    assert not (stories_dir / "people" / "Not A Slug").exists()


# --- the signing key, which is in a category of its own (F59) ---------------
#
# CREDENTIAL_FILENAMES above are scrypt hashes: withheld from non-admins as
# an offline guessing target, and an admin exporting their own book's is
# exporting something they already control. The session key is not a target,
# it is the answer — whoever holds it mints a cookie for any account in the
# book without guessing anything. So it leaves in nobody's zip, admin
# included, and comes back from none.


def _write_key(stories_dir, value="deadbeef" * 8):
    path = stories_dir / secret_key.SECRET_KEY_FILENAME
    path.write_text(value + "\n")
    return path


def test_the_signing_key_is_in_no_admin_s_export(cast, accounts_app, stories_dir):
    _write_key(stories_dir)
    names = _zip_for(accounts_app, "papa", "adminpass1").namelist()
    assert secret_key.SECRET_KEY_FILENAME not in names


def test_the_signing_key_is_in_no_family_member_s_export(cast, accounts_app, stories_dir):
    _write_key(stories_dir)
    names = _zip_for(accounts_app, "mamie", "mamiepass1").namelist()
    assert secret_key.SECRET_KEY_FILENAME not in names


def test_the_signing_key_is_in_no_export_with_accounts_off(stories_dir, auth_client):
    """With one shared password there is one identity and it gets
    everything — except this."""
    _write_key(stories_dir)
    storage.create_story(stories_dir, "A day", date(2026, 1, 1), "body")

    resp = auth_client.get("/export")

    assert resp.status_code == 200
    assert secret_key.SECRET_KEY_FILENAME not in zipfile.ZipFile(BytesIO(resp.data)).namelist()


def test_an_import_refuses_a_zip_carrying_a_signing_key(stories_dir):
    """Refused outright rather than skipped. A stranger's key overwriting
    this book's would hand them every session the app signs afterwards, and
    a zip is a file that arrives by mail."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-01-01-ok/index.md", "---\ntitle: Ok\ndate: 2026-01-01\n---\nbody\n")
        zf.writestr(secret_key.SECRET_KEY_FILENAME, "attackers-key")
    buf.seek(0)

    with pytest.raises(ValueError, match="signing key"):
        backup.import_backup(stories_dir, buf)

    assert not (stories_dir / secret_key.SECRET_KEY_FILENAME).exists()
    assert not (stories_dir / "2026-01-01-ok").exists()


def test_a_signing_key_hidden_deeper_in_the_zip_is_refused_too(stories_dir):
    """The check is on the filename anywhere in the tree, not just at the
    root, so `people/papa/secret_key` cannot sneak one past it."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-01-01-ok/index.md", "---\ntitle: Ok\ndate: 2026-01-01\n---\nbody\n")
        zf.writestr(f"people/papa/{secret_key.SECRET_KEY_FILENAME}", "attackers-key")
    buf.seek(0)

    with pytest.raises(ValueError, match="signing key"):
        backup.import_backup(stories_dir, buf)


def test_a_real_round_trip_survives_the_new_exclusion(stories_dir, tmp_path):
    """The exclusion must not cost the thing backups are for."""
    source = tmp_path / "source"
    source.mkdir()
    _write_key(source)
    storage.create_story(source, "A day worth keeping", date(2026, 1, 1), "the body")

    assert backup.import_backup(stories_dir, _backup_of(source)) == 1
    assert not (stories_dir / secret_key.SECRET_KEY_FILENAME).exists()
    restored = storage.list_stories(stories_dir)
    assert [s.title for s in restored] == ["A day worth keeping"]
