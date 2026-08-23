"""Reading a list of stories as a timeline (`app/timeline.py`).

These moved out of `tests/test_storage.py` with the code they test: they
build `Story` objects in memory and never touch a directory, which is what
said the functions were not really storage in the first place.

`test_visibility.py` (F0) and `test_on_this_day.py` (F5) also test this
module and stay where they are — this suite is one file per feature area,
not one per module, and those two are named for their feature.

The last section is new: the Feb 29 rule that three call sites used to
each write out for themselves.
"""

from datetime import date, datetime

from app import dates, life_events, people, storage, timeline


def test_stories_with_milestones_returns_only_matching_readable_stories(stories_dir):
    storage.create_story(stories_dir, "First steps", date(2026, 3, 1), "", milestone="First steps")
    storage.create_story(stories_dir, "No milestone", date(2026, 1, 1), "")
    storage.create_story(
        stories_dir, "Draft first", date(2026, 2, 1), "", milestone="Draft", draft=True
    )
    all_stories = storage.list_stories(stories_dir)
    result = timeline.stories_with_milestones(all_stories)
    assert [s.title for s in result] == ["First steps"]


def test_stories_with_milestones_sorted_chronologically(stories_dir):
    storage.create_story(stories_dir, "Second first", date(2026, 6, 1), "", milestone="Second")
    storage.create_story(stories_dir, "First first", date(2026, 1, 1), "", milestone="First")
    all_stories = storage.list_stories(stories_dir)
    result = timeline.stories_with_milestones(all_stories)
    assert [s.title for s in result] == ["First first", "Second first"]


# --- growth_photos: the birthday photo wall (FEATURES.md F29) ----------------


def _story_with_cover(id_, story_date, cover="photo-001.jpg"):
    return storage.Story(
        id=id_, title=id_, date=story_date, created=None, updated=None, cover=cover
    )


def test_growth_photos_empty_when_no_covers():
    result = timeline.growth_photos([], date(2020, 6, 18), today=date(2023, 1, 1))
    assert result == []


def test_growth_photos_one_entry_per_birthday():
    birthdate = date(2020, 6, 18)
    stories = [
        _story_with_cover("newborn", date(2020, 6, 20)),
        _story_with_cover("age1", date(2021, 6, 15)),
    ]
    result = timeline.growth_photos(stories, birthdate, today=date(2022, 1, 1))
    assert [e["age"] for e in result] == [0, 1]
    assert result[0]["story"].id == "newborn"
    assert result[1]["story"].id == "age1"


def test_growth_photos_picks_nearest_photo_overall():
    birthdate = date(2020, 6, 18)
    stories = [
        _story_with_cover("far", date(2020, 1, 1)),
        _story_with_cover("near", date(2020, 6, 19)),
    ]
    result = timeline.growth_photos(stories, birthdate, today=date(2020, 12, 1))
    assert result[0]["story"].id == "near"


def test_growth_photos_stops_before_future_birthdays():
    birthdate = date(2020, 6, 18)
    stories = [_story_with_cover("only", date(2020, 6, 20))]
    result = timeline.growth_photos(stories, birthdate, today=date(2022, 1, 1))
    assert [e["age"] for e in result] == [0, 1]


def test_growth_photos_feb29_birthdate_uses_mar1_makeup():
    birthdate = date(2020, 2, 29)
    stories = [_story_with_cover("only", date(2021, 3, 1))]
    result = timeline.growth_photos(stories, birthdate, today=date(2021, 3, 1))
    assert [e["birthday"] for e in result] == [date(2020, 2, 29), date(2021, 3, 1)]


def test_growth_photos_excludes_stories_without_covers():
    birthdate = date(2020, 6, 18)
    stories = [
        storage.Story(id="no-cover", title="x", date=date(2020, 6, 18), created=None, updated=None),
    ]
    result = timeline.growth_photos(stories, birthdate, today=date(2020, 7, 1))
    assert result == []


def test_growth_photos_excludes_drafts_and_sealed():
    birthdate = date(2020, 6, 18)
    draft = storage.Story(
        id="draft", title="x", date=date(2020, 6, 18), created=None, updated=None,
        cover="c.jpg", draft=True,
    )
    result = timeline.growth_photos([draft], birthdate, today=date(2020, 7, 1))
    assert result == []


# --- months_since_last_story: the gentle writing nudge (FEATURES.md F30) -----


def _story_created_on(id_, created_date):
    return storage.Story(
        id=id_, title=id_, date=created_date, created=datetime.combine(created_date, datetime.min.time()),
        updated=None,
    )


