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


def test_settings_travel_in_the_backup(auth_client, stories_dir):
    import io
    import zipfile

    storage.create_story(stories_dir, "A story", date(2026, 1, 1), "body")
    settings.save(stories_dir, {"title": "Milo's book"})
    with zipfile.ZipFile(io.BytesIO(auth_client.get("/export").data)) as zf:
        assert "settings.json" in zf.namelist()


def test_a_settings_file_edited_into_nonsense_costs_the_settings_not_the_book(fresh_dir):
    storage.create_story(fresh_dir, "A story", date(2025, 1, 1), "body")
    settings.settings_path(fresh_dir).write_text("{not json at all")
    assert settings.read(fresh_dir) == {}
    assert _client(fresh_dir).get("/").status_code == 200
