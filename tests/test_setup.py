"""Tests for FEATURES.md F51: setting the book up from inside the book.

The half of this that matters most is the half that must *not* happen. An
install that has been in use for a year has no settings file — it predates
one — and meeting a setup wizard on upgrade would be the worst kind of bug
this feature could have: a family asked to configure a book they have been
writing in since before the app could ask. So the upgrade case is tested
harder than the new-book case.
"""

from datetime import date

import pytest

from app import create_app, settings, storage

BASE = {"PASSWORD": "test-password", "SECRET_KEY": "test-secret", "WTF_CSRF_ENABLED": False}


@pytest.fixture
def fresh_dir(tmp_path):
    """A stories directory that has *not* been through conftest's marker —
    a genuinely new book."""
    d = tmp_path / "fresh"
    d.mkdir()
    return d


def _client(stories_dir, **config):
    app = create_app(test_config={"STORIES_DIR": stories_dir, **BASE, **config})
    client = app.test_client()
    client.post("/login", data={"password": "test-password"})
    return client


# --- the upgrade case ---------------------------------------------------------


def test_a_book_with_stories_in_it_is_already_set_up(fresh_dir):
    """The install this feature could most easily insult."""
    storage.create_story(fresh_dir, "A story from last year", date(2025, 3, 2), "body")
    assert settings.is_configured(fresh_dir)
    assert _client(fresh_dir).get("/").status_code == 200


def test_an_existing_book_is_never_sent_to_the_wizard(fresh_dir):
    storage.create_story(fresh_dir, "A story", date(2025, 3, 2), "body")
    resp = _client(fresh_dir).get("/", follow_redirects=False)
    assert resp.status_code == 200
    assert "/setup" not in resp.data.decode()


def test_the_wizard_itself_steps_aside_on_a_book_that_exists(fresh_dir):
    storage.create_story(fresh_dir, "A story", date(2025, 3, 2), "body")
    resp = _client(fresh_dir).get("/setup")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/settings")


def test_an_upgraded_book_keeps_working_from_its_environment(fresh_dir):
    """No settings file, so every value still comes from the variables the
    server was started with — which is exactly what it did yesterday."""
    storage.create_story(fresh_dir, "A story", date(2025, 3, 2), "body")
    client = _client(fresh_dir, TITLE="Le livre de Milo", BIRTHDATE=date(2023, 6, 18))
    html = client.get("/").data.decode()
    assert "Le livre de Milo" in html
    assert not settings.settings_path(fresh_dir).is_file()


def test_settings_prefill_from_the_environment_so_a_save_cannot_erase_it(fresh_dir):
    """The trap: an upgraded install opens Settings, presses Save, and its
    title and birth date are blanked because the form showed them empty."""
    storage.create_story(fresh_dir, "A story", date(2025, 3, 2), "body")
    client = _client(fresh_dir, TITLE="Le livre de Milo", BIRTHDATE=date(2023, 6, 18))
    html = client.get("/settings").data.decode()
    assert 'value="Le livre de Milo"' in html
    assert 'value="2023-06-18"' in html


def test_saving_that_prefilled_form_keeps_what_was_there(fresh_dir):
    storage.create_story(fresh_dir, "A story", date(2025, 3, 2), "body")
    client = _client(fresh_dir, TITLE="Le livre de Milo", BIRTHDATE=date(2023, 6, 18))
    client.post("/settings", data={
        "title": "Le livre de Milo", "birthdate": "2023-06-18",
        "child": "", "authors": "", "language": "", "theme": "",
    })
    html = client.get("/").data.decode()
    assert "Le livre de Milo" in html


# --- a genuinely new book -----------------------------------------------------


def test_a_brand_new_book_offers_the_wizard(fresh_dir):
    resp = _client(fresh_dir).get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/setup")


