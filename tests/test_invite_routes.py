"""Tests for FEATURES.md F39's HTTP surface: an admin issuing/withdrawing
an invite, the public /invite/<token> acceptance flow, and the
STORYBOOK_OPEN_REQUESTS variant of /request-account."""

import pytest

from app import accounts, invites, people
from tests.conftest import _bootstrap_admin, _login, _people_dir, _request_account


@pytest.fixture
def accounts_app(app_factory):
    return app_factory(ACCOUNTS_ENABLED=True)


@pytest.fixture
def accounts_client(accounts_app):
    return accounts_app.test_client()


@pytest.fixture
def admin_client(accounts_client):
    """A logged-in admin — the bootstrap first-request path, then a login."""
    _bootstrap_admin(accounts_client)
    _login(accounts_client, "papa", "hunter22")
    return accounts_client


def _invite_url(resp):
    """Pull the just-created invitation URL out of admin_invite.html."""
    html = resp.data.decode()
    start = html.index("http://") if "http://" in html else html.index("/invite/")
    end = html.index("<", start)
    return html[start:end].strip()


def _token(url):
    return url.rsplit("/invite/", 1)[1]


def _create_invite(client, **extra):
    data = {"new_person_name": "Mamie Rose", "role": "family"}
    data.update(extra)
    return client.post("/admin/accounts/invite", data=data)


# --- admin side --------------------------------------------------------------


def test_invite_page_is_admin_only(accounts_client):
    _bootstrap_admin(accounts_client)
    people_dir = _people_dir(accounts_client.application)
    slug = people.create_person(people_dir, "Mamie Rose")
    accounts.create_account(people_dir, slug, "mamie", "hunter22", "family")

    _login(accounts_client, "mamie", "hunter22")
    assert accounts_client.get("/admin/accounts/invite").status_code == 404
    assert accounts_client.post("/admin/accounts/invite").status_code == 404


def test_invite_page_404s_for_a_logged_out_visitor(accounts_client):
    resp = accounts_client.get("/admin/accounts/invite")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_admin_creates_an_invite_for_a_new_person(admin_client):
    resp = _create_invite(admin_client, new_person_name="Mamie Rose")
    assert resp.status_code == 200
    url = _invite_url(resp)
    assert "/invite/" in url

    people_dir = _people_dir(admin_client.application)
    assert invites.find_by_token(people_dir, _token(url)) is not None
    assert any(p.name == "Mamie Rose" for p in people.list_people(people_dir))


def test_admin_creates_an_invite_for_an_existing_person(admin_client):
    people_dir = _people_dir(admin_client.application)
    slug = people.create_person(people_dir, "Mamie Rose")

    resp = _create_invite(admin_client, person_slug=slug, new_person_name="")
    invite = invites.find_by_token(people_dir, _token(_invite_url(resp)))
    assert invite.person_slug == slug


def test_the_token_is_shown_once_and_never_again(admin_client):
    url = _invite_url(_create_invite(admin_client))
    assert _token(url) not in admin_client.get("/admin/accounts/invite").data.decode()
    assert _token(url) not in admin_client.get("/admin/accounts").data.decode()


def test_an_invited_person_drops_out_of_the_picker(admin_client):
    people_dir = _people_dir(admin_client.application)
    slug = people.create_person(people_dir, "Mamie Rose")
    assert slug in admin_client.get("/admin/accounts/invite").data.decode()

    _create_invite(admin_client, person_slug=slug, new_person_name="")
    assert slug not in admin_client.get("/admin/accounts/invite").data.decode()


def test_invite_rejects_a_bad_role(admin_client):
    resp = _create_invite(admin_client, role="superuser")
    assert "Invalid role." in resp.data.decode()
    assert invites.list_all_active(_people_dir(admin_client.application)) == []


def test_invite_needs_a_person(admin_client):
    resp = _create_invite(admin_client, new_person_name="", person_slug="")
    assert "Pick an existing family member" in resp.data.decode()


