"""Core story-reading/writing page routes: timeline, story pages, the
editor, drafts/archived, the book view, and backup export/import.

People/genealogy routes live in `routes_people.py`; family-accounts and
delegated-write-link routes live in `routes_accounts.py` — both register
onto the `bp` object defined here rather than declaring their own
blueprint, so every `url_for("pages.xxx")` reference (in Python and in
templates) keeps working unchanged regardless of which file a route's
code actually lives in. They're imported at the bottom of this file
(after `bp` and the handful of helpers they need — `_people_dir`,
`_person_ref`, `_other_people_refs`, `_serve_media`, `DEFAULT_AUTHOR_COLOR`
— already exist) purely for that side effect: registering their routes.
"""

import random
import tempfile
import zipfile
from datetime import date, datetime

from flask import (
    Blueprint,
    abort,
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    session,
    url_for,
)

from . import epub, groups, i18n, life_events, people, prompts, storage
from .auth import admin_required_in_accounts_mode, login_required
from .rendering import render_markdown

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


def _viewer_scope():
    """`(group_slugs, author_name)` for whoever is asking — the viewer half
    of `groups.can_see` (FEATURES.md F40).

    `(None, None)` means "scoping does not apply here": with
    STORYBOOK_ACCOUNTS off there is one shared password and therefore one
    identity, so there is nobody to scope a story *away from* and the whole
    feature is inert. Callers below treat a None group set as "sees
    everything" rather than "sees nothing" — the safe direction for a
    single-password install, where every existing story must keep showing.
    """
    if not current_app.config["ACCOUNTS_ENABLED"]:
        return None, None
    person_slug = session.get("person_slug")
    viewer_groups = groups.groups_for_person(current_app.config["STORIES_DIR"], person_slug)
    person = people.get_person(_people_dir(), person_slug) if person_slug else None
    return viewer_groups, (person.name if person else None)


def _visible_stories():
    """Every story the current viewer may see, in `list_stories` order.

    **The only way a page route should reach the story list.** Calling
    `storage.list_stories` directly from a route is how a scoped story
    leaks, and `tests/test_groups.py` walks the route files to make sure
    nothing does.
    """
    all_stories = storage.list_stories(current_app.config["STORIES_DIR"])
    viewer_groups, author_name = _viewer_scope()
    if viewer_groups is None:
        return all_stories
    return groups.visible_stories(all_stories, viewer_groups, author_name)


def _available_groups(story=None):
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


def _visible_page_stories():
    """`storage.readable_page_stories` narrowed to what the viewer may see
    — the candidate set for anything that turns pages (F15 random, F2
    reading order). Without the gate here the page-turn arrows and the
    random button would both hand out the titles of scoped stories."""
    return [s for s in storage.readable_stories(_visible_stories()) if s.kind == "story"]


def _get_story_or_404(stories_dir, story_id):
    """A single story by id, 404 if it doesn't exist *or* the viewer isn't
    in its audience — deliberately the same 404 either way, so a scoped
    story's existence isn't discoverable by URL (the app's existing
    pattern: `admin_required` 404s a non-admin rather than 403ing)."""
    s = storage.get_story(stories_dir, story_id)
    if s is None:
        abort(404)
    viewer_groups, author_name = _viewer_scope()
    if viewer_groups is not None and not groups.can_see(s, viewer_groups, author_name):
        abort(404)
    return s


def _serve_media(root_dir, id_value, filename):
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
# yet (person.author_color unset) — every entry _authors_and_colors hands
# to timeline.html's legend/dots needs a real value, since that template
# (shared with F1) renders `--author-color: {{ a.color }}` unconditionally
# for legend chips, unlike the per-story byline lookups which already
# guard on the color being present.
DEFAULT_AUTHOR_COLOR = "#9c8a6a"


def _authors_and_colors():
    """The (authors, author_colors) pair every timeline/book/story render
    needs for bylines and the legend. Two sources depending on mode
    (FEATURES.md F19 Phase 4): in accounts mode, every Person with a bound
    account — real identity, not config; otherwise the original
    STORYBOOK_AUTHORS list, untouched."""
    if current_app.config["ACCOUNTS_ENABLED"]:
        # Imported locally to avoid a module-load-order dependency on
        # accounts.py from this core file — only accounts mode needs it.
        from . import accounts

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
        authors = current_app.config.get("AUTHORS") or []
    author_colors = {a["name"]: a["color"] for a in authors}
    return authors, author_colors


