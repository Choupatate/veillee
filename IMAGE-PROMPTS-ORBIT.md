# Image prompts — the *orbit* theme pack

Prompts for the artwork of the **orbit** theme pack (F46): the same book,
kept somewhere off Earth. `IMAGE-PROMPTS.md` is the equivalent document for
the default *ranch* pack; this one exists separately because a house style
belongs to one art direction, and mixing two sets of style rules in one
file is how a pack drifts.

Generate externally, process locally, commit the result under
`app/static/themes/orbit/img/` — the app never fetches an image at runtime.

**Status: complete.** All 17 illustrations are generated, processed and
committed, and all 13 icons are in.

**The icons are drawn, not generated** — `scripts/draw_orbit_icons.py`,
in Pillow, from the subject table at the end of this file. That was not the
original plan and it is worth saying why it changed. An icon here is four
flat colours, a dark keyline and one silhouette that has to survive being
shown at twenty pixels: that is geometry rather than illustration, and it
is the thing a generator does worst — it softens small shapes, forgets the
outline between one image and the next, and will not hold thirteen drawings
to a single style. Drawing them also makes the set reproducible, which the
plates are not: change a colour in the script and all thirteen redraw.

The two icons that came from the generator (`icon-new-story`,
`icon-instant`) predated the outline rule below and were redrawn with the
rest, as this file previously said they should be — a half-outlined icon
set looks like a mistake.

The prompts in the icon section are kept as-is. They are still the right
brief, they are what the drawing follows, and they are what anyone making a
*different* pack should start from.

**Nothing here is blocking.** The orbit pack works with any subset: its
palette is complete, and any picture it hasn't drawn falls back to the
ranch's (`app/themes.py`). Generate one at a time, in any order; each one
that lands simply replaces a fallback.

**Every prompt below is complete.** Copy one whole fenced block into Gemini
as-is; the style, the ground, the size constraint and the negatives are
already inside each one. Nothing needs assembling.

Each entry says, first, **what a reader has to understand from the picture
alone** — the test the image has to pass for someone who reads none of the
words on the page.

## The house style of this pack

Written out here once so the prompts can stay short, and so a future asset
can be matched to the set:

- **A retro-futurist cutaway plate**, the way a 1970s space encyclopaedia
  or a mission patch was drawn: flat colour, confident linework, no
  photographic rendering, no lens flare, no chrome gradients.
- **Ground: deep blue-black** (`#0d1424`), not pure black — the same plate
  the `.illo` class mounts every picture on. Stars are sparse and small;
  this is an instrument drawing, not a nebula poster.
- **Palette:** instrument cyan (`#5cc8f5`), pale starlight (`#dce6f5`), one
  warm accent for life and danger — a rust orange (`#c8622f`) used sparingly,
  usually on a suit stripe or a planet's band. Nothing neon, nothing purple.
- **Figures are cosmonauts**: rounded helmets with a dark visor, soft
  suits with ribbed joints, generous silhouettes. They read as *people* —
  small, gestural, backs and three-quarter views — never as portraits, for
  the same reason as the ranch pack: these sit next to photographs of a
  real family.
- **Planets are the furniture**: banded gas giants, ringed worlds, small
  cratered moons. Rings are the pack's signature shape — it is what makes
  an icon legible at 20px.

Three hard rules. The first two are carried over from the ranch pack;
the third is what the first batch of generations taught:

**No lettering, ever.** The interface is bilingual (F38). A word baked into
an illustration can't be translated and will sit there in English on a
French page forever. No console labels, no dial numbers, no mission
patches with words, no star charts with names. If lettering appears anyway,
reply *"remove all text, numerals and lettering; leave those surfaces blank
or with faint tick marks"*.

**No faces.** Visors are **dark, opaque and reflective** — you cannot see
through them at all. This is a style choice in the ranch pack and a
stronger one here: an empty visor lets any reader be the cosmonaut. A
generation that shows eyes, a nose or a smile behind the glass is a
regeneration, not a keeper.

**No corner mark, no signature, no border.** Two things generators like to
add that both have to be asked away:

- *A sparkle, star, diamond or logo in a corner.* Every generation in the
  first batch came back with a small grey four-pointed sparkle stamped
  about 100 pixels in from the bottom-right corner. Ask for it not to be
  there — and check anyway, because the request is not always honoured.
  (The processing script covers that exact spot regardless; see below.)
