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

`can_see` is the whole point of the module and is deliberately pure — no
Flask, no filesystem, no session — so the rule that decides who reads what
can be tested exhaustively in isolation. Everything that reaches a story
in the web layer goes through it.
"""

import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from . import storage

logger = logging.getLogger(__name__)

GROUPS_FILENAME = "groups.json"
MAX_GROUP_NAME_LENGTH = 60


@dataclass
class Group:
    slug: str
    name: str
    members: list  # person slugs
    created_at: Optional[datetime] = None

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
    return Group(
        slug=slug,
        name=name.strip()[:MAX_GROUP_NAME_LENGTH],
        members=storage.parse_string_list(data.get("members")),
        created_at=created_at,
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
        }
        for g in all_groups
    ]
    tmp_path = path.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp_path, path)


def get_group(stories_dir, slug: str) -> Optional[Group]:
    for group in list_groups(stories_dir):
        if group.slug == slug:
            return group
    return None


def create_group(stories_dir, name: str, members: Optional[list] = None) -> Group:
    """Create a group, deriving its slug from the name the same way story
    ids are derived from titles. Raises ValueError for a blank name or a
    name that collides with an existing group's slug."""
    name = (name or "").strip()[:MAX_GROUP_NAME_LENGTH]
    if not name:
        raise ValueError("Give the group a name.")
    slug = storage.slugify(name)
    all_groups = list_groups(stories_dir)
    if any(g.slug == slug for g in all_groups):
        raise ValueError(f"There is already a group called {name!r}.")

    group = Group(slug=slug, name=name, members=list(members or []), created_at=datetime.now())
    all_groups.append(group)
    _write_groups(stories_dir, all_groups)
    return group


def rename_group(stories_dir, slug: str, name: str) -> None:
    """Change a group's display name. The slug never changes — stories
    reference it by slug, and rewriting every story's frontmatter to track
    a rename is exactly the kind of cascading write this app avoids."""
    name = (name or "").strip()[:MAX_GROUP_NAME_LENGTH]
    if not name:
        raise ValueError("Give the group a name.")
    all_groups = list_groups(stories_dir)
    match = next((g for g in all_groups if g.slug == slug), None)
    if match is None:
        raise FileNotFoundError(slug)
    match.name = name
    _write_groups(stories_dir, all_groups)


def set_members(stories_dir, slug: str, members: list) -> None:
    """Replace a group's membership wholesale. Unknown person slugs are
    rejected rather than stored — a typo'd member is one who silently
    can't read what they were meant to."""
    all_groups = list_groups(stories_dir)
    match = next((g for g in all_groups if g.slug == slug), None)
    if match is None:
        raise FileNotFoundError(slug)
    people_dir = storage.people_dir(stories_dir)
    cleaned = []
    for person_slug in storage.parse_string_list(members):
        if not (people_dir / person_slug).is_dir():
            raise ValueError(f"Unknown person: {person_slug}.")
        cleaned.append(person_slug)
    match.members = cleaned
    _write_groups(stories_dir, all_groups)


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
