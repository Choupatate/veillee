import os
import re
import secrets
from datetime import date, timedelta
from pathlib import Path

from flask import Flask, g, jsonify, render_template, request, url_for
from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFError
from werkzeug.middleware.proxy_fix import ProxyFix

from . import secret_key as secret_key_file
from . import settings, themes
from .throttle import DEFAULT_LIMIT, DEFAULT_WINDOW_SECONDS, FailureThrottle

MAX_CONTENT_LENGTH = 128 * 1024 * 1024

# Everything the app loads is served by the app itself (the no-CDN rule),
# so the Content-Security-Policy can be strict: no external hosts at all,
# and no inline <script> anywhere (base.html's theme boot lives in
# static/js/theme-boot.js for exactly this reason). This is real
# defense-in-depth: story bodies are rendered with |safe by design, and
# with this policy a <script> smuggled into one is refused by the browser.
# blob: appears because the camera (F34), the portrait cropper (F18), and
# the instant preview all show not-yet-uploaded media via createObjectURL;
# data: because the vendored Toast UI CSS embeds its icons that way.
# style-src allows inline styles for the --author-color / --photo-sepia
# custom-property attributes templates set.
_CSP = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data: blob:; "
    "media-src 'self' blob:; "
    "connect-src 'self'; "
    "object-src 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "frame-ancestors 'none'"
)

_HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def _parse_authors(value):
    """Parse STORYBOOK_AUTHORS ("Name:#hex,Name:#hex") into an ordered list
    of {"name": ..., "color": ...} dicts. Raises RuntimeError on malformed
    input so misconfiguration fails at startup, not at first page render."""
    authors = []
    seen = set()
    for entry in (value or "").split(","):
        entry = entry.strip()
        if not entry:
            continue
        name, _, color = entry.partition(":")
        name = name.strip()
        color = color.strip()
        if not name or "," in name or ":" in name or not _HEX_COLOR_RE.match(color):
            raise RuntimeError(
                f"Invalid STORYBOOK_AUTHORS entry {entry!r}. Expected comma-separated "
                'Name:#hexcolor pairs, e.g. STORYBOOK_AUTHORS="Papa:#d9a441,Maman:#7ba7d9"'
            )
        if name in seen:
            raise RuntimeError(f"Duplicate author name in STORYBOOK_AUTHORS: {name!r}")
        seen.add(name)
        authors.append({"name": name, "color": color})
    return authors


def _parse_theme(value):
    """Parse STORYBOOK_THEME (the name of a folder under
    `app/static/themes/`). Raises RuntimeError on an unknown pack rather
    than quietly serving the default one — a book whose art silently
    reverted would be a puzzle to debug, and the fix is one word."""
    if not value:
        return themes.DEFAULT_THEME
    value = value.strip()
    if not themes.is_valid_theme(value):
        known = ", ".join(themes.available_themes()) or "(none found)"
        raise RuntimeError(
            f"Unknown STORYBOOK_THEME {value!r}. Available themes: {known}"
        )
    return value


def _parse_birthdate(value):
    """Parse STORYBOOK_BIRTHDATE ("YYYY-MM-DD"). Raises RuntimeError on a
    malformed value so misconfiguration fails at startup (like STORYBOOK_AUTHORS)."""
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        raise RuntimeError(
            f"Invalid STORYBOOK_BIRTHDATE {value!r}. Expected an ISO date, e.g. "
            'STORYBOOK_BIRTHDATE="2023-06-18"'
        )


