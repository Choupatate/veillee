"""Claiming a fresh book (FEATURES.md F60).

F59 took the signing key out of the environment. This takes the password
out too, so that installing Veillée is running one container and opening a
browser — no `.env` to edit, and no install whose password is `changeme`
because that is what the example file said.

The security of it rests on one thing: the claim code exists only in the
machine's own logs. Most of what is tested here is that the code is
actually required, that a claimed book stops offering the page at all, and
that a book which has always had `STORYBOOK_PASSWORD` set is untouched by
every bit of this.
"""

import stat

import pytest

from app import backup, claim, create_app, settings

UNCLAIMED = {
    "TESTING": True,
    "WTF_CSRF_ENABLED": False,
    "PASSWORD_CONFIGURED": False,
    "PASSWORD": "unused",
}


@pytest.fixture
def fresh_dir(tmp_path):
    """A stories folder with nothing in it — no settings file, because a
    book nobody has claimed has certainly not been set up either."""
    d = tmp_path / "stories"
    d.mkdir()
    return d


@pytest.fixture
def unclaimed(fresh_dir):
    return create_app(test_config={"STORIES_DIR": fresh_dir, **UNCLAIMED})


@pytest.fixture
def code(fresh_dir):
    return claim.pending_code(fresh_dir)


# --- the code itself --------------------------------------------------------


def test_a_fresh_book_has_a_code(fresh_dir):
    assert len(claim.pending_code(fresh_dir)) == 12


def test_the_code_is_stable_across_restarts(fresh_dir):
    """Someone may be halfway through typing it when the container
    restarts, and two workers must print the same one."""
    assert claim.pending_code(fresh_dir) == claim.pending_code(fresh_dir)


def test_the_code_avoids_characters_that_get_misread(fresh_dir):
    """It is read off a terminal and typed into a phone."""
    assert not set(claim.pending_code(fresh_dir)) & set("IO01")


def test_the_code_file_is_not_world_readable(fresh_dir):
    claim.pending_code(fresh_dir)
    mode = (fresh_dir / claim.CLAIM_CODE_FILENAME).stat().st_mode
    assert stat.S_IMODE(mode) == 0o600


@pytest.mark.parametrize("typed", [
    "{code}", "{code_lower}", "{dashed}", "{dashed_lower}", " {dashed} ", "{spaced}",
])
def test_a_code_is_accepted_however_it_was_typed(fresh_dir, typed):
    """Dashes or not, upper case or not — a phone keyboard capitalizes the
    first letter and not the rest, and none of that is a wrong code."""
    code = claim.pending_code(fresh_dir)
    dashed = claim.formatted(code)
    variants = {
        "code": code, "code_lower": code.lower(),
        "dashed": dashed, "dashed_lower": dashed.lower(),
        "spaced": " ".join(code[i:i + 4] for i in range(0, 12, 4)),
    }
    claim.claim(fresh_dir, typed.format(**variants), "a-good-password")
    assert claim.is_claimed(fresh_dir)


def test_the_banner_shows_the_code_in_groups(fresh_dir):
    code = claim.pending_code(fresh_dir)
    assert claim.formatted(code) in claim.banner(code)
    assert claim.formatted(code).count("-") == 2


# --- claiming ---------------------------------------------------------------


def test_a_wrong_code_claims_nothing(fresh_dir, code):
    with pytest.raises(claim.ClaimError) as caught:
        claim.claim(fresh_dir, "WRON-GCOD-EXXX", "a-good-password")
    assert caught.value.reason == "code"
    assert not claim.is_claimed(fresh_dir)


def test_a_short_password_claims_nothing(fresh_dir, code):
    with pytest.raises(claim.ClaimError) as caught:
        claim.claim(fresh_dir, code, "short")
    assert caught.value.reason == "password"
    assert not claim.is_claimed(fresh_dir)


def test_a_failed_claim_leaves_the_code_usable(fresh_dir, code):
    """Getting it wrong must not brick the book — there is no way to ask
    for a second code."""
    with pytest.raises(claim.ClaimError):
        claim.claim(fresh_dir, code, "short")
    claim.claim(fresh_dir, code, "a-good-password")
    assert claim.verify_password(fresh_dir, "a-good-password")