def test_active_invites_are_listed_on_the_accounts_page(admin_client):
    _create_invite(admin_client, new_person_name="Mamie Rose")
    html = admin_client.get("/admin/accounts").data.decode()
    assert "Invitations sent" in html
    assert "Mamie Rose" in html


def test_admin_can_withdraw_an_invite(admin_client):
    people_dir = _people_dir(admin_client.application)
    url = _invite_url(_create_invite(admin_client))
    invite = invites.find_by_token(people_dir, _token(url))

    resp = admin_client.post(
        f"/admin/accounts/invite/{invite.person_slug}/{invite.id}/revoke"
    )
    assert resp.status_code == 302
    assert invites.list_all_active(people_dir) == []
    assert admin_client.get(url).status_code == 404


def test_withdrawing_an_unknown_invite_404s(admin_client):
    assert admin_client.post("/admin/accounts/invite/nobody/nope/revoke").status_code == 404


# --- the recipient's side ----------------------------------------------------


def test_accept_page_names_the_person_it_was_issued_for(accounts_client, admin_client):
    url = _invite_url(_create_invite(admin_client, new_person_name="Mamie Rose"))
    # A fresh, logged-out client — the recipient is not an account holder yet.
    resp = accounts_client.application.test_client().get(url)
    assert resp.status_code == 200
    assert "Mamie Rose" in resp.data.decode()


def test_recipient_chooses_their_own_username_and_password(accounts_app, admin_client):
    url = _invite_url(_create_invite(admin_client, new_person_name="Mamie Rose"))
    recipient = accounts_app.test_client()

    resp = recipient.post(
        url, data={"username": "mamie", "password": "hunter22", "confirm_password": "hunter22"}
    )
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]

    people_dir = _people_dir(accounts_app)
    account = accounts.get_account_by_username(people_dir, "mamie")
    assert account is not None
    assert account.role == "family"
    # The credentials really work, which is the whole point of the hand-off.
    assert _login(recipient, "mamie", "hunter22").status_code == 302


def test_accepting_does_not_log_anyone_in(accounts_app, admin_client):
    url = _invite_url(_create_invite(admin_client))
    recipient = accounts_app.test_client()
    recipient.post(
        url, data={"username": "mamie", "password": "hunter22", "confirm_password": "hunter22"}
    )
    assert recipient.get("/", follow_redirects=False).status_code == 302


def test_an_invite_works_only_once(accounts_app, admin_client):
    url = _invite_url(_create_invite(admin_client))
    first = accounts_app.test_client()
    first.post(
        url, data={"username": "mamie", "password": "hunter22", "confirm_password": "hunter22"}
    )

    second = accounts_app.test_client()
    resp = second.post(
        url, data={"username": "mamie2", "password": "hunter22", "confirm_password": "hunter22"}
    )
    assert resp.status_code == 404
    assert accounts.get_account_by_username(_people_dir(accounts_app), "mamie2") is None


def test_mismatched_passwords_are_rejected_without_burning_the_invite(accounts_app, admin_client):
    url = _invite_url(_create_invite(admin_client))
    recipient = accounts_app.test_client()

    resp = recipient.post(
        url, data={"username": "mamie", "password": "hunter22", "confirm_password": "hunter23"}
    )
    assert resp.status_code == 200
    assert "match" in resp.data.decode().lower()
    assert accounts.get_account_by_username(_people_dir(accounts_app), "mamie") is None
    # Still redeemable — a typo shouldn't cost the recipient their invitation.
    assert recipient.get(url).status_code == 200


def test_a_taken_username_is_rejected_without_burning_the_invite(accounts_app, admin_client):
    url = _invite_url(_create_invite(admin_client))
    recipient = accounts_app.test_client()

    resp = recipient.post(
        url, data={"username": "papa", "password": "hunter22", "confirm_password": "hunter22"}
    )
    assert resp.status_code == 200
    assert "taken" in resp.data.decode().lower()
    assert recipient.get(url).status_code == 200


def test_an_unknown_token_is_not_valid(accounts_client):
    assert accounts_client.get("/invite/not-a-real-token").status_code == 404