def create_app(test_config=None):
    app = Flask(__name__)

    stories_dir = os.environ.get("STORYBOOK_STORIES_DIR", "./stories")
    password = os.environ.get("STORYBOOK_PASSWORD")
    secret_key = os.environ.get("STORYBOOK_SECRET_KEY")
    cookie_secure = os.environ.get("STORYBOOK_COOKIE_SECURE") == "1"
    authors = _parse_authors(os.environ.get("STORYBOOK_AUTHORS"))
    birthdate = _parse_birthdate(os.environ.get("STORYBOOK_BIRTHDATE"))
    title_override = os.environ.get("STORYBOOK_TITLE") or None
    child_slug = os.environ.get("STORYBOOK_CHILD") or None
    accounts_enabled = os.environ.get("STORYBOOK_ACCOUNTS") == "1"
    open_requests = os.environ.get("STORYBOOK_OPEN_REQUESTS") == "1"
    trusted_proxies = int(os.environ.get("STORYBOOK_TRUSTED_PROXIES") or 0)
    default_language = os.environ.get("STORYBOOK_LANGUAGE") or None
    theme = _parse_theme(os.environ.get("STORYBOOK_THEME"))

    # F59: a book with a password needs a stable signing key, and asking
    # the person installing this to produce one by hand is how weak ones
    # get typed. The environment still wins when it has an answer; with no
    # answer, keep a generated one in the data folder. See secret_key.py.
    if password and not secret_key and not test_config:
        secret_key = secret_key_file.load_or_create(stories_dir)
        if not secret_key:
            raise RuntimeError(
                f"Could not read or write {secret_key_file.SECRET_KEY_FILENAME} in "
                f"{stories_dir!r}, and STORYBOOK_SECRET_KEY is not set. Make that "
                "directory writable (in Docker, mount a volume at the stories path), "
                "or set STORYBOOK_SECRET_KEY yourself: "
                "python -c 'import secrets; print(secrets.token_hex(32))'"
            )

    app.config.update(
        STORIES_DIR=Path(stories_dir).resolve(),
        PASSWORD=password or "dev",
        SECRET_KEY=secret_key or secrets.token_hex(32),
        DEV_MODE=password is None,
        AUTHORS=authors,
        BIRTHDATE=birthdate,
        TITLE=title_override,
        CHILD_SLUG=child_slug,
        ACCOUNTS_ENABLED=accounts_enabled,
        OPEN_REQUESTS_ENABLED=open_requests,
        PERMANENT_SESSION_LIFETIME=timedelta(days=90),
        MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=cookie_secure,
        DEFAULT_LANGUAGE=default_language,
        THEME=theme,
        LOGIN_ATTEMPT_LIMIT=DEFAULT_LIMIT,
        LOGIN_ATTEMPT_WINDOW=DEFAULT_WINDOW_SECONDS,
    )

    if test_config:
        app.config.update(test_config)

    # Behind a reverse proxy (the normal NAS setup), remote_addr is the
    # proxy's address, which would make the login throttle treat the whole
    # internet as one client — the first attacker to trip it would lock the
    # family out too. STORYBOOK_TRUSTED_PROXIES=<count of proxies in front>
    # tells the app to trust that many X-Forwarded-For / X-Forwarded-Proto
    # hops. Off by default: trusting those headers when no proxy sets them
    # would let clients spoof their IP past the throttle.
    if trusted_proxies > 0:
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=trusted_proxies,
            x_proto=trusted_proxies,
            x_host=trusted_proxies,
        )

    # One throttle shared by every password-bearing endpoint (login and,
    # in accounts mode, the invite-code form) — they guard the same secret.
    app.extensions["failure_throttle"] = FailureThrottle(
        limit=app.config["LOGIN_ATTEMPT_LIMIT"],
        window_seconds=app.config["LOGIN_ATTEMPT_WINDOW"],
    )

    app.config["STORIES_DIR"] = Path(app.config["STORIES_DIR"])
    app.config["STORIES_DIR"].mkdir(parents=True, exist_ok=True)

    from . import auth, i18n, routes_api, storage, timeline, views

    # Every page route registers onto the one `pages` blueprint `views.py`
    # defines, so which of these six files a route's code sits in never
    # reaches `url_for("pages.xxx")`. They are imported for that side
    # effect and nothing else — which is why they are imported here rather
    # than from the bottom of one of them, where they used to be: a file
    # that both defines the blueprint and imports everything registering
    # onto it is a cycle, and it was one.
    from . import (  # noqa: F401
        routes_accounts,
        routes_api_people,
        routes_groups,
        routes_pages,
        routes_people,
        routes_settings,
        routes_themes,
    )

    csrf = CSRFProtect(app)
    # The only CSRF exemption in the app, kept here rather than as a
    # decorator so that "what is unprotected" is one grep of the factory.
    # /share is posted by the phone's share sheet (F57), which builds the
    # request itself and cannot be handed a token; the route checks
    # Sec-Fetch-Site instead and creates only a draft.
    csrf.exempt(routes_pages.share_target)

    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    app.register_blueprint(routes_api.bp)

    @app.before_request
    def resolve_language():
        """One language per request (F38): the reader's own choice from
        the picker, else their browser's preference, else the book's own
        default (STORYBOOK_LANGUAGE), else English."""
        # F51: what the family has set from inside the book, over the top
        # of what the server was started with. Once per request, so a save
        # takes effect immediately and no render reads the file twice.
        #
        # **This has to come first.** `settings.book()` falls back to the
        # raw config while `g.book` is unset, which is right outside a
        # request and silently wrong here: computing the language above
        # this line read DEFAULT_LANGUAGE from the environment, so the
        # Language field in Settings did nothing at all while the title
        # and theme from the same file worked.
        g.book = settings.effective(app.config, app.config["STORIES_DIR"])
        g.lang = i18n.pick_language(
            request.cookies.get(i18n.COOKIE_NAME),
            request.headers.get("Accept-Language"),
            settings.book("DEFAULT_LANGUAGE"),
        )
        # F48: the book's pack, unless this browser asked for another one.
        # F50: which may be one the family made, living in the data folder.
        g.theme = themes.pick_theme(
            request.cookies.get(themes.COOKIE_NAME),
            settings.book("THEME"),
            themes.user_themes_dir(app.config["STORIES_DIR"]),
        )

    # F46: templates ask for a picture by name, never by folder, so a theme
    # pack can replace any of them — and inherit the default pack's for
    # everything it hasn't drawn yet.
    def current_theme():
        # `g` is unset for anything rendered outside a request (and before
        # before_request has run), where the book's own pack is the answer.
        return getattr(g, "theme", None) or settings.book("THEME") or app.config["THEME"]

    def user_themes_dir():
        return themes.user_themes_dir(app.config["STORIES_DIR"])

    def theme_img(filename):
        # F50: a made pack's pictures are files in the data folder, not
        # static assets, so where the picture comes from decides how its
        # URL is built. The fallback is already applied by `image_ref`.
        kind, pack, name = themes.image_ref(current_theme(), filename, user_themes_dir())
        if kind == "user":
            return url_for("pages.theme_media", theme=pack, filename=name)
        return url_for("static", filename=f"themes/{pack}/img/{name}")

    app.jinja_env.globals["theme_img"] = theme_img
    app.jinja_env.globals["is_sealed"] = timeline.is_sealed
    app.jinja_env.globals["thumb_filename"] = storage.thumb_filename
    app.jinja_env.globals["_"] = i18n._
    app.jinja_env.globals["_n"] = i18n._n
    app.jinja_env.globals["LANGUAGES"] = i18n.LANGUAGES
    app.jinja_env.globals["SCHEME_LABELS"] = themes.SCHEME_LABELS

    # Templates call age_label(birthdate, date) with no language argument;
    # bind the current request's language here so every caller localizes.
    app.jinja_env.globals["age_label"] = lambda b, d: i18n.age_label(
        b, d, i18n.current_language()
    )

    def _date_filter(style):
        return lambda value: i18n.format_date(value, i18n.current_language(), style)

    for name, style in (
        ("longdate", "long"), ("shortdate", "short"),
        ("shortdateyear", "short_year"), ("monthyear", "month_year"),
    ):
        app.jinja_env.filters[name] = _date_filter(style)
    app.jinja_env.filters["datetimestamp"] = lambda v: i18n.format_datetime(
        v, i18n.current_language()
    )

    def _group_names(app):
        """`{slug: name}` for the audience marker, empty outside accounts
        mode so the whole thing stays invisible on a single-password
        install. Reads one small JSON file; the account-mode pages already
        scan `people/` per request, so this is the same cost class."""
        if not app.config["ACCOUNTS_ENABLED"]:
            return {}
        from . import groups

        return {g.slug: g.name for g in groups.list_groups(app.config["STORIES_DIR"])}

    @app.context_processor
    def inject_title():
        # STORYBOOK_TITLE always wins when set (a family's own chosen name,
        # e.g. "Le livre de Milo", isn't ours to translate); absent that,
        # the app's own default name follows the reader's language too.
        return {
            "app_title": settings.book("TITLE") or i18n._("Veillée"),
            # None for the default pack, whose colours are main.css's own.
            "theme_stylesheet": themes.stylesheet_url_path(current_theme()),
            # F50: a made pack has no stylesheet on disk — its colours are
            # data, rendered by a route.
            "theme_stylesheet_url": (
                url_for("pages.theme_css", theme=current_theme())
                if themes.is_user_theme(current_theme(), user_themes_dir())
                else None
            ),
            # Which colour schemes the pack offers, for the nav toggle and
            # for theme-boot.js's check of what was last stored (F46).
            "color_schemes": themes.color_schemes(current_theme(), user_themes_dir()),
            # F48: the nav picker. A list of dicts rather than names so the
            # template never reaches into themes.py per pack, and a
            # one-pack install renders no picker at all.
            "current_theme": current_theme(),
            "theme_packs": [
                {
                    "name": name,
                    "label": themes.label(name, user_themes_dir()),
                    "swatch": themes.swatch(name, user_themes_dir()),
                }
                for name in themes.available_themes(user_themes_dir())
            ],
            "current_language": i18n.current_language(),
            "js_strings": i18n.js_strings(i18n.current_language()),
            # slug -> display name for audience groups (F40 Phase 2). A
            # context processor rather than a per-route argument because
            # the "kept to X" marker rides along with the shared story
            # partial, which four different routes render — threading it
            # through each one is four chances to forget, and forgetting
            # means a scoped story that looks public to its own writer.
            "group_names": _group_names(app),
        }

    @app.after_request
    def security_headers(response):
        """Hardening headers on every response (F36). Static files keep
        their long cache but get the same protective headers."""
        response.headers.setdefault("Content-Security-Policy", _CSP)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "same-origin")
        if app.config["SESSION_COOKIE_SECURE"]:
            # Only meaningful (and only sent) when the operator says the
            # app is served over HTTPS; a year, no preload — reversible.
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000"
            )
        content_type = response.headers.get("Content-Type", "")
        if content_type.startswith("text/html"):
            # Pages are personal content behind a login: never written to
            # a disk cache or held by an intermediary. (Photos keep their
            # long cache — see below — this is about the pages themselves.)
            response.headers["Cache-Control"] = "no-store"
        elif "max-age" in response.headers.get("Cache-Control", ""):
            # Cached media and static files are for this browser only,
            # never for a shared cache along the way.
            response.cache_control.private = True
            response.cache_control.public = False
        return response

    def _error_page(status, heading, message, api_message=None, hint=None):
        """Every error a family member can hit must render through
        base.html — it carries the viewport meta and the stylesheet. A bare
        Werkzeug error page has neither, so on a phone it lays out at 980px
        and reads as "the site is broken" (F37)."""
        if request.path.startswith("/api/"):
            return jsonify({"error": api_message or message}), status
        return render_template(
            "error.html", heading=heading, message=message, hint=hint
        ), status

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": i18n._("Not found.")}), 404
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def too_large(error):
        return _error_page(
            413,
            i18n._("That file is too big"),
            i18n._(
                "The upload limit is 128 MB. Try a smaller file, or copy it "
                "straight into the stories folder instead."
            ),
            api_message=i18n._("File too large (max 128 MB)."),
        )

    @app.errorhandler(CSRFError)
    def csrf_error(error):
        """A CSRF failure is nearly always one of two ordinary things: a
        page left open until its session expired, or a reverse proxy that
        isn't passing the browser's real host through. Say so, instead of
        Werkzeug's bare "Bad Request"."""
        referrer_mismatch = "referrer" in (error.description or "").lower()
        if referrer_mismatch:
            hint = i18n._(
                "This usually means the reverse proxy in front of this app "
                "isn't forwarding the address you typed. Whoever set it up "
                "should check that it sends X-Forwarded-Host and "
                "X-Forwarded-Proto, and that STORYBOOK_TRUSTED_PROXIES is set."
            )
        else:
            hint = None
        return _error_page(
            400,
            i18n._("That page had gone stale"),
            i18n._(
                "For safety this app refuses a form it can't match to your "
                "current session. Log in again and redo that last step — "
                "nothing was saved or lost."
            ),
            api_message=i18n._("Your session expired. Reload the page and try again."),
            hint=hint,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return _error_page(
            400,
            i18n._("Something was wrong with that request"),
            i18n._(
                "The app couldn't make sense of what the browser sent. "
                "Reload the page and try again."
            ),
        )

    @app.errorhandler(403)
    def forbidden(error):
        return _error_page(
            403,
            i18n._("Not allowed"),
            i18n._("You don't have access to that."),
        )

    @app.errorhandler(429)
    def too_many_requests(error):
        return _error_page(
            429,
            i18n._("Too many attempts"),
            i18n._("Wait a few minutes and try again."),
        )

    @app.errorhandler(500)
    def server_error(error):
        return _error_page(
            500,
            i18n._("Something went wrong"),
            i18n._(
                "That's a fault in the app, not anything you did. Your stories "
                "are files on disk and are unaffected."
            ),
        )

    return app
