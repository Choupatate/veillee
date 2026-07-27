"""Audience-group management (FEATURES.md F40): create a group, rename it,
choose who's in it. Registers onto the same `pages` blueprint
`routes_pages.py` defines — see that module's docstring for why these live
in a separate file without a separate blueprint.

Admin-only, and 404 throughout unless accounts mode is on: with one shared
password there is one identity, so a group would have nobody to scope a
story away from.

Note the division this file embodies, which is the values call at the
centre of F40: an admin manages groups but gets no reading privilege from
it. Nothing here lets an admin see a story scoped away from them — they
can add themselves to a group and then read it, which is a visible,
recorded act rather than an invisible capability.
"""

from flask import abort, current_app, flash, redirect, render_template, request, url_for

from . import accounts, groups, people, storage
from .i18n import _
from .auth import admin_required
from .routes_pages import _people_dir, bp


def _groups_enabled_or_404():
    if not current_app.config["ACCOUNTS_ENABLED"]:
        abort(404)
    return current_app.config["STORIES_DIR"]


def _member_rows(all_people, people_dir, member_slugs):
    """Each Person with whether they're in this group and whether they can
    actually log in — a member with no account is not wrong (they may get
    one later), but it's worth showing, since a group made entirely of
    people who can't log in silently protects nothing."""
    return [
        {
            "person": p,
            "is_member": p.slug in member_slugs,
            "has_account": accounts.get_account(people_dir, p.slug) is not None,
        }
        for p in all_people
    ]


@bp.route("/admin/groups", methods=["GET", "POST"])
@admin_required
def admin_groups():
    stories_dir = _groups_enabled_or_404()

    if request.method == "POST":
        try:
            group = groups.create_group(stories_dir, request.form.get("name") or "")
        except ValueError as exc:
            flash(_(str(exc)), "error")
        else:
            return redirect(url_for("pages.admin_group", slug=group.slug))

    people_dir = _people_dir()
    people_by_slug = {p.slug: p for p in people.list_people(people_dir)}
    all_stories = storage.list_stories(stories_dir)
    rows = []
    for group in groups.list_groups(stories_dir):
        rows.append({
            "group": group,
            "members": [people_by_slug[s] for s in group.members if s in people_by_slug],
            "story_count": sum(1 for s in all_stories if group.slug in s.audience),
        })
    return render_template("admin_groups.html", rows=rows)


@bp.route("/admin/groups/<slug>", methods=["GET", "POST"])
@admin_required
def admin_group(slug):
    stories_dir = _groups_enabled_or_404()
    group = groups.get_group(stories_dir, slug)
    if group is None:
        abort(404)
    people_dir = _people_dir()

    if request.method == "POST":
        try:
            groups.rename_group(stories_dir, slug, request.form.get("name") or group.name)
            groups.set_members(stories_dir, slug, request.form.getlist("members"))
        except ValueError as exc:
            flash(_(str(exc)), "error")
        except FileNotFoundError:
            abort(404)
        else:
            return redirect(url_for("pages.admin_groups"))
        group = groups.get_group(stories_dir, slug)

    all_people = people.list_people(people_dir)
    story_count = sum(
        1 for s in storage.list_stories(stories_dir) if slug in s.audience
    )
    return render_template(
        "admin_group.html", group=group,
        member_rows=_member_rows(all_people, people_dir, set(group.members)),
        story_count=story_count,
    )
