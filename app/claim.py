"""Claiming a fresh book, and the password it ends up with (FEATURES.md F60).

F59 took the signing key out of the environment because asking a family to
generate one by hand produced weak keys. The password is the same argument
one step further along: `STORYBOOK_PASSWORD=changeme` sits in
`.env.example`, and an install that never gets past copying the example
file is an install whose password is `changeme`.

So a book with no password in its environment starts **unclaimed**. It
serves one page — the claim page — and prints a one-time code to its own
logs:

    ┌─────────────────────────────────────────────┐
    │  This book is waiting to be claimed.        │
    │  Open it in a browser and enter this code:  │
    │                                             │
    │      K7QP-3MRW-92XD                         │
    └─────────────────────────────────────────────┘

Whoever types that code chooses the book's password and the book is
theirs. Nobody else can, because the code is only in the logs.

**Why a code at all**, when the alternative — first person to open the page
claims it — is simpler and is already how F19 treats the first account
request? Because F19's version happens on a book somebody is already
running, and this one happens on a book reachable at a domain name from
the moment the container starts. The window between "docker compose up"
and "opened the browser" is however long it takes someone to walk to
another room, and a book of photographs of a child is not something to
leave unlocked for that long on the open internet. Reading the machine's
own logs is proof of being the person who installed it, which is exactly
the thing being asserted.

The environment still wins, as it does for the signing key: with
`STORYBOOK_PASSWORD` set, none of this happens, no code is generated, and
an install that has been running for a year notices nothing at all.
"""

import hmac
import os
import secrets
from pathlib import Path
from typing import Optional

from werkzeug.security import check_password_hash, generate_password_hash

from .jsonstore import write_json

#: The one-time code, in the stories folder at mode 0600 beside the signing
#: key. Persisted rather than regenerated per start so that restarting the
#: container does not invalidate a code someone is halfway through typing,
#: and so two workers print the same one.
CLAIM_CODE_FILENAME = "claim_code"

#: The book's password, once chosen — a scrypt hash, never the password.
#: A credential file: `backup.CREDENTIAL_FILENAMES` keeps it out of a
#: non-admin's zip and out of every import, like `account.json`.
BOOK_PASSWORD_FILENAME = "book_password.json"

#: No I, O, 0 or 1 — the code is read off a terminal and typed into a
#: phone, and those four are the ones that get read wrong.
ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"

GROUPS, GROUP_SIZE = 3, 4

MIN_PASSWORD_LENGTH = 8


class ClaimError(ValueError):
    """The claim was refused.

    `reason` is `"code"` or `"password"`, and the caller decides both the
    wording and the consequence from it. Two things depend on telling them
    apart, and neither should be done by reading an error message: only a
    wrong code counts against the brute-force throttle (a short password is
    the person's own slip and costs them nothing), and the wording has to
    be translated, which a message carrying a baked-in number cannot be.
    """

    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def is_claimed(stories_dir) -> bool:
    return _stored_hash(stories_dir) is not None


def verify_password(stories_dir, password: str) -> bool:
    """Whether `password` is this book's, for a book claimed through the
    wizard rather than configured from the environment."""
    stored = _stored_hash(stories_dir)
    if not stored:
        return False
    return check_password_hash(stored, password or "")


def pending_code(stories_dir) -> Optional[str]:
    """The claim code for an unclaimed book, generating it on first call.

    None once the book is claimed — the code stops existing at that moment
    and there is no way to ask for another one, which is the point.

    Created with `O_EXCL` for the reason `secret_key.py` explains at
    length: two workers can start at once, and they must print the same
    code rather than each print their own.
    """
    if is_claimed(stories_dir):
        return None
    path = Path(stories_dir) / CLAIM_CODE_FILENAME
    existing = _read(path)
    if existing:
        return existing

    code = _generate()
    try:
        Path(stories_dir).mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(code + "\n")
        return code
    except FileExistsError:
        return _read(path)
    except OSError:
        return None


def claim(stories_dir, code: str, password: str) -> None:
    """Take ownership of an unclaimed book: check the code, set the
    password, and destroy the code.

    Raises ClaimError on a wrong code or a short password, and on a book
    that is already claimed — a claimed book has no code, so this is the
    same answer as a wrong one rather than a different error worth
    distinguishing to whoever is guessing.
    """
    expected = pending_code(stories_dir)
    if not expected or not hmac.compare_digest(normalize(code), expected):
        raise ClaimError("code")
    if len(password or "") < MIN_PASSWORD_LENGTH:
        raise ClaimError("password")
    write_json(
        Path(stories_dir) / BOOK_PASSWORD_FILENAME,
        {"hash": generate_password_hash(password)},
    )
    _forget_code(stories_dir)


def normalize(code: str) -> str:
    """A typed code as it is stored: upper case, no separators.

    Someone reading `K7QP-3MRW-92XD` off a terminal may type the dashes, or
    spaces, or neither, and a phone keyboard may capitalize the first
    letter and not the rest. None of that is a wrong code.
    """
    return "".join(ch for ch in (code or "").upper() if ch in ALPHABET)


def banner(code: str) -> str:
    """The block printed to the logs. A box because `docker compose up`
    scrolls, and this has to be findable afterwards."""
    lines = [
        "This book is waiting to be claimed.",
        "Open it in a browser and enter this code:",
        "",
        "    " + formatted(code),
    ]
    width = max(len(line) for line in lines) + 4
    out = ["", "┌" + "─" * width + "┐"]
    out += ["│  " + line.ljust(width - 2) + "│" for line in lines]
    out += ["└" + "─" * width + "┘", ""]
    return "\n".join(out)


def formatted(code: str) -> str:
    """`K7QP3MRW92XD` as `K7QP-3MRW-92XD`, for reading aloud and for typing."""
    return "-".join(
        code[i:i + GROUP_SIZE] for i in range(0, len(code), GROUP_SIZE)
    )


def _generate() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(GROUPS * GROUP_SIZE))


def _stored_hash(stories_dir) -> Optional[str]:
    import json

    try:
        data = json.loads(
            (Path(stories_dir) / BOOK_PASSWORD_FILENAME).read_text(encoding="utf-8")
        )
        value = data["hash"]
        return value if isinstance(value, str) and value else None
    except (OSError, ValueError, TypeError, KeyError):
        return None


def _read(path: Path) -> Optional[str]:
    try:
        return normalize(path.read_text(encoding="utf-8")) or None
    except OSError:
        return None


def _forget_code(stories_dir) -> None:
    try:
        (Path(stories_dir) / CLAIM_CODE_FILENAME).unlink()
    except OSError:
        pass