def _author_color(authors, author_colors, name):
    return author_colors.get(name) if (authors and name) else None


@bp.route("/")
@login_required
def timeline():
    all_stories = _visible_stories()
    stories = [s for s in all_stories if not s.draft and not s.archived]
    draft_count = sum(1 for s in all_stories if s.draft and not s.archived)
    archived_count = sum(1 for s in all_stories if s.archived)
    today = date.today()
    years = {}
    for story in stories:
        years.setdefault(story.date.year, []).append(story)
    authors, author_colors = _authors_and_colors()
    all_people = people.list_people(_people_dir())
    people_by_slug = {p.slug: p for p in all_people}
    birthdate = current_app.config.get("BIRTHDATE")
    quiet_months = storage.months_since_last_story(all_stories, today)
    if quiet_months is None or quiet_months < storage.QUIET_SPELL_MONTHS:
        quiet_months = None
    return render_template(
        "timeline.html",
        years=sorted(years.items()),
        stories=stories,
        authors=authors,
        author_colors=author_colors,
        draft_count=draft_count,
        archived_count=archived_count,
        today=today,
        birthdate=birthdate,
        on_this_day=storage.on_this_day(all_stories, today),
        birthdays_today=life_events.birthdays_today(all_people, today),
        union_anniversaries_today=life_events.union_anniversaries_today(all_people, today),
        people_by_slug=people_by_slug,
        has_firsts=bool(storage.stories_with_milestones(all_stories)),
        has_growth=bool(birthdate and storage.growth_photos(all_stories, birthdate, today)),
        quiet_months=quiet_months,
    )


@bp.route("/growth")
@login_required
def growth():
    all_stories = _visible_stories()
    birthdate = current_app.config.get("BIRTHDATE")
    photos = storage.growth_photos(all_stories, birthdate) if birthdate else []
    return render_template("growth.html", photos=photos, birthdate=birthdate)


@bp.route("/firsts")
@login_required
def firsts():
    all_stories = _visible_stories()
    return render_template("firsts.html", firsts=storage.stories_with_milestones(all_stories))


@bp.route("/help")
@login_required
def help_page():
    """A plain-language guide to the app's features, for the family actually
    using it rather than a developer (FEATURES.md F33) — everything else
    documenting these features (README.md, FEATURES.md) is written for the
    latter."""
    return render_template("help.html")


@bp.route("/random")
@login_required
def random_page():
    """Open a random readable story (FEATURES.md F15). Drafts, sealed
    letters, and instants (page-turning is for stories) are never chosen;
    `?not=<id>` excludes one story id (e.g. the one you're already on)."""
    candidates = _visible_page_stories()
    exclude_id = request.args.get("not")
    if exclude_id:
        candidates = [s for s in candidates if s.id != exclude_id]
    if not candidates:
        return redirect(url_for("pages.timeline"))
    choice = random.choice(candidates)
    return redirect(url_for("pages.story", story_id=choice.id))


@bp.route("/manifest.webmanifest")
def manifest():
    """Web app manifest for home-screen install (FEATURES.md F9). No login
    required — the manifest and icons must be fetchable before install."""
    title = current_app.config["TITLE"] or i18n._("Storybook")
    data = {
        "name": title,
        "short_name": title,
        "start_url": "/",
        "display": "standalone",
        "background_color": "#141210",
        "theme_color": "#141210",
        "icons": [
            {
                "src": url_for("static", filename="icons/icon-192.png"),
                "sizes": "192x192",
                "type": "image/png",
            },
            {
                "src": url_for("static", filename="icons/icon-512.png"),
                "sizes": "512x512",
                "type": "image/png",
            },
        ],
    }
    response = jsonify(data)
    response.mimetype = "application/manifest+json"
    return response


@bp.route("/book")
@login_required
def book():
    """The whole book on one page, for reading and printing (FEATURES.md F10).
    A year-chapter title page (FEATURES.md F31) precedes the first entry of
    each calendar year, one per year rather than one per story."""
    stories_dir = current_app.config["STORIES_DIR"]
    readable = storage.readable_stories(_visible_stories())
    authors, author_colors = _authors_and_colors()
    birthdate = current_app.config.get("BIRTHDATE")
    entries = []
    prev_year = None
    for s in readable:
        full = storage.get_story(stories_dir, s.id)
        body_html = render_markdown(full.body, f"/story/{full.id}/media")
        author_color = _author_color(authors, author_colors, full.author)
        year = full.date.year
        entries.append({
            "story": full, "body_html": body_html, "author_color": author_color,
            "chapter_year": year if year != prev_year else None,
            "chapter_age": i18n.age_label(birthdate, full.date, i18n.current_language()) if birthdate else None,
        })
        prev_year = year
    people_by_slug = {p.slug: p for p in people.list_people(_people_dir())}
    return render_template(
        "book.html",
        entries=entries,
        authors=authors,
        birthdate=birthdate,
        min_year=readable[0].date.year if readable else None,
        max_year=readable[-1].date.year if readable else None,
        people_by_slug=people_by_slug,
    )


