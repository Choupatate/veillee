"""Tests for FEATURES.md F39's data layer: app/invites.py (admin-issued
account invites) and the two additions to app/accounts.py that go with it
— the pending-queue cap and the duplicate-name hint."""

from datetime import datetime, timedelta

import pytest

from app import accounts, invites, people, storage


@pytest.fixture
def person(people_dir):
    people_dir.mkdir(parents=True, exist_ok=True)
    return people.create_person(people_dir, "Mamie Rose")


# --- creating invites --------------------------------------------------------


def test_create_invite_returns_a_token_only_once(people_dir, person):
    invite, token = invites.create_invite(people_dir, person, "family")
    assert token
    assert invite.role == "family"
    assert invite.person_slug == person
    # Only the hash is persisted — the raw token appears nowhere on disk.
    stored = (people_dir / person / "invites.json").read_text()
    assert token not in stored
    assert invite.token_hash in stored


def test_invite_defaults_to_a_two_week_expiry(people_dir, person):
    invite, _token = invites.create_invite(people_dir, person, "family")
    assert invite.expires_at is not None
    days = (invite.expires_at - datetime.now()).days
    assert 12 <= days <= invites.DEFAULT_EXPIRY_DAYS


def test_invite_can_be_made_to_never_expire(people_dir, person):
    invite, _token = invites.create_invite(people_dir, person, "family", expires_in_days=None)
    assert invite.expires_at is None


def test_create_invite_rejects_an_unknown_person(people_dir):
    people_dir.mkdir(parents=True, exist_ok=True)
    with pytest.raises(FileNotFoundError):
        invites.create_invite(people_dir, "nobody", "family")


def test_create_invite_rejects_a_bad_role(people_dir, person):
    with pytest.raises(ValueError):
        invites.create_invite(people_dir, person, "superuser")


def test_create_invite_rejects_a_person_who_already_has_an_account(people_dir, person):
    accounts.create_account(people_dir, person, "mamie", "hunter22", "family")
    with pytest.raises(ValueError):
        invites.create_invite(people_dir, person, "family")


def test_reissuing_an_invite_revokes_the_previous_one(people_dir, person):
    _first, first_token = invites.create_invite(people_dir, person, "family")
    _second, second_token = invites.create_invite(people_dir, person, "family")

    # One seat, one live token: the lost link stops working the moment a
    # replacement is issued.
    assert not invites.is_invite_valid(invites.find_by_token(people_dir, first_token))
    assert invites.is_invite_valid(invites.find_by_token(people_dir, second_token))
    assert len(invites.list_all_active(people_dir)) == 1


def test_history_survives_reissuing(people_dir, person):
    invites.create_invite(people_dir, person, "family")
    invites.create_invite(people_dir, person, "family")
    assert len(invites.list_invites(people_dir, person)) == 2


# --- validity ----------------------------------------------------------------


def test_expired_invite_is_not_valid(people_dir, person):
    invite, _token = invites.create_invite(people_dir, person, "family")
    invite.expires_at = datetime.now() - timedelta(seconds=1)
    assert not invites.is_invite_valid(invite)


def test_revoked_invite_is_not_valid(people_dir, person):
    invite, token = invites.create_invite(people_dir, person, "family")
    invites.revoke_invite(people_dir, person, invite.id)
    assert not invites.is_invite_valid(invites.find_by_token(people_dir, token))


def test_revoke_unknown_invite_raises(people_dir, person):
    with pytest.raises(FileNotFoundError):
        invites.revoke_invite(people_dir, person, "not-an-id")


def test_find_by_token_ignores_an_unknown_token(people_dir, person):
    invites.create_invite(people_dir, person, "family")
    assert invites.find_by_token(people_dir, "not-the-token") is None
    assert invites.find_by_token(people_dir, "") is None


def test_malformed_invites_file_is_treated_as_none(people_dir, person):
    (people_dir / person / "invites.json").write_text("{not json")
    assert invites.list_invites(people_dir, person) == []


# --- accepting ---------------------------------------------------------------


def test_accept_invite_creates_the_account_with_the_admin_s_role(stories_dir, people_dir, person):
    invites.create_invite(people_dir, person, "admin", created_by="papa")
    _invite, token = invites.create_invite(people_dir, person, "admin", created_by="papa")

    account = invites.accept_invite(stories_dir, token, "mamie", "hunter22")

    assert account.person_slug == person
    assert account.username == "mamie"
    assert account.role == "admin"  # the admin chose it, not the recipient
    assert account.approved_by == "papa"
    assert accounts.verify_login(people_dir, "mamie", "hunter22") is not None


def test_accepting_burns_the_invite(stories_dir, people_dir, person):
    _invite, token = invites.create_invite(people_dir, person, "family")
    invites.accept_invite(stories_dir, token, "mamie", "hunter22")

    assert invites.list_all_active(people_dir) == []
    with pytest.raises(LookupError):
        invites.accept_invite(stories_dir, token, "mamie2", "hunter22")


