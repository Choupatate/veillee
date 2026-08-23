"""Turning a made pack's three colours into a working theme (F50).

A pack that ships with the app writes its own `theme.css`. A pack a family
makes cannot: user-authored CSS on every page is the one place in this app
where someone else's text would become code, and a same-origin stylesheet
is not something a Content-Security-Policy can save you from. So a made
pack's colours are *data* — validated hex, in its `theme.json` — and this
module renders them into the same variables `orbit/theme.css` declares by
hand.

The other reason is the form. `theme.css` re-declares sixteen variables per
scheme; asking anyone to fill that in twice is asking them not to make a
theme at all. So a scheme is **three colours** — a background, a text
colour, an accent — and everything else is derived from them here: dimmed
text is text mixed back toward the background, a border is the background
nudged toward the text, the highlight is the accent at low alpha. The
derivations are deliberately boring, because their job is to be right for
any three colours someone picks, not to be clever for one.
"""

import re

_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

#: What a scheme is: three colours, and nothing else to fill in.
SEEDS = ("bg", "text", "accent")


def is_hex(value) -> bool:
    return bool(isinstance(value, str) and _HEX_RE.match(value.strip()))


def parse_hex(value) -> tuple[int, int, int]:
    """`#abc` and `#aabbcc` alike, as 0-255 channels. Callers validate with
    `is_hex` first; this raises rather than guessing."""
    if not is_hex(value):
        raise ValueError(f"not a hex colour: {value!r}")
    digits = value.strip().lstrip("#")
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    return tuple(int(digits[i : i + 2], 16) for i in (0, 2, 4))


def to_hex(rgb) -> str:
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(c))) for c in rgb)


def mix(a, b, amount: float) -> tuple[int, int, int]:
    """`amount` of `b` mixed into `a`, per channel. Plain sRGB rather than
    a perceptual space: these are small nudges between colours a person
    already chose to sit together, and a linear mix keeps the result
    predictable from the seeds."""
    ratio = max(0.0, min(1.0, amount))
    return tuple(a[i] + (b[i] - a[i]) * ratio for i in range(3))


def relative_luminance(rgb) -> float:
    """WCAG 2.1 relative luminance."""
    channels = []
    for value in rgb:
        c = value / 255
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(a, b) -> float:
    """WCAG contrast ratio, 1 to 21."""
    first, second = relative_luminance(a), relative_luminance(b)
    lighter, darker = max(first, second), min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def is_dark(bg) -> float:
    """Whether a scheme reads as dark, decided by its background rather
    than by its name — someone's "manuscript" is pale and someone else's
    is a candlelit study, and `color-scheme` has to match what is actually
    on screen or the browser draws its scrollbars and form controls in the
    wrong world."""
    return relative_luminance(parse_hex(bg)) < 0.4


#: What a dimmed label still has to clear against its background. Below
#: this it isn't dimmed, it's gone.
DIM_FLOOR = 4.5
#: A border is not text; it only has to be visible as an edge.
EDGE_FLOOR = 1.5


def _mix_to_floor(base, target, amount, *, against, floor, step=0.04):
    """Mix `target` into `base`, backing off until the result clears
    `floor` against `against`.

    The plain mix is right for the colours most books are built from — an
    off-white on a near-black, a dark brown on cream. It is wrong for a
    saturated one: mixing neon magenta toward a dark purple background
    produces 2.5:1, which is a label nobody can read. So the mix is a
    starting point and the contrast is the constraint.
    """
    amount = max(0.0, min(1.0, amount))
    while amount > 0:
        candidate = mix(base, target, amount)
        if contrast(candidate, against) >= floor:
            return candidate
        amount -= step
    return base


def _mix_up_to_floor(base, target, amount, *, against, floor, limit=0.6, step=0.04):
    """The other direction: mix further in until the result is at least
    `floor` — for an edge that would otherwise be invisible."""
    amount = max(0.0, min(1.0, amount))
    candidate = mix(base, target, amount)
    while contrast(candidate, against) < floor and amount < limit:
        amount += step
        candidate = mix(base, target, amount)
    return candidate


def _rgb_triple(rgb) -> str:
    """`150, 205, 255` — main.css's ambience variables are bare channels so
    the CSS can wrap them in rgba() with its own alpha."""
    return ", ".join(str(round(c)) for c in rgb)


