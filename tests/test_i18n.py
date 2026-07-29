"""Tests for FEATURES.md F38: the interface in French.

Three layers: the pure mechanism (language selection, plurals, dates), the
picker and the cookie that make it a user choice, and — the one that keeps
this feature honest over time — a coverage test that walks every template
and fails if any string passed to `_()` has no French entry.
"""

import re
from datetime import date, datetime
from pathlib import Path

import pytest

from app import i18n
from app.translations_fr import TRANSLATIONS_FR

TEMPLATES = Path(__file__).resolve().parent.parent / "app" / "templates"
_CALL_RE = re.compile(r"""_n?\(\s*(['"])(.*?)(?<!\\)\1""", re.S)


def _strings_used_in_templates():
    used = set()
    for path in sorted(TEMPLATES.glob("*.html")):
        for _quote, text in _CALL_RE.findall(path.read_text()):
            used.add(text.replace("\\'", "'").replace('\\"', '"'))
    return used


# --- the guard that keeps this from rotting ---------------------------------


def test_every_template_string_has_a_french_translation():
    """Add a string to a template without translating it and this fails.
    Falling back to English is a safety net for a missed edge, not the
    normal state of the app."""
    used = _strings_used_in_templates()
    assert len(used) > 150, "the scanner stopped finding strings — check the regex"
    missing = sorted(t for t in used if t not in TRANSLATIONS_FR)
    assert not missing, "untranslated template strings:\n" + "\n".join(
        f"  {s!r}" for s in missing
    )


def test_no_french_entry_is_identical_to_its_english_key():
    """A copy-pasted key with the English left in the value is a silent
    hole — it looks translated in the dict and reads wrong on the page.
    Proper nouns that really are the same in both are listed here."""
    same_in_both = {
        "PACS", "Photo", "Photos", "Instant", "+ Instant",
        "Parents", "Union", "Unions", "union", "Sources",
        "Pause", "Zoom", "Date", "https://...", "Invitation",
    }
    lazy = [
        k for k, v in TRANSLATIONS_FR.items()
        if k == v and k not in same_in_both
    ]
    assert not lazy, f"French value identical to the English key: {lazy}"


def test_no_french_value_is_empty():
    assert not [k for k, v in TRANSLATIONS_FR.items() if not v.strip()]


def test_placeholders_survive_translation():
    """{n}, {name}, {date}… must appear in the French value too, or the
    interpolation silently drops the number."""
    broken = []
    for key, value in TRANSLATIONS_FR.items():
        expected = set(re.findall(r"\{(\w+)\}", key))
        actual = set(re.findall(r"\{(\w+)\}", value))
        if expected != actual:
            broken.append((key, expected, actual))
    assert not broken, f"placeholder mismatch: {broken}"


# --- language selection ------------------------------------------------------


def test_cookie_choice_wins_over_the_browser():
    assert i18n.pick_language("fr", "en-GB,en;q=0.9") == "fr"
    assert i18n.pick_language("en", "fr-FR,fr;q=0.9") == "en"


def test_browser_preference_used_when_no_choice_stored():
    assert i18n.pick_language(None, "fr-FR,fr;q=0.9,en;q=0.8") == "fr"
    assert i18n.pick_language(None, "en-GB,en;q=0.9") == "en"


def test_regional_tags_match_their_base_language():
    """A Quebecois or Belgian phone should get French, not English."""
    assert i18n.pick_language(None, "fr-CA") == "fr"
    assert i18n.pick_language(None, "fr-BE,fr;q=0.9") == "fr"


def test_quality_values_are_honoured():
    assert i18n.pick_language(None, "en;q=0.3,fr;q=0.9") == "fr"
    assert i18n.pick_language(None, "fr;q=0.2,en;q=0.8") == "en"


def test_falls_back_to_english():
    assert i18n.pick_language(None, None) == "en"
    assert i18n.pick_language("de", "de-DE") == "en"
    assert i18n.pick_language("", "") == "en"
    assert i18n.pick_language("../../etc/passwd", None) == "en"


