"""FEATURES.md's index stays honest.

CLAUDE.md calls FEATURES.md "the most detailed and current source of truth
for how a given feature actually behaves", and at 7,000+ lines the index at
the top is the only way anyone finds anything in it. An index that has
quietly fallen a few features behind is worse than none: it looks
authoritative and it is wrong.

This is the same shape of guard as `test_i18n.py`'s — that one fails when a
`_("...")` lands with no French line, this one fails when a feature lands
with no index line. A convention nobody can forget beats a convention
everybody is asked to remember.

**Not tested here, deliberately: the order of the sections.** The file is
not in F-number order and it is not going to be. Its feature specs use
`##` for their own internal structure — F18 alone has `## Layer 1`,
`## API`, `## Tests`, `## Definition of done` — and five features are `#`
rather than `##`. Sorting the top-level headings would tear those specs
apart and interleave their subsections with unrelated features. The index
exists precisely so the order does not have to matter.
"""

import re
from pathlib import Path

import pytest

FEATURES = Path(__file__).resolve().parent.parent / "FEATURES.md"

#: A feature's own heading. Two levels because the file uses both, and the
#: `Feature spec — ` prefix because five of the older ones carry it.
HEADING_RE = re.compile(r"^#{1,2} (?:Feature spec — )?F(\d+)[.:\s]", re.M)

#: A line in the index at the top of the file.
INDEX_RE = re.compile(r"^- \*\*F(\d+)\*\*", re.M)


def _split():
    """The index, and everything after it. The first `# Feature spec`
    heading is where the log itself starts."""
    text = FEATURES.read_text(encoding="utf-8")
    lines = text.splitlines()
    for number, line in enumerate(lines):
        if line.startswith("# Feature spec"):
            return "\n".join(lines[:number]), "\n".join(lines[number:])
    pytest.fail("FEATURES.md has no feature specs — has the file moved?")


def test_every_feature_is_in_the_index():
    index, body = _split()
    documented = {int(n) for n in HEADING_RE.findall(body)}
    listed = {int(n) for n in INDEX_RE.findall(index)}
    missing = sorted(documented - listed)
    assert not missing, (
        f"F{missing} have sections in FEATURES.md but no line in its index. "
        "Add one — the index is how anyone finds anything in a 7,000-line "
        "file, and one that lags is worse than none."
    )


def test_the_index_points_at_nothing_that_is_gone():
    index, body = _split()
    documented = {int(n) for n in HEADING_RE.findall(body)}
    listed = {int(n) for n in INDEX_RE.findall(index)}
    stale = sorted(listed - documented)
    assert not stale, (
        f"the index lists F{stale}, which have no section in the file"
    )


def test_the_index_has_no_duplicate_entries():
    index, _body = _split()
    listed = INDEX_RE.findall(index)
    duplicates = sorted({n for n in listed if listed.count(n) > 1}, key=int)
    assert not duplicates, f"F{duplicates} appear in the index twice"


def test_no_feature_number_is_used_twice():
    """Two features sharing a number is how the index stops being able to
    point at either of them. Follow-ups are exempt: `## F51 follow-up 2`
    deliberately reuses its parent's number, and reads as part of it."""
    _index, body = _split()
    headings = re.findall(
        r"^#{1,2} (?:Feature spec — )?(F\d+[.:][^\n]*)$", body, re.M
    )
    seen = {}
    for heading in headings:
        number = int(re.match(r"F(\d+)", heading).group(1))
        seen.setdefault(number, []).append(heading)
    clashes = {n: h for n, h in seen.items() if len(h) > 1}
    assert not clashes, f"reused feature numbers: {clashes}"


def test_the_index_says_how_to_use_it():
    """The one instruction that makes an unordered file navigable — search
    for the heading text rather than scrolling — has to survive edits to
    the preamble."""
    index, _body = _split()
    assert "F<N>." in index, (
        "the index no longer tells the reader to search for the exact "
        "heading text, which is the only way to navigate a file that is "
        "not in numeric order"
    )


def test_the_newest_feature_is_documented():
    """A cheap canary for the file being appended to without its index
    being touched: the highest-numbered feature in the body must be listed.
    """
    index, body = _split()
    documented = {int(n) for n in HEADING_RE.findall(body)}
    listed = {int(n) for n in INDEX_RE.findall(index)}
    assert documented, "no features found at all"
    assert max(documented) in listed
