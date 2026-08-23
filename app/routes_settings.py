"""Setting the book up from inside it (FEATURES.md F51).

Two pages, registering onto the `pages` blueprint `views.py` defines. `/setup` runs once, on a book nobody has configured yet;
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
from .views import bp


def _stories_dir():
    return current_app.config["STORIES_DIR"]


def _birthdate_value():
    parsed = settings.clean_birthdate(request.form.get("birthdate"))
    return parsed.isoformat() if parsed else ""


#: How each stored setting is read back out of a submitted form. Keyed by
#: the name of the field that carries it, which is also the key it is
#: stored under.
_FIELDS = {
    "title": lambda: settings.clean_title(request.form.get("title")),
    "birthdate": _birthdate_value,
    "child": lambda: settings.clean_child(request.form.get("child")),
    "authors": lambda: settings.clean_authors(request.form.get("authors")),
    "language": lambda: settings.clean_language(
        request.form.get("language"), i18n.LANGUAGES
    ),
    "theme": lambda: _clean_theme(request.form.get("theme")),
}


def _blank(value):
    """What "the field was left empty" looks like for each kind of
    setting."""
    return value in ("", [], None)


def _form_values(keep_existing=False):
    """The settings *this* form submitted, validated. Raises SettingsError
    with something a person can act on.

    `keep_existing` is the setup wizard's rule: **a blank field means
    "skip this", not "erase what is there".** On /settings, clearing a box
    is how someone takes a title back off their book, and that has to keep
    working — it is a page they can return to, and it says so. The wizard
    is a one-time flow that a family may meet on a book that already has a
    name, a cast and a theme, and on that page an empty box is far more
    likely to mean "I did not fill this in" than "delete it". Measured on
    a book with a cast, a made theme and an audience group but no story
    yet: one submit with the fields cleared took away its title, birth
    date, narrators and language.

    This is deliberately belt-and-braces with `settings.is_configured`,
    which now recognises made themes and groups too. That one answers
    "should the wizard run at all"; this one makes the answer not matter,
    including for the case neither can detect — a stories volume that
    failed to mount looks exactly like a new book.

    Only the fields the form actually rendered, and that is load-bearing
    rather than tidy. To `settings.effective` a key that is *present but
    empty* means "no value" — it is how someone clears the title and gets
    the app's own name back — while a key that is *absent* falls through
    to the environment. So a form that returned all six keys regardless
    would erase whatever the environment set for any field it does not
    show.

    That is not hypothetical: the setup wizard offers no theme and no
    tree-child, and used to write both as empty. A fresh install started
    with STORYBOOK_THEME=orbit served the ranch from the moment anyone
    pressed "Start writing", which is the exact opposite of what F51
    promised about upgrading.
    """
    values = {}
    for key, read in _FIELDS.items():
        if key not in request.form:
            continue
        value = read()
        if keep_existing and _blank(value) and settings.book(settings.KEYS[key]):
            continue
        values[key] = value
    return values


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
            values = _form_values(keep_existing=True)
        except settings.SettingsError as error:
            flash(str(error), "error")
            return render_template(
                "setup.html", form=request.form, current=_current(), **_choices()
            )

        child_name = (request.form.get("child_name") or "").strip()
        # `.get`: the wizard renders no `child` field, so the key is not in
        # `values` at all — which is the point of the rule above.
        if child_name and not values.get("child"):
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
