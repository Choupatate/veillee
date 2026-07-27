"""Audience-group management (FEATURES.md F40, opened up in F41): create a
group, rename it, choose who's in it. Registers onto the same `pages`
blueprint `routes_pages.py` defines — see that module's docstring for why
these live in a separate file without a separate blueprint.

404 throughout unless accounts mode is on: with one shared password there
is one identity, so a group would have nobody to scope a story away from.

Anyone in the family can make a group. The thing that keeps that from
dissolving the feature is `groups.can_manage`: a group is changed by the
people in it, or by an admin, and by nobody else. If any logged-in person
could edit any group, anyone could add themselves to "Just us" and read
it.

Note the division this file still embodies, which is the values call at the
centre of F40: managing groups grants no reading privilege. Nothing here
lets an admin see a story scoped away from them — they can add themselves
to a group and then read it, which is a visible, recorded act rather than
an invisible capability.
"""

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import accounts, groups, people, storage
from .i18n import _
from .auth import login_required
from .routes_pages import _people_dir, bp


def _groups_enabled_or_404():
    if not current_app.config["ACCOUNTS_ENABLED"]:
        abort(404)
    return current_app.config["STORIES_DIR"]


def _viewer():
    """(person slug, display name, is_admin) for whoever is asking."""
    person_slug = session.get("person_slug")
    person = people.get_person(_people_dir(), person_slug) if person_slug else None
    return person_slug, (person.name if person else None), session.get("role") == "admin"


def _flash_group_error(exc):
    """GroupError carries an uninterpolated template plus its values, so the
    French catalog gets a key it can actually match (see groups.GroupError)."""
    flash(_(exc.message, **exc.params) if isinstance(exc, groups.GroupError) else str(exc), "error")


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


@bp.route("/groups", methods=["GET", "POST"])
@login_required
def groups_page():
    stories_dir = _groups_enabled_or_404()
    person_slug, _name, is_admin = _viewer()

    if request.method == "POST":
        try:
            group = groups.create_group(
                stories_dir, request.form.get("name") or "", created_by=person_slug
            )
        except ValueError as exc:
            _flash_group_error(exc)
        else:
            return redirect(url_for("pages.group_page", slug=group.slug))

    people_dir = _people_dir()
    people_by_slug = {p.slug: p for p in people.list_people(people_dir)}
    all_stories = storage.list_stories(stories_dir)
    rows = []
    for group in groups.list_groups(stories_dir):
        creator = people_by_slug.get(group.created_by) if group.created_by else None
        rows.append({
            "group": group,
            "members": [people_by_slug[s] for s in group.members if s in people_by_slug],
            "story_count": sum(1 for s in all_stories if group.slug in s.audience),
            "can_manage": groups.can_manage(group, person_slug, is_admin),
            "creator_name": creator.name if creator else None,
        })
    return render_template("groups.html", rows=rows, at_limit=len(rows) >= groups.MAX_GROUPS)


@bp.route("/groups/<slug>", methods=["GET", "POST"])
@login_required
def group_page(slug):
    stories_dir = _groups_enabled_or_404()
    group = groups.get_group(stories_dir, slug)
    if group is None:
        abort(404)
    people_dir = _people_dir()
    person_slug, viewer_name, is_admin = _viewer()
    can_manage = groups.can_manage(group, person_slug, is_admin)

    if request.method == "POST":
        # A group's existence isn't a secret — it's listed for everyone, and
        # its name shows on stories kept to it — so this is an honest 403
        # rather than the 404 used elsewhere to hide a page's existence.
        if not can_manage:
            abort(403)
        try:
            groups.rename_group(stories_dir, slug, request.form.get("name") or group.name)
            groups.set_members(stories_dir, slug, request.form.getlist("members"))
        except ValueError as exc:
            _flash_group_error(exc)
        except FileNotFoundError:
            abort(404)
        else:
            return redirect(url_for("pages.groups_page"))
        group = groups.get_group(stories_dir, slug)

    all_people = people.list_people(people_dir)
    kept_here = [s for s in storage.list_stories(stories_dir) if slug in s.audience]
    creator = people.get_person(people_dir, group.created_by) if group.created_by else None
    return render_template(
        "group.html", group=group,
        member_rows=_member_rows(all_people, people_dir, set(group.members)),
        story_count=len(kept_here),
        # Widening a group republishes other people's writing, not just your
        # own. Worth saying out loud on the page where you'd do it.
        others_count=sum(1 for s in kept_here if s.author and s.author != viewer_name),
        can_manage=can_manage,
        creator_name=creator.name if creator else None,
        # Rights follow membership, so taking yourself out is the one edit
        # you can't undo from this page.
        viewer_is_member=bool(person_slug) and person_slug in group.members,
    )
