"""Making a theme pack from inside the book (FEATURES.md F50).

Two public routes and a small admin area, all registering onto the `pages`
blueprint `routes_pages.py` defines — see that module's docstring for why
these live in their own file without a blueprint of their own.

The two public ones serve a made pack's palette and pictures. They are
public for the same reason `/static` is: the login page is dressed by the
pack too, and a login screen with broken images would be the first thing a
family saw. They can only ever reach `<stories>/themes/<pack>/img/`, and
only files the catalogue names.

Everything that *changes* a pack is behind `admin_required_in_accounts_mode`
— the admin when accounts are on, the one password-holder when they are
not. A write link never gets a session that passes `login_required` at all,
so a guest cannot reach any of this.
"""

from flask import (
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from . import theme_catalog, theme_packs, themes
from .auth import admin_required_in_accounts_mode
from .i18n import _
from .routes_pages import bp


def _user_dir():
    return themes.user_themes_dir(current_app.config["STORIES_DIR"])


def _asset_url(theme, filename, user_dir):
    """Where one picture of a *named* pack comes from, with the same
    fallback the book itself applies."""
    kind, pack, name = themes.image_ref(theme, filename, user_dir)
    if kind == "user":
        return url_for("pages.theme_media", theme=pack, filename=name)
    return url_for("static", filename=f"themes/{pack}/img/{name}")


def _pack_or_404(name):
    if not themes.is_user_theme(name, _user_dir()):
        abort(404)
    return name


# --- serving a made pack ------------------------------------------------------


@bp.route("/themes/<theme>/theme.css")
def theme_css(theme):
    """A made pack's stylesheet, generated from its palette.

    Not cached hard on purpose: unlike a photo, a pack's colours change
    under a filename that stays the same, and a year-long cache would show
    a family the palette they replaced.
    """
    _pack_or_404(theme)
    css = theme_packs.render_stylesheet(_user_dir(), theme)
    return current_app.response_class(css, mimetype="text/css")


@bp.route("/themes/<theme>/img/<filename>")
def theme_media(theme, filename):
    """One picture from a made pack. Validated the way `story_media` is:
    the pack has to be a real made pack, and the filename has to be one the
    catalogue names — which is an allowlist of 37 strings, not a pattern."""
    _pack_or_404(theme)
    if filename not in theme_catalog.BY_FILENAME:
        abort(404)
    img_dir = theme_packs.pack_dir(_user_dir(), theme) / "img"
    if not (img_dir / filename).is_file():
        abort(404)
    # Same reasoning as theme_css, and the same reasoning F12 uses for voice
    # memos: a filename that can come back meaning a different picture is
    # not a cache key.
    return send_from_directory(img_dir, filename, max_age=None)


# --- the admin area -----------------------------------------------------------


@bp.route("/themes")
@admin_required_in_accounts_mode
def themes_page():
    return render_template(
        "themes.html",
        packs=theme_packs.list_packs(_user_dir()),
        builtin=[
            {"name": name, "label": themes.label(name), "swatch": themes.swatch(name)}
            for name in themes.builtin_themes()
        ],
    )


def _form_palette():
    """The colour fields, as `{scheme: {bg, text, accent}}`. A scheme with
    no ticked checkbox isn't read at all, so an unticked scheme's colours
    are kept in the form without being saved."""
    picked = request.form.getlist("schemes")
    return {
        scheme: {
            key: request.form.get(f"{scheme}-{key}", "")
            for key in ("bg", "text", "accent")
        }
        for scheme in picked
    }


@bp.route("/themes/new", methods=["GET", "POST"])
@admin_required_in_accounts_mode
def new_theme():
    if request.method == "POST":
        label = request.form.get("label", "")
        name = theme_packs.slugify(request.form.get("name") or label)
        try:
            theme_packs.save_pack(
                _user_dir(), name,
                label=label,
                description=request.form.get("description", ""),
                scheme_colors=_form_palette(),
            )
        except theme_packs.PackError as error:
            flash(str(error), "error")
            return render_template("theme_editor.html", pack=None, form=request.form)
        return redirect(url_for("pages.theme_assets", theme=name))
    return render_template("theme_editor.html", pack=None, form=None)


@bp.route("/themes/<theme>/edit", methods=["GET", "POST"])
@admin_required_in_accounts_mode
def edit_theme(theme):
    _pack_or_404(theme)
    if request.method == "POST":
        try:
            theme_packs.save_pack(
                _user_dir(), theme,
                label=request.form.get("label", ""),
                description=request.form.get("description", ""),
                scheme_colors=_form_palette(),
            )
        except theme_packs.PackError as error:
            flash(str(error), "error")
            return render_template(
                "theme_editor.html",
                pack=theme_packs.read_pack(_user_dir(), theme) | {"name": theme},
                form=request.form,
            )
        flash(_("Saved."), "success")
        return redirect(url_for("pages.theme_assets", theme=theme))
    return render_template(
        "theme_editor.html",
        pack=theme_packs.read_pack(_user_dir(), theme) | {"name": theme},
        form=None,
    )


@bp.route("/themes/<theme>/pictures")
@admin_required_in_accounts_mode
def theme_assets(theme):
    """The sheet: one row per picture, with the prompt to paste into an AI
    on one side and the upload on the other."""
    _pack_or_404(theme)
    user_dir = _user_dir()
    manifest = theme_packs.read_pack(user_dir, theme)
    drawn = theme_packs.drawn_assets(user_dir, theme)
    description = manifest.get("description") or ""
    rows = [
        {
            "asset": asset,
            "drawn": asset.filename in drawn,
            "prompt": theme_catalog.prompt_for(asset, description),
            # This pack's picture, not the one the page happens to be
            # dressed in: an admin editing one theme while wearing another
            # would otherwise be shown the wrong book entirely.
            "src": _asset_url(theme, asset.filename, user_dir),
        }
        for asset in theme_catalog.CATALOG
    ]
    return render_template(
        "theme_assets.html",
        theme=theme,
        pack=manifest | {"name": theme},
        rows=rows,
        drawn_count=len(drawn),
        total=len(theme_catalog.CATALOG),
    )


@bp.route("/themes/<theme>/pictures/<filename>", methods=["POST"])
@admin_required_in_accounts_mode
def upload_theme_asset(theme, filename):
    _pack_or_404(theme)
    upload = request.files.get("file")
    if upload is None or not upload.filename:
        flash(_("Choose a picture first."), "error")
    else:
        try:
            theme_packs.save_asset(_user_dir(), theme, filename, upload.stream)
        except theme_packs.PackError as error:
            flash(str(error), "error")
    return redirect(url_for("pages.theme_assets", theme=theme) + f"#{filename}")


@bp.route("/themes/<theme>/pictures/<filename>/remove", methods=["POST"])
@admin_required_in_accounts_mode
def remove_theme_asset(theme, filename):
    _pack_or_404(theme)
    theme_packs.remove_asset(_user_dir(), theme, filename)
    return redirect(url_for("pages.theme_assets", theme=theme) + f"#{filename}")


@bp.route("/themes/<theme>/delete", methods=["POST"])
@admin_required_in_accounts_mode
def delete_theme(theme):
    _pack_or_404(theme)
    if theme_packs.delete_pack(_user_dir(), theme):
        flash(_("Theme deleted."), "success")
    else:
        flash(_("That theme could not be deleted."), "error")
    return redirect(url_for("pages.themes_page"))
