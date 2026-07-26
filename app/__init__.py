import os
import re
import secrets
from datetime import date, timedelta
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from flask_wtf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

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
    title = os.environ.get("STORYBOOK_TITLE") or "Storybook"
    child_slug = os.environ.get("STORYBOOK_CHILD") or None
    accounts_enabled = os.environ.get("STORYBOOK_ACCOUNTS") == "1"
    trusted_proxies = int(os.environ.get("STORYBOOK_TRUSTED_PROXIES") or 0)

    if password and not secret_key and not test_config:
        raise RuntimeError(
            "STORYBOOK_SECRET_KEY must be set when STORYBOOK_PASSWORD is set. "
            "Generate one with: python -c 'import secrets; print(secrets.token_hex(32))'"
        )

    app.config.update(
        STORIES_DIR=Path(stories_dir).resolve(),
        PASSWORD=password or "dev",
        SECRET_KEY=secret_key or secrets.token_hex(32),
        DEV_MODE=password is None,
        AUTHORS=authors,
        BIRTHDATE=birthdate,
        TITLE=title,
        CHILD_SLUG=child_slug,
        ACCOUNTS_ENABLED=accounts_enabled,
        PERMANENT_SESSION_LIFETIME=timedelta(days=90),
        MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=cookie_secure,
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

    from . import auth, dates, routes_api, routes_pages, storage

    CSRFProtect(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(routes_pages.bp)
    app.register_blueprint(routes_api.bp)

    app.jinja_env.globals["is_sealed"] = storage.is_sealed
    app.jinja_env.globals["age_label"] = dates.age_label
    app.jinja_env.globals["thumb_filename"] = storage.thumb_filename

    @app.context_processor
    def inject_title():
        return {"app_title": app.config["TITLE"]}

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

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def too_large(error):
        if request.path.startswith("/api/"):
            return jsonify({"error": "File too large (max 128 MB)."}), 413
        return render_template("404.html"), 413

    return app
