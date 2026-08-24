"""The core story pages: timeline, story, editor, drafts/archived, the
book view, help, random, the manifest, and backup export/import.

Registers onto the `pages` blueprint `views.py` defines, alongside
`routes_people.py`, `routes_accounts.py`, `routes_groups.py`,
`routes_settings.py` and `routes_themes.py` — so `url_for("pages.xxx")`
keeps working in Python and in templates regardless of which of the six
files a route's code sits in. `create_app` imports all six for that
registration side effect.

The shared view helpers this file used to own — `visible_stories`,
`get_story_or_404`, `current_people_dir`, `serve_media`, `person_ref` and
the rest — now live in `views.py`, because five of its siblings import
them and one file cannot both define a blueprint and be imported by
everything that registers onto it.

The export helpers below are the exception, and stay: they are the
`/export` route's own scoping rules, and nothing else calls them.
"""

import random
from datetime import date, datetime
from pathlib import Path

from flask import (
    current_app,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from . import backup, epub, groups, i18n, life_events, people, prompts, settings, storage

# By name rather than `from . import timeline`: the timeline *page* route
# below is `def timeline()`, and its endpoint is `pages.timeline` in a
# dozen templates. The module import would shadow it.
from .timeline import (
    QUIET_SPELL_MONTHS,
    growth_photos,
    is_sealed,
    months_since_last_story,
    on_this_day,
    readable_stories,
    stories_with_milestones,
)
from .auth import admin_required_in_accounts_mode, login_required
from .rendering import render_markdown
from .views import (
    color_for_author,
    authors_and_colors,
    available_groups,
    bp,
    current_people_dir,
    get_story_or_404,
    other_people_refs,
    serve_media,
    viewer_scope,
    visible_page_stories,
    visible_stories,
)


@bp.route("/")
@login_required
def timeline():
    # F51: a book nobody has set up yet sends whoever can set it up to the
    # wizard, once. Here rather than in a before_request so there is no way
    # to loop, and so a family member who *can't* configure anything simply
    # sees the timeline they came for.
    if not settings.is_configured(current_app.config["STORIES_DIR"]) and (
        not current_app.config["ACCOUNTS_ENABLED"] or session.get("role") == "admin"
    ):
        return redirect(url_for("pages.setup_page"))
    all_stories = visible_stories()
    stories = [s for s in all_stories if not s.draft and not s.archived]
    draft_count = sum(1 for s in all_stories if s.draft and not s.archived)
    archived_count = sum(1 for s in all_stories if s.archived)
    today = date.today()
    years = {}
    for story in stories:
        years.setdefault(story.date.year, []).append(story)
    authors, author_colors = authors_and_colors()
    all_people = people.list_people(current_people_dir())
    people_by_slug = {p.slug: p for p in all_people}
    birthdate = settings.book("BIRTHDATE")
    quiet_months = months_since_last_story(all_stories, today)
    if quiet_months is None or quiet_months < QUIET_SPELL_MONTHS:
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
        on_this_day=on_this_day(all_stories, today),
        birthdays_today=life_events.birthdays_today(all_people, today),
        union_anniversaries_today=life_events.union_anniversaries_today(all_people, today),
        people_by_slug=people_by_slug,
        has_firsts=bool(stories_with_milestones(all_stories)),
        has_growth=bool(birthdate and growth_photos(all_stories, birthdate, today)),
        quiet_months=quiet_months,
    )


@bp.route("/growth")
@login_required
def growth():
    all_stories = visible_stories()
    birthdate = settings.book("BIRTHDATE")
    photos = growth_photos(all_stories, birthdate) if birthdate else []
    return render_template("growth.html", photos=photos, birthdate=birthdate)


@bp.route("/firsts")
@login_required
def firsts():
    all_stories = visible_stories()
    return render_template("firsts.html", firsts=stories_with_milestones(all_stories))


# The three third-party bundles under `app/static/vendor/` are served to
# every visitor's browser, and serving them is redistribution — so their
# copyright and permission notices have to travel with them (F53).
# `path` points at the upstream licence text vendored beside each bundle,
# and the page renders *that file*, never a copy pasted into a template, so
# the notice on screen cannot drift from the notice in the repository.
# `tests/test_vendored_licences.py` is what keeps those files present.
VENDORED_LICENCES = (
    {
        "name": "Toast UI Editor",
        "version": "3.2.2",
        "purpose": "the editor you write stories in",
        "url": "https://github.com/nhn/tui.editor",
        "path": "vendor/toastui/LICENSE",
    },
    {
        "name": "family-chart",
        "version": "0.9.0",
        "purpose": "draws the family tree",
        "url": "https://github.com/donatso/family-chart",
        "path": "vendor/familychart/LICENSE",
    },
    {
        "name": "D3",
        "version": "7.9.0",
        "purpose": "the graphics library the family tree is built on",
        "url": "https://d3js.org",
        "path": "vendor/d3/LICENSE",
    },
)