def test_the_wizard_writes_the_settings_and_gets_out_of_the_way(fresh_dir):
    client = _client(fresh_dir)
    resp = client.post("/setup", data={
        "title": "Milo's book", "child_name": "Milo", "birthdate": "2023-06-18",
        "authors": "Papa #d9a441\nMaman #7ba7d9", "language": "fr", "theme": "",
    })
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
    stored = settings.read(fresh_dir)
    assert stored["title"] == "Milo's book"
    assert stored["birthdate"] == "2023-06-18"
    assert stored["authors"] == [
        {"name": "Papa", "color": "#d9a441"}, {"name": "Maman", "color": "#7ba7d9"}
    ]
    # ...and asking again is over for good.
    assert client.get("/").status_code == 200


def test_the_child_becomes_the_first_person_in_the_cast(fresh_dir):
    from app import people

    client = _client(fresh_dir)
    client.post("/setup", data={
        "title": "", "child_name": "Milo", "birthdate": "2023-06-18",
        "authors": "", "language": "", "theme": "",
    })
    cast = people.list_people(storage.people_dir(fresh_dir))
    assert [p.name for p in cast] == ["Milo"]
    assert cast[0].born == date(2023, 6, 18)
    # and the family tree is drawn around them
    assert settings.read(fresh_dir)["child"] == cast[0].slug


def test_not_now_is_a_real_answer(fresh_dir):
    """It must count as set up, or the wizard becomes a banner that follows
    a family around forever."""
    client = _client(fresh_dir)
    resp = client.post("/setup", data={"skip": "1"})
    assert resp.status_code == 302
    assert settings.is_configured(fresh_dir)
    assert client.get("/").status_code == 200


def test_a_bad_date_says_so_instead_of_failing(fresh_dir):
    client = _client(fresh_dir)
    resp = client.post("/setup", data={
        "title": "x", "child_name": "", "birthdate": "18/06/2023",
        "authors": "", "language": "", "theme": "",
    }, follow_redirects=True)
    assert resp.status_code == 200
    assert "year-month-day" in resp.data.decode()
    assert not settings.is_configured(fresh_dir)


def test_a_narrator_line_that_makes_no_sense_says_which_one(fresh_dir):
    client = _client(fresh_dir)
    resp = client.post("/setup", data={
        "title": "x", "child_name": "", "birthdate": "",
        "authors": "Papa\nMaman #7ba7d9", "language": "", "theme": "",
    }, follow_redirects=True)
    assert "Papa" in resp.data.decode()
    assert not settings.is_configured(fresh_dir)


# --- what settings do once they are set ---------------------------------------


def test_a_setting_beats_the_environment_it_was_started_with(fresh_dir):
    client = _client(fresh_dir, TITLE="From the environment")
    client.post("/setup", data={
        "title": "From the app", "child_name": "", "birthdate": "",
        "authors": "", "language": "", "theme": "",
    })
    assert "From the app" in client.get("/").data.decode()


def test_clearing_a_setting_means_no_value_not_the_environments(fresh_dir):
    """Someone emptying the title wants the app's own name back, not a
    variable they have never seen."""
    client = _client(fresh_dir, TITLE="From the environment")
    client.post("/setup", data={"skip": "1"})
    client.post("/settings", data={
        "title": "", "birthdate": "", "child": "", "authors": "",
        "language": "", "theme": "",
    })
    html = client.get("/").data.decode()
    assert "From the environment" not in html
    assert "Storybook" in html


def test_a_change_takes_effect_without_a_restart(fresh_dir):
    client = _client(fresh_dir)
    client.post("/setup", data={"skip": "1"})
    client.post("/settings", data={
        "title": "First name", "birthdate": "", "child": "", "authors": "",
        "language": "", "theme": "",
    })
    assert "First name" in client.get("/").data.decode()
    client.post("/settings", data={
        "title": "Second name", "birthdate": "", "child": "", "authors": "",
        "language": "", "theme": "",
    })
    assert "Second name" in client.get("/").data.decode()


