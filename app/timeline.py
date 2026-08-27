"""Reading a list of stories as a timeline (F5, F28, F29, F30, F58).

Pure functions over `list[storage.Story]` and a date — no filesystem, no
Flask, nothing to set up to test. They lived in `storage.py`, whose own
docstring says it is "all filesystem read/write for stories" and whose
CLAUDE.md entry had to add "also home to several small pure date-math
helpers": a hedge is usually a file boundary asking to be drawn.

What these decide is *which pages of the book you are shown*:
`readable_stories` is the canonical set (published, unsealed, unarchived,
date-ascending) that reading order, the book view and everything below is
built on. It is not an access-control gate — audience scoping is
`groups.can_see`, reached through `views.visible_stories`, and these
functions are always given a list that has already been through it.
"""

from datetime import date, datetime
from typing import Optional

from . import dates, storage


def stories_with_milestones(stories: list[storage.Story]) -> list[storage.Story]:
    """Readable stories with a `milestone` set, date-ascending (FEATURES.md
    F28) — the register of firsts, in the order they actually happened."""
    return [s for s in readable_stories(stories) if s.milestone]


def growth_photos(stories: list[storage.Story], birthdate: date,
                   today: Optional[date] = None) -> list[dict]:
    """For every birthday from birth to today (FEATURES.md F29), the
    readable story with a cover photo whose date lands closest to that
    birthday — "watch them grow" in one glance. Empty if no readable story
    has a cover yet. Each entry is `{"age", "birthday", "story"}`."""
    if today is None:
        today = date.today()
    candidates = [s for s in readable_stories(stories, today) if s.cover]
    if not candidates:
        return []

    result = []
    age = 0
    while True:
        try:
            birthday = birthdate.replace(year=birthdate.year + age)
        except ValueError:
            # Feb 29 birthdate, non-leap year. The same makeup rule
            # `dates.same_day_of_year` applies, arrived at from the other
            # direction: there is no Feb 29 to land on, so it is Mar 1.
            birthday = date(birthdate.year + age, 3, 1)
        if birthday > today:
            break
        nearest = min(candidates, key=lambda s: abs((s.date - birthday).days))
        result.append({"age": age, "birthday": birthday, "story": nearest})
        age += 1
    return result


QUIET_SPELL_MONTHS = 3


def months_since_last_story(stories: list[storage.Story], today: Optional[date] = None) -> Optional[int]:
    """Whole months since the most recently *written* story, by `created`
    rather than the story's own `date` (FEATURES.md F30) — writing about
    an old memory today shouldn't itself count as "nothing new since
    then." None when there are no stories yet at all — a brand-new book
    isn't nagged before it's even begun. Includes drafts/instants: any of
    them is genuine writing activity worth recognizing."""
    if today is None:
        today = date.today()
    created_dates = [s.created for s in stories if s.created]
    if not created_dates:
        return None
    latest = max(created_dates).date()
    return dates.whole_months_between(latest, today)


#: A backup older than this many months, with writing done since, is worth
#: a word on the timeline (FEATURES.md F58). Longer than QUIET_SPELL_MONTHS
#: because the two nudges say different things: three quiet months is an
#: invitation to write, and half a year of unsaved writing is a risk.
BACKUP_NUDGE_MONTHS = 6


def months_at_risk(stories: list[storage.Story], last_backup: Optional[date] = None,
                   today: Optional[date] = None) -> Optional[int]:
    """How old the oldest *un-backed-up* story is, in whole months, or None
    when nothing is at risk (FEATURES.md F58).

    Deliberately not "months since the last backup". That question nags a
    book nobody has written in — the one book where the backup on the shelf
    is already complete and there is nothing whatsoever to lose. It also
    stays quiet about a book backed up last week and written in every day
    since, which is the same mistake facing the other way.

    The question worth asking is how much unsaved work has piled up, so
    this measures from the oldest story `created` after `last_backup`
    rather than from the backup itself. By `created` and not the story's
    own `date`, exactly as `months_since_last_story` is: writing today
    about a memory from 2019 puts today's work at risk, not 2019's.

    `last_backup` of None means this book has never been backed up, and
    every story counts. Drafts and instants count too — an unfinished
    story is still an evening of someone's writing.
    """
    if today is None:
        today = date.today()
    at_risk = [
        s.created.date() for s in stories
        if s.created and (last_backup is None or s.created.date() > last_backup)
    ]
    if not at_risk:
        return None
    return dates.whole_months_between(min(at_risk), today)


def is_sealed(story: storage.Story, today: Optional[date] = None) -> bool:
    """True while a story's unlock date is still in the future."""
    if today is None:
        today = date.today()
    return story.unlock is not None and story.unlock > today


def readable_stories(stories: list[storage.Story], today: Optional[date] = None) -> list[storage.Story]:
    """Published, unsealed, unarchived stories, date-ascending — the
    canonical "pages of the book" used by reading order, on-this-day, and
    the book view."""
    if today is None:
        today = date.today()
    result = [s for s in stories if not s.draft and not s.archived and not is_sealed(s, today)]
    result.sort(key=lambda s: (s.date, s.created or datetime.min))
    return result


def on_this_day(stories: list[storage.Story], today: Optional[date] = None) -> list[storage.Story]:
    """Readable stories from a previous year whose month/day matches `today`
    (FEATURES.md F5), newest first, capped at 3. A Feb 29 story surfaces on
    Mar 1 in non-leap years, since Feb 29 doesn't occur that year."""
    if today is None:
        today = date.today()
    matches = []
    for s in readable_stories(stories, today):
        if s.date.year >= today.year:
            continue
        if dates.same_day_of_year(s.date, today):
            matches.append(s)
    matches.sort(key=lambda s: s.date.year, reverse=True)
    return matches[:3]