def test_claiming_destroys_the_code(fresh_dir, code):
    claim.claim(fresh_dir, code, "a-good-password")
    assert not (fresh_dir / claim.CLAIM_CODE_FILENAME).exists()
    assert claim.pending_code(fresh_dir) is None


def test_the_code_works_exactly_once(fresh_dir, code):
    claim.claim(fresh_dir, code, "a-good-password")
    with pytest.raises(claim.ClaimError):
        claim.claim(fresh_dir, code, "someone-elses-password")
    assert claim.verify_password(fresh_dir, "a-good-password")


def test_the_password_is_stored_as_a_hash_not_a_password(fresh_dir, code):
    claim.claim(fresh_dir, code, "correct-horse")
    stored = (fresh_dir / claim.BOOK_PASSWORD_FILENAME).read_text()
    assert "correct-horse" not in stored
    assert "scrypt" in stored or "pbkdf2" in stored


def test_the_wrong_password_does_not_verify(fresh_dir, code):
    claim.claim(fresh_dir, code, "a-good-password")
    assert not claim.verify_password(fresh_dir, "not-the-password")


# --- the page ---------------------------------------------------------------


def test_every_path_leads_to_the_claim_page(unclaimed):
    client = unclaimed.test_client()
    for path in ("/", "/login", "/firsts", "/people"):
        resp = client.get(path)
        assert resp.status_code == 302, path
        assert resp.headers["Location"].endswith("/claim"), path


def test_the_claim_page_never_shows_the_code(unclaimed, fresh_dir, code):
    """It says where to find it. Printing it on the page would defeat the
    entire mechanism."""
    body = unclaimed.test_client().get("/claim").data.decode()
    assert code not in body
    assert claim.formatted(code) not in body
    assert "logs" in body


def test_claiming_through_the_page_logs_you_in_and_starts_the_wizard(unclaimed, fresh_dir, code):
    client = unclaimed.test_client()
    resp = client.post("/claim", data={"code": claim.formatted(code), "password": "a-good-password"})

    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/setup")
    assert claim.is_claimed(fresh_dir)
    with client.session_transaction() as sess:
        assert sess["authed"] is True


def test_a_claimed_book_has_no_claim_page_at_all(unclaimed, fresh_dir, code):
    client = unclaimed.test_client()
    client.post("/claim", data={"code": claim.formatted(code), "password": "a-good-password"})

    assert client.get("/claim").status_code == 404


def test_the_chosen_password_then_logs_in(unclaimed, fresh_dir, code):
    client = unclaimed.test_client()
    client.post("/claim", data={"code": claim.formatted(code), "password": "a-good-password"})
    client.post("/logout")

    assert client.post("/login", data={"password": "wrong-password"}).status_code == 200
    resp = client.post("/login", data={"password": "a-good-password"})
    assert resp.status_code == 302


def test_a_wrong_code_on_the_page_claims_nothing(unclaimed, fresh_dir, code):
    client = unclaimed.test_client()
    resp = client.post("/claim", data={"code": "WRON-GCOD-EXXX", "password": "a-good-password"})

    assert resp.status_code == 200
    assert not claim.is_claimed(fresh_dir)
    with client.session_transaction() as sess:
        assert "authed" not in sess


def test_guessing_the_code_gets_throttled(unclaimed, fresh_dir, code):
    """The one secret the person defending the book cannot change."""
    client = unclaimed.test_client()
    for _ in range(unclaimed.config["LOGIN_ATTEMPT_LIMIT"]):
        client.post("/claim", data={"code": "WRON-GCOD-EXXX", "password": "a-good-password"})

    resp = client.post("/claim", data={"code": claim.formatted(code), "password": "a-good-password"})
    assert resp.status_code == 429
    assert not claim.is_claimed(fresh_dir)


def test_a_short_password_does_not_count_against_the_throttle(unclaimed, fresh_dir, code):
    """Fumbling your own new password should never lock you out of your
    own book."""
    client = unclaimed.test_client()
    for _ in range(unclaimed.config["LOGIN_ATTEMPT_LIMIT"] + 2):
        client.post("/claim", data={"code": claim.formatted(code), "password": "sho"})

    resp = client.post("/claim", data={"code": claim.formatted(code), "password": "a-good-password"})
    assert resp.status_code == 302
    assert claim.is_claimed(fresh_dir)