def test_settings_travel_in_the_backup(auth_client, stories_dir, fresh_dir):
    """Both halves of "travel", because for a while only the first was
    true: the export put `settings.json` in the zip and `import_backup`
    skipped every root-level file on the way back, so a restore onto a new
    server silently dropped the book's name, its narrators and its
    language. The Settings page promises this in so many words."""
    import io
    import zipfile

    storage.create_story(stories_dir, "A story", date(2026, 1, 1), "body")
    settings.save(stories_dir, {
        "title": "Milo's book",
        "language": "fr",
        "authors": [{"name": "Papa", "color": "#d9a441"}],
    })
    backup = auth_client.get("/export").data
    with zipfile.ZipFile(io.BytesIO(backup)) as zf:
        assert "settings.json" in zf.namelist()

    storage.import_backup(fresh_dir, io.BytesIO(backup))
    restored = settings.read(fresh_dir)
    assert restored["title"] == "Milo's book"
    assert restored["language"] == "fr"
    assert restored["authors"] == [{"name": "Papa", "color": "#d9a441"}]


def test_a_restore_never_overwrites_a_book_that_is_already_set_up(
    auth_client, stories_dir, fresh_dir
):
    """Additive, like people and made themes: an install that has already
    been configured keeps what it is doing. Restoring an old zip over a
    live book must not roll its title back."""
    import io

    storage.create_story(stories_dir, "A story", date(2026, 1, 1), "body")
    settings.save(stories_dir, {"title": "The old name"})
    backup = auth_client.get("/export").data

    settings.save(fresh_dir, {"title": "The name it has now"})
    storage.import_backup(fresh_dir, io.BytesIO(backup))
    assert settings.read(fresh_dir)["title"] == "The name it has now"


def test_a_backup_may_only_put_back_settings_this_app_writes(fresh_dir):
    """Same rule a theme folder is held to: a zip is a portable file and
    may not use `settings.json` as a way to drop arbitrary keys into the
    book. Anything outside `settings.KEYS` is dropped on the way in."""
    import io
    import json
    import zipfile

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-01-01-a-story/index.md", "---\ntitle: A story\n---\nbody\n")
        zf.writestr("settings.json", json.dumps({
            "title": "Restored", "SECRET_KEY": "nope", "stories_dir": "/etc",
        }))
    buf.seek(0)
    storage.import_backup(fresh_dir, buf)
    assert settings.read(fresh_dir) == {"title": "Restored"}


def test_an_unreadable_settings_file_in_a_backup_costs_the_settings_not_the_restore(
    fresh_dir
):
    """Losing a title on the way back from a dead server is a nuisance;
    losing the stories is the thing this app exists to prevent."""
    import io
    import zipfile

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        zf.writestr("2026-01-01-a-story/index.md", "---\ntitle: A story\n---\nbody\n")
        zf.writestr("settings.json", "{ this is not json")
    buf.seek(0)
    assert storage.import_backup(fresh_dir, buf) == 1
    assert (fresh_dir / "2026-01-01-a-story" / "index.md").is_file()


def test_a_settings_file_edited_into_nonsense_costs_the_settings_not_the_book(fresh_dir):
    storage.create_story(fresh_dir, "A story", date(2025, 1, 1), "body")
    settings.settings_path(fresh_dir).write_text("{not json at all")
    assert settings.read(fresh_dir) == {}
    assert _client(fresh_dir).get("/").status_code == 200


# --- what a fresh install is actually promised --------------------------------
#
# Three defects a code review found after F51 shipped, each of which broke
# an install that was configured by environment variable — which is every
# install that predates the settings page, and every install started from
# .env.example. The tests are written as the promise rather than as the
# bug, so they keep meaning something once the bug is a memory.


def test_a_form_never_writes_a_setting_it_did_not_offer(fresh_dir):
    """The wizard shows no theme and no tree-child, so pressing its button
    must not touch either.

    `effective` reads a key that is present-but-empty as "no value" — that
    is how clearing the title gets the app's own name back. So writing
    every key regardless would erase whatever the environment set for a
    field the form does not show. A book started with STORYBOOK_THEME=orbit
    served the ranch from the moment anyone finished the wizard.
    """
    client = _client(fresh_dir, THEME="orbit", CHILD_SLUG="milo")
    client.post("/setup", data={
        "title": "Veillée", "birthdate": "", "child_name": "",
        "authors": "", "language": "fr",
    })

    stored = settings.read(fresh_dir)
    assert "theme" not in stored
    assert "child" not in stored
    assert stored["title"] == "Veillée"

    app = create_app(test_config={"STORIES_DIR": fresh_dir, **BASE,
                                  "THEME": "orbit", "CHILD_SLUG": "milo"})
    effective = settings.effective(app.config, fresh_dir)
    assert effective["THEME"] == "orbit"
    assert effective["CHILD_SLUG"] == "milo"


