"""FEATURES.md F55: turning the page.

Cross-document view transitions are one at-rule and no JavaScript, which
makes them almost impossible to test and very easy to break by tidying.
Two things are worth pinning, and both are about *where* the at-rule sits
rather than that it exists:

- it must stay inside `prefers-reduced-motion: no-preference`, because a
  view transition is motion and this file opts *in* to animation
  everywhere else;
- the timing override must name `root`, since that is the only transition
  group a page with no `view-transition-name` anywhere produces.

Verified in a real Chromium (141) when it was written: with reduced motion
unset, `pagereveal` fires with `event.viewTransition` set; with reduced
motion on, it fires with no transition at all. That check needs a browser
and so lives in the commit message rather than here.
"""

import re
from pathlib import Path

import pytest

CSS = (Path(__file__).resolve().parent.parent
       / "app" / "static" / "css" / "main.css").read_text(encoding="utf-8")

REDUCED_MOTION_OPT_IN = "@media (prefers-reduced-motion: no-preference) {"


def _blocks(source: str, opener: str):
    """Every `opener { ... }` block in `source`, brace-counted so a nested
    rule doesn't end the block early."""
    for match in re.finditer(re.escape(opener), source):
        start = match.end()
        depth = 1
        for index in range(start, len(source)):
            if source[index] == "{":
                depth += 1
            elif source[index] == "}":
                depth -= 1
                if depth == 0:
                    yield source[start:index]
                    break


def test_the_at_rule_is_there_at_all():
    assert "@view-transition" in CSS


def test_transitions_are_opt_in_with_the_rest_of_the_animation():
    """Hoisting `@view-transition` to the top level would animate
    navigation for someone who asked their whole system not to."""
    inside = [b for b in _blocks(CSS, REDUCED_MOTION_OPT_IN) if "@view-transition" in b]
    assert inside, (
        "@view-transition is not inside a `prefers-reduced-motion: "
        "no-preference` block — a reader who asked for reduced motion "
        "would get the transition anyway"
    )


def test_navigation_is_auto_not_none():
    block = next(b for b in _blocks(CSS, REDUCED_MOTION_OPT_IN) if "@view-transition" in b)
    declaration = next(_blocks(block, "@view-transition {"))
    assert "navigation: auto" in declaration


@pytest.mark.parametrize("pseudo", ["::view-transition-old(root)", "::view-transition-new(root)"])
def test_both_halves_of_the_crossfade_are_timed(pseudo):
    """Timing only one side gives a fade-out and a snap-in."""
    assert pseudo in CSS


def test_the_duration_is_a_deliberate_number():
    """Not a guard against a specific value — a guard against the
    override being deleted and the platform default coming back
    silently."""
    block = next(b for b in _blocks(CSS, REDUCED_MOTION_OPT_IN) if "@view-transition" in b)
    durations = re.findall(r"animation-duration:\s*(\d+)ms", block)
    assert len(durations) >= 1
    assert all(120 <= int(d) <= 500 for d in durations), (
        f"{durations}ms — under ~120ms reads as no transition, over ~500ms "
        "as a slideshow"
    )
