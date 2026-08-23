"""Account invites (FEATURES.md F39): an admin picks a Person and a role,
hands out a one-off link, and the recipient chooses their own username and
password. The opposite direction from `accounts.py`'s pending queue — there
the stranger proposes and the admin disposes; here the admin decides first
and the link only lets someone fill in credentials for a seat already set
aside for them.

Stored per person, a sibling of account.json and write_links.json:
`people/<slug>/invites.json`. Pure functions taking the people directory as
their first argument, same shape as the rest of this app.

Deliberately close to `write_links.py` in mechanism (a
`secrets.token_urlsafe` bearer token, only its SHA-256 hash persisted, with
an expiry and a revoke flag) and deliberately unlike it in consequence: a
write-link grants one story and never an identity, an invite grants a real
login and nothing else. They are separate files rather than one shared
"token" module because the two lifecycles diverge everywhere that matters —
an invite is always single-use, always bound to a role, and dies the moment
its Person has an account by any other route.

The same fast-hash reasoning as write_links.py applies to the token here:
~192 bits of entropy from `secrets` needs a hash that isn't reversible, not
one that resists brute force on a weak human-chosen input.
"""

import hashlib
import json
import logging
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from . import accounts, jsonstore, storage

logger = logging.getLogger(__name__)

INVITES_FILENAME = "invites.json"
TOKEN_BYTES = 32
DEFAULT_EXPIRY_DAYS = 14


@dataclass
class Invite:
    id: str  # non-secret identifier for revoke URLs — never the token itself
    person_slug: str
    token_hash: str
    role: str
    created_at: Optional[datetime]
    created_by: Optional[str]
    expires_at: Optional[datetime]
    accepted_at: Optional[datetime]
    revoked: bool


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def _invites_path(people_dir, person_slug: str) -> Path:
    return Path(people_dir) / person_slug / INVITES_FILENAME


def _parse_dt(value) -> Optional[datetime]:
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


def _invite_from_dict(person_slug: str, data: dict) -> Invite:
    return Invite(
        id=data.get("id"),
        person_slug=person_slug,
        token_hash=data.get("token_hash"),
        role=data.get("role"),
        created_at=_parse_dt(data.get("created_at")),
        created_by=data.get("created_by"),
        expires_at=_parse_dt(data.get("expires_at")),
        accepted_at=_parse_dt(data.get("accepted_at")),
        revoked=bool(data.get("revoked", False)),
    )


def list_invites(people_dir, person_slug: str) -> list[Invite]:
    """Every invite ever issued for this person, newest first — including
    accepted/expired/revoked ones, so the record of how an account came to
    exist survives. Tolerant of a missing/malformed file, same as
    account.json."""
    path = _invites_path(people_dir, person_slug)
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logger.warning("Failed to load %s for %s", INVITES_FILENAME, person_slug, exc_info=True)
        return []
    invites = [_invite_from_dict(person_slug, d) for d in data]
    invites.sort(key=lambda i: i.created_at or datetime.min, reverse=True)
    return invites


def _write_invites(people_dir, person_slug: str, invites: list[Invite]) -> None:
    path = _invites_path(people_dir, person_slug)
    data = [
        {
            "id": invite.id,
            "token_hash": invite.token_hash,
            "role": invite.role,
            "created_at": (invite.created_at or datetime.now()).isoformat(),
            "created_by": invite.created_by,
            "expires_at": invite.expires_at.isoformat() if invite.expires_at else None,
            "accepted_at": invite.accepted_at.isoformat() if invite.accepted_at else None,
            "revoked": invite.revoked,
        }
        for invite in invites
    ]
    jsonstore.write_json(path, data)


def get_invite(people_dir, person_slug: str, invite_id: str) -> Optional[Invite]:
    for invite in list_invites(people_dir, person_slug):
        if invite.id == invite_id:
            return invite
    return None


def is_invite_valid(invite: Invite) -> bool:
    """False once revoked, accepted, or past its expiry — the three ways an
    invite stops working. Always single-use: an invite buys exactly one
    account, and `accept_invite` refuses a second one anyway."""
    if invite.revoked or invite.accepted_at:
        return False
    if invite.expires_at and datetime.now() > invite.expires_at:
        return False
    return True


