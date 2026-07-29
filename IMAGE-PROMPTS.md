# Image prompts

Prompts for the illustrations this app is still missing, written so a
generated image lands in the same world as the ones already committed
(FEATURES.md F17 for the paper-card illustrations, F22 for the flat button
icons). Generate externally, process locally, commit the result under
`app/static/themes/ranch/img/` — the app never fetches an image at runtime.

**Status:** every asset below has been generated, processed and wired in.
The prompts are kept for regenerating one or matching a new asset to the
set. See F42 in FEATURES.md for how the shipped files were processed, and
F17's and F22's tables for what went where.

**Every prompt below is complete.** Copy one whole fenced block into
Gemini as-is; the style, the paper, the size constraint and the negatives
are already inside each one. Nothing needs assembling, and nothing needs a
"see above".

Each entry says, first, **what a reader has to understand from the picture
alone**. That's the test the image has to pass: someone who reads none of
the words on the page should still come away with the right idea.

## How to run these through Gemini

1. **One asset per conversation.** Paste the block, generate, then iterate
   in the same thread ("keep everything, move the two outside figures
   further from the rope") rather than re-pasting a modified prompt — the
   thread holds the style steady.
2. **Anchor the style with a real file.** Upload
   `app/static/themes/ranch/img/empty-chest.jpg` or `tree-sapling.jpg` with the first
   message and add: *"Match the linework, colour palette and paper of this
   image exactly."* This is the single biggest quality lever — the words
   below describe the house style, but an actual sample pins it.
3. **Generate three or four** of each and pick by the squint test (step 4
   of processing, below). Cheap to do, and these compositions either read
   at thumbnail size or they don't.
4. **Aspect ratio is stated in words** inside each prompt (Gemini takes no
   `--ar` flag). If a generation comes back square when the prompt asked
   for wide, say *"same image, wider composition, more empty paper left and
   right"* rather than starting over.
5. If lettering appears anyway — it sometimes does on books, signs and
   calendars — reply *"remove all text and lettering; leave those surfaces
   blank or with wavy ink strokes suggesting handwriting"*. Do not accept
   an image with legible words in it (see below).

**Why "no lettering" is a hard rule, not a preference:** the interface is
bilingual (F38). A word baked into an illustration can't be translated, and
it will sit there in English on a French page forever.

**Why faces stay generic:** these illustrations sit next to photographs of
a real family. Figures should read as *people* — small, gestural, backs and
three-quarter views — not as portraits of anyone in particular.

## Processing what comes back

1. Trim to the drawn content, keep a little paper margin.
2. Keep the cream background **baked into the JPEG** — the `.illo` class
   mounts it as a cream paper card in every theme, including dark, where
   it reads as a photo tucked into an album. A transparent PNG would break
   that.
3. Downscale to roughly 2× the display size (~700-760px on the long
   edge), save as JPEG quality 82, and keep each page under ~150 KB of
   added illustration weight. `/help` carries two cards, which is the
   page that sets that budget.
4. **The squint test**: view it at 250 px wide. If the idea disappears, the
   composition is too busy — ask for fewer figures and larger shapes, not
   more detail.
5. Look at it in **both themes** at a 390 px viewport before committing.
6. Add the file to the table in FEATURES.md F17 so the inventory stays
   true.

---

## 1. Groups — the one that has to teach scoping

**File:** `group-circle.jpg` · **committed at** 760×612

**What the reader must understand without reading a word:** a story kept to
a group sits inside a closed circle; some people are in it and the others —
still family, still nearby, not villains — simply aren't. Nobody should
need "audience" explained to them after seeing this.

```
Draw a closed lasso rope lying on the ground, forming one unbroken ring
around a small campfire at dusk. Inside the ring, four people sit close
together on logs, warmly lit by the fire, one of them mid-story with a hand
raised; an open book rests on a log by the flames. Outside the ring,
standing a few steps back on plain empty ground in cool blue-grey shade,
two more people stand with their backs half-turned, one glancing over a
shoulder — near, unbothered, simply not inside. The rope is the boundary
and must read as one: everything inside it is warm and lit, everything
outside is cool and unlit, with clear empty ground between the rope and the
two outside figures.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Wide landscape composition, roughly 5:4, the figures small within it, with
quiet empty paper around the scene.

The figures are small and gestural — backs, three-quarter views and
silhouettes, never portraits of identifiable people.

It must stay legible at 250 pixels wide: large simple shapes, few figures,
no fine detail that vanishes when shrunk.

Do not include: any text, lettering, numbers, signage, labels or watermark;
walls, locks, chains, guards, or a rope tied around a person; anyone
looking excluded, sad or shut out; modern objects such as phones, screens
or laptops; photorealism or 3D rendering; heavy black ink, neon or
saturated colour; a white, grey or transparent background; any frame,
border or vignette.
```

The feeling is *a smaller circle of the same family*, not a prison and not
a rejection. If the rope ring doesn't come out clean after a few tries, the
same idea in three other compositions — swap the first paragraph, keep
everything after it:

```
Draw a low split-rail corral fence enclosing a lantern-lit table with four
people seated around it, leaning in together, warmly lit. Outside the
fence, on plain empty ground in cool blue-grey shade, two people stand a
few steps away, backs half-turned. The gate is closed but not locked. The
fence is the boundary and must read as one: warm and lit inside, cool and
unlit outside.
```

```
Draw three covered wagons drawn into a closed circle around a small
campfire at dusk, with four people sitting inside the circle, warmly lit.
Outside the wagons, on open prairie in cool blue-grey shade, two people
stand a few steps away, backs half-turned. The ring of wagons is the
boundary and must read as one: warm and lit inside, cool and unlit outside.
```

```
Draw an oil lantern hanging from a wooden post at dusk, casting one clear
round pool of warm light on the ground. Four people sit inside the pool of
light, close together, one mid-story with a hand raised. Just beyond the
edge of the light, in cool blue dusk, two people stand with their backs
half-turned. The edge of the lit circle is the boundary and must read as
one.
```

**Where it goes** (wired): `groups.html` under the `<h1>`, and `help.html`
at the top of the "Who can read a story" section. The markup every page
illustration uses:

```html
<img class="illo illo--page" src="{{ theme_img('group-circle.jpg') }}"
     alt="" loading="lazy" decoding="async" width="760" height="612">
```

`.illo` does the paper-card treatment, `.illo--page` the sizing
(`.illo--page-tall` for the portrait ones). **Keep the `width`/`height`
attributes, and never size an illustration with `max-width` alone** — the
attributes pin the height while the width shrinks and the picture renders
squashed, which is why `.illo--page` also sets `width: 100%; height:
auto`.

---

## 1b. The matching button icon (different style — F22, not F17)

**File:** `icon-group.png` · **160×160, transparent** · **displayed** 20 px

The timeline's *kept to a group* marker and the editor's audience row want
an icon, and F17's fine linework turns to mud at 24 px. This is the bold
flat companion style instead:

```
Draw a bold flat vector icon: a rope ring enclosing three small round
figures, with one figure standing clearly outside the ring.

Style: thick uniform dark-brown outlines of even weight, two or three flat
fill colours only (cream, ochre, dusty blue), no shading, no
cross-hatching, no gradients, no texture. Simple geometric shapes. The icon
is centered on a plain white background with a generous even margin around
it.

It must be instantly legible at 24 pixels: chunky shapes, wide gaps between
elements, no thin lines and no small detail.

Do not include: any text, lettering or numbers; drop shadows; photorealism;
3D rendering; gradients; thin or varying line weights; a coloured or
transparent background.
```

Process it like the rest of the F22 set — with one caveat this asset
taught: if the fill inside the ring comes back near the paper colour, a
colour-distance key punches a hole through the middle of the icon. Flood
fill in from the four corners instead, close the mask to swallow the
paper's flecks, then crop to content, repad square (2% margin here — 8%
left the ring too small) and downscale to 160×160.

