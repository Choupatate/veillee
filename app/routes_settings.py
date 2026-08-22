"""Setting the book up from inside it (FEATURES.md F51).

Two pages, registering onto the `pages` blueprint `routes_pages.py`
defines. `/setup` runs once, on a book nobody has configured yet;
`/settings` is the same values, changeable forever after. Both are behind
`admin_required_in_accounts_mode`, the gate the theme pages and the backup
restore already use: the admin when accounts are on, the one
password-holder when they are not.

The wizard exists because of who this app is for. A parent who wants to
write their child's stories should not have to learn what an environment
variable is, restart a container, or read a README to give their book a
name. What is left in the environment after this is only what genuinely
describes the machine — the password, the session key, where the files
live, whether a proxy sits in front.
"""

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from . import i18n, people, settings, storage, themes
from .auth import admin_required_in_accounts_mode
from .i18n import _
from .routes_pages import bp


def _stories_dir():
    return current_app.config["STORIES_DIR"]


def _form_values():
    """The six settings as the form submitted them, validated. Raises
    SettingsError with something a person can act on."""
    return {
        "title": settings.clean_title(request.form.get("title")),
        "birthdate": (
            settings.clean_birthdate(request.form.get("birthdate")).isoformat()
            if settings.clean_birthdate(request.form.get("birthdate"))
            else ""
        ),
        "child": settings.clean_child(request.form.get("child")),
        "authors": settings.clean_authors(request.form.get("authors")),
        "language": settings.clean_language(
            request.form.get("language"), i18n.LANGUAGES
        ),
        "theme": _clean_theme(request.form.get("theme")),
    }


def _clean_theme(value):
    value = (value or "").strip()
    if not value:
        return ""
    user_dir = themes.user_themes_dir(_stories_dir())
    if not themes.is_valid_theme(value, user_dir):
        raise settings.SettingsError("There is no theme with that name.")
    return value


def _current():
    """What the book is doing right now — a value set in the app, or the
    environment variable behind it.

    The wizard prefills from this too. An install upgrading into this
    feature already has its settings in environment variables, and a form
    that showed them as empty would quietly erase them the moment someone
    pressed Save.
    """
    return {
        "title": settings.book("TITLE") or "",
        "birthdate": (settings.book("BIRTHDATE").isoformat()
                      if settings.book("BIRTHDATE") else ""),
        "child": settings.book("CHILD_SLUG") or "",
        "authors": settings.authors_text(settings.book("AUTHORS")),
        "language": settings.book("DEFAULT_LANGUAGE") or "",
        "theme": settings.book("THEME") or "",
    }


def _choices():
    """What the two forms offer: the packs installed, the languages built
    in, and the cast (so the family tree's child is picked, not typed)."""
    user_dir = themes.user_themes_dir(_stories_dir())
    return {
        "themes": [
            {"name": name, "label": themes.label(name, user_dir)}
            for name in themes.available_themes(user_dir)
        ],
        "languages": i18n.LANGUAGES,
        "people": people.list_people(storage.people_dir(_stories_dir())),
    }


@bp.route("/settings", methods=["GET", "POST"])
@admin_required_in_accounts_mode
def settings_page():
    stories_dir = _stories_dir()
    if request.method == "POST":
        try:
            values = _form_values()
        except settings.SettingsError as error:
            flash(str(error), "error")
            return render_template(
                "settings.html", form=request.form, **_choices()
            )
        settings.save(stories_dir, values)
        flash(_("Saved."), "success")
        return redirect(url_for("pages.settings_page"))

    stored = settings.read(stories_dir)
    return render_template(
        "settings.html",
        form=None,
        stored=stored,
        current=_current(),
        **_choices(),
    )


@bp.route("/setup", methods=["GET", "POST"])
@admin_required_in_accounts_mode
def setup_page():
    """The one-time walk-through. Gone once the book has been set up: a
    wizard that can be reached again is just a second settings page with
    worse wording."""
    stories_dir = _stories_dir()
    if settings.is_configured(stories_dir):
        return redirect(url_for("pages.settings_page"))

    if request.method == "POST":
        # "Not now" is a real answer. It writes the file empty, so the book
        # counts as set up and nobody is asked again — the alternative is a
        # banner that follows a family around forever.
        if request.form.get("skip"):
            settings.save(stories_dir, {})
            return redirect(url_for("pages.timeline"))
        try:
            values = _form_values()
        except settings.SettingsError as error:
            flash(str(error), "error")
            return render_template(
                "setup.html", form=request.form, current=_current(), **_choices()
            )

        child_name = (request.form.get("child_name") or "").strip()
        if child_name and not values["child"]:
            # The book is for someone, so that someone becomes the first
            # person in the cast — with their birthday already on it.
            slug = people.create_person(
                storage.people_dir(stories_dir),
                child_name,
                born=settings.clean_birthdate(request.form.get("birthdate")),
            )
            values["child"] = slug
        settings.save(stories_dir, values)
        flash(_("Your book is ready. Write the first story."), "success")
        return redirect(url_for("pages.timeline"))

    return render_template("setup.html", form=None, current=_current(), **_choices())
