import stat

import pytest

from app import create_app, secret_key


# --- The signing key generates itself when nobody supplied one (F59) --------
#
# This file used to assert the opposite: a password with no
# STORYBOOK_SECRET_KEY raised RuntimeError. The refusal was replaced, not
# relaxed — an unreadable data folder still refuses to start, below.


def test_missing_secret_key_with_password_generates_and_persists_one(monkeypatch, tmp_path):
    monkeypatch.setenv("STORYBOOK_PASSWORD", "prod-password")
    monkeypatch.delenv("STORYBOOK_SECRET_KEY", raising=False)
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    app = create_app()

    key_file = tmp_path / secret_key.SECRET_KEY_FILENAME
    assert key_file.is_file()
    assert app.config["SECRET_KEY"] == key_file.read_text().strip()
    assert len(app.config["SECRET_KEY"]) == 64


def test_generated_secret_key_is_stable_across_restarts(monkeypatch, tmp_path):
    """The whole point. A key regenerated on each boot logs the family out
    every time the container is updated, which is what the old RuntimeError
    was protecting against."""
    monkeypatch.setenv("STORYBOOK_PASSWORD", "prod-password")
    monkeypatch.delenv("STORYBOOK_SECRET_KEY", raising=False)
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    first = create_app().config["SECRET_KEY"]
    second = create_app().config["SECRET_KEY"]

    assert first == second


def test_generated_secret_key_is_not_world_readable(monkeypatch, tmp_path):
    monkeypatch.setenv("STORYBOOK_PASSWORD", "prod-password")
    monkeypatch.delenv("STORYBOOK_SECRET_KEY", raising=False)
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    create_app()

    mode = (tmp_path / secret_key.SECRET_KEY_FILENAME).stat().st_mode
    assert stat.S_IMODE(mode) == 0o600


def test_environment_secret_key_wins_and_writes_no_file(monkeypatch, tmp_path):
    """It is machine configuration: when the machine has an answer, that is
    the answer, and the app leaves no key lying in the data folder."""
    monkeypatch.setenv("STORYBOOK_PASSWORD", "prod-password")
    monkeypatch.setenv("STORYBOOK_SECRET_KEY", "from-the-environment")
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    app = create_app()

    assert app.config["SECRET_KEY"] == "from-the-environment"
    assert not (tmp_path / secret_key.SECRET_KEY_FILENAME).exists()


def test_unusable_stories_dir_still_refuses_to_start(monkeypatch, tmp_path):
    """The refusal survives where it was actually protecting something: a
    data folder the app cannot write to, most likely a volume that wasn't
    mounted. Falling back to an in-memory key here would log everyone out
    on every restart, silently.

    A plain file where the directory should be, rather than a chmod: this
    suite runs as root often enough that mode bits prove nothing.
    """
    blocked = tmp_path / "data"
    blocked.write_text("not a directory\n")
    monkeypatch.setenv("STORYBOOK_PASSWORD", "prod-password")
    monkeypatch.delenv("STORYBOOK_SECRET_KEY", raising=False)
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(blocked))

    with pytest.raises(RuntimeError, match="STORYBOOK_SECRET_KEY"):
        create_app()


def test_a_racing_second_worker_adopts_the_first_key(tmp_path):
    """Two workers can start at once. O_EXCL means one wins; the loser must
    read the winner's key rather than write a competing one, or the two
    sign cookies differently and log each other's readers out."""
    winner = secret_key.load_or_create(tmp_path)
    loser = secret_key.load_or_create(tmp_path)

    assert winner == loser


def test_dev_mode_without_password_or_secret_does_not_raise(monkeypatch, tmp_path):
    monkeypatch.delenv("STORYBOOK_PASSWORD", raising=False)
    monkeypatch.delenv("STORYBOOK_SECRET_KEY", raising=False)
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    app = create_app()
    assert app.config["DEV_MODE"] is True


def test_password_and_secret_key_both_set_does_not_raise(monkeypatch, tmp_path):
    monkeypatch.setenv("STORYBOOK_PASSWORD", "prod-password")
    monkeypatch.setenv("STORYBOOK_SECRET_KEY", "a-real-secret")
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    app = create_app()
    assert app.config["PASSWORD"] == "prod-password"


def test_session_cookie_hardening_defaults(monkeypatch, tmp_path):
    monkeypatch.delenv("STORYBOOK_COOKIE_SECURE", raising=False)
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    app = create_app()
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert app.config["SESSION_COOKIE_SECURE"] is False


def test_session_cookie_secure_env_var(monkeypatch, tmp_path):
    monkeypatch.setenv("STORYBOOK_COOKIE_SECURE", "1")
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))

    app = create_app()
    assert app.config["SESSION_COOKIE_SECURE"] is True


def test_max_content_length_set(tmp_path, monkeypatch):
    monkeypatch.setenv("STORYBOOK_STORIES_DIR", str(tmp_path))
    app = create_app()
    assert app.config["MAX_CONTENT_LENGTH"] == 128 * 1024 * 1024