def test_accept_rejects_a_revoked_invite(stories_dir, people_dir, person):
    invite, token = invites.create_invite(people_dir, person, "family")
    invites.revoke_invite(people_dir, person, invite.id)
    with pytest.raises(LookupError):
        invites.accept_invite(stories_dir, token, "mamie", "hunter22")


def test_accept_rejects_an_unknown_token(stories_dir, people_dir, person):
    with pytest.raises(LookupError):
        invites.accept_invite(stories_dir, "nope", "mamie", "hunter22")


def test_accept_rejects_a_username_taken_by_an_account(stories_dir, people_dir, person):
    other = people.create_person(people_dir, "Papa")
    accounts.create_account(people_dir, other, "mamie", "hunter22", "admin")
    _invite, token = invites.create_invite(people_dir, person, "family")

    with pytest.raises(ValueError):
        invites.accept_invite(stories_dir, token, "mamie", "hunter22")
    # Rejected for a fixable reason, so the invite is still usable.
    assert invites.is_invite_valid(invites.find_by_token(people_dir, token))


def test_accept_rejects_a_username_sitting_in_the_pending_queue(stories_dir, people_dir, person):
    accounts.create_pending_request(stories_dir, "mamie", "hunter22", "Someone Else")
    _invite, token = invites.create_invite(people_dir, person, "family")
    with pytest.raises(ValueError):
        invites.accept_invite(stories_dir, token, "mamie", "hunter22")


def test_accept_rejects_a_short_password(stories_dir, people_dir, person):
    _invite, token = invites.create_invite(people_dir, person, "family")
    with pytest.raises(ValueError):
        invites.accept_invite(stories_dir, token, "mamie", "short")


def test_accept_rejects_a_bad_username(stories_dir, people_dir, person):
    _invite, token = invites.create_invite(people_dir, person, "family")
    with pytest.raises(ValueError):
        invites.accept_invite(stories_dir, token, "Mamie Rose!", "hunter22")


def test_accept_refuses_once_the_person_got_an_account_another_way(
    stories_dir, people_dir, person
):
    """The window an unredeemed invite leaves open: an admin creates the
    account directly while the link is still in someone's inbox."""
    _invite, token = invites.create_invite(people_dir, person, "family")
    accounts.create_account(people_dir, person, "mamie", "hunter22", "family")

    with pytest.raises(LookupError):
        invites.accept_invite(stories_dir, token, "mamie-rose", "hunter22")


# --- the pending-queue cap ---------------------------------------------------


def test_pending_queue_is_capped(stories_dir, monkeypatch):
    monkeypatch.setattr(accounts, "MAX_PENDING_REQUESTS", 3)
    for i in range(3):
        accounts.create_pending_request(stories_dir, f"person-{i}", "hunter22", f"Person {i}")

    with pytest.raises(ValueError, match="too many requests"):
        accounts.create_pending_request(stories_dir, "one-too-many", "hunter22", "Nope")


def test_rejecting_frees_a_slot_in_a_full_queue(stories_dir, monkeypatch):
    monkeypatch.setattr(accounts, "MAX_PENDING_REQUESTS", 1)
    accounts.create_pending_request(stories_dir, "first", "hunter22", "First")
    accounts.reject_pending(stories_dir, "first")
    accounts.create_pending_request(stories_dir, "second", "hunter22", "Second")
    assert [p.username for p in accounts.list_pending(stories_dir)] == ["second"]


# --- duplicate-name hints ----------------------------------------------------


def _people(*names):
    return [
        people.Person(slug=storage.slugify(n), name=n, created=None, updated=None)
        for n in names
    ]


def test_similar_people_matches_an_exact_name():
    matches = accounts.similar_people(_people("Mamie Rose", "Papa"), "Mamie Rose")
    assert [p.name for p in matches] == ["Mamie Rose"]


def test_similar_people_folds_case_accents_and_punctuation():
    matches = accounts.similar_people(_people("Jean-Luc"), "jean luc")
    assert [p.name for p in matches] == ["Jean-Luc"]


def test_similar_people_matches_a_longer_form_of_the_same_name():
    matches = accounts.similar_people(_people("Rose"), "Mamie Rose")
    assert [p.name for p in matches] == ["Rose"]


def test_similar_people_ignores_short_coincidences():
    """"Jo" inside "Joseph" is a coincidence, not a duplicate — flagging it
    would make the hint noise the admin learns to skip."""
    assert accounts.similar_people(_people("Joseph", "Jocelyne"), "Jo") == []


def test_similar_people_ignores_unrelated_names():
    assert accounts.similar_people(_people("Mamie Rose", "Papa"), "Camille") == []


def test_similar_people_handles_an_empty_name():
    assert accounts.similar_people(_people("Papa"), "") == []
    assert accounts.similar_people(_people("Papa"), "!!!") == []
