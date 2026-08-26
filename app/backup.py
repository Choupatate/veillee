"""Making a backup zip, and restoring one (FEATURES.md F8, F43, F50, F51, F58).

**Both halves of the round trip live here, and that is the whole point of
the file.** Export used to be thirty lines inside the `/export` route and
import a hundred and fifty inside `storage.py` — two ends of one contract,
in two layers, unable to see each other. Two things went wrong because of
it. `storage.py` had to reach *up* to `settings`, `themes` and
`theme_catalog` through imports written inside a function body to keep the
dependency arrow presentable. And the tests grew their own export: two
byte-identical `_export_zip` helpers that walked the directory and zipped
everything, applying neither the `.tmp` skip nor the credential filter the
real export applies — so every import test restored a zip this app would
never have produced.

**What is deliberately *not* here: who may export what.** `write_backup`
takes the two decisions already made — which story folders may go in, and
whether credential files may — and does not make them. Those are
`routes_pages.py`'s `_exportable_story_ids` and
`_viewer_may_export_credentials`, which read the session and stay beside
the route they govern. The split is on purpose: this module is the
mechanism, the route is the policy, and an access-control rule is easier
to audit next to the thing it guards than one import away.

The three answers that policy produces, for reference, since this is where
someone will come looking: a write-link guest never reaches `/export` at
all; a family member gets the stories they can see and no credential
files; an admin gets everything. With accounts off there is one identity
and one answer — everything.
"""

import json
import zipfile
from datetime import date
from pathlib import Path
from tempfile import TemporaryFile
from typing import Optional

from . import groups, settings, storage, themes
from .jsonstore import write_json
from .theme_catalog import BY_FILENAME
from .themes import USER_THEMES_DIRNAME


# Files under stories/ that hold credentials rather than memories: password
# hashes, and the token hashes behind invite and write links. Named here
# because a backup is the only thing that ever has to know the difference,
# but each file is written by the module that owns the feature —
# `accounts.ACCOUNT_FILENAME`, `accounts.PENDING_FILENAME`,
# `invites.INVITES_FILENAME`, `write_links.WRITE_LINKS_FILENAME`,
# cross-checked by `tests/test_backup_credentials.py` so the two can't
# drift apart.
#
# They never travel in a backup zip in either direction (F43): a non-admin's
# export leaves them out, and an import never restores them. A zip carries
# memories and people; logins stay where they were made.
CREDENTIAL_FILENAMES = frozenset({
    "account.json",
    "pending_accounts.json",
    "invites.json",
    "write_links.json",
})

#: Root-level entries that are not story folders, and so are never
#: audience-scoped on the way out. Everything else at the top of the
#: stories directory is a story id.
NOT_A_STORY = frozenset({
    storage.PEOPLE_DIRNAME,
    themes.USER_THEMES_DIRNAME,
    groups.GROUPS_FILENAME,
})


class ImportCollision(ValueError):
    """Raised when a backup zip contains a story id that already exists on
    disk. Nothing is written when this is raised — see import_backup()."""

    def __init__(self, colliding_ids: list[str]):
        self.colliding_ids = colliding_ids
        noun = "story" if len(colliding_ids) == 1 else "stories"
        super().__init__(f"{len(colliding_ids)} {noun} already exist: {', '.join(colliding_ids)}")


def write_backup(stories_dir, *, allowed_ids=None, with_credentials=True):
    """Zip the stories directory into a temporary file, rewound and ready
    to stream. The caller closes it (`send_file` does).

    `allowed_ids` is the set of story folders that may go in, or None for
    "all of them" — None is what a single-password install and an admin
    both get, and what makes this identical to the backup the app has
    always written. `with_credentials=False` drops every
    `CREDENTIAL_FILENAMES` entry.

    Both are decisions, and neither is made here: see the module docstring.

    Stored rather than deflated. The bulk of any real backup is JPEGs,
    which do not compress, and a family restoring from a dead NAS is
    better served by a zip that any tool on any machine can open than by
    one that is four per cent smaller.
    """
    stories_dir = Path(stories_dir)
    tmp = TemporaryFile()
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_STORED) as zf:
        for path in sorted(stories_dir.rglob("*")):
            if path.is_dir() or path.name.endswith(".tmp"):
                continue
            if not with_credentials and path.name in CREDENTIAL_FILENAMES:
                continue
            relative = path.relative_to(stories_dir)
            # The first path segment is the story id for anything under a
            # story folder; people/, themes/ (F50), groups.json and the
            # other root-level files aren't stories and are never
            # audience-scoped.
            top = relative.parts[0]
            if (
                allowed_ids is not None
                and top not in NOT_A_STORY
                and (stories_dir / top).is_dir()
                and top not in allowed_ids
            ):
                continue
            zf.write(path, relative)
    tmp.seek(0)
    return tmp