def test_invite_routes_404_when_accounts_are_disabled(auth_client):
    assert auth_client.get("/invite/anything").status_code == 404
    assert auth_client.get("/admin/accounts/invite").status_code == 404


# --- open requests -----------------------------------------------------------


@pytest.fixture
def open_client(app_factory):
    return app_factory(ACCOUNTS_ENABLED=True, OPEN_REQUESTS_ENABLED=True).test_client()


def test_open_requests_off_still_demands_the_code(accounts_client):
    _request_account(accounts_client, invite_code="")
    assert accounts.list_pending(_people_dir(accounts_client.application).parent) == []


def test_open_requests_lets_someone_ask_without_a_code(open_client):
    resp = _request_account(open_client, username="mamie", invite_code="")
    assert "review your request" in resp.data.decode()

    stories_dir = open_client.application.config["STORIES_DIR"]
    assert [p.username for p in accounts.list_pending(stories_dir)] == ["mamie"]


def test_a_codeless_request_never_becomes_the_bootstrap_admin(open_client):
    """The whole risk of opening the form up: on a book with no accounts
    yet, the first request auto-approves as admin. It must only do that for
    someone who proved they know the invite code."""
    _request_account(open_client, username="stranger", invite_code="")

    stories_dir = open_client.application.config["STORIES_DIR"]
    assert accounts.list_accounts(_people_dir(open_client.application)) == []
    assert [p.username for p in accounts.list_pending(stories_dir)] == ["stranger"]


def test_the_code_still_bootstraps_an_admin_when_requests_are_open(open_client):
    _request_account(open_client, username="papa", invite_code="test-password")
    accounts_list = accounts.list_accounts(_people_dir(open_client.application))
    assert [a.username for a in accounts_list] == ["papa"]
    assert accounts_list[0].role == "admin"


def test_a_wrong_code_is_still_wrong_when_requests_are_open(open_client):
    """Omitting the code is newly allowed; getting it wrong is not — else
    the code would be freely guessable one attempt at a time."""
    resp = _request_account(open_client, username="mamie", invite_code="not-the-password")
    assert "Incorrect invite code." in resp.data.decode()

    stories_dir = open_client.application.config["STORIES_DIR"]
    assert accounts.list_pending(stories_dir) == []


def test_open_requests_are_capped(open_client, monkeypatch):
    monkeypatch.setattr(accounts, "MAX_PENDING_REQUESTS", 2)
    for i in range(2):
        _request_account(open_client, username=f"person-{i}", display_name=f"P{i}", invite_code="")

    resp = _request_account(open_client, username="one-more", invite_code="")
    assert "too many requests" in resp.data.decode()

    stories_dir = open_client.application.config["STORIES_DIR"]
    assert len(accounts.list_pending(stories_dir)) == 2


# --- duplicate hints ---------------------------------------------------------


def test_review_page_warns_about_a_person_who_can_already_log_in(admin_client):
    """The bootstrap admin is bound to a Person named "Papa"; a second
    request under the same name is the duplicate this hint exists for."""
    _request_account(admin_client, username="papa2", display_name="Papa")

    html = admin_client.get("/admin/accounts/pending/papa2").data.decode()
    assert "can already log in" in html


def test_review_page_suggests_binding_to_an_existing_person(admin_client):
    people.create_person(_people_dir(admin_client.application), "Mamie Rose")
    _request_account(admin_client, username="mamie", display_name="Mamie Rose")

    html = admin_client.get("/admin/accounts/pending/mamie").data.decode()
    assert "already in the book" in html


def test_accounts_page_flags_a_duplicate_request(admin_client):
    _request_account(admin_client, username="papa2", display_name="Papa")
    html = admin_client.get("/admin/accounts").data.decode()
    assert "already has an account" in html


def test_an_unrelated_request_gets_no_warning(admin_client):
    _request_account(admin_client, username="mamie", display_name="Mamie Rose")
    html = admin_client.get("/admin/accounts/pending/mamie").data.decode()
    assert "already in the book" not in html