@bp.route("/book.epub")
@login_required
def book_epub():
    """The whole book as a downloadable EPUB (readable in any e-reader app,
    unlike the browser-print PDF flow at /book)."""
    stories_dir = current_app.config["STORIES_DIR"]
    readable = storage.readable_stories(_visible_stories())
    authors = current_app.config.get("AUTHORS") or []
    entries = []
    for s in readable:
        full = storage.get_story(stories_dir, s.id)
        body_html = render_markdown(full.body, f"/story/{full.id}/media")
        entries.append({"story": full, "body_html": body_html})

    def image_loader(story_id, filename):
        if not storage.is_valid_story_id(story_id) or not storage.is_valid_filename(filename):
            return None
        path = stories_dir / story_id / filename
        return path.read_bytes() if path.is_file() else None

    title = current_app.config["TITLE"] or i18n._("Storybook")
    buf = epub.build_epub(
        title,
        readable[0].date.year if readable else None,
        readable[-1].date.year if readable else None,
        authors,
        entries,
        image_loader,
    )
    filename = f"{storage.slugify(title)}.epub"
    return send_file(buf, mimetype=epub.MIMETYPE, as_attachment=True, download_name=filename)


def _export_is_scoped():
    """Whether this viewer's backup would leave stories out — what the
    import/export page needs to warn them about, since a partial backup
    someone believes is complete is the one real cost of scoping exports."""
    allowed_ids = _exportable_story_ids()
    if allowed_ids is None:
        return False
    return len(storage.list_stories(current_app.config["STORIES_DIR"])) > len(allowed_ids)


def _exportable_story_ids():
    """Which story folders the current viewer's backup zip may contain, or
    None for "all of them" (FEATURES.md F40).

    A backup is scoped to what you can see. The alternative — a complete
    zip for whoever clicks it — would make `/export` the way around every
    group, since the zip carries `.versions/` and photos too. The cost of
    this choice is that a backup taken by someone who can't see every story
    is partial, which the import/export page says in as many words rather
    than leaving it to be discovered.
    """
    viewer_groups, author_name = _viewer_scope()
    if viewer_groups is None:
        return None
    return {s.id for s in groups.visible_stories(
        storage.list_stories(current_app.config["STORIES_DIR"]), viewer_groups, author_name
    )}


@bp.route("/export")
@login_required
def export():
    """Stream a zip of the stories directory (FEATURES.md F8), minus any
    story the viewer isn't in the audience for (F40)."""
    stories_dir = current_app.config["STORIES_DIR"]
    allowed_ids = _exportable_story_ids()
    tmp = tempfile.TemporaryFile()
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_STORED) as zf:
        for path in sorted(stories_dir.rglob("*")):
            if path.is_dir() or path.name.endswith(".tmp"):
                continue
            relative = path.relative_to(stories_dir)
            # The first path segment is the story id for anything under a
            # story folder; people/, groups.json and the other root-level
            # files aren't stories and are never audience-scoped.
            top = relative.parts[0]
            if (
                allowed_ids is not None
                and top not in ("people", groups.GROUPS_FILENAME)
                and (stories_dir / top).is_dir()
                and top not in allowed_ids
            ):
                continue
            zf.write(path, relative)
    tmp.seek(0)
    filename = f"storybook-backup-{date.today().isoformat()}.zip"
    return send_file(tmp, mimetype="application/zip", as_attachment=True, download_name=filename)


@bp.route("/import")
@admin_required_in_accounts_mode
def import_page():
    return render_template("import.html", export_is_scoped=_export_is_scoped())


@bp.route("/drafts")
@login_required
def drafts():
    all_stories = _visible_stories()
    draft_stories = [s for s in all_stories if s.draft and not s.archived]
    draft_stories.sort(key=lambda s: s.updated or datetime.min, reverse=True)
    authors, author_colors = _authors_and_colors()
    return render_template(
        "drafts.html", stories=draft_stories, authors=authors, author_colors=author_colors
    )