def import_backup(stories_dir, zip_file) -> int:
    """Restore a backup zip produced by the /export download.

    Extracts entries shaped like `<valid-story-id>/...`, plus the people in
    `people/<slug>/...` (see below). If ANY of the zip's story ids already
    exist on disk, raises ImportCollision and writes nothing — an import
    either fully succeeds or has no effect at all. Returns the number of
    story folders imported; restored people are not counted, since a
    restore is about the memories and the cast comes along with them.

    Unsafe paths (absolute, or containing `..`) still abort the whole
    import. Other root-level entries are *skipped* rather than rejected,
    which is what lets a real backup be restored at all: since F19 an
    export can contain `pending_accounts.json`, and since F40 `groups.json`
    too, and aborting on the first one made every accounts-mode backup
    un-importable — a one-tap backup you cannot restore being the exact
    failure this app exists to avoid.

    Skipped, not imported, deliberately: those files are live operational
    state (who is waiting for an account, who is in which group), and
    silently overwriting them from an old zip would be worse than leaving
    them alone. A consequence worth knowing: a restored story can reference
    a group this install doesn't have. `groups.can_see` treats an unknown
    group as "nobody but the author", so that fails private rather than
    public.

    **People are additive, never a collision (F43).** `people` matches
    `is_valid_story_id`, so it used to be treated as one enormous story
    folder — which meant any backup from a book with a cast could not be
    restored into a book that already had one: the collision check saw
    `people` on both sides and aborted everything. Every person in the zip
    whose folder is already here is now simply skipped, and the rest are
    restored. Skipped rather than merged because the living folder is the
    newer truth, and a person's `index.md` carries edges (parents,
    partners) that a half-old copy would contradict.

    **Made themes come back, additively (F50).** A theme pack under
    `themes/<name>/` is made content — someone described a world and
    generated thirty-five pictures for it — so it is restored like a
    person rather than skipped like operational state. A pack whose folder
    is already here is left alone, and only the two shapes this app writes
    (`theme.json`, and pictures the catalogue names) are extracted, so a
    zip cannot use a theme folder as a way to drop arbitrary files into the
    stories directory.

    **The book's own settings come back on a fresh restore (F51).** They
    are family content, not operational state — the book's name, whose
    childhood it is, who writes in it — and the Settings page says in so
    many words that they travel with the backup. Restored the way a person
    or a theme is: only when this book has none of its own, so a zip can
    never overwrite a live title with an older one. Read through
    `settings.KEYS` rather than extracted verbatim, for the same reason a
    theme folder is: a zip may only put back shapes this app writes.

    **Credentials never come back.** `CREDENTIAL_FILENAMES` are dropped from
    a person's folder on the way in. A zip is a portable file: restoring one
    from another book would otherwise silently install its accounts —
    including its admins — into this one. Losing logins on a restore is an
    inconvenience an admin can fix with an invite; gaining someone else's is
    not.
    """
    stories_dir = Path(stories_dir)
    people_root = storage.people_dir(stories_dir)

    with zipfile.ZipFile(zip_file) as zf:
        members = []
        story_ids = set()
        person_members = []
        theme_members = []
        settings_member = None
        for info in zf.infolist():
            name = info.filename
            if name.endswith("/"):
                continue
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError(f"Unsafe path in backup: {name!r}")
            parts = Path(name).parts
            top = parts[0] if parts else ""
            if top == storage.PEOPLE_DIRNAME:
                # people/<slug>/<file>; anything else under people/ is a
                # shape this app never writes, so it isn't restored.
                if len(parts) < 3 or not storage.is_valid_story_id(parts[1]):
                    continue
                if Path(name).name in CREDENTIAL_FILENAMES:
                    continue
                if (people_root / parts[1]).exists():
                    continue
                person_members.append(info)
                continue
            if top == USER_THEMES_DIRNAME:
                # themes/<pack>/theme.json, or themes/<pack>/img/<picture>.
                if len(parts) < 3 or not storage.is_valid_story_id(parts[1]):
                    continue
                if (stories_dir / USER_THEMES_DIRNAME / parts[1]).exists():
                    continue
                if parts[2:] == ("theme.json",) or (
                    len(parts) == 4 and parts[2] == "img" and parts[3] in BY_FILENAME
                ):
                    theme_members.append(info)
                continue
            if len(parts) == 1 and top == settings.SETTINGS_FILENAME:
                settings_member = info
                continue
            if not storage.is_valid_story_id(top):
                continue
            story_ids.add(top)
            members.append(info)

        if not members:
            raise ValueError("Backup contains no stories.")

        colliding = sorted(sid for sid in story_ids if (stories_dir / sid).exists())
        if colliding:
            raise ImportCollision(colliding)

        for info in members + person_members + theme_members:
            zf.extract(info, stories_dir)

        # After the extraction, and only into a book that has none of its
        # own: an install that has already been configured keeps what it
        # is doing, exactly as it keeps its own people and themes.
        if settings_member and not settings.settings_path(stories_dir).is_file():
            _restore_settings(zf, settings_member, stories_dir)

    return len(story_ids)


