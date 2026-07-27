"""Login/logout and the @login_required / @admin_required /
@delegate_required decorators.

Two modes, selected by STORYBOOK_ACCOUNTS (FEATURES.md F19):

- Off (default): a single shared password, no accounts, no roles — exactly
  the original behavior, untouched.
- On: per-person username/password accounts (app/accounts.py), with an
  admin role. STORYBOOK_PASSWORD never logs anyone in here — once accounts
  mode is on, it's only the invite code required on pages.request_account,
  and the very first submitted request auto-approves as admin (see there).

A third, much narrower kind of session exists alongside those two: a
delegate session (Phase 3 write-links, app/write_links.py), opened by
visiting a bearer-token link a real account holder issued. It never sets
session["authed"], so login_required rejects it exactly like a logged-out
visitor — it only unlocks the handful of routes gated by
@delegate_required instead.
"""

import hmac
import time
from functools import wraps

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import accounts, i18n, storage, write_links
from .i18n import _, _n

bp = Blueprint("auth", __name__)


def _safe_next_url(next_url):
    """Only ever redirect to a local path, never an external URL."""
    if not next_url or not next_url.startswith("/") or next_url.startswith("//") or "\\" in next_url:
        return url_for("pages.timeline")
    return next_url


def throttle_key():
    """What the brute-force throttle counts failures against: the client
    IP (via ProxyFix when STORYBOOK_TRUSTED_PROXIES is set, so a reverse
    proxy doesn't collapse the whole internet into one key)."""
    return request.remote_addr or "unknown"


def throttled_response(template, **context):
    """The 429 page for a blocked client: no password check ran, no
    thread slept, and Retry-After says when to come back."""
    throttle = current_app.extensions["failure_throttle"]
    retry_after = throttle.retry_after(throttle_key(), time.time())
    minutes = max(1, (retry_after + 59) // 60)
    flash(
        _n(
            "Too many attempts. Try again in about {n} minute.",
            "Too many attempts. Try again in about {n} minutes.",
            minutes,
        ),
        "error",
    )
    response = current_app.make_response(render_template(template, **context))
    response.status_code = 429
    response.headers["Retry-After"] = str(retry_after)
    return response


def set_session_for_account(account):
    """Populate a fresh session for a real (non-delegate) account — shared
    by login() and any route that changes the current user's own password
    (which bumps session_version and would otherwise immediately lock the
    very session that just requested the change)."""
    session.clear()
    session["authed"] = True
    session["account_username"] = account.username
    session["person_slug"] = account.person_slug
    session["role"] = account.role
    session["session_version"] = account.session_version
    session.permanent = True


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("authed"):
            return redirect(url_for("auth.login", next=request.path))
        if current_app.config["ACCOUNTS_ENABLED"] and session.get("account_username"):
            # Sessions are client-signed cookies with no server-side store,
            # so a disabled account, or one whose password just changed,
            # must be re-checked on every request to take effect
            # immediately rather than whenever its 90-day cookie expires.
            people_dir = storage.people_dir(current_app.config["STORIES_DIR"])
            account = accounts.get_account_by_username(people_dir, session["account_username"])
            if (
                account is None
                or account.status != "active"
                or session.get("session_version") != account.session_version
            ):
                session.clear()
                return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if session.get("role") != "admin":
            abort(404)
        return view(*args, **kwargs)

    return login_required(wrapped_view)


def delegate_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        person_slug = session.get("delegate_person_slug")
        link_id = session.get("delegate_link_id")
        if not person_slug or not link_id:
            abort(404)
        people_dir = storage.people_dir(current_app.config["STORIES_DIR"])
        link = write_links.get_link(people_dir, person_slug, link_id)
        if link is None or not write_links.is_link_valid(link):
            # Re-checked every request, same reasoning as login_required's
            # disabled-account check: a revoked/expired/used-up link must
            # stop working immediately, not just refuse new /w/<token> hits.
            session.clear()
            abort(404)
        return view(*args, **kwargs)

    return wrapped_view


@bp.route("/login", methods=["GET", "POST"])
def login():
    accounts_enabled = current_app.config["ACCOUNTS_ENABLED"]
    no_accounts_yet = accounts_enabled and not accounts.any_accounts_exist(
        storage.people_dir(current_app.config["STORIES_DIR"])
    )

    if request.method == "POST":
        throttle = current_app.extensions["failure_throttle"]
        key = throttle_key()
        # Checked before the password so a blocked client learns nothing
        # from this request — not even whether the password was right.
        if throttle.is_blocked(key, time.time()):
            return throttled_response(
                "login.html",
                accounts_enabled=accounts_enabled,
                no_accounts_yet=no_accounts_yet,
            )
        if accounts_enabled:
            people_dir = storage.people_dir(current_app.config["STORIES_DIR"])
            username = request.form.get("username", "").strip().lower()
            password = request.form.get("password", "")
            account = accounts.verify_login(people_dir, username, password)
            if account:
                throttle.clear(key)
                set_session_for_account(account)
                return redirect(_safe_next_url(request.args.get("next", "")))
            throttle.register_failure(key, time.time())
            time.sleep(1)
            flash(_("Incorrect username or password."), "error")
        else:
            password = request.form.get("password", "")
            correct = hmac.compare_digest(password, current_app.config["PASSWORD"])
            if correct:
                throttle.clear(key)
                session.clear()
                session["authed"] = True
                session.permanent = True
                return redirect(_safe_next_url(request.args.get("next", "")))
            throttle.register_failure(key, time.time())
            time.sleep(1)
            flash(_("Incorrect password."), "error")

    return render_template(
        "login.html", accounts_enabled=accounts_enabled, no_accounts_yet=no_accounts_yet
    )


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.route("/language/<lang>", methods=["POST"])
def set_language(lang):
    """Remember a language choice (FEATURES.md F38).

    Deliberately not `@login_required`: the login page has the picker too,
    so someone who doesn't read English can switch before typing a
    password. A cookie rather than the session because it must survive
    logging out, and rather than a per-account setting because it has to
    work before there is an account.

    POST-only and CSRF-protected like every other state change, and the
    redirect target goes through the same allowlist as the login `next`,
    so this can't be turned into an open redirect.
    """
    if not i18n.is_supported(lang):
        abort(404)
    response = redirect(_safe_next_url(request.form.get("next", "")))
    response.set_cookie(
        i18n.COOKIE_NAME,
        lang,
        max_age=i18n.COOKIE_MAX_AGE,
        httponly=False,  # harmless to JS and lets a future picker read it
        samesite="Lax",
        secure=current_app.config["SESSION_COOKIE_SECURE"],
    )
    return response