@bp.route("/archived")
@login_required
def archived():
    all_stories = _visible_stories()
    archived_stories = [s for s in all_stories if s.archived]
    archived_stories.sort(key=lambda s: s.updated or datetime.min, reverse=True)
    authors, author_colors = _authors_and_colors()
    return render_template(
        "archived.html", stories=archived_stories, authors=authors, author_colors=author_colors
    )


@bp.route("/story/<story_id>")
@login_required
def story(story_id):
    s = _get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    authors, author_colors = _authors_and_colors()
    author_color = _author_color(authors, author_colors, s.author)
    if storage.is_sealed(s):
        return render_template("sealed.html", story=s, author_color=author_color)
    body_html = render_markdown(s.body, f"/story/{story_id}/media")
    prev_story, next_story = _reading_order_neighbors(current_app.config["STORIES_DIR"], s)
    memos = storage.list_memos(current_app.config["STORIES_DIR"] / story_id)
    people_by_slug = {p.slug: p for p in people.list_people(_people_dir())}
    return render_template(
        "story.html", story=s, body_html=body_html, authors=authors, author_color=author_color,
        prev_story=prev_story, next_story=next_story, memos=memos,
        birthdate=current_app.config.get("BIRTHDATE"), people_by_slug=people_by_slug,
    )


def _reading_order_neighbors(stories_dir, current):
    """Previous/next readable story either side of `current` (F2). None/None
    when `current` isn't itself readable (e.g. a draft, archived, or an
    instant) or at either end. Instants are also skipped as candidate
    neighbors for a real story (FEATURES.md F13: page-turning is for
    stories)."""
    if current.draft or current.archived or current.kind != "story":
        return None, None
    readable = _visible_page_stories()
    for i, r in enumerate(readable):
        if r.id == current.id:
            prev_story = readable[i - 1] if i > 0 else None
            next_story = readable[i + 1] if i < len(readable) - 1 else None
            return prev_story, next_story
    return None, None


@bp.route("/story/<story_id>/history")
@login_required
def story_history(story_id):
    s = _get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    versions = storage.list_versions(current_app.config["STORIES_DIR"], story_id)
    return render_template("history.html", story=s, versions=versions)


@bp.route("/story/<story_id>/media/<filename>")
@login_required
def story_media(story_id, filename):
    # Gated on the story, not just the filename: without this the page
    # 404s for a non-member but every photo in it stays fetchable by
    # direct URL, which is most of what a scoped story is protecting.
    _get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    return _serve_media(current_app.config["STORIES_DIR"], story_id, filename)


@bp.route("/new")
@login_required
def new_story():
    authors = current_app.config.get("AUTHORS") or []
    prompt_list = prompts.load_prompts(current_app.config["STORIES_DIR"])
    initial_prompt = random.choice(prompt_list) if prompt_list else None
    return render_template(
        "editor.html", story=None, today=date.today(), authors=authors,
        prompts=prompt_list, initial_prompt=initial_prompt, memos=[],
        all_people=_other_people_refs(), all_groups=_available_groups(),
    )


@bp.route("/new-instant")
@login_required
def new_instant():
    authors = current_app.config.get("AUTHORS") or []
    return render_template(
        "instant.html", today=date.today(), authors=authors,
        all_groups=_available_groups(),
    )


@bp.route("/edit/<story_id>")
@login_required
def edit_story(story_id):
    s = _get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    authors = current_app.config.get("AUTHORS") or []
    memos = storage.list_memos(current_app.config["STORIES_DIR"] / story_id)
    return render_template(
        "editor.html", story=s, today=date.today(), authors=authors, memos=memos,
        all_people=_other_people_refs(), all_groups=_available_groups(s),
    )


def _people_dir():
    return storage.people_dir(current_app.config["STORIES_DIR"])


def _person_ref(people_by_slug, slug):
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


def _other_people_refs(exclude_slug=None):
    all_people = people.list_people(_people_dir())
    people_by_slug = {p.slug: p for p in all_people}
    return [
        _person_ref(people_by_slug, p.slug) for p in all_people if p.slug != exclude_slug
    ]


# Registers routes_people.py's, routes_accounts.py's and routes_groups.py's
# routes onto `bp` (see module docstring) — must come after every helper
# they import above.
from . import routes_accounts, routes_groups, routes_people  # noqa: E402,F401