# Installed from PyPI and run on the server only — never sent to a browser,
# so no notice obligation attaches to them. Listed for transparency, not
# for compliance. Kept in step with `requirements.txt` by
# `tests/test_licences.py`, which fails when a pinned package is missing
# from here.
SERVER_LICENCES = (
    ("Flask, Werkzeug, Jinja2, Click, itsdangerous", "BSD-3-Clause"),
    ("Flask-WTF, WTForms", "BSD-3-Clause"),
    ("Python-Markdown", "BSD-3-Clause"),
    ("PyMdown Extensions", "MIT"),
    ("python-frontmatter, PyYAML", "MIT"),
    ("Pillow", "MIT-CMU"),
    ("pillow-heif", "BSD-3-Clause (its bundled codecs are LGPLv3/GPLv2)"),
    ("Waitress", "ZPL 2.1"),
    ("MCP Python SDK", "MIT"),
    ("faster-whisper (optional, transcription only)", "MIT"),
)


def _vendored_licences():
    """Each vendored bundle's licence text, read off disk once per process.

    Cached on the app rather than with `functools.lru_cache`, so a test app
    pointed at a different static folder cannot inherit another app's text.
    """
    cached = current_app.extensions.get("vendored_licences")
    if cached is not None:
        return cached
    static_dir = Path(current_app.static_folder)
    entries = []
    for library in VENDORED_LICENCES:
        try:
            text = (static_dir / library["path"]).read_text(encoding="utf-8").strip()
        except OSError:
            # A missing licence file is a packaging bug worth surfacing, and
            # `tests/test_vendored_licences.py` fails on it — but it is not
            # worth 500-ing a page whose whole job is to be readable.
            text = ""
        entries.append({**library, "text": text})
    current_app.extensions["vendored_licences"] = entries
    return entries


@bp.route("/licences")
@login_required
def licences_page():
    """Third-party notices for everything this book is built on (F53).

    The vendored JS and CSS is served to browsers, so its licences are
    reproduced here in full; the server-side packages are listed for
    transparency only. Behind `login_required` like every other page — the
    obligation is discharged by the notices shipping with the code and by
    being readable to whoever receives the app, not by being on the open
    internet.
    """
    return render_template(
        "licences.html",
        vendored=_vendored_licences(),
        server_licences=SERVER_LICENCES,
    )


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
    candidates = visible_page_stories()
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
    title = settings.book("TITLE") or i18n._("Storybook")
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
    readable = readable_stories(visible_stories())
    authors, author_colors = authors_and_colors()
    birthdate = settings.book("BIRTHDATE")
    entries = []
    prev_year = None
    for s in readable:
        full = storage.get_story(stories_dir, s.id)
        body_html = render_markdown(full.body, f"/story/{full.id}/media")
        author_color = color_for_author(authors, author_colors, full.author)
        year = full.date.year
        entries.append({
            "story": full, "body_html": body_html, "author_color": author_color,
            "chapter_year": year if year != prev_year else None,
            "chapter_age": i18n.age_label(birthdate, full.date, i18n.current_language()) if birthdate else None,
        })
        prev_year = year
    people_by_slug = {p.slug: p for p in people.list_people(current_people_dir())}
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
    readable = readable_stories(visible_stories())
    authors = settings.book("AUTHORS") or []
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

    title = settings.book("TITLE") or i18n._("Storybook")
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
    viewer_groups, author_name = viewer_scope()
    if viewer_groups is None:
        return None
    return {s.id for s in groups.visible_stories(
        storage.list_stories(current_app.config["STORIES_DIR"]), viewer_groups, author_name
    )}


def _viewer_may_export_credentials():
    """Whether this viewer's zip may contain account files.

    Admins only, and everyone outside accounts mode — there, one shared
    password is one identity, exactly as `viewer_scope` treats it.

    The hashes are scrypt, so this is not a password handed over. It is an
    *offline* guessing target, which is the part that matters: the login
    throttle (F36) cannot see an attacker working on a zip at home, and the
    file names the role beside the hash, so it says which account is worth
    the effort. An admin's password recovered that way reaches every group,
    since an admin can add themselves to one — the escalation F40 and F41
    deliberately made visible would become invisible again.
    """
    if not current_app.config["ACCOUNTS_ENABLED"]:
        return True
    return session.get("role") == "admin"