**Where it goes** (wired): next to the audience picker's "Who can see this"
label, via `.editor__audience-label`. Not the timeline's *kept to a group*
pill — at that size it degrades to a ring and a smudge, and the words
already say it.

---

## 2. Write links — one page, not a key to the house

**File:** `write-link-pass.jpg` · **committed at** 700×600

**What the reader must understand:** the person you hand this to can add
*one* page and nothing else. They don't get the book.

```
Draw a single loose sheet of paper and a pencil being passed by one hand
over a wooden fence rail to a visitor standing on the far side, seen from
the side. On the near side of the fence, a thick leather-bound book rests
closed on a small table, its clasp shut, plainly staying where it is. Only
the one sheet crosses the fence. The mood is warm, neighbourly and
unhurried — a favour, not a transaction.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Landscape composition, roughly 7:6, centered, with quiet empty paper around
the scene.

The figures are small and gestural — hands, backs and three-quarter views,
never portraits of identifiable people.

It must stay legible at 250 pixels wide: large simple shapes, no fine
detail that vanishes when shrunk.

Do not include: any text, lettering, numbers, signage, labels or watermark;
readable handwriting on the sheet (leave it blank); modern objects such as
phones, screens or laptops; photorealism or 3D rendering; heavy black ink,
neon or saturated colour; a white, grey or transparent background; any
frame, border or vignette.
```

**Where it goes** (wired): `account_write_links.html` under the `<h1>`,
and `delegate_write.html`, the page the guest actually lands on.