def derive(seed: dict, texture: str | None = None) -> dict:
    """Every variable one scheme sets, from `{bg, text, accent}`.

    `texture` is a CSS url() for the pack's tile, or None for a scheme with
    no tile — a flat background is a complete theme, and the tile is an
    extra someone can add later.
    """
    bg = parse_hex(seed["bg"])
    text = parse_hex(seed["text"])
    accent = parse_hex(seed["accent"])
    dark = relative_luminance(bg) < 0.4

    # The label drawn *on* the accent — whichever of the reader's own two
    # colours can be read against it. Picked by measurement, because an
    # accent light enough to need dark text is a choice someone is allowed
    # to make.
    accent_text = bg if contrast(accent, bg) >= contrast(accent, text) else text

    variables = {
        "--color-bg": to_hex(bg),
        "--color-bg-raised": to_hex(mix(bg, text, 0.07)),
        "--color-text": to_hex(text),
        "--color-text-dim": to_hex(
            _mix_to_floor(text, bg, 0.42, against=bg, floor=DIM_FLOOR)
        ),
        "--color-accent": to_hex(accent),
        "--color-accent-text": to_hex(accent_text),
        "--color-highlight-bg": "rgba(%s, 0.18)" % _rgb_triple(accent),
        "--color-border": to_hex(
            _mix_up_to_floor(bg, text, 0.18, against=bg, floor=EDGE_FLOOR)
        ),
        # The mount an illustration sits on: barely off the page, with an
        # edge just visible enough to read as a frame.
        "--illo-mount": to_hex(mix(bg, text, 0.04)),
        "--illo-mount-edge": to_hex(
            _mix_up_to_floor(bg, text, 0.18, against=bg, floor=EDGE_FLOOR)
        ),
        # F44's firelight, which is a wash of the accent: pale backgrounds
        # swallow it, so they get more of it.
        "--ambience-glow": _rgb_triple(mix(accent, (255, 255, 255), 0.35)),
        "--ambience-glow-edge": _rgb_triple(accent),
        "--ambience-shade": _rgb_triple(bg),
        "--firelight-strength": "1" if dark else "1.6",
        "--surface-texture": texture or "none",
        "color-scheme": "dark" if dark else "light",
    }
    if texture:
        variables["--surface-texture-size"] = "512px 512px"
    return variables


def _complete(seed) -> bool:
    return isinstance(seed, dict) and all(is_hex(seed.get(key)) for key in SEEDS)


def _block(selector: str, variables: dict, indent: str = "  ") -> str:
    lines = [f"{selector} {{"]
    for name, value in variables.items():
        lines.append(f"{indent}{name}: {value};")
    lines.append("}")
    return "\n".join(lines)


def render_css(palette: dict, schemes, extra=None, name: str = "") -> str:
    """A made pack's whole stylesheet, in the shape `orbit/theme.css` is
    written by hand.

    `extra` is variables that belong to the pack rather than to one
    scheme — the divider and the brand mark, which main.css reaches through
    a variable and a template's `theme_img()` therefore never sees. They go
    in the `:root` block, where every scheme inherits them.

    Four kinds of block, and the order is what makes them work:
    `:root` carries the pack's default scheme; a `prefers-color-scheme`
    query re-declares the pale one for readers who have chosen nothing; and
    one `[data-theme=...]` block per scheme lets the nav toggle win over
    both. A scheme missing from `palette` is simply not emitted — the nav
    only offers what `theme.json` declares anyway.
    """
    extra = extra or {}
    # A palette that came back from a backup, or was edited by hand, can say
    # anything at all. A scheme whose colours aren't colours is skipped
    # rather than raised on: the cost is a scheme that looks like main.css,
    # and the alternative is a stylesheet route that 500s a whole book.
    usable = [s for s in schemes if _complete(palette.get(s))]
    if not usable:
        return ""

    # The default is the pack's own first scheme, which is what a reader
    # with no stored choice and a dark system gets.
    default = usable[0]
    out = [
        f"/* {name or 'A made theme'} — generated from theme.json (F50)."
        "\n * Edited through the app, not by hand: any change here is lost"
        "\n * the next time the palette is saved. */",
        _block(":root", {**derive(palette[default]), **extra}),
    ]

    # Whichever offered scheme is the pale one answers the system
    # preference. A pack with no pale scheme leaves the query out entirely
    # rather than pretending.
    pale = next((s for s in usable if not is_dark(palette[s]["bg"])), None)
    if pale:
        inner = _block(":root:not([data-theme])", derive(palette[pale]))
        out.append(
            "@media (prefers-color-scheme: light) {\n"
            + "\n".join("  " + line for line in inner.split("\n"))
            + "\n}"
        )

    for scheme in usable:
        out.append(_block(f':root[data-theme="{scheme}"]', derive(palette[scheme])))
    return "\n\n".join(out) + "\n"
