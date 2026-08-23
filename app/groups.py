"""Audience groups (FEATURES.md F40): a named handful of people a story can
be scoped to, so that "just us four" is something you can write down rather
than something you decide not to record at all.

One file at the stories root, `stories/groups.json`, not a key on each
Person's `index.md`: a group is a thing in its own right, with a name and
an identity, not a property of a person. Membership edits stay one atomic
write, and the file reads as a list of groups when someone opens it in a
text editor years from now — which is the actual test this app's storage
decisions are held to.

Members are **person slugs**, not usernames. An account is a login bolted
onto a Person (F19) and the Person is this app's identity, so a member who
has no account yet simply can't log in to use their membership; giving
them one later needs no change here.

Anyone in the family can make a group (F41), and the people in a group are
the ones who can change it — see `can_manage`. That gate is load-bearing
rather than tidy-minded: if any logged-in person could edit any group,
anyone could add themselves to "Just us" and read it, and a group would
protect nothing at all.

`can_see` is the whole point of the module and is deliberately pure — no
Flask, no filesystem, no session — so the rule that decides who reads what
can be tested exhaustively in isolation. Everything that reaches a story
in the web layer goes through it.
"""

import json
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import jsonstore, storage

logger = logging.getLogger(__name__)

GROUPS_FILENAME = "groups.json"
MAX_GROUP_NAME_LENGTH = 60

# Every group is a chip in the editor's audience row, on a phone, above the
# keyboard. Past a couple of dozen that row stops being a choice you can
# make at a glance, which is when someone starts tapping the wrong one.
MAX_GROUPS = 40


class GroupError(ValueError):
    """A rule violation with a message the interface can translate.

    The message stays an uninterpolated template — a literal catalog key —
    and its values ride alongside in `params`, so the route can hand both
    to `_()`. An f-string baked in here would arrive at the catalog already
    interpolated and never match anything, quietly pinning every one of
    these to English.

    Subclasses ValueError, so `except ValueError` still catches it.
    """

    def __init__(self, message: str, **params):
        super().__init__(message.format(**params) if params else message)
        self.message = message
        self.params = params


@dataclass
class Group:
    slug: str
    name: str
    members: list  # person slugs
    created_at: Optional[datetime] = None
    created_by: Optional[str] = None  # person slug; None for pre-F41 groups

    def __post_init__(self):
        if self.members is None:
            self.members = []


def _groups_path(stories_dir) -> Path:
    return Path(stories_dir) / GROUPS_FILENAME


def _group_from_dict(data: dict) -> Optional[Group]:
    slug = data.get("slug")
    name = data.get("name")
    if not isinstance(slug, str) or not storage.is_valid_story_id(slug):
        return None
    if not isinstance(name, str) or not name.strip():
        return None
    created_at = data.get("created_at")
    if isinstance(created_at, str):
        try:
            created_at = datetime.fromisoformat(created_at)
        except ValueError:
            created_at = None
    else:
        created_at = None
    created_by = data.get("created_by")
    if not isinstance(created_by, str) or not created_by.strip():
        created_by = None
    return Group(
        slug=slug,
        name=name.strip()[:MAX_GROUP_NAME_LENGTH],
        members=storage.parse_string_list(data.get("members")),
        created_at=created_at,
        created_by=created_by,
    )


def list_groups(stories_dir) -> list[Group]:
    """Every group, oldest first. Tolerant of a missing/malformed file and
    of individual malformed entries — same philosophy as list_stories, a
    bad line loses one group rather than the whole page."""
    path = _groups_path(stories_dir)
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logger.warning("Failed to load %s", GROUPS_FILENAME, exc_info=True)
        return []
    if not isinstance(data, list):
        return []
    result = [g for g in (_group_from_dict(d) for d in data if isinstance(d, dict)) if g]
    result.sort(key=lambda g: g.created_at or datetime.min)
    return result


