"""The one place a sidecar JSON file gets written (`app/jsonstore.py`).

Written after finding the same three lines copied into seven places, four
of which had drifted: they wrote `json.dumps(data, indent=2)` with no
`ensure_ascii=False`, so an account's display name and a write link's
label went to disk as escape sequences while the group carrying the same
name did not.

These tests pin the two properties the copies were supposed to share, and
the last one makes a copy hard to reintroduce.
"""

import json
from datetime import date

import pytest

from app import accounts, groups, jsonstore, people, settings, storage, write_links

#: A name a French family would actually type, and the one that exposed
#: the drift.
ACCENTED = "Amélie Noëlle Côté"


def test_a_typed_name_stays_readable_on_disk(tmp_path):
    path = tmp_path / "thing.json"
    jsonstore.write_json(path, {"name": ACCENTED})
    raw = path.read_text(encoding="utf-8")
    assert ACCENTED in raw, raw
    assert "\\u00e9" not in raw


def test_it_ends_with_a_newline_like_every_other_text_file_here(tmp_path):
    path = tmp_path / "thing.json"
    jsonstore.write_json(path, {"a": 1})
    assert path.read_text(encoding="utf-8").endswith("}\n")


def test_the_previous_file_survives_a_write_that_dies(tmp_path, monkeypatch):
    """Atomicity is the whole reason this isn't `path.write_text(...)`. A
    save that fails must leave the old settings readable, not a truncated
    file every page then 500s on."""
    path = tmp_path / "settings.json"
    jsonstore.write_json(path, {"title": "Before"})

    def boom(*args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(jsonstore.os, "replace", boom)
    with pytest.raises(OSError):
        jsonstore.write_json(path, {"title": "After"})
    assert json.loads(path.read_text(encoding="utf-8")) == {"title": "Before"}


def test_the_temporary_file_sits_beside_its_target(tmp_path):
    """`os.replace` is only atomic within one filesystem, so the temp file
    has to be a sibling — not in /tmp, which on a NAS is very often a
    different mount from the stories volume."""
    path = tmp_path / "deep" / "theme.json"
    path.parent.mkdir()
    jsonstore.write_json(path, {"label": ACCENTED})
    assert not list(path.parent.glob("*.tmp"))
    assert path.is_file()


# --- the files that were writing escapes ------------------------------------
#
# Only two of the four carry text a person typed. `account.json` holds a
# slug, a username, a role and a scrypt hash; `invites.json` holds a slug,
# a role and a token hash — neither has a field a name can reach today.
# They were fixed anyway, because the next field added to either is the one
# that would have found out.


def test_a_pending_request_keeps_the_name_someone_typed(tmp_path):
    """`display_name` and `note` are free text, typed by whoever is asking
    for an account (F39), and they sat in `pending.json` as escapes."""
    people_dir = storage.people_dir(tmp_path)
    people_dir.mkdir(parents=True, exist_ok=True)
    accounts.create_pending_request(
        people_dir, "amelie", "hunter22", display_name=ACCENTED, note=ACCENTED
    )
    raw = (people_dir / accounts.PENDING_FILENAME).read_text(encoding="utf-8")
    assert raw.count(ACCENTED) == 2, raw


def test_a_write_link_label_is_readable_on_disk(tmp_path):
    """The label is what the writer calls the link — "Mamie's page" — and
    it is the other field a name reaches."""
    people_dir = storage.people_dir(tmp_path)
    slug = people.create_person(people_dir, "Papa")
    write_links.create_link(people_dir, slug, label=ACCENTED)
    raw = (people_dir / slug / "write_links.json").read_text(encoding="utf-8")
    assert ACCENTED in raw, raw


def test_a_group_name_is_still_readable_on_disk(tmp_path):
    """groups.py was one of the three that already got this right — this is
    here so the shared helper doesn't quietly take it away again."""
    people_dir = storage.people_dir(tmp_path)
    people.create_person(people_dir, "Papa")
    groups.create_group(tmp_path, ACCENTED, created_by="papa")
    raw = (tmp_path / "groups.json").read_text(encoding="utf-8")
    assert ACCENTED in raw, raw


def test_a_book_title_is_still_readable_on_disk(tmp_path):
    settings.save(tmp_path, {"title": ACCENTED})
    raw = (tmp_path / "settings.json").read_text(encoding="utf-8")
    assert ACCENTED in raw, raw


def test_an_account_file_still_says_what_it_always_said(tmp_path):
    """The helper changed how `account.json` is written, so this pins what
    is in it — the role in particular, which `auth.login_required` reads on
    every request and which every access-control rule in the app hangs
    off."""
    people_dir = storage.people_dir(tmp_path)
    slug = people.create_person(people_dir, ACCENTED)
    accounts.create_account(people_dir, slug, "amelie", "hunter22", "admin")
    data = json.loads((people_dir / slug / "account.json").read_text(encoding="utf-8"))
    assert data["username"] == "amelie"
    assert data["role"] == "admin"
    assert data["password_hash"].startswith("scrypt:")
    assert accounts.get_account(people_dir, slug).role == "admin"


# --- the ratchet ------------------------------------------------------------


def test_no_module_hand_rolls_its_own_json_write():
    """The drift happened because the idiom was cheap to copy. This makes a
    copy fail the suite instead of merely being noticed in review.

    Only `json.dumps` *written to a file* is the problem; dumping to a
    string for an HTTP response or a template is fine, so this looks for
    the write rather than the dump.
    """
    import pathlib

    app_dir = pathlib.Path(__file__).resolve().parent.parent / "app"
    offenders = []
    for path in sorted(app_dir.glob("*.py")):
        if path.name == "jsonstore.py":
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if "json.dumps" in line and "write_text" in line:
                offenders.append(f"{path.name}:{number}")
    assert not offenders, (
        f"{offenders} write JSON by hand — use jsonstore.write_json so the "
        "file stays atomic and readable (ensure_ascii=False)"
    )


def test_a_story_still_saves_the_accented_title_it_was_given(tmp_path):
    """Not a jsonstore file — a sanity check that the round-trip this whole
    thing is about was never broken for stories, which write frontmatter."""
    story_id = storage.create_story(tmp_path, ACCENTED, date(2026, 1, 1), "body")
    assert ACCENTED in (tmp_path / story_id / "index.md").read_text(encoding="utf-8")