---

## 3. Invitations — how someone new gets in

**File:** `invite-card.jpg` · **committed at** 700×564

**What the reader must understand:** getting into this book happens by
someone handing you a way in. It isn't a public door, and it isn't a form
you fill in for a company.

```
Draw an envelope closed with a red wax seal, resting on a rough plank
table, with a small brass key lying half-tucked beneath its flap. Behind
the table, a rope gate stands slightly ajar onto a lit path leading away.
Warm evening light. The mood is personal and welcoming — an invitation from
someone you know.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Landscape composition, roughly 5:4, centered, with quiet empty paper around
the subject.

It must stay legible at 250 pixels wide: large simple shapes, no fine
detail that vanishes when shrunk.

Do not include: any text, lettering, numbers, addresses, stamps, postmarks
or watermark — the envelope is blank; nothing institutional or corporate;
padlocks or chains; modern objects such as phones, screens or laptops;
photorealism or 3D rendering; heavy black ink, neon or saturated colour; a
white, grey or transparent background; any frame, border or vignette.
```

**Where it goes** (wired): `admin_invite.html`, `accept_invite.html`,
`request_account.html`. The three guest-facing form pages drop their card
under 700 px of viewport *height* (`.page-login .illo--page`), the way
`/new-instant` hides its camera (F17), so the form stays above the fold.

---

## 4. Firsts — a register of first times

**File:** `firsts-boots.jpg` · **committed at** 760×519

**What the reader must understand:** this page collects the *first* time
something happened, in the order it happened — a trail, not a list.

```
Draw a trail of small bare child's footprints crossing soft dust from the
lower left towards the upper right, the prints growing very slightly larger
along the way. The first print, at the lower left, is deep and freshly
pressed; a pair of tiny worn leather boots sits beside it. A length of rope
lies loosely along the edge of the trail. Low wide composition with a lot
of quiet paper above the trail.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Wide landscape composition, roughly 7:5.

It must stay legible at 250 pixels wide: large simple shapes, clearly
separated prints, no fine detail that vanishes when shrunk.

Do not include: any text, lettering, numbers, signage or watermark; any
people or body parts — only the prints and the boots; modern objects such
as phones, screens or laptops; photorealism or 3D rendering; heavy black
ink, neon or saturated colour; a white, grey or transparent background; any
frame, border or vignette.
```

**Where it goes** (wired): `firsts.html`, under the flourish — including
on the empty state, where it does the most work.

---

## 5. Almanac — the family's year

**File:** `almanac-book.jpg` · **committed at** 700×700

**What the reader must understand:** birthdays, weddings and deaths, kept
month by month like a farmer's almanac — a record book, not a calendar app.

```
Draw a worn almanac lying open and flat on a rough plank table, seen from
slightly above. Both visible pages are ruled into a grid of small empty
squares — completely blank squares, no numbers and no words — with three or
four squares ringed in ink and one holding a small pressed flower. A
feather quill and a stub of candle rest beside the book, and a sprig of
wheat is tucked into the gutter between the pages. Warm, well-used,
domestic.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Composition roughly 5:5, centered, with quiet empty paper around the book.

It must stay legible at 250 pixels wide: a bold clear grid, few marked
squares, no fine detail that vanishes when shrunk.

Do not include: any text, lettering, numbers, dates, month names, headings
or watermark — every square and every page is blank; modern objects such as
phones, screens or laptops; photorealism or 3D rendering; heavy black ink,
neon or saturated colour; a white, grey or transparent background; any
frame, border or vignette.
```

**Where it goes** (wired): `almanac.html`, under the flourish.

---

## 6. Growing up — one photo per birthday

**File:** `growth-doorpost.jpg` · **committed at** 567×760

**What the reader must understand:** the same child, measured again and
again, rising up the page year by year.

```
Draw a wooden doorframe seen straight on, with a ladder of short horizontal
pencil height-marks climbing its post, each mark a little higher than the
one below. Beside each mark, a small blank photograph is pinned to the
wood, curling slightly at the corners — the photographs are blank cream
rectangles with no image and no writing on them. Tall narrow composition,
the marks rising from low to high.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Tall portrait composition, roughly 3:4, with quiet empty paper either side.

It must stay legible at 250 pixels wide: five or six marks at most, clearly
separated, no fine detail that vanishes when shrunk.

Do not include: any text, lettering, numbers, dates or names beside the
marks — nothing written anywhere; any people; modern objects such as
phones, screens or laptops; photorealism or 3D rendering; heavy black ink,
neon or saturated colour; a white, grey or transparent background; any
frame, border or vignette.
```

**Where it goes** (wired): `growth.html`, under the flourish, with
`.illo--page-tall` so the year grid stays the point.