def create_invite(
    people_dir, person_slug: str, role: str,
    expires_in_days: Optional[int] = DEFAULT_EXPIRY_DAYS,
    created_by: Optional[str] = None,
) -> tuple[Invite, str]:
    """Set a seat aside for an existing Person. Returns (invite, raw_token)
    — the raw token exists only here, at creation time; only its hash is
    persisted, so it can never be shown or recovered again.

    Any still-valid invite for the same Person is revoked first: an admin
    re-issuing a link (the recipient lost it, it went to the wrong chat)
    should end up with one live token, not two, since only one of them
    could ever be redeemed anyway.

    Raises FileNotFoundError for an unknown person, ValueError for a bad
    role or a Person who already has an account.
    """
    people_dir = Path(people_dir)
    if role not in accounts.ROLES:
        raise ValueError(f"Invalid role: {role!r}")
    if not (people_dir / person_slug).is_dir():
        raise FileNotFoundError(person_slug)
    if accounts.get_account(people_dir, person_slug) is not None:
        raise ValueError(f"{person_slug} already has an account.")

    token = secrets.token_urlsafe(TOKEN_BYTES)
    invite = Invite(
        id=secrets.token_hex(8),
        person_slug=person_slug,
        token_hash=_hash_token(token),
        role=role,
        created_at=datetime.now(),
        created_by=created_by,
        expires_at=(datetime.now() + timedelta(days=expires_in_days)) if expires_in_days else None,
        accepted_at=None,
        revoked=False,
    )
    invites = list_invites(people_dir, person_slug)
    for existing in invites:
        if is_invite_valid(existing):
            existing.revoked = True
    invites.append(invite)
    _write_invites(people_dir, person_slug, invites)
    return invite, token


def revoke_invite(people_dir, person_slug: str, invite_id: str) -> None:
    invites = list_invites(people_dir, person_slug)
    match = next((i for i in invites if i.id == invite_id), None)
    if match is None:
        raise FileNotFoundError(invite_id)
    match.revoked = True
    _write_invites(people_dir, person_slug, invites)


def _mark_accepted(people_dir, person_slug: str, invite_id: str) -> None:
    invites = list_invites(people_dir, person_slug)
    match = next((i for i in invites if i.id == invite_id), None)
    if match is None:
        raise FileNotFoundError(invite_id)
    match.accepted_at = datetime.now()
    _write_invites(people_dir, person_slug, invites)


def find_by_token(people_dir, token: str) -> Optional[Invite]:
    """Scan every person's invites.json for a token hash match — a small,
    bounded scan across a handful of family members, same cost class as
    accounts.get_account_by_username and write_links.find_by_token."""
    if not token:
        return None
    token_hash = _hash_token(token)
    people_dir = Path(people_dir)
    if not people_dir.is_dir():
        return None
    for entry in people_dir.iterdir():
        if not entry.is_dir() or not storage.is_valid_story_id(entry.name):
            continue
        for invite in list_invites(people_dir, entry.name):
            if invite.token_hash == token_hash:
                return invite
    return None


def list_all_active(people_dir) -> list[Invite]:
    """Every still-redeemable invite across every person, newest first —
    the admin dashboard's "who has a link out right now" view. Accepted,
    revoked and expired invites are omitted; they're not actionable."""
    people_dir = Path(people_dir)
    result = []
    if not people_dir.is_dir():
        return result
    for entry in people_dir.iterdir():
        if not entry.is_dir() or not storage.is_valid_story_id(entry.name):
            continue
        for invite in list_invites(people_dir, entry.name):
            if is_invite_valid(invite):
                result.append(invite)
    result.sort(key=lambda i: i.created_at or datetime.min, reverse=True)
    return result


def accept_invite(stories_dir, token: str, username: str, password: str) -> accounts.Account:
    """Redeem an invite: create the account it was issued for, with the
    username and password the recipient chose and the role the admin
    picked, then burn the invite.

    Every uniqueness rule the admin-driven paths enforce is re-checked here
    rather than trusted from creation time, because an invite can sit
    unredeemed for days while the world changes underneath it: the Person
    may have been given an account by another route, and the username may
    have been claimed by an account or by a request still in the pending
    queue.

    Raises LookupError for a token that isn't valid (unknown, revoked,
    expired, already accepted) — distinct from ValueError, which here always
    means "the form is wrong", something the caller should re-prompt for
    rather than turn away.
    """
    people_dir = storage.people_dir(stories_dir)
    invite = find_by_token(people_dir, token)
    if invite is None or not is_invite_valid(invite):
        raise LookupError("invite")
    if accounts.get_account(people_dir, invite.person_slug) is not None:
        raise LookupError("invite")

    username = (username or "").strip().lower()
    if accounts.is_username_reserved(stories_dir, username):
        raise ValueError(f"Username already taken: {username!r}")

    account = accounts.create_account(
        people_dir, invite.person_slug, username, password, invite.role,
        approved_by=invite.created_by,
    )
    _mark_accepted(people_dir, invite.person_slug, invite.id)
    return account