@bp.route("/export")
@login_required
def export():
    """Stream a zip of the stories directory (FEATURES.md F8), minus any
    story the viewer isn't in the audience for (F40) and, unless they are an
    admin, minus every account file (F43).

    The two `_`-prefixed calls are the whole of the access control, and
    they stay here rather than in `backup.py` on purpose: reading the
    session is what makes them policy, and a rule about who may see what
    is easier to audit beside the route it guards.
    """
    tmp = backup.write_backup(
        current_app.config["STORIES_DIR"],
        allowed_ids=_exportable_story_ids(),
        with_credentials=_viewer_may_export_credentials(),
    )
    filename = f"storybook-backup-{date.today().isoformat()}.zip"
    return send_file(tmp, mimetype="application/zip", as_attachment=True, download_name=filename)


@bp.route("/import")
@admin_required_in_accounts_mode
def import_page():
    return render_template("import.html", export_is_scoped=_export_is_scoped())


@bp.route("/drafts")
@login_required
def drafts():
    all_stories = visible_stories()
    draft_stories = [s for s in all_stories if s.draft and not s.archived]
    draft_stories.sort(key=lambda s: s.updated or datetime.min, reverse=True)
    authors, author_colors = authors_and_colors()
    return render_template(
        "drafts.html", stories=draft_stories, authors=authors, author_colors=author_colors
    )


@bp.route("/archived")
@login_required
def archived():
    all_stories = visible_stories()
    archived_stories = [s for s in all_stories if s.archived]
    archived_stories.sort(key=lambda s: s.updated or datetime.min, reverse=True)
    authors, author_colors = authors_and_colors()
    return render_template(
        "archived.html", stories=archived_stories, authors=authors, author_colors=author_colors
    )


@bp.route("/story/<story_id>")
@login_required
def story(story_id):
    s = get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    authors, author_colors = authors_and_colors()
    author_color = color_for_author(authors, author_colors, s.author)
    if is_sealed(s):
        return render_template("sealed.html", story=s, author_color=author_color)
    body_html = render_markdown(s.body, f"/story/{story_id}/media")
    prev_story, next_story = _reading_order_neighbors(current_app.config["STORIES_DIR"], s)
    memos = storage.list_memos(current_app.config["STORIES_DIR"] / story_id)
    people_by_slug = {p.slug: p for p in people.list_people(current_people_dir())}
    return render_template(
        "story.html", story=s, body_html=body_html, authors=authors, author_color=author_color,
        prev_story=prev_story, next_story=next_story, memos=memos,
        birthdate=settings.book("BIRTHDATE"), people_by_slug=people_by_slug,
    )


def _reading_order_neighbors(stories_dir, current):
    """Previous/next readable story either side of `current` (F2). None/None
    when `current` isn't itself readable (e.g. a draft, archived, or an
    instant) or at either end. Instants are also skipped as candidate
    neighbors for a real story (FEATURES.md F13: page-turning is for
    stories)."""
    if current.draft or current.archived or current.kind != "story":
        return None, None
    readable = visible_page_stories()
    for i, r in enumerate(readable):
        if r.id == current.id:
            prev_story = readable[i - 1] if i > 0 else None
            next_story = readable[i + 1] if i < len(readable) - 1 else None
            return prev_story, next_story
    return None, None


@bp.route("/story/<story_id>/history")
@login_required
def story_history(story_id):
    s = get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    versions = storage.list_versions(current_app.config["STORIES_DIR"], story_id)
    return render_template("history.html", story=s, versions=versions)


@bp.route("/story/<story_id>/media/<filename>")
@login_required
def story_media(story_id, filename):
    # Gated on the story, not just the filename: without this the page
    # 404s for a non-member but every photo in it stays fetchable by
    # direct URL, which is most of what a scoped story is protecting.
    get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    return serve_media(current_app.config["STORIES_DIR"], story_id, filename)


@bp.route("/new")
@login_required
def new_story():
    authors = settings.book("AUTHORS") or []
    prompt_list = prompts.load_prompts(current_app.config["STORIES_DIR"])
    initial_prompt = random.choice(prompt_list) if prompt_list else None
    return render_template(
        "editor.html", story=None, today=date.today(), authors=authors,
        prompts=prompt_list, initial_prompt=initial_prompt, memos=[],
        all_people=other_people_refs(), all_groups=available_groups(),
    )


@bp.route("/new-instant")
@login_required
def new_instant():
    authors = settings.book("AUTHORS") or []
    return render_template(
        "instant.html", today=date.today(), authors=authors,
        all_groups=available_groups(),
    )


@bp.route("/edit/<story_id>")
@login_required
def edit_story(story_id):
    s = get_story_or_404(current_app.config["STORIES_DIR"], story_id)
    authors = settings.book("AUTHORS") or []
    memos = storage.list_memos(current_app.config["STORIES_DIR"] / story_id)
    return render_template(
        "editor.html", story=s, today=date.today(), authors=authors, memos=memos,
        all_people=other_people_refs(), all_groups=available_groups(s),
    )