# --- a book that already has a password is untouched ------------------------


def test_a_configured_book_has_no_claim_page(client):
    assert client.get("/claim").status_code == 404


def test_a_configured_book_still_logs_in_normally(client):
    assert client.post("/login", data={"password": "test-password"}).status_code == 302


def test_a_configured_book_generates_no_code(app, stories_dir):
    """The environment wins, exactly as it does for the signing key. An
    install that has been running for a year must notice none of this."""
    app.test_client().get("/")
    assert not (stories_dir / claim.CLAIM_CODE_FILENAME).exists()


def test_the_environment_wins_even_over_a_claimed_password(fresh_dir, code):
    """Both present is not a conflict worth a rule of its own: the machine's
    answer is the answer, and the stored one is simply not consulted."""
    claim.claim(fresh_dir, code, "the-claimed-password")
    settings.save(fresh_dir, {})
    app = create_app(test_config={
        "STORIES_DIR": fresh_dir, "TESTING": True, "WTF_CSRF_ENABLED": False,
        "PASSWORD_CONFIGURED": True, "PASSWORD": "from-the-environment",
    })
    client = app.test_client()

    assert client.post("/login", data={"password": "the-claimed-password"}).status_code == 200
    assert client.post("/login", data={"password": "from-the-environment"}).status_code == 302


# --- and none of it travels in a backup -------------------------------------


def test_the_password_hash_is_a_credential(fresh_dir, code):
    assert claim.BOOK_PASSWORD_FILENAME in backup.CREDENTIAL_FILENAMES


def test_the_claim_code_never_leaves(fresh_dir, code):
    assert claim.CLAIM_CODE_FILENAME in backup.NEVER_EXPORTED


# --- the two ways out, which docs/install.md promises ----------------------
#
# Both are "delete a file and restart", and both are only available to
# somebody with access to the machine's filesystem — which, for a book on a
# NAS in your own house, is the same person as the one who installed it.
# There is deliberately no way to do either from the browser: a password
# reset reachable over the network is a password reset for whoever finds
# the domain.


def test_deleting_the_password_unclaims_the_book(fresh_dir, code):
    """"I forgot the book's password." Delete `book_password.json`,
    restart, read the new code from the logs."""
    claim.claim(fresh_dir, code, "the-forgotten-one")
    (fresh_dir / claim.BOOK_PASSWORD_FILENAME).unlink()

    assert not claim.is_claimed(fresh_dir)
    fresh = claim.pending_code(fresh_dir)
    assert fresh and fresh != code

    claim.claim(fresh_dir, fresh, "the-new-one")
    assert claim.verify_password(fresh_dir, "the-new-one")
    assert not claim.verify_password(fresh_dir, "the-forgotten-one")


def test_the_stories_survive_a_password_reset(fresh_dir, code):
    """The reset must cost the password and nothing else."""
    from datetime import date

    from app import storage

    claim.claim(fresh_dir, code, "the-forgotten-one")
    storage.create_story(fresh_dir, "A day worth keeping", date(2026, 1, 1), "the body")
    (fresh_dir / claim.BOOK_PASSWORD_FILENAME).unlink()
    claim.claim(fresh_dir, claim.pending_code(fresh_dir), "the-new-one")

    assert [s.title for s in storage.list_stories(fresh_dir)] == ["A day worth keeping"]


def test_deleting_the_code_before_claiming_issues_another(fresh_dir, code):
    """"I lost the claim code." Nobody has claimed anything yet, so there
    is nothing to protect — issue a new one."""
    (fresh_dir / claim.CLAIM_CODE_FILENAME).unlink()

    fresh = claim.pending_code(fresh_dir)
    assert fresh and fresh != code
    claim.claim(fresh_dir, fresh, "a-good-password")
    assert claim.is_claimed(fresh_dir)


def test_the_old_code_dies_with_the_file(fresh_dir, code):
    (fresh_dir / claim.CLAIM_CODE_FILENAME).unlink()
    claim.pending_code(fresh_dir)

    with pytest.raises(claim.ClaimError):
        claim.claim(fresh_dir, code, "a-good-password")