def _write_groups(stories_dir, all_groups: list[Group]) -> None:
    path = _groups_path(stories_dir)
    data = [
        {
            "slug": g.slug,
            "name": g.name,
            "members": g.members,
            "created_at": (g.created_at or datetime.now()).isoformat(),
            "created_by": g.created_by,
        }
        for g in all_groups
    ]
    jsonstore.write_json(path, data)


def get_group(stories_dir, slug: str) -> Optional[Group]:
    for group in list_groups(stories_dir):
        if group.slug == slug:
            return group
    return None


def clean_members(stories_dir, members) -> list:
    """The member slugs, de-duplicated and order-preserved, with every one
    checked against a real Person. Unknown slugs are rejected rather than
    dropped: a member who silently isn't there is one who can't read what
    they were meant to, and nothing on screen would say so."""
    people_dir = storage.people_dir(stories_dir)
    cleaned = []
    for person_slug in storage.parse_string_list(members):
        if person_slug in cleaned:
            continue
        if not storage.is_valid_story_id(person_slug) or not (people_dir / person_slug).is_dir():
            raise GroupError("Unknown person: {person}.", person=person_slug)
        cleaned.append(person_slug)
    return cleaned


def scope_twin(all_groups: list, members, exclude_slug: Optional[str] = None) -> Optional[Group]:
    """An existing group covering exactly the same people, if any.

    Two groups with identical membership are the same circle under two
    names, and that is worse than redundant: a story kept to one of them
    looks protected from people who can in fact read it through the other,
    and widening one leaves the other silently behind. So it's refused
    rather than merely discouraged.

    Fewer than two people never counts as a twin. An empty group is a state
    on the way to being filled in, not a scope; and a group of one is a note
    to a single person, where a second name for the same one person misleads
    nobody. Counting those as twins would also make the rule fight the app:
    making a group puts you in it, so your first group is {you}, and it would
    collide with any existing group that happened to be {you} — refusing a
    group at the moment someone types its name, for a membership they never
    chose.
    """
    wanted = set(members)
    if len(wanted) < 2:
        return None
    for group in all_groups:
        if group.slug != exclude_slug and set(group.members) == wanted:
            return group
    return None


def create_group(
    stories_dir,
    name: str,
    members: Optional[list] = None,
    created_by: Optional[str] = None,
) -> Group:
    """Create a group, deriving its slug from the name the same way story
    ids are derived from titles.

    Raises GroupError for a blank name, a name colliding with an existing
    group, a membership another group already covers exactly, or one group
    too many.
    """
    name = (name or "").strip()[:MAX_GROUP_NAME_LENGTH]
    if not name:
        raise GroupError("Give the group a name.")
    slug = storage.slugify(name)
    all_groups = list_groups(stories_dir)
    if any(g.slug == slug for g in all_groups):
        raise GroupError("There is already a group called {name}.", name=name)
    if len(all_groups) >= MAX_GROUPS:
        raise GroupError(
            "There are already {n} groups, which is as many as this book keeps. "
            "Rename or reuse one instead.",
            n=MAX_GROUPS,
        )
    members = clean_members(stories_dir, members or [])
    # Whoever makes a group is in it. Editing rights follow membership
    # (`can_manage`), so a creator left outside would be locked out of the
    # group they just made, with nothing on screen explaining why.
    if created_by and created_by not in members:
        members = clean_members(stories_dir, [created_by]) + members
    twin = scope_twin(all_groups, members)
    if twin is not None:
        raise GroupError(
            "{other} already covers exactly these people. Use that group, or "
            "choose a different set of people for this one.",
            other=twin.name,
        )

    group = Group(
        slug=slug,
        name=name,
        members=members,
        created_at=datetime.now(),
        created_by=created_by or None,
    )
    all_groups.append(group)
    _write_groups(stories_dir, all_groups)
    return group


