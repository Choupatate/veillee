"""The `pages` blueprint and the view helpers every page route shares.

Split out of `routes_pages.py`, which had grown three jobs: it defined the
blueprint, it held the helpers its five sibling route files import, *and*
it implemented the timeline/story/book/export pages. The third job is what
made the other two awkward — every sibling had to import the module that
imported them, so the routes got registered by a side-effect import at the
bottom of `routes_pages.py`, and `routes_api.py` had to reach for
`viewer_scope` from inside a function body to stay out of the cycle.

Nothing imports `routes_pages` now. Every route file imports *this*, this
imports none of them, and `create_app` pulls them all in for their
registration side effect. The cycle is gone.

The helpers lost their leading underscores in the move. Five modules were
importing `_visible_stories`, `_people_dir`, `_serve_media`, `_person_ref`
and `_other_people_refs` across a module boundary already; the underscore
was claiming "private" about names that plainly were not. `_people_dir`
became `current_people_dir` rather than `people_dir` — half the functions
here already have a local of that name and one takes it as a parameter.

**Three of these are the audience gate** (FEATURES.md F40).
`visible_stories` and `get_story_or_404` are the only sanctioned ways a
page route reaches a story, and `viewer_scope` is what both are built on.
`tests/test_groups.py::test_no_route_file_reaches_stories_unscoped` counts
the unscoped alternatives in every route file *and in this one*, so moving
them here did not move them out from under the ratchet.
"""

from flask import (
    Blueprint,
    abort,
    current_app,
    g,
    send_from_directory,
    session,
    url_for,
)

from . import accounts, groups, people, settings, storage


bp = Blueprint("pages", __name__)

# Re-encoded photos (storage.save_image_to always writes .jpg or .png) are
# never overwritten or reused under a different number, so they're safe to
# cache for a long time. Voice memos are excluded: delete_memo can free up a
# number that a later upload then reuses for different audio, so their
# filename isn't a stable cache key.
_LONG_CACHE_EXTENSIONS = {"jpg", "png"}
_LONG_CACHE_MAX_AGE = 31536000  # 1 year


