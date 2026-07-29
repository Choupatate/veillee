"""Tests for FEATURES.md F45: a toggle that looks off when it is off.

Every toggle in the app is a `.btn` with `aria-pressed`, and `.btn:hover`
borrows the accent for its border — the same accent that means "on". With a
pointer resting on a chip you had just switched off, the two states differed
by text colour alone; on a touch screen, where `:hover` sticks to the last
element tapped, they went on looking alike until you tapped elsewhere.

The fix is in CSS, so the tests are too: the lit state must carry something
hover can never give it, and hover on an unlit toggle must not reach for the
accent.
"""

import re
from pathlib import Path

MAIN_CSS = (Path(__file__).resolve().parent.parent / "app" / "static" / "css"
            / "main.css").read_text()

LIT_TOGGLES = (".editor__toggle-chip", ".editor__gender-btn")


def _rule(selector):
    match = re.search(re.escape(selector) + r" \{([^}]*)\}", MAIN_CSS)
    assert match, f"no rule for {selector}"
    return match.group(1)


def test_a_lit_toggle_is_filled_not_merely_outlined():
    """Border and text colour alone are exactly what a hover can imitate.
    The fill is the part hover never gives, so it is what actually tells
    the two states apart."""
    for selector in LIT_TOGGLES:
        body = _rule(selector + '[aria-pressed="true"]')
        assert "background: var(--color-highlight-bg)" in body, selector
        assert "border-color: var(--color-accent)" in body, selector
        assert "color: var(--color-accent)" in body, selector


def test_hovering_an_unlit_toggle_does_not_borrow_the_accent():
    """On a toggle the accent means on. `.btn:hover` gives every button an
    accent border, which on these has to be overridden — otherwise the chip
    you just switched off keeps looking lit under the pointer, and stays
    that way on a phone until something else is tapped."""
    body = _rule('.editor__toggle-chip[aria-pressed="false"]:hover,\n'
                 '.editor__gender-btn[aria-pressed="false"]:hover,\n'
                 '.editor__author-chip[aria-pressed="false"]:hover')
    assert "border-color: var(--color-text-dim)" in body


def test_the_override_comes_after_the_hover_it_overrides():
    """`.btn:hover` and `.editor__toggle-chip[aria-pressed="false"]:hover`
    are not the same weight, but the fill rule and `.btn:hover` both touch
    border-color — keep the toggle rules downstream of the base button so
    the cascade stays on the right side of this."""
    assert MAIN_CSS.index('.editor__toggle-chip[aria-pressed="true"]') > MAIN_CSS.index(".btn:hover")


def test_the_state_still_reaches_the_server(auth_client, stories_dir):
    """The paint was the bug, not the wiring — but the wiring is what makes
    the paint worth having, so pin the round trip too."""
    from app import storage

    resp = auth_client.post("/api/stories", json={
        "title": "Kept back", "date": "2026-02-01", "body": "not ready", "draft": True,
    })
    assert resp.status_code == 200
    story_id = resp.get_json()["id"]
    assert storage.get_story(stories_dir, story_id).draft is True

    resp = auth_client.put(f"/api/stories/{story_id}", json={
        "title": "Kept back", "date": "2026-02-01", "body": "ready now", "draft": False,
    })
    assert resp.status_code == 200
    assert storage.get_story(stories_dir, story_id).draft is False
