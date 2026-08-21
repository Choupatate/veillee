"""What a theme pack is made of, and how to ask an AI for each piece (F50).

Thirty-seven pictures, described by the *job* each one does rather than by
what the ranch happens to draw for it. That distinction is the whole file.
`login-campfire.jpg` is not "a campfire": it is the welcome on the login
page, the thing that says *this is a private place, come and sit down* —
and in a book kept in orbit that is a fire in a viewport, in a woodblock
world it is a paper lantern. The filename never changes, because a pack is
a skin and not a rename (CLAUDE.md), so the filename cannot be the brief.

Each entry therefore carries two lines: `where` (so the person filling
this in knows what page they are dressing) and `subject` (what the picture
has to show for that page to make sense), plus the size the app draws it
at.

`prompt_for` glues an entry to the description of the world someone wrote,
and adds the rules this project learned the hard way over F17, F22, F42 and
F46 — no lettering, no corner watermark, no paper border, and, for icons, a
dark outline without which nothing survives on both a light and a dark
page. They are stated every time because a generator forgets between
images, not because the reader needs reminding.
"""

from dataclasses import dataclass

PLATE = "plate"
ICON = "icon"
ORNAMENT = "ornament"
TILE = "tile"


@dataclass(frozen=True)
class Asset:
    filename: str
    kind: str
    where: str
    subject: str
    width: int
    height: int

    @property
    def is_icon(self) -> bool:
        return self.kind == ICON

    @property
    def wants_transparency(self) -> bool:
        return self.kind in (ICON, ORNAMENT)


#: Every picture a pack can draw, in the order it is worth drawing them:
#: the pages a family meets first, then the rest, then the icons, which are
#: the fiddliest and the least missed while they are still borrowed.
CATALOG = (
    Asset("login-campfire.jpg", PLATE, "the login page",
          "the welcome: a gathering point that says this is a private, warm "
          "place to come and sit down. No people's faces.", 856, 735),
    Asset("empty-chest.jpg", PLATE, "the timeline, before the first story",
          "something open and waiting to be filled — a container with "
          "nothing in it yet, hopeful rather than sad.", 653, 729),
    Asset("book-frame.jpg", PLATE, "the top of the printable book",
          "the whole book as one object, closed, seen as a keepsake.", 715, 897),
    Asset("person-oval.jpg", PLATE, "a person in the cast with no photo yet",
          "an empty upright portrait frame, oval, waiting for a face. The "
          "frame is the subject; nobody is in it.", 600, 732),
    Asset("group-circle.jpg", PLATE, "the Groups page — who can read a story",
          "a small closed circle of figures seen from outside, shoulders "
          "turned inward, so it reads as \"these people and no others\". "
          "Silhouettes, no faces.", 760, 612),
    Asset("write-link-pass.jpg", PLATE, "a delegated one-off write link",
          "a single-use pass: one small token that opens one door, once, and "
          "is spent afterwards.", 700, 600),
    Asset("invite-card.jpg", PLATE, "the invitation page",
          "an invitation being handed over — something offered from one hand "
          "toward another.", 700, 564),
    Asset("sealed-letter.jpg", PLATE, "a story sealed until a future date",
          "something closed and sealed, plainly not to be opened yet.", 576, 495),
    Asset("firsts-boots.jpg", PLATE, "the Firsts page",
          "first times: the smallest pair of something worn or used, kept "
          "long after it was outgrown.", 760, 519),
    Asset("growth-doorpost.jpg", PLATE, "the Growing up page",
          "the marks that measure a child growing — a series of small "
          "notches climbing a vertical surface, the oldest lowest.", 567, 760),
    Asset("almanac-book.jpg", PLATE, "the Almanac — the family's year",
          "the year coming round again: a book or dial of dates that "
          "repeat.", 700, 700),
    Asset("history-pages.jpg", PLATE, "a story's earlier versions",
          "the previous version still there: pages layered so an older one "
          "shows beneath the newest.", 720, 598),
    Asset("accounts-keys.jpg", PLATE, "the Accounts page",
          "everyone has their own key: several different keys hanging "
          "together, no two alike.", 760, 540),
    Asset("help-lantern.jpg", PLATE, "the Help page",
          "a light to read by — small, carried, enough to see the next few "
          "steps. Not a manual, not a sign.", 628, 700),
    Asset("instant-camera.jpg", PLATE, "the Instants page",
          "a photo and one line, taken in fifteen seconds: a simple camera "
          "that prints at once.", 522, 652),
    Asset("tree-sapling.jpg", PLATE, "the family tree, before anyone is added",
          "a young growing thing with its branches not yet out — a family "
          "not yet drawn.", 760, 739),
    Asset("tumbleweed.jpg", PLATE, "a quiet stretch with no new stories",
          "the sign of a long quiet: something drifting alone across an "
          "empty place. Gently funny, never a reproach.", 900, 488),
    Asset("tree-map.jpg", TILE, "behind the family tree, on a pale page",
          "the ground the family is drawn on: a faint chart or map, "
          "light-toned and busy with nothing in particular, since names sit "
          "on top of it and must stay readable.", 900, 900),
    Asset("tree-map-dark.jpg", TILE, "behind the family tree, on a dark page",
          "the same ground as tree-map.jpg, remade dark: the identical "
          "chart at night, still faint, names still readable on top.", 900, 900),
    Asset("tree-map-tile.jpg", TILE, "the tiling version of tree-map.jpg",
          "the same pale chart, but seamless — every edge must meet its "
          "opposite so it repeats without a visible seam.", 1024, 1024),
    Asset("tree-map-tile-dark.jpg", TILE, "the tiling version of tree-map-dark.jpg",
          "the same dark chart, seamless in the same way.", 1024, 1024),
    Asset("rope-divider.png", ORNAMENT, "the line between sections",
          "a long horizontal ornament that divides two parts of a page — a "
          "cord, a band, a run of small marks. Much wider than it is tall, "
          "and it must read at a glance.", 1000, 144),
    Asset("lasso-ring.png", ORNAMENT, "the spinner, while something saves",
          "a closed loop, drawn so it still reads as a loop while it spins. "
          "Simple: it turns at small size.", 320, 320),
    Asset("brand-star.png", ORNAMENT, "the mark beside the book's name",
          "one small emblem for the whole book — the simplest shape in the "
          "set, recognisable at the size of a full stop.", 240, 240),
    Asset("icon-new-story.png", ICON, "the + New story button",
          "writing something down: a writing tool over a surface.", 160, 160),
    Asset("icon-instant.png", ICON, "the + Instant button",
          "a camera seen head-on, one round lens.", 160, 160),
    Asset("icon-save.png", ICON, "the Save button",
          "a thick downward arrow coming to rest on a short horizontal bar.",
          160, 160),
    Asset("icon-draft.png", ICON, "the Draft toggle",
          "unfinished: the same shape twice, one solid and one drawn as a "
          "few thick dashes with wide gaps.", 160, 160),
    Asset("icon-archive.png", ICON, "the Archive toggle",
          "a wide storage box seen square-on, wider than tall, with a "
          "separate lid bar across the top.", 160, 160),
    Asset("icon-seal.png", ICON, "sealing a story until a date",
          "something closed with a single round seal on its seam.", 160, 160),
    Asset("icon-source.png", ICON, "adding a source link to a story",
          "a link to somewhere else: two thick interlocking shapes, or a "
          "dish pointing away.", 160, 160),
    Asset("icon-record.png", ICON, "the voice recorder",
          "a microphone head with two sound arcs beside it.", 160, 160),
    Asset("icon-print.png", ICON, "printing the book",
          "a flat sheet emerging from a slot.", 160, 160),
    Asset("icon-import.png", ICON, "restoring a backup",
          "an arrow going in: an arrowhead entering an open container.",
          160, 160),
    Asset("icon-tree.png", ICON, "the family tree",
          "three small shapes joined by two straight struts, one above two.",
          160, 160),
    Asset("icon-new-person.png", ICON, "adding someone to the cast",
          "one figure's silhouette with a small plus beside it. Head and "
          "shoulders only, no face.", 160, 160),
    Asset("icon-group.png", ICON, "the Groups page",
          "three figures' silhouettes gathered inside one enclosing shape.",
          160, 160),
)

