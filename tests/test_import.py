"""Tests for restoring a backup zip (from /export) via /import."""

import zipfile
from datetime import date
from io import BytesIO

import pytest

from app import backup, storage


def _export_zip(source_dir):
    """The real export, not a lookalike.

    This used to be a hand-rolled walk that zipped everything under
    `source_dir` — which skipped neither `.tmp` leftovers nor credential
    files, so every test below restored a zip the app would never have
    produced. `backup.write_backup` is what `/export` calls; the defaults
    are the admin/single-password answer (every story, credentials
    included), which is the widest zip a restore ever has to survive.
    """
    return backup.write_backup(source_dir)


# --- storage.import_backup ----------------------------------------------------


def test_import_backup_restores_into_empty_dir(tmp_path, stories_dir):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    story_id = storage.create_story(source_dir, "Restored story", date(2026, 1, 1), "body")

    count = backup.import_backup(stories_dir, _export_zip(source_dir))

    assert count == 1
    story = storage.get_story(stories_dir, story_id)
    assert story.title == "Restored story"
    assert story.body.strip() == "body"


def test_import_backup_rejects_on_collision_writes_nothing(tmp_path, stories_dir):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    story_id = storage.create_story(source_dir, "Story", date(2026, 1, 1), "new body")
    storage.create_story(stories_dir, "Story", date(2026, 1, 1), "existing body")

    zip_buf = _export_zip(source_dir)
    with pytest.raises(backup.ImportCollision) as exc_info:
        backup.import_backup(stories_dir, zip_buf)
    assert story_id in exc_info.value.colliding_ids

    # Nothing was written: the one story folder that was here is still the
    # only one. (Counted as story folders rather than directory entries —
    # a book also carries settings.json and may carry themes/ or people/.)
    assert len(list(storage.list_stories(stories_dir))) == 1
    existing = storage.get_story(stories_dir, story_id)
    assert existing.body.strip() == "existing body"


def test_import_backup_rejects_path_traversal(stories_dir):
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("../evil.txt", "pwned")
    buf.seek(0)
    with pytest.raises(ValueError):
        backup.import_backup(stories_dir, buf)


def test_import_backup_skips_unexpected_root_files(stories_dir):
    """A zip of nothing but root files still errors — but for having no
    stories in it, not for the files themselves."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("readme.txt", "hi")
    buf.seek(0)
    with pytest.raises(ValueError, match="no stories"):
        backup.import_backup(stories_dir, buf)
    assert not (stories_dir / "readme.txt").exists()


def test_a_real_accounts_mode_backup_can_be_restored(stories_dir):
    """The round trip that was broken before F40's inspection: since F19 an
    export carries `pending_accounts.json`, and since F40 `groups.json` too,
    and aborting on the first one made every accounts-mode backup
    un-importable. A one-tap backup you cannot restore is the exact failure
    this app exists to avoid."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-05-01-a-day-out/index.md",
                    "---\ntitle: A day out\ndate: 2026-05-01\n---\nbody\n")
        zf.writestr("people/papa/index.md", "---\nname: Papa\n---\n")
        zf.writestr("pending_accounts.json", "[]\n")
        zf.writestr("groups.json", "[]\n")
    buf.seek(0)

    # One story. `people/` used to be counted as a second "story folder",
    # which is the same mistake that made a backup un-restorable into a book
    # that already had a cast (F43) — people now ride along uncounted.
    assert backup.import_backup(stories_dir, buf) == 1
    assert (stories_dir / "2026-05-01-a-day-out" / "index.md").is_file()
    assert (stories_dir / "people" / "papa" / "index.md").is_file()
    # Live operational state is never overwritten from an old zip.
    assert not (stories_dir / "pending_accounts.json").exists()
    assert not (stories_dir / "groups.json").exists()


def test_import_still_aborts_on_an_unsafe_path(stories_dir):
    """Skipping unknown root entries must not have weakened zip-slip: an
    unsafe path aborts the whole import even alongside a valid story."""
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-05-01-fine/index.md",
                    "---\ntitle: Fine\ndate: 2026-05-01\n---\nbody\n")
        zf.writestr("../evil.txt", "pwned")
    buf.seek(0)
    with pytest.raises(ValueError, match="Unsafe path"):
        backup.import_backup(stories_dir, buf)
    assert not (stories_dir / "2026-05-01-fine").exists()


def test_import_backup_rejects_empty_zip(stories_dir):
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w"):
        pass
    buf.seek(0)
    with pytest.raises(ValueError):
        backup.import_backup(stories_dir, buf)


def test_import_backup_rejects_bad_zip(stories_dir):
    buf = BytesIO(b"not a zip file")
    with pytest.raises(zipfile.BadZipFile):
        backup.import_backup(stories_dir, buf)


def test_import_backup_includes_images(tmp_path, stories_dir, jpeg_bytes):
    from werkzeug.datastructures import FileStorage

    source_dir = tmp_path / "source"
    source_dir.mkdir()
    story_id = storage.create_story(source_dir, "Photo story", date(2026, 1, 1), "")
    filename = storage.save_image(
        source_dir, story_id, FileStorage(stream=jpeg_bytes(color="blue", size=(50, 50)), filename="p.jpg")
    )

    backup.import_backup(stories_dir, _export_zip(source_dir))

    assert (stories_dir / story_id / filename).is_file()


# --- API -------------------------------------------------------------------------


def test_api_import_requires_auth(client):
    resp = client.post("/api/import", data={}, content_type="multipart/form-data")
    assert resp.status_code == 302


def test_api_import_no_file_returns_400(auth_client):
    resp = auth_client.post("/api/import", data={}, content_type="multipart/form-data")
    assert resp.status_code == 400


def test_api_import_success(auth_client, stories_dir, tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    storage.create_story(source_dir, "Restored", date(2026, 1, 1), "body")

    resp = auth_client.post(
        "/api/import",
        data={"file": (_export_zip(source_dir), "backup.zip")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 200
    assert resp.get_json()["imported"] == 1


def test_api_import_collision_returns_409(auth_client, stories_dir, tmp_path):
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    storage.create_story(source_dir, "Story", date(2026, 1, 1), "new")
    storage.create_story(stories_dir, "Story", date(2026, 1, 1), "existing")

    resp = auth_client.post(
        "/api/import",
        data={"file": (_export_zip(source_dir), "backup.zip")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 409
    assert "error" in resp.get_json()


def test_api_import_bad_zip_returns_400(auth_client):
    resp = auth_client.post(
        "/api/import",
        data={"file": (BytesIO(b"not a zip"), "backup.zip")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 400


# --- page --------------------------------------------------------------------------


def test_import_page_renders(auth_client):
    resp = auth_client.get("/import")
    assert resp.status_code == 200
    assert b"Import a backup" in resp.data


def test_import_page_requires_auth(client):
    resp = client.get("/import")
    assert resp.status_code == 302