def _restore_settings(zf, info, stories_dir) -> None:
    """The settings out of a backup, filtered to the keys this app writes.

    Never raises: a zip whose `settings.json` is unreadable costs the
    restored settings and not the restore. Losing a title on the way back
    from a dead server would be a nuisance; losing the stories would be
    the thing this app exists to prevent.
    """
    try:
        data = json.loads(zf.read(info).decode("utf-8"))
    except (OSError, ValueError, KeyError, UnicodeDecodeError):
        return
    if not isinstance(data, dict):
        return
    kept = {key: data[key] for key in settings.KEYS if key in data}
    if kept:
        settings.save(stories_dir, kept)


# --- When this book was last backed up (FEATURES.md F58) --------------------

#: Root-level sidecar recording the last complete backup. Here rather than
#: in `settings.py` because it is not a setting: nobody chooses it, and it
#: is written by the act of taking a backup. Here rather than in
#: `timeline.py` because that file touches no filesystem, and here rather
#: than in `storage.py` because it is not a story folder — the rule
#: CLAUDE.md states for exactly this decision.
BACKUP_MARKER_FILENAME = "last_backup.json"


def record_backup(stories_dir, when: Optional[date] = None) -> None:
    """Remember that a complete backup was taken today (FEATURES.md F58).

    Called by `/export` only when the person downloading could take a
    *whole* one. A family member's partial zip is a real backup of what
    they can see and no use at all as the book's copy of record, so it
    must not quiet the nudge for everyone else.

    A date, not a timestamp: the nudge counts whole months, so an hour of
    precision would be stored and never read, and a plain `YYYY-MM-DD` is
    what someone opening this file by hand would hope to find.
    """
    if when is None:
        when = date.today()
    write_json(Path(stories_dir) / BACKUP_MARKER_FILENAME, {"at": when.isoformat()})


def last_backup(stories_dir) -> Optional[date]:
    """The date of the last complete backup, or None if there has never
    been one — which is also what a missing, unreadable or malformed
    marker returns.

    Tolerant on purpose. This file exists to prompt a kindness, and the
    worst a corrupt one should ever do is prompt it again; refusing to
    render the timeline over it would be absurd.
    """
    path = Path(stories_dir) / BACKUP_MARKER_FILENAME
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return date.fromisoformat(data["at"])
    except (OSError, ValueError, TypeError, KeyError):
        return None