def test_the_settings_form_offers_every_key_it_writes(fresh_dir):
    """The general version of the test above, so the next field added to
    one form and not the other is caught here rather than by somebody's
    theme quietly reverting.

    /settings is the page that claims to change everything, so every key
    in `settings.KEYS` has to have a field on it.
    """
    client = _client(fresh_dir)
    settings.save(fresh_dir, {})          # count the book as set up
    body = client.get("/settings").get_data(as_text=True)
    missing = [key for key in settings.KEYS if f'name="{key}"' not in body]
    assert not missing, f"/settings writes but never offers: {missing}"


def test_the_language_setting_actually_changes_the_language(fresh_dir):
    """`settings.book()` falls back to the raw config while `g.book` is
    unset, which is right outside a request and silently wrong inside one.
    Resolving the language before `g.book` was assigned read
    DEFAULT_LANGUAGE from the environment, so this field did nothing at
    all while the title and theme from the same file worked.
    """
    settings.save(fresh_dir, {"title": "Veillée", "language": "fr"})
    client = _client(fresh_dir, DEFAULT_LANGUAGE="en")
    body = client.get("/").get_data(as_text=True)
    assert '<html lang="fr"' in body
    # ...and the neighbouring settings still work, which is what made the
    # original bug so easy to miss.
    assert "Veillée" in body


def test_every_family_setting_is_read_through_the_request_context(fresh_dir):
    """The rule CLAUDE.md states and nothing enforced: a value a family can
    change is read through `settings.book()`, per request, not out of
    `config` at import or startup.

    Checked by setting each key in the file to something the environment
    disagrees with, and asserting the file wins.
    """
    settings.save(fresh_dir, {
        "title": "From the file",
        "language": "fr",
        "theme": "orbit",
    })
    app = create_app(test_config={
        "STORIES_DIR": fresh_dir, **BASE,
        "TITLE": "From the environment", "DEFAULT_LANGUAGE": "en",
        "THEME": "ranch",
    })
    client = app.test_client()
    client.post("/login", data={"password": "test-password"})
    body = client.get("/").get_data(as_text=True)
    assert "From the file" in body
    assert "From the environment" not in body
    assert '<html lang="fr"' in body
    assert "/static/themes/orbit/" in body


@pytest.mark.parametrize("authors", [
    ["Papa", "Maman"],                                  # the shape a person types
    [{"name": "Papa"}],                                 # half an entry
    [{"name": "Papa", "color": "not-a-colour"}],
    [{"name": "", "color": "#d9a441"}],
    ["Papa", {"name": "Maman", "color": "#8f2f2a"}],     # one of each
    "Papa #d9a441",                                      # not a list at all
])
def test_a_hand_edited_narrator_list_costs_the_settings_not_the_book(
    fresh_dir, authors
):
    """`read()`'s promise, applied to the one key that was not keeping it.
    Every page indexes a narrator as `a["name"]`, so a list of bare strings
    — which is exactly what someone would write by hand — turned the whole
    book into a 500."""
    settings.save(fresh_dir, {"authors": authors})
    client = _client(fresh_dir)
    assert client.get("/").status_code == 200


def test_a_hand_edited_narrator_list_keeps_the_entries_that_are_fine(fresh_dir):
    """Filtered, not rejected wholesale: one bad line should not cost the
    other narrators their colours."""
    settings.save(fresh_dir, {"authors": [
        {"name": "Papa", "color": "#d9a441"},
        "Maman",
        {"name": "Mamie", "color": "#5f8f6a"},
    ]})
    app = create_app(test_config={"STORIES_DIR": fresh_dir, **BASE})
    assert settings.effective(app.config, fresh_dir)["AUTHORS"] == [
        {"name": "Papa", "color": "#d9a441"},
        {"name": "Mamie", "color": "#5f8f6a"},
    ]