def _media_max_age(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return _LONG_CACHE_MAX_AGE if ext in _LONG_CACHE_EXTENSIONS else None


def _unambiguous_author_name(people_dir, person):
    """The viewer's display name, or None if some other Person shares it.

    `can_see`'s author rail matches on the author *name* a story carries
    (F1 stores a name, not a slug), so two People called "Maman" would see
    each other's scoped stories. Reaching that state takes an admin
    approving a second Person with a name already in the book — which is
    what F39's duplicate hints exist to flag — but "unlikely" is not
    "prevented", and this is an access-control comparison.

    So an ambiguous name simply doesn't get the rail. Compared casefolded,
    which is deliberately broader than the exact match it guards: erring
    towards withholding the rail costs a safety net, while erring the other
    way costs a private story. The real owner still reads their story
    through the group like everyone else, and an admin renaming one of the
    two Persons restores the rail for both.
    """
    if person is None:
        return None
    target = person.name.casefold().strip()
    for other in people.list_people(people_dir):
        if other.slug != person.slug and other.name.casefold().strip() == target:
            return None
    return person.name


def viewer_scope():
    """`(group_slugs, author_name)` for whoever is asking — the viewer half
    of `groups.can_see` (FEATURES.md F40).

    `(None, None)` means "scoping does not apply here": with
    STORYBOOK_ACCOUNTS off there is one shared password and therefore one
    identity, so there is nobody to scope a story *away from* and the whole
    feature is inert. Callers below treat a None group set as "sees
    everything" rather than "sees nothing" — the safe direction for a
    single-password install, where every existing story must keep showing.

    Nothing here reads the request. The group set comes from the session's
    Person and `groups.json` on disk, so there is no field a client could
    set to claim membership (FEATURES.md F41) — and it is recomputed per
    request rather than cached in the session, which is what makes adding
    and removing someone take effect immediately.

    Memoized on `g` for the duration of one request: `story_media` reaches
    this through `get_story_or_404` for every single photo on a page, and
    it now walks the people list.
    """
    if not current_app.config["ACCOUNTS_ENABLED"]:
        return None, None
    if "viewer_scope" not in g.__dict__:
        person_slug = session.get("person_slug")
        people_dir = current_people_dir()
        person = people.get_person(people_dir, person_slug) if person_slug else None
        g.viewer_scope = (
            groups.groups_for_person(current_app.config["STORIES_DIR"], person_slug),
            _unambiguous_author_name(people_dir, person),
        )
    return g.viewer_scope


def visible_stories():
    """Every story the current viewer may see, in `list_stories` order.

    **The only way a page route should reach the story list.** Calling
    `storage.list_stories` directly from a route is how a scoped story
    leaks, and `tests/test_groups.py` walks the route files to make sure
    nothing does.
    """
    all_stories = storage.list_stories(current_app.config["STORIES_DIR"])
    viewer_groups, author_name = viewer_scope()
    if viewer_groups is None:
        return all_stories
    return groups.visible_stories(all_stories, viewer_groups, author_name)


def available_groups(story=None):
    """The groups the audience picker offers (FEATURES.md F40 Phase 2).

    Empty outside accounts mode, which makes the picker disappear entirely
    rather than offering a choice that couldn't mean anything — the same
    way F1's author chips vanish without STORYBOOK_AUTHORS.

    Every group is offered, not just the writer's own: scoping a story to a
    group you aren't in is legitimate (writing something for the
    grandparents), and `can_see` keeps the author's own access either way.

    A story may also name a group this install doesn't have — restore a
    backup into a fresh book and the stories come back while `groups.json`
    doesn't. Those orphaned slugs get a chip of their own, labelled with
    the raw slug, so the editor round-trips them. Without it the picker
    shows nothing lit, an ordinary save sends an empty audience, and a
    story that was private quietly becomes public on the next edit — the
    one failure this whole feature exists to prevent.
    """
    if not current_app.config["ACCOUNTS_ENABLED"]:
        return []
    all_groups = groups.list_groups(current_app.config["STORIES_DIR"])
    if story is None:
        return all_groups
    known = {g.slug for g in all_groups}
    orphans = [s for s in (story.audience or []) if s not in known]
    return all_groups + [groups.Group(slug=s, name=s, members=[]) for s in orphans]


def visible_page_stories():
    """`storage.readable_page_stories` narrowed to what the viewer may see
    — the candidate set for anything that turns pages (F15 random, F2
    reading order). Without the gate here the page-turn arrows and the
    random button would both hand out the titles of scoped stories."""
    return [s for s in storage.readable_stories(visible_stories()) if s.kind == "story"]


def get_story_or_404(stories_dir, story_id):
    """A single story by id, 404 if it doesn't exist *or* the viewer isn't
    in its audience — deliberately the same 404 either way, so a scoped
    story's existence isn't discoverable by URL (the app's existing
    pattern: `admin_required` 404s a non-admin rather than 403ing)."""
    s = storage.get_story(stories_dir, story_id)
    if s is None:
        abort(404)
    viewer_groups, author_name = viewer_scope()
    if viewer_groups is not None and not groups.can_see(s, viewer_groups, author_name):
        abort(404)
    return s


def serve_media(root_dir, id_value, filename):
    """Validate `id_value`/`filename`, then serve `filename` from
    `root_dir/id_value` — the shared story_media/person_media pattern
    (CLAUDE.md: validate, then check existence, then serve). Falls back to
    the full-size photo when a `.thumb.` filename doesn't exist on disk yet
    (photos uploaded before thumbnails existed)."""
    if not storage.is_valid_story_id(id_value) or not storage.is_valid_filename(filename):
        abort(404)
    media_dir = root_dir / id_value
    if not (media_dir / filename).is_file():
        fallback = storage.original_filename_from_thumb(filename)
        if not fallback or not (media_dir / fallback).is_file():
            abort(404)
        filename = fallback
    return send_from_directory(media_dir, filename, max_age=_media_max_age(filename))


# Fallback color for an account-mode author who hasn't picked their own
# yet (person.author_color unset) — every entry authors_and_colors hands
# to timeline.html's legend/dots needs a real value, since that template
# (shared with F1) renders `--author-color: {{ a.color }}` unconditionally
# for legend chips, unlike the per-story byline lookups which already
# guard on the color being present.
DEFAULT_AUTHOR_COLOR = "#9c8a6a"


def authors_and_colors():
    """The (authors, author_colors) pair every timeline/book/story render
    needs for bylines and the legend. Two sources depending on mode
    (FEATURES.md F19 Phase 4): in accounts mode, every Person with a bound
    account — real identity, not config; otherwise the original
    STORYBOOK_AUTHORS list, untouched."""
    if current_app.config["ACCOUNTS_ENABLED"]:
        people_dir = storage.people_dir(current_app.config["STORIES_DIR"])
        people_by_slug = {p.slug: p for p in people.list_people(people_dir)}
        authors = []
        for account in accounts.list_accounts(people_dir):
            person = people_by_slug.get(account.person_slug)
            if person:
                authors.append(
                    {"name": person.name, "color": person.author_color or DEFAULT_AUTHOR_COLOR}
                )
    else:
        authors = settings.book("AUTHORS") or []
    author_colors = {a["name"]: a["color"] for a in authors}
    return authors, author_colors


def color_for_author(authors, author_colors, name):
    return author_colors.get(name) if (authors and name) else None


def current_people_dir():
    return storage.people_dir(current_app.config["STORIES_DIR"])


def person_ref(people_by_slug, slug):
    """A lightweight {slug, name, photo_url, photo_sepia} dict for linking
    to another person in a template — None when the slug isn't a real
    person."""
    p = people_by_slug.get(slug)
    if p is None:
        return None
    photo_url = (
        url_for("pages.person_media", slug=p.slug, filename=storage.thumb_filename(p.photo))
        if p.photo else None
    )
    return {"slug": p.slug, "name": p.name, "photo_url": photo_url, "photo_sepia": p.photo_sepia}


def other_people_refs(exclude_slug=None):
    all_people = people.list_people(current_people_dir())
    people_by_slug = {p.slug: p for p in all_people}
    return [
        person_ref(people_by_slug, p.slug) for p in all_people if p.slug != exclude_slug
    ]