def rename_group(stories_dir, slug: str, name: str) -> None:
    """Change a group's display name. The slug never changes — stories
    reference it by slug, and rewriting every story's frontmatter to track
    a rename is exactly the kind of cascading write this app avoids.

    A rename is therefore always safe: no story's audience moves, and
    nobody's access changes. It's the one edit here with no consequences,
    which is why it needs no confirmation."""
    name = (name or "").strip()[:MAX_GROUP_NAME_LENGTH]
    if not name:
        raise GroupError("Give the group a name.")
    all_groups = list_groups(stories_dir)
    match = next((g for g in all_groups if g.slug == slug), None)
    if match is None:
        raise FileNotFoundError(slug)
    if any(g.slug != slug and g.name.casefold() == name.casefold() for g in all_groups):
        raise GroupError("There is already a group called {name}.", name=name)
    match.name = name
    _write_groups(stories_dir, all_groups)


def set_members(stories_dir, slug: str, members: list) -> None:
    """Replace a group's membership wholesale. Unknown person slugs are
    rejected rather than stored — a typo'd member is one who silently
    can't read what they were meant to — and so is a membership that some
    other group already covers exactly (see `scope_twin`)."""
    all_groups = list_groups(stories_dir)
    match = next((g for g in all_groups if g.slug == slug), None)
    if match is None:
        raise FileNotFoundError(slug)
    cleaned = clean_members(stories_dir, members)
    twin = scope_twin(all_groups, cleaned, exclude_slug=slug)
    if twin is not None:
        raise GroupError(
            "{other} already covers exactly these people. Use that group, or "
            "choose a different set of people for this one.",
            other=twin.name,
        )
    match.members = cleaned
    _write_groups(stories_dir, all_groups)


def can_manage(group: Group, person_slug: Optional[str], is_admin: bool = False) -> bool:
    """Whether this viewer may rename `group` or change who's in it: the
    people in it, or an admin.

    A circle maintains itself — the people already inside are the ones who
    decide who else comes in, the way it works when a family actually
    talks. `created_by` is recorded for provenance but grants nothing on
    its own, which is why `create_group` puts its creator in the group:
    otherwise you could make one and immediately be unable to touch it.

    The cost, accepted deliberately: any member can widen the group, and
    that republishes stories other people kept to it. The group page says
    so out loud rather than pretending otherwise, and nobody outside the
    circle can do it.
    """
    if is_admin:
        return True
    return bool(person_slug) and person_slug in group.members


def groups_for_person(stories_dir, person_slug: Optional[str]) -> set:
    """The slugs of every group this Person belongs to — the viewer half
    of `can_see`. An empty set for None (no person bound to the session)."""
    if not person_slug:
        return set()
    return {g.slug for g in list_groups(stories_dir) if person_slug in g.members}


# ---------------------------------------------------------------------------
# The rule itself. Pure — no Flask, no filesystem — so it can be tested
# exhaustively without a request context, and so there is exactly one
# statement anywhere in the app of who may read what.
# ---------------------------------------------------------------------------


def can_see(story, viewer_groups, viewer_author_name: Optional[str] = None) -> bool:
    """Whether a viewer may read `story`.

    - A story with no `audience` is visible to everyone. This is the
      default and stays the default: scoping is opt-in per story.
    - Otherwise the viewer must belong to at least one listed group. Union,
      not intersection — "close family and the godparents" is a real thing
      to want.
    - The author always sees their own story, even if they scoped it to a
      group they aren't in. That's a safety rail against a mis-tap in the
      editor making a story vanish from the person who wrote it,
      recoverable otherwise only by hand-editing frontmatter.

    Note what is deliberately *not* here: any notion of role. An admin is
    not exempt (F40) — membership governs reading, role governs managing.
    An admin can always add themselves to a group and then read, but that
    is a visible, recorded act rather than an invisible capability.
    """
    audience = getattr(story, "audience", None) or []
    if not audience:
        return True
    if viewer_author_name and story.author and story.author == viewer_author_name:
        return True
    return any(slug in viewer_groups for slug in audience)


def visible_stories(stories: list, viewer_groups, viewer_author_name: Optional[str] = None) -> list:
    """`can_see` over a list, preserving order."""
    return [s for s in stories if can_see(s, viewer_groups, viewer_author_name)]
