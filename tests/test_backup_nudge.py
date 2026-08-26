"""The backup nudge (FEATURES.md F58).

The book's promise is that a child reads this in fifteen years. The file
format keeps that promise; a single disk does not. `/export` has been one
tap since F8 and nothing has ever reminded anyone to take it — the only
mention was a comment in `.env.example`, in a file a family who installed
this from Docker never opens.

What is tested here is mostly *when the app stays quiet*, because a nudge
that fires when there is nothing to do is one people learn to ignore, and
then it is not there on the day it matters.
"""

from datetime import date, datetime

import pytest

from app import backup, storage, timeline

from app import accounts, people

from tests.conftest import _login


def _story_created_on(id_, created_date):
    return storage.Story(
        id=id_, title=id_, date=created_date,
        created=datetime.combine(created_date, datetime.min.time()), updated=None,
    )


# --- months_at_risk: how much unsaved writing has piled up ------------------


def test_nothing_at_risk_in_an_empty_book():
    assert timeline.months_at_risk([], None, today=date(2026, 8, 26)) is None


def test_a_brand_new_book_is_not_nagged():
    """Written this week, never backed up: true, and not worth saying."""
    stories = [_story_created_on("first", date(2026, 8, 20))]
    assert timeline.months_at_risk(stories, None, today=date(2026, 8, 26)) == 0


def test_a_year_of_writing_and_no_backup_ever():
    stories = [_story_created_on("old", date(2025, 8, 20))]
    assert timeline.months_at_risk(stories, None, today=date(2026, 8, 26)) == 12


def test_a_recent_backup_puts_nothing_at_risk():
    stories = [_story_created_on("old", date(2025, 8, 20))]
    result = timeline.months_at_risk(stories, date(2026, 8, 20), today=date(2026, 8, 26))
    assert result is None


def test_a_stale_backup_of_a_book_nobody_writes_in_is_silent():
    """The case that makes this "months at risk" rather than "months since
    the last backup". The zip on the shelf is a complete copy and not one
    word has been written since — there is nothing whatsoever to lose, and
    a nudge here would be the app crying wolf for a year."""
    stories = [_story_created_on("last-one", date(2025, 1, 1))]
    result = timeline.months_at_risk(stories, date(2025, 6, 1), today=date(2026, 8, 26))
    assert result is None


def test_writing_done_since_a_stale_backup_is_at_risk():
    stories = [
        _story_created_on("backed-up", date(2025, 1, 1)),
        _story_created_on("not-backed-up", date(2025, 12, 20)),
    ]
    result = timeline.months_at_risk(stories, date(2025, 6, 1), today=date(2026, 8, 26))
    assert result == 8


def test_it_measures_the_oldest_unsaved_story_not_the_newest():
    """Eight months of exposure is the fact worth reporting, not the fact
    that someone also wrote something yesterday."""
    stories = [
        _story_created_on("old-and-unsaved", date(2025, 12, 20)),
        _story_created_on("written-yesterday", date(2026, 8, 25)),
    ]
    result = timeline.months_at_risk(stories, date(2025, 6, 1), today=date(2026, 8, 26))
    assert result == 8


def test_drafts_count_as_writing_worth_keeping():
    story = _story_created_on("half-written", date(2025, 8, 20))
    story.draft = True
    assert timeline.months_at_risk([story], None, today=date(2026, 8, 26)) == 12


def test_a_story_written_on_the_backup_day_is_not_counted_as_saved():
    """Same-day is the ambiguous one: the marker stores a date, so a story
    written hours after the export shares it. Counted as saved rather than
    at risk, which errs toward quiet — and one day's exposure never reaches
    the six-month threshold anyway."""
    stories = [_story_created_on("same-day", date(2026, 6, 1))]
    assert timeline.months_at_risk(stories, date(2026, 6, 1), today=date(2026, 8, 26)) is None


# --- the marker file --------------------------------------------------------


def test_a_book_that_has_never_been_backed_up_reports_none(stories_dir):
    assert backup.last_backup(stories_dir) is None


def test_record_and_read_back(stories_dir):
    backup.record_backup(stories_dir, date(2026, 3, 4))
    assert backup.last_backup(stories_dir) == date(2026, 3, 4)


def test_recording_again_replaces_the_date(stories_dir):
    backup.record_backup(stories_dir, date(2026, 3, 4))
    backup.record_backup(stories_dir, date(2026, 7, 9))
    assert backup.last_backup(stories_dir) == date(2026, 7, 9)