- *A paper or card border around the picture.* Several plates came back
  matted on cream stock, which fights the pack's dark `--illo-mount` and
  reads as a double frame. The artwork has to run edge to edge.

## How to run these through Gemini

1. **One asset per conversation.** Paste the block, generate, then iterate
   in the same thread ("keep everything, make the ring thicker and tilt it
   further") rather than re-pasting a modified prompt — the thread holds
   the style steady.
2. **Anchor the style with a real file** once you have one. Upload the
   first orbit asset you're happy with alongside the next prompt and add:
   *"Match the linework, colour palette and background of this image
   exactly."* Until then, the style paragraph in each prompt is doing that
   job alone, so read the first few generations critically.
3. **Generate three or four** of each and pick by the squint test. Cheap to
   do, and these compositions either read at thumbnail size or they don't.
4. **Aspect ratio is stated in words** (Gemini takes no `--ar` flag). If a
   generation comes back square when the prompt asked for wide, say *"same
   image, wider composition, more empty space left and right"*.

## Processing what comes back

Same pipeline as the ranch pack, with two differences — step 1 and step 2:

1. **Trim off any cream border and cover the corner mark.** Both are
   mechanical and neither depends on the generation: the border is a
   uniformly light margin, and the sparkle sits at a fixed inset (97-144
   pixels from the right and bottom edges, about 47 across), so it is
   covered by geometry rather than by detection — which is the only thing
   that works on the plates where it is a pale mark on pale regolith. It
   is replaced with the same box copied from directly above it. F46 in
   FEATURES.md records the script that did this for the first batch.
2. **Keep the deep blue-black background baked into the JPEG.** The `.illo`
   class mounts it as a plate in every colour scheme — including the light
   ones, where it reads as a viewport cut into the page. (The orbit pack
   sets `--illo-mount: #0d1424` for exactly this; the picture's own
   background has to match it or the card will show a seam.)
3. Downscale to roughly 2× display size (~700-760px on the long edge),
   save as JPEG quality 82, and keep each page under ~150 KB of added
   illustration weight.
4. **The squint test**: view it at 250px wide. If the idea disappears, ask
   for fewer elements and larger shapes, not more detail.
5. Look at it in **both colour schemes** at a 390px viewport before
   committing — the day side is where a too-dark plate goes wrong.
6. Add the file to F46's table in FEATURES.md so the inventory stays true.

**Icons are different** and follow F22's rules, not these: transparent PNG,
no background plate, bold flat shapes that survive 20px, a 2% square
margin. Their section is at the end.

## Where to start

The illustrations are done. **The icons are what is left**, and they are
what a reader notices next: every button on a blue page is still wearing
the ranch's brown leather. Thirteen of them, one prompt, a table of
subjects — the last section of this file.

Two of the illustrations took a second pass, and both for reasons worth
remembering when the icons come back:

- `group-circle.jpg` — the first generation showed the crew's faces
  through their visors. It is the one picture in the app that has to
  *teach* rather than decorate, and a face turns it into a portrait. The
  fix was one sentence in the prompt: *every visor is completely dark and
  opaque*.
- `login-campfire.jpg` — simply missed in the first batch, and it is the
  first thing anyone ever sees.

---

## 1. The welcome — `login-campfire.jpg`

**Replaces:** the ranch's campfire on the login page and the timeline's
footer. **Committed at:** ~760×520, wide.

**What the reader must understand without reading a word:** this is a warm,
private place where a small group gathers to tell each other things. Not a
product, not a facility — a hearth, even in a vacuum.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering, no lens flare, no chrome.

Scene: three cosmonauts in soft ribbed spacesuits with rounded helmets sit
close together on the regolith of a small moon, gathered around a low
lantern that casts a pale cyan glow up onto their suits. Their visors are
dark and reflective — no faces visible. Behind and above them, a large
banded gas giant with a tilted ring system fills a third of the sky, lit
from one side. A few small sparse stars. One of the seated figures leans
toward another as if mid-story.

Background: deep blue-black, hex #0d1424, filling the whole frame edge to
edge. Palette: instrument cyan #5cc8f5 and pale starlight #dce6f5 for
light, one rust orange #c8622f used sparingly on a suit stripe.

Wide landscape composition, roughly 4:3, with quiet empty space left and
right. The three figures should read as a single warm cluster at thumbnail
size.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals, no mission patches with words. No
faces. No neon, no purple, no photographic realism.
```

---

## 2. A person without a photo — `person-oval.jpg`

**Replaces:** the ranch's oval portrait frame, shown for anyone with no
photo. **Committed at:** ~400×500, portrait.

**What the reader must understand:** someone is here, we just don't have a
picture of them yet. It must feel like a *placeholder held open for
someone*, not like an error or an anonymous silhouette.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a single empty spacesuit helmet, three-quarter view, drawn as a
warm and inviting object rather than an eerie one — rounded, soft-shouldered,
with a dark reflective visor that shows a small curved reflection of a
ringed planet. The helmet sits inside a simple oval instrument frame with a
thin cyan bezel, like a porthole. Nothing inside the helmet is visible.

Background: deep blue-black, hex #0d1424, filling the frame. Palette:
instrument cyan #5cc8f5, pale starlight #dce6f5, a single rust orange
#c8622f line on the helmet's collar.

Upright portrait composition, roughly 4:5, the helmet centred and large
enough to read clearly at 120 pixels tall.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals. No face, no eyes, no skull imagery —
this must feel like a seat kept warm, never like a ghost.
```

---

## 3. The empty book — `empty-chest.jpg`

**Replaces:** the ranch's empty chest, shown when a timeline has no stories
yet. **Committed at:** ~700×560.

**What the reader must understand:** nothing has been written yet, and that
is a beginning rather than a fault. The picture should invite, not
apologise.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: an open, empty equipment locker or sample case, floating gently in
zero gravity with its lid ajar and a soft cyan light spilling from inside
it. The interior is lined and empty — clearly ready to hold something, not
broken or ransacked. Two or three tiny drifting objects near it suggest
weightlessness. A distant ringed planet, small, in one corner.

Background: deep blue-black, hex #0d1424, filling the frame. Palette:
instrument cyan #5cc8f5, pale starlight #dce6f5, one rust orange #c8622f
band on the case.

Landscape composition, roughly 5:4, with quiet empty space around the case.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals. Nothing damaged, nothing sinister — the
case is waiting, not abandoned.
```

---

## 4. Groups — the one that has to teach — `group-circle.jpg`

**Replaces:** the ranch's rope circle on the Help page. **Committed at:**
~760×612, wide.

**What the reader must understand without reading a word:** a story kept to
a group sits inside a closed boundary; some people are inside it and the
others — still family, still nearby, not villains — simply aren't. Nobody
should look excluded *from the family*, only from this one story.

This is the hardest image in the pack and the one worth iterating on most.
The failure mode is making the outside figures look sad or shut out.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Scene: five cosmonauts in soft ribbed spacesuits stand on pale regolith.
Every visor is completely dark and opaque — a solid reflective panel with
no face, no eyes and nothing visible behind it.
Four of them stand together inside a glowing circular ring marked on the
ground — a soft cyan light-ring, like a landing circle, clearly closed and
clearly enclosing them. They are lit warmly by it. The fifth cosmonaut
stands outside the ring, close by, relaxed and unbothered, facing the same
direction as the others and doing something of their own — looking up at
the sky. The one outside must read as content and included in the group of
people, just not standing in this particular circle.

Background: deep blue-black, hex #0d1424, with a large ringed planet low on
the horizon. Palette: instrument cyan #5cc8f5 for the ring's light, pale
starlight #dce6f5 for the suits, one rust orange #c8622f stripe on each
suit so all five clearly belong to the same crew.

Wide landscape composition, roughly 5:4. The ring must be unmistakably a
closed boundary at 250 pixels wide.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals. No faces. Nobody sad, nobody turned
away, no barrier or wall — a line of light on the ground, not a fence.
```

---

## 5. Sealed until — `sealed-letter.jpg`

**What the reader must understand:** this is written but deliberately not
open yet, and opening early would spoil something. A held breath, not a
lock.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a small sealed capsule or canister floating in zero gravity, its
seam marked by a single band of soft cyan light, with a simple wax-like
seal disc pressed onto it bearing an abstract ring-and-dot mark. It is
intact and calm, drifting slowly. A faint countdown of three small dots
trails behind it suggesting time passing.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5, rust orange #c8622f for the seal disc.

Portrait-ish composition, roughly 4:5, the capsule centred.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals, no dates. No padlock, no chain, no
keyhole — this is a seal to be broken in its own time, not security.
```

---

## 6. Firsts — `firsts-boots.jpg`

**What the reader must understand:** a register of things done for the very
first time.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a single line of small bootprints pressed into pale regolith,
leading away from the viewer toward the horizon, with the very first print
in the line noticeably crisper and lit by a soft cyan glow. Beside the
first print, a tiny pair of child-sized moon boots stands, toes pointing
forward. A ringed planet sits low on the horizon.

Background: deep blue-black sky, hex #0d1424, meeting pale grey regolith.
Palette: instrument cyan #5cc8f5, pale starlight #dce6f5, one rust orange
#c8622f on the boots.

Wide landscape composition, roughly 3:2, with the trail leading the eye.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals. No flag, no planted banner — this is
about a first step, not a conquest.
```

---

## 7. Growing up — `growth-doorpost.jpg`

**What the reader must understand:** the same person, measured again and
again as they get taller, over years.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: the inside of a ship's bulkhead with a vertical row of small
horizontal marks scratched into it at increasing heights, the way a
doorframe records a child's height. A small cosmonaut in a soft suit stands
with their back against the bulkhead at the topmost mark, standing very
straight. Each mark is a simple tick; the highest ones glow faintly cyan.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5, rust orange #c8622f on the suit.

Upright portrait composition, roughly 3:4, so the height of the marks is
the subject.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals, no dates beside the marks — ticks only.
No face.
```

---

## 8. The almanac — `almanac-book.jpg`

**What the reader must understand:** a calendar of the family's own
recurring dates — birthdays, anniversaries — that comes round each year.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: an orrery — a mechanical model of a star with several planets on
concentric brass-like rings — sitting on a shelf, with one small planet
marked by a soft cyan glow as it passes a fixed pointer. The rings clearly
describe repeating orbits. Warm and hand-made rather than clinical.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5, rust orange #c8622f on the orrery's arms.

Square-ish composition, roughly 1:1.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals, no dials with numbers. No zodiac
symbols.
```

---

## 9. History — `history-pages.jpg`

**What the reader must understand:** earlier versions of the same thing are
kept, and you can go back to one.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a stack of identical flat data plates or slides floating in a
gentle arc in zero gravity, each one slightly rotated from the next so the
stack reads as a sequence going back in time. The nearest plate is lit
cyan; the ones further back fade. Their surfaces carry faint wavy ink
strokes suggesting handwriting, never actual words.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5.

Landscape composition, roughly 6:5.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals — wavy strokes only, and they must not
resolve into letters at any zoom.
```

---

## 10. Accounts — `accounts-keys.jpg`

**What the reader must understand:** each person has their own way in, and
they are not interchangeable.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: four differently-shaped access tokens or keycards hanging side by
side on individual hooks, each with a distinct silhouette and a small
coloured band, one of them glowing faintly cyan as if just used. Clearly
four different keys for four different people, not a set.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5, one rust orange #c8622f band.

Wide landscape composition, roughly 3:2.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals, no barcodes that resolve into
characters.
```

---

## 11. Invitation — `invite-card.jpg`

**What the reader must understand:** someone is being asked in, personally,
and the invitation is single-use.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a single small docking beacon on a post, projecting one narrow
cone of soft cyan light toward the viewer, with a lone cosmonaut in the
middle distance drifting gently along that beam toward it. Welcoming and
specific — one light, one traveller.

Background: deep blue-black, hex #0d1424, a ringed planet behind.
Palette: instrument cyan #5cc8f5, pale starlight #dce6f5, rust orange
#c8622f on the suit.

Landscape composition, roughly 5:4.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals. No crowd, no queue.
```

---

## 12. Write link — `write-link-pass.jpg`

**What the reader must understand:** a one-off pass that lets a visitor add
one thing, then stops working.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a single-use airlock pass — a thin token being fed into a slot
beside a small hatch, with the hatch showing one soft cyan light. Beside
the slot, a small chute where a spent token has already dropped, making it
clear the token is consumed by use.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5, rust orange #c8622f on the hatch frame.

Landscape composition, roughly 5:4.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals.
```

---

## 13. Help — `help-lantern.jpg`

**What the reader must understand:** here is where things are explained.
Steady, patient light.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a small handheld work lamp hooked onto a rail, casting a steady
warm cone of pale cyan light downward onto an open, blank instrument panel
below. Calm and helpful, nothing urgent, nothing flashing.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5.

Upright portrait composition, roughly 5:6.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals, no dials with markings — the panel is
blank on purpose.
```

---

## 14. The book — `book-frame.jpg`

**What the reader must understand:** all of it, together, as one object you
could hold.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a bound logbook floating in zero gravity, closed, with a simple
ring-and-planet emblem embossed on its cover and a cyan light seam along
its edge. It reads as complete, valuable and physical — an object with
weight, despite floating.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5, rust orange #c8622f on the spine.

Portrait composition, roughly 4:5.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals, no title on the cover — the emblem
carries it.
```

---

## 15. Instants — `instant-camera.jpg`

**What the reader must understand:** a photo and one line, captured in
seconds.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a chunky hand-held survey camera in a gloved cosmonaut's hand,
just having taken a shot, with a single square image plate emerging from
its base. The plate is blank pale cyan. Quick and casual — the camera is
held one-handed, slightly tilted.

Background: deep blue-black, hex #0d1424. Palette: instrument cyan
#5cc8f5, pale starlight #dce6f5, rust orange #c8622f on the camera body.

Landscape composition, roughly 5:4.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals on the camera's controls.
```

---

## 16. The tree — `tree-sapling.jpg`

**What the reader must understand:** a family, drawn as connections between
people, still growing.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a small green seedling growing inside a glass hydroponics dome on
a bare moon surface, with a few slender cyan support struts branching from
its base in a way that echoes a family tree. Life, deliberately kept, in a
place that has none.

Background: deep blue-black, hex #0d1424, a ringed planet behind the dome.
Palette: instrument cyan #5cc8f5, pale starlight #dce6f5, and — the one
place this pack allows green — a soft leaf green on the seedling.

Portrait composition, roughly 4:5.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals.
```

---

## 17. Not found — `tumbleweed.jpg`

**What the reader must understand:** there is nothing at this address, and
that's mildly funny rather than alarming.

```
A retro-futurist illustration in the style of a 1970s space encyclopaedia
plate: flat colour, confident hand-drawn linework, no photographic
rendering.

Subject: a single small satellite drifting slowly and aimlessly through
empty space, one panel askew, clearly lost rather than broken. Gently
comic — a shrug, not an alarm.

Background: deep blue-black, hex #0d1424, empty apart from a few sparse
stars and a very distant ringed planet.
Palette: instrument cyan #5cc8f5, pale starlight #dce6f5.

Wide landscape composition, roughly 2:1, with a lot of empty space around
the satellite — the emptiness is the joke.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals. Nothing on fire, nothing exploding, no
warning symbols.
```

---

## Icons — a different set of rules

These follow **F22**, not the plate style above: transparent PNG, no
background, bold flat shapes that survive being drawn at 20 pixels. The
pack's signature shape is the **ring** — a tilted ellipse around a body —
because it is the one silhouette that stays legible that small.

These are drawn by `scripts/draw_orbit_icons.py` rather than generated —
see the status note at the top of this file for why. Run it to redraw the
set after changing a colour; pass a filename to redo just one.

`scripts/process_orbit_icons.py` remains for a *generated* icon: it keys a
mid-grey background out, trims to content, pads by 2% and downscales to
160×160. The drawing script frames its output the same way, so drawn and
generated icons sit in the same box.

### The rule the first batch taught: every icon needs a dark outline

An icon has to read on **both** of orbit's schemes, and no single colour in
the pack's palette does. Measured against the raised surface each one sits
on:

| | on the night side | on the day side |
|---|---|---|
| pale starlight `#dce6f5` | 14.5:1 | **1.11:1** |
| instrument cyan `#5cc8f5` | 9.6:1 | **1.36:1** |
| dark navy `#17253f` | **1.19:1** | 10.9:1 |
| rust `#c8622f` | 4.6:1 | 2.9:1 |

A pale or cyan icon is invisible in daylight; a dark one is invisible at
night. This is exactly why the ranch's icons work on both cream and near-
black: they are **light shapes inside a dark outline**, so whichever scheme
you are in, one half of the icon carries it.

So: **every shape carries a dark navy `#17253f` outline, thick enough to
survive 20 pixels**, with cyan and pale starlight as the fills inside it.
The prompt below says so; do not drop it, and check a generation against
the day side before accepting it.

Drawing them taught a corollary the prompts do not state, because a
generator would never hit it: **a line cannot simply *be* the keyline.** A
navy stroke is invisible at night for the same reason a navy fill is, so
every stroke in the set is drawn twice — a fat navy keyline with a lighter
core on top. Filled shapes need only the outline; strokes need both.

Two more things drawing them taught, both about composition rather than
colour, and both cost several attempts:

- **Three heads inside an oval is a face.** Arranged in a triangle it is
  unmistakably one; in a row it becomes a pod. `icon-group` only worked
  when it was inverted — the enclosing shape filled dark, the three
  figures light silhouettes inside it, no per-figure outline at all. That
  is also what the catalogue asks for in words.
- **A dark oval centred in a pale disc is an eye.** `icon-new-person`'s
  visor had to become a band across the helmet before it read as a helmet.

The other thing the first batch taught: *the subject line has to name a
shape, not a concept*. "A ringed planet inside a downward chevron" came
back as a shield with ears — the generator drew the container, not the
direction. Where a subject is abstract, describe the silhouette you want.

Committed sizes and filenames must match the ranch pack exactly:
`icon-new-story.png`, `icon-instant.png`, `icon-save.png`, `icon-draft.png`,
`icon-archive.png`, `icon-seal.png`, `icon-source.png`, `icon-record.png`,
`icon-print.png`, `icon-import.png`, `icon-tree.png`, `icon-new-person.png`,
`icon-group.png`.

A single prompt covers the set; change only the **subject** line:

```
A single bold, flat vector-style icon, centred, drawn as one confident
shape — the visual weight of a mission patch symbol.

Every shape is outlined in dark navy #17253f, with a thick, even stroke
roughly one tenth of the icon's width. Inside those outlines the fills are
instrument cyan #5cc8f5 and pale starlight #dce6f5, with one rust orange
#c8622f accent allowed. The outline is not optional: this icon has to stay
legible on a near-black background and on a pale blue one, and only the
dark outline works on both.

Plain flat mid-grey background, no shadow, no gradient, no glow, no
rounded-square badge or container behind the icon.

Subject: <SUBJECT>

The shape must still be recognisable when the whole image is 20 pixels
wide: one large silhouette, generous negative space, no stroke thinner
than a tenth of the icon's width, no small elements, no more than three
distinct parts.

No sparkle, star, diamond or logo in any corner. No border, frame or
paper mat around the picture — the artwork runs edge to edge.
No text, no lettering, no numerals. No 3D rendering, no perspective, no
photographic style.
```

Subjects, one per file:

| File | `<SUBJECT>` |
|---|---|
| `icon-new-story.png` | a ringed planet with a stylus arcing over it like an orbit |
| `icon-instant.png` | a chunky survey camera seen head-on, one round lens |
| `icon-save.png` | a thick downward-pointing arrow, its shaft crossed by a tilted planet's ring seen edge-on, the arrowhead resting on a short horizontal bar |
| `icon-draft.png` | a ringed planet whose body is drawn as four thick dashes with wide gaps between them, the ring solid and unbroken |
| `icon-archive.png` | a wide storage crate seen square-on, wider than it is tall, with a separate lid bar across the top and one rust band across the middle |
| `icon-seal.png` | a capsule with a single wax seal disc on its seam |
| `icon-source.png` | a small antenna dish pointing up and to the right |
| `icon-record.png` | a round microphone grille with two sound arcs |
| `icon-print.png` | a flat plate emerging from a slot |
| `icon-import.png` | an arrow entering an open hatch |
| `icon-tree.png` | three small moons linked by two straight struts |
| `icon-new-person.png` | a helmet silhouette with a small plus beside it |
| `icon-group.png` | three helmet silhouettes inside one tilted ring |

---

## The two decorations that need no file

`--flourish-image` (the divider between stories) and `--brand-mark` (the
star on the tree's root card) are drawn in CSS in `theme.css`, as a fading
horizon line and a small ringed star. They need no artwork at all. If you
ever want drawn versions, point those two variables at `img/…` files —
that's the seam, and the comment in `theme.css` marks it.