---

## 7. History — the previous version is still there

**File:** `history-pages.jpg` · **committed at** 720×598

**What the reader must understand:** saving doesn't destroy what was there
before; an older page can be pulled back out.

```
Draw a neat stack of handwritten pages on a plank table, each sheet offset
slightly from the one beneath so that all of their edges show as a fan of
layers. The top sheet is crisp and pale; the lower ones are softly foxed
and yellowed with age. One sheet from the middle of the stack is being
drawn halfway out, as if retrieved. A coil of rope rests on one corner as a
paperweight. The handwriting on the sheets is suggested only by rows of
wavy ink strokes — nothing readable.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Landscape composition, roughly 6:5, centered, with quiet empty paper
around the stack.

It must stay legible at 250 pixels wide: a clear layered edge, one sheet
obviously pulled out, no fine detail that vanishes when shrunk.

Do not include: any text, lettering, numbers, dates or readable
handwriting; modern objects such as phones, screens or laptops;
photorealism or 3D rendering; heavy black ink, neon or saturated colour; a
white, grey or transparent background; any frame, border or vignette.
```

**Where it goes** (wired): `history.html`, under the `<h1>`.

---

## 8. Help — a lantern, not a manual

**File:** `help-lantern.jpg` · **committed at** 628×700

**What the reader must understand:** this page is a small friendly light,
not a manual you're required to read.

```
Draw an old oil lantern hanging lit from a wooden post, casting a warm pool
of light down onto a small field guide lying open on a tree stump beneath
it. The open pages carry only rows of wavy ink strokes and one tiny sketch
— nothing readable. Dusk beyond, drawn lightly with a low horizon. Calm,
quiet and inviting.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Slightly tall composition, roughly 9:10, centered, with quiet empty paper
around the subject.

It must stay legible at 250 pixels wide: the lantern and the pool of light
are the two shapes that must survive, no fine detail that vanishes when
shrunk.

Do not include: any text, lettering, numbers, signage or watermark; any
people; modern objects such as phones, screens or laptops; photorealism or
3D rendering; heavy black ink, neon or saturated colour; a white, grey or
transparent background; any frame, border or vignette.
```

**Where it goes** (wired): `help.html`, between the flourish `<hr>` and the
intro paragraph, with `.illo--page-tall illo--tilt-right` so it stays small
and leans the other way from the group card further down the page.

---

## 9. Accounts — everyone has their own key

**File:** `accounts-keys.jpg` · **committed at** 760×540

**What the reader must understand:** in accounts mode there is no single
shared password any more — each person has their own way in, and an admin
looks after the keyring.

```
Draw a row of five iron keys of clearly different shapes, each hanging from
its own nail on a wooden board, each carrying a small blank leather tag on
a string. One nail at the end of the row is empty. Warm workshop light,
with hatched shadows falling on the board behind the keys.

Style: hand-drawn ink engraving in the manner of a 19th-century frontier
storybook — fine pen linework with cross-hatched shading, tinted with a
light watercolor wash. Warm sepia, ochre and soft brown, with dusty
blue-grey used sparingly for depth. The whole drawing sits on aged cream
paper (#f9f2e1): the cream paper is the background edge to edge with a
faint mottled grain, and a soft hatched shadow falls beneath the subject.
Wide landscape composition, roughly 7:5, centered, with quiet empty paper
above and below.

It must stay legible at 250 pixels wide: five large distinct key
silhouettes, well separated, no fine detail that vanishes when shrunk.

Do not include: any text, lettering, numbers or names on the tags — the
tags are blank; padlocks, chains or anything that reads as a lock-out;
modern objects such as phones, screens or laptops; photorealism or 3D
rendering; heavy black ink, neon or saturated colour; a white, grey or
transparent background; any frame, border or vignette.
```

**Where it goes** (wired): `account_home.html`, under the `<h1>`. Not
`admin_accounts.html` after all — that page is a working list of accounts
and pending requests, and an illustration on it is noise on a surface
someone is trying to act on.

---

## Order worth doing them in

1. **`group-circle.jpg`** (and `icon-group.png` with it) — the only one
   where the picture carries a rule people can otherwise get wrong: who can
   read this?
2. **`write-link-pass.jpg`** and **`invite-card.jpg`** — the other two
   places where a reader is deciding what someone else will be able to see.
3. Everything else, which is decoration that happens to also orient — nice,
   not load-bearing.

Nothing here is wired into the templates yet: an `<img>` pointing at a file
that doesn't exist is a broken image on a real family's page. Drop a
generated JPEG into `app/static/themes/ranch/img/`, paste the two snippets from its
entry, check both themes at 390 px, and that asset is done.