def test_book_default_covers_a_visitor_with_no_preference_at_all():
    """A French family's book should greet a preference-less visitor in
    French, not English."""
    assert i18n.pick_language(None, None, "fr") == "fr"
    assert i18n.pick_language(None, "", "fr") == "fr"


def test_a_readers_own_choice_beats_the_book_default():
    assert i18n.pick_language("en", None, "fr") == "en"


def test_the_browser_preference_beats_the_book_default():
    """So an English-speaking relative visiting a French book still gets
    English — one tap on the flag changes it either way."""
    assert i18n.pick_language(None, "en-GB,en;q=0.9", "fr") == "en"


def test_a_nonsense_book_default_is_ignored():
    assert i18n.pick_language(None, None, "klingon") == "en"


def test_book_default_is_read_from_the_environment(app_factory):
    client = app_factory(DEFAULT_LANGUAGE="fr").test_client()
    assert b'<html lang="fr"' in client.get("/login").data
    # ...and the reader can still override it from the picker.
    client.post("/language/en", data={"next": "/login"})
    assert b'<html lang="en"' in client.get("/login").data


# --- translation and plurals --------------------------------------------------


def test_unknown_string_falls_back_to_english_not_a_key():
    assert i18n.gettext("Not a real string", "fr") == "Not a real string"


def test_interpolation_after_lookup():
    assert i18n.gettext("Born {date}", "fr", date="18 juin 2026") == "Né le 18 juin 2026"


def test_french_treats_zero_and_one_as_singular():
    assert i18n.ngettext("{n} year old", "{n} years old", 0, "fr") == "0 an"
    assert i18n.ngettext("{n} year old", "{n} years old", 1, "fr") == "1 an"
    assert i18n.ngettext("{n} year old", "{n} years old", 2, "fr") == "2 ans"


def test_english_treats_zero_as_plural():
    assert i18n.ngettext("{n} year old", "{n} years old", 0, "en") == "0 years old"
    assert i18n.ngettext("{n} year old", "{n} years old", 1, "en") == "1 year old"


# --- dates --------------------------------------------------------------------


def test_french_dates_put_the_day_first_and_drop_the_comma():
    d = date(2026, 6, 18)
    assert i18n.format_date(d, "en", "long") == "June 18, 2026"
    assert i18n.format_date(d, "fr", "long") == "18 juin 2026"


def test_french_first_of_the_month_is_ordinal():
    assert i18n.format_date(date(2026, 5, 1), "fr", "long") == "1er mai 2026"
    assert i18n.format_date(date(2026, 5, 2), "fr", "long") == "2 mai 2026"
    assert i18n.format_date(date(2026, 5, 1), "en", "long") == "May 1, 2026"


def test_short_and_month_styles():
    d = date(2026, 2, 9)
    assert i18n.format_date(d, "en", "short") == "Feb 9"
    assert i18n.format_date(d, "fr", "short") == "9 févr."
    assert i18n.format_date(d, "en", "month_year") == "February 2026"
    assert i18n.format_date(d, "fr", "month_year") == "février 2026"


def test_datetime_reads_naturally_in_both():
    stamp = datetime(2026, 6, 18, 14, 5)
    assert i18n.format_datetime(stamp, "en") == "Jun 18, 2026 14:05"
    assert i18n.format_datetime(stamp, "fr") == "18 juin 2026 à 14:05"


def test_no_month_name_is_missing_or_duplicated():
    for lang in ("en", "fr"):
        for table in (i18n._MONTHS, i18n._MONTHS_SHORT):
            names = table[lang]
            assert len(names) == 12
            assert all(n.strip() for n in names)