def test_months_since_last_story_none_when_no_stories():
    assert timeline.months_since_last_story([]) is None


def test_months_since_last_story_zero_for_recent_activity():
    stories = [_story_created_on("recent", date(2026, 6, 1))]
    result = timeline.months_since_last_story(stories, today=date(2026, 6, 15))
    assert result == 0


def test_months_since_last_story_counts_whole_months():
    stories = [_story_created_on("old", date(2026, 1, 15))]
    result = timeline.months_since_last_story(stories, today=date(2026, 6, 20))
    assert result == 5


def test_months_since_last_story_boundary_day_not_yet_elapsed():
    stories = [_story_created_on("old", date(2026, 1, 20))]
    result = timeline.months_since_last_story(stories, today=date(2026, 6, 15))
    assert result == 4


def test_months_since_last_story_uses_most_recent_of_several():
    stories = [
        _story_created_on("older", date(2025, 1, 1)),
        _story_created_on("newer", date(2026, 5, 1)),
    ]
    result = timeline.months_since_last_story(stories, today=date(2026, 6, 1))
    assert result == 1


# --- the calendar rule the three of them share ------------------------------


def test_a_feb29_anniversary_comes_round_on_mar1_in_a_non_leap_year():
    """`dates.same_day_of_year`, which used to be written out three times:
    in `on_this_day`, in `life_events._matches_today`, and as the
    `except ValueError` branch of `growth_photos`."""
    leap_day = date(2024, 2, 29)
    assert dates.same_day_of_year(leap_day, date(2025, 3, 1)) is True
    assert dates.same_day_of_year(leap_day, date(2025, 2, 28)) is False


def test_a_feb29_anniversary_needs_no_makeup_in_a_leap_year():
    leap_day = date(2024, 2, 29)
    assert dates.same_day_of_year(leap_day, date(2028, 2, 29)) is True
    assert dates.same_day_of_year(leap_day, date(2028, 3, 1)) is False


def test_mar1_is_not_swallowed_by_the_makeup_rule():
    """The rule must not work backwards — a Mar 1 anniversary is a Mar 1
    anniversary, and is not also claimed by Feb 29."""
    assert dates.same_day_of_year(date(2024, 3, 1), date(2025, 3, 1)) is True
    assert dates.same_day_of_year(date(2024, 3, 1), date(2025, 2, 28)) is False


def test_a_story_and_a_birthday_land_on_the_same_day(stories_dir):
    """The point of sharing the rule. A leap-day story surfacing on Mar 1
    while a leap-day birthday surfaced on Feb 28 — or neither, or one but
    not the other — was possible while each module carried its own copy.
    """
    non_leap_mar1 = date(2025, 3, 1)
    story = storage.Story(
        id="leap-day", title="Leap day", date=date(2024, 2, 29),
        created=None, updated=None,
    )
    people_dir = storage.people_dir(stories_dir)
    people.create_person(people_dir, "Leapling", born=date(2024, 2, 29))
    cast = people.list_people(people_dir)

    assert [s.id for s in timeline.on_this_day([story], today=non_leap_mar1)] == ["leap-day"]
    assert [p.slug for p in life_events.birthdays_today(cast, today=non_leap_mar1)] == [
        "leapling"
    ]


def test_neither_surfaces_on_feb28(stories_dir):
    feb28 = date(2025, 2, 28)
    story = storage.Story(
        id="leap-day", title="Leap day", date=date(2024, 2, 29),
        created=None, updated=None,
    )
    people_dir = storage.people_dir(stories_dir)
    people.create_person(people_dir, "Leapling", born=date(2024, 2, 29))

    assert timeline.on_this_day([story], today=feb28) == []
    assert life_events.birthdays_today(people.list_people(people_dir), today=feb28) == []


def test_timeline_is_pure(stories_dir):
    """No filesystem in any of it — the property that says these belong in
    their own module rather than in `storage.py`. A tmp directory is
    handed in and must come back untouched."""
    before = sorted(p.name for p in stories_dir.iterdir())
    stories = [
        storage.Story(id="a", title="A", date=date(2026, 1, 1), created=None,
                      updated=None, cover="photo-001.jpg", milestone="First"),
    ]
    timeline.readable_stories(stories)
    timeline.stories_with_milestones(stories)
    timeline.on_this_day(stories, today=date(2027, 1, 1))
    timeline.growth_photos(stories, date(2026, 1, 1), today=date(2026, 6, 1))
    timeline.months_since_last_story(stories, today=date(2026, 6, 1))
    assert sorted(p.name for p in stories_dir.iterdir()) == before