def test_the_marker_is_readable_by_a_person(stories_dir):
    """Plain YYYY-MM-DD, like everything else in this folder."""
    backup.record_backup(stories_dir, date(2026, 3, 4))
    text = (stories_dir / backup.BACKUP_MARKER_FILENAME).read_text()
    assert "2026-03-04" in text


@pytest.mark.parametrize("junk", ["", "not json at all", "{}", '{"at": "the fourth"}', "[]"])
def test_a_corrupt_marker_prompts_the_backup_again_rather_than_breaking(stories_dir, junk):
    """This file exists to prompt a kindness. The worst a damaged one may
    do is prompt it twice — never to take the timeline down with it."""
    (stories_dir / backup.BACKUP_MARKER_FILENAME).write_text(junk)
    assert backup.last_backup(stories_dir) is None


# --- who the nudge is for ---------------------------------------------------


def _write_old_story(stories_dir, title="Ancient", created="2020-01-01T00:00:00"):
    """A story on disk that was written years ago.

    `create_story` stamps `created` with now, which is the right behaviour
    and the wrong fixture — the nudge measures the age of unsaved writing,
    so the age has to be real. Rewritten in the frontmatter afterwards
    rather than faked in the clock, so the story that reaches the route is
    an ordinary one this app could have written.
    """
    story_id = storage.create_story(stories_dir, title, date(2020, 1, 1), "Long ago.")
    path = stories_dir / story_id / "index.md"
    lines = [
        f"created: '{created}'" if line.startswith("created:") else line
        for line in path.read_text().splitlines()
    ]
    path.write_text("\n".join(lines) + "\n")
    return story_id


def test_the_keeper_is_told(auth_client, stories_dir):
    _write_old_story(stories_dir)
    body = auth_client.get("/").data
    assert b"never been backed up" in body


def test_a_book_with_a_fresh_backup_says_nothing(auth_client, stories_dir):
    _write_old_story(stories_dir)
    backup.record_backup(stories_dir, date.today())
    assert b"never been backed up" not in auth_client.get("/").data


def test_downloading_the_zip_quiets_the_nudge(auth_client, stories_dir):
    _write_old_story(stories_dir)
    assert b"never been backed up" in auth_client.get("/").data

    assert auth_client.get("/export").status_code == 200

    assert backup.last_backup(stories_dir) == date.today()
    assert b"never been backed up" not in auth_client.get("/").data


def test_an_empty_book_is_never_nudged(auth_client):
    assert b"never been backed up" not in auth_client.get("/").data


# --- and who it is not for, once accounts are on (F19/F43 segregation) ------


@pytest.fixture
def accounts_app(app_factory):
    return app_factory(ACCOUNTS_ENABLED=True)


@pytest.fixture
def cast(accounts_app, stories_dir):
    """An admin who keeps the book, and a family member who reads it."""
    people_dir = stories_dir / "people"
    for name in ("Papa", "Mamie"):
        people.create_person(people_dir, name)
    accounts.create_account(people_dir, "papa", "papa", "adminpass1", role="admin")
    accounts.create_account(people_dir, "mamie", "mamie", "mamiepass1", role="family")
    _write_old_story(stories_dir)
    return accounts_app


def _timeline_for(app, username, password):
    client = app.test_client()
    _login(client, username, password)
    return client


def test_the_admin_is_told(cast):
    client = _timeline_for(cast, "papa", "adminpass1")
    assert b"never been backed up" in client.get("/").data


def test_a_family_member_is_not_asked_to_do_the_keeper_s_job(cast):
    """Mamie cannot take a complete backup — hers is scoped to what she can
    see (F40) and carries no account files (F43). Telling her the book is
    at risk asks for something she cannot give, and the month count would
    be computed from her partial list anyway."""
    client = _timeline_for(cast, "mamie", "mamiepass1")
    assert b"never been backed up" not in client.get("/").data


def test_a_family_member_s_partial_zip_does_not_quiet_the_book(cast, stories_dir):
    """The segregation that matters here. If Mamie's scoped export counted
    as the book's backup, one relative downloading their own slice would
    tell the admin — falsely — that everything was safe."""
    mamie = _timeline_for(cast, "mamie", "mamiepass1")
    assert mamie.get("/export").status_code == 200

    assert backup.last_backup(stories_dir) is None
    papa = _timeline_for(cast, "papa", "adminpass1")
    assert b"never been backed up" in papa.get("/").data


def test_an_admin_s_zip_does_quiet_it(cast, stories_dir):
    papa = _timeline_for(cast, "papa", "adminpass1")
    assert papa.get("/export").status_code == 200

    assert backup.last_backup(stories_dir) == date.today()
    assert b"never been backed up" not in papa.get("/").data
