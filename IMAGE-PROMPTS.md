# Image prompts

Prompts for the illustrations this app is still missing, written so a
generated image lands in the same world as the ones already committed
(FEATURES.md F17 for the paper-card illustrations, F22 for the flat button
icons). Generate externally, process locally, commit the result under
`app/static/img/` — the app never fetches an image at runtime.

Each entry below says, first, **what a reader has to understand from the
picture alone**. That's the test the image has to pass: someone who reads
none of the words on the page should still come away with the right idea.
Everything else in the entry is in service of that.

---

## The house style (paste this in front of every prompt)

> Hand-drawn ink engraving in the style of a 19th-century frontier
> storybook: fine pen linework with cross-hatched shading, tinted with a
> light watercolor wash. Warm sepia, ochre and soft brown, with dusty
> blue-grey used sparingly for depth. Printed on aged cream paper
> (#f9f2e1) — the paper is the background, edge to edge, with a faint
> mottled grain. A single subject, centered, with plenty of quiet paper
> around it and a soft hatched shadow beneath. No frame, no border, no
> vignette.

And the negatives, every time:

> No text, no lettering, no numbers, no signage, no watermark. No modern
> objects (phones, screens, laptops). No photorealism, no 3D render, no
> heavy black, no neon or saturated colour. No white or grey background —
> the paper must stay cream to the edges.

**Why "no lettering" is a hard rule, not a preference:** the interface is
bilingual (F38). A word baked into an illustration is a word that can't be
translated, and it will sit there in English on a French page forever.

Two more constraints worth respecting while generating:

- **Faces stay generic.** These illustrations sit next to photographs of a
  real family; figures should read as *people*, small and gestural, not as
  portraits of anyone in particular. Backs, three-quarter views and
  silhouettes work better than faces.
- **It has to survive being small.** Every one of these renders at roughly
  200–300 px wide on a phone. Squint at the result at that size: if the
  idea disappears, the composition is too busy — ask for fewer figures and
  larger shapes rather than more detail.

## Processing what comes back

1. Trim to the drawn content, keep a little paper margin.
2. Keep the cream background **baked into the JPEG** — the `.illo` class
   mounts it as a cream paper card in every theme, including dark, where
   it reads as a photo tucked into an album. A transparent PNG would break
   that.
3. Downscale to roughly 2× the display size (the sizes below), save as
   JPEG quality ~85, and check the page stays under ~150 KB of added
   illustration weight.
4. Look at it in **both themes** and at a 390 px viewport before
   committing.
5. Add the file to the table in FEATURES.md F17 so the inventory stays
   true.

---

## 1. Groups — the one that has to teach scoping

**File:** `group-circle.jpg` · **target** ~760×620 · **displayed** ~15rem

**What the reader must understand without reading a word:** a story kept to
a group is inside a closed circle, some people are in it, and the others —
who are still family, still nearby, not villains — simply aren't. Nobody
should have to be told what "audience" means after seeing this.

> A closed lasso rope lying on the ground, forming an unbroken ring around
> a small campfire at dusk. Inside the ring, four people sit close together
> on logs, warmly lit by the fire, one of them mid-story with a hand
> raised; an open book rests by the flames. Outside the ring, standing a
> few steps back on plain empty ground in cool blue-grey shade, two more
> people stand with their backs half-turned, one glancing over a shoulder
> — near, unbothered, simply not inside. The rope reads clearly as the
> boundary: everything inside it is warm and lit, everything outside is
> cool and unlit. Wide composition, figures small.

Ask for three or four generations of this and pick by the squint test: at
thumbnail size you should still see *ring, warm inside, cool outside*.

**Variants, if the rope circle doesn't come out clean:**

- *Corral gate* — "a low split-rail corral fence enclosing a lantern-lit
  table with four seated figures; two figures stand outside the fence in
  cool shade, the gate closed but not locked."
- *Wagon circle* — "three covered wagons drawn into a closed circle around
  a fire with four small figures inside; two figures on the open prairie
  outside, in cooler light."
- *Lamplight* — "a hanging lantern casting a clear circle of warm light on
  the ground with four figures inside it; two figures just beyond the edge
  of the light, in blue dusk."

Avoid, in any variant: walls, locks, chains, guards, a rope *tied around a
person*, or anyone looking excluded or unhappy. The feeling is *a smaller
circle of the same family*, not a prison and not a rejection.

**Where it goes.** In `groups.html`, under the `<h1>`, above the hint
paragraph; and in `help.html`, at the top of the "Who can read a story"
section. Both:

```html
<img class="illo admin__illo" src="{{ url_for('static', filename='img/group-circle.jpg') }}"
     alt="" loading="lazy" decoding="async" width="760" height="620">
```

```css
.admin__illo,
.help__illo {
  max-width: 15rem;
  margin: 0 auto 1.25rem;
}
```

(The `.illo` class does the paper-card treatment; the page class only sets
the size and centering. Same pattern as `login__illo` / `tree__illo`.)

**Companion button icon.** The timeline's *kept to a group* marker and the
editor's audience row want a 24 px icon, which is the F22 flat style, not
this one — a different prompt entirely:

> Bold flat vector icon, thick uniform dark-brown outline, two or three
> flat fill colours (cream, ochre, dusty blue), no shading, no
> cross-hatching, no gradient, no text. A simple rope ring enclosing three
> small round figures; one figure stands clearly outside the ring. Centered
> on a plain white background, generous margin, legible at 24 px.

Save as `icon-group.png`, background keyed to transparent and repadded to
160×160 like the rest of the F22 set.

---

## 2. Write links — one page, not a key to the house

**File:** `write-link-pass.jpg` · **target** ~700×620 · **displayed** ~13rem

**What the reader must understand:** the person you hand this to can add
*one* page and nothing else. They don't get the book.

> A single loose sheet of paper and a pencil being passed over a wooden
> fence rail to a visitor standing on the far side, drawn from the side.
> On the near side of the fence, a thick closed leather-bound book rests on
> a table, clasped shut and plainly staying where it is. Only the one sheet
> crosses the fence. Warm, neighbourly, unhurried.

**Where it goes:** `account_write_links.html` (under the `<h1>`) and
`delegate_write.html` (the page the guest actually lands on), max-width
13rem.

---

## 3. Invitations — how someone new gets in

**File:** `invite-card.jpg` · **target** ~700×560 · **displayed** ~13rem

**What the reader must understand:** getting into this book happens by
someone handing you a way in — it isn't a public door and it isn't a form
you fill in for a company.

> An envelope closed with a red wax seal, resting on a plank table, with a
> small brass key lying half-tucked beneath its flap. Beside it, a rope
> gate stands slightly ajar onto a lit path. Warm evening light, nothing
> institutional.

**Where it goes:** `admin_invite.html`, `accept_invite.html`,
`request_account.html`, max-width 12rem. On `request_account.html` keep it
above the form and hide it under 700 px of viewport *height* the way
`/new-instant` hides its camera (F17), so the form stays above the fold.

---

## 4. Firsts — a register of first times

**File:** `firsts-boots.jpg` · **target** ~760×540 · **displayed** ~14rem

**What the reader must understand:** this page collects the *first* time
something happened, in the order it happened — a trail, not a list.

> A trail of small bare child's footprints crossing soft dust from the
> lower left to the upper right, growing slightly larger along the way. The
> first print is deep and fresh; a pair of tiny worn boots sits beside it.
> A rope loops loosely along the edge of the trail. Low, wide composition,
> lots of quiet paper above.

**Where it goes:** `firsts.html`, under the `<h1>`, max-width 14rem —
including on the empty state, where it does the most work.

---

## 5. Almanac — the family's year

**File:** `almanac-book.jpg` · **target** ~700×680 · **displayed** ~13rem

**What the reader must understand:** birthdays, weddings and deaths, kept
month by month like a farmer's almanac — a record book, not a calendar app.

> A worn open almanac lying flat on a plank table, its two pages ruled into
> a month grid of small empty squares — no numbers, no words — with a few
> squares ringed in ink and one marked with a small pressed flower. A
> feather quill and a candle stub rest beside it. Seasonal sprigs (wheat,
> holly) tucked into the gutter of the book.

**Where it goes:** `almanac.html`, under the `<h1>`, max-width 13rem.

---

## 6. Growing up — one photo per birthday

**File:** `growth-doorpost.jpg` · **target** ~560×760 · **displayed** ~11rem

**What the reader must understand:** the same child, measured again and
again, rising up the page year by year.

> A wooden doorframe seen straight on, with a ladder of short pencil
> height-marks climbing it, each mark a little higher than the last. A
> small blank photograph is tucked beside each mark, curling slightly, held
> by a pin. Tall narrow composition. No writing beside the marks.

**Where it goes:** `growth.html`, under the `<h1>`, max-width 11rem
(portrait — keep it small so the year grid stays the point).

---

## 7. History — the previous version is still there

**File:** `history-pages.jpg` · **target** ~720×600 · **displayed** ~12rem

**What the reader must understand:** saving doesn't destroy what was there
before; an older page can be pulled back out.

> A neat stack of handwritten pages on a table, each sheet offset slightly
> from the one beneath so all their edges show, the top sheet crisp and the
> lower ones softly foxed with age. One sheet from the middle of the stack
> is being drawn halfway out. A rope paperweight holds the stack. No
> readable writing — the handwriting is suggested by wavy ink strokes.

**Where it goes:** `history.html`, under the `<h1>`, max-width 12rem.

---

## 8. Help — a lantern, not a manual

**File:** `help-lantern.jpg` · **target** ~640×700 · **displayed** ~12rem

**What the reader must understand:** this page is a small friendly light,
not a manual you're required to read.

> An old oil lantern hanging from a wooden post, lit, casting a warm pool
> of light onto a small open field-guide lying on a stump beneath it. The
> guide's pages carry only wavy ink strokes and a tiny sketch, no readable
> words. Dusk beyond, drawn lightly. Calm and inviting.

**Where it goes:** `help.html`, between the flourish `<hr>` and the intro
paragraph, max-width 12rem, `.illo--tilt-right` so it leans the other way
from the group card further down the page.

---

## 9. Accounts — everyone has their own key

**File:** `accounts-keys.jpg` · **target** ~760×540 · **displayed** ~13rem

**What the reader must understand:** in accounts mode there isn't one
shared password any more — each person has their own way in, and an admin
looks after the keyring.

> A row of four or five iron keys of different shapes hanging from a wooden
> board on individual nails, each with a small blank leather tag on a
> string. One nail is empty. Warm workshop light, hatched shadows on the
> board behind.

**Where it goes:** `admin_accounts.html` and `account_home.html`, under the
`<h1>`, max-width 13rem.

---

## Order worth doing them in

1. **`group-circle.jpg`** — the only one where the picture carries a rule
   people can otherwise get wrong (who can read this?).
2. **`write-link-pass.jpg`** and **`invite-card.jpg`** — the other two
   places where a reader is deciding what someone else will be able to see.
3. Everything else, which is decoration that happens to also orient — nice,
   not load-bearing.

Nothing here is wired into the templates yet: an `<img>` pointing at a file
that doesn't exist is a broken image on a real family's page. Drop a
generated JPEG into `app/static/img/`, paste the two snippets from its
entry, check both themes at 390 px, and that asset is done.
