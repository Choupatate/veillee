"""Every vendored third-party library ships its licence and its provenance.

CLAUDE.md's rule: "If you vendor a new third-party library, document its
version and provenance in a banner comment the way
`toastui-editor-all.min.js` does." That rule was written *about* the Toast
UI bundle, and the Toast UI folder was the one that went a year with no
`LICENSE` file at all while `d3/` and `familychart/` both had one.

The bundle's own banner had always named the licence, so nothing looked
wrong from inside the code. What was missing was the text MIT asks to be
distributed with copies — the kind of gap that stays invisible until
somebody redistributes the app, which is exactly what this app is for.

So the convention is a test now rather than a paragraph. It is also
deliberately about *files on disk*, not about what a page renders: the
obligation attaches to the copy in the repository.
"""

import re
from pathlib import Path

import pytest

VENDOR = Path(__file__).resolve().parent.parent / "app" / "static" / "vendor"

#: One directory per vendored library.
LIBRARIES = sorted(p for p in VENDOR.iterdir() if p.is_dir())

#: Enough of the MIT/ISC/BSD grant to tell a real licence from a stub.
GRANT_RE = re.compile(r"permission (is hereby granted|to use)", re.I)


def test_there_is_something_to_check():
    assert LIBRARIES, "no vendored libraries found — has app/static/vendor moved?"


@pytest.mark.parametrize("library", LIBRARIES, ids=lambda p: p.name)
def test_every_vendored_library_ships_its_licence(library):
    licence = library / "LICENSE"
    assert licence.is_file(), (
        f"{library.name}/ has no LICENSE. Vendoring a library means "
        "redistributing it, and every licence this app's dependencies use "
        "asks for the notice to travel with the copy."
    )
    text = licence.read_text(encoding="utf-8")
    assert GRANT_RE.search(text), f"{library.name}/LICENSE has no grant of rights in it"
    assert re.search(r"copyright", text, re.I), (
        f"{library.name}/LICENSE names no copyright holder"
    )


@pytest.mark.parametrize("library", LIBRARIES, ids=lambda p: p.name)
def test_every_vendored_library_has_its_provenance_written_down(library):
    """Where it came from, which version, and how to rebuild it.

    `d3/` has no `VENDORED.md` of its own and does not need one — it is
    family-chart's required peer and is documented in that folder's file.
    What matters is that some `VENDORED.md` in here accounts for it, so
    nothing sits in this tree unexplained.
    """
    notes = list(VENDOR.glob("*/VENDORED.md"))
    assert notes, "no VENDORED.md anywhere under app/static/vendor"
    own = library / "VENDORED.md"
    if own.is_file():
        return
    mentioned = any(library.name in n.read_text(encoding="utf-8") for n in notes)
    assert mentioned, (
        f"{library.name}/ has no VENDORED.md and is not mentioned in any "
        "other one — say where it came from, at what version, and how to "
        "rebuild it"
    )


@pytest.mark.parametrize("library", LIBRARIES, ids=lambda p: p.name)
def test_each_served_file_carries_a_licence_notice(library):
    """The notice has to be in the file a browser downloads, not only in a
    markdown file beside it.

    Toast UI's dark theme stylesheet is the reason this is checked: upstream
    ships it without a banner, so the one copy of it this app serves went
    out with no copyright line on it. A banner was added locally, and
    `VENDORED.md` records that as the folder's only local edit.
    """
    served = [
        p for p in library.rglob("*")
        if p.is_file() and p.suffix in (".js", ".css")
    ]
    assert served, f"{library.name}/ ships no js or css"
    naked = []
    for path in served:
        head = path.read_text(encoding="utf-8", errors="replace")[:1500]
        if not re.search(r"copyright|@license|licen[cs]ed under", head, re.I):
            naked.append(str(path.relative_to(VENDOR)))
    assert not naked, (
        f"{naked} are served to browsers with no licence notice in the first "
        "1500 characters — add a banner comment and record it in the "
        "folder's VENDORED.md as a local edit"
    )


def test_the_vendor_tree_holds_nothing_but_libraries():
    """A loose file at the top of `vendor/` belongs to no library, so
    nothing above would check it."""
    loose = sorted(p.name for p in VENDOR.iterdir() if p.is_file())
    assert not loose, (
        f"{loose} sit directly in app/static/vendor/ — put a vendored file "
        "in its library's folder so its licence is accounted for"
    )
