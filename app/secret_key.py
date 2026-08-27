"""The session-signing key, kept in the data folder when nobody supplied
one (FEATURES.md F59).

`STORYBOOK_SECRET_KEY` used to be mandatory the moment `STORYBOOK_PASSWORD`
was set: the app refused to start without it, pointing at a `python -c`
one-liner. That refusal was right about the danger and wrong about who was
standing in front of it. The person following the Docker instructions is
being asked, in the middle of an install, to understand what a signing key
is, why it differs from the password they just chose, and why
`change-this-to-a-long-random-string` is not itself a long random string.
The predictable answer is a key that is neither long nor random, and
nothing anywhere tells them so — a weak key silently weakens every session
cookie the app will ever sign.

So the app generates one instead, 32 bytes from `secrets`, and keeps it in
the stories directory — the only place a container is guaranteed to have a
volume mounted, and the folder a family already knows to back up.

Three properties this file is responsible for, none of them optional:

- **The environment still wins.** A key given in `STORYBOOK_SECRET_KEY` is
  used and this file is never written. It is machine configuration, and
  the machine's answer is the answer; this is the fallback for when there
  isn't one.
- **`O_EXCL`, not "check then write".** Two workers can start at once
  (waitress, gunicorn, a container restarting into a running one). Whoever
  creates the file wins and the loser reads what the winner wrote, so the
  two never sign cookies with different keys and log each other's readers
  out.
- **Mode 0600 at creation**, in the open flags rather than a later
  `chmod`, so the key is never briefly world-readable on a NAS where the
  stories folder is shared.

It never travels in a backup: see `backup.NEVER_EXPORTED`.
"""

import os
import secrets
from pathlib import Path
from typing import Optional

#: The key file, in the stories directory beside `settings.json` and
#: `groups.json`. Underscored, which `storage.STORY_ID_RE` cannot match, so
#: an import can never mistake it for a story folder — belt to
#: `backup.import_backup`'s braces, not a substitute for them.
SECRET_KEY_FILENAME = "secret_key"


def load_or_create(stories_dir) -> Optional[str]:
    """The persisted session key, generating and storing one on first run.

    Returns None if the key can neither be read nor written — a read-only
    or missing data folder, most likely a volume that wasn't mounted. The
    caller refuses to start on None rather than falling back to an
    in-memory key: a key that changes on every restart logs the whole
    family out every time the container is updated, and would do it
    silently.
    """
    path = Path(stories_dir) / SECRET_KEY_FILENAME
    existing = _read(path)
    if existing:
        return existing

    key = secrets.token_hex(32)
    try:
        Path(stories_dir).mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(key + "\n")
        return key
    except FileExistsError:
        # Another worker created it between the read above and here. Its
        # key is the book's key now.
        return _read(path)
    except OSError:
        return None


def _read(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8").strip() or None
    except OSError:
        return None