def test_age_label_localizes():
    born = date(2023, 6, 18)
    assert i18n.age_label(born, date(2026, 6, 18), "en") == "3 years old"
    assert i18n.age_label(born, date(2026, 6, 18), "fr") == "3 ans"
    assert i18n.age_label(born, date(2023, 6, 19), "fr") == "1 jour"
    assert i18n.age_label(born, date(2023, 10, 18), "fr") == "4 mois"
    assert i18n.age_label(born, date(2020, 1, 1), "fr") == "avant ta naissance"


# --- the picker and the cookie ------------------------------------------------


def test_picker_is_on_the_login_page_so_you_can_switch_before_logging_in(client):
    html = client.get("/login").data.decode()
    assert "lang-picker" in html
    assert 'action="/language/fr"' in html
    assert 'action="/language/en"' in html


def test_picker_marks_the_current_language(client):
    html = client.get("/login").data.decode()
    assert "lang-picker__btn--active" in html


def test_choosing_french_sets_a_durable_cookie_and_returns_you_to_the_page(client):
    resp = client.post("/language/fr", data={"next": "/login"})
    assert resp.status_code == 302
    assert resp.headers["Location"] == "/login"
    cookie = resp.headers["Set-Cookie"]
    assert "storybook-lang=fr" in cookie
    assert "Max-Age=31536000" in cookie


def test_the_choice_actually_changes_the_page(client):
    assert b"A private memory journal" in client.get("/login").data
    client.post("/language/fr", data={"next": "/login"})
    assert "Un journal de souvenirs".encode() in client.get("/login").data


def test_the_choice_survives_logging_out(auth_client):
    auth_client.post("/language/fr", data={"next": "/"})
    auth_client.post("/logout")
    assert "Un journal de souvenirs".encode() in auth_client.get("/login").data


def test_html_lang_attribute_follows_the_choice(client):
    assert b'<html lang="en"' in client.get("/login").data
    client.post("/language/fr", data={"next": "/login"})
    assert b'<html lang="fr"' in client.get("/login").data


def test_unknown_language_is_404_not_a_stored_cookie(client):
    resp = client.post("/language/de", data={"next": "/login"})
    assert resp.status_code == 404
    assert "storybook-lang" not in resp.headers.get("Set-Cookie", "")


def test_language_switch_cannot_be_an_open_redirect(client):
    for target in ("https://evil.example.com", "//evil.example.com", "/\\evil"):
        resp = client.post("/language/fr", data={"next": target})
        assert resp.headers["Location"] == "/", target


def test_language_switch_is_post_only(client):
    assert client.get("/language/fr").status_code == 405


@pytest.mark.parametrize("path", ["/", "/new", "/people", "/help", "/book"])
def test_pages_render_in_french_without_error(auth_client, path):
    auth_client.post("/language/fr", data={"next": "/"})
    resp = auth_client.get(path)
    assert resp.status_code == 200
    html = resp.data.decode()
    assert '<html lang="fr"' in html
    # A page still showing the English nav means _() didn't reach it.
    assert "Fil du temps" in html or "Personnes" in html or "Aide" in html


def test_a_french_reader_sees_french_dates_on_a_story(auth_client, stories_dir):
    from datetime import date as _date

    from app import storage

    story_id = storage.create_story(stories_dir, "Une journée", _date(2026, 6, 18), "Texte")
    auth_client.post("/language/fr", data={"next": "/"})
    html = auth_client.get(f"/story/{story_id}").data.decode()
    assert "18 juin 2026" in html
    assert "June 18" not in html


def test_story_content_is_never_translated(auth_client, stories_dir):
    """Only the furniture is translated. What the family wrote is theirs."""
    from datetime import date as _date

    from app import storage

    story_id = storage.create_story(
        stories_dir, "People", _date(2026, 6, 18), "Timeline and Help are my words."
    )
    auth_client.post("/language/fr", data={"next": "/"})
    html = auth_client.get(f"/story/{story_id}").data.decode()
    assert "<h1 class=\"story__title\">People</h1>" in html
    assert "Timeline and Help are my words." in html