BY_FILENAME = {asset.filename: asset for asset in CATALOG}


def aspect_words(asset: Asset) -> str:
    if asset.width > asset.height * 1.15:
        return "landscape"
    if asset.height > asset.width * 1.15:
        return "portrait"
    return "square"


#: Said on every prompt because a generator forgets between images. Each
#: line is a mistake this project actually had to undo by hand.
PLATE_RULES = (
    "No lettering, numbers, words or signature anywhere in the image.",
    "No watermark, logo or sparkle in any corner.",
    "No paper border, mount or frame around the picture — the app draws "
    "its own.",
    "One subject, centred, with room around it.",
)

ICON_RULES = (
    "A single flat icon, centred, filling most of the square.",
    "Bold enough to read at 20 pixels: thick shapes, no thin lines, no "
    "small details, no lettering.",
    "Outline every shape in a dark colour, about a tenth of the icon's "
    "width — without it an icon vanishes on either the light or the dark "
    "page, whichever it matches.",
    "Two or three colours at most, flat, no gradients.",
    "Plain mid-grey background, no shadow — the background is cut away.",
)

TILE_RULES = (
    "Seamless: every edge must meet its opposite so it repeats without a "
    "visible seam.",
    "Faint and low-contrast — text and photographs sit on top of this and "
    "have to stay readable.",
    "No lettering, no watermark, no border.",
)


def rules_for(asset: Asset) -> tuple:
    if asset.is_icon:
        return ICON_RULES
    if asset.kind == TILE:
        return TILE_RULES
    if asset.kind == ORNAMENT:
        return ICON_RULES[:1] + ICON_RULES[2:]
    return PLATE_RULES


def prompt_for(asset: Asset, description: str) -> str:
    """One copy-and-paste prompt: the world someone described, the job this
    picture does in it, and the rules that keep what comes back usable."""
    world = (description or "").strip() or "A simple, warm, hand-drawn style."
    lines = [
        f"Draw one picture in this style: {world}",
        "",
        f"Subject: {asset.subject}",
        "",
    ]
    lines += [f"- {rule}" for rule in rules_for(asset)]
    lines += [
        "",
        f"Size: {aspect_words(asset)}, about {asset.width} by {asset.height} "
        "pixels.",
    ]
    return "\n".join(lines)
