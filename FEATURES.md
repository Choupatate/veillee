## Index

Every feature shipped so far, in numeric order. **The file below is not**,
and will not be: features were written up as they landed, a few early
batches predate F-numbering being sequential, and the specs use `##` for
their own internal structure — F18 alone has `## Layer 1`, `## API`,
`## Tests` and `## Definition of done`. Sorting the top-level headings
would tear those specs apart and interleave their subsections with
unrelated features. This index is what makes the order not matter.

Use it to find which section covers something without scrolling, then
search for the exact `F<N>.` heading text to jump to it. Five of the older
features are `#` rather than `##`; searching the heading text finds them
either way.

`tests/test_features_index.py` fails if a feature lands here without a
line in this list, if a line here points at a section that is gone, or if
two features claim the same number — so this list can be trusted to be
complete rather than merely intended to be.

- **F0** — Groundwork: story visibility (draft/sealed/archived filtering
  used by F2/F4/F5/F6/F10)
- **F1** — Authors: two voices, one book (multiple narrators, shared
  timeline, still no accounts)
- **F2** — Reading order: previous/next story navigation
- **F3** — Age at each memory (the child's age label on each story)
- **F4** — Sealed letters ("open when you're 18")
- **F5** — "X years ago today" (on-this-day)
- **F6** — Drafts
- **F7** — Tap-to-zoom photos (lightbox)
- **F8** — One-tap backup (export zip)
- **F9** — Home-screen install (manifest, no service worker)
- **F10** — The book view (`/book`): read it all, print it all
- **F11** — HEIC/HEIF photo uploads (Android & iPhone originals)
- **F12** — La voix: voice memos on stories
- **F13** — Instants: photo + one line, fifteen seconds on a phone
- **F14** — Personnages: the cast of the book (people)
- **F15** — Au hasard: open a page at random
- **F16** — Graines d'histoires: writing prompts
- **F17** — Le style du ranch: hand-drawn visual identity
- **F18** — L'arbre: the family tree (plus several follow-up refinement
  rounds afterward: a nav/UI audit, a whole-codebase dedup pass, a
  fresh-eyes audit, and six "Everyone" layout rounds)
- **F19** — Family accounts, admin approval, delegated writing
- **F20** — Event tagging, story↔people linkage, and source citations
- **F21** — People picker: searchable scrolling list, ticked stays on top
- **F22** — Button icons: a bold/flat companion set to F17
- **F23** — Hover/press feedback across the interface
- **F24** — Hover feedback round 2, and a dead-CSS catch on `/tree`
- **F25** — Splitting `routes_pages.py`/`routes_api.py` by resource
- **F26** — CSRF protection
- **F27** — Life dates: birthdays, deaths, and unions
- **F28** — Firsts: a chronological register of milestones
- **F29** — Growing up: the photo nearest each birthday
- **F30** — A gentle nudge after a quiet spell
- **F31** — Year chapters in the book view
- **F32** — MCP server: an AI-assisted authoring surface
- **F33** — Help: an in-app, plain-language guide for the family
- **F34** — Taking a photo, not just adding one (in-app camera)
- **F35** — Photos that look right everywhere (editor preview, stacked
  figures, no overflow)
- **F36** — Hardening for the open internet (login lockout, CSP and
  security headers, cache privacy, the auth-perimeter test)
- **F37** — Every error is a real page (no more bare 980px Werkzeug
  pages on a phone)
- **F38** — The interface in French, with a flag picker each reader sets
  for themselves
- **F39** — Invitations and open requests (admin-issued invite links, an
  optional-code request form, duplicate-account hints)
- **F40** — Groups: scoping a story to fewer people than the whole family
  (the audience rule and every surface enforcing it, plus the editor
  picker and the "kept to a group" markers)
- **F41** — Groups anyone can make: creating a group stops being an admin
  errand, a group is changed by the people in it, and two groups can't
  quietly cover exactly the same people
- **F42** — Help as a glossary: the in-app guide restructured into one
  term per line (and finally covering groups), plus `IMAGE-PROMPTS.md`,
  the prompt catalogue for the illustrations still missing
- **F43** — What a backup may carry: an export stops handing every family
  member the household's password hashes, and a restore stops colliding
  on the cast (or importing someone else's logins)
- **F44** — Writing in the book's own hand, and firelight: the editor
  re-dressed in the theme variables instead of Toast UI's white box, plus
  a slow warm wash over every page with a flame switch to turn it off
- **F45** — A toggle that looks off when it is off: Draft and Archive (and
  every other pressed chip) stopped being imitable by a plain hover
- **F46** — Theme packs: the art direction became a folder, so a second one
  (*orbit*, a book kept off Earth, under a starfield) could ship its
  palette on day one and its pictures one at a time
- **F47** — A recording that survives a locked screen: the phone is asked to
  stay awake while you talk, anything that interrupts a recording anyway
  ends it on purpose and keeps the audio, and a level meter makes a
  microphone that has quietly died visible while you are still talking
- **F48** — Picking the art direction from the nav: the theme pack stopped
  being a restart away, without becoming something one reader can change
  for the whole family
- **F49** — Everything about how the book looks behind one button: a tap
  still cycles light and dark, a press-and-hold opens the rest
- **F50** — Making a theme from inside the book: describe a world, get a
  prompt for each of its thirty-five pictures, and bring them back one at
  a time
- **F51** — Setting the book up from inside it: four questions on a fresh
  install, a Settings page forever after, and nothing asked of a book that
  already exists
- **F52** — Seeing the colours before saving them: the theme editor's live
  preview, held to the server's own palette maths by a cross-language test
- **Housekeeping** — the `pages` blueprint and the shared view helpers
  leave `routes_pages.py` for `views.py`; one `jsonstore.write_json`
  replaces seven hand-rolled atomic writes
- **Housekeeping 2** — `write_backup` and `import_backup` move in together
  as `backup.py`, so the two ends of the backup contract can finally be
  tested as a pair
- **Housekeeping 3** — the pure date maths leaves `storage.py` for
  `timeline.py`, and the Feb 29 rule that three call sites each wrote out
  becomes one `dates.same_day_of_year`
- **Housekeeping 4** — `crop-logic.js` and `draft-logic.js` come out of
  `editor.js`; the cropper's preview and saved JPEG become one calculation,
  and crash recovery stops discarding drafts it should have offered back
- **Housekeeping 5** — this index becomes a tested promise rather than an
  intention, and the plan to sort the file is abandoned with reasons
- **F53** — The licences, where a reader can actually see them: `/licences`
  reproduces the vendored bundles' notices from the files on disk, and the
  README is reframed around Veillée
- **Housekeeping 6** — Toast UI gets the `LICENSE` it never had, and a test
  that catches the next vendored file served without a copyright notice
- **F54** — The name, in both languages: the app is *Veillée* in English
  too, on both senses of the word — the fire the family gathers at, and the
  watch someone keeps — and the login screen finally says so

# Feature spec — F1: Authors ("two voices, one book")

Follow-up feature to be implemented **after** the fixes in `REVIEW.md`. Same
ground rules as `PLAN.md`: all decisions are made here — implement, don't
redesign. No new dependencies. Everything stays plain markdown on disk.

## What it is

Multiple family members (e.g. Papa and Maman) write stories in the **same
shared timeline** — one book, several narrators. Each story carries its
author, and each author has their own color so the two voices are clearly
distinguishable at a glance on the timeline and on story pages.

There are still **no accounts**: one shared password, one login. The author is
a label on the story, not an identity system. Do not add users, permissions,
or per-author passwords.

## 1. Configuration

New env var, documented in `.env.example` and the README config table:

```
STORYBOOK_AUTHORS="Papa:#d9a441,Maman:#7ba7d9"
```

- Comma-separated `Name:#hexcolor` pairs. Name is a display string (unicode
  allowed, no commas or colons); color is a CSS hex color chosen by that
  author.
- Parse in `create_app()` into `app.config["AUTHORS"]`: an ordered list of
  `{"name": ..., "color": ...}` dicts. On a malformed entry, raise
  `RuntimeError` at startup with a message showing the expected format (fail
  fast, like the SECRET_KEY check).
- **If unset or empty, the entire feature is invisible**: no selector in the
  editor, no bylines, no legend — the app behaves exactly as today. All
  templates and JS must guard on this.
- README should advise picking mid-brightness colors that read well on both
  the dark and light background, and state that renaming an author in the env
  var does not rewrite existing files (see §2).

## 2. Storage (frontmatter)

- New **optional** frontmatter field on `index.md`: `author: Papa` (the plain
  name string, not the color — colors live only in config so they can be
  retuned anytime).
- `Story` dataclass gets `author: Optional[str] = None`.
- `_write_index()` / `create_story()` / `save_story()` pass it through;
  omit the key entirely when the story has no author.
- **Unknown author names must never break anything.** A story whose `author`
  is not in the configured list (author renamed, config lost, file copied
  from elsewhere) renders with the byline text but the neutral default accent
  color. The files outlive the config; tolerate drift silently.

## 3. API

- `POST /api/stories` and `PUT /api/stories/<id>` accept an optional
  `author` string.
- Validation: if `STORYBOOK_AUTHORS` is configured and a non-empty `author`
  is provided, it must be one of the configured names → otherwise 400 JSON
  error (the UI is a picker; anything else is a bug or tampering). Empty /
  missing author is always allowed. If no authors are configured, ignore the
  field entirely.

## 4. Editor UI

- Below the date input, a row of **author chips** (one `<button type="button">`
  per configured author): the author's name with a small filled dot in their
  color. Tapping selects (one at a time; tapping the selected chip deselects
  → story saved without author). Selected chip gets a visible border in the
  author color + `aria-pressed="true"`. Rendered server-side from config;
  hidden entirely when no authors configured.
- Preselection order: the story's existing `author` when editing; otherwise
  `localStorage["storybook-author"]` if it matches a configured name;
  otherwise none. On change, store the choice in `localStorage` — each
  parent's phone remembers who they are, so after the first time it's
  zero-tap.
- `editor.js` includes the selected author in both create and update payloads.
  This must also apply to the auto-create that happens on first image upload
  (`ensureStoryId`), and the fallback textarea editor path must support the
  chips identically (they live outside the editor widget, so this should be
  free — verify it).

## 5. Story page

- Byline appears inside the existing date line:
  `JUNE 18, 2023 · MAMAN`, where the author name is preceded by a small
  colored dot (author's color) and the name uses the same small-caps style as
  the date. No author → date line unchanged.
- The `<hr class="story__flourish">` under the title takes the author's color
  (neutral accent when no/unknown author). Subtle, but it tints the whole
  page's mood toward its narrator.

## 6. Timeline — the "clear visual split"

This is the heart of the feature. Three coordinated cues, all driven by a
single inline `style="--author-color: #7ba7d9"` custom property set on the
entry when the story has a configured author (entries without an author keep
the neutral accent via the variable's fallback):

1. **The dot** on the spine is filled with the author's color and slightly
   enlarged (visible at arm's length — this is the primary cue).
2. **The author's name** appears after the date in the entry's date line
   (`Jun 18 · Maman`), in the author's color, same small size as the date.
3. **A legend** at the top of the timeline (only when ≥1 author configured):
   one chip per author — colored dot + name — so the color mapping is
   self-explanatory to a reader who has never seen the app. Static, not a
   filter (filtering is out of scope; add to "Ideas for later" if tempted).

Implementation notes: pass the configured author→color mapping into the
template from the route (build a dict once); do not inline hex values in CSS —
everything reads `var(--author-color, var(--accent))`.

## 7. Seed + tests + docs

- `scripts/seed_demo.py`: give the existing sample stories a mix of two
  authors and one story with no author, so the timeline demonstrates the
  split out of the box (seed works regardless of env config since unknown
  authors degrade gracefully).
- Tests to add:
  - config parsing (valid, malformed → RuntimeError, unset → feature off),
  - author round-trip through create/update API and frontmatter,
  - API 400 on unknown author when list configured; accepted when list not
    configured,
  - story/timeline pages render byline and legend when configured, and render
    identically to today when not,
  - unknown author on disk → page renders, neutral color.
- Update README (config table, a short "Several narrators" paragraph) and
  `.env.example`.

## Definition of done

- With `STORYBOOK_AUTHORS` unset: pixel-identical behavior to before (no
  selector, no legend, no bylines); all pre-existing tests untouched and green.
- With two authors configured: creating a story from a phone as "Maman" takes
  zero extra taps after the first visit; the timeline shows both voices
  clearly split by color with a legend; `index.md` on disk contains
  `author: Maman` and nothing about colors.
- Bare `pytest` green from a clean checkout.

---

# Feature batch 2 — F2..F10 (reading experience, rituals, durability)

Same ground rules: all decisions are made here — implement, don't redesign.
**No new dependencies** (stdlib + what's already vendored only). Every feature
is invisible/off when its configuration is absent, and every new piece of
story state is a plain optional frontmatter field — the files stay readable
forever without the app.

Where this batch conflicts with `PLAN.md` §11 ("out of scope for v1"), this
document supersedes it: print/PDF export (F10), a lightbox (F7), and a web app
manifest without a service worker (F9) are now in scope. Update the README's
"Ideas for later" section accordingly when done.

**Implementation order (respect it — later features build on earlier ones):**
F0 groundwork → F6 drafts → F4 sealed letters → F2 reading order → F3 age →
F5 on this day → F7 lightbox → F8 export → F9 manifest → F10 book view.
Commit per feature; bare `pytest` green before each commit.

---

## F0. Groundwork: story visibility (required by F2, F4, F5, F6, F10)

Two new **optional** frontmatter fields, parsed tolerantly (bad values are
treated as absent, never crash — same philosophy as unknown authors):

```yaml
draft: true          # boolean; absent means published
unlock: 2040-06-18   # ISO date; absent means not sealed
```

- `Story` dataclass gains `draft: bool = False` and
  `unlock: Optional[date] = None`. `_write_index()` writes each key only when
  set (`draft` only when true).
- New helpers in `storage.py` (pure, unit-tested):
  - `is_sealed(story, today)` → `story.unlock is not None and story.unlock > today`
  - `readable_stories(stories, today)` → published (non-draft), non-sealed,
    date-ascending — the canonical "pages of the book" used by F2, F5, F10.
- `POST/PUT /api/stories` accept optional `draft` (bool) and `unlock`
  (ISO string or `""`/absent to clear). Invalid `unlock` → 400 JSON error.
- Editor UI (both Toast and fallback paths — these live outside the widget):
  - a "Draft" toggle chip styled like the author chips, `aria-pressed`,
    placed on the same row as the author chips, right-aligned;
  - a "Seal until" `<input type="date">` (optional, clearable) next to the
    story date input, with a short label. Both sent on create and update,
    preserved when editing.

## F2. Reading order — previous / next story

The book gets page turning. On the story page footer, between "‹ Timeline"
and "Edit":

- `‹ <previous title>` and `<next title> ›` links, neighbors taken from
  `readable_stories()` (drafts and sealed letters are skipped). Truncate
  titles over ~40 chars with an ellipsis. First/last story: omit that side.
- Add `<link rel="prev">` / `<link rel="next">` in `<head>`.
- Keyboard: on the story page, plain (no modifier) `ArrowLeft`/`ArrowRight`
  navigate to prev/next unless focus is in an input/textarea/contenteditable.
  ~15 lines in a new `app/static/js/story.js`, loaded only by `story.html`.
- Layout: footer becomes a two-row grid on narrow screens (prev/next row above
  the Timeline/Edit row); tap targets ≥ 44px.
- Tests: middle story has both links in order; first/last omit one; a draft
  and a sealed story between two published ones are skipped; a draft story's
  own page renders without prev/next.

## F3. Age at each memory

New optional env `STORYBOOK_BIRTHDATE=YYYY-MM-DD` (the child's birth date;
document in `.env.example` + README). Invalid value → `RuntimeError` at
startup (fail fast, like STORYBOOK_AUTHORS). When unset, nothing changes.

- New pure helper `age_label(birthdate, on_date)` in a new `app/dates.py`:
  - `on_date < birthdate` → `"before you were born"`
  - under 1 month → `"N days old"` (`"1 day old"` singular)
  - under 1 year → `"N months old"` (full months, day-adjusted)
  - otherwise → `"N years old"` (floor; `"1 year old"` singular)
- Story page date line becomes `JUNE 18, 2023 · 2 YEARS OLD · PAPA` (age
  between date and author, same small-caps style, separated by the existing
  `·`). Timeline entries append it after the author: `Jun 18 · Papa · 2 years
  old` — smaller/dimmer than the date so rows don't get noisy.
- Sealed entries and the sealed page do NOT show age (the envelope stays
  minimal).
- Tests: each `age_label` branch incl. day-adjustment edge (born the 20th,
  story on the 19th of a later month), and page rendering with/without the
  env var.

## F4. Sealed letters ("open when you're 18")

A story with a future `unlock` date is a sealed envelope: visible as an
object, unreadable as text. **State plainly in the README**: the seal is
ceremonial, not cryptographic — anyone with the password (or the disk) can
open the file; the point is ritual, not security.

- Story page (`GET /story/<id>`) while sealed renders a dedicated
  `sealed.html` instead: centered column with an inline-SVG envelope (~64px,
  stroked in the author's color, neutral accent otherwise), then
  `A sealed letter{% if author %} from {{ author }}{% endif %}`, then
  `It opens on June 18, 2040.` and a `‹ Timeline` link. No title, no body, no
  cover, no age, no Edit link (authors reach editing via `/edit/<id>`
  directly, which keeps working — note this in the README paragraph).
- Timeline entry while sealed: keeps its chronological position; the dot is
  replaced by a small envelope glyph in the author color; text is
  `A sealed letter · opens June 18, 2040` (no title, no thumb); links to the
  sealed page. After the unlock date passes, the entry automatically becomes
  a normal entry — no action needed.
- Excluded from: prev/next (F2), on-this-day (F5), `/book` (F10), covers.
- Tests: sealed story page shows envelope not body; timeline shows envelope
  entry; unlock date in the past renders normally (freeze "today" by passing
  it into helpers — do not monkeypatch datetime globally; thread `today`
  through route → helper as a parameter with `date.today()` default).

## F5. "X years ago today"

On the timeline, when any readable story (per F0) from a previous year has
today's month and day: a quiet banner between the nav and the legend —
one line per match, newest first, capped at 3:

> 3 years ago today — [First bike ride](/story/...)

- Wording exactly: `{N} year{s} ago today — <linked title>`. Numeral, not
  spelled out.
- Style: small, warm, subtle — a left-accent-bordered box using the story
  author's color when present; no icon, no dismiss button, no animation.
- Feb 29 stories surface on Mar 1 in non-leap years (implement by "matches
  today" OR "story is Feb 29 and today is Mar 1 in a non-leap year").
- Tests: match, no-match, multiple matches capped at 3 and ordered, Feb 29
  rule, drafts/sealed never surface. Thread `today` as in F4.

## F6. Drafts

- `draft: true` stories are excluded from the timeline list, legend counts,
  F2 navigation, F5 banners, and F10's book. Their story page renders
  normally but with a small `DRAFT` pill next to the date line, and their
  direct URL keeps working (everyone with the password is family; no reader/
  author split exists).
- When ≥1 draft exists, the timeline shows a discreet `Drafts (N)` link under
  the legend → new page `GET /drafts` (`drafts.html`): a plain list of
  title + date + author dot, each linking to the story page, sorted by
  `updated` descending. When 0 drafts, no link and `/drafts` shows an empty
  state.
- Editor: the Draft chip (F0) defaults to off for new stories, reflects the
  saved value when editing.
- Tests: excluded everywhere listed; pill renders; drafts page lists and
  sorts; chip round-trips through the API.

## F7. Tap-to-zoom photos (lightbox)

Dependency-free, ~50 lines JS + CSS, loaded only on the story page
(`story.js` from F2 is the home for it):

- Tapping any `.story__body figure img` or the cover opens a full-viewport
  overlay: near-opaque background (`rgba(0,0,0,.92)`), image centered with
  `max-width/max-height: 100%; object-fit: contain`, the `<figcaption>` text
  (when present) in small italic below.
- Closes on: tap/click anywhere, `Escape`, or browser Back (push a history
  state on open; close on `popstate` — on a phone the back gesture is the
  natural exit).
- While open: `overflow: hidden` on `<body>`; focus moves to the overlay
  (`role="dialog"`, `aria-label` from the caption or "Photo"); restore focus
  on close. Fade-in ≤150ms, none under `prefers-reduced-motion`.
- No zoom/pinch handling, no prev/next arrows, no thumbnails strip — one
  photo, full screen, done. (Pinch-zoom still works via native browser
  gesture on the overlay image.)

## F8. One-tap backup

- `GET /export` (login required): streams a zip of the entire stories
  directory. Stdlib `zipfile` with `ZIP_STORED` (photos are already
  compressed), built into a `tempfile.TemporaryFile`, then `send_file` with
  `download_name=f"storybook-backup-{date.today().isoformat()}.zip"`.
  Skip `*.tmp` leftovers. Folder structure inside the zip = exactly the
  on-disk layout.
- UI: a small footer line at the bottom of the timeline:
  `Download everything (.zip)` — quiet text link, not a button.
- Tests: zip round-trip (create stories → export → open zip in test → same
  files/bytes), `.tmp` excluded, auth required.

## F9. Home-screen install (manifest, no service worker)

- New optional env `STORYBOOK_TITLE` (default `"Storybook"`): used in the nav
  brand, `<title>` suffix, manifest `name`, and the F10 book cover. This is
  how the app becomes "Le livre de <son's name>" on two phones. Document it.
- `GET /manifest.webmanifest` served by a tiny route (it needs the title from
  config): `name`/`short_name` from `STORYBOOK_TITLE`, `display: standalone`,
  `start_url: /`, `background_color`/`theme_color` = the dark background hex
  from `main.css`, icons: 192px and 512px PNG.
- Icons: `scripts/make_icons.py` (Pillow, run manually, outputs committed to
  `app/static/icons/`): dark rounded-square background using the theme's
  near-black, a simple stylized open book in the accent amber (exact shape at
  implementer's discretion — keep it geometric and legible at 48px). Generate
  192, 512, and 180 (`apple-touch-icon.png`).
- `base.html` head: `<link rel="manifest">`,
  `<link rel="apple-touch-icon" ...>`, and two `<meta name="theme-color">`
  (one per `prefers-color-scheme` via the `media` attribute).
- Explicitly NO service worker, no offline caching — revisit only if ever
  needed.
- Tests: manifest route returns valid JSON with the configured title; head
  contains the links.

## F10. The book view (`/book`) — read it all, print it all

One page containing every readable story (F0 ordering), for two uses: reading
the whole book start-to-finish on screen, and printing to PDF/paper.

- `GET /book` (login required), `book.html`:
  - **Cover section**: `STORYBOOK_TITLE`, then `Stories from {min year} to
    {max year}`, then the authors as name + dot (when configured). Vertically
    centered, full first page when printed (`page-break-after: always`).
  - **Stories**: each rendered with the same header structure as
    `story.html` (date line with age/author, title, flourish, cover image,
    body — extract a shared Jinja partial `_story_article.html` and reuse it
    in both templates rather than duplicating) separated on screen by a
    small centered ornament (`· · ·`).
  - A floating `Print / save as PDF` button (bottom right, hidden in print)
    calling `window.print()`.
- Print stylesheet (in `main.css` under `@media print`, applies to every
  page but matters here): force the light palette (white background, near-
  black text) regardless of theme; hide nav, minimap, legend, footers,
  buttons, flash messages; each `/book` story starts on a new page
  (`break-before: page`); body ~11pt serif, `line-height 1.5`; images
  `max-width: 100%`, `max-height: 22cm`, `break-inside: avoid`; `<mark>`
  prints with a light amber background and black text; `@page { margin:
  20mm }`.
- Link to it: a small `Read as a book` link next to the timeline's export
  link (F8 footer line).
- Performance note: at family scale (hundreds of stories) rendering
  everything on one page is fine; do not paginate, do not lazy-render.
- Tests: `/book` contains all readable stories in order and excludes drafts
  and sealed letters; cover shows configured title and year range; the shared
  partial keeps `story.html` rendering identical (existing page tests stay
  green).

---

## Batch definition of done

- Each feature off/invisible when unconfigured; with nothing configured
  beyond F1, every pre-batch test still passes unmodified.
- Full manual pass on a 390px viewport, dark theme: turn pages through three
  stories with a draft and a sealed letter interleaved; seal a story from the
  editor and see the envelope on the timeline; tap a photo full screen and
  exit with the back gesture; download the zip; `/book` prints a clean PDF
  with a cover page.
- No external requests from any page (re-check with browser devtools — this
  is checked after every batch, forever).
- Bare `pytest` green from a clean checkout.

---

## F11. HEIC/HEIF photo uploads (Android & iPhone originals)

The family's photo library is stored in compressed HEIF/HEIC (Android default
in their case; also iPhone originals via Files/AirDrop). Pillow alone cannot
decode these — uploads currently fail with `400 Could not process image`.
This is an ingestion-only change: **stored output remains plain JPEG**, so
the durability contract is untouched.

- Add `pillow-heif` to `requirements.txt`, pinned like the other deps. This
  is a deliberate exception to the minimal-dependencies rule, approved
  because every one of the family's photos is HEIF; do not add any other
  format plugin alongside it.
- In `app/storage.py`, at module import:

  ```python
  from pillow_heif import register_heif_opener
  register_heif_opener()
  ```

  That is the whole integration: `Image.open()` then handles `.heic`/`.heif`
  and the existing pipeline (EXIF transpose → resize → `convert("RGB")` →
  JPEG q85) applies unchanged. Verify `ImageOps.exif_transpose` still
  corrects orientation for HEIF (pillow-heif exposes EXIF; add a test).
- HEIF is not PNG, so the `is_png` branch stays false → output is
  `photo-NNN.jpg`. Correct; do not add a HEIF-passthrough.
- Tests (`tests/test_storage.py`): generate a real HEIC fixture in the test
  itself with pillow-heif (`Image.new(...).save(tmp / "x.heic")` after
  registering), including one with an EXIF orientation tag; upload through
  `POST /api/stories/<id>/images` in `tests/test_api.py` and assert a valid
  JPEG lands in the story folder with corrected orientation and long edge
  ≤ 2000px.
- README: add HEIC/HEIF to a short "supported photo formats" line (JPEG,
  PNG, WebP, AVIF, GIF/TIFF/BMP, HEIC/HEIF — everything except PNG is stored
  as JPEG).

---

# Feature batch 3 — F12..F16 (voices, instants, people, rituals)

**Prerequisite: batch 2 (F0, F2–F10) and F11 are implemented; this batch
builds on them.** F13 relies on the shared partial and exclusion lists from
F0/F2/F10; F15 relies on `readable_stories()`.

Same ground rules as batch 2: all decisions are made here — implement, don't
redesign. **No new runtime dependencies** (stdlib + browser APIs + what's
already installed only). The one apparent exception, transcription (F12), is
*not* an exception: it is an optional offline script with its own separate
requirements file, and **nothing in `app/` may ever import it**. The app must
run, test, and deploy exactly as before with that script deleted.

One shared architectural rule for this batch: **no new storage formats.** An
instant is a story with one extra frontmatter key. A person is the same
folder-with-`index.md`-and-photos shape stories already use. A voice memo and
its transcript are two plain files in the story folder. `stories/` remains the
single backup unit and stays fully readable with a file browser.

**Implementation order (respect it):**
F13 instants → F15 random → F16 prompts → F12 voice → F14 people.
Commit per feature; bare `pytest` green before each commit.

---

## F13. Instants — photo + one line, fifteen seconds on a phone

A low-friction capture mode: one photo, one sentence, done. Instants live on
the timeline alongside stories but visually lighter, so real stories keep
their weight.

### Storage

New **optional** frontmatter key, parsed tolerantly like `draft`/`unlock`:

```yaml
kind: instant        # absent or any unrecognized value means "story"
```

- `Story` dataclass gains `kind: str = "story"`. `_write_index()` writes the
  key only when it is `"instant"`.
- An instant is otherwise a completely normal story folder: `title` is the
  line truncated to 60 chars (or `"Instant"` when the line is empty), `cover`
  is the photo, the body is the one line of text as a single markdown
  paragraph. Nothing else.

### API

- `POST /api/stories` accepts optional `kind`: `"story"` (default) or
  `"instant"`; any other value → 400 JSON error. `PUT` does not accept
  `kind` — it is set at creation and preserved on update.
- If `PUT /api/stories/<id>` does not already accept a `cover` field, add it:
  optional filename, must match `FILENAME_RE` and exist in the story folder,
  else 400. (F13's capture flow needs to set the cover explicitly.)

### Capture UI

- `GET /new-instant` (login required) → `instant.html`: a deliberately tiny
  form — photo `<input type="file" accept="image/*">` (no `capture`
  attribute, so the phone offers both camera and gallery), a single-line text
  input (placeholder `One line…`, maxlength 200), a date input defaulting to
  today, the author chips (same markup/localStorage behavior as the editor —
  extract the chip logic if needed rather than duplicating it), and one Save
  button. No Toast UI, no draft/seal controls.
- New `app/static/js/instant.js` (~60 lines), loaded only by `instant.html`.
  On save: `POST /api/stories` with `{title, date, kind: "instant",
  markdown: line, author}` (title derived from the line per the storage rule)
  → upload the photo via the existing images endpoint → `PUT` with
  `cover: <filename>` → redirect to `/`. Photo is required (block save with
  a message if missing); the line is optional. Disable the Save button while
  in flight. All fetches go through the `response.ok` error pattern from
  `editor.js`.
- Timeline header: next to `+ New story`, a secondary (outline-style) button
  `+ Instant` → `/new-instant`.

### Rendering

- Timeline: instants render as compact entries — small square thumbnail
  (~56px), the line in body-text style (no title styling, no title at all),
  then the usual date + author dot. Clearly quieter than a story entry.
- Story page for an instant (`/story/<id>`) works as normal (cover + line);
  `/edit/<id>` opens the full editor (kind is preserved through save — see
  API rule above).
- Instants are **excluded from**: F2 prev/next (page-turning is for stories;
  an instant's own page shows no prev/next), and F15 random. They are
  **included in**: the timeline, F5 "years ago today" banners, and F10's
  `/book` — where they render compactly (photo + line as a captioned figure,
  no drop cap, no page-break-before; they are interludes, not chapters).
- Tests: kind round-trips through create/read and survives an edit-PUT;
  invalid kind → 400; cover-PUT validation; timeline shows the compact
  entry; prev/next skips instants; random never returns one; book includes
  it compactly.

## F15. Au hasard — open a page at random

- `GET /random` (login required): pick uniformly from
  `readable_stories(...)` filtered to `kind == "story"`, excluding the story
  id in the optional `?not=<id>` query param; 302 to `/story/<id>`. No
  eligible story → 302 to `/`.
- Entry points, exact labels:
  - timeline footer line (where F8/F10 links live): `Open a page at random`;
  - story page footer, on the prev/next row: a centered `At random` link
    between the two arrows, carrying `?not=<current id>`.
- Tests: redirects to an eligible story; with 2+ eligible stories and `?not`,
  never returns the excluded id; drafts, sealed letters, and instants are
  never chosen; empty case → timeline.

## F16. Graines d'histoires — against the blank page

A gentle writing prompt shown only when starting a new, empty story. Never
inserted into the text, never generated — a plain list of questions in a
plain text file.

### Prompt source

- Default list shipped at `app/prompts/default.txt` — the exact 56 lines in
  the appendix at the bottom of this document, verbatim, one prompt per line,
  UTF-8. (They are in French — the family's writing language. The UI chrome
  around them stays in English like the rest of the app.)
- Override: if `<stories_dir>/prompts.txt` exists and contains at least one
  valid line, it is used **instead** (not merged). Lines are stripped; blank
  lines and lines starting with `#` are ignored. This file belongs to the
  family and travels with their backup.
- New `app/prompts.py`: `load_prompts(stories_dir) -> list[str]` implementing
  the above, unit-tested (default, override, override-empty falls back,
  comments skipped).

### Editor UI

- Only on `/new` (no story id) and only until the story is first saved: above
  the editor widget, a single line in small italic muted type — the prompt
  text — followed by a small `↻` button (`aria-label="Another idea"`). No
  label, no icon, no box. Tapping `↻` shows another prompt (random, not
  sequential, no repeat until the list is exhausted).
- The server injects the initial prompt and the full list into the template
  as `<script type="application/json">`; cycling is client-side in
  `editor.js` (~15 lines). Nothing is ever inserted into the editor content.
- Hidden entirely when editing an existing story or when the list is empty.
- Tests: `load_prompts` cases above; `/new` page contains a prompt;
  `/edit/<id>` does not.

## F12. La voix — voice memos on stories

The story in your own voice. Recording uses the browser's built-in
`MediaRecorder` — no library. Unlimited length.

### Storage

- Audio files live in the story folder next to the photos:
  `memo-001.webm`, `memo-002.m4a`, … — same `NNN` numbering scheme as
  photos (next free number, per-story). Allowed extensions:
  `.webm .m4a .mp3 .ogg`.
- Optional transcript sidecar: same stem, `.txt` (`memo-001.txt`), plain
  UTF-8 text. **The app only ever reads sidecars; it never writes or
  generates them.** A sidecar can be produced by the offline script below or
  typed by hand — the app cannot tell the difference and must not care.
- Discovery: no frontmatter. `storage.py` gains
  `list_memos(story_dir) -> list[Memo]` (a small dataclass: `filename`,
  `transcript: Optional[str]`), sorted by filename; filenames must match
  `memo-\d{3}\.(webm|m4a|mp3|ogg)`.

### Server

- Raise `MAX_CONTENT_LENGTH` to `128 * 1024 * 1024` (long memos; ~9 h of
  Opus). Update the 413 handler message to "max 128 MB" and the item-3 test.
- `POST /api/stories/<id>/memos` (multipart `file`): validate the extension
  against the allowlist using the uploaded filename (the client names the
  blob `memo.webm` or `memo.m4a` from the recorder's actual mimetype);
  store as the next `memo-NNN.<ext>`; return `{"filename": ...}` 201.
  Invalid extension → 400 JSON.
- `DELETE /api/stories/<id>/memos/<filename>` (filename must match the memo
  pattern above, 404 if absent): removes the audio file **and its sidecar if
  present**, returns 204. (Accidental pocket recordings are common; this is
  the one deletion the app supports, and it stays memo-scoped.)
- Playback goes through the existing `/story/<id>/media/<filename>` route —
  `send_from_directory` already answers Range requests (verify with a test
  asserting a 206 on a `Range: bytes=0-3` request; iOS Safari requires Range
  support for audio seeking).

### Recorder UI (editor page, both Toast and fallback paths)

- A "Voice" section below the editor widget: a record button, an elapsed
  `mm:ss` timer, pause/resume, and stop. On stop, upload immediately (via
  `ensureStoryId()`, same as images), then append the new memo to the list.
- Use `MediaRecorder` with `audio/webm;codecs=opus` when
  `MediaRecorder.isTypeSupported` says so, else `audio/mp4` (iOS) — file
  extension `.webm`/`.m4a` accordingly. Call `recorder.start(1000)` and
  collect chunks so long recordings don't produce one giant final buffer.
  No client-side length cap.
- Below the controls, the story's existing memos: an `<audio controls
  preload="none">` player each, plus a delete button with a
  `confirm("Delete this recording?")` guard.
- Feature-detect: if `navigator.mediaDevices?.getUserMedia` or
  `window.MediaRecorder` is missing, hide the record controls but still show
  existing memos. If the user denies the mic permission, show a one-line
  message in the section, not an alert loop.
- **README note (required):** microphone capture only works in a secure
  context — HTTPS or `localhost`. On plain LAN HTTP the record button will
  not appear; playback still works everywhere. Recommend HTTPS via the
  reverse proxy for this feature.

### Story page

- After the story body, before the footer: a "Listen" section (small-caps
  heading, same style as the date line) — one `<audio controls
  preload="none">` per memo, in order. When a memo has a transcript sidecar,
  a `<details><summary>Transcript</summary>` below its player with the text
  as paragraphs. Section absent when the story has no memos. Sealed stories
  never show memos (the envelope stays sealed).

### Offline transcription (optional, never imported by the app)

- `scripts/transcribe_memos.py`: walks a stories dir, finds memos without a
  `.txt` sidecar, transcribes with `faster-whisper`, writes the sidecar.
  CLI: `python scripts/transcribe_memos.py ./stories --language fr --model
  small` (both flags with those defaults). Print per-file progress; skip and
  warn on failure, never crash the batch.
- Its dependencies go in `requirements-transcribe.txt` **only** — never in
  `requirements.txt`, never imported anywhere under `app/`. Add a README
  section: what it does, that it downloads a model on first run (hundreds of
  MB), that it is meant to be run occasionally from a laptop against the
  stories folder (or a copy of it — sidecars can be copied back), and that
  transcripts are ordinary text files anyone can also just write by hand.
- No tests for the script itself (its deps aren't installed in CI); test the
  app-side behavior only (sidecar shown when present, absent when not).

### Tests

Upload happy path (file lands as `memo-001.webm`, 201) and numbering after
an existing memo; bad extension → 400; delete removes audio + sidecar → 204,
unknown filename → 404, traversal-shaped filename → 400/404; `list_memos`
ordering and pattern strictness; story page with/without memos and
with/without sidecar; Range → 206; auth required on all memo endpoints.

## F14. Personnages — the cast of the book

Real books introduce their characters. One page per recurring person — who
they are *to him*.

### Storage

- `stories/people/<slug>/index.md` + photos, inside the existing stories
  dir — **one backup folder, unchanged**. `list_stories()` must skip the
  `people/` entry silently (explicitly, no "malformed folder" warning; add a
  test).
- Frontmatter: `name` (required), `relation` (optional free text, e.g.
  `"your grandmother"`), `photo` (optional filename in the same folder — the
  portrait), plus `created`/`updated` like stories. Body: free markdown
  about the person. Slug from `name` via the existing `slugify`, same `-2`
  collision rule; photos via the **same** image pipeline (refactor
  `save_image` so stories and people share it — resize/EXIF/naming
  identical, `photo-NNN` numbering).
- New `app/people.py` mirroring `storage.py`'s shape: `list_people`,
  `get_person`, `create_person`, `update_person` — pure functions taking the
  people dir, same atomic-write rule, same tolerant parsing (missing `name`
  → skip with a logged warning).

### Routes & pages

- `GET /people` → `people.html`: a card grid — portrait (square,
  `object-fit: cover`, subtle rounded corners; a neutral initial-letter
  placeholder when no photo), name, relation. Sorted by `created` ascending
  (the order they entered the book). Empty state: one quiet sentence and the
  New button. Header: `+ New person`.
- `GET /people/<slug>` → `person.html`: styled like a story page — relation
  as the small-caps line where the date goes, name as the title, portrait as
  the cover, body below. Footer: `‹ People` and `Edit`.
- `GET /people/<slug>/media/<filename>`: same validation/serving as story
  media.
- `GET /new-person`, `GET /edit-person/<slug>`: the editor page, reused (see
  below).
- API: `POST /api/people` (`{name, relation, markdown}`, name required →
  400 when blank), `PUT /api/people/<slug>`,
  `POST /api/people/<slug>/images` (returns `{"filename": ...}`; the first
  uploaded image becomes `photo` automatically if `photo` is not yet set).
- Nav: a `People` link in the top nav, always visible (it is the only way to
  discover the feature; the empty state explains it).
- Markdown image srcs in a person body must resolve to the person's media
  route: generalize the existing image-rewriting treeprocessor to take a
  media base path instead of hardcoding `/story/<id>/media/`.

### Editor reuse — do not fork editor.js

Parametrize instead of duplicating: `editor.js` currently hardcodes
`/api/stories...` endpoints. Change it to read its endpoints from the form's
data attributes (`data-create-url`, `data-update-url-template`,
`data-image-url-template`, `data-redirect-template`), with the story
editor template supplying today's values — behavior identical. The person
editor template supplies the people endpoints, omits the date input, the
author chips, the draft/seal controls, and the voice section, and relabels
the title input `Name` plus one extra plain text input `Relation`.
`editor.js` must tolerate all of those being absent (most already are
optional in batch 2's markup — keep it that way). Prompts (F16) do not
appear on person pages.

### Linking, deletion, book

- Stories link to people manually in markdown
  (`[Mamie](/people/mamie)`) — no auto-linking, no mention syntax; state
  this in the README.
- No person deletion (consistent with stories).
- People do **not** appear in `/book` or on the timeline in this batch.

### Tests

CRUD happy paths; blank name → 400; slug collision; people dir skipped by
`list_stories` without warning; person media traversal rejected; first image
becomes portrait; pages render (grid, person page, empty state); auth
required; story editor still works against its own endpoints (existing
editor tests stay green).

---

## Batch 3 definition of done

- With batch 3 deployed and nothing new configured: timeline, stories, and
  all batch-2 features behave exactly as before until someone records a
  memo, saves an instant, or creates a person. Every pre-batch-3 test passes
  unmodified (except the 413 limit test, updated per F12).
- Manual pass on a real phone (390px, dark): capture an instant end-to-end
  in under 20 seconds; record a 2-minute memo over HTTPS, play it back with
  seeking, delete a junk take; drop a hand-written `memo-001.txt` next to a
  memo and see the transcript appear; create two people and visit their
  pages; tap "Open a page at random" three times.
- `stories/` inspected by hand afterwards: instants, memos, sidecars, and
  people are all obvious, readable files in obvious places.
- No external requests from any page — including while recording.
- Bare `pytest` green from a clean checkout.

---

## Appendix — `app/prompts/default.txt` (copy verbatim, one per line)

```
Qu'est-ce qui t'a fait rire aux éclats cette semaine ?
Raconte le petit rituel du soir en ce moment, minute par minute.
Quel mot inventes-tu ou écorches-tu en ce moment ? Qui te comprend à ta place ?
Décris un dimanche matin ordinaire de cette période de ta vie.
Qu'est-ce que tu refuses catégoriquement de manger en ce moment — et la tête que tu fais ?
Raconte la dernière conversation surprenante qu'on a eue avec toi.
Quel jouet (ou objet improbable) ne te quitte jamais en ce moment ?
Raconte ta première rencontre avec quelqu'un qui compte aujourd'hui dans ta vie.
Qu'est-ce qui te fait peur en ce moment, et comment on te rassure ?
Décris ta chambre telle qu'elle est aujourd'hui, comme si on la faisait visiter.
Raconte le jour où on a appris que tu allais arriver.
Comment on a choisi ton prénom — et ceux qu'on a failli te donner.
Raconte ta naissance, du point de vue de celui ou celle qui écrit.
À quoi ressemblait la maison le jour où tu es arrivé ?
Quelle chanson te calme (ou te déchaîne) en ce moment ?
Raconte une bêtise récente qu'on n'a pas réussi à gronder sans rire.
Qu'est-ce que tu fais en ce moment qui ressemble trait pour trait à ton père ou ta mère ?
Raconte le trajet qu'on fait le plus souvent ensemble, et ce que tu y regardes.
Quel livre on te lit en boucle, et à quel moment tu ris ou tournes la page ?
Décris tes mains, tes pieds, tes cheveux en ce moment — ils changent si vite.
Raconte un moment récent où tu as été incroyablement courageux.
Qu'est-ce que tu dis au réveil, en ce moment ?
Raconte la dernière fois qu'on a dansé ou chanté ensemble dans la cuisine.
Quel est ton plat préféré du moment, et comment tu le manges ?
Raconte une visite chez tes grands-parents, telle qu'elle s'est vraiment passée.
Qu'est-ce qu'on aimerait que tu saches sur cette période de notre vie de parents ?
Raconte une nuit difficile — honnêtement — et ce qu'on s'est dit à trois heures du matin.
Décris ton rire. Vraiment. Qu'on l'entende en le lisant.
Quelle est ta cachette ou ton coin préféré de la maison en ce moment ?
Raconte tes premiers pas (ou le premier « presque »).
Quel a été ton premier mot — et le contexte exact ?
Raconte un anniversaire (le tien ou celui de quelqu'un d'autre) vu par toi.
Qu'est-ce que tu collectionnes ou accumules mystérieusement en ce moment ?
Raconte une grosse colère récente, et ce qui se passait vraiment derrière.
Décris comment tu t'endors, et ce qu'il faut absolument pour y arriver.
Raconte la première fois qu'on t'a vu te faire un ami.
Qu'est-ce que tu réclames « encore ! » sans jamais te lasser ?
Raconte une sortie récente — marché, forêt, piscine — avec un détail que toi seul as remarqué.
Quelles sont les personnes que tu réclames par leur nom en ce moment ?
Raconte le moment de la journée qu'on préfère secrètement passer avec toi.
Qu'est-ce que la saison actuelle change à tes journées — flaques, neige, cerises ?
Raconte un objet de famille qu'on veut te transmettre, et son histoire.
Qu'est-ce qu'on faisait, nous, à ton âge ? Raconte un souvenir d'enfance en miroir.
Raconte la dernière fois que tu nous as impressionnés sans le savoir.
Décris un repas complet avec toi en ce moment, du début motivé à la fin par terre.
Quelle expression ou grimace fais-tu qu'on veut absolument ne pas oublier ?
Raconte comment tu accueilles les gens qui passent la porte.
Qu'est-ce que tu fais quand tu crois qu'on ne te regarde pas ?
Raconte une promesse qu'on se fait à ton sujet en ce moment.
Quel métier ou quelle passion déclares-tu vouloir faire plus tard, cette semaine ?
Raconte la dernière photo qu'on a prise de toi : ce qu'il y a autour, avant, après.
Qu'est-ce qui a été difficile pour nous cette semaine, et pourquoi ça valait le coup quand même ?
Raconte le bain en ce moment : la logistique, les inondations, les jouets.
Décris ta voix en ce moment, les phrases que tu répètes, ton accent à toi.
Raconte une tradition familiale qu'on est en train d'inventer avec toi.
Qu'est-ce qu'on voudrait te dire aujourd'hui, si tu pouvais tout comprendre ?
```

# F17. Le style du ranch — hand-drawn visual identity

The interface gets a set of hand-engraved western-storybook illustrations
(generated once, committed as static files — the app never fetches anything).
The processed assets are already committed under `app/static/img/`:

| file | size | where it goes |
|---|---|---|
| `tumbleweed.jpg` | 900×488 | 404 page |
| `sealed-letter.jpg` | 576×495 | sealed-story page |
| `empty-chest.jpg` | 653×729 | drafts + archived empty states |
| `person-oval.jpg` | 600×732 | person placeholder + people empty state |
| `instant-camera.jpg` | 522×652 | /new-instant decorative accent |
| `book-frame.jpg` | 715×897 | /book cover ornament |
| `rope-divider.png` | 1000×144, transparent | flourishes/dividers |
| `lasso-ring.png` | 320×320, transparent, centered | loading spinner |

Added later by F42, from the prompts in `IMAGE-PROMPTS.md`, same paper-card
treatment (`.illo`) and the shared `.illo--page` sizing:

| file | size | where it goes |
|---|---|---|
| `group-circle.jpg` | 760×612 | /groups + help's "Who can read a story" |
| `write-link-pass.jpg` | 700×600 | /account/write-links + the delegate page |
| `invite-card.jpg` | 700×564 | invite, accept-invite, request-account |
| `firsts-boots.jpg` | 760×519 | /firsts |
| `almanac-book.jpg` | 700×700 | /almanac |
| `growth-doorpost.jpg` | 567×760 | /growth |
| `history-pages.jpg` | 720×598 | a story's /history |
| `help-lantern.jpg` | 628×700 | /help header |
| `accounts-keys.jpg` | 760×540 | /account |

Also committed: `login-campfire.jpg` (856×735) — the login-page
illustration, reused for the empty-timeline state — and the leather-journal
app icon regenerated over the old placeholder icons at
`app/static/icons/icon-512.png`, `icon-192.png`, and
`apple-touch-icon.png` (same filenames; the manifest and templates need no
path changes). Wire the login page and empty-timeline placements like every
other card: the login page shows the campfire card between the subtitle and
the password field (max-width 20rem), the empty timeline shows it above the
"No stories yet" line.

## The paper-card treatment (the key to theming)

Every JPEG illustration carries its own cream paper background, so it is
displayed as a "paper card pinned to the page": a shared `.illo` class —
background the same cream as the illustrations (sample it from any of the
JPEGs; they are consistent), padding ~0.75rem, a thin border using the
light theme's border color regardless of theme, border-radius 4px, a soft
shadow, and a slight rotation (default -1.2deg; add `.illo--tilt-right`
with +1deg to alternate). The card stays cream in ALL themes — in dark
mode it reads as a photograph card in an album, which is the intent. The
transparent PNGs (`rope-divider.png`, `lasso-ring.png`) are NOT cards —
they sit directly on the page background in every theme.

Every decorative `<img>` gets `alt=""`, `loading="lazy"`,
`decoding="async"`, and explicit `width`/`height` attributes (no layout
shift). Displayed sizes are roughly half the pixel size (they are 2×
assets). Total added weight per page stays under ~150 KB — each page uses
at most one or two illustrations.

## Placements

- **404**: tumbleweed card above the existing message, max-width 20rem.
- **Sealed page**: sealed-letter card replaces the inline envelope SVG,
  max-width 18rem; keep the title and "opens on" line unchanged.
- **Drafts / Archived when empty**: chest card, max-width 14rem, above a
  one-line empty message (add one if missing, e.g. "Nothing here — drafts
  you start will wait in this chest.").
- **People**: grid placeholder portraits use `person-oval.jpg` as the tile
  image with the person's initial rendered on top (absolutely positioned
  over the oval's center, current font/color); people empty state shows the
  same oval card with the existing empty text.
- **/new-instant**: camera, small (max-height 9rem), centered above the
  photo picker, hidden on viewports under 700px tall so the form stays
  above the fold — the 20-second flow must not get slower or longer.
- **/book cover**: `book-frame.jpg` centered on the cover page with the
  book title, year range, and author legend overlaid INSIDE the frame
  opening (absolute positioning over the image); frame max-width 24rem on
  screen. In print (`@media print`) keep it — it prints beautifully — but
  verify the title stays inside the opening at A4.
- **Flourishes**: the `· · ·` separator in /book and the `story__flourish`
  hr on story pages become `rope-divider.png` (`width: 240px` in book,
  `160px` on story pages, centered; keep an `<hr>`/role for semantics).
- **Spinner**: `.lasso-spinner` = `lasso-ring.png` at 40×40, CSS
  `animation: spin 1.4s linear infinite`. Under
  `prefers-reduced-motion: reduce`, no rotation — pulse opacity instead.
  Show it: on /new-instant next to the disabled Save while uploading, on
  /import while the restore request runs, and in the editor save bar while
  saving. Never block input with it; it is an indicator only.

## Rules

No new dependencies. No external requests (re-verify after — the images
are local static files). The story/instant/person markdown format is
untouched — this feature is chrome only. `pytest` green; update any test
that asserts on the sealed page's SVG or the flourish markup.

Definition of done: phone-width pass of 404, sealed, drafts (empty),
people (with and without portraits), /new-instant, /book (screen + printed
PDF), a story page, in all three themes — paper cards read as cards on
dark; transparent rope elements show no cream box; no horizontal scroll;
no cumulative layout shift when images load; zero external requests.

# F18. L'arbre — the family tree

A genealogical tree built on the people pages (F14), designed in three
layers with different life expectancies: facts in frontmatter (forever),
a Python kinship engine with a JSON contract (life of the app), and a
vendored JS renderer (replaceable). The renderer — family-chart 0.9.0 +
d3 7.9.0 — is **already committed** under `app/static/vendor/familychart/`
and `app/static/vendor/d3/` (pinned, licensed, audited for zero network
calls; see VENDORED.md there). Do not fetch anything from npm.

Ground rules: no new pip dependencies; the vendored JS is the only new
front-end code source; every new frontmatter field is optional and
tolerantly parsed; the whole feature is invisible until the first family
link exists; the backup format does not change.

## Layer 1 — facts in frontmatter (`stories/people/<slug>/index.md`)

New optional fields, all slugs referring to other people:

```yaml
parents: [papi-georges, mamie-lise]   # this person's parents
partners: [claire]                    # spouses/companions (symmetric)
friend_of: [papa]                     # for friends: whose friend they are
gender: m                             # m | f, only used to pick label words
```

- Store ONLY these atomic facts. Never store computed kinship ("uncle",
  "cousin") — it is always derived. The existing free-text `relation`
  field stays and, when present, wins over any computed label.
- `parents` is the single source of parent/child truth; children are
  computed by reverse lookup. Cap of 2 parents enforced on write; extra
  entries on disk are read tolerantly.
- `partners` is symmetric: the API writes both sides; reads take the
  union of both directions so a hand-edited single side still works.
- Dangling or unknown slugs anywhere: ignored silently. Files outlive
  edits.
- `Person` dataclass gains `parents`, `partners`, `friend_of` (lists,
  default empty) and `gender` (optional). Writers omit empty fields.

## Config

`STORYBOOK_CHILD=<slug>` (optional, alongside STORYBOOK_BIRTHDATE in
.env.example + README): the anchor person all kinship labels are relative
to. Unset or slug not found → no kinship labels, everything else works.
The child should get his own person page — document that in the README
("create a person for your child and point STORYBOOK_CHILD at it").
When the book is inherited, the heir re-points this one line and every
label re-anchors to the next generation.

## Layer 2 — kinship engine (`app/kinship.py`, new, stdlib only)

- `build_graph(people) -> Graph`: nodes by slug; parent and partner edges
  (partner edges from the union of both sides).
- `children_of`, `siblings_of` (share ≥1 parent), `partners_of` helpers.
- `kinship_label(graph, anchor_slug, person_slug) -> str | None`:
  BFS from anchor over parent/child edges, classify by (steps up, steps
  down), gendered word when `gender` is set:
  - up n: parent / grandparent / great-grandparent / (n-2)×"great-" —
    m: father→"your father", grandfather…; f: mother…; absent: parent…
  - down n: son/daughter/child, grandson… (used when anchor is an
    ancestor of the person's descendants view — labels are always about
    the PERSON relative to the anchor: "your uncle", "your cousin")
  - up 1 + down 1: brother / sister / sibling
  - up 2 + down 1: uncle / aunt / "aunt or uncle"
  - up n≥3 + down 1: great-uncle / great-aunt (one "great-" per extra step)
  - up 2 + down 2: cousin; anything deeper or unequal: "cousin"
  - up 1 + down 2 does not exist from a child anchor; nephews/nieces
    (down via sibling) appear when the anchor changes generations:
    sibling's child = nephew / niece / "niece or nephew"
  - partner of a labeled relative, not otherwise related: "X's husband /
    wife / partner" using the closest labeled relative's short label
    (e.g. "your uncle's wife"). One hop only — beyond that, no label.
  - unreachable from anchor: None.
- Cycle guard: `would_create_cycle(graph, child, new_parent) -> bool`
  (a person cannot be their own ancestor).
- All label text in English, matching the app UI. Unit-test the label
  table exhaustively with a fixture family of ~15 people including a
  great-grandmother, an uncle by marriage, and a half-sibling.

## API

- `PUT /api/people/<slug>` (and POST create) accepts `parents`,
  `partners`, `friend_of` (lists of slugs) and `gender` ("m"/"f"/"").
  Validation, each → 400 with a clear message: unknown slug; self
  reference; >2 parents; parent cycle (use the cycle guard); gender not
  in {m, f, ""}.
  Partner symmetry: when partners change, update the other person's file
  too (add/remove the reverse link); their `updated` timestamp changes —
  that is correct and version history (F8) records it.
- `GET /api/tree` (login required): the Layer-2/3 contract —
  ```json
  { "anchor": "milo",
    "people": [ { "id": "papi-georges", "name": "Papi Georges",
      "gender": "m", "photo": "/people/papi-georges/media/photo-001.jpg",
      "url": "/people/papi-georges", "kinship": "your grandfather",
      "rels": { "parents": ["henri"], "partners": ["mamie-lise"],
                "children": ["papa", "remi"] } } ] }
  ```
  `anchor` null when unset; `photo` null when none; `kinship` null when
  no anchor or unreachable; `rels.children` computed. Friends (people
  whose only link is `friend_of`) are included with a `"friend_of":
  [...]` key instead of `kinship`. Document this contract in the README —
  it is the seam future renderers plug into.

## Person pages (works without JavaScript)

- A "Family" section after the body, computed server-side: Parents,
  Partner, Children, Siblings — name links to their pages, portraits as
  small inline thumbs where available. Rendered only when non-empty.
- The kinship label: when an anchor is set and `relation` (free text) is
  absent, the small-caps line above the name uses the computed label
  ("YOUR GREAT-GRANDMOTHER"). Free-text `relation` always wins.
- Friend pages: the small-caps line reads "Friend of Papa" (linked),
  from `friend_of` + the same relation-wins rule.

## Person editor — filling the tree in

A "Family" fieldset below Relation, shown only when at least one other
person exists: three pickers (Parents — up to two, Partner, Friend of),
each a row of person-chips reusing the author-chip look (portrait thumb +
name, tap to toggle), plus a Gender segmented control (M / F / unset).
editor.js includes the values in the person PUT payload. No drag-and-drop
tree editing — the pickers are the entire editing surface.

## Layer 3 — the /tree page

- `GET /tree` (login required): page with a full-height chart container,
  loading the vendored `d3.min.js`, `family-chart.min.js`,
  `family-chart.css`, and a new `app/static/js/tree.js` (~80 lines) that
  fetches `/api/tree`, maps it to family-chart's Datum format
  (`{id, data: {label, avatar, gender}, rels: {parents, spouses,
  children}}`; gender absent → "M" is NOT assumed, pass the field only
  when known and default the card styling to neutral), and calls
  `f3.createChart('#FamilyChart', data)` with `setCardHtml()`, card
  display = name, `cardImageField` avatar (fallback: the
  `person-oval.jpg` asset), main id = anchor (else first person),
  `setSingleParentEmptyCard(false)`, vertical orientation, transition
  ~600ms. Card click navigates to the person's page; the mini re-root
  control (library default) stays enabled so any family member can
  become the center. Hide the library's edit/add-relative UI — editing
  happens only in the person editor.
- Ranch restyle in main.css (scoped under `.page-tree .f3`): cream card
  faces (`--card` tokens per theme), umber connectors, gold border on the
  main card, Georgia/serif labels, neutralize the library's pink/blue
  gender fills in ALL themes. The dark theme shows dark cards with cream
  portraits — cards here are chart cards, not F17 paper cards.
- Below the chart, a plain HTML list "Friends & others": friends (with
  "friend of X") and people with no links at all. Nothing is ever
  invisible just because it is unlinked.
- Discoverability: a "Family tree" link on the /people page header, shown
  only when at least one person has parents or partners; same condition
  for showing nothing at /tree except a gentle empty state ("Link two
  people in the person editor and the tree will grow here.").
- Print: `@media print` hides the chart and shows the "Friends & others"
  list plus a note to use the app for the interactive tree (a dedicated
  print layout is a future feature — do not attempt it here).

### View scopes (added after dogfooding)

The hourglass layout only ever shows the main person's direct line, so
collateral relatives (aunts, uncles, cousins) become visible by rooting
the layout at an ancestor. A toolbar above the chart, built by tree.js
from the ancestor levels that actually exist for the focus person:

- **Direct line** — main = focus (the original behavior).
- **Grandparents' branch**, **Great-grandparents' branch**, … — one
  button per intermediate ancestor level; rooting at a grandparent shows
  aunts/uncles (their children) and cousins (their grandchildren).
- **Whole family** — rooted at the focus's deepest ancestor.
- When a level has several couples (paternal vs maternal side), "via
  Rose & Jean" chips pick the branch; couples are grouped by partner
  links, first couple is the default.
- The focus person keeps a thin gold ring (`card-inner--focus`) in
  rooted views so they stay findable; the full brand stays on
  `card-main` (the current root). The mini-tree control now moves the
  focus and resets to Direct line.
- The toolbar is hidden when the focus has no recorded ancestors, and
  hidden in print with the chart.

### The moving survey map (added after dogfooding)

The R5.7 map background was a static CSS JPEG on the container, so it
stayed put while the chart panned underneath. Replaced by an SVG
`<pattern>` filling a large rect injected as the first child of the
chart's `g.view` pan/zoom group — it translates and scales in lockstep
with the tree. The pattern holds two seamless 1024px raster tiles
(`tree-map-tile-dark.jpg` dark leather, `tree-map-tile.jpg` parchment;
image-model art post-processed to tile: vignette flattened, edges
torus-blended along the measured 128px grid period, ornament patched
out); CSS shows the tile matching the theme (`tree-map-img--dark/
light`), the container keeps only the base leather/parchment color.
The old full-bleed `tree-map.jpg` / `tree-map-dark.jpg` are no longer
referenced.

### Second dogfooding round: editor hint, recenter, kinship on cards,
### honest branch depth, remembered view

- **Empty-editor hint.** When `/new-person` or `/edit-person/<slug>`
  has no `other_people` yet, the Family fieldset used to simply not
  render — someone filling in their very first person had no clue it
  existed. `person_editor.html` now renders `<p class="editor__family-hint">`
  in its place: "Add another person and you'll be able to link parents,
  a partner, and gender here…". The hint's class deliberately avoids the
  literal substring `editor-family` so it doesn't trip the existing
  "fieldset absent" tests, which assert that exact string is nowhere in
  the response.
- **Recenter button.** `family-chart` auto-fits the tree to the viewport
  on every `updateTree()` (a d3-zoom transform on `#f3Canvas`, exposed
  as `canvas.__zoomObj`), but a reader who pans/zooms away has no way
  back short of reloading. `tree.js` snapshots that transform via
  `d3.zoomTransform(canvas)` ~650ms after each render settles (matching
  `setTransitionTime(600)`) and a pinned `.tree__recenter-btn` in the
  chart's corner re-applies it with `canvas.__zoomObj.transform`.
- **Kinship labels on cards.** `/api/tree` already computed
  `kinship` per person (F18 Layer 2); it just wasn't surfaced in the
  chart. Cards now show it in small caps under the name
  (`.f3-card-kinship`, with a `title` attribute so a long label like
  "your great-great-grandmother" is still readable via hover/long-press
  when the 12rem card truncates it). Card width bumped 10rem → 12rem so
  the common cases ("your grandfather", "your cousin") fit without
  truncating.
- **Honest branch depth ("Whole family" bug fix).** The view-scope
  toolbar's level buttons used to re-root at `levels[lv-1][0]` — the
  first ancestor at that depth from ANY branch, regardless of which
  branch the reader had already drilled into. Clicking "Whole family"
  while looking at the maternal grandparents could silently jump to an
  unrelated paternal great-grandmother. Fixed by tracking a `chain[]` of
  the ancestor selected at each depth (extended via
  `TreeLogic.chainToLevel`, which walks the first parent one generation
  at a time from whichever root is already selected) — level buttons now
  extend the CURRENT branch, and a branch that runs out of recorded
  ancestors just stops there instead of jumping elsewhere. `viewLevel`
  is always derived from `chain.length`, so the toolbar's pressed state
  reflects what's actually on screen (if "Whole family" only reaches
  depth 2 on this branch, the depth-2 button shows pressed, not
  "Whole family"). The pure chain/level logic (`ancestorLevels`,
  `coupleGroups`, `levelLabel`, `chainToLevel`) was extracted out of
  `tree.js` into `app/static/js/tree-logic.js`, a dependency-free
  UMD module, specifically so it could be unit-tested (see Tests below)
  — this is also what made the original arbitrary-pick bug easy to spot
  and fix with confidence.
- **Remembered view.** The chosen `{focusId, chain}` is saved to
  `localStorage["storybook-tree-view"]` on every view change and
  restored on the next `/tree` visit (only when `focusId` still matches
  and every chain entry still resolves to a real person — a deleted
  person or a changed `STORYBOOK_CHILD` just falls back to Direct line).
  Silently no-ops when localStorage is unavailable (private browsing,
  quota) — nothing else depends on it.
### Code-review fixes round

A recall-focused review of the second dogfooding round above turned up
several real bugs and duplication in the same view-scope/map-background
code, before any of it shipped to a wider audience. Fixed:

- **Branch-chip chain corruption.** Switching branches used to patch
  only the deepest chain entry (`chain.slice(0, viewLevel - 1)
  .concat([group[0]])`), which is wrong whenever the new couple is on a
  different lineage than what's already in the chain (paternal vs.
  maternal) — clicking a maternal grandparents chip while chain was
  `['papa', 'papi-jean']` produced `['papa', 'papi-paul']`, and
  papi-paul isn't papa's parent. `tree-logic.js` gained `ancestorPath`
  (walks the parent graph from focus to find the REAL chain reaching a
  target ancestor), and the branch-chip handler now uses that instead
  of patching.
- **Stale localStorage chains.** `restoreSavedView` used to accept a
  saved chain as long as every id still existed as *some* person,
  never checking the links were still parent/child — so an edited
  parent link could restore an internally inconsistent view instead of
  falling back to Direct line as documented. `tree-logic.js` gained
  `isValidChain`; an invalid saved chain is now discarded entirely.
- **Toolbar level-1 gap.** The level-button loop skipped level 1
  whenever the tree went deeper than one generation (it looked
  redundant with Direct line), but a branch that dead-ends after one
  generation can legitimately leave `viewLevel` at 1 — with no button
  for it, nothing showed pressed. The loop now always includes level 1
  (given its own "Parents' branch" label, fixing an old off-by-one
  where `levelLabel(1, deepest)` collided with level 2's label).
- **Keyboard focus loss.** `renderToolbar()` rebuilds every button via
  `innerHTML = ""` on each click, which silently dropped keyboard
  focus to `<body>`. It now remembers whether focus was inside the
  toolbar before rebuilding and restores it to whichever button ends
  up pressed.
- **Focus-person gold ring never rendered.** `.card-inner--focus`'s
  border/box-shadow lost a CSS specificity tie to the older, more
  specific `div.card-inner` rule, so the ring was always overridden.
  Fixed by matching that rule's specificity.
- **Map background double-fetch.** Both theme tiles were always
  inserted into the SVG pattern, with CSS `display:none` hiding the
  inactive one — which doesn't stop the browser fetching/decoding it.
  Only the active theme's tile is injected now, with a
  `MutationObserver` on `data-theme` and a `prefers-color-scheme`
  listener to swap it live if the reader changes theme mid-session.
- **Recenter timing.** The 650ms snapshot delay was guessed to match
  `setTransitionTime(600)`, but the vendored bundle's fit transition
  adds its own 100ms pre-delay before that duration starts — settling
  at ~700ms, not 600ms. Bumped to 720ms so Recenter doesn't capture a
  still-interpolating transform.
- **Pedigree collapse.** `ancestorLevels`'s single, all-levels `seen`
  map meant an ancestor reachable via two lineages at different depths
  (a remarriage or cousin match) was silently dropped from the deeper
  occurrence. Dedup now happens only within a level, with a
  generation-count cap standing in for the removed cycle guard.
- **escapeHtml() didn't escape quotes** — fine for text content, not
  safe for the `title=`/`href=` attribute contexts this round started
  using it in. Now escapes `"` and `'` too.
- **Decorative SVG map elements** (the injected `<image>`/`<rect>`)
  now carry `aria-hidden="true"`, matching how the old CSS background
  was invisible to assistive tech by construction.
- **installMapBackground()** now `console.warn`s instead of silently
  no-op'ing if the vendored bundle's internal SVG structure
  (`svg.main_svg` / `g.view`) ever stops matching, so a future
  vendored-library upgrade that breaks it is at least debuggable.
- **Cleanup:** `.tree__view-btn`/`.tree__recenter-btn` now compose
  with the existing `.btn` class instead of re-declaring its
  flex-centering/font/cursor from scratch. A new
  `app/static/js/safe-storage.js` (same dependency-free UMD shape as
  `tree-logic.js`) centralizes the try/catch-wrapped localStorage
  access that `tree.js`, `editor.js`'s autosave, and `author-chips.js`
  each used to reimplement independently.

Tests: `tests/js/tree_logic_test.mjs` gained coverage for
`ancestorPath`, `isValidChain`, the level-1 label, and the pedigree-
collapse case; a new `tests/js/safe_storage_test.mjs` covers the
storage wrapper (including simulated private-mode/quota failures).

### Multi-branch rendering round

The branch-chip toggle above let a reader see one ancestor couple's
descendants at a time, but never two at once — so paternal and maternal
grandparents (or any two couples at the same depth) could never appear
together on screen, only reached one at a time. Rooting the chart
directly at the focus person (level 0, "Direct line") was never actually
broken this way: a person has at most two parents, so a pedigree rooted
at them already recurses through both sides simultaneously. The gap was
specific to levels ≥ 1, which exist to reveal *lateral* relatives
(aunts/uncles/cousins) by re-rooting at a specific ancestor to show
*their* descendants — and one ancestor's descendants are a different,
disjoint subtree from their partner-couple's counterpart on the other
side. No single-root hourglass can show two disjoint subtrees in one
drawing.

Fixed by replacing the single chart + branch-chip switcher with one
independent `family-chart` instance **per ancestor couple** at the
chosen level, rendered together — stacked on phones, a `repeat(auto-fit,
minmax(20rem, 1fr))` grid from `700px` up (`.tree__panels` /
`.tree__panel` in `main.css`), each captioned "via Name & Name" and each
fully interactive (its own pan/zoom, mini-tree re-root, Recenter). Level
0 is untouched — still the single big chart. This reuses the
already-vendored, network-audited `family-chart` + `d3` bundle as
multiple independent mounts; no new dependency, no vendored-file changes.

This also deleted code rather than adding much: with every couple at a
level shown at once, there's no more "which branch is selected" to
track, so `tree-logic.js`'s `ancestorPath`, `isValidChain`, and
`chainToLevel` — and the `chain[]`/branch-chip machinery in `tree.js`
built around them — are gone. View state is now just `{focusId,
viewLevel}`; `ancestorLevels` and `coupleGroups` (unchanged) are enough
to compute which panels a level needs on every render. Charts are always
torn down and rebuilt on a level or focus change rather than re-rooted
in place — the same "just rebuild it" approach `renderToolbar()` already
used — since the number of panels needed can change between any two
levels. One consequence: the injected ranch-map SVG pattern/image ids
(`tree-map-grid-*`) are now suffixed per panel, since `url(#id)`
resolves against the whole document and several simultaneous panels
would otherwise fight over one id; the `MutationObserver`/
`prefers-color-scheme` listener that refreshes them on a theme change
was hoisted to run once for the page instead of once per chart instance,
which would have leaked a new observer on every rebuild.

Tests: `tests/js/tree_logic_test.mjs` dropped the now-dead
`ancestorPath`/`isValidChain`/`chainToLevel` coverage and gained a
`coupleGroups` case asserting the paternal and maternal branches land in
separate groups, which is what the multi-panel view depends on.

### Print outline round — closing the print/PDF gap

`/tree` never had a print representation of the family itself — only
"Friends & others" and a static note survived `@media print`, since the
interactive chart obviously can't. Rather than trying to make an SVG
chart survive print, the note is replaced with a plain-text generation
outline, server-rendered (works without JS, like every other family
page): headings such as "Great-grandparents' generation" / "Parents'
generation" / "Milo's generation" / "Children's generation", oldest
first, each listing names with their existing computed kinship label
("Papi Paul — your grandfather").

Each in-family person gets a **generation offset** relative to
`STORYBOOK_CHILD`: positive toward ancestors, negative toward
descendants, 0 for the anchor's own generation. This is measured from
each person's own nearest common ancestor with the anchor (`kinship.py`'s
existing `_blood_updown`, extracted out of `_blood_kinship` — same
`(up, down)` pair `kinship_label` already computes, just exposed as a new
`generation_offset()` alongside it) — deliberately **not** a structural
"depth from the deepest recorded root," which would misfile a grandparent
a whole generation off whenever their own parents aren't recorded (the
fixture family already has exactly this shape on the maternal side). An
offset bucket like "Parents' generation" intentionally mixes real parents
with aunts/uncles (same net distance) — that's colloquially accurate, not
a bug, and the per-person kinship label still gives the precise relation.
A person reachable only via one hop of partnership (e.g. an uncle's wife
with no blood link of her own) inherits her partner's offset, mirroring
`kinship_label`'s existing "your uncle's wife" fallback; someone
reachable by neither blood nor that one hop (an isolated in-law couple
with no connection to the family's blood graph) lands in a final "Other
family" bucket rather than silently vanishing. Without `STORYBOOK_CHILD`
set, generation math doesn't apply — everyone in-family lands in one
plain "Family" bucket, same as kinship labels already disappearing
app-wide without an anchor.

`routes_pages.py`'s `tree_page()` folds this into the loop that already
built the `others` list (no second pass over `all_people`), bucketing by
`kinship.generation_offset()` and sorting real offsets descending
(oldest generation first) before rendering. `tree.html` renders it as
`.tree__print-outline`, `display: none` on screen and forced to `display:
block` inside `main.css`'s existing `@media print` block, the same
shape `.tree__print-note` used before it.

Tests: `tests/test_kinship.py` gained a `generation_offset` table
parametrized against the same 16-person fixture the kinship-label table
already uses (including the great-uncle/uncle's-wife/cousin cases, plus
an isolated-partner-pair case for the "no path at all" `None` result) and
a `generation_group_label` table; `tests/test_family_pages.py` gained
`/tree` cases for the anchored multi-generation outline, the unanchored
single-bucket fallback, and confirming friends/unlinked people never leak
into the outline.

### Tests (second round)

`tests/js/tree_logic_test.mjs` — plain Node, no framework or npm
dependency, exercises `tree-logic.js`'s pure functions against a small
fixture family (three generations plus one paternal-only
great-grandmother), including the specific regression case: switching to
a branch with no recorded parents and then clicking "Whole family" must
stay on that branch rather than jumping to the other side's deeper
ancestor. Wired into the pytest suite via `tests/test_tree_logic_js.py`,
which shells out to `node` and skips (not fails) if it isn't on `PATH` —
GitHub's `ubuntu-latest` runners ship Node by default, so this still
runs in CI without adding a Node setup step. Server-rendered pieces
(the empty-editor hint, `tree-logic.js` load order) are covered in
`tests/test_family_pages.py` the normal way.

### "Everyone" round — one canvas for the whole family

Real dogfooding feedback: neither existing view actually shows everyone
at once. "Direct line" is one chart, but only the focus's own ancestors —
no siblings, aunts, uncles, or cousins. "Whole family" reveals those, but
splits every ancestor couple at the deepest level into its own separate
side-by-side panel — paternal and maternal branches are two disconnected
charts a reader has to pan/zoom individually, and a family with more than
two branches gets more scattered panels, not fewer.

Closed by adding a fourth toolbar option, "Everyone", that renders every
branch in **one** `family-chart` instance instead of one per couple.
`family-chart` only ever draws the ancestors-and-descendants of a single
`main_id`; there's no library-native way to hand it several disjoint
lineages at once. The fix is a synthetic, hidden root: `tree.js` computes
one representative id per otherwise-disjoint blood lineage
(`TreeLogic.rootAncestors`) and adds one extra card, `EVERYONE_ROOT_ID`
(`"__everyone__"` — can't collide with a real slug, since
`storage.slugify()` strips every non a-z0-9 character server-side)
listing those ids as its `rels.children`. Rooting the chart there makes
it recurse down through every lineage in a single pass; the root's own
card is hidden via a `[data-id="__everyone__"]` CSS rule in `main.css`,
but the connector lines above each real branch still draw, reading as
one shared family rather than implying a fake shared ancestor.

**Picking the roots correctly was the actual difficulty.** A naive "every
person with no recorded parents" filter is wrong: it also catches anyone
who married into an otherwise-connected lineage but whose own parents
just were never recorded (a very common case, not a different family
branch). Including them as a *second*, independent root would draw their
married-in partner's entire descendant subtree a second time, for no
reason — since they'd already be pulled in automatically as their
partner's spouse once the partner's own (recorded) lineage is rooted.
`TreeLogic.rootAncestors(ids, parentsOf, partnersOf)` fixes this: a
parentless person only becomes an explicit root if *every* one of their
partners is *also* parentless (an unresearched-further couple, or no
partner at all); a parentless person whose partner has recorded parents
is excluded, since that partner's own branch will surface them via
`family-chart`'s existing automatic spouse-pairing. Couples where both
(or neither) qualify still dedupe to one representative via the existing
`coupleGroups`.

**Marriages that genuinely bridge two disjoint lineages still duplicate
by design** — a couple, and everyone below them, is drawn once per side,
because a family is a DAG (a child has two distinct parent lineages), not
a strict tree, and no single-root hierarchy can show both without
repeating the join point. `family-chart` treats this as a first-class
case (it flags every repeat past the first via `node.duplicate`, distinct
from `node.data.id`, which is never itself suffixed); `cardInnerHtml`
surfaces that flag as a small "also shown elsewhere" note so a repeated
card doesn't read as a different person. In practice this affects far
fewer people than expected: verified against a two-grandparent-branch
demo family, only the *shared children* (e.g. Milo, reachable as a real
`rels.children` entry from both his father's blood branch and his
mother's) duplicated — the married-in parents themselves (Papa, Maman)
each appeared exactly once, correctly positioned under their own birth
family, since `family-chart`'s spouse-pairing adds a partner as an
annotation card only, without re-walking into their ancestry a second
time.

The toolbar's existing hide condition (no button row at all when focus
has no recorded ancestors) is loosened slightly: "Everyone" is worth
showing whenever more than one root branch exists anywhere in the family,
even if focus personally has none. `viewLevel` gained a third shape
(the literal string `"all"`, alongside the existing numeric levels and
`0`) — `restoreSavedView`'s localStorage round-trip and `renderView`'s
level-clamping both had to account for it explicitly rather than assuming
a number.

No backend changes: `/api/tree` already returns the entire family graph
(every in-family person, not just those reachable from one focus), which
is exactly what building a merged dataset needs — this is a purely
client-side addition.

Tests: `tests/js/tree_logic_test.mjs` gained three `rootAncestors` cases
(the motivating bug fixed — a parentless person whose partner has
recorded parents is excluded; a couple where neither has recorded parents
dedupes to one root; an unpartnered parentless ancestor is always a
root). Manually verified end-to-end (Playwright, a seeded two-branch demo
family): the "Everyone" button renders every person in one canvas with
correct kinship labels and a visible connecting bar across both branches;
duplicate cards carry the "also shown elsewhere" note and both the
original and duplicate navigate to the correct person page on click; the
hidden root card is confirmed `display: none` while its connectors still
render; existing Direct line / branch levels are unaffected (same card
counts as before); phone-width viewport wraps the toolbar and scales the
chart the same way the existing levels already do, no new mobile-specific
work needed.

## Tests

Kinship label table (the fixture family), cycle rejection, partner
symmetry round-trip through the API, tolerant parsing of dangling slugs,
/api/tree contract shape (including friends and anchor-unset), person
page Family section rendering, tree page 200 + contains the vendored
script tags, feature fully invisible (no Family fieldset, no tree link)
when no links exist. Bare pytest green.

## Definition of done

Phone-width pass in all three themes: link up a three-generation family
of ~10 people through the editor pickers only; the tree renders with
portraits, expands a collapsed uncle branch, re-roots on a grandparent
and back; person pages show correct computed labels ("your uncle", "your
great-grandmother") and the free-text override still wins; JS disabled →
person pages still show the full Family section; zero external network
requests with the tree page open (the vendored bundle must be re-audited
by watching the network panel during pan/zoom/expand); hand-inspect one
person's index.md — the only new lines are the plain optional fields.

---

## Performance round: photo thumbnails and markdown parser reuse

Two contained optimizations found during a codebase-wide audit, no
behavior change beyond what's noted below.

**Dedicated avatar thumbnails.** `storage.save_image_to` (shared by F11's
photo pipeline) now generates a second, small copy alongside the existing
full-size re-encode: `photo-NNN.thumb.<ext>`, capped at
`THUMB_MAX_EDGE = 320` (vs. `MAX_IMAGE_EDGE = 2000` for the full photo),
same PNG-vs-JPEG-q85 rule as the full image. Before this, the small
avatar-style contexts — `.timeline__thumb` (72px/56px story-cover
thumbnails) and the `photo_thumb` macro's `.person-family__thumb`/
`.family-chip__thumb` (32px/24px) — were downloading the full 2000px
photo just to paint a tiny circle, real bandwidth waste on a mobile-first
app. `timeline.html` and `routes_pages._person_ref` now point at
`thumb_filename(...)` for those contexts only; every other photo usage
(story/person cover, book pages, epub, lightbox, the body of a story)
is untouched and still serves the full-size image.

Photos uploaded before this change have no `.thumb.` sibling on disk yet.
Rather than a migration, `_serve_media` (the shared story_media/
person_media handler) falls back to serving the full-size original when
a requested `.thumb.` filename doesn't exist on disk — the same "files
outlive app changes" tolerance the rest of storage.py already follows
elsewhere (e.g. `_parse_unlock`). `storage.thumb_filename` /
`original_filename_from_thumb` are the pure filename transforms behind
this; `_next_photo_number`'s `photo-*` glob already tolerates the new
`.thumb.` sibling since it matches the same leading `photo-NNN.` prefix.

**Markdown parser reuse.** `rendering.render_markdown` used to construct
a brand-new `markdown.Markdown()` instance (full extension chain,
including the story-image treeprocessor) on every single call — real
waste given `/book` and `/book.epub` call it once per readable story in a
loop. It now keeps one parser per thread in a `threading.local()` (not a
single shared module-global — a threaded production WSGI deployment must
never have two requests racing on the same parser's `media_base`/parse
state), resetting it between conversions via the documented `md.reset()`
API and updating the story-image treeprocessor's `media_base` in place
before each `.convert()` call.

Tests: `tests/test_storage.py` gained thumbnail-file assertions on the
existing JPEG/PNG upload tests plus a `thumb_filename`/
`original_filename_from_thumb` round-trip test; `tests/test_pages.py`
gained a `_serve_media` fallback-to-full-size test and a stronger
cover-thumbnail URL assertion; `tests/test_family_pages.py`'s family-thumb
test updated to expect the `.thumb.` URL; `tests/test_rendering.py`
gained a test that repeated calls with different `media_base` values
never leak into each other now that the parser is reused.

---

# Feature spec — F19: family accounts, admin approval, delegated writing

Multi-user accounts is one of the items README's "Ideas for later" lists as
deliberately out of scope, "if any of these become worth doing, they belong
here first, not as a surprise addition." This is that discussion, written up
before implementation the way F1 was. Same ground rule as F1: no accounts
system should make this feel less like a book and more like a web app with
users — restraint over features, still no comments/reactions/search/tags,
still one shared timeline, still plain files on disk, nothing here changes
that.

## Why this is a bigger deal than it sounds, and how the design resolves it

Storybook's whole design rests on: no database, one trust level, one shared
password, "book not blog." Real accounts pull against all three. That's not
a reason to avoid it, but it means the design should be the least new
machinery that satisfies the actual requirement, not a generic auth system
bolted on. Three choices carry that principle through the whole feature:

1. **Fully opt-in, off by default**, gated by `STORYBOOK_ACCOUNTS` — same
   pattern as `STORYBOOK_AUTHORS`/`STORYBOOK_BIRTHDATE`. A family that wants
   the one-shared-password simplicity forever just never sets it, and
   nothing about their install changes, ever.
2. **An account is not a new identity system — it's a login bolted onto an
   existing Person.** `people.py` already models "the cast of the book."
   Every account (admin or family) is required to bind to a Person, so "who
   can log in" and "who this book is about" stay the same graph instead of
   becoming two things an admin has to keep in sync.
3. **Still no database.** Credentials live in plain files under `stories/`,
   same as everything else — readable, backed up with everything else,
   survives the app being deleted. (A password hash is safe to sit in a
   plain file; the plaintext never is.)

## Roles

| Role | Bound to a Person? | Can do |
|---|---|---|
| **Admin** | Yes, always | Everything Family can do, plus: create accounts, bind them to a Person (existing or new), disable/re-enable accounts |
| **Family** | Yes, always | Full read/write on the whole timeline/tree/book — unchanged from today's single-password trust model, not a permissions system; manage their own password; (Phase 3) create/revoke their own delegated write-links |
| **Delegate** (Phase 3, write-link) | No — scoped to whoever granted the link | Submit one new story, attributed to the granting Person. Nothing else. |

Admin isn't a separate kind of identity, it's a capability flag on a
Person-bound account — in practice the person who deploys the app approves
themselves as the first admin and usually also writes stories.

**Permissions decision, stated explicitly since it's a values call and not
derivable from anything above:** once someone has an approved Family
account, they can edit/delete *any* story, exactly like today. The account
system answers who gets in the door and how they're attributed, not who can
touch what once they're in — a permission-walled model would be a bigger,
more blog-like feature than anything else in this app.

## Data model

`app/accounts.py`, same shape as `people.py`: pure functions taking the
people directory as their first argument, no hidden state.

```
stories/
  people/
    papa/
      index.md          # existing Person file, untouched
      account.json       # only exists if papa has an account
    milo/
      index.md            # a Person with no account.json is just a person —
                           # most people in the book never log in
```

Credentials live in a sibling file, not new `index.md` frontmatter keys:
`index.md` is read by every page render, kinship walk, and tree JSON build,
so keeping the password hash out of it shrinks the blast radius of any
future bug that logs or dumps a `Person`. Plain JSON, not YAML: this is
small structured data with no prose body, and stdlib `json` avoids leaning
on python-frontmatter's transitive PyYAML dependency for something new.
Hashing is `werkzeug.security` (`generate_password_hash`/
`check_password_hash`) — already installed transitively via Flask, so this
is one dependency avoided, not added.

```json
{
  "username": "papa",
  "password_hash": "scrypt:...",
  "role": "admin",
  "status": "active",
  "created_at": "2026-07-20T18:32:00",
  "approved_by": null
}
```

## Authentication & sessions

`auth.login()` grows a second mode selected by `STORYBOOK_ACCOUNTS`. Off:
untouched, single shared password. On: username+password, verified via
`accounts.verify_login`, setting `session["account_username"]`,
`session["person_slug"]`, `session["role"]`.

`login_required` re-checks the account's `status` from disk on every
request when accounts mode is on, rather than trusting the session cookie
alone — sessions here are client-signed with no server-side store, so a
disabled account must lock out immediately, not whenever its 90-day cookie
happens to expire. `admin_required` layers a role check on top.

**Bootstrap:** the first account has no admin to create it. `STORYBOOK_PASSWORD`
never logs anyone in once accounts mode is on — instead it's the invite
code required on the public request form (Phase 2), and the very first
request ever submitted auto-approves as admin instead of joining the
pending queue. This needed no separate bootstrap env var: already knowing
the shared password is already the proof-of-ownership the app needs.
(Phase 1, before the request form existed, used a simpler stopgap: the
shared password logged in directly as a one-time bootstrap admin session.
Phase 2 replaced that outright rather than keeping both paths alive —
see the Phase 2 round below.)

## Delegated write-links (Phase 3 — "give access to someone so they write
for them")

A family/admin account holder generates a share-to-write link (a
`secrets.token_urlsafe` bearer token, stored hashed) from their own account
page. Opening it sets a session scoped to submitting one story attributed to
the granting Person — deliberately *not* `session["authed"]`, so it's
structurally distinct from a real login and can't reach anything else in the
app. No username, no password, no admin approval to get one — matching "no
account access as such" literally. Revocable at any time by the person who
issued it or by an admin. Considered and rejected: a delegate-created
sub-login (reads like exactly what "no account access as such" rules out),
and literally sharing one's own login (no audit trail, revoking it logs the
owner out of their own devices too).

Two scope trims from the original idea, made for proportionality rather
than found necessary along the way: **no editing after submission** (a
multi-use link lets someone come back and write *another new* story, not
revise a previous one — tracking per-story edit authorization for a
one-shot contribution is real complexity for a marginal case, and the
person who granted the link can always fix a typo themselves afterward),
and **text-only, no photos** (the real editor's photo upload is a
multi-step JS flow built around a story already having an id to attach
images to; reusing it for a scoped delegate session was a much bigger lift
than the rest of Phase 3 combined). Both are easy to revisit later if the
text-only cameo-contribution case turns out not to be enough.

## Interaction with existing features

- **F1 Authors** (`STORYBOOK_AUTHORS`) is superseded automatically the
  moment `STORYBOOK_ACCOUNTS` is on (Phase 4): an account's bound Person
  becomes the author directly, with its own `author_color` replacing the
  env-config color. `STORYBOOK_AUTHORS` itself is never read in that mode
  — left set or unset, it makes no difference — so there's no forced
  migration step; an install that never turns accounts on keeps F1 exactly
  as it always was.
- **F14 People / F18 kinship-tree**: no changes. Accounts are additive
  metadata on Persons that already exist; `kinship.py`, `tree.js`, and the
  family-chart rendering stay completely account-unaware.
- Existing installs: with `STORYBOOK_ACCOUNTS` unset, zero behavior change,
  zero migration required, `story.author` strings keep rendering exactly as
  they do today.

## Security checklist

- `hmac.compare_digest` for the shared/bootstrap password (already the
  pattern), `check_password_hash`'s constant-time comparison for account
  passwords.
- `verify_login` hashes a dummy password on an unknown-username lookup so
  that path costs roughly the same CPU time as a real check, keeping
  username validity untimeable.
- Failed logins keep the existing `time.sleep(1)` throttle; a per-account
  lockout counter is a reasonable future addition but deliberately not a
  dependency like Flask-Limiter — one household, not internet scale.
- State-changing routes (create/disable account) are POST-only, relying on
  the existing `SESSION_COOKIE_SAMESITE="Lax"` — this app has no CSRF
  tokens anywhere today and F19 doesn't introduce a token system just for
  itself, but the stakes of a gap are higher now (CSRF could create/disable
  an account, not just re-submit an already-known password), worth
  revisiting if a request-based public flow (Phase 2) ships.
- Usernames are validated against a strict allowlist (`^[a-z0-9-]{3,32}$`),
  same spirit as `storage.is_valid_story_id`.

## Phasing

1. **Data model + `app/accounts.py` + admin/family login** (done). No
   public request flow yet — an admin creates every account directly, for
   dogfooding.
2. **Public request/approve flow** (done) — a "request an account" form
   gated by the shared password as an invite code, a pending queue, admin
   approve/reject binding to a Person.
3. **Delegated write-links** (done).
4. **F1 retirement path** (done) — `author_color` on Person,
   `STORYBOOK_AUTHORS` superseded automatically in accounts mode.

---

### Phase 1 implementation round

Built exactly as specified above, feature-flagged behind
`STORYBOOK_ACCOUNTS` (default off — every existing test and install is
unaffected; the whole suite passes with the flag never set).

- **`app/accounts.py`** (new): `Account` dataclass, `create_account`,
  `get_account`/`get_account_by_username`, `list_accounts`,
  `any_accounts_exist`, `is_username_taken`/`is_valid_username`,
  `set_status`, `verify_login` — as specified, JSON sibling files under
  `people/<slug>/account.json`.
- **`app/auth.py`**: `login()` branches on `ACCOUNTS_ENABLED` and whether
  any account exists yet (bootstrap); `login_required` re-validates account
  status from disk each request when accounts mode is on; new
  `admin_required` (404s a non-admin rather than revealing the admin
  section exists, consistent with this app having no 403 pattern anywhere
  else).
- **`app/routes_pages.py`**: `/admin/accounts` (list, admin-only),
  `/admin/accounts/new` (GET/POST — also the bootstrap admin's landing
  page; creating an account while bootstrapped upgrades the current
  session in place rather than requiring a second login),
  `/admin/accounts/<slug>/disable` and `/enable`.
- **Templates**: `login.html` grows a conditional username field (bootstrap
  mode shows the old password-only form with an explanatory note); new
  `admin_accounts.html` (list + enable/disable) and
  `admin_new_account.html` (bind to an existing unbound Person or create a
  new one, username/password/role); `base.html` nav gains an "Accounts"
  link, visible only to a logged-in admin when accounts mode is on.
- **`app/__init__.py`**: `STORYBOOK_ACCOUNTS=1` → `config["ACCOUNTS_ENABLED"]`,
  same fail-open pattern as the other optional `STORYBOOK_*` vars (no value
  is a hard requirement, no startup `RuntimeError` path needed since there's
  nothing to parse/validate at boot, unlike `STORYBOOK_AUTHORS`/
  `STORYBOOK_BIRTHDATE`).

Tests: `tests/test_accounts.py` (new) — the pure `app/accounts.py` API:
round-trip creation, username validation/lowercasing/uniqueness, password
length, disable/enable, `verify_login` for correct/wrong/unknown/disabled.
`tests/test_account_auth.py` (new) — the full HTTP flow: bootstrap login,
first-admin creation, shared password retiring afterward, family-account
login, 404 on admin routes for non-admins and for logged-out visitors,
binding to an existing unbound Person vs. creating a new one, duplicate-
username/no-person-selected validation errors, and the immediate-lockout
behavior (an already-active session is redirected to `/login` on its very
next request after an admin disables it, not after its cookie expires).
Manually verified end-to-end over HTTP (curl, a fresh `STORYBOOK_ACCOUNTS=1`
install): bootstrap → first admin → second (family) account → role-gating
→ disable → immediate lockout → re-login refused while disabled, all
matching the automated tests.

At the time, Phases 2-4 (the public request/approve flow, delegated
write-links, and F1 retirement) were not yet built — see their own rounds
below for what shipped since.

---

### Phase 2 implementation round

Built as specified, and **replaces** Phase 1's shared-password bootstrap
login outright rather than keeping both paths alive — once a public
request form exists, a second "or just type the shared password into
`/login`" bootstrap route would be redundant machinery and a second thing
to reason about securely. `auth.login()` is simpler after this round than
it was after Phase 1: no more bootstrap branch, no more session
self-upgrade mid-request — it always expects username+password when
accounts mode is on, full stop.

- **`app/accounts.py`**: new `PendingRequest` dataclass and
  `list_pending`/`get_pending`/`create_pending_request`/`reject_pending`/
  `approve_pending`/`is_username_reserved`, stored as one shared
  `stories/pending_accounts.json` (not one-file-per-request — a request
  queue is meant to be reviewed and cleared quickly, never expected to
  pile into the hundreds unnoticed, so a single small file is simpler than
  an index). These take `stories_dir`, not `people_dir` like the rest of
  the module — the queue lives at the stories root since a pending request
  has no Person to be a sibling of yet. `approve_pending` requires exactly
  one of an existing unbound Person slug or a new person's name, creates
  the Person if needed, writes the real `account.json`, and removes the
  request from the queue in the same call.
- **`app/auth.py`**: `login()` loses the bootstrap branch entirely —
  `STORYBOOK_PASSWORD` now only matters when accounts mode is *off*. A
  `no_accounts_yet` hint (still computed, just for copy on the login page)
  is all that's left of the old bootstrap flag.
- **`app/routes_pages.py`**: `/request-account` (GET/POST, public — 404s
  when accounts mode is off) creates a pending request after checking the
  invite code with `hmac.compare_digest`; auto-approves as admin inline
  when `accounts.any_accounts_exist()` is still false. `/admin/accounts`
  now also lists the pending queue. `/admin/accounts/pending/<username>`
  (GET/POST, admin-only) reviews and approves one request;
  `/admin/accounts/pending/<username>/reject` removes it. The
  bind-to-existing-or-new-person validation that both this and
  `admin_new_account` need was pulled into a shared `_bind_and_create`
  helper rather than duplicated.
- **Templates**: new `request_account.html` (the public form, plus a
  submitted/auto-approved confirmation state instead of redirecting away)
  and `admin_review_pending.html`; `admin_accounts.html` gained a pending
  section above the accounts list; the "pick an existing Person or create
  one" fieldset used by both `admin_new_account.html` and
  `admin_review_pending.html` was pulled into a `person_picker` macro in
  `_macros.html` rather than duplicated a third time; `login.html` lost
  its bootstrap-specific form branch and gained a "request one"/"request
  the first one" link instead.

Tests: `tests/test_accounts.py` gained the pending-request API — round
trip, validation (bad username/short password/blank name), uniqueness
enforced *across* pending and bound accounts together, approve binding to
a new vs. existing person, reject, and the "exactly one of person_slug/
new_person_name" contract. `tests/test_account_auth.py`'s bootstrap tests
were rewritten around `/request-account` (the old login-based bootstrap
helper no longer exists): first request auto-approves as admin and
creates its Person; a second request goes to the pending queue instead;
wrong invite code and duplicate-pending-username are rejected; admin
approve (both binding shapes) and reject; a non-admin family account gets
404 reviewing a pending request; the shared password never logs anyone in
once accounts mode is on, before or after any account exists. Manually
verified end-to-end over HTTP (curl and Playwright, a fresh
`STORYBOOK_ACCOUNTS=1` install): first request auto-approves as admin →
shared password stops working → second request queues → admin sees it on
`/admin/accounts` → approves, binding to a brand-new Person → that account
logs in and is correctly 404'd from admin routes → a third request is
rejected and disappears from the queue.

At the time, delegated write-links (Phase 3) and F1 retirement (Phase 4)
were not yet built — see their own rounds below for what shipped since.

---

### Phase 3 implementation round

Built with the two scope trims noted above (no post-submission editing,
text-only). New standalone module rather than folding into
`app/accounts.py`: a write-link isn't a credential or an identity, it's a
capability token with its own lifecycle (expiry, single-use, revocation,
usage tracking) — different enough in shape to earn its own file.

- **`app/write_links.py`** (new): `WriteLink` dataclass and
  `create_link`/`list_links`/`get_link`/`revoke_link`/`mark_used`/
  `find_by_token`/`is_link_valid`/`list_all_active`, stored as
  `people/<slug>/write_links.json`. Tokens are hashed with plain SHA-256
  (`hashlib`, not `werkzeug.security`'s slow password hash) — a
  `secrets.token_urlsafe(32)` token already has ~192 bits of entropy, so a
  fast deterministic hash is the right tool, the same reasoning GitHub/GitLab
  use for personal access tokens. Each link also gets its own non-secret
  `id` (`secrets.token_hex(8)`) used everywhere a link needs to be
  referenced (revoke URLs, admin lists) so the real bearer token is never
  echoed back anywhere after the moment it's created.
- **`app/auth.py`**: new `delegate_required`, parallel to `login_required`/
  `admin_required` — checks `session["delegate_person_slug"]`/
  `["delegate_link_id"]` and re-validates the link's status from disk on
  *every* request (not just at the initial `/w/<token>` hit), so a
  revoked/expired/used-up link locks out an already-open delegate session
  immediately, same reasoning as the disabled-account check from Phase 1.
- **`app/routes_pages.py`**: `/account/write-links` (GET/POST, any logged-in
  account — create a link, see history, revoke); `/account/write-links/
  <person_slug>/<link_id>/revoke` (owner or admin only); `/w/<token>`
  (public — validates and opens a delegate session, `session.clear()`-ing
  first so a real account holder accidentally opening their own share link
  can't end up with mixed session state); `/w/write` (delegate-only — the
  entire delegate experience, one form, no nav out).
- **`admin_accounts.html`** gained a third section, "Active write-links"
  (only currently-valid ones — revoked/expired/used links aren't
  actionable and would just be dashboard noise), so an admin can shut down
  a link they didn't issue themselves.
- **Templates**: `account_write_links.html`, `delegate_write.html`,
  `delegate_thanks.html`, `write_link_invalid.html` — all deliberately
  thin, no site-nav links out of the delegate ones (they inherit
  `base.html`'s nav, which already hides every link behind
  `session.get('authed')`, and a delegate session never sets that, so this
  needed no special-casing in the shared template).
- A delegate-created story's `author` field is set to the granting
  Person's name directly, bypassing F1's `STORYBOOK_AUTHORS`-membership
  check entirely (that check lives in the `/api/stories` route layer, not
  in `storage.create_story` itself, and this flow calls the latter
  directly) — it renders as a plain neutral-color byline if the name isn't
  a configured F1 author, exactly the graceful fallback F1 already
  documented for a renamed/removed author.

Tests: `tests/test_write_links.py` (new) — the pure `write_links.py` API:
round-trip creation, expiry math, `is_link_valid`'s three failure modes
(revoked/expired/used-up-single-use) versus a multi-use link staying valid
after one use, `find_by_token` only matching a real token, and
`list_all_active` excluding everything not currently valid.
`tests/test_write_link_routes.py` (new) — the full HTTP surface: creating a
link and seeing its URL exactly once, single-use-checkbox semantics, owner
and admin revocation, a non-owner family account correctly 404'd trying to
revoke someone else's link, the `/w/<token>` → `/w/write` handoff, a
submitted story landing in `storage.list_stories` with the right author, a
single-use link refusing a second submission (and the token itself going
dead), a multi-use link accepting a second story, revoking a link locking
out an already-open delegate session immediately, a delegate session unable
to reach any real app route, and opening a link clearing a pre-existing
real login session. Manually verified end-to-end (curl and Playwright,
screenshots): create a labeled single-use link → open it in a fresh
browser context → submit a story → it appears correctly on the real
timeline with the right author byline → re-opening the same link shows
"isn't valid anymore" → the delegate's nav bar never showed anything but
the app title, confirming the scoping is structural (inherited from
`base.html`'s existing `authed` guard) rather than something that had to
be bolted on per-page.

At the time, F1 retirement (Phase 4) was not yet built — see its own round
below for what shipped since, and F19 is now fully built out end to end.

---

### Phase 4 implementation round

Built as specified: real accounts supersede F1 the moment
`STORYBOOK_ACCOUNTS` is on, with no config migration required and zero
change to F1 itself when accounts mode stays off.

- **`app/people.py`**: `Person` gains `author_color: Optional[str]`, an
  optional hex color, same validation shape
  (`is_valid_author_color`/`_parse_author_color`) and "unset = neutral,
  malformed on disk = drop to None" tolerance as every other optional
  field here. Threaded through `create_person`/`update_person`/
  `_write_index` exactly like `gender` — `None` leaves it unchanged on
  update, `""` clears it.
- **`app/routes_api.py`**: `_validate_author` now short-circuits to
  `(None, None)` whenever accounts mode is on, *before* even looking at
  `STORYBOOK_AUTHORS` — a client-submitted `author` is never trusted once
  real identity exists, closing what would otherwise be a spoofing gap (a
  family account claiming to have written as someone else). A new
  `_author_name_for_current_account()` resolves the actual author from
  `session["person_slug"]` and is applied only in `create_story` — never
  in `update_story`, so editing a story can never silently reassign who
  wrote it. `_validate_author_color`, mirroring `_validate_gender` exactly,
  wired into both person create/update handlers.
- **`app/routes_pages.py`**: `_authors_and_colors()` branches on
  `ACCOUNTS_ENABLED` — in accounts mode, "authors" becomes every Person
  with a bound account (not `STORYBOOK_AUTHORS`), colored by their own
  `author_color` or a new `DEFAULT_AUTHOR_COLOR` fallback. That fallback
  matters because `timeline.html`'s legend chip renders
  `--author-color: {{ a.color }}` unconditionally (unlike the per-story
  byline lookups, which already guard on the color being present) — every
  entry handed to it must have a real value, and a freshly-approved
  account has no `author_color` yet until someone visits their person
  page. Reusing this one function's output is what let every other F1
  render path (timeline legend/dots, book, story byline) work in accounts
  mode with *zero* template changes.
- **Templates**: `editor.html`/`instant.html`'s existing
  `{% if authors %}` guard around the chip picker gained `and not
  config.ACCOUNTS_ENABLED` — picking an author from a hand-picked list
  makes no sense once attribution is automatic from the session.
  `person_editor.html` gained a native `<input type="color">` for
  `author_color`, shown only in accounts mode.
- **`app/static/js/editor.js`**: one new line reading the color input into
  the shared story/person payload builder — no other JS changes needed.
  The author-chip-picker JS (`author-chips.js`) already treated a missing
  root element as "no chips" gracefully (empty array, `getSelected()`
  stays `null`), from before this feature existed, so hiding the chip
  markup server-side was sufficient on its own; the client keeps sending
  an empty `author` field harmlessly, and the server ignores it anyway.

Tests: `tests/test_people.py` and `tests/test_family_api.py` gained
`author_color` round-trip/validation/clear-on-empty-string/malformed-
frontmatter-tolerance cases, mirroring the existing `gender` ones exactly.
`tests/test_accounts_authorship.py` (new) covers the actual behavior
change: creating a story auto-attributes to the logged-in account;
a spoofed client-submitted `author` is silently overridden; instants get
the same treatment; editing a story never reassigns its author even when
a different account holder makes the edit; the timeline legend shows
account holders with the default color when unset and a person's own
color once they set one; the chip picker is absent from both the story
and instant editors in accounts mode; the color picker only appears on
the person editor in accounts mode; and — the regression guard for
everything above — F1's picker and validation are completely unaffected
on an install that never turns `STORYBOOK_ACCOUNTS` on. Manually verified
end-to-end (Playwright): created a story with no chip picker visible,
confirmed it auto-attributed to "Papa," set a custom byline color through
the actual JS-driven person editor (not just the API directly), and
watched that exact color render on the real timeline's legend and byline.

F19 is now fully built: admin/family accounts, the public request/approve
queue, delegated write-links, and real per-account authorship superseding
F1 — all gated behind one `STORYBOOK_ACCOUNTS` flag, every install that
leaves it unset unaffected by any of it.

---

### Follow-up round: self-service password change and role management

Two gaps found by explicitly auditing "is everything actually reachable
from the web UI, with no need to hand-edit `account.json`" after F19
shipped: there was no way to change your own password, and no way to
promote/demote an existing account's role. Both required manual file
editing to work around — exactly what this whole module exists to avoid.
Closed in this round, plus one related footgun caught while building the
fix (see below).

- **`app/accounts.py`**: `Account` gains `session_version: int = 0`.
  `set_password(people_dir, person_slug, new_password)` re-hashes and
  **bumps** `session_version` — the point of changing a password is that
  every other already-open session for that account stops working too,
  not just that a new password now also happens to log in. `set_role`
  promotes/demotes, validating the role like `create_account` already
  does. Both `set_role` and the pre-existing `set_status` gained a shared
  `_active_admin_count()` guard: **neither will demote nor disable the
  last active admin.** That specific footgun wasn't part of the original
  ask — it surfaced while writing `set_role` (a demote is symmetrically
  as dangerous as a disable, and `set_status` already had the exact same
  unguarded lockout risk from Phase 1) — fixed in the same round rather
  than filed as a separate gap, since it's the identical failure mode
  this whole round exists to close.
- **`app/auth.py`**: `login_required`'s existing per-request re-check
  (previously just account status) now also compares
  `session["session_version"]` against the account's current value, so a
  password change invalidates other sessions on their very next request —
  same reasoning and same code path as the disabled-account check from
  Phase 1, just one more field. New `set_session_for_account()` factors
  out the "populate a fresh session" logic `login()` already had, so the
  self-service password-change route can refresh *its own* session's
  `session_version` after changing it — without that, the very session
  that requested the change would immediately lock itself out on its next
  request, which is not what "change your own password" should do to you.
- **`app/routes_pages.py`**: `/account` (a small hub, replacing the bare
  "Write links" nav link with "Account"), `/account/password`
  (self-service — requires the current password, matching password-change
  UX conventions generally, and refreshes the session as above),
  `/admin/accounts/<slug>/reset-password` (admin-set, no current password
  needed — the only account-recovery path this app has, since it has no
  email), `/admin/accounts/<slug>/role`. `admin_disable_account` — which
  could previously crash with an unhandled 500 the moment `set_status`
  gained its guard — now catches `ValueError`/`FileNotFoundError` and
  flashes instead, same pattern every other admin action here already
  used.
- **Templates**: new `account_home.html`, `account_password.html`,
  `admin_reset_password.html`; `admin_accounts.html`'s account rows gained
  an inline role `<select>` + "Set" button and a "Reset password" link
  alongside the existing disable/enable action.

Tests: `tests/test_accounts.py` gained `set_password`/`set_role` coverage
(hash change, session_version bump, validation) and the last-admin guard
for both `set_role` and `set_status` (including a disabled admin not
counting as "remaining"). `tests/test_account_self_service.py` (new)
covers the full HTTP surface: wrong-current-password and mismatched-
confirmation rejections, a successful change keeping the *current* session
logged in while logging out a *second* open session for the same account,
admin reset without needing the old password (and it also invalidates
open sessions), non-admins 404'd from both admin routes, and — the
regression tests for the crash this round fixed — demoting or disabling
the only admin redirects with a flash message rather than a 500. Manually
verified end-to-end (Playwright): changed a password through the actual
form and confirmed the session survived; promoted a family account to
admin, demoted the original admin now that a second one existed, then
attempted to demote the last remaining admin and watched the guard
message render correctly instead of crashing.

### Follow-up round: re-link an account to a different person

A gap surfaced by real deployment, not by design review: `/request-account`
auto-approves the very first submitted request as admin, and since there's
no admin yet at that point to pick from the family, it always binds the
new account to a brand-new Person built from the display name
(`request_account`'s `new_person_name=pending.display_name`) — even when
the real family member already had a Person page from before accounts
were turned on. Result: a duplicate Person, with no way to fix it short of
hand-editing `account.json`.

- **`app/accounts.py`**: `set_person(people_dir, person_slug,
  new_person_slug)` moves an account's `account.json` from one Person's
  folder to another's — `account.person_slug` is reassigned and the file
  rewritten at the new path via the existing `_write_account`, then the
  old path is unlinked. Deliberately never deletes the old Person itself
  (this app has no person-deletion machinery anywhere, by design — see
  the "book, not blog" restraint in `CLAUDE.md`); it's simply left
  unbound afterward, same as any family member who never gets an
  account. Raises `FileNotFoundError` for an unknown source/target slug,
  `ValueError` if the target Person already has its own account, and is
  a no-op when the two slugs match.
- **`app/routes_pages.py`**: `admin_accounts()` now also collects
  `unbound_people` (Persons with no `account.json`); new
  `/admin/accounts/<slug>/link-person` (admin-only, POST) calls
  `set_person` and flashes on error, matching every other admin account
  action's error-handling shape. If the account being re-linked is the
  *current* session's own account (true for the common case — the
  bootstrap admin fixing their own duplicate), it updates
  `session["person_slug"]` in place so the session doesn't keep pointing
  at the stale Person until the next login; unlike a password change,
  nothing else about the session (role, username, session_version)
  changes, so a full `set_session_for_account()` reset isn't needed here.
- **`app/templates/admin_accounts.html`**: each account row gets a second
  inline form (visible only when at least one unbound Person exists) — a
  `<select>` defaulted to the currently-linked Person plus every unbound
  Person as alternatives, and a "Link" button.

Tests: `tests/test_accounts.py` covers `set_person` moving the file
correctly, the same-slug no-op, rejecting a target that already has an
account, and rejecting unknown slugs. `tests/test_account_self_service.py`
covers the route: an admin re-linking their own just-bootstrapped account
onto a pre-existing Person (the motivating scenario, reproduced end-to-end:
bootstrap, create a second "real" Person, re-link, confirm the old
duplicate has no account and the new Person does, and the session stays
logged in against the new Person), the already-has-an-account rejection,
and non-admins 404ing.

---

## UI audit round: nav overflow, admin row overflow, book cover frame

A user report ("top bar buttons getting out of scope") drove a full
manual/automated pass over every page, at six viewport widths (360px to
1440px) and both themes, using a seeded demo family with deliberately
adversarial content (a hyphenated long name, a long friend name, a long
custom `STORYBOOK_TITLE`) rather than the short defaults every earlier
round happened to test with. Three real bugs found and fixed, all
CSS-only:

- **`.site-nav__actions` had no `flex-wrap`.** F19 added two more nav
  links ("Accounts", "Account"), which — combined with the pre-existing
  "People", "+ New story", "+ Instant" — pushed the row's total width
  past what fits at phone widths. `.site-nav` itself already wraps
  between the brand row and the actions row, but the actions row's own
  five items had no fallback once *they* didn't fit on one line, so the
  last two buttons were pushed off-screen rather than wrapping to a
  second line. This is the bug reported. Fixed by giving
  `.site-nav__actions` the same `flex-wrap: wrap` every other
  multi-button row in this app already uses (`.site-nav`,
  `.tree__views-row`, `.admin__row`), plus `justify-content: flex-end`
  so a wrapped second line still reads as right-aligned rather than
  snapping to the left edge.
- **`admin_accounts.html`'s "Link" person-picker `<select>` had no width
  constraint.** Its options are real person names (arbitrary length,
  unlike the fixed-length "Admin"/"Family" role `<select>` next to it),
  so a longer name sized the native control past the available row
  width — flexbox's default `min-width: auto` stops a flex item
  shrinking below its content size even inside an already-wrapping
  parent (`.admin__row` wraps fine, but a single overlong child can't
  shrink to make room for wrapping to help). Fixed with `min-width: 0`
  on both the form and the select, plus `max-width` +
  `text-overflow: ellipsis` so a long name truncates instead of
  stretching the row.
- **The book cover's decorative rope frame (`book-frame.jpg`) has a much
  tighter text-safe interior than its CSS `inset` assumed**, and only
  the title had any responsive sizing — the date range and author line
  were fixed-size regardless of viewport, so they hit their tightest
  relative fit exactly on narrow screens. Measured the image's actual
  rope-free interior directly (sampling pixel rows/columns in Python via
  Pillow for "cream vs. rope" color, not eyeballing) rather than guessing
  at percentages: horizontally ~18.3%–20.7% inset, vertically
  ~14.5%–16.2%, both narrower than the previous `inset: 20% 13%`.
  Verified the touching wasn't a narrow-viewport-only regression — the
  default short "Storybook" title never touches at any width, but a
  longer custom title (the exact example `STORYBOOK_TITLE="Le livre de
  Milo"` given in `.env.example`) touched the border even on a 1200px
  desktop viewport, so this was a real gap for anyone using that
  documented customization, not an artifact of stress-testing. Fixed
  `inset: 22% 20%`, gave `.book-cover__range` and `.book-cover__authors`
  their own `clamp()` responsive font-sizes (previously only
  `.book-cover__title` had one) so every line shrinks together with the
  frame instead of just the title, and trimmed the title's own clamp
  ceiling (2.25rem → 1.75rem) so it keeps a visible margin from the rope
  instead of exactly filling its box at the largest size.

No template or JS changes — every fix lives entirely in `main.css`.
Verified via an automated Playwright sweep (108 checks: 18 pages × 6
viewport widths, checking `document.documentElement.scrollWidth` for
horizontal overflow and flagging any `.site-nav` descendant whose
bounding box crosses the viewport edge) going from 36 flagged checks
before the fixes to 0 after, plus manual screenshot review of every page
in both themes and a pixel-level before/after comparison of the book
cover. `pytest` (660 tests) and `ruff check .` unaffected, as expected
for a CSS-only change.

---

## Whole-codebase dedup round

A follow-up to the UI audit above: a broader sweep for duplication
accumulated across the F19 accounts rounds and the tree "Everyone" view,
in the spirit of the earlier "Dedup" rounds. Three findings, all verified
against the full suite before and after:

- **`app/routes_pages.py`: a real bug, found via the duplication itself.**
  `admin_disable_account`, `admin_set_role`, and `admin_set_account_person`
  all shared the same shape — call an `accounts.py` mutator, catch
  `(ValueError, FileNotFoundError)`, flash, redirect to `/admin/accounts`
  — but `admin_enable_account`, the fourth route in the same family,
  called `accounts.set_status(...)` directly with no error handling at
  all. `POST /admin/accounts/<unknown-slug>/enable` would raise an
  unhandled `FileNotFoundError` straight into a 500, the exact crash the
  F19 follow-up round had already fixed for the *disable* route but never
  revisited for *enable*. New `_admin_mutate_account(person_slug,
  mutator, *args, on_success=None)` gives all four routes the shared
  shape (the `on_success` hook covers link-person's extra "sync the
  caller's own session" step), closing the gap as a side effect of
  removing the duplication rather than as a separate fix. New regression
  test: `test_enabling_an_unknown_account_fails_gracefully_not_a_500`.
- **`admin_accounts.html`: four identical single-button POST forms**
  (Reject/Disable/Enable/Revoke — `<form method="post" action="...">
  <button>Label</button></form>`) were hand-written inline instead of
  using `_macros.html`, which every sibling admin template already
  imports. New `action_button_form(action_url, label)` macro; visually
  verified identical rendering before/after.
- **Test helper triplication.** `_bootstrap_admin`, `_login`, and
  `_people_dir` — byte-identical, ~143 call sites total — were
  copy-pasted across `test_account_auth.py`, `test_account_self_service.py`,
  `test_write_link_routes.py`, and `test_accounts_authorship.py`, one
  pair added fresh in each F19 round rather than reused from the last.
  `test_account_auth.py`'s own `_bootstrap_admin` was already just
  `_request_account(...)` with its defaults — the two were never
  actually different functions, just written twice. Moved all four
  (`_people_dir`, `_request_account`, `_bootstrap_admin`, `_login`) to
  `tests/conftest.py` as plain module-level functions (not
  `@pytest.fixture`s — they take an explicit `client` argument rather
  than needing pytest's injection) and imported them into each file via
  `from tests.conftest import ...`, matching the existing implicit-namespace-package
  import style (`tests/` has no `__init__.py`; `pythonpath = ["."]` in
  `pyproject.toml` already makes `from tests.conftest import X` work).
  Deliberately left every call site untouched — the ~143 calls to
  `_bootstrap_admin(...)`/`_login(...)` didn't need to change at all,
  since the imported names keep their original identifiers; only the
  definitions moved. `people_dir` already existed as a *fixture* in
  conftest.py for the plain `stories_dir`-based tests — deliberately
  didn't try to unify it with the accounts files' `_people_dir(app)`
  plain function despite the overlap, since that would mean touching
  every one of those ~143 call sites' function signatures for a
  same-value, different-shape rename; not worth the regression risk for
  a test-only readability win.

`pytest` (661 tests, +1 for the new regression test) and `ruff check .`
green throughout; the test-helper move was verified as a pure
relocation by running the full suite immediately after, with no other
changes in the same commit.

## Fresh-eyes audit round: a stored-XSS regression, a stale doc, an admin-bootstrap race

A from-scratch read of the whole codebase (no prior context on this
project), looking for anything a first pass would miss. Three findings,
the first a real vulnerability, all fixed and covered by regression tests:

- **Stored XSS via write-links, verified end to end.** `render_markdown()`
  passes raw HTML straight through, and every template renders the result
  with `{{ body_html|safe }}`. `REVIEW.md` explicitly accepted this:
  "Raw HTML in markdown is rendered (`|safe`). Acceptable: the only author
  is the trusted password-holder. Do not add a sanitizer dependency." That
  held until F19 Phase 3 added delegated write-links — a bearer link any
  account holder can hand to someone with **no account at all** ("no
  account access as such") to submit exactly one story. The delegate's
  submission was never distinguished from a trusted author's before
  reaching `render_markdown`, so a write-link holder could plant
  `<script>...</script>` in a story body and have it execute unescaped in
  whichever family member or admin later opened it — a real privilege
  path from "someone handed a share link" to "runs script in an admin's
  authenticated session." Reproduced live with the test client (bootstrap
  admin → create a link → submit a story containing a `<script>` tag as an
  anonymous delegate → load the story as the admin → raw tag present in
  the response) before fixing it. Fixed narrowly, without touching the
  rendering pipeline trusted authors rely on (REVIEW.md's "do not add a
  sanitizer dependency" stands for everyone else): new
  `_neutralize_html()` in `routes_pages.py` escapes `<`/`>` in the
  delegate's submitted body before it ever reaches `storage.create_story`,
  applied only on the `/w/write` path. Markdown syntax never needs a
  literal `<`/`>`, so this can't break normal formatting for that flow.
  New regression test:
  `test_delegate_submission_cannot_inject_raw_html`.
- **Stale doc.** `README.md`'s backup section still said "the app's 32 MB
  upload limit" — `MAX_CONTENT_LENGTH` was raised to `128 * 1024 * 1024`
  a while back (see the Performance round above) for long voice memos,
  and the 413 handler's own message was updated at the time, but this one
  README sentence never was.
- **TOCTOU race in first-admin bootstrap.** `request_account()` did
  `auto_approved = not accounts.any_accounts_exist(...)` then a separate
  `accounts.approve_pending(...)` call. Two people who both know the
  invite code and submit within the same instant, before any account
  exists yet, could both observe "no accounts yet" and both auto-approve
  as admin — breaking the documented "the very first request ever
  submitted is special" invariant. New `accounts.approve_if_first()`
  does the check-and-act under a module-level `threading.Lock`, closing
  the window (the app runs as a single process under waitress by
  default, so an in-memory lock is sufficient — this doesn't cover a
  hypothetical multi-process deployment, which isn't how this app is
  deployed). New regression test:
  `test_approve_if_first_only_approves_once_for_two_simultaneous_requests`.

`pytest` (663 tests, +2) and `ruff check .` green throughout.

---

## "Everyone" round 2 — a real family graph, not a merged hourglass

Real dogfooding feedback on the previous round's "Everyone" view: on an
actual (not toy-demo) family, it "duplicates people" badly enough to be
confusing. Reproduced with a deliberately messy test family (two
remarriages — Papa's and Maman's each — plus a re-married uncle, half-
siblings on both sides) rather than guessing: the old implementation drew
**Papa, Maman, and Milo each twice**, not just the one bridging child the
first round's simpler test family had led me to expect. Investigated
whether `family-chart` (the vendored library) had a config option to
suppress this — it doesn't; the one internal flag that looked promising
(`one_level_rels`, found by reading the vendored source) turned out to be
a narrow special-case switch for an interactive "add relative" UI mode,
and forcing it on for normal rendering collapsed the chart to almost
nothing. This isn't a bug in how it was used: `family-chart` is
fundamentally a single-root hourglass pedigree renderer, and a real
family with remarriages is a graph, not a tree — a single hierarchy
rooted anywhere will always duplicate whoever bridges two otherwise-
disjoint branches. Assessed three options with the user (keep the chart
and just visually de-emphasize duplicates; promote the already-built
print-only generation outline to the primary on-screen view instead of a
chart, trading the graph look for a guaranteed-zero-duplication list; or
build a real graph layout from scratch) — chose the third: a genuine
family-graph chart where every person appears exactly once, replacing
`family-chart` entirely for this one view (Direct line and the
branch-level panels are untouched, still `family-chart`, since they were
never the problem — they deliberately show one branch/pedigree at a
time and never had this failure mode).

### The layout: `app/static/js/tree-graph-logic.js`

A new, dependency-free, unit-tested-in-isolation module (matching
`tree-logic.js`'s existing UMD pattern), computing a DAG layout with no
external layout library — `d3` (already vendored) is used only for pan/
zoom in the renderer, not for this math:

- **`computeLayers(ids, parentsOf, partnersOf)`** — every person's
  generation row: 0 for anyone with no recorded parents, otherwise one
  more than their deepest parent's layer (the standard "longest path
  from a root" DAG layering — deliberately not `kinship.py`'s anchor-
  relative `generation_offset`, which needs a reachable path to one
  anchor and returns `None` otherwise; this needs a definite row for
  *every* in-family person, anchor or not). Partners are then pulled to
  the same layer as each other to a fixed point — a couple reads as one
  generation on paper even when one side's ancestry wasn't researched as
  far back, and pulling a partner down can cascade to pull *their* own
  children down a layer too (a prior-marriage child who'd otherwise land
  on the same row as their own parent). Bounded by a `MAX_LAYERS` safety
  cap, same reasoning as `tree-logic.js`'s `MAX_LEVELS` — never expected
  to bind on real data, just a guard against hand-edited/corrupted
  `parents` edges.
- **`coupleUnits(rowIds, partnersOf)`** — groups a row into ordering
  units along partner links. The actual difficulty here, found by
  building the naive version first and looking at the result: a person
  with two partners in the same row (a remarriage) must end up in the
  *middle* of their unit (`Ex-Anne — Papa — Maman`), not with both
  partners bunched on one side — otherwise Ex-Anne and Maman render
  adjacent to each other despite never having been a couple. Fixed by
  finding each row's partner-subgraph connected components, then walking
  a simple-path component from one of its ends (a degree-≤1 node) rather
  than a plain DFS; a component with someone in 3+ partnerships within
  the same row (rare) falls back to a best-effort traversal order,
  without the every-neighbor-is-a-couple guarantee.
- **`orderRows(...)`** — the standard (heuristic; true crossing-minimal
  layout is NP-hard) Sugiyama barycenter method: each row initially
  ordered by its couple-units' input order, then a few refinement passes
  alternating "order by parents' positions" (top-down) and "order by
  children's positions" (bottom-up), converging quickly for graphs this
  size.
- **`groupChildrenByParents`** / **`partnerPairs`** — the edges to draw:
  siblings sharing a parent-set share one drop-line from the couple
  instead of each redrawing their own (and correctly split into separate
  groups for half-siblings, who share only one parent); a person with
  two partners produces two separate partner-pairs, never a 3-way group.
- **`layoutFamily(...)`** ties it together: `{positions: {[id]: {layer,
  x}}, partnerEdges, parentEdgeGroups}`. `x` is a row-relative integer
  rank, not a pixel or global coordinate — converting that to a pixel
  position is the renderer's job.

Tests: `tests/js/tree_graph_logic_test.mjs` (13 cases) — layer assignment
including the partner-pull-down fixed point, `coupleUnits`' remarriage-
chain ordering (asserting every rendered neighbor is a real partner, not
just checking the set of members), parent/child grouping including
half-siblings, and the full pipeline against both the motivating blended
family (asserting `Object.keys(positions).length === ids.length` — the
actual "no duplication" guarantee, plus that no two people on the same
layer share an `x`) and a plain two-branch family as a regression
baseline. Wired into `pytest` via `test_tree_logic_js.py` (skips without
`node`, same as the existing JS test wiring).

### The renderer: `renderFamilyGraph` in `tree.js`

Same architectural split `family-chart` itself uses — SVG for the
connector lines, plain HTML `<div>`s for cards (photos, text-overflow
ellipsis, hover — "for free" via ordinary CSS) — rather than
`<foreignObject>`, which has known cross-browser quirks. Both are
children of the mount element and share one `d3.zoom` transform, applied
manually to each on every `"zoom"` event (`svg`'s group via SVG
`transform`, the cards `<div>` via CSS `transform: translate() scale()`)
since they're separate DOM subtrees, not one containing the other.
Auto-fits to the container on load (scale/translate computed from the
laid-out content's pixel bounds vs. the container's `getBoundingClientRect()`,
capped at 1x so a small family never renders oversized) and offers the
same Recenter button pattern the other views already have — reusing the
existing `.tree__recenter-btn` class outright, and generalizing
`installMapBackground(mountEl, svg, view)` (previously hardcoded to
family-chart's `svg.main_svg`/`g.view` structure) to accept the SVG/
pan-zoom-group elements as parameters, so both this renderer and
`createChartInstance` can share it. Parent-child edges draw one shared
trunk from a couple's (or single parent's) midpoint, branching to each
child. Clicking a card navigates to that person's page — no mini-tree
re-root corner icon here (that's `family-chart`'s widget); re-rooting
elsewhere is one click away via Direct line.

`app/templates/tree.html` gained a `<script>` tag for the new
`tree-graph-logic.js`, loaded before `tree.js`. New CSS
(`.tree-graph`/`.tree-graph__*`) mirrors the existing `.f3-card-*`
visual language (cream card, gold focus ring, serif name, small-caps
kinship line, dashed rope-colored connectors — solid for partner links,
so a marriage reads differently at a glance from a generation
drop-line) but under fresh class names, since this view no longer uses
`family-chart` or its `.f3`-scoped CSS at all. `.tree-graph` also
carries `.tree__chart` for the shared container chrome (leather/
parchment background, border, height) it still has in common with the
other views.

### Cleanup and a caught mistake

The old merge-root approach's `EVERYONE_ROOT_ID` synthetic card, its
`[data-id="__everyone__"] { display: none; }` CSS, and the "all"
branch's family-chart data-splicing in `renderChartArea` are gone
entirely. While removing what looked like the matching duplicate-badge
CSS (`.f3-card-duplicate`), realized it was about to delete something
still needed: `cardInnerHtml`'s `node.duplicate` handling is
`family-chart`'s own general pedigree-collapse flag (e.g. a first-cousin
marriage putting the same grandparent on two lines of one person's
ancestry *within a single Direct-line or branch-panel chart*) — nothing
to do with the old Everyone hack, and still load-bearing for those
unchanged views. Restored it (re-worded to describe what it's actually
for now) before it shipped as a real regression.

Tests: `pytest` (664, +1 for the new JS-wiring test) and `ruff check .`
green. Manually verified (Playwright): the blended test family renders
17 cards for 17 people (zero duplication, vs. the old 20-for-17), click
navigation and Recenter both work, panning drags correctly, no
regression to Direct line/branch panels (unchanged card counts, no
console errors) or to a plain non-blended family (13-for-13, still
clean), no horizontal overflow on a 390px viewport, and correct
rendering in dark theme.

## "Everyone" round 3 — connected-component clustering

More dogfooding feedback, this time on the round-2 graph itself: an
in-law with no recorded parents of their own — "the husband of my
stepsister" — was rendering on the same row as the true grandparents,
with nothing visually distinguishing them from the actual family.
Broader complaint alongside it: the view reads as "just a list," people
"stacked" rather than organized into legible subgroups; asked for
something closer to a proximity/acquaintance-based arrangement, with
extra room between unrelated subfamilies for readability, while
explicitly leaving the approach open rather than dictating one.

Root cause, confirmed with a hand-built repro before touching any
rendering code: `computeLayers` (see round 2) has no way to know a
disconnected person's true generation, so anyone with no recorded
parents *and* no intact partner-chain back to the family defaults to
layer 0 — the same bucket as real root ancestors, with no signal left to
tell them apart. There's no better layer number to guess here (the data
genuinely doesn't say), so the fix isn't a smarter layer computation —
it's making sure a person in that situation never reads as part of a
cluster they're not actually connected to.

- **`connectedComponents(ids, parentsOf, partnersOf)`** (new, in
  `tree-graph-logic.js`) — every person's component index over the
  *undirected* blood-and-partner graph (parent/child and partner edges
  both count, direction ignored), assigned by a plain flood fill in
  first-appearance order. This is the one piece of information
  `computeLayers` doesn't have: whether two people who happen to share a
  layer number are actually reachable from each other at all.
- **`orderRows`** now takes `componentOf` and sorts each row by component
  *first*, barycenter position only breaking ties within a component —
  so two unrelated clusters landing on the same row are never
  interleaved, and a cluster's relative position stays stable across
  every row it spans (never left-of on one row, right-of on the next).
  For the common case — one connected family, one component for
  everyone — this is a no-op and the ordering is bit-for-bit what round
  2 already produced; verified against both existing fixtures (the
  17-person blended family and the 13-person plain one) with no change
  in output.
- Renderer (`tree.js`): row layout switched from a uniform per-column
  pixel grid to walking each row's ordered ids directly, adding the
  normal column gap between two cards in the *same* component and a much
  wider `GRAPH_CLUSTER_GAP` (column gap + 96px) between two different
  components sharing a row — enough to read as a deliberate separation,
  not just a slightly loose layout.

Reproduced the exact bug report with a small fixture (an isolated
"Belle-Soeur Nadia" + "Beau-Frere Karim" couple, partnered only with each
other, no parent link to anyone) alongside a normal two-grandparent
family: before the fix, both landed at `x: 0, 1` on layer 0, indistinguishable
from the real grandparents; after, they land in their own component,
grouped together and pushed to the far side of the row with the wide gap
between.

Tests: `tests/js/tree_graph_logic_test.mjs` gained 3 cases (16 total) —
`connectedComponents` on a single-component family and on the isolated-
couple scenario, plus a `layoutFamily` case asserting the in-law
component shares layer 0 with the grandparents but a distinct
`componentOf`, grouped contiguously after the main family rather than
interleaved. `pytest` (664) and `ruff check .` green. Manually verified
(Playwright) against both the disconnected-in-law fixture (clear gap
separating the isolated couple from the grandparents row, no
intermixing) and the original round-2 blended family (unchanged
17-for-17 rendering, confirming the single-component no-op case holds in
the browser too, not just in the unit tests).

## "Everyone" round 4 — a real crack at "it looks like a list"

Round 3 fixed the reported bug but not the underlying complaint: even a
correct, non-duplicating, cleanly-separated-by-component render still
looked like uniform rows of evenly-spaced boxes on any family with more
than one nuclear unit per generation — round 3's own gap constant was
a single value applied identically to every adjacent pair whether they
were a married couple or two unrelated cousins. Verified this with a
deliberately larger, messier fixture (20 people, five sibling branches,
a divorced-and-remarried aunt) before touching any code — screenshotting
round 3's output against it confirmed the "list" read was real and not
fixed by the round-3 work, despite every individual bug being gone.

**A detour that didn't pan out, worth recording:** the first attempt at
a fix was a from-scratch force-directed layout (`d3-force`, part of the
already-vendored `d3` bundle — no new dependency needed) — generation
rows hard-pinned every tick, `forceLink`/`forceManyBody`/`forceCollide`
left to organically cluster everything else. Implemented and screenshot-
tested against the same messy fixture: it converged to something
numerically and visually indistinguishable from a uniform grid. Root
cause, found by inspecting the actual converged coordinates: `forceCollide`'s
per-node minimum-separation radius was larger than the `forceLink`
partner-distance target, so collision resolution dominated everywhere and
overrode the very links that were supposed to create visible clustering
— every gap converged to nearly the same width regardless of whether the
two adjacent people were married, siblings, or unrelated. A real fix
would need a genuine per-cluster attraction force (dynamically recomputed
centroids, the standard "cluster force" recipe), which is exactly the
kind of hard-to-verify, iteration-tuned behavior this codebase's
"boring, minimal, testable" bar is a poor fit for — reverted rather than
shipped once the numbers showed it wasn't actually better than round 3.

**What shipped instead**: kept `layoutFamily`'s deterministic per-row
grid entirely (still `computeLayers` + `connectedComponents` +
barycenter ordering, unchanged), but replaced the single uniform column
gap with four explicit tiers, tightest to widest:

1. **Partners** — almost touching (10px). A married couple should read
   as a couple at a glance.
2. **Close** (new — `closelyRelated` in `tree-graph-logic.js`) —
   siblings/half-siblings (share a parent) or co-parents (share a
   child): 28px, round 3's old uniform gap.
3. **Same component, not closely related** — cousins, in-laws-of-
   in-laws, or two grandparent couples related only through their
   children's marriage: 96px.
4. **Different connected component** — 200px, round 3's existing
   cross-component separation, now the widest tier rather than the only
   special-cased one.

The subtlety that took a second pass to get right: deciding a gap from
the two literal touching cards isn't enough. A remarriage chain like
Marc–Julie sitting next to Papa–Maman puts Julie (Marc's wife, no blood
link to Papa) directly against Papa — checking only that pair would miss
that Marc and Papa are brothers and wrongly fall back to the wide tier.
Caught this by computing exact pixel gaps (not just eyeballing a
screenshot) against the messy fixture and finding Julie→Papa measured
96px where it should have been 28. Fixed by grouping each row into its
`coupleUnits` first and checking every member of one unit against every
member of its neighbor — Marc (in the left unit) paired against Papa (in
the right unit) correctly finds the sibling link even though neither of
them is the card physically on the boundary.

Tests: `tree_graph_logic_test.mjs` gained 5 `closelyRelated` cases (21
total) — partners, siblings-by-shared-parent, co-parents-by-shared-child,
cousins (correctly *not* closely related), and two unconnected
grandparent couples (correctly not closely related). `pytest` (664) and
`ruff check .` green. Manually verified (Playwright, with exact pixel
gap measurements, not just visual inspection) against three fixtures:
the messy 20-person family (now reads as visibly organized clusters —
tight couples, close-but-distinct sibling branches, a clear gap to the
disconnected in-law pair — where round 3 read as a flat grid), the
original round-2 blended family (unchanged card count and no
regression, same clean two-grandparent-branch separation), and the
round-3 disconnected-in-law repro (still correctly isolated with the
widest gap tier).

## "Everyone" round 5 — children under their parents (aligned columns)

Round 4's tiered gaps made each ROW read correctly, but rows were still
packed independently from the left — nothing tied a couple's horizontal
position to where its own children sat. On a wide family (verified with
a new 30-person / 3-generation / 5-branch fixture before touching any
code) a couple could drift almost two card-widths sideways from its own
children, drop-lines wandered diagonally across the whole chart, and
vertically adjacent generations read as unrelated rows — the
"presenting a mix of people" complaint, still alive after four rounds
of fixing everything else. The measurement that finally captured it
(and that card counts and per-row checks never could): for every
parent-couple, the horizontal distance between the couple's centroid
and their children's centroid. Round 4 measured **0.74 card-widths mean
/ 1.88 max** on the 30-person fixture.

Fix: a new coordinate-assignment stage, `assignPixelPositions` in
`tree-graph-logic.js` (pure, dependency-free, Node-tested like the rest
of the module). It keeps everything round 2–4 already got right — exact
generation rows, `orderRows`' left-to-right order, partners glued at
`gapPartner`, the four gap tiers as *minimum* constraints — and then
runs a fixed number of alternating sweeps: top-down, each row's units
pull toward the mean of their members' parents' positions; bottom-up,
toward the mean of their children's. Each row's pulls are reconciled
against its min-gap ordering constraints *exactly* (not iteratively)
with the classic pool-adjacent-violators algorithm — least-squares
optimal, order-preserving, deterministic, ~25 lines. No physics, no
convergence tuning; the earlier force-directed detour (round 4's
FEATURES entry) failed precisely because its solver couldn't respect
"gaps are hard constraints, alignment is a preference" — PAV encodes
that distinction natively.

A test assertion caught a nice subtlety worth keeping in mind: at a
fixed point, a grandparent couple centers over its blood children's
CARDS, not over its child's whole marriage — so the trunk from the
grandparents drops vertically onto their own child, with the spouse
hanging beside — which is the classic pedigree presentation, not a bug
(the initial test asserted the wrong invariant and failed against
correct behavior).

`tree.js`'s `renderFamilyGraph` now just calls `assignPixelPositions`
with its pixel constants and reads back per-card x positions — the
round-4 gap-walk code moved wholesale into the logic module where it's
unit-testable.

Measured after (same fixtures, same metric — deviation in card-widths,
mean/max): 30-person ring **0.36 / 1.15** (all five child-couples at
exactly 0.00; the residual is only the grandparent row of the marriage
ring, where five couples' children each marry in two different
directions and no linear arrangement can center everyone — provably
irreducible), 20-person messy family **0.02 / 0.07** (was 0.74 mean),
17-person blended family **0.04 / 0.10**, with half-siblings under
their actual parent pairs in both. Zero same-row overlaps and exact
partner gaps everywhere; the isolated in-law couple still keeps the
full cross-component gap (its two grandparent couples now sit jointly
centered over the child couple — each 0.77 off, the provable optimum
when two 458px-wide couples both want to center over cards 186px
apart). Mobile (390px): no page overflow, auto-fit unchanged.

Tests: `tree_graph_logic_test.mjs` gained 7 cases (28 total) — three
direct `poolAdjacentViolators` cases (monotone input unchanged,
weighted pooling, output always non-decreasing) and four
`assignPixelPositions` cases (exact centering when nothing conflicts,
exact partner gaps + no min-gap violations, cross-component separation
preserved, byte-identical determinism across runs). `pytest` (664) and
`ruff check .` green.

### Same round, follow-up: traceable connector lines

Immediate feedback on the aligned layout: "just look at the links, it
is not tracable." Correct — and the cause was one line of the drawing
code: every parent-group's horizontal connector ran at the SAME height
(`trunkY = parentY + ROW_GAP / 2`), so on any generation with several
families, all their horizontal segments merged into what read as a
single dashed line spanning the chart, with no way to tell which
drop-line belonged to which couple. The card layout work couldn't fix
this; no card position makes overlapping same-height lines readable.

Three changes, all to the connector drawing only (card positions
untouched):

- **Lane assignment** (`assignLanes` in `tree-graph-logic.js`, pure +
  unit-tested): per corridor between generations, families whose
  horizontal runs would overlap get distinct heights, assigned
  first-fit left-to-right; families whose runs don't overlap share a
  lane, so a simple tree keeps its clean single-height connectors.
  Lanes spread evenly across the corridor (one lane sits centered —
  the classic look; two land at 1/3 and 2/3) rather than being offset
  by a token amount.
- **Marriage-line trunk starts**: a couple's drop-line now starts ON
  the marriage line, descending through the gap between the two
  partner cards — the line visibly emerges from *that couple*, which
  matters most in remarriage chains (Ex-Marc—Maman—Papa—Ex-Anne draws
  three separate drops, one per marriage, each from its own gap to its
  own children). A single recorded parent's line still starts at their
  card's bottom edge.
- **Rounded elbows** where a run turns down toward a child — a smooth
  corner is what lets the eye keep following one line through a
  crossing instead of losing it at a sharp right angle.

Verified numerically (parsing the rendered SVG paths, not eyeballing):
on the 30-person ring fixture, every corridor's same-height spans are
separated by comfortable gaps — zero near-merges within 20px — where
before ALL runs in a corridor shared one y exactly. 4 new `assignLanes`
tests (32 total). `pytest` (664) and `ruff check .` green; blended and
messy fixtures re-verified visually with every drop-line traceable to
its marriage.

## "Everyone" round 6 — co-parents without a recorded partnership

Real-data bug report, with a screenshot that made the cause findable: a
child's two recorded parents rendered at OPPOSITE ENDS of their
generation row, reading as if "only one parent is recognized," and one
parent stranded a full generation too high. The data was fine — the
missing ingredient was a *partner* link between the two parents. Every
piece of family-unit handling in the layout (same-layer pull in
`computeLayers`, side-by-side unit grouping in `coupleUnits`, the
marriage-line trunk start) keyed exclusively off recorded partners; two
people who share a child but no recorded partnership (divorced,
unmarried, or simply an incomplete entry) got none of it. So:
`computeLayers` never pulled such a parent down to their co-parent's
generation (someone with no recorded parents and no partner link
defaults to layer 0, up among the grandparents); the row ordering
scattered the pair like strangers; and the child's drop-line drew from
the midpoint of two far-apart cards — a line starting in mid-air,
crossing everything, traceable to nobody.

Fix, in `tree-graph-logic.js`: a new `coParentPairs(ids, parentsOf)`
(distinct pairs sharing at least one child) and `unitLinkMap` (partner
links ∪ co-parent links, one symmetric neighbor map). `computeLayers`
equalizes layers across the combined map — sharing a child is proof
enough of a shared generation — and `orderRows`/`assignPixelPositions`
group row units along it, so co-parents stand side by side over their
children exactly like a married couple. What co-parents deliberately do
NOT get: the solid marriage line (`partnerPairs` still draws only
recorded partnerships), and the trunk's marriage-line start — in
`tree.js`, a parent pair's trunk starts at mid-card height only when
the two are recorded partners; an unpartnered pair's drop starts at
card-bottom level in the (adjacent) gap between them, so the render
still tells the truth about what's recorded. Recording the partnership
in the data remains the better fix where a marriage actually exists —
it adds the marriage line and the husband/wife kinship labels — but the
tree no longer falls apart when it's absent.

Reproduced the reported structure exactly in a fixture (two unpartnered
co-parent pairs, one of them with the co-parent marrying into the main
family's descent line, plus a single-parent child) — before: one parent
at each end of the row, the other co-parent stranded on the wrong
generation; after: both pairs adjacent on the correct rows, children
centered under them (deviation 0.00 for both pairs' children), every
drop-line traceable. The 30-person ring fixture re-measured bit-for-bit
unchanged (all its co-parents are also partners, so the new links are a
no-op there — the common case costs nothing). 4 new tests (36 total):
`coParentPairs` dedup, `computeLayers` co-parent layer pull,
adjacency + centered-child through the full pixel pipeline, and
`partnerPairs` drawing no marriage line for unpartnered co-parents.
`pytest` (664) and `ruff check .` green.

## "Everyone" round 7 — links flow from each parent, not from a union point

Direct user feedback on round 6: "link should flow from parent to
child directly, not from union." The connectors had always emanated
from an abstract union point — the couple's midpoint (round 5 put it on
the marriage line; round 6 moved unpartnered pairs' to the card-bottom
gap) — so a child's line rose into empty space between two cards
rather than visibly connecting to either parent.

Redrawn as the classic T-bar descendant chart, connector geometry only
(card positions and lane assignment untouched): each parent drops a
line from their own card's bottom edge onto the family's horizontal
bar, and each child hangs from that same bar — so a two-parent child
traceably connects to BOTH parents' cards with no invisible junction
anywhere. The bar spans from the leftmost to the rightmost of the
family's attachment points, with rounded corners into whichever
terminal sits at each end (up toward a parent, down toward a child) and
plain T-junctions for the ones between. A single parent directly above
their only child degenerates to one straight drop, no bar.

One wrinkle worth recording: a remarried parent belongs to several
families, which now means several drops from the same card bottom —
drawn naively they'd all start at the card's center X and overprint on
the shared stretch below the card. Each parent's drops are nudged 12px
apart around their card center, ordered so each leans toward its own
family's side (sorted by bar midpoint), which reads as two distinct
lines leaving one card — verified on the blended fixture, where Papa,
Maman, and Oncle Paul each carry one drop per marriage.

The round-6 distinction between married and merely-co-parenting pairs
lost its geometric expression (there's no union start to vary anymore)
— it now rests entirely on the marriage line itself, which still draws
only for recorded partners.

Verified (Playwright + the SVG-parsing near-merge check) against the
co-parents fixture, the blended fixture, and the 30-person ring — all
consistency metrics unchanged from round 6 (connector geometry doesn't
move cards), zero overlaps, every line starting at a real card. `pytest`
(664), `ruff check .`, and the 36 Node tests green.

## F20. Event tagging, story↔people linkage, and source citations

README/FEATURES (F19) had twice declared `tags` deliberately out of scope
for v1 — "belongs in a discussion first, not a surprise addition." This is
that discussion, revisited on direct request: a parent wanted (1) event
tags, (2) a way to say who's *in* a given story, on top of the existing
genealogy (F14/F18), and (3) somewhere to paste a citation link for a photo
or fact ("this came from aunt Jane's post"). Nothing here fetches
anything; every link is pasted in by hand.

To keep this inside "book, not blog" (no search, no discovery surface),
tags/people/sources are **display metadata plus a filter on the existing
single-purpose timeline search box** — not a new tag-browsing/tag-cloud
page, and not a general search feature.

### Storage

- `Story` (storage.py) gains `people` (list of person slugs), `tags` (list
  of free strings, capped at `MAX_TAGS`=20 × `MAX_TAG_LENGTH`=40, deduped),
  and `sources` (list of `{"url", "note"}` dicts) — all tolerantly parsed
  (garbage silently dropped, same philosophy as every other frontmatter
  field), threaded through `create_story`/`save_story`/`_write_index`/
  `restore_version` with the same "`None` means leave unchanged, empty
  clears" convention `cover`/`author` already use.
- `Person` (people.py) gains `sources` only — a person doesn't link to
  itself.
- New `storage.stories_featuring(stories_dir, person_slug)`: stories whose
  `people` includes the slug, for the person page's new "Appears in"
  section (filtered through `readable_stories` — a draft or sealed story
  doesn't leak its existence just because someone's tagged in it).

### API validation (routes_api.py)

- `_validate_story_people` reuses the existing `_validate_slug_list` (the
  same one `parents`/`partners`/`friend_of` already use) — no new
  slug-validation logic needed.
- `_validate_tags`: trims/dedupes/caps, no other rules — tags are display
  metadata, not an identity system.
- `_validate_sources`: **restricts `url` to `http://`/`https://` only.**
  These render back as `<a href>` on the story/person page, so accepting a
  `javascript:`/`data:` scheme here would be a stored-XSS vector — this is
  the one place in the feature where "just paste a link" needed a real
  guardrail.

### Editor UI (editor.js, shared by story + person forms)

- Story editor gets a people chip-picker (reusing the same `initChipPicker`
  widget the family pickers already use, via a generalized `chip_group`
  macro lifted from `person_editor.html` into `_macros.html`) and a plain
  comma-separated tags input — no new chip-input widget for free text.
- Both story and person editors get a small repeatable-row "Sources"
  widget (add/remove URL+note pairs), hydrated from a
  `<script type="application/json">` block the same way F16's prompt list
  already is. Autosave/crash-recovery (`applyDraft`) restores all three
  fields too, same as every other editor field.

### Display

- Story page: linked people as name links under the title, tags as small
  quiet pills, sources as a plain list at the bottom — no counts, no
  engagement chrome.
- Person page: a new "Appears in" section (styled like the existing family
  sections) plus the person's own sources list.
- Timeline: entries carry a `hidden` (DOM-only, not visually shown — the
  single-row timeline layout has no room for a subtitle line) span with the
  entry's tags + linked people's names, so the existing client-side search
  box matches on them too. Never rendered for a sealed entry, so a sealed
  letter's tags/people stay hidden along with everything else about it.
  Search placeholder updated to "Search titles, tags, people…".

### Explicitly not built

- A dedicated tag-browse/tag-cloud page — would cross from "metadata" into
  the excluded "search" territory.

23 new tests across `test_storage.py`, `test_history.py`, `test_api.py`,
`test_family_api.py`, `test_people.py`, `test_family_pages.py`,
`test_pages.py`, and `test_timeline_search.py` (687 total). Manually
verified end-to-end with Playwright: person + story creation with
tags/people/sources, story/person page rendering, timeline search matching
on both a tag and a linked person's name, a sealed story's tags/people
never appearing in the page source, and a `javascript:` source URL being
rejected with an inline error rather than saved. `pytest` and
`ruff check .` green.

## F21. People picker: searchable scrolling list, ticked stays on top

Direct feedback on F18/F20's chip-wall picker (parents/partners/friend_of,
plus F20's story-people field): it's a wrapped wall of pill buttons with
no search, and once the cast grows there's no reliable way to confirm
who's ticked without scanning the whole thing.

Replaced the shared `chip_group` macro (`_macros.html`) and its
`initChipPicker` JS (`editor.js`) — used at all four call sites — with a
`people_picker` macro + `initPeoplePicker`: a search box above a
fixed-height (`14rem`, ~5 rows) scrollable list of row buttons. Ticked
rows always sort to the top (alphabetically within each of the
selected/unselected groups) and are **never hidden by the search filter**
— only the unselected pool gets filtered — so a selection can't get lost
to scrolling or to typing an unrelated query afterwards.

Kept the exact same JS API (`getSelected()`, `setSelected(slugs)`,
`maxSelected`) so `buildStoryPayload`/`addFamilyFields`/the autosave
`applyDraft` needed zero changes, and the same `<button
data-person-slug="..." aria-pressed="...">` shape existing tests assert
on — this is a rendering/interaction change only, no data-model or
validation change. Authors chips and gender buttons (separate, small,
fixed-option widgets) are untouched.

All 687 existing tests passed unmodified. Manually verified with
Playwright at a 390px mobile width against a 10-person fixture: search
narrows the unselected rows, a ticked-then-searched-away row stays
visible and pinned at top, `maxSelected=2` still blocks a third parent,
and reopening the edit page reloads with both selections pinned at the
top. `pytest` (687) and `ruff check .` green.

## F22. Button icons — a small bold/flat companion set to F17

F17's illustrations (fine etched linework, cross-hatching) are gorgeous at
full size but don't survive being shrunk to icon size — tested directly:
at 24px (the real size an icon renders next to a button label) the fine
detail collapses into an illegible smudge, confirmed by rendering a test
icon at 24/32/44px before committing to a style. A second, bolder style —
flat 2-3 color fills, thick uniform outlines, no cross-hatching — reads
clearly even at 24px, so that's what this set uses. It is a deliberate
second, smaller-scale companion to F17's style, not a replacement for it.

Every button already carries a clear text label (verified — no icon-only
button exists anywhere in the app); these icons are a small accent next
to the existing label, never a replacement for it.

### Assets

Generated externally (Gemini) from prompts describing the bold/flat
style, then processed locally: each image's background is auto-keyed to
transparent (sampling the image's own border pixels as the reference
color, so it adapts to whatever near-white shade a given generation
comes back as, rather than a hardcoded threshold), cropped to its content
bounding box, repadded to a square with an 8% margin, and downscaled to
160×160 (comfortably above the ~40px a 20px display size would need at
2x). All 12 committed under `app/static/img/`:

| file | used on |
|---|---|
| `icon-save.png` | Save button (story + person editor, instant) |
| `icon-new-story.png` | "+ New story" (nav, timeline empty state) |
| `icon-instant.png` | "+ Instant" (nav) |
| `icon-new-person.png` | "+ New person" (people page) |
| `icon-tree.png` | "Family tree" link (people page) |
| `icon-draft.png` | Draft toggle (editor) |
| `icon-archive.png` | Archive toggle (editor) |
| `icon-seal.png` | "Seal until" label (editor) |
| `icon-source.png` | "+ Add source" (story + person editor) |
| `icon-record.png` | "Record" (voice memo) |
| `icon-print.png` | "Print / save as PDF" (book view) |
| `icon-import.png` | "Import" (backup restore) |
| `icon-group.png` | "Who can see this" (audience picker, F42) |

New shared `.btn-icon` class (main.css): 20×20px, `flex: none`, small
right margin — relies on the parent already being `display: flex/inline-
flex` (true for every `.btn`); `.book__print-btn` and `.editor__unlock-
label` weren't flex containers before this, so both gained `display:
inline-flex; align-items: center` alongside the icon. No filter applied
(these are flat-color illustrations, not photos — same treatment as
`rope-divider.png`/`brand-star.png`, not the photo-filter path).

Verified in both light and dark themes with Playwright (390px width):
every icon renders with a clean edge, no white halo, in both themes;
`pytest` (687) and `ruff check .` still green — no test asserted on a
button's exact inner HTML, only on attributes of the opening tag, so
none needed updating.

## F23. Hover/press feedback across the interface

Audited the whole interface for interaction feedback and found the gap
was total: `.btn` (the single most-reused class in the app) had no
`:hover` or `:active` state at all, nor did the timeline row links, the
family/person-picker links, or the shared "‹ Back" links used on a dozen
pages. Every click landed with zero visual acknowledgment.

- `.btn` (and everything built on it — `.btn--primary`, toggle chips, the
  people-picker rows, since they all carry the `.btn` class): hover shifts
  the border to the accent color; `.btn--primary` additionally brightens
  slightly. Press (`:active`) does a quick `scale(0.96)` — a tactile
  "pressing a real button" feel rather than a card-lift/shadow effect,
  kept in the "boring, minimal" spirit rather than borrowing a modern
  SaaS elevation pattern. Gated behind `@media (prefers-reduced-motion:
  no-preference)` — only the transform is gated; the border-color fade
  is not real "motion" and stays for everyone.
- `.people-picker__row` (F21) additionally gets a background tint on
  hover — a border-color change alone is too subtle on a full-width list
  row — and opts out of the press-scale (`transform: none`), since
  scaling a row edge-to-edge inside a bordered list looks like a glitch,
  not a button press.
- `.book__print-btn` isn't built on `.btn` (it's a `position: fixed`
  pill), so it got the same border-color hover / press-scale treatment
  directly.
- `.person-family__link` (F18's family-section links) gets the same
  border-color hover.
- `.timeline__link`: the whole row has no spare horizontal padding (an
  absolutely-positioned dot/envelope/thumb share the space), so a
  background-tint hover risked clipping oddly against them untested;
  underlining the title on hover instead is layout-safe and still reads
  clearly as "this is a link."
- Every "‹ Back" link across the app shares a single-class wrapper
  convention (`.people__back`, `.import__back`, `.admin__back`, etc.) —
  one shared selector (`[class$="__back"] a`, plus `.story__back` which
  is applied directly to its `<a>`) gives all of them an underline-on-
  hover without touching a single template.

Verified with Playwright across the nav, editor (Save/Draft/Archive/
people-picker), timeline, and `/book`'s print button, in both light and
dark themes — clean visual feedback everywhere, no clipping or layout
shift. `pytest` (687) and `ruff check .` green (CSS-only change, no
template or Python edits).

## F24. Hover feedback, round 2 — the rest of the interactive surface, and a dead-CSS catch on /tree

Continued F23's audit to the remaining interactive elements: the theme
toggle (every page, top-left nav — high traffic, previously totally
inert), the import/instant photo drop-zones (dashed border → accent on
hover), the lightbox close button, the photo-crop zoom buttons, the
editor's markdown-fallback toolbar, the logout link, a transcript
`<summary>`, and the timeline's right-edge year minimap ticks (carefully
excluding `.is-active` from the hover rule — equal specificity to a
plain `:hover`, so it needed an explicit `:not(.is-active)` guard or
hovering the current year would've broken its highlight).

**The family tree cards were the interesting one.** `.tree-graph__card`
exists in main.css and looked like the obvious hover target — but
testing it live (Playwright, walking the actual DOM) showed the tree
page never renders that class at all. It renders through the vendored
`family-chart` library's own markup (`.f3 div.card-inner`, styled by the
`.page-tree .f3 ...` rules a few hundred lines down, per R5.1/R5.2's
paper-card-and-gold-ring treatment). `.tree-graph__card` is dead CSS from
an earlier implementation. Added the hover there instead of leaving
inert rules behind — border darkens, shadow deepens — and, following the
exact same specificity trap the existing R5.2 comment already documents
(a plain rule and a same-specificity modifier rule tie, so the modifier
must repeat itself or the plain rule's `:hover` silently wins): both
`.card-inner--focus:hover` (re-rooted target) and `.card-main .card-inner:hover`
(the configured anchor, gold ring + brand stamp) explicitly repeat their
gold border rather than inheriting the plain card's darker hover color.
Verified live: hovering the anchor keeps its ring and stamp intact,
hovering any other card gets the plain darkened treatment.

Would have shipped silently-inert CSS without the live-DOM check — worth
remembering that a class existing in main.css doesn't mean anything
renders it.

`pytest` (687) and `ruff check .` green throughout (CSS-only).

## F25. Splitting routes_pages.py / routes_api.py by resource (no URL changes)

`routes_pages.py` (969 lines) and `routes_api.py` (718 lines) had each
accumulated every resource's routes — stories, people/genealogy,
accounts/admin, delegated write-links — in one file. Split each by
resource without renaming a single endpoint or touching a template:

- `routes_pages.py` keeps the `pages` Blueprint and the core
  story-reading/writing routes (timeline, story pages, the editor,
  drafts/archived, `/book`, backup export/import) plus the helpers more
  than one group needs (`_people_dir`, `_person_ref`,
  `_other_people_refs`, `_serve_media`, `DEFAULT_AUTHOR_COLOR`).
- `routes_people.py` (new) — people/genealogy pages (F14/F18): the people
  list, person page, `/tree`, new/edit person.
- `routes_accounts.py` (new) — family accounts (F19): the request/approve
  flow, admin account management, self-service password change,
  delegated write-links.
- Same split for the API blueprint: `routes_api.py` keeps the core story
  API (create/update/restore, image/memo uploads, backup import) plus
  `_validate_slug_list`/`_people_dir` (needed by both story and person
  validation); `routes_api_people.py` (new) holds person/family CRUD,
  photo uploads, and `/api/tree`.

**The trick that makes this a pure file reorganization, not a routing
change:** the new files don't declare their own `Blueprint` — they `from
.routes_pages import bp` (or `.routes_api import bp`) and add `@bp.route`
in their own file. Every `url_for("pages.xxx")` / `url_for("api.xxx")`
call, in Python and in every template, keeps resolving to the exact same
endpoint name it always did, regardless of which file the route's code
now physically lives in. The split files are imported at the very bottom
of `routes_pages.py`/`routes_api.py` (after `bp` and every helper they
need already exist) purely for that side effect — registering their
routes onto the shared blueprint before `app.register_blueprint()` runs
in `create_app()`. `app/__init__.py` needed zero changes.

Verified: `app.url_map` has the identical 52 rules before and after: full
`pytest` (687, unmodified) green; a live smoke test hit one route from
each new file (`/people`, `/tree`, `/account` [404 as expected, accounts
mode off], `POST /api/people`) to confirm real request handling, not just
import-time registration.

## F26. CSRF protection

This app is session-cookie-authenticated (a single shared password, or
per-person accounts in F19 mode) and lives publicly on GitHub as a
self-hostable project — exactly the shape where a malicious page could
submit a form or `fetch()` to a logged-in user's own Storybook instance
and have the browser attach valid session cookies automatically. There
was no CSRF protection anywhere; this closes that gap.

Used Flask-WTF's `CSRFProtect` rather than hand-rolling token
generation/comparison (`requirements.txt`: `flask-wtf==1.3.0`, pinned like
every other dependency). Wired in `app/__init__.py` right after the
blueprint imports: `CSRFProtect(app)`. No extra config needed —
`SECRET_KEY` already exists whenever `STORYBOOK_PASSWORD` is set, and
CSRF tokens key off it. `CSRFProtect` checks every unsafe-method request
(POST/PUT/PATCH/DELETE) for a valid token and rejects with 400 otherwise;
safe methods (GET/HEAD) are never checked. Nothing is exempted.

Two attack surfaces, two delivery mechanisms for the same token:

- **Native server-rendered forms** (login, admin actions, account
  settings, delegated write-links, logout, ...): `csrf_token()` becomes
  an automatic Jinja global once `CSRFProtect` is initialized. Added
  `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">` to
  every native `<form method="post">` — one edit to `_macros.html`'s
  `action_button_form` macro covers every button that reuses it (all of
  `admin_accounts.html`'s reject/disable/enable/revoke buttons), plus
  ~10 standalone forms (`login.html`, `account_password.html`,
  `account_write_links.html`, `admin_accounts.html`'s inline role forms,
  `admin_new_account.html`, `admin_reset_password.html`,
  `admin_review_pending.html`, `delegate_write.html`,
  `request_account.html`, `timeline.html`'s logout form). The editor,
  instant-story, import, and person-editor forms are untouched here —
  none of them has `method="post"`; their submit is already intercepted
  by JS and turned into a `fetch()`, so they're covered by the mechanism
  below instead.
- **JSON API calls from JS** (`editor.js`, `instant.js`, `import.js`,
  `history.js`): a header, not a form field. New
  `app/static/js/csrf.js`, a small IIFE in the same style as `theme.js`
  (loaded globally, exposes one thing on `window`, no Node test — there's
  no meaningful DOM-free logic to extract from "read a meta tag"):
  reads `<meta name="csrf-token" content="{{ csrf_token() }}">` (added to
  `base.html`'s `<head>`) and returns a copy of a `fetch()` options object
  with `X-CSRFToken` merged into its headers. Every mutating `fetch()`
  call site wraps its options through `window.CsrfFetch.withToken(...)`:
  7 in `editor.js` (photo/memo upload, memo delete, create/update story,
  image upload), 3 in `instant.js` (create, image upload, update), 1 in
  `history.js` (version restore), 1 in `import.js` (backup import).
  Read-only `fetch()` calls (`tree.js`'s GET) are untouched.

One subtlety surfaced while testing: `auth.py`'s login route calls
`session.clear()` on successful password login (deliberate
anti-session-fixation practice, predates this feature) before setting
`session["authed"]`. That wipes the session's CSRF secret, so a token
fetched from the pre-login `/login` page becomes invalid the instant
login succeeds — a same-session client needs a *fresh* token (e.g. from
the next page's `<meta>` tag) for its first post-login request. This
doesn't affect real usage (every page's own render always embeds a
current token for its own forms/fetches), but it's why
`tests/test_csrf.py`'s post-login API test fetches a fresh token from an
authenticated page rather than reusing the pre-login one.

`tests/conftest.py`'s shared `BASE_TEST_CONFIG` gained
`"WTF_CSRF_ENABLED": False` — one line disables CSRF for the ~687
existing tests (none of them are about proving CSRF works, and none
submit real tokens). Two tests that bypass `BASE_TEST_CONFIG` entirely to
exercise real env-var config (`test_epub.py`,
`test_manifest.py`) needed the same flag set directly on their
bare `create_app()` instance. New `tests/test_csrf.py` uses the real
default (CSRF *on*) to prove the whole thing actually works: a bare POST
is rejected (400), GET is unaffected, the login page renders a real
token, a POST with a valid token succeeds, a wrong token is rejected, and
the `/api/*` JSON path is rejected without the header and succeeds with
it.

Verified live (not just unit-tested): started the dev server, logged in
through the real `/login` form (native form + token), created an instant
story end-to-end through `/new-instant` (3 chained CSRF-protected
`fetch()` calls — create, image upload, update — all succeeding), and
logged out through the native logout form — all with Playwright driving
a real browser, confirming both delivery mechanisms work outside of unit
test mocking.

`pytest` (694: 687 existing + 7 new) and `ruff check .` green.

## F27. Life dates — birthdays, deaths, and unions

Requested directly: a parent wanted to record grandparents' birthdays and
deaths, plus wedding/PACS dates (and, when it happens, when a union
ended). Rather than six separate features, this is one small addition to
`Person`: two dates (`born`/`died`) and a list of unions, each an optional
kind/since/until on an existing partner link.

### Storage (`app/people.py`)

- `Person` gains `born`/`died` (`Optional[date]`) and `unions` (a list of
  `{"partner", "kind", "since", "until"}` dicts — `kind` is
  `wedding`/`pacs`/`union`, `until` optional). All tolerantly parsed
  (malformed entries dropped, not raised — files outlive edits, same
  philosophy as `sources`/`tags`).
- `create_person`/`update_person` follow the established "None means leave
  unchanged" convention for all three (photo/sources/author_color already
  work this way): `born`/`died` additionally treat `""` as "clear",
  `unions` treats `[]` as "clear".
- Deliberately **not** a new top-level dataclass or a redesign of
  `partners` — a union is descriptive metadata layered on an *existing*
  partner link, not a new kind of relationship. `partners` (and
  everything built on it: `kinship.py`, the tree chart, `tree.js`) is
  completely untouched.

### API (`routes_api_people.py`)

- `_validate_born`/`_validate_died`: ISO date or 400; a
  `died < born` cross-check also 400s. `_validate_unions`: tolerant, not
  strict — an entry with an unknown `kind`, an unparseable date, an
  `until` before its `since`, or a `partner` not in that person's own
  `partners` list is silently dropped rather than rejecting the whole
  request (a union record isn't a security boundary the way F20's source
  URL scheme is).
- Union records are symmetric on disk, exactly like the partner link
  itself: a wedding date is one fact about two people. `_sync_union_symmetry`
  mirrors kind/since/until onto the other partner's file, mirroring
  `_sync_partner_symmetry`'s existing shape. Dropping a partner (even via
  a hand-crafted request that never resends `unions`) also drops any
  union with them on both sides — the invariant "every union's partner is
  a current partner" is enforced unconditionally at write time, not only
  when the client happens to submit `unions` in the same request.

### Editor UI (`person_editor.html`, `editor.js`)

- Two plain date inputs, "Born"/"Died", always present on the person
  editor (not gated behind any other field).
- "Unions": a repeatable-row list under the existing Partner picker —
  partner (a `<select>` populated from whoever's currently ticked in the
  Partner picker), kind, since, until, and a remove button. Same
  repeatable-row shape as F20's Sources UI. Clicking "+ Add union" with no
  partner selected shows a quiet inline message instead of adding an
  unusable row.

### Display

- Person page: `born`/`died` render as a small line under the name —
  "Born {date} · {age}" when only `born` is set (reusing F3's
  `age_label`), a `{born} – {died}` span when both are set. A `died`-only
  person (a relative from before the book started) shows "Died {date}".
  An "Unions" section lists each partner with kind + year range, styled
  like the existing Parents/Partners/Children groups.
- New `/almanac` page (`app/life_events.py`, `routes_people.py`): every
  recorded birth, death, and union date, month by month, independent of
  year — a real family record book's calendar page, not the timeline's
  dated entries. A union's `until` is noted on its one entry rather than
  becoming a second recurring date — this page is a record, not something
  to mark as an anniversary. Linked from `/people` (only when at least
  one person actually has a life date set).
- Timeline: a living person's birthday and an ongoing union's anniversary
  (both month/day matches, Feb 29 makeup rule reused from F5) surface as
  quiet banners next to the existing "X years ago today", e.g. "Mamie
  turns 70 today" / "Papa & Claire — 10-year wedding anniversary today".
  **Deliberately excluded from the timeline:** death anniversaries and
  ended unions. Both are recorded (person page, almanac) but never
  surfaced as a banner — an unprompted "would have been 70 today" or an
  anniversary of a separation is the wrong kind of surprise for a book a
  child reads freely; the almanac is something you visit, a timeline
  banner is something that visits you.

### Tests

`tests/test_people.py` (storage layer: parsing, tolerant malformed
frontmatter, None/""/[] semantics), `tests/test_family_api.py` (validation,
died-before-born, unknown kind/partner dropped, symmetric sync, partner
removal cascades to unions on both sides), `tests/test_family_pages.py`
(person page rendering), and new `tests/test_life_events.py` (the pure
`birthdays_today`/`union_anniversaries_today`/`almanac_entries` functions,
plus route-level timeline banner and `/almanac` rendering). Verified live
with Playwright: created a person with born/died and a union with a
second person on a 390px mobile viewport, confirmed the reverse union
appeared on the partner's own page, confirmed the almanac listed both,
and confirmed a real 70th-birthday banner rendered on the timeline.

`pytest` (736: 694 existing + 42 new) and `ruff check .` green.

## F28. Firsts — a chronological register of milestones

The second of a batch of proposed features, following F27's life dates. A
parent wanted somewhere to see every "first" — first steps, first word,
first day of school — at a glance, in the order they actually happened,
each linking back to the story written about it (if any).

### Design

Not a new kind of record: a single optional field, `milestone` (a short
free-text label, capped at 80 characters), on the existing `Story`.
Whichever story you wrote about a first — a full story or a quick
instant — just gets that label, the same way it already gets tags or a
cover photo. This keeps the register a *view* over ordinary stories
rather than a parallel thing to maintain, and it means a first you
already wrote about doesn't need re-entering anywhere.

Deliberately not added to `instant.html`'s quick-capture form — F13's
whole point is "fifteen seconds on a phone," and a milestone label isn't
always known in the fifteen seconds it takes to snap a photo. An instant
is still editable afterward through the same shared `editor.html` used
for full stories (kind is preserved, everything else becomes editable),
so marking an already-captured instant as a first later is one field
away, without slowing down the capture itself.

### Storage (`storage.py`)

- `Story.milestone: Optional[str]`, tolerantly parsed (`_parse_milestone`
  — non-string or blank drops to `None`, same "files outlive edits"
  philosophy as everywhere else) and threaded through
  `create_story`/`save_story`/`_write_index`/`restore_version` with the
  established "`None` means leave unchanged, `""` clears" convention
  `cover`/`author` already use.
- New `stories_with_milestones(stories)`: `readable_stories` (so a draft
  or sealed first doesn't leak) filtered to `milestone` set — the
  register's data source, date-ascending like everything else that reads
  chronologically.

### API (`routes_api.py`)

- `_validate_milestone`: trim and cap at `MAX_MILESTONE_LENGTH` (80), no
  format constraint — free text, same tolerant-cap treatment as tags,
  not a validated field like a source URL.

### Editor UI

One more plain text input on `editor.html`, right under Tags:
placeholder "A first? (e.g. First steps)", `maxlength="80"`. No new
widget — same understated placeholder-only style tags already uses.

### Display

- Story page (`_story_article.html`): the milestone renders as a small
  accent-bordered pill under the title, unmissable but not shouting.
- Timeline: the same pill appears inline in each entry's row, next to the
  date/age — a first is worth noticing right there in the normal
  chronological flow, not just on a separate page.
- New `/firsts` page (`routes_pages.py`, `firsts.html`): every readable
  story with a milestone, oldest first, each row showing the milestone
  label, the date, and the story's title, linking straight to it. Linked
  from the timeline's footer-links row, but — same pattern as the
  Almanac link on `/people` — only when at least one milestone actually
  exists, so there's no dead link on a fresh install.

### Tests

`tests/test_storage.py` (round-trip, None/""/truncation semantics,
`stories_with_milestones` filtering and ordering),
`tests/test_api.py` (validation, empty-string clears, omitted leaves
unchanged, truncation via the API), and `tests/test_pages.py` (the
timeline pill, the story-page pill, `/firsts` listing/ordering/empty
state/draft-and-sealed exclusion, the conditional footer link, and an
auth check). Verified live with Playwright: created a story with a
milestone from the real editor, confirmed the pill on both the story
page and the timeline, and confirmed it appeared correctly on `/firsts`.

`pytest` (754: 736 existing + 18 new) and `ruff check .` green.

## F29. Growing up — the photo nearest each birthday

Third of the batch, following F27 (life dates) and F28 (firsts): "watch
them grow in one glance" — one photo per year of the child's life, the
one closest to their actual birthday, so flipping through the page reads
like a growth chart.

### Design

Pure derived view — no new data, nothing to write. It reuses whichever
story cover photos already exist and the same `STORYBOOK_BIRTHDATE`
config F3's "age at each memory" already depends on (not the newer
per-`Person` `born` field from F27 — `BIRTHDATE` is specifically the
book's subject, already wired everywhere age is shown, so this piggybacks
on that rather than introducing a second "whose birthday is this" source
of truth).

- New pure `storage.growth_photos(stories, birthdate, today=None)`: for
  every birthday from birth through today, picks the `readable_stories`
  cover photo whose date is closest to that birthday (globally nearest,
  not "the best in that year" — with a small/early photo collection,
  the same photo can legitimately be the nearest match for more than one
  birthday, and that's shown as-is rather than hidden). Reuses F5's Feb
  29 -> Mar 1 makeup rule for a leap-day birthdate. Empty list (not an
  error) when no readable story has a cover yet.
- `/growth` (`routes_pages.py`, `growth.html`): a responsive photo grid,
  oldest first, each card labeled "Newborn" (age 0) or "Turning {N}",
  captioned with the photo's actual date and story title, linking to the
  story. Three states: no `STORYBOOK_BIRTHDATE` configured (a short
  explanation of the env var, not a dead page), configured but no cover
  photos yet (a gentle nudge), and the populated grid.
- Linked from the timeline's footer row as "Growing up" — same
  conditional-link pattern as Firsts/Almanac, shown only once there's
  both a configured birthdate *and* at least one candidate photo.

### Tests

`tests/test_storage.py` (empty-when-no-covers, one entry per birthday,
nearest-overall selection, stops before future birthdays, Feb 29 makeup,
excludes covers-less/draft/sealed stories) and new `tests/test_growth.py`
(auth required, both empty states, a real listing with real uploaded
covers via the `dated_app`/`dated_auth_client` fixtures test_age.py
already established for `BIRTHDATE`-dependent pages, the conditional
timeline link, draft exclusion). Verified live with Playwright: created
two stories with real uploaded cover photos a birthday apart, confirmed
the "Growing up" link appeared only once a photo existed, and confirmed
the grid rendered both "Newborn" and "Turning 1" cards correctly.

`pytest` (767: 754 existing + 13 new) and `ruff check .` green.

## F30. A gentle nudge after a quiet spell

Last of the batch, after F27-F29. Not a notification, not a streak
counter, not a guilt mechanic — one quiet italic line on the timeline
when it's genuinely been a while: "Nothing new in 4 months — a little
story?", the "a little story?" itself linking to `/new`.

### Design

- New pure `storage.months_since_last_story(stories, today=None)`: whole
  months since the most recently *written* story, by `created` — not by
  the story's own `date`. Writing today about something from three years
  ago is real writing activity; it shouldn't itself read as "nothing new
  since three years ago." Includes drafts and instants (any of them is
  genuine engagement) and returns `None` when there are no stories at
  all, so a brand-new install is never nagged before it's begun.
- `QUIET_SPELL_MONTHS = 3`: the threshold below which nothing is shown —
  a routine week or two of quiet isn't "a quiet spell."
- Shown on the timeline only, styled like F16's writing-prompt line
  (muted italic serif, no box, no icon) — deliberately quieter than the
  boxed "X years ago today"/birthday/anniversary banners above it, since
  this is a nudge, not a notable occasion.

### Tests

`tests/test_storage.py` (no stories -> `None`, recent activity -> 0,
whole-month counting including the day-of-month boundary, most-recent-of-
several). `tests/test_pages.py` (no nudge right after writing; a nudge
after backdating a story's `created` field on disk — the same
hand-edited-frontmatter technique other tests already use — well past the
threshold). Verified live with Playwright: backdated a story's `created`
timestamp and confirmed the exact quiet italic banner text and link
rendered on the real timeline.

`pytest` (774: 767 existing + 7 new) and `ruff check .` green.

## F31. Year chapters in the book view

The fifth and last of the proposed batch (F27-F31), independent of the
other four: `/book` reads as one long scroll today; a printed/PDF copy
should feel like a real book instead, with a chapter divider — the year,
and the child's age — each time the calendar turns, not just a
continuous run of stories.

### Design

- `routes_pages.py`'s `book()` now tracks the previous entry's year while
  building the entries list and marks the first entry of each new year
  with `chapter_year` (and `chapter_age`, `dates.age_label(birthdate,
  story.date)` when `STORYBOOK_BIRTHDATE` is configured — reusing F3's
  existing age computation rather than inventing a second one). No new
  storage or data model — purely a grouping computed at render time from
  data that already exists.
- `book.html`: a centered `.book__year-chapter` divider (year, age
  subtitle, the same flourish rule used on every other page header)
  inserted before an entry whenever `chapter_year` is set. Screen-only:
  reads as a section break scrolling down the page.
- Print/PDF (the reason this exists): `.book__year-chapter` forces a page
  break before it (`break-before: page`), same mechanism the existing
  per-story `.book__story { break-before: page; }` rule already uses.
  The adjacent-sibling rule `.book__year-chapter + .book__story {
  break-before: avoid; }` cancels that first story's own break so it
  joins the chapter-title page instead of leaving a second, nearly blank
  page — the chapter divider *is* that page's opening, not a page unto
  itself. An instant right after a chapter divider needs no such override
  since instants never force their own break to begin with (F13:
  "interludes, not chapters").

### Tests

`tests/test_book.py`: one chapter per year (not per story), a
single-year book still gets its one chapter, an empty book shows no
chapter markup, the age subtitle appears only when `STORYBOOK_BIRTHDATE`
is configured. Verified live with Playwright across four stories
spanning three years: confirmed three chapter dividers in the right
order on screen, and — switching to print media emulation and reading
each element's computed `break-before` — confirmed every chapter forces
a page break while the story immediately after it does not, exactly the
intended pagination.

`pytest` (779: 774 existing + 5 new) and `ruff check .` green.

## F32. MCP server — an AI-assisted authoring surface

Requested directly, after a round of "what else could we add" brainstorming
landed on documentation: rather than (or in addition to) prose docs "for AI
tools," expose Storybook itself over
[MCP](https://modelcontextprotocol.io) so an assistant like Claude can read
and write stories/people as a genuine second way to author the book,
alongside the web editor.

### Scope decision

The request was explicitly for a **read-write** server (the same write
paths as the web editor, just invoked by an AI instead of a form) rather
than a read-only context server. Given this app's data is a private
journal with a child's photos, that's a real trust decision, made
knowingly: the mitigating factor is that this server only ever runs
locally over stdio, launched directly by an MCP client on the same
machine — it is not part of the Flask app, has no network listener, and
carries no login of its own. The trust boundary is identical to running
the app locally in the first place (whoever can launch the process already
has filesystem access to `stories/`), so it adds no new remote attack
surface. It must never be pointed at a network-reachable transport.

### Dependency tradeoff

New pinned dependency `mcp==1.28.1` (`requirements.txt`) — the official
Python SDK, used rather than hand-rolling JSON-RPC framing/handshake
compliance (the same "don't roll your own protocol" reasoning F26 applied
to CSRF tokens). Worth being explicit about the cost: this pulls in ~25
transitive packages (`starlette`, `uvicorn`, `pydantic`, `httpx`,
`cryptography`, `jsonschema`, ...) for HTTP/SSE transport support this app
never uses, a real departure from the "boring, minimal dependencies"
philosophy. It's an optional add-on (`mcp_server.py` is a separate
entrypoint from `run.py`; the Flask app never imports it), so a deployment
that doesn't want the extra dependency weight can simply not install/run
it — nothing in the web app depends on `mcp` being present.

### Design

- `app/mcp_server.py`: a `FastMCP` instance with 11 tools, wired to the
  exact same `storage.py`/`people.py` functions the web editor's routes
  call — atomic `index.md` writes, `.versions/` snapshots on every save,
  Pillow re-encoding for photos, symmetric partner/union syncing (F18/F27).
  This module never touches a story/person file directly itself; it only
  adds MCP-shaped argument validation (raising `ValueError` on bad input,
  which FastMCP turns into a proper tool-error result rather than a server
  crash) and tool wiring on top.
  - Read: `list_stories` (filterable by tag/person/milestone/date range),
    `get_story`, `list_people`, `get_person`, and `get_journal_context` — a
    single snapshot tool (total/draft/readable story counts, the most
    recent story, `months_since_last_story`/quiet-spell status from F30,
    today's birthdays/union anniversaries from F27, the firsts count from
    F28, the child's age today from F3 if `STORYBOOK_BIRTHDATE` is set,
    and a random writing prompt from F16) meant to be the first call an
    assistant makes, so it has context before creating anything.
  - Write: `create_story`/`update_story`, `add_story_photo`,
    `create_person`/`update_person`, `set_person_photo`.
- Config is read from the same `STORYBOOK_STORIES_DIR`/`STORYBOOK_AUTHORS`/
  `STORYBOOK_BIRTHDATE`/`STORYBOOK_TITLE` environment variables
  `app/__init__.py`'s `create_app()` uses, re-parsed locally rather than
  imported from `app/__init__.py` — same "don't import back into
  `app/__init__.py`'s internals" convention `people.py` already follows for
  `_AUTHOR_COLOR_RE`. This module is never imported by `app/__init__.py`
  and doesn't require the Flask app to exist at all.
- `update_story`/`update_person` follow the rest of the app's "None means
  leave unchanged, empty clears" convention for optional fields, with one
  deliberate deviation from the web route's behavior: `draft`/`archived`
  default to *leaving the current value unchanged* when omitted, rather
  than the HTTP form's "always resend the checkbox, so an absent field
  means false" rule. A web form's checkboxes are always visibly present;
  an AI-driven partial update is not, so defaulting an omitted `draft` to
  `False` could silently un-draft a story the assistant never meant to
  touch. `title`/`date`/`body` (`name`/`body` for people) stay always-
  required/always-overwritten, matching the web routes exactly.
- Photo uploads (`add_story_photo`, `set_person_photo`) take
  base64-encoded image bytes (a `data:image/...;base64,` prefix is
  stripped if present) instead of a multipart file, decoded into a tiny
  adapter object exposing the `.stream` attribute `storage.save_image_to`
  expects from a Werkzeug `FileStorage` — every other guarantee (Pillow
  re-encoding, thumbnailing, EXIF transpose) is identical to a web upload.
  Voice memos and zip import/export are deliberately not exposed as tools
  in this first version.
- `mcp_server.py` at the repo root is a two-line launcher (`from
  app.mcp_server import mcp; mcp.run(transport="stdio")`), mirroring
  `run.py`'s relationship to `create_app()`.

### Tests

New `tests/test_mcp_server.py` (41 tests) calls the tool functions
directly — the `@mcp.tool()` decorator returns the original function
unchanged (confirmed against the installed SDK's source), so no MCP
transport is needed to test the create/read/update logic, validation
errors, photo uploads, partner/union symmetry (including the F27
orphaned-union-on-partner-removal case), author validation against
`STORYBOOK_AUTHORS`, and `get_journal_context`'s fields. Also verified
once, live, over the real protocol: spun up the server with the SDK's
in-memory client transport, called `list_tools` (confirmed all 11 appear
with schemas derived from the type hints/docstrings), `create_story`
end-to-end, and a deliberately-invalid `get_story` call (confirmed it
comes back as a tool error result, not a crash) — proving the plain-Python
tests reflect what a real MCP client actually sees.

`pytest` (820: 779 existing + 41 new) and `ruff check .` green.

## F33. Help — an in-app, plain-language guide for the family

While improving documentation for maintainers/AI agents (this file's new
Index above, and README's dependency table alongside F32), the gap on the
other side became obvious: everything explaining *how the app works* —
what a Story vs. an Instant is, what sealing a letter does, what a
milestone is — lives only in `README.md`, which the actual family reading
the timeline (not the person who set the app up) will likely never open.
There was no in-app help at all.

### Design

- New `/help` route (`routes_pages.py`, `help_page()`) rendering a single
  static template, `help.html` — no dynamic data needed beyond
  `config.ACCOUNTS_ENABLED` (already a Jinja global via Flask's `config`
  context), so the route itself is a one-line `render_template` call.
- Content is a condensed, friendly rewrite of README's feature tour aimed
  at the person actually using the app day to day, not a developer:
  writing (Story vs. Instant, drafts, sealed letters, milestones), the
  cast (people, family tree, life dates/almanac), growing up, reading it
  back (timeline, random page, on-this-day, book/EPUB), voice memos, and
  backing up. The family-accounts section is conditional on
  `STORYBOOK_ACCOUNTS=1`, same guard-on-config convention every other
  accounts-specific UI element already follows.
- `help.html` follows the same static-page template shape as
  `almanac.html`/`firsts.html`/`growth.html`: a `__back` link to the
  timeline, an `<h1>`, the shared rope-divider flourish, then a series of
  `<section>` blocks. Deliberately scoped as one page, not a multi-page
  manual or an interactive tour — "book, not blog" applies to the help
  text too.
- Linked from the main nav (`base.html`, next to "People") rather than
  the timeline's footer-links row, since — unlike Firsts/Growing Up —
  it's always relevant regardless of what data exists yet.

### Tests

New `tests/test_help.py`: requires auth, renders every core section,
hides/shows the family-accounts section based on `STORYBOOK_ACCOUNTS`
(using the existing `_bootstrap_admin`/`_login` account-flow test
helpers, since accounts-mode login isn't the shared-password login the
other test fixtures use), and confirms the nav link appears only when
logged in. Verified live with Playwright at both a desktop width and a
390px mobile viewport, and confirmed clicking the nav's new "Help" link
actually navigates to `/help`.

`pytest` (826: 820 existing + 6 new) and `ruff check .` green.

## F34. Taking a photo, not just adding one

Every way of getting a photo into the book assumed the photo already
existed: the instant form, the story editor's image button, and the
person editor's Photo panel all opened the OS file picker. On a phone
that picker does offer the camera, so this was survivable — but on a
laptop with a webcam there was no camera at all, and even on a phone
"take a photo of this drawing right now" meant a round trip out to the
camera app, into the gallery, back into the picker.

F12 already records audio in the browser with `getUserMedia`; this is the
same idea for the lens instead of the microphone.

### Design

- **`app/static/js/camera.js`** — one shared full-screen overlay
  (`window.StorybookCamera`), built in JS rather than duplicated into
  three templates. `open()` returns a `Promise<File|null>`: a JPEG `File`
  shaped exactly like one an `<input type="file">` would hand over —
  which is the whole point, since every existing upload path (re-encode
  with Pillow, `photo-NNN.jpg` naming, thumbnails, HEIC conversion,
  cropper) then works untouched. `null` means the user backed out. No new
  endpoint, no new storage code, no server change of any kind.
- Live preview → shutter → **review step** ("Retake" / "Use photo"), so a
  blurry frame never reaches the book. Also: "Flip" (shown only when
  `enumerateDevices` reports two or more cameras), "Cancel", Escape, and
  the phone's back gesture (a `history.pushState` on open, mirroring F7's
  lightbox) — all of which stop every track, so the camera light goes out
  the moment the overlay closes.
- The selfie camera previews mirrored (`scaleX(-1)`) but is *captured*
  raw, matching what every phone camera does: you see yourself the way a
  mirror shows you, the book keeps the photo the way everyone else sees
  you.
- **`app/static/js/camera-logic.js`** — the DOM-free half (frame scaling,
  the front/back toggle, capture filenames) as a UMD module with Node
  tests, per the repo's rule about testable client logic. `captureSize`
  caps the longest edge at 2000px to match `storage.MAX_IMAGE_EDGE` (the
  server re-encodes to that anyway, so this only saves upload bytes) and
  returns `null` for a 0×0 `<video>`, which is how a not-yet-ready stream
  is told apart from a real frame.

### Where it appears

- **`/new-instant`** — a "Take a photo" button under the photo picker.
  The capture and a picked file are deliberately exclusive: choosing one
  clears the other, so the preview and the save always agree on which
  photo is *the* photo. The file input lost its `required` attribute for
  this — a camera photo never reaches the input, so the browser would
  otherwise block a save that does have a photo (the JS check that was
  already there still catches a genuinely empty form).
- **The story editor** — a "Photo" section above "Voice", symmetric with
  it. The capture uploads through the existing images endpoint and is
  inserted at the cursor as `![](photo-NNN.jpg)`. It sits beside the
  toolbar's image button rather than replacing it: that one adds a photo
  you already have, this one takes a new one. Insertion goes through a
  new `insertImage` method on both editor wrappers (Toast UI's
  `exec("addImage", …)`, and a cursor splice in the no-JS-editor
  fallback), which also de-duplicated the fallback's existing insert.
- **The person editor** — a "Take a photo" button beside "Add a
  photo"/"Change photo". The captured file goes straight into F18's
  existing pan/zoom cropper, so a portrait taken in the app is framed and
  toned exactly like an uploaded one.

### Degrading gracefully

`getUserMedia` requires a secure context. Over plain LAN HTTP
`navigator.mediaDevices` is undefined, `isSupported()` is false, and
every "Take a photo" button stays hidden — the file inputs are untouched
and remain the way in. This is the same bargain F12's voice memos already
make, and it's why all three buttons ship `hidden` in the template and
are unhidden by JS, never the reverse. Denied permission, no camera, and
a camera busy in another app each get their own message inside the
overlay instead of a dead button.

### Tests

- `tests/js/camera_logic_test.mjs` (13 assertions: scaling both
  orientations, aspect-ratio preservation, the not-ready 0×0 case, the
  facing toggle, filename formatting), wired into pytest via
  `test_tree_logic_js.py` like the other Node suites.
- `tests/test_camera.py` covers the server-rendered contract the scripts
  hang off: the camera scripts load on exactly the three pages that can
  add a photo and on none of the reading pages, every button ships
  hidden, the instant photo input is no longer `required`, and a
  `camera-<timestamp>.jpg` upload round-trips through the images endpoint
  and can become an instant's cover.
- Verified live in Chromium with a fake webcam
  (`--use-fake-device-for-media-stream`) at 390px and at 1280px, in both
  themes: capture → retake → use on all three surfaces, an instant saved
  from a capture appearing on the timeline, a captured photo rendering on
  the saved story page, a captured portrait surviving the cropper, and
  Escape/back/Cancel all closing the overlay without touching the form.

`pytest` (835: 826 existing + 9 new) and `ruff check .` green.

## F35. Photos that look right everywhere

Adding the in-app camera (F34) made it obvious how many photos a story
now collects, and three things about how they rendered were not neat.

### The problem

**A photo added in the editor showed as a broken image.** Story markdown
stores image links as bare filenames — `![](photo-001.jpg)` — on purpose:
the folder has to stay readable and movable without the app, so
`rendering.py` is what resolves a bare src to `/story/<id>/media/<file>`
at render time. The browser editor has no such step. It resolves
`photo-001.jpg` against the page URL (`/new`, `/edit/<id>`) and gets a
404, in both the WYSIWYG pane and the markdown preview pane. The photo
was uploaded and saved correctly and appeared on the story page; only the
editor's own view of it was wrong. That's still the worst place for it to
be wrong, because it's the moment the writer is deciding whether the
photo belongs there.

**Two photos added in a row rendered as raw inline images.** Both the
camera button and the toolbar's image button insert at the cursor, so
clicking twice produces `![](a.jpg)![](b.jpg)` in one paragraph. The
figure rule only fired for a paragraph holding exactly one image, so a
pair fell through to bare `<img>` — no `<figure>`, none of the figure
styling, no caption, not clickable for the F7 lightbox.

**An image sharing a paragraph with text overflowed the page.** Nothing
styled a non-figure image at all, so a 1920px photo rendered at 1920px
inside a 632px column and ran off the side, on the story page and in the
book alike.

### The design

**Editor preview** — `app/static/js/media-links.js`, a small UMD module
with `toEditorMarkdown` / `toStoredMarkdown` / `toEditorSrc`. Bare
filenames are expanded to real media URLs on the way *into* the Toast UI
editor and collapsed back to bare filenames on the way *out*. Both
directions apply the same "is this absolute?" test `rendering.py` uses,
so external URLs, root-relative paths and another story's media URL are
all left exactly as written; only a single path segment under this
story's own media base ever collapses.

The conversion hangs entirely off the wrapper object `createToastEditor`
already returns — `getMarkdown` / `setMarkdown` / `insertImage`, plus
`initialValue` and `addImageBlobHook`. Everything outside that wrapper
(saving, autosave, the dirty check, the fallback textarea editor) keeps
seeing bare filenames and needed no changes. Nothing about the saved file
changed: `index.md` still stores `![](photo-001.jpg)`.

The markdown-source pane now shows the full media URL rather than the
bare filename. That's the deliberate trade: it's what makes the preview
pane resolve, and the WYSIWYG pane — the default — is where nearly all
writing happens.

The alternative, storing resolvable URLs in `index.md`, was rejected
outright: it would pin every story to the app's URL scheme and break the
"delete the app and the folder still works" guarantee.

**Stacked figures** — `rendering.py`'s rule widened from "a paragraph
holding exactly one image" to "a paragraph holding nothing but images",
emitting one `<figure>` per image. `![](a.jpg)![](b.jpg)` and
`![](a.jpg)\n![](b.jpg)` now both render as two proper stacked figures.
Fixed at the render layer rather than by making the editor insert block
breaks: driving Toast UI's block structure means poking at the vendored
build's ProseMirror internals, and the failure mode is `<br>` litter
written into someone's `index.md` — a bad trade in an app whose whole
point is clean files. Fixing it in `rendering.py` also repairs stories
that already exist, including imported backups and hand-written markdown.

**No overflow** — `.story__body img` finally has a rule of its own
(`max-width: 100%`, `height: auto`, and the same rounded corners the
figures have). An image genuinely mixed in with text stays inline,
because that is what the author wrote, but it can no longer break out of
the column. The print stylesheet already had `max-width: 100%`; this
brings the screen in line with it.

**Lightbox** — F7's selector widened from `.story__body figure img` to
`.story__body img`, so an inline photo is zoomable like every other one.
`story.js` skips an image the author wrapped in a link (that click
belongs to the link) and adds a `story__zoomable` class to the images it
actually wired up, so the zoom cursor only ever appears on something that
really does zoom.

### The book

Unchanged, and confirmed working: `/book` renders every story through the
same `render_markdown` with that story's media base, and `/book.epub`
rewrites those srcs to epub-relative paths and packs the real image bytes
into the zip. Verified end to end — 8 images embedded, every `src` in the
XHTML resolving to a file in the archive, nothing broken or overflowing
on the book page.

### Tests

- `tests/js/media_links_test.mjs` (23 assertions: expansion, collapsing,
  alt text and link titles surviving, absolute/protocol-relative/
  root-relative URLs left alone, plain links untouched, a byte-for-byte
  expand→collapse round trip), wired into pytest via
  `test_tree_logic_js.py`.
- `tests/test_editor_images.py` — the contract the script depends on
  (both editors ship `media-links.js` and a `data-media-url-template`,
  loaded before `editor.js`, and the template really is the URL that
  serves the file) plus the invariant it protects (a saved body still
  holds bare filenames; an absolute media URL that somehow reaches
  `index.md` still renders).
- `tests/test_rendering.py` — stacked figures from glued and
  soft-broken images, text-mixed images staying inline, a linked image
  staying a link, images-only paragraphs keeping their neighbours, list
  items and blockquotes behaving.
- Verified live in Chromium: photos loading in both editor panes via the
  toolbar button and the camera, on a new story and a reopened one, in
  the person editor against its own media base, `index.md` unchanged
  across a resave, zero console errors, no image wider than its column on
  any story or in the book, and the lightbox opening from an inline
  image.

`pytest` (851: 835 existing + 16 new) and `ruff check .` green.

## F36. Hardening for the open internet

Written for the moment this stops being a LAN app: a NAS, a port forward,
and photos of a real child behind one login form. Earlier rounds
(REVIEW.md items 1–4, F19's hashing and token design) already closed the
classic holes — CSRF everywhere, HttpOnly/SameSite/Secure cookies,
constant-time compares, salted account hashes, 32-byte write-link tokens
stored hashed, re-encoded uploads, allowlisted paths, zip-slip
protection, fail-fast secret key. What was still missing was specific to
being reachable by strangers, and this feature adds exactly that.

### Brute-force lockout (`app/throttle.py`)

`time.sleep(1)` on a failed login slows one connection; it does nothing
against parallel guessing, and each sleeping request holds a waitress
thread. `FailureThrottle` is a pure sliding-window counter (no Flask, no
clock of its own — `now` is a parameter, so tests never sleep): after 10
failures per key per 15 minutes, further attempts get an immediate 429
with `Retry-After`, before any password check runs — a blocked client
learns nothing, not even whether its last guess was right. The key is the
client IP; a successful login clears it, so a family member who fumbled
their password isn't one typo from a lockout all evening. GETs of the
login page are never throttled — a blocked person can still see the form
and the "try again in N minutes" message.

Both password-bearing endpoints share one throttle instance: `/login`
and, in accounts mode, `/request-account` — the invite code *is*
`STORYBOOK_PASSWORD`, so guessing it there is guessing the login
password, and failures on either count against the same key.

State is in-memory and per-process, which fits: waitress is one process,
and a restart forgiving the counters costs an attacker nothing the window
wouldn't forgive minutes later anyway. No dependency added.

`STORYBOOK_TRUSTED_PROXIES=<n>` (default 0) wraps the app in werkzeug's
`ProxyFix` so `remote_addr` is the visitor's real IP behind a reverse
proxy — without it, the whole internet shares the proxy's address and the
first attacker to trip the limit would lock the family out too. Off by
default because trusting `X-Forwarded-For` when no proxy sets it lets
clients fake their IP past the throttle.

### Security headers, and a CSP with teeth

One `after_request` in `create_app()` puts on every response:
`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`,
`Referrer-Policy: same-origin`, `Strict-Transport-Security` (only when
`STORYBOOK_COOKIE_SECURE=1` says HTTPS is real), and a strict
`Content-Security-Policy`: `default-src 'self'`, `script-src 'self'`,
`frame-ancestors 'none'`, `form-action 'self'`, `object-src 'none'`,
plus `blob:` for the camera/cropper/instant previews and `data:` for
Toast UI's embedded icons. The policy names no external host — the no-CDN
rule, enforced by the browser.

The CSP is not checkbox security here. Story bodies are rendered with
`|safe` by design (trusted family), but F19 delegates and write-link
holders are only semi-trusted — and with `script-src 'self'` and no
inline scripts, a `<script>` tag or `onerror=` handler smuggled into
markdown is refused by the browser. Verified live: an injected
`window.__pwned` script in a story body does not run, and the console
shows the CSP refusal. The one inline `<script>` the app had (the
theme-boot snippet in `base.html`, which must run before first paint)
moved to `static/js/theme-boot.js`, still a blocking script in `<head>`,
so the policy needs no nonces and no `unsafe-inline` for scripts.
`style-src` keeps `'unsafe-inline'` for the `--author-color` /
`--photo-sepia` custom-property attributes — style injection is a far
smaller risk than script, and the trade was worth zero nonce plumbing.

### Cache privacy

HTML pages are personal content behind a login: `Cache-Control: no-store`
on every one, so nothing lands in a disk cache or an intermediary. Media
and static files keep their long `max-age` (F-lightbox-era design, safe
because photo filenames are immutable) but now carry `private`, so only
the logged-in family member's own browser caches them — never a shared
cache along the way.

### The auth-perimeter test

The guardrail that matters most long-term: `tests/test_security.py`
walks the entire `url_map` and asserts every GET route refuses an
anonymous client except the four deliberately public endpoints (`/login`,
`/manifest.webmanifest`, `/request-account`, `/w/<token>` — plus
static). A future page added without `@login_required` fails CI the day
it's written, and a second test pins the allowlist itself so a new
public endpoint is always a conscious decision in a diff.

### Deployment guidance

README gained "Opening it to the internet": VPN-first advice (WireGuard/
Tailscale — the safest option is an unreachable login page), then the
checklist for real exposure — HTTPS-only with a real certificate,
`STORYBOOK_COOKIE_SECURE=1`, `STORYBOOK_TRUSTED_PROXIES=1`, a long
passphrase, host patching, never exposing the MCP server, off-box
backups — and an honest closing: nothing is "unhackable"; what remains
rides on the password and the TLS in front.

### Tests

- `tests/test_throttle.py` — the pure counter: blocks at the limit and
  not before, unblocks when the oldest failure ages out, per-key
  independence, `clear()` on success, `retry_after` countdown, bounded
  memory.
- `tests/test_security.py` — headers on the wire (CSP directives, no
  external host in the policy, HSTS only under HTTPS, `no-store` pages,
  `private` media), lockout behavior end-to-end (429 after the limit,
  right-password-while-blocked still 429 and still logged out, success
  clears, GET never throttled, invite-code form shares the lockout), no
  inline `<script>` in any rendered page, and the perimeter walk.
- Verified live in Chromium with the CSP active: the Toast UI editor,
  image upload + preview, the F34 camera (blob: preview), the voice
  recorder, the portrait cropper, the family tree (d3 + family-chart),
  book/timeline/almanac/help all work with zero console errors — and the
  injected-script story is neutralized.

`pytest` (873: 851 existing + 22 new) and `ruff check .` green.

## F37. Every error is a real page

Found while reproducing a reverse-proxy problem on a phone viewport, and
partly caused by F36.

### The problem

`404.html` extended `base.html`, so a missing page looked like the app.
Every *other* error fell through to Werkzeug's built-in page: bare HTML,
no stylesheet, and — the part that matters — **no `<meta name="viewport">`**.
Without that tag a phone lays the page out at 980px and zooms out, so
"Bad Request" renders as a few words of unreadable type floating in a
desktop-width void. Measured on a 390px iPhone viewport:
`clientWidth: 980`, `styleSheets.length: 0`, `viewportMeta: null`. It
doesn't read as "one request failed", it reads as "the whole site is
broken".

That was largely theoretical while 400s were hard to reach. F36 changed
that: Flask-WTF's `WTF_CSRF_SSL_STRICT` referrer check only runs when
`request.is_secure`, and `request.is_secure` only became true behind a
reverse proxy once F36 added `ProxyFix`. On a proxy that doesn't forward
the browser's real host, *every* form submission — login included — now
400s. So F36 turned a rare ugly page into a likely one, and this fixes it.

### The design

A shared `error.html` (extending `base.html`, reusing the `empty-state`
layout and the tumbleweed illustration) plus a `_error_page` helper, and
handlers for 400, 403, 413, 429, 500 and `CSRFError`. Each gets a plain
heading and a sentence written for a family member, not an operator:
"That file is too big", "Something went wrong — that's a fault in the
app, not anything you did. Your stories are files on disk and are
unaffected."

`/api/*` paths keep returning JSON from the same helper, so the editor's
`fetch` error handling is unchanged (this also fixed `/api/*` 404s, which
had been returning the HTML 404 page to JSON callers).

The CSRF handler is the interesting one. A CSRF failure is nearly always
one of two ordinary things, and the page says which:

- **A stale tab** — "That page had gone stale… nothing was saved or
  lost." The reassurance is the point; a CSRF error looks alarming.
- **A misconfigured reverse proxy** — when the failure is specifically
  the referrer check, an extra hint names it: check that the proxy sends
  `X-Forwarded-Host` and `X-Forwarded-Proto`, and that
  `STORYBOOK_TRUSTED_PROXIES` is set. Anyone hitting this is otherwise
  stuck staring at "Bad Request" with no thread to pull.

The referrer check itself is left on. It's real defense-in-depth, and the
correct fix for a proxy that trips it is to configure the proxy, not to
switch a security check off.

### Tests

`tests/test_error_pages.py`:

- Each of 400/403/413/429 renders with the viewport meta and the
  stylesheet — the exact two things whose absence caused the mobile bug.
- `/api/*` equivalents stay JSON, and the 413 message still names the
  128 MB limit.
- A CSRF failure is a readable page, says "nothing was saved or lost",
  and never says "Bad Request"; on the API it's JSON.
- A referrer mismatch over HTTPS names the reverse proxy and
  `X-Forwarded-Host`; a *matching* referrer over HTTPS still logs in, so
  the guard can't fire on a correctly configured setup.

Also verified by standing up a real HTTPS reverse proxy (self-signed
cert, forwarding to the app with DSM's `X-Forwarded-*` headers) and
driving it in Chromium at 390px with an iPhone user-agent: through a
correctly configured proxy every page lays out at 390px with all CSS
loaded and zero failed requests, and the CSRF page now does too.

`pytest` (888: 873 existing + 15 new) and `ruff check .` green.

## F38. The interface in French

The README's "Ideas for later" listed i18n as deliberately out of scope,
with the note that if it ever became worth doing it belonged in a
discussion rather than a surprise PR. This is that discussion resolved:
the book is for a French family, and a grandmother reading it should not
have to work around an English interface.

### What is and isn't translated

The **interface** is translated. What the family **wrote** never is —
story titles, bodies, tags, milestone labels, people's names, relation
lines. Two readers of the same book see the same memories with different
furniture around them. This is the whole design constraint: translation
is a rendering concern, and `stories/` on disk is untouched by it. Not a
byte of the storage format changed.

### Why not Flask-Babel

It was the obvious choice and was rejected: `.po`/`.mo` files need
`pybabel` to compile them, which is a build step, and this project has
none and wants none (CLAUDE.md). What it buys — plural rules for
languages with more than two forms, message extraction tooling — is
overkill for two languages that both have exactly two.

Instead `app/i18n.py` is a dict lookup, a plural rule, and a date
formatter, with the French strings in `app/translations_fr.py`. No new
dependency.

Keys are the **English source strings**, so templates stay readable
(`{{ _("Back to the timeline") }}`) and a missing entry degrades to
English rather than to a raw key like `error.notfound.title`.

### The picker

Two flags in the nav, present on every page including `/login` — someone
who can't read English has to be able to switch *before* typing a
password, so the route is deliberately not `@login_required`.

- **Inline SVG flags**, not emoji. Emoji flags were the shortcut and were
  rejected: Windows renders them as bare letters, defeating the entire
  point. Each flag carries its `EN`/`FR` code beside it anyway, and the
  buttons are 68×44px — a real tap target on a phone.
- **One tiny POST form per language**, not a `<select>` plus JS: it works
  with JavaScript off and is CSRF-protected like every other state change.
  A hidden `next` field carries the current path so switching leaves you
  on the page you were reading — through the same local-paths-only
  allowlist as the login redirect, so it can't become an open redirect.
- The current language is dimmed and marked `aria-current` rather than
  removed, so the row never reflows when you switch.

### Where the choice lives

A one-year `storybook-lang` cookie, not the session and not a per-account
setting. It has to survive logging out, and it has to work before there
is an account at all (the login page, and the F19 request-account page).

Resolution order per request: **the reader's own choice → their browser's
`Accept-Language` → the book's own `STORYBOOK_LANGUAGE` → English**. A
French phone therefore gets French on its very first visit without
touching anything, and regional tags match their base language so `fr-CA`
and `fr-BE` both land on French.

`STORYBOOK_LANGUAGE` exists because this is one family's book, not a
public site: a visitor arriving at a French family's book with no
preference of their own should be greeted in French. It sits *below* the
browser preference deliberately — an English-speaking relative visiting a
French book still gets English rather than a wall of French — and below
the reader's own pick, which always wins and is one tap away either way.

### Dates, and why not strftime

`strftime("%B")` is locale-dependent and needs the locale generated on
the host, which a slim Docker image doesn't have; `%-d` is glibc-only
besides. A month-name lookup table is smaller, deterministic, and
identical everywhere. French also isn't English with the words swapped:
the day comes first, there's no comma before the year, and the first of
the month takes an ordinal — `1er mai 2026`, not `1 mai 2026`.

Plural rules differ too: French keeps the singular at zero ("0 jour"),
English doesn't ("0 days"). `ngettext` handles it per language, which is
also how F3's age labels became `3 ans` / `1 jour` / `avant ta naissance`.
The arithmetic behind those moved into `dates.age_parts()` so both
languages share one implementation of the month/day rounding.

Register note: the app addresses the child directly in a few places, and
the French keeps that familiar tone — "tu", never "vous".

### Tests

`tests/test_i18n.py`, and the first one is the one that matters:

- **Coverage** — walks every template, collects every string passed to
  `_()`/`_n()`, and fails if any lacks a French entry. Add an
  untranslated string and CI fails the day you write it. "Falls back to
  English" stays a safety net rather than the normal state.
- **Quality guards** on the dict itself: no French value identical to its
  English key (with an explicit allowlist for words that really are the
  same — *Parents*, *Sources*, *Zoom*…), none empty, and placeholders
  (`{n}`, `{name}`) preserved on both sides so interpolation can't
  silently drop a number.
- Language resolution: cookie beats browser, quality values honoured,
  regional tags matched, unknown/garbage input falls back to English.
- Dates and plurals in both languages, including `1er`, and the fact that
  no month name is missing.
- The picker and cookie end to end: present on `/login`, switching
  changes the page and `<html lang>`, survives logout, an unknown code is
  404 with no cookie set, the redirect can't be turned into an open
  redirect, and GET is 405.
- **Story content is never translated** — a story titled "People" still
  says "People" on a French page.

Verified in Chromium at 390px and 1280px: switching on the login page
before logging in, the choice surviving login, no English left on the
timeline/editor/people/help/book, French dates on the timeline and story
pages (`18 juin`, `18 juin 2023 · 0 jour`), no horizontal overflow, and
zero console errors.

`pytest` (923: 888 existing + 35 new) and `ruff check .` green.

---

## F39. Invitations, open requests, and not letting one person in twice

F19 Phase 2 gave the app a request queue: a stranger who knows the shared
invite code fills in a form, and an admin approves or rejects it from
**Accounts**. That flow was already admin-validated — but in use it turns
out to answer only one of the three questions a family actually has about
letting someone in, and to answer that one from the wrong end.

The three, and what this feature does about each:

1. **"I want to add my mother, but she'd have to pick a password and send
   it to me."** Approving a request means the newcomer set their
   credentials before the admin ever saw the request. There was no way to
   go the other direction — decide first, let them fill in the rest. Now
   there is: an admin-issued **invitation**.
2. **"My cousin found the book but was never given the code."** The invite
   code was mandatory, so "just ask, and wait" wasn't expressible.
   `STORYBOOK_OPEN_REQUESTS=1` makes the code optional.
3. **"How do I know this isn't the same person again?"** Username
   uniqueness and one-account-per-Person were already enforced; the same
   human requesting twice under two usernames was not, and can't be, since
   this app has no email address to key an identity on. The honest answer
   is to put the likely match in front of the admin at the moment they
   decide.

Nothing here changes the permission model. F19 said plainly that an
approved family account can read and edit the whole book, and that stays
true — this is entirely about *how someone gets a login*, not what a login
can then do.

## Invitations (`app/invites.py`)

An admin opens **Accounts → + Invite**, picks the Person (an existing one
with no account, or a new one created from a name on the spot) and the
role, and gets back a URL to send. The recipient opens it, chooses their
own username and password, and is redirected to the login page to use
them.

```
stories/people/mamie-rose/
  index.md          # the Person, untouched
  invites.json      # this feature
  account.json      # appears once the invitation is accepted
```

Mechanically this is `write_links.py` again — a `secrets.token_urlsafe`
bearer token with only its SHA-256 hash persisted, an expiry, a revoke
flag, a bounded scan across `people/*/invites.json` to resolve a token.
The same fast-hash reasoning applies: ~192 bits of entropy needs a hash
that isn't reversible, not one that resists brute force on a weak input.

**Why a separate module rather than generalising `write_links.py`.** The
two look alike and behave differently everywhere it counts. A write-link
grants one story and never an identity; an invitation grants a real login
and nothing else. An invitation is always single-use, always carries a
role, and dies the moment its Person acquires an account by any other
route — none of which a write-link has an opinion about. Merging them
would mean a shared record where half the fields are inapplicable to
whichever kind you're holding, which is how a "token" table ends up being
the thing nobody dares touch.

Decisions worth stating:

- **Re-issuing revokes the previous invitation.** One seat, one live
  token. An admin re-sending because the link was lost, or went to the
  wrong chat, should end up with exactly one thing that works — and only
  one could ever be redeemed anyway, since accepting creates the account
  that makes every other invitation for that Person invalid. Making that
  explicit at creation beats leaving a stale token alive until someone
  discovers it doesn't work.
- **History survives.** Revoked and accepted invitations stay in the file;
  only `list_all_active` filters them out. How an account came to exist is
  worth keeping, and this app doesn't delete things.
- **Accepting never logs you in.** It redirects to the login page instead.
  An account that has never survived a real login round-trip is one typo
  away from needing an admin password reset; this way the typo surfaces
  while the person is still at the keyboard. It costs one extra form
  submission and removes the app's most annoying possible support call —
  there being no email, and therefore no self-service reset.
- **Every uniqueness rule is re-checked at acceptance, not trusted from
  creation.** An invitation can sit in an inbox for two weeks while the
  world changes: the Person may have been given an account directly, and
  the chosen username may have been claimed by an account or by a request
  still sitting in the queue. `accept_invite` re-validates all of it.
- **`LookupError` vs `ValueError`.** The route has to distinguish "this
  link is dead, show the invalid page" from "your form is wrong, try
  again" — and getting that backwards would either burn a good invitation
  on a typo or keep showing a form for a token that can never work.
  `accept_invite` raises `LookupError` for the first and `ValueError` for
  the second, so the route branches on the exception type rather than on
  string-matching a message.

## Open requests (`STORYBOOK_OPEN_REQUESTS`)

Off by default; requires accounts mode. When on, the invite code field on
`/request-account` becomes optional and the page's wording changes from
"ask whoever set this up for the invite code" to "ask to join, and someone
in the family will let you in."

Two properties are load-bearing rather than incidental, and both have
tests named after them:

- **A codeless request can never become the bootstrap admin.** The very
  first request ever submitted auto-approves as admin — there being no
  admin yet to review it. Opening the form up without guarding that would
  hand the entire book to the first stranger to find a freshly deployed
  install. `approve_if_first` now only runs when the code was actually
  supplied and correct.
- **A wrong code is still a wrong code.** Only *omitting* it is newly
  allowed. Submitting a wrong one fails and counts against the F36
  throttle exactly as before, so the code doesn't become guessable one
  attempt at a time by anyone who noticed the field went optional.

An open form is also an unauthenticated endpoint that appends to a file on
disk, so `accounts.MAX_PENDING_REQUESTS` (25) caps the queue. Rejecting
frees a slot, as it already freed the username. The number is set so a
real family never meets it: an admin with 25 people genuinely waiting has
a reviewing problem, not a capacity one.

Considered and rejected: rate-limiting requests per IP on top of the cap.
The existing throttle is shared with login, so spending its budget on the
request form would let someone lock the family out of their own book by
spamming a public form — the cap achieves the same protection without
handing an attacker that lever.

## Duplicate hints

`accounts.similar_people(all_people, display_name)` — pure, takes the list
of People rather than a directory, compares through `storage.slugify` so
case, accents and punctuation fold together ("Jean-Luc" matches "jean
luc"). An exact match counts at any length; "one contains the other" only
counts once both names are at least 4 characters, or "Jo" would flag every
Joseph and Jocelyne in the book and the hint would become noise the admin
learns to skip.

Shown in two places, worded by severity: on the **Accounts** list as a
quiet inline note, and on the **Review request** screen as a warning. A
match that already has an account is the real duplicate signal ("approving
this would give the same person a second account"); a match without one is
just the Person this request should be bound to instead of creating a
second entry for the same human.

This is deliberately a prompt and not a refusal. Two family members really
can share a name, and the app has no way to tell that case from a
duplicate — refusing outright would make the honest case unfixable without
hand-editing files, which is exactly what the accounts module exists to
avoid.

## Implementation

- **`app/invites.py`** (new): `Invite` dataclass, `create_invite`,
  `get_invite`/`list_invites`/`list_all_active`, `find_by_token`,
  `is_invite_valid`, `revoke_invite`, `accept_invite`.
- **`app/accounts.py`**: `MAX_PENDING_REQUESTS` enforced in
  `create_pending_request`; `similar_people` added.
- **`app/__init__.py`**: `OPEN_REQUESTS_ENABLED` from
  `STORYBOOK_OPEN_REQUESTS`.
- **`app/routes_accounts.py`**: `/admin/accounts/invite` (GET/POST),
  `/admin/accounts/invite/<person_slug>/<invite_id>/revoke`,
  `/invite/<token>` (public, GET/POST); `request_account` grows the
  optional-code branch; `admin_accounts`/`admin_review_pending` grow
  duplicate hints via a shared `_duplicate_hints` helper.
- **Templates**: `admin_invite.html`, `accept_invite.html`,
  `invite_invalid.html` (new); `admin_accounts.html`,
  `admin_review_pending.html`, `request_account.html` updated. The invite
  form reuses the existing `person_picker` macro rather than growing a
  second Person-picking widget.
- **CSS**: `.admin__token`, `.admin__row-hint`, `.admin__hint--warn`,
  `.login__hint`, `.flash--success` (the app's first success flash).
- **French**: every new string translated in `translations_fr.py`, which
  `tests/test_i18n.py`'s coverage test enforces anyway.

### A pre-existing bug this found

`.admin__token` exists because the browser pass caught the freshly-created
invitation URL running 261px off the right edge of a 390px viewport: a
token is one unbreakable ~43-character word, and the old markup put it in
`.admin__row`, a flex container with nothing to make it wrap.
`account_write_links.html` had shipped with the identical defect since F19
Phase 3 — same markup, same overflow, on the one screen you are most
likely to be looking at from a phone while pasting the link into a
message. Both now use `.admin__token`, which wraps mid-token.

### Tests

`tests/test_invites.py` (30) covers the data layer: token stored only as a
hash, the default 14-day expiry, re-issue revoking its predecessor while
keeping history, every rejection path in `accept_invite` (revoked,
expired, already accepted, unknown token, taken username, username sitting
in the pending queue, short password, bad username, Person given an
account by another route), the queue cap, and every branch of
`similar_people`.

`tests/test_invite_routes.py` (29) covers the HTTP surface: admin-only
access to the invite screens, creating for an existing or new Person, the
token appearing exactly once and never again, an invited Person dropping
out of the picker, withdrawing, and the recipient's flow — accepting,
working exactly once, and the two failures that must *not* burn the
invitation (mismatched passwords, taken username). Plus open requests: the
codeless path, the bootstrap-admin guard, the wrong-code guard, the cap,
and both duplicate-hint wordings.

Verified in Chromium at 390px across the whole flow in both languages:
open request form, bootstrap, codeless request, the admin list with a
duplicate flagged, the review warning, creating an invitation, accepting
it (with a deliberate password typo first), logging in with the new
credentials, and re-opening the burnt link. Zero horizontal overflow on
every screen after the `.admin__token` fix.

`pytest` (1007: 948 existing + 59 new) and `ruff check .` green.

---

# Feature spec — F40: groups, or telling some stories to fewer people

Written up before implementation, the way F1 and F19 were. Nothing here is
built yet; this document is the design discussion, and the decisions marked
**(confirm)** are values calls that should be settled before any code is
written rather than discovered in review.

## What this is, and what it reverses

Today every account can read every story. F19 said so on purpose:

> once someone has an approved Family account, they can edit/delete *any*
> story, exactly like today. The account system answers who gets in the
> door and how they're attributed, not who can touch what once they're in
> — a permission-walled model would be a bigger, more blog-like feature
> than anything else in this app.

This feature reverses the read half of that call, deliberately and with
the reason stated: a book that the whole extended family can read is a
book you write differently. Some things are for a wife and a son and
nobody else, and the current model's only options are "everyone sees it"
or "don't write it down." The second option loses the memory forever,
which is the one outcome this whole app exists to prevent.

What is *not* reversed: the edit half. A family member who can see a story
can still edit it. Per-story authorship walls would be a second
permissions axis for no gain — the people who can see a scoped story are
by construction the small group it was written for.

**Restraint clause, same as F19's.** This must not turn the book into a
social network with privacy settings. No per-story ACLs, no "share with
person X" one-offs, no visibility dropdown on every screen. A group is a
named handful of people that exists because the family actually thinks of
it as a unit ("just us four"), and the default for every story stays what
it is today: everyone.

## The data

Groups live in one file at the stories root, next to `pending_accounts.json`:

```json
// stories/groups.json
[
  {
    "slug": "just-us",
    "name": "Just us",
    "members": ["papa", "maman", "milo"],
    "created_at": "2026-08-01T10:00:00"
  }
]
```

Members are **person slugs**, not usernames — an account is already a
login bolted onto a Person (F19), and the Person is this app's identity.
A member who has no account yet simply can't log in to use it; adding
their login later needs no change to the group.

Scoping a story is one optional frontmatter key:

```yaml
---
title: The night we told him
date: 2026-08-01
audience: [just-us]
---
```

**Absent or empty means everyone**, exactly like `draft`/`archived`
already work, so every story that exists today keeps working with zero
migration and zero rewrite. A story with `audience` set is visible to
anyone in *any* listed group (union, not intersection) — "close family
and the godparents" is a real thing to want and costs nothing.

Why one central `groups.json` rather than a `groups:` key on each Person's
`index.md`: a group is a thing in its own right, with a name and an
identity, not a property of a person. Membership edits stay atomic in one
write, and the file reads as a list of groups when you open it in a text
editor five years from now, which is the actual test.

## Who sees what

| | Reads a scoped story |
|---|---|
| Member of a listed group | Yes |
| The story's author | Yes, always — even if they scoped it to a group they're not in |
| Admin who is not a member | **No (confirm)** |
| Family account, not a member | No |
| Delegate (write-link) | No — delegates never read anything |
| Accounts mode off | N/A — see below |

Two of these need justifying.

**The author always sees their own story.** Otherwise a mis-tap in the
editor makes a story disappear from its own writer, recoverable only by
hand-editing frontmatter. This is a safety rail, not a permission.

**Admins do not get to read past a group (confirm).** This is the values
call in the feature, and it's the one you asked for directly: "groups
should actually be only accessible by the people in it." The consequence
worth being sure about is that admin becomes a *management* role, not a
superuser one — an admin can create groups, rename them, and change who's
in them, and can therefore always add themselves and then read. The
difference is that doing so is a visible, recorded act rather than an
invisible capability. Membership governs reading; role governs managing.

**Groups are meaningless with `STORYBOOK_ACCOUNTS` off.** One shared
password is one identity, so there is nobody to scope *away from*. The
entire feature must be invisible in that mode — no groups page, no
audience picker in the editor, no `audience` key written — the same way F1
disappears when `STORYBOOK_AUTHORS` is unset. An install that never turns
accounts on sees no change whatsoever.

## The actual work: every surface that shows a story

The data model is a morning's work. This table is the feature. Today
"readable" is a property of a story alone; it becomes a property of
*(story, viewer)*, and every one of these currently reaches stories
without a viewer in hand.

| Surface | File | Note |
|---|---|---|
| Timeline (+ on-this-day, quiet-spell nudge, draft/archive counts) | `routes_pages.py:119` | |
| Story page | `routes_pages.py:344` | |
| **Story media** | `routes_pages.py:388` | Gate the page but not this and the photos leak by direct URL |
| Story history | `routes_pages.py:381` | `.versions/` snapshots hold full body text |
| Editor | `routes_pages.py:414` | |
| Book, EPUB | `routes_pages.py:234`, `:268` | |
| Firsts, Growth, Random | `routes_pages.py:166`, `:157`, `:187` | All compute over every story |
| Drafts, Archived | `routes_pages.py:320`, `:332` | |
| Person page "appears in" | `routes_people.py` | via `storage.stories_featuring` |
| **Export** | `routes_pages.py:302` | Zips the *entire* stories dir, `.versions/` included |
| Story create/update, image/memo upload, memo delete, version restore | `routes_api.py` | A story you can't see must 404 on write too |
| MCP server | `mcp_server.py` | No session at all — see below |

### How the gate is applied

One helper in the web layer, not a new parameter on
`storage.readable_stories`:

```python
# routes_pages.py
def _visible_stories():
    """Every story the current viewer may see — the only way any route
    should reach the story list."""
```

Routes call `_visible_stories()` instead of
`storage.list_stories(current_app.config["STORIES_DIR"])`, and
`_visible_story_or_404()` instead of `_get_story_or_404`. `storage.py`
stays pure and viewer-unaware; the predicate itself
(`groups.can_see(story, viewer_slug, viewer_groups)`) is a pure function
in the new module, unit-testable with no Flask.

The reason this is worth being fussy about: a missed surface is a silent
leak, and there are fourteen of them. So the change is deliberately
mechanical and greppable — and backed by a test that walks the URL map the
way F36's auth-perimeter test does, asserting that a non-member gets 404
from every story-bearing route for a scoped story. A new route that
forgets the gate fails that test the day it's written. **That test is not
optional and should be written first.**

### Export (confirm)

`/export` currently zips everything on disk. Three options, and the choice
matters more than it looks:

1. **Admin-only.** Simplest, but contradicts the rule above — an admin
   outside a group could read its stories by downloading them.
2. **Complete, but only for someone who can see everything.** Honest about
   backups, but leaves most of the family with no backup button at all.
3. **Scoped: you export what you can see**, with the page saying plainly
   that a backup taken by someone who can't see every story is partial.

**Recommendation: 3.** It preserves the group promise exactly, keeps F8's
one-tap backup working for everyone, and the honesty is in the wording
rather than in a silent surprise. The risk it carries — someone treats a
partial export as their only backup — is real, and the mitigation is that
the notice has to be blunt, not a footnote. `/import` becomes admin-only
regardless, since importing is how you'd otherwise write yourself past a
group.

### MCP (confirm)

`mcp_server.py` has no session — it's local stdio, running as whoever
started it, and README's trust model already says it's the owner's own
tool on the owner's own machine. **Recommendation: it sees everything, and
README says so in one sentence rather than leaving it to be discovered.**
Building a viewer identity into a single-user stdio tool would be
ceremony, not security; the honest move is to document that the MCP
surface is unscoped and let the owner decide whether to run it.

## Things that will bite

- **`restore_version` drops `audience`.** `storage.py:588` rebuilds a
  story from an old snapshot field by field, and any field not listed is
  lost. Restoring a version from before a story was scoped would silently
  un-scope it. `audience` must be threaded through there, and a test
  should pin it — this is the single most likely way to build a quiet leak
  into this feature.
- **Media caching.** `story_media` sets a one-year `max-age`; F36 already
  forces `private` on cached media, so a shared proxy can't hold a scoped
  photo. Worth re-asserting in a test rather than assuming, since the
  consequence changed: it used to be a privacy nicety, now it's the
  difference between a photo staying in the family and not.
- **Version history of a story whose audience changed.** Access to
  `/story/<id>/history` and every snapshot must key off the story's
  *current* audience, not the audience recorded in the snapshot.
- **`_reading_order_neighbors`.** Previous/next must skip stories the
  viewer can't see, or the page-turn arrows leak titles.
- **Counts as an oracle.** "3 drafts" when you can see one is a small
  leak, but it's a leak. Counts get filtered too.
- **A group with no members** should not act as "visible to nobody but
  behaves oddly" — a story scoped to a group whose members were all
  removed is visible to its author only, and the groups page should say so
  rather than leaving an invisible story.
- **Deleting a group.** The app doesn't delete things. A group can be
  emptied and renamed; stories referencing a gone group would be
  author-only, which is a trap. Recommendation: groups can't be deleted,
  only emptied — consistent with the no-deletion stance everywhere else.

## Phasing

**Phase 1 — the wall.** Everything security-relevant, no UI polish.
`app/groups.py` (dataclass, CRUD, the pure `can_see` predicate), the
`audience` frontmatter key through `create_story`/`save_story`/
`restore_version`, `_visible_stories`/`_visible_story_or_404`, every
surface in the table gated, `_validate_audience` in `routes_api.py`
following the existing `_validate_slug_list` pattern, the export/import
decision, and the perimeter-style test written first. Admin groups page
(create, rename, membership) with plain forms. No editor picker yet —
Phase 1 ships with `audience` settable only by an admin editing
frontmatter, which is enough to prove the wall holds.

**Phase 2 — the writing experience.** The audience picker in the editor,
sitting with the existing Draft/Archive chips: a row of group chips,
nothing selected meaning everyone. A quiet marker on the timeline and the
story page saying who can see this one — without it the writer can't tell
a scoped story from a public one, which is how someone writes something
private into a public story. Mobile-first, checked at 390px.

**Phase 3 — the edges.** EPUB and book-view scoping wording, the MCP
sentence in README, the FEATURES.md write-up, and a French pass.

Phase 1 is the one with real risk in it. Phases 2 and 3 are ordinary work.

## Rejected

- **Per-story person lists** ("share this with Marie and Luc"). Every
  story becomes a permissions decision, which is exactly the blog-shaped
  thing F19's restraint clause rules out. Groups are named because naming
  them is what keeps this small.
- **A "private" flag with no group** (visible only to the author). Almost
  free to build, and it's a diary, not a book written for someone. If it
  turns out to be wanted, it's a group of one.
- **Encrypting scoped stories at rest.** README lists encryption as out of
  scope, and it would break the "delete the app and the folder is still
  readable" promise that the whole design rests on. Scoping is an access
  rule in the app, and the frontmatter says plainly who a story was for —
  which is the right behavior when the family reads these files in thirty
  years without the app.

---

### F40 Phase 1 implementation round — the wall

Built as the spec above describes, with the three `(confirm)` items
resolved to their recommended answers. Phase 1 is deliberately the
security half only: the audience rule, every surface enforcing it, and
admin screens to manage groups. No editor picker yet (Phase 2) — an
`audience` is set through the API or by hand, which is enough to prove
the wall holds before building a UI on top of it.

**`app/groups.py`** (new): `Group` dataclass, `list_groups`/`get_group`/
`create_group`/`rename_group`/`set_members`, `groups_for_person`, and the
two functions the rest of the app actually leans on — `can_see` and
`visible_stories`, both pure, no Flask and no filesystem, so who-reads-what
is one testable statement rather than a rule smeared across fourteen
routes. Groups live in `stories/groups.json`; a story names them in an
`audience:` frontmatter list, absent meaning everyone.

**One chokepoint, not a parameter.** `storage.readable_stories` stays
viewer-unaware; the gate is `_visible_stories()` / `_get_story_or_404()`
in `routes_pages.py`, and every page route goes through them.
`storage.py` never learns what a session is. A story a viewer may not see
404s rather than 403s — the same choice `admin_required` already makes, so
a scoped story's *existence* isn't discoverable by URL either.

Decisions that came out of building it:

- **Restoring a version deliberately does not restore `audience`.** The
  spec flagged `restore_version` as the likeliest place to build a quiet
  leak, and the fix turned out to be the opposite of the obvious one.
  Threading `audience` through faithfully means pulling up a version from
  before a story was scoped silently republishes it to the whole family —
  a leak nobody performed and nobody would see. Restoring is about getting
  old *words* back; a story's audience is a standing decision about who
  may read it today. So `restore_version` omits the field and `save_story`
  carries the current one over. `test_restoring_an_old_version_keeps_the_current_audience`
  asserts both halves: the body came back, the audience didn't move.
- **An unknown group slug is a 400, not a dropped value.** Every other
  list field in `routes_api.py` silently drops junk. Here, dropping one
  turns a story the writer believed was scoped into a public one — the
  single worst way this feature could fail — so `_validate_audience`
  rejects instead.
- **Writes are gated on readability.** `_readable_story_or_error` guards
  update, restore, image upload, memo upload and memo delete. A story you
  can't read is one you can't write, or `PUT /stories/<id>` becomes a way
  to overwrite — or simply read back — something scoped away from you.
- **`story_media` is gated on the story, not just the filename.** Gate the
  page and not this and every photo stays fetchable by direct URL, which
  is most of what a scoped story is protecting.
- **`/import` and `/api/import` became admin-only** — but only in accounts
  mode, via a new `auth.admin_required_in_accounts_mode`. A plain
  `admin_required` would lock every single-password install out of its own
  import page, since `session["role"]` is never set there. A backup zip
  can carry whatever frontmatter it likes, so restoring one is a way to
  write around a group.
- **Export is scoped to what you can see**, and the import page says so in
  red when it applies. The alternative — a complete zip for whoever clicks
  it — would make `/export` the way around every group, since the zip
  carries `.versions/` and photos too. The cost is that a partial backup
  can be mistaken for a whole one, so the notice is blunt rather than a
  footnote.
- **The MCP server stays unscoped**, documented in its module docstring
  and in README. It's stdio running as whoever launched it, against a
  folder that user can already read; building a viewer identity into a
  single-user local tool would be ceremony, not security. But someone
  deciding whether to run it deserves to know it reads past every group.

### Tests

`tests/test_groups.py` (38), in three layers. The pure rule first
(everyone by default, membership required, union across several groups,
the author's own story, order preserved). Then the storage round-trip,
including the restore-version trap and a malformed `audience:` key being
ignored rather than fatal.

Then the leak perimeter, which is the point of the file: a fixture builds
a book with one public story, one scoped story, an admin deliberately
*outside* the group and a family member inside it, and asserts the
outsider gets nothing — no title on any listing page (`/`, `/book`,
`/firsts`, `/growth`, `/drafts`, `/archived`, the person page), no body in
`/book`, nothing in the EPUB, 404 from the story page, editor, history and
media URLs, no page-turn neighbour, never a `/random` landing, 404 from
every mutating endpoint, and a backup zip with the scoped folder missing —
while the insider sees all of it and the public story is untouched.

Two guard tests keep that honest as the app grows:
`test_no_page_route_reaches_the_story_list_directly` walks the route files
and fails if one calls `storage.list_stories` instead of
`_visible_stories()`, and `test_accounts_mode_off_means_no_scoping_at_all`
pins that a single-password install is unaffected.

Verified in Chromium at 390px in both languages: creating a group, adding
a member, an admin outside the group finding no trace of a story scoped to
it while the member sees it normally, and the partial-backup warning
reading as a caution rather than another line of intro (it first shipped
sharing a class with `.import__intro` and lost the color to it).

`pytest` (1045: 1007 existing + 38 new) and `ruff check .` green.

---

### F40 Phase 2 implementation round — the writing experience

Phase 1 built the wall but left `audience` settable only through the API,
which meant the app had a privacy feature nobody could use and — worse —
no way to tell a scoped story from a public one while writing. Phase 2 is
the picker and the two markers.

**The picker** is a row of chips ("Who can see this") built by a shared
`audience_picker` macro and driven by `app/static/js/audience.js`, a
factory both `editor.js` and `instant.js` call. Nothing lit means
everyone.

The state line under the chips is the reason this is a module rather than
three lines inlined twice. **"No chips lit" and "the whole family can read
this" have to read as the same thing**, and a picker whose default is
invisible is one where somebody eventually writes something private into a
public story. So the current audience is spelled out in words in every
state — *Everyone*, or *Only Just us* — and turns accent-colored the
moment it stops being everyone.

**Instants get the picker too.** The original ask was "stories or
instants", and an instant you can't scope is a hole you'd only discover
after posting one. Worth noting how it survives the instant's two-step
save: the create carries `audience`, and the follow-up PUT that attaches
the uploaded cover omits it — which is correct precisely because
`save_story` treats an absent `audience` as "leave unchanged". Verified on
disk rather than assumed.

**The markers.** A scoped story says *Kept to Just us* under its title
(in `_story_article.html`, so the story page and the book view both get
it) and carries a quiet *kept to a group* pill on the timeline. The pill
is deliberately plainer than the milestone pill beside it: it states a
fact about the story, it isn't celebrating one.

`group_names` (slug → display name) comes from a **context processor**
rather than a per-route argument. The marker rides along with the shared
story partial, which four routes render; threading a dict through each is
four chances to forget, and forgetting means a scoped story that looks
public to its own writer. Empty outside accounts mode, so the whole thing
stays invisible on a single-password install.

`_available_groups()` offers *every* group, not only the writer's own:
scoping a story to a group you aren't in is legitimate (writing something
for the grandparents), and `can_see`'s author rule keeps your own access
either way.

### Tests

`tests/test_groups.py` grows to 48 (10 new): the editor offers every
group and pre-lights a scoped story's chips (read out of the markup with a
regex, not inferred from "some chip somewhere is pressed"), leaves them
unlit for a public story, the instant composer offers them too, no picker
appears without accounts mode or without any groups, the story page names
the groups, a public story says nothing, the timeline marks a scoped
story — and an outsider's timeline carries no pill at all, since the pill
would otherwise leak the existence of a story they can't see.

Verified in Chromium at 390px in both languages, driving the real UI:
lighting a chip and watching the state line go *Everyone* → *Only Just
us*, writing and saving a story through the editor, its marker on the
story page and pill on the timeline, re-opening the editor with the chip
still lit, and saving a scoped instant with a photo — then checking
`audience: [just-us]` really landed in its `index.md`. Zero horizontal
overflow, zero console errors, French correct throughout (*Tout le
monde* / *Seulement Just us* / *Réservée à Just us*).

`pytest` (1055: 1007 existing + 48 F40) and `ruff check .` green.

---

### F40 inspection round — two real bugs, one of them older than F40

A deliberate adversarial pass over the finished feature: every surface
probed live as an admin deliberately outside a group, every write endpoint
attacked, both export zips opened and compared. The read/write perimeter
held everywhere — every listing clean, every scoped URL and mutating
endpoint 404, the outsider's zip missing the scoped folders, `.versions/`
and photos included. Three things did come out of it.

**Two dead helpers were removed.** `storage.stories_featuring` and
`storage.readable_page_stories` both lost their last caller when Phase 1
routed everything through the gate. Neither is merely unused: both read
every story straight off disk and both look exactly like the helper a
future person page or page-turn feature would reach for, and the Phase 1
guard test only grepped for `storage.list_stories`. Deleted, the guard
widened to count `storage.get_story` too and to walk every route file
rather than three, and a test added that asserts neither name comes back.

**Backups could not be restored — since F19, not since F40.**
`import_backup` rejected any zip entry whose top path segment wasn't a
valid story id, and an accounts-mode export contains
`pending_accounts.json` (F19) and now `groups.json` (F40). So any install
that had ever seen an account request produced a backup that aborted on
import with `Unexpected path in backup`. A one-tap backup you cannot
restore is precisely the failure this app exists to prevent, and F8 is a
headline feature, so it's fixed here rather than filed: unknown root-level
entries are now skipped instead of aborting. Unsafe paths (absolute, `..`)
still abort the whole import, with a test pinning that the zip-slip
guarantee didn't weaken as a side effect.

Those files are skipped rather than imported on purpose. They're live
operational state — who is waiting for an account, who is in which group —
and silently overwriting them from an old zip would be worse than leaving
them alone.

**Which made a third bug reachable, so it's fixed too.** Restore a backup
into a fresh book and the stories come back while `groups.json` doesn't, so
a story names a group that doesn't exist here. `can_see` already failed
safe (an unknown group means nobody but the author). The editor did not:
it rendered no lit chip for the orphaned slug, so an ordinary save sent an
empty audience and a story that was private quietly became public — the
one failure this whole feature exists to prevent, arriving through the
disaster-recovery path of all places.

Now `_available_groups(story)` gives an orphaned slug a chip of its own,
labelled with the raw slug, and `_validate_audience` accepts a slug already
on the story being updated. The rule became "you can't introduce an unknown
group, and you can't accidentally drop one either" — inventing a new
unknown slug is still a 400.

Rehearsed end to end: export a book with a scoped story, wipe, restore into
a fresh install. The stories come back still scoped, unreadable by anyone
until the group is recreated, and recreating it under the same name
realigns the slug (`Just us` → `just-us`) and restores access with the
audience intact.

### Two boundaries worth knowing, deliberately left alone

- **`groups.json` is in every export**, so any family member's backup
  reveals every group's name and membership. Group *management* is
  admin-only in the UI, so this is an inconsistency — but membership isn't
  story content, everyone in it is already named on the family tree, and
  dropping the file would make a restored backup lose its groups entirely.
- **`people/*/account.json` is in every export too**, so any family member
  can download every account's password hash. Pre-existing since F19 and
  unrelated to groups; the hashes are scrypt and this is a household app,
  but it is worth knowing before handing someone a Family account.

`pytest` (1060) and `ruff check .` green.

---

## F41. Groups anyone can make

F40 shipped groups but kept the two screens that manage them behind
`@admin_required`. So the feature read, in practice, as: you may keep a
story to fewer people, provided an admin has already made the right circle
for you. Wanting to write something for three particular people meant
stopping, asking, and waiting — which mostly means not writing it. Groups
are a writing tool, and a writing tool you have to file a request for is
one nobody uses.

So: **anyone in the family can make a group.** `/admin/groups` and
`/admin/groups/<slug>` became `/groups` and `/groups/<slug>` (endpoints
`pages.groups_page` / `pages.group_page`, templates `groups.html` /
`group.html`), the nav link shows for everyone in accounts mode, and the
`admin_required` decorator is gone from `routes_groups.py`. Still 404
without accounts mode: one shared password is one identity, and a group
would have nobody to scope a story away from.

### The one thing that can't be opened up

Making a group is harmless. Editing an existing one is not — if any
logged-in person could edit any group, anyone could add themselves to
"Just us" and read it, and the whole of F40 would collapse to a
suggestion.

`groups.can_manage(group, person_slug, is_admin)` is the gate: **a group is
changed by the people in it, or by an admin.** A circle maintains itself,
the way it works when a family actually talks — the people already inside
decide who else comes in. Membership, not authorship: `created_by` is
recorded and displayed ("made by Maman") but grants nothing on its own.

Which forces one small thing to be true: **making a group puts you in it.**
Rights follow membership, so a creator left outside would be locked out of
the group they'd just made, with nothing on screen explaining why. The
create form says so before you use it, and the edit form warns before you
take yourself out, since that's the one edit you can't undo from that page.

An empty group therefore has no family editors and is admin-only. That
falls out of the rule rather than being special-cased, and it fails closed,
which is the direction to fail in.

Non-managers still get the page, read-only — a group's name isn't a secret,
it's printed on every story kept to it, and you need to know who's in a
group to choose it in the editor. A POST without rights is a **403, not the
404** used elsewhere in this app to hide a page's existence: the resource is
genuinely visible, so pretending otherwise would be a lie the UI
immediately contradicts.

### The barriers

**Two groups can't cover exactly the same people.** Identical membership is
one circle under two names, and that's worse than merely redundant: a story
kept to one looks protected from people who can in fact read it through the
other, and widening one leaves the other silently behind.
`groups.scope_twin` finds the offender and the message names it — *"Just us
already covers exactly these people"* — so the answer is to use that group
rather than to guess.

Fewer than two people never counts as a twin. An empty group is a state on
the way to being filled in, not a scope; a group of one is a note to a
single person, where a second name for the same person misleads nobody.
That exemption isn't a nicety — without it the rule fights the app, because
making a group puts you in it, so everyone's first group is {you} and it
would collide with any existing group that happened to be {you}. Refusing a
group at the moment someone types its name, over a membership they never
chose, would be the feature's worst first impression.

**A rename can't collide either.** The slug never changes on rename (F40:
stories reference it by slug, and rewriting every story's frontmatter to
track a rename is the cascading write this app avoids), so without a check
two groups could end up *displaying* the same name — two identical-looking
chips in the editor doing different things. Compared case-insensitively.

**A cap of 40 groups** (`groups.MAX_GROUPS`). Every group is a chip in the
audience row, on a phone, above the keyboard; past a couple of dozen that
row stops being a choice you can make at a glance, which is when someone
taps the wrong one. At the cap the create form is replaced by an
explanation, rather than left there to fail on submit.

**Unknown or duplicated members are rejected, not dropped.** `clean_members`
now validates at creation too (F40 only did it on edit), de-duplicates, and
checks each slug against `is_valid_story_id` before touching the
filesystem. A member who silently isn't there is one who can't read what
they were meant to, with nothing on screen saying so.

### Leaks found while building it

**A story count is content.** The group page said "1 story is kept to this
group" to everyone. Fine when only admins could open it; not fine once
every family member can, because it tells an outsider how many stories
exist that they aren't allowed to read — precisely what F40 stops the
timeline's "kept to a group" pill from leaking. Both the list and the group
page now show counts only to people who can manage the group. Caught in the
browser, not by a test; the test came after.

**Widening republishes other people's writing.** Adding a person to a group
opens every story kept to it, not only your own. Under F40 an admin did
that knowingly; under F41 a member might not think of it. The group page
counts the stories kept there that *someone else* wrote and says so above
the form. It's a warning, not a block — the members of a circle are the
right people to make that call, they just should know they're making it.

### Untranslatable errors, fixed on the way past

`groups.py` raised `ValueError(f"There is already a group called {name!r}.")`
and the route did `flash(_(str(exc)))`. That reaches the French catalog
already interpolated, so it never matched a key: every one of these
messages was silently pinned to English since F40.

`groups.GroupError` now carries the uninterpolated template plus its values
(`GroupError("There is already a group called {name}.", name=name)`), and
`_flash_group_error` hands both to `_()`. It subclasses `ValueError`, so
existing `except ValueError` handlers are unchanged. Verified in the
browser: *"Grandparents regroupe déjà exactement ces personnes."*

### Also true now

F40 noted that `groups.json` sitting in every export was "an inconsistency,
since group management is admin-only in the UI". It isn't an inconsistency
any more — group names and membership are visible to every family member by
design. The export still carries account password hashes (F19), which is
unrelated and still worth knowing.

### Where a group comes from, and where it never comes from

Opening group-making to everyone is only safe if the browser has no say in
who reads what, so the trust model got audited rather than assumed.

The viewer's group set has exactly one source: `_viewer_scope()` takes
`session["person_slug"]` and asks `groups.groups_for_person` to read
`groups.json` off disk. That's it. No request field — query string, form
body, JSON key, or header — reaches it, and there is no client-side
filtering anywhere: `audience.js` only *sends* an audience when writing,
and scoped stories are omitted from the HTML server-side rather than
hidden with CSS, so View Source shows a non-member nothing.

Two properties fall out of reading membership per request rather than
caching it in the session at login, and both are the ones you want:
adding someone grants access on their next page load, and removing someone
revokes it on their next request, with the session they already hold.

The session cookie is signed with `STORYBOOK_SECRET_KEY`; editing a byte
of it logs you out rather than promoting you. Verified live against a
running server, logged in as a family account in no group at all: the
scoped story's page, editor, history, and photo URLs all 404; forged
`?groups=`, `?audience=`, `?person_slug=`, `?role=` and `X-Viewer-Groups:`
change nothing; `PUT /api/stories/<id>` is a 404 even with a valid CSRF
token; posting yourself onto the group's member list is a 403 and the
story stays a 404 afterwards.

### The namesake hole in the author rail, closed

The audit turned up one path that wasn't a client-side trick and was real:
`can_see`'s author rail compares `story.author` — a display *name*, since
F1 stores a name rather than a slug — to the viewer's Person name. Two
People called "Maman" therefore read each other's scoped stories, no
tampering required. Getting there needs an admin to approve a second Person
with a name already in the book, which is exactly what F39's duplicate
hints flag, but "unlikely" isn't "prevented" and this is an access-control
comparison.

Rather than change what a story stores — the author name is F1's data
model, and rewriting every story's frontmatter to carry a slug is the
cascading write this app avoids — the *comparison* now refuses to run on an
ambiguous name. `_unambiguous_author_name` returns the viewer's name only
when no other Person shares it (casefolded, deliberately broader than the
exact match it guards), and `_viewer_scope` passes None otherwise.

Both namesakes lose the rail, not just the newcomer: from a name alone the
app can't tell which is which, and withholding a safety net is the cheaper
mistake than exposing a private story. The real author still reads her
story through the group like everyone else, and an admin renaming either
Person restores the rail for both — tested, since that's the fix an admin
would actually reach for.

`_viewer_scope` is now memoized on `g` for the request, because it walks
the people list and `story_media` reaches it through `_get_story_or_404`
once per photo on a page.

### One boundary this deliberately doesn't change

**Anyone who can read a story can edit it, including its audience.** A
member of *Just us* can widen a story someone else kept to it. That's the
app's writing model — a family journal with no per-story ownership — not
something groups introduced, and the group page's warning is the same idea
applied to membership. Worth knowing: a group protects a story from the
people outside it, not from the people inside it.

### Tests

42 new tests in `tests/test_groups.py` (94 in the file, 1102 in the suite):
the membership gate from both sides, an admin editing a group they're not
in, an empty group failing closed, the read-only page, creation putting you
in the group, the story-count leak, the widening warning appearing only
when someone else's writing is at stake, every branch of the twin rule
(order-independence, the exempt sizes, ignoring the group being edited),
the rename collision, the cap and its form, duplicate and traversal-shaped
member slugs, and `created_by` surviving a round trip and degrading to
`None` when malformed.

Plus a section for the audit above — *nothing the client says about groups
is believed*: forged query parameters and JSON fields on every reading
surface, a tampered session cookie, membership taking effect (and being
revoked) mid-session without a re-login, the outsider's HTML never carrying
the story at all, and adding yourself to a group as the one client-side
move that would actually grant reading, plus the namesake rail from
every side — the impostor, a case-only difference, the real author losing
it too, a rename restoring it, and a unique name keeping it.

Verified in Chromium at 390px in English and French: the list, the editable
page, the read-only page, creating a group end to end, and both refusal
flashes in both languages.

`pytest` (1102) and `ruff check .` green.

## F42. Help as a glossary, and the prompts for the pictures it still wants

The help page (F33) had drifted into an essay. Eight sections of prose, and
the prose was explaining the wrong altitude of thing — a paragraph on how
the camera button works ("you'll see the picture before it's kept, so you
can retake it as many times as you like") next to nothing at all about
groups, which is the one feature in this app where a reader can be wrong
about who will see what. Nobody needs to be told a camera button takes a
photo. Somebody does need to be told that a story kept to a group is a
story their sister can't read.

### One term, one line

The page is now a **glossary**, not a tour: `<dl>` blocks where each `<dt>`
is a word the reader actually meets on screen — Story, Instant, Draft,
Sealed letter, Milestone, Archived, Group, Write link, History, Backup —
and each `<dd>` is a single line saying what it is. New `.help__defs`
styling (term in the body colour, definition in `--color-text-dim`) so the
page scans as a list of answers rather than reading as a chapter.

What changed in substance:

- **A "Who can read a story" section**, guarded by `config.ACCOUNTS_ENABLED`
  exactly like the accounts section, covering the audience rule (F40) and
  the two things F41 makes true and non-obvious: making a group puts you in
  it, and widening a group opens other people's stories too, not only your
  own. Guarded rather than always-on because with one shared password there
  is nobody to scope a story away from, and describing a feature that isn't
  there is worse than saying nothing.
- **Archived, History and the writing prompts get a line each** — three
  things the app does that the help page had never mentioned.
- **Cut**: the camera walkthrough, the "you'll never need to read this"
  throat-clearing, the "ask whoever set up Storybook" refrain repeated in
  four sections (kept once, where it's actionable — the https caveat).

Net: shorter than before while covering three more features. The 8 English
sections became 6–8 (two are conditional), and the two longest paragraphs
in the file are gone.

Translation is the reason to keep help copy short, incidentally: every
string here is a key in `translations_fr.py`, and a five-line paragraph is
a five-line paragraph to keep in sync in two languages forever. Glossary
lines age better. Terms already translated elsewhere (Story, Draft,
Archived, Firsts, Growing up, History) resolve through their existing
entries rather than being restated.

`Invitation` joined `test_i18n.py`'s `same_in_both` allowlist — it really
is the same word in both languages, and the "you left the English in"
guard needed telling.

### IMAGE-PROMPTS.md

The other half of the same problem: some of what the help page explains in
words would be explained better by a picture, and this app already has a
visual language for that (F17's paper cards, F22's flat icons) — what it
doesn't have is the pictures.

`IMAGE-PROMPTS.md` is the catalogue: how to drive Gemini through these
(one asset per thread, an existing JPEG uploaded as the style anchor), the
processing steps, and ten assets, each with **what a reader must understand
from the picture alone** stated before the prompt itself. Every prompt is
self-contained — style, paper, aspect, size constraint and negatives are
repeated inside each one rather than referenced, because a prompt you have
to assemble from two places is a prompt that gets pasted wrong. The group one is the point of the
exercise — a closed lasso ring with four figures warm inside it and two
standing in cool light outside, so that "kept to a group" is understood
before a word of the section is read — and it ships with three fallback
compositions, because a generated image either reads at thumbnail size or
it doesn't and you want alternatives ready.

Two rules in that document are load-bearing rather than stylistic:

- **No lettering, ever.** The interface is bilingual (F38); a word baked
  into a JPEG can't be translated and will sit there in English on a French
  page forever.
- **Faces stay generic.** These illustrations sit beside photographs of a
  real family. Small gestural figures, backs and three-quarter views — not
  portraits of anyone.

Nothing is wired into a template yet, deliberately: an `<img>` pointing at
a file that doesn't exist is a broken image on a real family's page. Each
entry carries the exact `<img>` line and CSS to paste once its JPEG lands
in `app/static/img/`.

### Tests

`tests/test_help.py` gained a glossary test (the terms the interface uses
are the terms the page defines, asserted as `<dt>` elements) and a groups
test from both sides — the section is absent with one shared password and
present, with `<dt>Group</dt>`, in accounts mode. The core-sections test
follows the renamed "Photos and voice memos" heading.

Verified in Chromium at 390px in English and French and at 1280px in the
dark theme: no horizontal overflow, the definition lists read as lists at
phone width, and the French page uses the vocabulary the rest of the app
already uses (*cercle*, *première fois*, *lien d'écriture*).

`pytest` (1104) and `ruff check .` green.

### F42 follow-up: the illustrations landed

Nine of the ten assets in `IMAGE-PROMPTS.md` came back from Gemini and are
committed (see the second table in F17 for sizes and placements). Only
`icon-group.png` — the flat 24px companion for the timeline's *kept to a
group* pill — is still outstanding.

The group image was generated in all three of the compositions the
catalogue offers (lasso ring, corral fence, wagon circle). The **lasso
ring** is the one committed: it's the only one of the three where the
boundary is a rope on open ground rather than a built structure, so it
reads as *a circle drawn around some of us* rather than as a fence keeping
people out — which is the difference between the feature and a
misunderstanding of it. The other two are good drawings and were not
committed; unused static files are weight with no reader.

Processing followed the catalogue: trim to content with a 3% paper margin,
downscale to ~2× display size, JPEG q82 (q85 put `/history` over 100 KB on
its own). Paper colour was left alone — the new files measure between
(248,236,208) and (250,242,220) at the border, inside the spread the
existing F17 assets already occupy (`tree-sapling.jpg` is (248,237,213)),
so normalising would have meant repainting art to fix a difference nobody
can see against `.illo`'s cream.

One asset needed a fix: `history-pages.jpg` came back with legible *Lorem
ipsum* on its top sheet, which the catalogue's no-lettering rule exists to
prevent (a word baked into a JPEG can't be translated). Rather than
regenerate an otherwise-good drawing, that one line was softened with a
feathered 1.6px gaussian so it reads as handwriting like every other line
on the page. Illegible at display size, and now illegible at 2× too.

### The CSS bug this caught

`.illo--page` first shipped as `max-width` + `margin` only, which looks
right in a stylesheet and is wrong in a browser: the `width`/`height`
attributes on the `<img>` (kept deliberately, so nothing shifts while the
image loads) then pin the height while the width shrinks, and every
picture renders squashed into a tall narrow box. Caught in Chromium, not
by a test — nothing in the suite can see a wrong aspect ratio. The rule now
carries `width: 100%; height: auto` like `.login__illo` always did, with a
comment saying why both are needed.

Verified in Chromium at 390px, light and dark, on all nine pages: correct
aspect ratio, no horizontal overflow, no broken image, no 4xx, and the
cards reading as cream photographs against the dark theme. The guest-facing
form pages (`request-account`, `accept-invite`, the delegate page) drop
their illustration under 700px of viewport height, the way `/new-instant`
does, so the form stays above the fold — confirmed at 390×640.

### F42 follow-up: the last asset, and where an icon is too small to help

`icon-group.png` closes the catalogue — a rope ring around three figures
with a fourth outside, in F22's flat style rather than F17's engraving,
because fine linework is a smudge at 20px.

Keying it needed one change from F22's recipe. That set was auto-keyed by
colour distance from the border pixels; here the fill *inside* the rope
ring is nearly the same cream as the paper around it, so a distance key
punches a hole through the middle of the icon. The background is found by
flood-filling in from the four corners instead — only paper actually
connected to the edge goes transparent. The paper's printed flecks survive
that as tiny opaque islands (they're enclosed, not connected), so a closing
on the background mask swallows anything smaller than ~9px before the
alpha is cut. Cropped to content, squared with a 2% margin — 8%, F22's
figure, left the ring too small once the composition's own width was
included — and downscaled to 160×160.

It goes next to the audience picker's **"Who can see this"** label, in the
editor and on `/new-instant`. `.btn-icon` needs a flex parent (F22), and
`.editor__family-label` is shared with the Sources label, so the flex lives
on a new `.editor__audience-label` alongside it rather than on the shared
class.

**Not** on the timeline's *kept to a group* pill, which is where this icon
was first imagined. Rendered at the pill's scale the icon degrades to a
brown ring with a grey smudge beside it — tested at 14px and 16px before
deciding. The pill is 0.6875rem text in a border; at that size an icon
stops being an accent and becomes noise, and the words already say it.
Same reasoning F22 used to reject F17's linework for buttons, applied one
size down.

Verified in Chromium at 390px and at 4× device scale, light and dark: the
transparent key is clean with no halo in either theme, and the icon sits on
the label's baseline without shifting the chips below it.

## F43. What a backup may carry

A question worth asking about any app that offers "download everything":
*what is everything?* F40 had already answered half of it — a zip is scoped
to the stories you can read, so `/export` isn't the way around a group. The
other half had never been asked, and the answer was wrong.

### The hole

`/export` walks `stories/` and zips what it finds. Since F19 that folder
holds more than memories:

```
people/papa/account.json      username, scrypt password hash, role, status
people/papa/write_links.json  token hashes for delegated writing
people/tata/invites.json      token hashes for unredeemed invitations
pending_accounts.json         the same hashes, for requests not yet approved
```

Every logged-in family member could download all of it. Verified in a real
book before fixing, not inferred: mamie, a plain `family` account in no
group, got papa's `account.json` in her zip.

The hashes are scrypt (`32768:8:1`, salted), so this is not a password
handed over. What it is, is an **offline** guessing target, and that is the
part that matters:

- F36's login lockout is a rate limit on *this server*. It cannot see
  someone working through a wordlist on a laptop.
- Family passwords are family passwords. A first name and a year is a
  realistic guess space.
- The file names the `role` next to the hash, so it says which account is
  worth the effort.
- And the payoff is exactly what F40/F41 were built to prevent: an admin
  can add themselves to any group, so a cracked admin password reads every
  scoped story in the book. F41 made that escalation *visible* — a recorded
  change to a group — and this made it invisible again.

Nobody was even paying for the risk: `import_backup` only ever extracted
story-shaped entries, so those files were carried in every zip and restored
by nothing.

### The rule

**A backup carries memories and people. Logins stay where they were made.**

`storage.CREDENTIAL_FILENAMES` names the four files, and both directions
read it:

- **Out**: `/export` drops them unless the viewer is an admin — or accounts
  mode is off, where one shared password is one identity and there are no
  accounts to leak, the same reasoning `_viewer_scope` already uses.
- **In**: `import_backup` never restores them, for anyone. A zip is a
  portable file; restoring one taken from another book would otherwise
  install its accounts — its admins included — into yours. Losing logins on
  a restore is an inconvenience an admin fixes with an invitation; gaining
  someone else's is not.

The constant lives in `storage.py`, which owns the on-disk layout, while
each file is still written by the module that owns its feature.
`tests/test_backup_credentials.py` cross-checks the two so a rename in
`accounts.py` can't quietly start shipping hashes again.

Admins keep the complete zip. They manage accounts and can reset any
password from the UI already, so withholding the file would protect
nothing and would cost the one person taking a real backup its
completeness.

### The bug found while fixing it

`is_valid_story_id("people")` is `True` — the regex is `^[a-z0-9-]+$`, and
`people` is a perfectly good story id. So `import_backup` treated the whole
cast as one enormous story folder, and its collision check did the rest:

```
409 Import aborted, nothing was changed: 1 already exist here (people).
```

**Any backup from a book with people could not be restored into a book that
already had people.** Which is to say: into any book that had ever been
used. Restoring into a fresh install worked, so the one-tap backup looked
fine right up until the day you needed it in an existing book — the exact
failure `import_backup`'s own docstring says the design exists to avoid,
sitting inside the function that says it.

People are now handled on their own terms rather than as a story: each
`people/<slug>/` in the zip is restored if this book doesn't have that
person, and skipped if it does. Skipped rather than merged because the
living folder is the newer truth, and a person's `index.md` carries edges
(parents, partners, unions) that a half-old copy would contradict. Stories
keep the strict all-or-nothing rule — a colliding story still aborts
everything, including the zip's people.

One consequence, deliberate: the count `import_backup` returns is still
stories only, so restoring a zip of 3 stories and 8 people reports 3. The
number in the UI answers "how many memories came back", which is the
question being asked.

### Tests

`tests/test_backup_credentials.py`, ten tests over both directions: a
family member's zip has no credential file and no `password_hash` or
`token_hash` byte anywhere in it, an admin's still has all four kinds,
shared-password mode is untouched, F40's story scoping still holds
alongside the new rule, people restore into a book that already has a cast,
an existing person is left exactly as they are, credentials never come back
even from a zip that has them, a story collision still writes nothing at
all (people included), and odd shapes under `people/` are skipped rather
than extracted. Plus the constant cross-check against `accounts.py`,
`invites.py` and `write_links.py`.

`test_import.py`'s accounts-mode round trip asserted `== 2` for "the story
and people/" — it was encoding the bug. Now 1, with a comment saying why.

The import page gained a line, in both languages, saying restoring brings
back stories and people but never logins. It's admin-only, which is exactly
who needs to know before a disaster recovery.

`pytest` (1114) and `ruff check .` green.

## F44. Writing in the book's own hand, and firelight

Two requests, one theme: the app looks like a hand-made book everywhere
except the one screen where the book is actually written, and the room it
is read in could use a fire.

### The editor didn't belong to the app

Toast UI ships its own palette — a white page, a blue-grey toolbar, 13px
Open Sans — and until now the app just dropped that widget onto the page
and hoped. The result was worst in the manuscript theme, where a stark
white rectangle sat on aged paper with a cold grey rail across the top of
it, and only slightly better in dark, where the vendored dark theme's
`#121212`/`#232428` read blue next to the app's warm `#141210`. Nothing
about the writing surface said "book": not the font, not the size, not the
colour of the paper.

`app/static/css/editor-theme.css` re-dresses it. Every value in that file
is one of main.css's theme variables, so the editor now follows the
light/dark/manuscript toggle like every other surface: the frame is a field
like the tags and title fields around it, the toolbar is transparent over
that field with a hairline under it, and the writing area is the theme's
own paper carrying the theme's own text colour. The prose itself is
`var(--font-serif)` at 1.0625rem/1.7 — the same typography `.story__body`
uses on the finished page, a shade smaller so a paragraph still fits a
phone. Blockquotes take the accent-coloured left rule the story page gives
them. Writing a memory now looks like reading one.

The dressing goes all the way down, because half-dressed is worse than
undressed: the link and image dialogs, the context menu, the ⋯ overflow
toolbar a phone falls back to, the tooltips, the Markdown/WYSIWYG tabs, the
markdown-mode syntax colours, and the `==` highlight button `editor.js`
adds by hand (which had no colour of its own at all and was invisible on a
dark toolbar).

**Two mechanical rules, both easy to break silently, both now tested.**

The sheet is linked from `_editor_head.html` rather than living in
main.css, because base.html links main.css *before* `{% block head %}` —
rules in main.css would load before the vendor's and lose. And every
selector carries a `:root` prefix, which is not decoration: the vendored
dark theme selects with two classes (`.toastui-editor-dark
.toastui-editor-defaultUI-toolbar`), so a one-class rule here loses to it
whatever the load order. `:root` buys exactly the class-worth of
specificity that ties it, and last-loaded then wins. Drop the prefix on one
rule and that rule stops applying **in dark theme only** — the kind of bug
that ships.

The vendored CSS itself was not touched, and the vendored dark theme is
still loaded: it carries the toolbar icon sprite's second row (light glyphs
at `background-position-y: -49px`) plus dozens of rules for tables, code
blocks and task lists this app's toolbar never offers. Replacing all of
that to save one HTTP request would have been a lot of surface area for
nothing.

One consequence worth naming: the icon sprite is the only part of the
editor that can't be a CSS variable, since the row is chosen by a class.
`theme.js` now fires a `storybook:themechange` event and `editor.js`
re-applies `toastui-editor-dark` on the editor when it hears one, so
switching theme with the editor open no longer leaves light glyphs on a
suddenly-cream toolbar. Everything else follows the toggle live, for free.

While in there, a mobile bug that predates this: the vendor centres its
300px popup on the button that opened it by hand (`left: <px>` inline plus
`margin-left: -150px`), which on a 390px phone drops half the link dialog
off the left edge. Under 32rem the popup is now pinned inside the editor
instead. The one `!important` in the file is there because the vendor's
position is an inline style set from JS, and that is the only way to beat
one.

### Firelight

The app is called *veillée* — an evening spent together by the fire — and
the reading themes are all warm paper and lamplight, so the room was asking
for the fire itself.

`.firelight` is a fixed, click-through overlay of two warm radial gradients
that animate nothing but `opacity`, so the whole effect lives on the
compositor and can never cause a layout or a repaint. The two layers run on
deliberately mismatched cycles — 11s and 7.3s, one reversed — because a
fire that pulsed on a countable beat would read as a broken animation
rather than a fire. Measured on the timeline in dark theme, the mean
brightness of the upper page drifts between about 26.6 and 30.4 of 255 over
a cycle: a breath you notice if you look up, never a flicker you have to
read through.

Each theme declares its own `--firelight-strength`, because a wash that
looks like lamplight on `#141210` looks like a yellow filter on aged paper:
dark takes it at full strength, light and manuscript at about half. That
variable has **no fallback** on purpose — a new theme that forgets to
declare it should fail a test rather than quietly wash a bright page at
full strength, and `test_every_theme_declares_its_own_strength` is that
test.

The button next to the theme toggle turns it off for good. Like the
theme, the choice is stored in `localStorage` and re-applied by
`theme-boot.js` in `<head>`, so a page never paints the wash and then yanks
it away. Only the string `"off"` is ever *read* back, because firelight is
on by default and an empty slot has to mean on for a first visit. The
button isn't rendered without JS (it couldn't do anything), and it carries
`aria-pressed` set from the DOM rather than from the server, since the page
is cacheable and the preference isn't.

Restraint, in the places it matters: `pointer-events: none` so it can never
swallow a click; `z-index: 1`, above the page but under the lightbox (200)
and the skip link (100); hidden entirely in print; and no animation at all
under `prefers-reduced-motion: reduce`, where the layers keep their warm
tint but stop moving — the same bargain `.lasso-spinner` makes. It is
decoration, so the overlay is `aria-hidden` and only the button is
announced.

### Tests

`tests/test_editor_theme.py` (7) pins the two contracts that break
silently: the stylesheet loads after both vendor sheets on both editors,
every selector keeps its `:root` prefix, no hex colour ever appears in the
file, the icon sprite is never touched with the `background` shorthand
(which would erase every glyph), and no other page pays for a sheet it
doesn't need.

`tests/test_firelight.py` (14) covers the markup on every page including
login, the `aria-hidden`/`aria-pressed` split, the `data-firelight`
attribute applied before first paint, the button not being offered without
JS, every theme declaring a strength, the reduced-motion guard, the two
cycles being unequal, `pointer-events: none`, the z-index staying under the
lightbox, and the print rule.

Verified in a browser at 390px and 1280px across all three themes: the
editor with prose in it, both editor modes, the ⋯ overflow toolbar, the
link dialog on a phone, and the firelight measured frame by frame.

`pytest` (1135) and `ruff check .` green.

### Follow-up: a flame you can see, and a fire you can notice

Two things the first cut got wrong, both reported from a real browser
rather than a screenshot.

**Nobody could tell whether the firelight was on.** The switch was a bare
☼ glyph that looked identical in both states — `aria-pressed` told a screen
reader and nobody else. It now carries a flame, hand-drawn as inline SVG in
the spirit of `favicon.svg` (two paths, no gradients, no filters), and the
two states are told apart three ways at once: the flame is amber in a ring
of the same colour when lit, and grey, ringed in plain border and scaled to
82%, when out. Three signals rather than one because WCAG 1.4.1 rules out
colour on its own, and because a difference you have to hunt for isn't a
difference.

The flame is inline rather than an `<img>` precisely so it can inherit the
button's `color`, and its hollow heart is a filled path in
`var(--color-bg-raised)` — the button's own background showing through —
which is why it stays correct in all four themes without a second asset.
The label went from the noun "Firelight" to the action, "Turn the firelight
off" / "on", rewritten by `firelight.js` from the same string table
everything else in the app reads, so it's right in French too.

**The wash itself was too faint to notice.** Measured, the first cut moved
the mean brightness of a dark page by 3.85 of 255 — real, but below the
threshold where you'd spot it without being told. Three changes, in order
of how much each mattered:

- The keyframes now dip to 0.3 instead of 0.58. The *swing* is what reads
  as fire, not the tint, so travelling further costs nothing in how orange
  the page ever gets.
- `--firelight-strength` stopped being an `opacity` on the container and
  became a multiplier on the gradient alphas. This is not a refactor: an
  `opacity` clamps at 1, and the pale themes need *more* paint than the
  dark one, not less. Amber added to a near-white page barely changes its
  brightness at all, so the same visible swing costs roughly 1.6× there.
  A theme that now forgets to declare the variable makes the gradient
  invalid, which paints nothing — a safe failure, and still a test failure.
- A third layer, `.firelight__shadow`, darkens instead of lighting. This is
  the one that rescued the manuscript theme: adding amber to aged cream
  shifts its hue and not its luminance, but corners falling into shadow
  read as the fire dipping on *any* background. It runs on its own 9.1s
  cycle, so all three layers are now mutually out of step.

Measured again over a full cycle, mean page brightness now moves 24% in
dark (10.8 of 255 across the top of the page, where the glow is
strongest), 4.1% in light and 3.5% in manuscript — the pale themes still
the quietest, which is the honest ceiling for warm light on white paper,
but all three now visibly breathe.

`tests/test_firelight.py` grew to 20: the flame's two paths, the three-way
state difference, the switch's rules coming after `.theme-toggle`'s in the
file (both are one class deep, so order is all that decides them), the
action labels being in the table JS reads, the strength being a multiplier
with at least one theme above 1, the darkening layer, and three distinct
cycle durations rather than two.

`pytest` (1141) and `ruff check .` green.

## F45. A toggle that looks off when it is off

Reported from real use: the editor's **Draft** and **Archive** chips didn't
seem to switch off when you clicked them.

They did switch off — the state round-tripped to disk correctly the whole
time. What failed was the paint, and the cause was a collision between two
rules that were each reasonable on their own:

```css
.btn:hover                              { border-color: var(--color-accent); }
.editor__toggle-chip[aria-pressed=true] { border-color: var(--color-accent);
                                          color: var(--color-accent); }
```

The accent is what "on" means on every toggle in the app — and it is also
what hover gives every button in the app. So with the pointer still resting
on a chip you had just switched off, the two states differed by *text
colour alone*, under an identical accent ring, next to a colour icon that
never changes. On a phone it was worse than subtle: `:hover` sticks to the
last element tapped until something else is tapped, so a chip you turned off
went on looking lit indefinitely.

Both halves are now fixed:

- **A lit toggle is filled, not merely outlined** —
  `background: var(--color-highlight-bg)` on top of the accent border and
  text. A fill is something hover never gives, so it is the signal that
  actually separates the states, and it holds up in all four themes because
  it is the theme's own highlight colour.
- **Hover on an unlit toggle stops at a neutral border**
  (`var(--color-text-dim)`) instead of the accent. F23 asked for hover
  feedback on everything; it just can't be delivered in the one colour that
  already carries meaning here.

Applied to `.editor__toggle-chip` (Draft, Archive and F40's audience chips,
which share the class) and to `.editor__gender-btn`, which had exactly the
same two-rule collision one screen over. `.editor__author-chip` gets the
hover half — it had the same defect, but its lit colour is the author's own,
so a generic accent fill would fight it. `.people-picker__row` was already
safe: a ticked row shows a ✓, and a shape is not a colour.

### Tests

`tests/test_toggle_chips.py`, four: the lit state carries a fill and not
just an outline, hovering an unlit toggle doesn't borrow the accent, the
toggle rules stay downstream of `.btn:hover` in the cascade, and — since the
wiring is what makes the paint worth having — the draft flag still round
trips through the API to disk.

Verified in a browser in all three themes at 390px and 1280px, including
the case that produced the report: clicking a chip off and leaving the
pointer on it.

## F46. Theme packs — the art direction as a folder

The app had three *colour schemes* (dark, light, manuscript) and exactly one
*look*: the hand-drawn western storybook of F17 and F22. Adding a palette
was already 15 lines. Adding a **different world** was impossible, because
every one of the 37 pictures was named directly in a template.

This splits the two apart. A **theme pack** is a folder:

```
app/static/themes/ranch/img/*          ← the 37 files that were in static/img/
app/static/themes/orbit/theme.css      ← a palette, and no pictures at all
```

Templates stopped naming folders. `{{ theme_img('help-lantern.jpg') }}`
returns the configured pack's copy when it has one and the default pack's
otherwise, and `STORYBOOK_THEME` says which pack a book uses.

### The fallback is the whole design

A pack of 35 illustrations is a wall nobody starts climbing. A pack that
works the day its palette is written, and takes its artwork one picture at
a time, is a ramp. So a pack **only has to draw what it wants to change**,
and `orbit` ships today with a complete palette and zero image files,
borrowing every picture from `ranch` while its own are drawn.

Everything else follows from wanting that property to stay true:

- **A pack is a skin, not a rename.** The same filename means the same
  picture in every pack. Rename one and it silently inherits the default's
  forever while shipping a file nothing loads — so a test walks the packs
  and fails on any file the default pack has no name for.
- **The default pack is the only one allowed no holes.** Another test
  scans every `theme_img(...)` call in every template and fails if `ranch`
  is missing one.
- **An unknown `STORYBOOK_THEME` fails at startup**, like
  `STORYBOOK_AUTHORS` does. Silently serving the default pack would be a
  puzzle to debug and the fix is one word.
- **The filename is validated like a path, because it is one.** It builds a
  URL *and* a filesystem probe, so anything that isn't a plain asset name
  resolves to the default pack rather than being interpolated.

### Two axes, kept apart

The pack is the **book's** identity, set once by whoever runs it. The
light/dark/manuscript toggle stays **each reader's** choice within it. So a
pack declares all three schemes rather than replacing the toggle — three
states, not nine, and a reader who prefers a light screen still gets one
whatever world the book is set in.

### What a pack can change, beyond colour

Three ranch-isms were hardcoded in `main.css` and had to be lifted for a
pack to be more than a palette:

- `--illo-mount` / `--illo-mount-edge` — the `.illo` card's paper. It was
  literally `#f9f2e1`, the cream the shipped JPEGs are drawn on. A pack
  whose pictures are drawn on black needs the mount to follow, or every
  card shows a seam.
- `--flourish-image` / `--brand-mark` — the two pictures CSS draws rather
  than a template names (the rope divider, the tree's root star). Both are
  now variables, and both use background *longhands* rather than the
  shorthand, so a pack can supply several gradient layers instead of one
  image — which is exactly what `orbit` does, drawing its divider and star
  in pure CSS and shipping no file for either.
- `--ambience-glow` / `--ambience-glow-edge` / `--ambience-shade` — F44's
  firelight, as colours. The machinery is untouched; only the hue moves. In
  `orbit` the hearth becomes a distant star: cold white-blue light, and the
  shadow it leaves when it dips is the void rather than soot.

`--photo-filter` was already a variable, so `orbit` drops F35's sepia for a
faint cool cast without any change to the code that applies it.

### The orbit pack

A ship's cabin on the night side of a planet: `#080b16` ground, instrument
cyan `#5cc8f5`, rust orange for warmth. Its "manuscript" scheme is the
daylight side — pale regolith grey with a fine dust grain, reusing the same
self-contained SVG turbulence the ranch's aged paper uses.

`IMAGE-PROMPTS-ORBIT.md` is its prompt catalogue: 17 illustrations and 13
icons, each with what a reader has to understand from the picture alone,
plus the pack's house style (retro-futurist encyclopaedia plates,
cosmonauts with dark visors, rings as the signature shape). It carries the
ranch pack's two hard rules unchanged — no lettering ever, because the
interface is bilingual, and no faces, so any reader can be the cosmonaut.

Written as a separate file rather than a section: a house style belongs to
one art direction, and two sets of style rules in one document is how a
pack drifts.

### Tests

`tests/test_themes.py`, 25: the fallback in both directions, a pack serving
what it has, an unknown pack falling back rather than interpolating,
filenames that aren't plain asset names (traversal, subpaths, uppercase,
empty) never reaching a pack, pack names rejected the same way, the default
pack being complete against every `theme_img` call in every template, no
pack shipping a file the default has no name for, no template naming an
image folder directly, `main.css` hardcoding no pack's art, an unknown
`STORYBOOK_THEME` raising at startup, and a real page served under `orbit`
carrying orbit's stylesheet and ranch's pictures.

One F44 test changed shape: it asserted the shadow layer's literal
`rgba(26, 15, 4, …)`, which is now `var(--ambience-shade)`. It asserts the
variable instead — the layer still has to exist and still has to darken.

Verified in a browser under `STORYBOOK_THEME=orbit` at 1280px: login,
timeline and a story page, including the CSS-drawn divider and the
inherited ranch illustrations mounted on orbit's dark plate.

### Follow-up: a pack owns its schemes, and orbit gets a sky

Three corrections from seeing it running, all of them the same mistake:
orbit had inherited assumptions from the ranch instead of making its own.

**A pack now decides which colour schemes it offers.** Orbit's third scheme
was aged-paper regolith — a ranch reflex, and the wrong world. But deleting
it wasn't enough, because the toggle's list was hardcoded in `theme.js` and
would still have cycled to a scheme the pack no longer designed. So a pack
declares its schemes in an optional `theme.json`:

```json
{ "schemes": ["dark", "light"] }
```

That list reaches the page as `<html data-schemes="dark light">` — on the
root element, so `theme-boot.js` can read it in `<head>` before first paint
— and both scripts now work from it instead of a literal. `theme.js` cycles
it; `theme-boot.js` checks membership before applying whatever was stored,
so a reader who chose *manuscript* in a ranch book and then opens an orbit
one isn't handed a scheme that pack never designed. They fall back to their
system preference, which is the right answer and not an error.

Anything unreadable in `theme.json` means *all* the schemes, never none —
a pack with a typo in its metadata should look over-generous, not present a
toggle that does nothing.

**Both of orbit's schemes are blue now.** The night side is near-black
(`#04060d`) with marine blue in the raised surfaces; the day side is sky
blue and marine, the same two colours the other way round. Not white paper
— there is no paper out here, and a white scheme in a space book was the
same borrowed instinct as the regolith.

**And it has a sky.** A new `--surface-texture` variable, defaulted to
`none` in main.css and applied on `body`, lets a pack lay something over
its background. Orbit tiles a starfield: two self-contained SVG data URIs
at different sizes and brightnesses — a dense field of faint far stars at
360px, a sparse one of brighter near stars at 600px — so the pattern never
lines up with itself and the sky has some depth. Nothing is fetched, the
same rule the ranch's aged paper follows. The light scheme sets it to
`none`: the stars are still there, you simply can't see them in daylight.

That starfield cost an hour to a trap worth writing down: **a raw `#`
inside `url("data:image/svg+xml,…")` starts a fragment identifier.** Every
`fill='#cfe2ff'` truncated the SVG at the first colour. The CSS parsed, the
property computed, `background-image` reported a `url(...)`, and nothing
was drawn. It has to be `%23`, and a test now walks every pack's stylesheet
and fails on a raw `#` in a data URI.

### Tests

`tests/test_themes.py` grew to 40: the scheme list defaulting to all three,
orbit narrowing it to two, six kinds of unusable `theme.json` all falling
back rather than emptying the toggle, `data-schemes` rendered for both
packs, both scripts reading it rather than hardcoding, theme-boot checking
membership before applying a stored scheme, the `%23` rule across every
pack's CSS, and orbit putting stars in the night and not in the day.

`tests/test_i18n.py` asserted the exact string `<html lang="en">`; the tag
grew `data-schemes`, so those five assertions now match the lang attribute
without pinning the whole tag.

Verified in a browser: the toggle cycling dark→light→dark and never
offering a third stop, a stale `manuscript` from another book being ignored
on load, and the starfield measured off a screenshot (peak pixel 224 of 255
against a `#04060d` sky) rather than trusted to the eye — which is how the
truncated data URI was caught in the first place.

### Follow-up: the pack gets its artwork

All seventeen of orbit's illustrations arrived, generated from the prompts
in `IMAGE-PROMPTS-ORBIT.md` and committed under
`app/static/themes/orbit/img/` — 928 KB in total. The pack now inherits
from the ranch only its icons:

| File | Size | | File | Size |
|---|---|---|---|---|
| `login-campfire.jpg` | 856×621 | | `accounts-keys.jpg` | 760×510 |
| `person-oval.jpg` | 590×732 | | `invite-card.jpg` | 700×564 |
| `empty-chest.jpg` | 729×587 | | `write-link-pass.jpg` | 700×564 |
| `group-circle.jpg` | 860×450 | | `help-lantern.jpg` | 582×700 |
| `sealed-letter.jpg` | 486×620 | | `book-frame.jpg` | 723×897 |
| `firsts-boots.jpg` | 760×496 | | `instant-camera.jpg` | 652×516 |
| `growth-doorpost.jpg` | 558×760 | | `tree-sapling.jpg` | 605×760 |
| `almanac-book.jpg` | 700×700 | | `tumbleweed.jpg` | 900×429 |
| `history-pages.jpg` | 720×598 | | | |

Two things every generation needed fixing, and neither is a judgement call,
so `scripts/process_orbit_plates.py` does both and stays in the repo for
the next batch:

- **A cream paper mat.** Six plates came back matted on card stock, which
  against orbit's dark `--illo-mount` reads as a double frame. The script
  strips a margin only where it is genuinely uniform and light, so a plate
  whose own artwork reaches the edge — a lit horizon, a pale regolith
  floor — is never cut into.
- **The generator's corner sparkle.** Every single plate carried a small
  grey four-pointed mark near the bottom-right. Detection is the obvious
  approach and it fails: on the plates where the mark sits on pale
  regolith it has almost no local contrast. Measuring instead showed it is
  stamped at a *fixed* inset — 97 to 144 pixels from the right and bottom
  edges, about 47 across — in every generation regardless of aspect ratio.
  So it is covered by geometry, with the same box copied from directly
  above it, which is invisible at display size because these backgrounds
  are locally uniform vertically.

The prompt document gained both as hard rules for future generations, on
top of the two it already had, and every prompt block now carries the
negatives inline.

Two plates took a second pass, and both are worth recording because they
are the failure modes to watch for in the next batch:

- **`group-circle.jpg`** came back with the crew's faces visible through
  their visors. On any other picture that would be a style slip; on this
  one — the only illustration in the app whose job is to *teach* the
  scoping rule rather than decorate — a face turns it into a portrait of
  somebody. The fix was one sentence added to the prompt (*every visor is
  completely dark and opaque, with nothing visible behind it*), and the
  regeneration also improved the composition: the figure outside the ring
  is now visibly busy with a rover of their own, which is exactly the
  "not excluded, just not in this one" reading the picture needs.
- **`login-campfire.jpg`** was simply missed in the first batch, and it is
  the first thing anyone ever sees.

### Follow-up: the first icons, and the rule they taught

Five icons came back; two were committed (`icon-new-story`,
`icon-instant`) and three were not. `scripts/process_orbit_icons.py` does
their processing: cover the corner sparkle *first* — it is lighter than
the grey backdrop, so the key would stop at it and leave an opaque speck
floating beside the icon — then flood the background from the four corners
so an enclosed grey area *inside* the artwork (the hole in a ring, the
gaps in a dashed circle) stays part of the icon instead of being punched
out with it, then trim, pad to a square by 2%, and downscale to 160×160.

**What the batch taught is a contrast rule, and it is the useful part.**
An icon has to read on both of orbit's schemes, and measured against the
raised surface each sits on, *no single colour in the pack's palette
does*:

| | night side | day side |
|---|---|---|
| pale starlight `#dce6f5` | 14.5:1 | **1.11:1** |
| instrument cyan `#5cc8f5` | 9.6:1 | **1.36:1** |
| dark navy `#17253f` | **1.19:1** | 10.9:1 |
| rust `#c8622f` | 4.6:1 | 2.9:1 |

A pale or cyan icon vanishes in daylight; a dark one vanishes at night.
Which is exactly why the ranch's icons survive on both cream and
near-black: they are light shapes inside a *dark outline*, so whichever
scheme you are in, one half of the icon carries it. The orbit icon prompt
now requires a dark navy outline on every shape, thick enough to survive
20 pixels, with cyan and starlight as fills inside it. Rendering the batch
at 20/24/44px on both schemes is what surfaced this; the two icons that
passed did so because they are chunky solid masses, not because they were
right.

The second lesson was smaller and also general: **a subject line has to
name a shape, not a concept.** "A ringed planet inside a downward chevron"
came back as a shield with ears — the generator drew the container and
ignored the direction. The three rejected subjects were rewritten to
describe silhouettes ("a thick downward-pointing arrow, its shaft crossed
by a tilted planet's ring seen edge-on…").

The three that were held back — `icon-save` (read as a fox's head),
`icon-draft` (strokes too fine, and pale-on-pale in daylight) and
`icon-archive` (read as a cup) — are simply absent from the pack, so those
buttons keep the ranch's icons until a better generation lands. That is
the per-file fallback doing exactly the job it exists for: a wrong icon is
worse than a borrowed one.

`pytest` (1185) and `ruff check .` green.


## F47. A recording that survives a locked screen

Reported from a phone, and the worst kind of bug this app can have:

> my screen turned off while recording on the app on chrome and the thing
> stopped recording when my phone screen closed... that is a real problem
> as I lost nearly 2 minutes of recording because of this

...and then, on looking at the file:

> the recording carried on but there was no voice during the 2 minutes.
> and when I stopped the thing there is 1 minute of recording and 2
> minutes of no noise

That second message is the whole feature. The recorder did **not** stop.
Android took the microphone away with the screen and `MediaRecorder` went
on banking silence — no error, no `stop` event, a timer still counting up.
Someone talked for two minutes into a microphone that was not there, and
found out on playback. A recorder that dies loudly is a nuisance; one that
keeps a straight face while recording nothing is a trap.

Underneath it is a second property, the one that makes any of this
dangerous: **until a recording is stopped and uploaded, its audio exists
in exactly one place — the tab.** No file on disk, nothing on the server,
nothing another tab could recover.

So there are three jobs, in order of how much they are worth:

1. keep the screen on, so the microphone is never taken in the first place;
2. when it is taken anyway, end the recording *on purpose* and keep what
   was captured — never carry on into silence;
3. show the input level, so a microphone that dies is visible while
   someone is still talking rather than discovered afterwards.

### Keep the screen awake — `static/js/wake-lock.js`

A small module around the [Screen Wake Lock
API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Wake_Lock_API):
`request()` while recording, `release()` when the microphone is released.
It needs a secure context, which is the same condition `getUserMedia`
already imposes — wherever recording works at all, the lock can at least
be asked for.

The part that is easy to get wrong: **the browser drops the lock whenever
the page is hidden, and never gives it back.** A page that asks once and
assumes it holds the screen forever is wrong the first time the user
glances at a notification. The module therefore remembers that the lock is
*wanted*, listens for `visibilitychange`, and asks again on the way back —
and asks for nothing while hidden, where the request would be refused
anyway.

Everything about it is best-effort by design. A browser without the API, a
battery saver refusing the request, a rejected promise — all resolve
`false` and change nothing except that the screen behaves as it always
did. Nothing downstream is allowed to depend on the lock being held; the
salvage below is what makes the feature safe, and the lock is what makes
it pleasant.

### Treat an interruption as the end of a recording, not a failure

The rule is stated once, in `static/js/recorder-logic.js`, and it has no
exceptions: **anything that interrupts a recording stops it on purpose.**
Stopping is what makes `MediaRecorder` hand over its chunks; letting the
browser kill the recorder instead is what loses them. Four interruptions,
all of them observed rather than imagined:

| reason | what it is |
| --- | --- |
| `hidden` | the page went to the background — screen lock, or an app switch |
| `ended` | the microphone track ended: device gone, or taken by another app |
| `muted` | the track went silent, so carrying on would bank silence |
| `error` | `MediaRecorder` itself gave up |

Each carries its own sentence, shown *after* the audio is safe, so the
news arrives with the memo rather than instead of it: "Recording stopped
when the page went to the background. Everything recorded up to then has
been saved." An unrecognised reason salvages too, and borrows the generic
wording — a new browser behaviour should cost a vague message, never the
recording.

This does mean switching apps mid-recording ends the memo. That is the
deliberate trade: a memo that stops early is an inconvenience, and the
next tap starts another one; a memo that records silence, or vanishes, is
not recoverable at all.

### Show the level — the thing that would have caught it live

Interruptions only help if the browser reports one, and the case that
started this reported nothing at all. So while a recording runs, the input
is measured through an `AnalyserNode` and drawn as a small bar beside the
timer. It costs one `requestAnimationFrame` loop and answers, continuously,
the question no wording on a page can: *is it still hearing me?*

The same measurement feeds a watchdog. A live microphone in a silent room
is never mathematically silent — room tone and the preamp's own noise sit
orders of magnitude above zero — while a microphone the phone has switched
off is exactly zero. Twenty unbroken seconds of that is treated as `muted`
and salvaged.

Three deliberate limits on it:

- **Twenty seconds, not five.** Some phones gate their noise suppressor all
  the way to zero between words. The two mistakes are not equal: ending a
  good recording early is a rude surprise, while missing a dead microphone
  only falls through to the interruptions above, which catch the
  screen-lock case anyway.
- **It stands down while paused.** Nothing is being kept, so a silent pause
  means nothing.
- **It stands down without float precision.** `getByteTimeDomainData`
  quantises a quiet room's noise floor to zero, which would make the
  watchdog stop perfectly good recordings; where only 8-bit data exists the
  bar still moves and only the watchdog goes quiet.

The bar is `aria-hidden`: it duplicates nothing a screen reader needs, and
when it matters the watchdog says the same thing in words.

### The upload queue

Salvaging is only half of it. The likeliest moment to *need* the salvage —
a phone freezing the page behind a lock screen — is also the likeliest
moment for the upload to be cut off mid-flight. So a finished recording
goes into a queue rather than straight into a single in-flight request:

- the head is uploaded; on success it is shifted off and the next one
  starts, so a memo saved during an interruption never blocks the one
  recorded after it;
- **on failure it stays at the head.** Every way back into the page —
  `visibilitychange` to visible, another recording finishing — drains the
  queue again. A network failure is told apart from a refusal by the
  server, so the message can promise another go ("keep this page open and
  it will try again") instead of blaming the file;
- while anything is queued, or a recording is running, `beforeunload`
  warns. Closing the tab is now the only way left to lose audio, and it
  takes a confirmation.

### The clock, made a value

`recorder-logic.js` also owns the elapsed-time clock the timer reads:
`{ banked, startedAt }`, with `start`/`pause`/`resume` as pure functions of
the old clock and the current time. It replaces a pair of mutable
variables in `editor.js` that pause and resume shuffled between them, and
it is where two small bugs were fixed on the way past — a system clock
jumping backwards can no longer run the timer backwards, and an hour of
recording now reads `1:00:00` instead of `60:00` (memos have no length
cap, so an hour is reachable).

### Tests

The two decidable pieces are DOM-free UMD modules with plain-Node tests,
per the repo's usual split:

- `tests/js/recorder_logic_test.mjs` (29) — the clock across pause,
  resume, restart and a backwards system clock; the `mm:ss` / `h:mm:ss`
  readout; every interruption salvaging, including one nobody anticipated;
  the watchdog holding its nerve through a noise floor and a reset run, and
  the meter's dB curve putting speech in the middle of the bar.
- `tests/js/wake_lock_test.mjs` (11) — driven through a hand-written fake
  window, which is the only way to stage the case that matters: the
  browser dropping the lock while hidden, and the page taking it back on
  return. Also that a refusal resolves `false` rather than throwing, and
  that an unsupported browser is simply unsupported.
- `tests/test_recording_guard.py` (20) — the server-rendered contract: the
  scripts are served on both editor pages and *before* `editor.js` (no
  bundler, so page order is the whole dependency mechanism), the lock is
  released where the stream is, every interruption is wired up, the
  beforeunload guard covers unsaved audio, the queue only shifts on
  success, the meter ships hidden and takes its colour from the theme, the
  watchdog stands down while paused and without float precision — and,
  asking `recorder-logic.js` itself for the list so it cannot drift, that
  every sentence the recorder can say exists in `JS_STRINGS` and is
  translated into French.

Verified by hand in Chromium at 390px with a fake microphone, which is the
only way to see the actual bug: record, hide the page, and watch the memo
arrive anyway. Also checked there: the lock held and then let go, the
blocked-upload-then-return retry, the bar moving with the fake device's
tone and dropping to zero while paused, and the watchdog ending a recording
into silence with its memo intact.

`pytest` (1207) and `ruff check .` green.


## F48. Picking the art direction from the nav

> hum where do I change the theme in the interface?

Nowhere, was the answer. F46 made the art direction a folder and left
choosing it to `STORYBOOK_THEME` — an environment variable and a restart,
which is a strange price for "let me see what the other one looks like".
The colour-scheme toggle sat right there in the nav the whole time, which
made it worse: two things called "theme", one of them a tap away and the
other one a redeploy.

### What it changes, and for whom

The question that decides the whole feature is *whose* screen a pick
changes. Three answers were on the table; this is the middle one:

- **`STORYBOOK_THEME` stays the book's pack** — what every reader gets
  unless they say otherwise, and still the only way to change what the
  family sees.
- **A reader can put another pack on their own screen**, from a picker in
  the nav. It is a cookie, so it reaches exactly one browser and outlives
  logging out.

The alternative — writing the choice somewhere shared so any family member
redecorates the book for everyone — was rejected for the obvious reason: a
grandmother trying the other art direction should not repaint the
grandchild's book. F46's docstring claimed the pack "is the book's own
decision, not a per-reader toggle"; that claim is now half wrong and has
been rewritten rather than left to mislead.

### Where it resolves

One function, `themes.pick_theme(chosen, configured)`, and one place it is
called: a `before_request` that puts the answer in `g.theme`. Everything
that used to read `config["THEME"]` — `theme_img`, the pack stylesheet,
the scheme list — reads a `current_theme()` helper instead. Anything added
later that reaches for the config directly will silently ignore the
reader's choice, which is why `CLAUDE.md` now says so out loud.

`pick_theme` forgives everything: a cookie naming a pack since deleted, a
hand-edited one, a name with a `..` in it. All of them fall through to the
book's pack and then to `ranch`, because a book that renders beats a book
that argues. Startup still argues — `_parse_theme` refuses an unknown
`STORYBOOK_THEME` outright — because that is where there is a person
reading the error.

### The picker

Built as the language picker's twin, deliberately: it sits beside it, does
the same kind of thing, and two neighbouring controls that behave alike
should look alike. One tiny POST form per pack — works with JavaScript
off, CSRF-protected like every other state change, a real 44px tap target
each — with `next` carrying the current path so changing the art leaves
you on the page you were reading. The current pack is marked with
`aria-current` and a border rather than removed from the row, so nothing
reflows under your thumb.

Each pack shows two or three dots of its own palette, overlapping like
fanned paint chips so they read as one object. The colours come from the
pack's `theme.json`, never from the template — a picker that knew any
pack's colours would be a third place to update when a pack changes its
mind. On a phone the names are visually hidden (still in the accessibility
tree) and the swatches are what you aim at, because the nav is already
carrying a brand, two toggles, two flags and five links.

Two details that fall out of the design rather than being decided:

- **A one-pack install renders no picker at all.** A control offering one
  choice is a button that does nothing.
- **A new pack needs no code.** Drop a folder in with a `theme.json` and
  it is in the picker, with its name and its swatch.

Also, the `theme.json` schema grew from "the schemes, so far" to a real
little manifest: `label`, `swatch`, `schemes`. Both shipped packs now have
one — `ranch` had none until today, since it had nothing to declare.

### One string had to be split

The `◐` button's label was "Toggle color theme" and the new group's is
"Theme". Two controls with the same name, one of which changes the
palette and the other the entire art direction, is exactly the confusion
that produced the question at the top of this section — so the toggle is
now "Toggle light and dark" (*Basculer clair / sombre*).

### Tests

`tests/test_theme_picker.py` (23): the resolution order and every way a
name can be wrong; that each shipped pack names itself and declares a
swatch; that the picker is in the nav, marks the current pack, and
disappears for a one-pack install; that a pick sets an HttpOnly SameSite
cookie, really does change the stylesheet and the artwork served, drags
the scheme list along with it, survives logging out, works before logging
in, and is confined to the browser that made it; and that the route
refuses an unknown pack, a GET, a missing CSRF token and an off-site
`next`.

One existing test had to be re-scoped rather than the code changed:
`test_story_page_unknown_author_renders_neutral` asserted the author
colour appeared nowhere in the page, and the ranch's swatch is that same
amber. The colour reaches a story through `--author-color` on the
`<article>` and nowhere else, so that is what it checks now.

Verified by hand in Chromium at 390px and 1280px: the swatches, the 44px
targets, the switch landing back on the same page, and orbit's own icons
and starfield arriving with it.

`pytest` (1230) and `ruff check .` green.


## F49. One button for how the book looks

F48 put the pack picker in the nav and it worked, but it left two
neighbours doing related things — a cycler and a row of swatches — plus
the flame, the flags, the brand and five links, on a phone. The suggestion
that fixed it:

> to switch themes maybe it would be better to have a long touch or long
> press on the color toggle button rather than the 2 themes. even thinking
> maybe the long press should disclose the theme configuration

So the swatches moved *under* the `◐` button. A tap still cycles light and
dark — that is the fast path, and losing it would be a bad trade — and
holding the button opens a panel with the colour schemes and the packs.

### It is a `<details>`, and that is the whole trick

The obvious build is a button and a `hidden` div, which is also the build
that stops existing when JavaScript does. Instead the control is a real
`<details>`/`<summary>`, so there are two honest behaviours rather than
one behaviour and a broken state:

- **No JavaScript:** an ordinary disclosure. Tap, the panel opens, and the
  pack forms inside it are the same POST forms F48 shipped. Switching the
  book's art direction works with scripting off entirely.
- **JavaScript:** `theme.js` takes the tap for the fast path (the summary
  never toggles itself) and opens the panel on a hold, a right-click, or
  the down arrow instead.

The colour-scheme chips are the one part that genuinely needs JavaScript —
they are remembered in `localStorage` — so they are the one part hidden
until the `js` class is on the root. A chip that couldn't remember what it
was showing would be worse than no chip.

### What a press means

Three inputs, one pure function (`theme-logic.js`, tested under Node), and
the order they are tested in *is* the rule:

| | |
| --- | --- |
| held | open the menu — and, critically, the click that a long press leaves behind must not also cycle. Someone holding the button to look at their options would otherwise have their colours changed underneath the menu they asked for. |
| menu open | the toggle is the way out of it |
| otherwise | cycle, which is why the menu is behind a hold in the first place |

Around that: 450ms to count as a hold, `pointerdown`/`pointerup` so mouse
and touch are one code path, `contextmenu` intercepted (press-and-hold
with a mouse is a right-click, and on a phone the callout would otherwise
land on top of the menu it was meant to open), Escape and an outside click
to close, and `-webkit-touch-callout: none` plus `user-select: none` so
iOS doesn't select the glyph under the finger instead.

### The honest cost

**A hold is undiscoverable.** Three mitigations, and none of them is a
complete answer:

- the button carries a small notch in its ring — enough to say there is
  more here, not enough to read as a second button;
- its `aria-label` says what a press does *and* how to open the menu,
  because a disclosure whose activation doesn't disclose has to explain
  itself, and a screen-reader user who hears "collapsed" and then gets a
  colour change deserves better than a surprise;
- the Help page (F33's family-facing glossary) gained a "How it looks"
  section covering all three controls, the flame included.

Keyboard users get the down arrow, which also moves focus into the panel.
Right-click covers a mouse. Both are documented in the label rather than
left to be guessed.

### Two things that came along

- **"System" is now reachable.** The cycler could put you *into* a chosen
  scheme but never back out of one; the panel's last chip forgets the
  stored value so the page follows `prefers-color-scheme` again, exactly
  as a first visit does. It also restores the two `theme-color` metas,
  which are captured before anything overwrites them.
- **The cycle now starts from what you chose,** not from what you are
  looking at. It reads the stored value rather than the computed one, so
  the first tap after "System" lands on the first stop instead of the one
  after whatever the OS happened to be showing.

### Tests

- `tests/js/theme_logic_test.mjs` (9) — the cycle across both packs'
  scheme lists, a scheme the current pack doesn't offer, and every
  combination of the press table, including the one it exists for.
- `tests/test_theme_menu.py` (13) — the disclosure markup, the label
  mentioning the hold, the picker having actually moved inside, the chips
  following the pack (no manuscript in orbit), the schemes hidden without
  `js` while the pack forms are not, the summary's marker suppressed in
  every engine, the callout suppressed, and the chosen chip not told apart
  by colour alone (F45's rule).

Verified by hand in Chromium at 390px with touch: tap cycling all three
and wrapping, a hold opening the panel *without* cycling on the way in,
picking a scheme, "System" clearing `localStorage`, tap-to-close,
ArrowDown-to-open with focus landing on the first chip, Escape, an outside
click, switching pack from inside the panel — and the whole thing again
with JavaScript disabled, where the panel opens on a tap, the chips are
absent and the packs still work.

`pytest` (1244) and `ruff check .` green.


## F50. Making a theme from inside the book

F46 made the art direction a folder and F48 let a reader pick one. The
question that finishes the arc:

> would it be an idea to give the possibility to import themes? [...] for
> each image to be imported you need to tell the user what should this
> image look like. [...] the user would be able to have 2 windows open (one
> with its AI and the one with the creation interface)

That two-window workflow is the feature. Everything else here exists to
serve it.

### Where a made pack lives, and why it matters

**In the data folder: `<stories>/themes/<name>/`.** Not in
`app/static/themes/` beside the shipped ones, and this is the decision the
rest of the design hangs off. Artwork someone generated, chose and uploaded
is *their content*, not part of the program: an app update, a container
rebuild or a re-clone must not delete it, and it has to travel in the
backup zip like every story and photo. A pack is a `theme.json` and a
folder of pictures, so a family who stops using this app still has both.

`themes.py` therefore resolves from two roots, **built-in first**. That
order is load-bearing: every pack falls back to `ranch` for anything it
hasn't drawn, so a made pack called `ranch` would quietly break the
fallback for everyone. A folder with that name is ignored rather than
obeyed.

Two consequences worth stating:

- a made pack's pictures cannot be `/static` files, so they are served by a
  route out of the data folder, validated the way `story_media` is;
- it is **public**, like `/static`, because the login page is dressed by
  the pack too and a login screen with broken pictures would be the first
  thing a family saw. It can only ever reach `<stories>/themes/<pack>/img/`
  and only files the catalogue names.

### The palette is data, never CSS

A made pack has no `theme.css`. A textarea whose contents become a
stylesheet on every page is the one place in this app where someone else's
text would become code, and a same-origin stylesheet is not something a CSP
can save you from. So a pack's colours are validated hex in its
`theme.json`, and `palette.py` renders them into the same blocks
`orbit/theme.css` declares by hand — a `:root` default, the
`prefers-color-scheme` answer, and one `[data-theme=...]` block per scheme
so the nav toggle wins over both.

And the form had to be small enough that someone actually fills it in.
`theme.css` re-declares sixteen variables per scheme; asking for that twice
is asking for no theme at all. So **a scheme is three colours** — a
background, a text colour, an accent — and the rest is derived: dimmed text
is text mixed back toward the background, a border is the background nudged
toward the text, the highlight is the accent at low alpha, the label drawn
*on* the accent is whichever of the reader's own two colours can be read
against it (measured, not assumed). `color-scheme` follows the background's
luminance rather than the scheme's name, because someone's "manuscript" may
be candlelit and the browser draws its own scrollbars from that.

A palette that comes back from a backup, or is edited by hand, can say
anything at all — so a scheme whose colours aren't colours is skipped
rather than raised on. The cost is one scheme that looks like main.css; the
alternative is a stylesheet route that 500s a whole book.

### The catalogue, and why filenames can't be the brief

Thirty-seven pictures, described by the **job each one does** rather than
by what the ranch happens to draw for it. `login-campfire.jpg` is not "a
campfire": it is the welcome on the login page, the thing that says *this
is a private place, come and sit down* — which in a book kept in orbit is a
fire in a viewport and in a woodblock world is a paper lantern. The
filename can never be the brief, because a pack is a skin and not a rename
(CLAUDE.md), so every entry carries `where` (what page you are dressing)
and `subject` (what the picture has to show for that page to make sense).

`prompt_for` glues an entry to the world someone described and adds the
rules this project learned by undoing them by hand across F17, F22, F42 and
F46: no lettering, no corner watermark, no paper border, one subject with
room around it — and for icons, bold enough to read at 20px and **outlined
in a dark colour**, without which nothing survives on both a light and a
dark page (F46's follow-up measured exactly that). They are restated on
every single prompt because a generator forgets between images, not because
the reader needs reminding.

A test asserts the catalogue is *exactly* the default pack's files. A name
in one and not the other is either a picture that can never be replaced or
a prompt for a picture nothing draws.

### Taking the pictures in

Upload processing per kind, all of it Pillow, none of it writing the bytes
it was given:

- **plates** — re-encoded JPEG, capped at the size the app draws them;
- **tiles** — resized to exactly the square they tile at, the one place a
  picture is fitted rather than merely capped;
- **icons and ornaments** — background keyed out by flooding from the four
  corners (so the hole in a ring survives), closed with a Max/Min filter
  pair, trimmed to the drawing, centred and reduced to 160px. An upload
  that is already transparent is taken at its word.

This is `scripts/process_orbit_icons.py` grown up: the same technique the
orbit pack's icons went through by hand, now the thing that makes an
upload usable straight out of a generator.

**The filename allowlist is the catalogue.** The uploaded file's own name
is never used — the *route* names which of the 37 pictures this is, and
anything else is refused. It is the strongest form of this codebase's
"never build a path from user input" rule: the input isn't used to build
the path at all, only to choose from a fixed list.

### Who can do it

`admin_required_in_accounts_mode`, which already existed and is exactly the
rule asked for: the admin when accounts are on, the one password-holder
when they are not. A write-link visitor never gets a session that passes
`login_required`, so a guest cannot reach any of it by construction. The
way in — "Make a theme" at the foot of F49's menu — is shown under the same
condition, so nobody is offered a door that 404s.

### The bug the browser found

The sheet showed each picture with `theme_img()`, which renders whatever
the *reader* is wearing. An admin filling in a new theme while still
wearing orbit was being shown orbit's pictures as though they were their
own. The sheet now resolves each row against the pack being edited, with
the same fallback the book applies, and a test wears one theme while
editing another to keep it that way.

### Tests

- `tests/test_theme_making.py` (34) — the data layer: a made pack in the
  data folder, a shipped name never shadowed, hostile names and hostile
  colours refused before anything is written, three colours becoming a
  whole stylesheet in the shape a shipped pack is written in, a broken
  palette costing a scheme rather than the book, uploads cut out, capped,
  re-encoded and refused when they aren't in the catalogue, deletion that
  leaves a folder someone put something else in, and a made theme
  surviving a round trip through the backup zip.
- `tests/test_theme_making_routes.py` (24) — who can get in (a family
  member gets 404s, not 403s, and isn't shown the door), the whole
  make-and-fill flow, the upload's own filename never being used as a
  path, the media route serving nothing but a pack's own pictures, and a
  made pack dressing the book while still borrowing the rest.

Driven end to end by hand in Chromium at 390px: hold the toggle → Make a
theme → describe a world → three colours a scheme → a sheet of 37 prompts →
upload a plate and an icon → "2 of 37 pictures drawn" → wear it → the
made pack's icon on the editor and its campfire on the login page **while
logged out**, which is the public-route requirement doing its job.

`pytest` (1302) and `ruff check .` green.

### Follow-up: what the first real theme taught

> to be honest I've tried a cyberpunk 2077 theme but it didn't work well.
> [...] the generated pictures were bad

Cyberpunk is the hardest thing anyone could have tried first, and it broke
the prompts in three separate ways — each of which was a hole in the
wording, not in the generator.

**A style named as a place gets you the place.** "A neon-lit night city"
makes a generator draw a night city with the subject somewhere inside it,
thirty-seven times. The old wording's whole defence was one bullet: *one
subject, centred, with room around it*, which is no match for a setting.
Now every plate prompt carries a `Composition:` line of its own that says
what the picture *is*: "one single object, centred, on a plain and almost
empty background... This is an object drawn in that world, not a view of
the world: no street, no landscape, no room, no crowd, no blurred depth
behind it." Stated as its own paragraph rather than a bullet, because
that is the sentence doing the work.

**The app knew the palette and wasn't saying it.** The pack's colours were
already in `theme.json`, and every prompt went out without them — so a
generator picked its own cyan thirty-seven times. Prompts now name the
hexes: the first scheme's three, plus the other schemes' accents, capped at
five. Deliberately **one** background: a prompt naming two names none.

**"No lettering" fights a genre made of neon signs**, and a rule with no
alternative is a rule that gets ignored. It now offers somewhere to go:
"if this style would normally carry signs or writing, suggest them as
abstract glowing marks only — nothing readable."

Two smaller ones from the same session: plates are now told they hang on
*both* the dark and pale page, so their own ground should be a mid tone
rather than pure black or white; and icon prompts forbid glow explicitly,
since a glow is a gradient and a gradient is exactly what stops the corner
flood-fill — it comes back as a halo or a grey box.

The pages gained the two sentences that would have prevented the whole
thing: the description field now says **describe a way of drawing, not a
place** — what it is drawn with, how it is lit, what the lines are like —
and the sheet says **do the first one, look at it, and only then do the
rest**, adding that a scene or a wrong colour means the description is what
to change, not the picture.

### Follow-up: derivations that survive a saturated palette

Measuring cyberpunk palettes through `palette.py` turned up a real defect
next door. Dimmed text is derived by mixing the text colour toward the
background, which is right for the off-white-on-near-black most books use
and wrong for a saturated one: neon magenta on dark purple came out at
**2.5:1**, and the border at 1.2:1 — invisible.

So the mix is now a starting point and the contrast is the constraint.
`_mix_to_floor` walks back toward the text colour until the result clears
4.5:1; `_mix_up_to_floor` pushes an edge further in until it clears 1.5:1.
An ordinary palette lands on exactly the value it did before — a test
pins that — and the neon one now clears both.

What no derivation can rescue is a text colour that is unreadable on its
own background to begin with, since everything else is mixed *from* those
two. That is now measured on save and **reported rather than enforced**:
"the text colour is hard to read on that background (1.7 to 1, where 4.5 is
the usual floor). It is saved either way." It is someone's book; a
deliberate choice is allowed, but it should be a choice and not a surprise.

`pytest` (1315) and `ruff check .` green.


## F51. Setting the book up from inside the book

A product observation rather than a bug report:

> everything can be set up directly from the web interface for the first
> setup [...] we're targeting people that are not experts and that are
> basically interested in something simple to set up. So maybe the README
> is not assessing this.

Checking it first was the right move, because it wasn't true. **None** of
the thirteen `STORYBOOK_*` variables could be changed from the app; there
was no settings page and no first run. What *was* already browser-run was
the content and the people — accounts (the first request auto-approves as
admin), invites, roles, the cast, the tree, groups, themes, backups — which
is a lot, and is where the impression came from.

The gap was specific: six values that describe **the family** were living
in a dotfile. What the book is called. Whose childhood it is. Who writes in
it. Asking a parent to edit `.env` and restart a container to rename their
own book is asking the wrong person.

### The split, and which side each thing is on

- **The machine stays in the environment**: `STORYBOOK_PASSWORD`,
  `SECRET_KEY`, `STORIES_DIR`, `COOKIE_SECURE`, `TRUSTED_PROXIES`,
  `ACCOUNTS`, `OPEN_REQUESTS`. The app needs these before it can serve a
  page, and two of them decide whether it serves one at all.
- **The book moves into `settings.json`**, in the stories folder beside
  `groups.json`: title, birth date, the tree's child, narrators, language,
  theme. In the data folder, so it is inside the backup and readable long
  after this app is gone.

**The environment is the default; the app wins.** A variable is what a
fresh install starts from, and anything set inside the book overrides it
from the very next request — no restart. The person pressing Save is making
the more recent decision, and a setting that silently reverted to a
variable they have never seen would be indefensible. A key present but
*empty* means "no value", not "fall back": someone clearing the title wants
the app's own name back, not the environment's leftover.

Mechanically it is one accessor. `settings.book("BIRTHDATE")` replaced
nineteen `current_app.config[...]` reads across four route files, resolved
once per request into `g` by `before_request`. Anything added later that
reaches for the config directly will silently ignore what the family set,
which is why `CLAUDE.md` now says so.

### The wizard, and the thing it must not do

A fresh book sends whoever can configure it to `/setup` — four questions,
none required, all changeable later, with a "Not now" that counts as an
answer (a wizard you can dismiss but not finish becomes a banner that
follows a family around forever). Answering it writes the settings and,
if the book is *for* someone, creates them as the first person in the cast
with their birthday already on it, and points the family tree at them.

Then the user asked the question that mattered most:

> please make sure that the thing does not require a setup if I already
> have something existing [...] I believe that it would be a bit
> problematic if I'm to reset up

It did not, and my reasoning had not covered it. An install predating this
feature has no `settings.json`, so it was "unconfigured" — a family who had
been writing for a year would have been met by a setup wizard for a book
that plainly already exists. And worse than the insult: the form showed
empty fields, so pressing Save would have written empties over the title
and birth date their environment variables were supplying.

Both fixed, and both pinned by tests:

- **A book with stories in it is already set up**, settings file or not.
  Stories rather than people, deliberately: in accounts mode the first
  account creates a Person before a single story exists, so people would
  make every new book look like an old one.
- **Both forms prefill from what is in force**, environment included, so a
  save can only ever write back what the book was already doing.

`tests/test_setup.py` (17) leads with that case rather than with the happy
path: a book with stories is never redirected, the wizard steps aside on
one, an upgraded book keeps working from its environment with no file
written, Settings prefills from it, and saving that prefilled form keeps
what was there.

The test fixtures gained one line — `stories_dir` now marks itself set up —
because every existing test is about a configured book. Two tests had to
say what they meant instead of what they assumed: one counted directory
entries where it meant story folders, and one built its own app on a bare
tmp_path.

### Follow-up: can anyone trigger it again and lose the book?

Asked after the fact, and worth answering with tests rather than
reassurance, since "a wizard that resets everything" is the shape of a
genuinely bad bug. `tests/test_setup_access.py` (12) is that answer.

The reach of both pages, probed as each role that exists:

| who | `/setup` and `/settings` |
| --- | --- |
| a stranger | 302 to the login page, both verbs |
| a family member (accounts mode) | 404, both verbs — and the nav never offers the link |
| a write-link guest | 302 to login: a delegate session never sets `authed`, so `login_required` turns it away before any role is considered |
| the admin / password-holder | allowed, which is the point |

And the two properties underneath:

- **The wizard cannot be re-armed from inside the app.** A book with
  stories is set up for good, and *no route in this app deletes a story* —
  a test asserts the complete list of deleting routes is F12's voice memo
  and F50's theme, both of which leave the book's stories where they are.
  Archiving every story doesn't do it either; archived stories are still
  files on disk. Losing the settings file doesn't do it: the stories are
  the other flag.
- **Neither page can destroy anything, even for the person allowed to use
  them.** They write one small JSON file, and the wizard adds at most one
  person to the cast. A test takes the story and people sets before and
  after clearing every field and compares them.

One honest residual, and it is operational rather than a hole: if the
stories volume fails to mount, the app sees an empty directory, believes
it is a new book, and offers the wizard. Nothing is lost — the real book is
on the volume that didn't mount — but it is the one way to meet this page
unexpectedly, and the fix is the mount, not the app.

### The README, which is what was actually asked about

It now opens with what there is to do: two values in a file, and everything
else in the browser. The configuration section is two tables — the machine,
and the book, the second one annotated with where each value lives in
Settings — and it says plainly that an existing install is untouched.

`pytest` (1344) and `ruff check .` green. Driven by hand in Chromium at
390px: a fresh install landing on the wizard straight after login, four
answers, the child appearing in the cast with their birth date, the timeline
under its new name, `/setup` then stepping aside to `/settings`, and the
form prefilled with what had just been saved.

---

## F50 follow-up: the pictures a theme could not actually change

> I do not see the different images within the text for all the themes,
> how come?

Three separate faults, found by reading what the browser fetched rather
than what the code intended.

**Two pictures were never reachable by a made pack at all.** main.css draws
the divider between stories and the family tree's brand stamp through CSS
variables — `--flourish-image` and `--brand-mark` — not through an `<img>`,
so `theme_img()` never sees them. A pack with a hand-written `theme.css`
(orbit) redeclares them; a made pack has no such file, and F50 never
emitted them. Uploading `rope-divider.png` did nothing at all, silently.
`render_stylesheet` now declares both when the pack has drawn them.

**And then they still didn't appear**, which is the interesting part. A
relative `url()` inside a custom property is resolved against the
stylesheet that *uses* the property, not the one that declares it — so
`url("img/rope-divider.png")`, declared in `/themes/<name>/theme.css` and
used in `/static/css/main.css`, was fetched from
`/static/css/img/rope-divider.png`. A 404 in the network log, the default
pack's ornament still on screen, and nothing anywhere to explain it. The
generated URLs are absolute now, and a test asserts they always will be,
with the reason attached — it looks like a pointless detail otherwise.

**Two catalogue entries asked for pictures nothing draws.** The family tree
tiles its background, so `tree-map.jpg` and `tree-map-dark.jpg` — the
un-tiled pair the tiling replaced — are referenced by no template, no
stylesheet and no script. The sheet was asking someone to generate two
pictures that would never be shown; it now asks for 35. They stay on disk
(deleting committed artwork is a separate decision) behind a named
constant, and a new test walks every catalogue entry and fails on any
filename that appears in no template, stylesheet or script.

A fourth thing turned up while checking: `brand-star.png` was described as
"the mark beside the book's name". It isn't — it is stamped on the anchor
person's card in the family tree, at 28 pixels. Someone would have drawn
the wrong picture, and drawn it too detailed.

Also removed: F50 mapped `--surface-texture` to the tree-map tile, which
would have tiled the family tree's chart across every page of the book.
A made pack has no page texture, which is the honest answer — the ranch's
is an SVG filter and orbit's is a starfield in its own stylesheet, and
neither is a catalogue asset.

`pytest` (1348) and `ruff check .` green. Verified in Chromium by watching
the network: before, `404 /static/css/img/rope-divider.png`; after,
`200 /themes/ornaments/img/rope-divider.png`, with the used value on the
element pointing at the pack's own file.

Two of my own checks were wrong on the way here and are worth recording:
the first probe fetched the URL relative to the *page* rather than letting
CSS resolve it, and the second ran in a fresh browser context with no theme
cookie, so it was measuring the default pack both times and would have
reported success.

## F52. Seeing the colours before saving them

> please create a preview for the text so the user can relate

The theme editor asked for a name, a description and **eighteen hex
fields**, and gave back nothing until you saved. The colour swatch beside
each field showed one colour on its own, which is the one thing that never
tells you anything: a palette is a set of relationships — text on
background, accent on background, the dimmed label the app derives for
you — and none of them are visible one square at a time. So the only way
to find out what nine hexes added up to was to save, switch the book to
that theme, and go and look at a story.

Now a miniature of the book sits above the colour fields and repaints as
they are typed: the nav with its brand and its outlined **+ New story**
button, an "on this day" card, a year marker, a timeline row with its
milestone pill, and the empty mount an illustration is pinned to. Under it,
the three ratios the palette is actually held to.

**The preview computes nothing of its own.** This is the whole design
constraint, and it is why the feature is more than a decorative box.
`app/palette.py` derives eleven variables from three seed colours, and
several of them are not obvious from the seeds — dimmed text is text mixed
back toward the background *and then backed off in 4% steps until it clears
4.5:1*, a border is the background nudged toward the text until it is
visible as an edge, the accent's label is whichever of your own two colours
can be read on it. A preview that eyeballed those would be worse than no
preview: it would tell someone their quiet text was fine when the server
was about to decide otherwise. So `app/static/js/palette-logic.js` is a
port of `palette.py`, operation for operation, and
`tests/test_palette_preview.py` runs 255 seeds through both and fails on
the first hex that differs.

Two things that port badly and would never show up in a spot check:

- **Python's `round()` is half-to-even; JavaScript's `Math.round` is
  half-up.** They disagree on exactly the values a mix produces
  (126.5 → 126 in Python, 127 in the browser). `pyRound` does it Python's
  way.
- **Both back-off loops are iterative**, and their result depends on
  accumulating `amount -= 0.04` in the same order. A closed-form
  "improvement" on either side would drift, and the cross-check is what
  would catch it.

Three smaller decisions:

- **It is sticky at the top of the form.** Eighteen fields is a long scroll
  on a phone; a preview you have to scroll back to is a preview nobody
  uses. Changing the accent and seeing the year marker move is the point.
- **Everything inside the pane is written `var(--color-accent)`**, exactly
  as main.css writes it, and the JS sets the derived variables on the pane.
  There is no second set of colours to keep in step, and a test fails on
  any literal hex appearing in the preview markup.
- **It is not offered with JavaScript off.** The element ships `hidden` and
  the script reveals it. Without the script the miniature would be painted
  by main.css's own palette — a picture of the *current* theme captioned as
  the one being typed, which is the single most misleading thing this page
  could show.

The live warning under the miniature is the same measurement
`theme_packs.palette_warnings` makes on save, so the page cannot cry wolf
about a palette the server would accept, or stay quiet about one it will
complain about; a test holds the two to the same verdicts.

`pytest` (1360) and `ruff check .` green — 19 new Node checks, a 255-seed
cross-language comparison, six route tests. Verified in Chromium at 390px
and 1280px: typing the dark seed `#0f0d14 / #ece0c8 / #c9a227` produced
`--color-bg-raised: #1e1c21`, `--color-text-dim: #8f877c`,
`--color-border: #373334`, `--illo-mount: #18151b` in the live DOM — the
same values `palette.py` returns for those seeds — and the three scheme
tabs flipped `color-scheme` along with the palette. A palette whose text
cannot be read renders visibly unreadable *and* says so.

Also corrected while here: the interface still said a theme was
thirty-seven pictures. It has been thirty-five since the two un-tiled maps
left the catalogue (F50 follow-up), in the editor's own hint, the French
translation of it, README, and four comments and docstrings.

## F46 follow-up: orbit's icons, drawn rather than generated

> I thought you had a command to generate images within Claude code

There is no image generator here — but eleven of orbit's thirteen icons
were still borrowed from the ranch, so a book kept in orbit had a lasso and
a branding iron on its buttons. Those eleven are the part of a pack that
least needs a generator, and it took saying "I can't generate these" out
loud to notice why.

An icon in this project is four flat colours, a dark keyline and one
silhouette that has to survive being drawn at twenty pixels. That is
geometry, not illustration — and it is precisely what a generator is worst
at: it softens small shapes, forgets the outline between one image and the
next, and will not hold thirteen drawings to one style. So
`scripts/draw_orbit_icons.py` draws them, in Pillow, from the subject table
in IMAGE-PROMPTS-ORBIT.md. Pillow is already a pinned dependency, so the
set is reproducible from `requirements.txt` alone: change a colour in the
script and all thirteen redraw. The generated plates have never been
reproducible in that sense, and never can be.

The two icons that *did* come from the generator were redrawn with the
rest, which IMAGE-PROMPTS-ORBIT.md had already said should happen once the
others arrived — they predated the outline rule, and a half-outlined set
looks like a mistake.

**What drawing them taught, beyond what generating them had.** The pack's
existing rule is that every shape carries a dark navy outline, because
nothing in the palette reads on both the night side and the day side —
starlight is 14.5:1 on one and 1.11:1 on the other. Drawing added a
corollary a generator would never have surfaced: **a line cannot simply
*be* the keyline.** A navy stroke disappears at night exactly as a navy
fill does, so every stroke here is drawn twice, a fat navy keyline under a
lighter core. Filled shapes need one pass; strokes need two.

Two more, both about composition, and both cost several attempts each:

- **Three heads inside an oval is a face.** In a triangle it is
  unmistakably one; in a row it becomes a pod. `icon-group` only worked
  inverted — the enclosing shape filled dark, three light silhouettes
  inside it, no per-figure outline at all. Which is what the catalogue asks
  for in words; the drawing had to catch up with the sentence.
- **A dark oval centred in a pale disc is an eye.** `icon-new-person`'s
  visor read as one until it became a band across the helmet.
- And one that is just a fact about Pillow: an arc's rounded end caps read
  as *bolts* when the arc is long enough to be a rim, so `arc()` takes
  `caps=False` for the hatch and the dashed orbit.

Five passes, and the honest record is that the first one produced six
usable icons out of thirteen. What was wrong was never the colour or the
keyline — it was that a shape which reads at 160 pixels can mean something
else entirely at 20.

`pytest` (1360) and `ruff check .` green. Verified in Chromium against a
running book with `STORYBOOK_THEME=orbit`: the editor requests
`/static/themes/orbit/img/icon-{new-story,instant,seal,draft,archive,source,record,save}.png`
with no 404 and no ranch fallback, and every one reads on both
`data-theme="dark"` and `data-theme="light"` — which is the test the
keyline exists to pass.

## F51 follow-up: the three ways a configured install lost its settings

A code review of F51 found five defects. Three of them broke the same
person — someone whose book is configured by environment variable, which
is every install that predates the settings page and every install started
from `.env.example`. That is the audience F51 and the README were written
for, so these are fixed first.

Each was reproduced against a running app before being touched, and each
fix has a test that fails without it.

**The wizard erased what it never asked about.** `_form_values()` returned
all six settings on every submit, and `setup.html` renders neither a theme
nor a tree-child. To `effective()` a key that is *present but empty* means
"no value" — that is how clearing the title gets the app's own name back —
so a book started with `STORYBOOK_THEME=orbit` and `STORYBOOK_CHILD=milo`
wrote `{"theme": "", "child": ""}` and served the ranch from the moment
anyone pressed "Start writing". F51's own entry claims a save can only
write back what the book was already doing; it could not. `_form_values()`
now returns only the keys whose field the form actually rendered, which is
the general rule rather than a patch for these two — and `save()` merges,
so an omitted key leaves whatever was there alone.

**The Language field did nothing.** `resolve_language` computed `g.lang`
from `settings.book("DEFAULT_LANGUAGE")` one line *before* `g.book` was
assigned. `book()` falls back to the raw config while `g.book` is unset —
correct outside a request, silently wrong inside one — so the language came
from the environment while the title and theme from the same file worked,
which is exactly why nobody noticed. The two lines are swapped, with the
reason written above them.

**A hand-edited narrator list took the whole book down.** `read()` promises
that a settings file edited into nonsense costs the settings and not the
book, and the birthdate branch keeps that promise. `authors` only checked
that the value was a list, and every page indexes an entry as `a["name"]`
— so `{"authors": ["Papa", "Maman"]}`, which is precisely what a person
would write by hand, was a 500 on every page. Entries are now validated by
shape and *filtered* rather than the list rejected: one bad line should not
cost the other three narrators their colours.

Five new tests, and the guard that matters more than the fixes:
`test_the_settings_form_offers_every_key_it_writes` walks `settings.KEYS`
against the rendered form, and
`test_every_family_setting_is_read_through_the_request_context` sets each
key to something the environment disagrees with and asserts the file wins.
Those are the general versions — the next field added to one form and not
the other fails here, rather than in somebody's book six months later.

Each new test was run against the unfixed code to confirm it fails there;
a guard that passes on the bug it describes is not a guard.

`pytest` (1371) and `ruff check .` green.

Still outstanding from the same review, and next: the MCP server reads
authors, title and birthdate from the environment only, so a family who
sets narrators in the app leaves its author allowlist empty; and
`settings.html` promises the settings travel with a backup, which the
export honours and `import_backup` silently drops.

## F51 follow-up 2: the two places a setting stopped at the web app

The other half of the same review. Both are the same shape as the three
before them — a value a family can now change in the app, and something
else that still read it from the environment — but neither breaks a page,
so neither was going to be noticed by looking.

**A backup did not bring the settings back.** `settings.html` says the
settings travel with the backup; the export does put `settings.json` in
the zip, and `import_backup` skipped it. Every root-level file was skipped,
for a good reason that did not apply here: `pending_accounts.json` and
`groups.json` are live operational state, and silently overwriting *those*
from an old zip would be worse than leaving them alone. The book's own
settings are not operational state — they are the book's name, whose
childhood it is, who writes in it — and a restore onto a new server is
exactly when you want them.

So they come back the way a person or a made theme comes back: **only into
a book that has none of its own.** An install that has already been
configured keeps what it is doing, and an old zip can never roll a live
title back. They are read through `settings.KEYS` rather than extracted
verbatim, for the same reason a restored theme folder is filtered to the
catalogue's filenames — a zip is a portable file, and may only put back
shapes this app writes. A `settings.json` that is unreadable costs the
restored settings and not the restore: losing a title on the way back from
a dead server is a nuisance, losing the stories is the thing this app
exists to prevent.

**The MCP server never learned about the settings page.** It read authors,
title and birthdate from `STORYBOOK_*` only, so a family who set their
narrators in the app left its allowlist empty — and `create_story` reads
`if configured and author not in configured`, which does not reject
everything when the set is empty, it validates *nothing*. An assistant
could write a story under any name at all. `book_overview` reported the
default title and no birthdate at the same time, so ages were missing from
everything it said about the book.

It now resolves the same way the web app does: `settings.effective` over an
environment-shaped config, read per call rather than cached at import. Per
call matters — the process outlives any single change, and a parent adding
a narrator in the app has to be able to name them in the very next tool
call, exactly as a browser picks the change up on the next request. It also
inherits the shape-filtering from the previous follow-up for free, so a
hand-edited narrator list cannot reach an assistant either.

Nine tests. Seven of them fail against the unfixed code — checked, not
assumed. The other two (a restore not overwriting a configured book, and an
unreadable `settings.json` not costing the restore) pin new behaviour
rather than catching the old bug, since nothing was being restored at all
before.

`pytest` (1380) and `ruff check .` green.

That closes every finding from the review of F51 and F52.

## F46 follow-up 2: the keyline that was on the wrong side of the line

A second review of the drawn orbit icons found three faults in artwork I
had reported as verified on both schemes. All three were invisible in the
things I checked with, which is the part worth recording.

**The light core was outside the keyline, not inside it.** Pillow draws an
arc's and an ellipse's stroke *inward* from its bounding box rather than
centred on it, so `arc()` and `ring()` — which drew a fat navy band and
then a narrower light one from the same box — put the light band outermost
and the navy within. That is the exact inverse of the rule the whole pack
is built on: on the pale page the shape loses its outer edge entirely.
`stroke()` never had it, because `line()` *is* centred on its path, which
is why the icons built from strokes looked right and the ones built from
arcs looked slightly soft.

Measured through one dash of `icon-draft`, before: navy r=35–56, starlight
r=59–68 — light on the outside. After: navy 35–47, starlight 50–68, navy
71. Enclosed.

**Three shapes were drawn past the edge of the grid** — the review found
two, and measuring found a third. A shape drawn off-grid is cut flat and
the cut carries no keyline, and it does not look wrong either: `render`
trims to content and *then* pads, so the flat edge lands inside the padded
frame rather than on the image border, where somebody would notice.
`icon-new-person`'s plus reached x=65.7 on a 64-wide grid.

**`icon_draft`'s docstring described the opposite of what it drew.** The
module header says those docstrings are the catalogue's subject line so a
drawing that has drifted is visible right there — a mechanism that only
works if the line is kept in step when the drawing changes, and it was not.
The drawing won on merit here (a dashed *orbit* survives 20px where a
dashed body closes up into a solid rim), so the line was corrected to match
the drawing rather than the reverse, with the reason attached.

**The tests are the point of this entry.** `tests/test_orbit_icons.py`
measures the three properties instead of admiring them: bands along a ray
must run navy, core, navy; nothing may be drawn past the grid; and every
icon must still have ink on it at the twenty pixels the app draws it, on
every scheme the pack offers. The floor is 8% of a 20×20 square clearing
3:1 against the button's own background — picked from measurement, not
taste. All fifty-six were run against the unfixed code first; the three
that describe the bugs fail there.

A finding that came out of writing that floor, and is *not* fixed here.
Measured each pack against its own `--color-bg-raised` rather than another
pack's — the mistake I made on the first attempt, which flattered orbit and
libelled the ranch — several of the **default** pack's icons fall well
below the same floor:

| ranch icon | dark | light | manuscript |
|---|---|---|---|
| `icon-new-person` | **0.0%** | 28.0% | 27.8% |
| `icon-tree` | 7.5% | 5.5% | **2.8%** |
| `icon-source` | 21.0% | 7.8% | **4.5%** |
| `icon-print` | 17.0% | 12.8% | **7.2%** |

Orbit's weakest is 9.5%. These are thin-line drawings that dissolve at
button size — the catalogue's own "no stroke thinner than a tenth of the
icon's width" is the rule they miss.

**Raised, decided, and deliberately left alone.** The numbers were put to
the book's owner and the answer was that the ranch's icons are fine as
they are. That is a taste call and it is theirs: the ranch is the app's
own hand, the drawings have character a measurement cannot see, and the
alternative — thickening four of them, or giving the ranch a drawing
script the way orbit now has one — would trade that character for a
number. Recorded here so it reads as a decision that was made rather than
a defect nobody noticed, and so the next person to run the same
measurement does not re-open it.

The floor in `tests/test_orbit_icons.py` therefore applies to the icons
that script draws, and to nothing else. It is not a rule the ranch is
held to, and it should not become one without the same conversation.

`pytest` (1436) and `ruff check .` green.

## F51 follow-up 3: the wizard cannot dismiss a book

> please make sure that the wizard cannot dismiss an entire portfolio

Asked after the wizard had already been caught erasing two settings it
never showed. Audited rather than reasoned about, and the answer was: it
cannot delete anything, but it could still take a book's *identity* away.

**What it can and cannot do.** Every path through `/setup` writes exactly
one file — `settings.json` — and may create one Person. No path deletes a
story, a person, a theme, a group or an account. That is now a test rather
than a claim.

**What it could still do.** `is_configured` recognised an existing book by
its *stories*, so a family who spent an evening adding the cast, making a
theme and deciding who may read what — before writing the first entry —
still met the wizard. Measured on exactly that book: one submit with the
fields cleared took away the title, the birth date, the narrators and the
language. The content survived; the book's identity did not.

Two independent guards, because the interesting failure is the one neither
can see:

**A book is more than its stories.** `is_configured` now also counts made
themes and audience groups. Neither exists unless somebody deliberately
made it. People are still *not* counted, and that exclusion is now pinned
by a test of its own: in accounts mode the first account creates a Person
before a single story is written, so counting them would meet every
genuinely new book with a redirect away from its own setup wizard.

**A blank field on the wizard means "skip this", not "erase that".**
`/settings` keeps the power to clear — it is a page someone returns to,
and clearing a box is how a title comes back off a book. The wizard does
not. It is a one-time flow a family may meet on a book that already has a
name, and there an empty box is far more likely to mean "I did not fill
this in".

The second guard is what makes the first one's accuracy stop mattering,
which is the point of having both: **a stories volume that failed to mount
looks exactly like a new book, and always will.** Nothing in the app can
tell that case from a genuine first run. What it can do is make finishing
the wizard on top of it cost nothing — and now it does, because there is
no value present to be cleared and the file it writes falls straight
through to the environment.

Ten tests, all six of the ones describing the two defects run against the
unfixed code to confirm they fail there. `pytest` (1446) and
`ruff check .` green.

## Housekeeping: one blueprint file, and one way to write a JSON file

Two structural changes with no user-visible behaviour, taken from a read
of the codebase looking for where its own conventions had come apart.
Neither adds a feature; both remove a way to get one wrong later.

### `views.py`: the blueprint and the shared helpers leave `routes_pages.py`

`routes_pages.py` had grown three jobs. It defined the `pages` blueprint,
it held the view helpers its five sibling route files import, and it
implemented the timeline/story/book/export pages. The third job is what
made the first two awkward: every sibling had to import the module that
imported *them*, so the routes were registered by a side-effect import at
the bottom of `routes_pages.py`, and `routes_api.py` had to fetch
`viewer_scope` from inside a function body to stay clear of the cycle.

The tell was in the names. Five modules were importing `_visible_stories`,
`_people_dir`, `_serve_media`, `_person_ref` and `_other_people_refs`
across a module boundary — an underscore claiming "private" about names
that plainly were not.

So the blueprint and those helpers moved to `app/views.py`, and lost the
underscores on the way. Nothing imports `routes_pages` now except
`create_app`, which imports all six page-route files purely so their
routes register. `views.py` imports no route file, so there is nothing to
cycle. `_people_dir` became `current_people_dir` rather than `people_dir`,
because half the functions around it already have a local of that name and
one takes it as a parameter; `_author_color` became `color_for_author` for
the same reason.

While there, `routes_api.py`'s own copy of `_people_dir` went — it was the
second of three identical one-liners.

**What did not move, deliberately: `/export`'s scoping rules.**
`_exportable_story_ids` and `_viewer_may_export_credentials` are the
export route's own, nothing else calls them, and they are the three-way
distinction the whole audience feature rests on — a guest gets no export
at all, a family member gets the stories they can see and no credential
files, an admin gets everything. Moving them would have been tidiness at
the expense of keeping an access-control rule next to the route it
governs.

Verified rather than assumed, because a refactor that touches the audience
gate has to be:

* the route table is **byte-identical** before and after — 74 rules, same
  endpoints, same methods, diffed;
* `/export` probed on a running app as an admin, as a family member inside
  the group, as one outside it, as a write-link guest holding a real
  session, and as the single password-holder with accounts off. Same
  answers as before: `scoped=True/credentials=3`, `scoped=True/0`,
  `scoped=False/0`, `302 → /login`, `scoped=True/4`;
* the guest tier had no test at all, and now has one — a write-link holder
  can reach `/w/write` and cannot reach `/export` or the timeline;
* a browser pass over all fifteen pages plus a story, its editor and its
  history: 200 everywhere, no console errors.

Two ratchets came out of it. `test_groups.py`'s unscoped-access count now
includes `views.py` — the gate moved into a file that list did not know
about, and the count would have gone green with the gate unwatched — plus
a new `test_every_route_file_is_counted`, so the *next* file cannot slip
past the same way. And `tests/test_view_helpers.py` pins the shape: nobody
imports `routes_pages`, `views.py` imports no route file, one blueprint
named `pages`, `create_app` imports all six, and twenty named endpoints
still answer. Both were confirmed to fail when violated.

### `jsonstore.write_json`: the same three lines, seven times, four of them wrong

Write to a `.tmp` beside the target, then `os.replace`. Copied into
`accounts.py` (twice), `groups.py`, `invites.py`, `write_links.py`,
`settings.py` and `theme_packs.py` — and four of the copies wrote
`json.dumps(data, indent=2)` with no `ensure_ascii=False`.

Two of those four carry text somebody typed. An account request's display
name and note went to disk as `Am\u00e9lie No\u00eblle`, while the same
name in a group, written by one of the copies that got it right, stayed
`Amélie Noëlle`. Nothing was broken by it — Python reads both back
identically — but *plain text, readable long after this app is gone* is
the promise the whole storage design exists to keep, and escape sequences
are not what a family should find when they open their own files.

`app/jsonstore.py` is a leaf: it imports nothing from the rest of the app,
which is what lets `settings.py` use it while keeping the independence it
is careful about elsewhere. `account.json` and `invites.json` have no
field a name reaches today; they moved over anyway, because the next field
added to either is the one that would have found out. `account.json`'s
contents are pinned by a test either way — `auth.login_required` reads the
role out of it on every request, and every access rule in the app hangs
off that.

`test_no_module_hand_rolls_its_own_json_write` is the ratchet: a
`json.dumps` written to a file anywhere in `app/` other than `jsonstore.py`
fails the suite. Confirmed by adding one.

Twenty-five tests added. The five content tests were run with
`ensure_ascii` restored to confirm they fail there. `pytest` (1471) and
`ruff check .` green.

## Housekeeping 2: the backup's two halves move in together

`/export` wrote a zip in thirty lines inside a route. `import_backup` read
one back in a hundred and fifty inside `storage.py`. They are two ends of
a single contract — which files go out has to match which files may come
back — and they were in different layers, unable to see each other.

Three things had already gone wrong because of it.

`storage.py` had to reach *up*. Restoring a backup means knowing about
settings (F51), made theme packs (F50) and the catalogue that says which
picture filenames are legitimate — so the data layer every other module
leans on imported `settings`, `themes` and `theme_catalog` from inside a
function body, with a comment explaining that keeping the imports local
kept the dependency arrow presentable. It was a workaround for the
function being in the wrong file.

**The test suite had written its own export. Twice.** `tests/test_import.py`
and `tests/test_backup_credentials.py` each carried a byte-identical
`_export_zip`/`_backup_of` helper that walked the directory and zipped
everything it found. Neither skipped `.tmp` leftovers. Neither applied the
credential filter. So every import test in the app was restoring a zip the
app would never have produced, and the one property most worth checking —
that what export writes, import reads — had no test at all, because
nothing could call both.

And there was nowhere for a round-trip test to live.

`app/backup.py` now holds `write_backup`, `import_backup`,
`CREDENTIAL_FILENAMES` and `ImportCollision`. `storage.py` loses 183 lines
and all three upward imports. The `/export` route is down to the two calls
that decide what the viewer may have, and one call that builds it.

**What deliberately did not move: who may export what.** `write_backup`
takes `allowed_ids` and `with_credentials` and does not decide either.
`_exportable_story_ids` and `_viewer_may_export_credentials` read the
session and stay beside the route they govern — this module is the
mechanism, the route is the policy, and an access-control rule is easier
to audit next to the thing it guards than one import away.

Both test helpers are now one line calling the real export, and
`tests/test_backup_roundtrip.py` checks the thing that matters to a
family: **the backup you took is the book you get back**, and for a viewer
who cannot see everything, exactly the part they could see and no more.
Twelve tests, including the three tiers restoring into a fresh book, and
the rule that has to hold on all of them at once — an admin's zip
legitimately *contains* credential files, and a restore still must not put
them back, or a zip becomes a way to install your admins into somebody
else's book.

Verified by breaking each property in turn and watching the right test
fail: export stops skipping `.tmp` → one failure; import stops dropping
credential files → the admin tier fails; export stops scoping to the
viewer → three fail. And the export tiers were re-probed on a running app
either side of the move, unchanged: admin `scoped/3 credentials`, member
in the group `scoped/0`, member outside it `public only/0`, write-link
guest `302 → /login`, single password-holder `everything/4`.

`pytest` (1483) and `ruff check .` green.

## Housekeeping 3: storage.py stops being five modules

906 lines, the highest fan-in in the app — fifteen modules import it — and
the only large file in the repo with no section banners. It held five
jobs: validating the strings that become paths, reading a folder into a
`Story`, writing one back, `.versions/`, and media. Plus two that were not
filesystem read/write for stories at all.

`backup.py` took the first (above). This takes the second. CLAUDE.md's own
entry for the module had been hedging about it for a while — *"Also home
to several small pure date-math helpers used by the timeline"* — and a
hedge in a one-line description is usually a file boundary asking to be
drawn.

`app/timeline.py` now holds `readable_stories`, `on_this_day` (F5),
`stories_with_milestones` (F28), `growth_photos` (F29),
`months_since_last_story` (F30) and `is_sealed`. Pure functions over a
list of stories and a date: no filesystem, no Flask, nothing to set up to
test. `storage.py` goes 906 → 650 and gains the five banners.

One thing worth saying plainly in the new module's docstring, because the
name invites the wrong assumption: **`readable_stories` is not an
access-control gate.** It decides which pages of the book you are *shown* —
published, unsealed, unarchived. Audience scoping is `groups.can_see`,
reached through `views.visible_stories`, and everything here is always
handed a list that has already been through it.

### The Feb 29 rule, which was written three times

Extracting the functions made the duplication visible. A leap-day
anniversary has to come round on Mar 1 in a non-leap year, and that rule
existed in three places:

* `on_this_day`'s `feb29_makeup`, for stories;
* `life_events._matches_today`, for birthdays and wedding anniversaries —
  whose docstring said, in as many words, "the same Feb 29 → Mar 1
  non-leap-year makeup rule as storage.on_this_day";
* the `except ValueError` branch inside `growth_photos`, arriving at the
  same answer from the other direction — there is no Feb 29 to land on, so
  it is Mar 1.

The first two were the same boolean expression, byte for byte. They are
now one `dates.same_day_of_year`, and the test that matters is the one
that could not have been written before: **a leap-day story and a leap-day
birthday surface on the same day**, and neither surfaces on Feb 28. While
each module carried its own copy, one drifting and not the other was a
silent, once-every-four-years bug — the kind nobody would ever catch by
reading.

The pure-list tests moved out of `test_storage.py` into
`tests/test_timeline.py` with the code, since they build `Story` objects in
memory and never touch a directory — which is what said the functions were
not really storage. `test_visibility.py` (F0) and `test_on_this_day.py`
(F5) also test this module and stayed where they are: this suite is one
file per feature area, not one per module, and both are named for their
feature.

`pytest` (1489) and `ruff check .` green.

## Housekeeping 4: two pure modules out of editor.js, and a bug in the second

`editor.js` is 1,650 lines and the only large piece of front-end code that
had never been through this codebase's own extraction pattern — ten UMD
modules with plain-Node tests, and none of them from the biggest file.
Two of its eleven sections are pure arithmetic hiding behind a browser.

This is not a line-count exercise. `editor.js` is barely shorter
afterwards, because the code was replaced by calls rather than deleted.
What changed is that two things that could quietly be wrong now cannot.

### `crop-logic.js`: the preview and the saved photo were computed twice

The pan/zoom cropper worked out where the photo sits in two places:
`updateCropTransform`, in CSS pixels against the on-screen stage, and
`rasterizeCrop`, in canvas pixels against a 900px square. The same
arithmetic, written out separately — and the failure mode if they ever
drifted is the worst kind this app has. **The photo a parent framed would
not be the photo their book keeps, and nothing on screen would say so.**

`placement(state, k)` is that arithmetic now. `k` is 1 for the preview and
`900 / stageSize` for the canvas, and it is the entire difference between
the two callers. Nineteen checks, including the one the two copies were
always supposed to satisfy and nothing tested: for five different photo
shapes, zooms and pans, the canvas placement equals the preview placement
times `k`. Introducing a one-pixel drift at output scale fails it.

Two smaller things the extraction turned up and fixed: a pinch whose two
pointers arrive at the same coordinates used to divide by zero and set the
zoom to `NaN`, which the slider cannot come back from; and clamping a
negative drag against a limit of zero yields `-0` in JavaScript, which
survives JSON and comparisons.

Verified in a real browser as well as in Node — a 1200×800 photo on a
256px stage, zoomed to 50 and dragged 60px left, produced exactly the
placement `CropLogic` predicts, and the saved 900×900 JPEG contained
exactly the predicted region of the source image (green band left, yellow
right, the marker ellipse where the maths said it would be).

### `draft-logic.js`: crash recovery was throwing drafts away

This one is a defect, not a refactor.

`applyDraft` restores fourteen fields — the date, the sealed-until date,
the draft and archived toggles, the people, the tags, the sources, the
audience, the family pickers, the sepia dial. The question *"is there
anything to restore?"* compared **two**: the title and the markdown.

So a parent who opened the editor, set the date, chose who the story was
for, tagged it, and then lost the tab got no banner and no draft. The
autosave had run and written all of it. The recovery read it back,
decided nothing had changed, and called `clearAutosave()`.

Reproduced in a browser before fixing it, and again after putting the old
comparison back: with two fields, a date-only edit and a tags-only edit
both come back `banner=false`; with the whole payload compared, both are
`banner=true`, and a genuinely unchanged page still shows nothing.

The comparison is now over every field either side mentions, which also
means a field added to the payload later is picked up with no change here.
Fifteen checks, including the nine "only this changed" cases that used to
be discarded, and the ones that guard the other direction: `false` and `0`
and `""` are values rather than absences, key order in an object is not a
change, the order of `people` and `sources` is, and anything else that
turns up in that localStorage key is not a draft at all.

`pytest` (1491) and `ruff check .` green.

## Housekeeping 5: the index earns its trust

The plan for this one was to sort FEATURES.md into F-number order. Reading
the file properly showed that was the wrong idea, so it did not happen.

Its feature specs use `##` for their own internal structure. F18 alone has
`## Layer 1`, `## API`, `## Person pages`, `## Tests` and `## Definition of
done`; F19 and the original PLAN-era sections do the same. Five features
are `#` rather than `##`. A mechanical sort of the top-level headings would
tear those specs apart and interleave their subsections with unrelated
features — a worse file, arrived at confidently.

The index is what makes the order not matter, and the index turned out to
be in better shape than the diagnosis assumed: all fifty-three features
were already listed, none stale, none duplicated. What it lacked was any
reason to believe that would stay true.

`tests/test_features_index.py` supplies it. Six checks: every feature
heading has an index line, every index line has a heading, no duplicates,
no two features claiming the same number, the newest feature is listed, and
the one instruction that makes an unordered file navigable — search the
heading text — survives edits to the preamble. Confirmed to fail both ways
by appending a feature with no index line and by adding a second `## F50`.

It is the same shape of guard as the i18n test, which fails when a
`_("...")` lands with no French line. A convention nobody can forget beats
a convention everybody is asked to remember.

The index's own preamble now says all of this, including why the file will
not be sorted, so the next person to have this idea can save the afternoon.

Also: `scripts/process_orbit_icons.py` is marked superseded at the top. Its
generate-and-key pipeline was replaced by `draw_orbit_icons.py`, and
anything it produced today would fail `tests/test_orbit_icons.py`. It stays
because its four keying passes are the record of what went wrong with
generated icons, and the framing rules in it are the ones the drawing
script matches.

`pytest` (1497) and `ruff check .` green.

## Housekeeping 6: the vendored libraries ship their licences

Found while working out whether three unmerged branches were worth
keeping. One of them — a session from July that never landed — carried an
in-app credits page under feature numbers that other work has since taken,
so it cannot merge as it stands. But it was right about one thing, and that
thing is still true on `main`.

**`app/static/vendor/toastui/` had no `LICENSE` file.** `d3/` and
`familychart/` both had one; `familychart/` had a `VENDORED.md` too. Toast
UI had neither — no licence text, no provenance note — despite CLAUDE.md's
vendoring rule being written *about* that very bundle.

Nothing looked wrong from inside the code, because the bundle's own banner
already named the licence. What was missing was the text MIT asks to be
distributed with copies. This app exists to be self-hosted and handed
around; that is exactly the situation the obligation is about.

So: the MIT text (verified against upstream — `Copyright (c) 2020 NHN Cloud
Corp.`), and a `VENDORED.md` recording the version, the esbuild rebuild
command, the `usageStatistics: false` rule, and where its class names may
be styled.

### The test found a second one on its first run

`tests/test_vendored_licences.py` checks three things per vendored library:
a `LICENSE` with an actual grant and a copyright holder in it, provenance
written down somewhere (`d3/` has no `VENDORED.md` of its own and does not
need one — it is family-chart's peer and is documented in that folder's
file), and **a licence notice in every `.js`/`.css` file a browser
downloads**.

That third check is the one that matters, and it failed immediately on
`familychart/family-chart.css`. Upstream ships that file without a banner,
so the only copy of it this app serves was going out with no copyright line
on it — the same defect as Toast UI's, in a library that already had its
`LICENSE`. Toast UI's dark theme stylesheet was the same story.

Both now carry a banner added locally, and each folder's `VENDORED.md`
names that as its only local edit, so a future re-vendoring knows to put it
back. The vendored CSS is otherwise untouched: the diffs are pure
additions, and both stylesheets parse to exactly the rule count they did
before (99 and 145), checked in a browser rather than assumed.

The guard was confirmed to fail three ways: a library folder with no
`LICENSE`, a loose file dropped at the top of `vendor/` where no library
owns it, and the banner taken off again.

`pytest` (1508) and `ruff check .` green.

## F53. The licences, where a reader can actually see them

Housekeeping 6 put the licence *files* in the repository, which is what
discharges the obligation. This is the other half: a page inside the book
that shows them to whoever ends up running it.

Reached from Help, at `/licences`, behind `login_required` like every other
page. Being on the open internet was never the point — the notices have to
travel with the copy and be readable by whoever receives it, and a family's
book is not a public website.

Three sections, and the distinction between the first two is the whole
reason the page is worth building rather than pasting a list into a README:

**Sent to your browser.** The three vendored bundles — Toast UI Editor,
family-chart, D3 — are part of the page a reader is looking at. Serving
them is redistribution, so their licences appear **in full**. The route
reads each `LICENSE` off disk at request time and renders that file. A copy
pasted into the template would look identical today and drift silently the
first time a bundle is upgraded; this cannot.

**Running on the server.** Flask, Pillow, pillow-heif and the rest never
leave the machine, so no notice obligation attaches. They are listed
anyway, because knowing what you depend on is part of depending on it —
including that pillow-heif's bundled codecs are LGPLv3/GPLv2, which is the
one entry on the page anyone redistributing a built image needs to think
about.

**Fonts and pictures.** No webfonts are downloaded — the text is set in
whatever the reader's own device already had. The artwork was made for this
project: the ranch pack generated and then processed by hand, the orbit
pack drawn in code. No stock imagery, no icon set, and a theme a family
makes stays on their own machine.

### Keeping it from going stale

A credits page is the kind of thing that is accurate the day it ships and
quietly wrong a year later, so the lists are checked against the real
files rather than trusted:

* every directory under `app/static/vendor/` must appear on the page —
  adding a bundle and forgetting the page fails the suite;
* every entry must point at a `LICENSE` that exists, and the page must
  reproduce enough of each one to prove it is the whole text, not a
  summary;
* every package pinned in `requirements.txt` must be named somewhere in
  the server list, plus the optional transcription dependency that is not
  pinned there and so would otherwise be missed;
* the licence the page claims for the app itself must match the root
  `LICENSE` file.

A missing licence file costs the notice, not the page: the entry falls back
to naming the path so whoever hits it can find what went missing.
`tests/test_vendored_licences.py` is what makes that fallback unreachable in
practice.

Sixteen tests. The page is translated into French like the rest of the
interface — including the three "what this library does" lines, which are
passed through `_()` as variables and so are invisible to the template
scanner that catches everything else.

### The README, while we were here

The project is *Veillée* and the README said *Storybook*. It now opens with
the name, the sense of the word, and what the thing actually is, followed by
a short tour of what is in it — which had been buried under three
paragraphs about the colour-scheme toggle.

It also says plainly what the rename does *not* cover: the application is
still `STORYBOOK_*` internally and the site title defaults to "Storybook"
until a family sets their own. Renaming the internals is a separate, larger
change, and a README that implied otherwise would be the more confusing of
the two options.

`pytest` (1524) and `ruff check .` green.


## F54. The name, in both languages

The project was *Veillée* and the application was *Storybook*. F53 wrote
that split down honestly in the README, and it was still a split: a French
reader met the real name, an English reader met a word that means nothing
in particular and that [Storybook](https://storybook.js.org) has owned in
software for a decade. The app now calls itself **Veillée** in English and
**La Veillée** in French.

### Both senses of the word

*Veillée* carries two, and the app wants both. They are not rivals — the
app is the second **because** it is the first.

The everyday sense is the gathering: the evening the family sat round the
fire after the day's work, hands busy, and someone told the stories worth
keeping. That is what the book is *for*, and it is what the app is already
dressed as — the firelight wash (F44), the warm paper schemes, the campfire
on the login screen, the deliberate refusal of anything that would make it
a feed.

Underneath it is the root verb, *veiller*: to stay awake, to keep watch
over someone. That one is what the app *does*. Markdown that outlives the
software, `.versions/` snapshots taken before every save, sealed letters
kept shut until their hour, the dead still named in the almanac every year.
A vigil kept over a childhood.

The README's epigraph is where both are said outright, in that order — the
fire first, because that is the room a reader should picture, and the verb
second, because that is the promise the storage format is making:

> *la veillée* — the evening the family gathered by the fire, and someone
> told the stories worth keeping. From *veiller*: to stay awake, to keep
> watch over someone.

One thing the first sense asks for and does not yet have, noted here rather
than built: a veillée is an *occasion*, and the app has none. It has days
(a story is dated to one), months (the almanac) and years (Growing up), but
no evening — no moment when the family is together with the book rather
than each alone with it. `months_since_last_story` (F30) is the closest
thing and it nudges the writer, not the readers. That is a feature-shaped
gap, not a naming one.

### The login screen

The one screen that speaks in the app's own voice rather than the family's
— before you are anyone, before their book title means anything to you —
was captioning a campfire with **"A private memory journal."** A category,
under a picture and a whole staged room that were already saying something
better. It now reads:

> Memories fade, what's written stays.

In French, **"Les souvenirs s'évaporent, les écrits restent."** — which is
the line that matters, the English being written to match it rather than
the other way round.

It is a rewrite of *"Les paroles s'envolent, les écrits restent"*, the
proverb every French speaker already carries, and the echo is the point:
the sentence arrives half-known. What changes is the half that makes it
this app's — *paroles* become *souvenirs*, so the thing at risk is not a
spoken word but a memory, which is exactly what a family loses and exactly
what this software exists to stop.

The order is the proverb's, not the first draft's, and deliberately: the
vanishing half goes first so the sentence **lands on what survives**.
Ending on *s'évaporent* ends on the loss; ending on *restent* ends on the
promise. The screen belongs to a book a parent is writing for a child who
will read it in twenty years, and the last three words are the reason to
bother — the nearest thing in the app to a lesson, which is what it was
asked to be.

The fire is not in the line, and does not need to be: it is in the
illustration directly beneath it, in the firelight wash over the whole
page (F44), and in the name at the top. The words are free to do the other
half.

`.login__subtitle` carries `text-wrap: balance`, and this sentence is the
one that most repays it. The English fits one line at 390px; the French
does not, and both wrap at 320px — and in every case the break falls on
the comma, so each half of the proverb gets a line of its own. That is the
best reading this sentence has, and it is luck plus `balance` rather than
anything the markup asks for. An earlier draft of a different line put its
last word alone on a second row, which is exactly the sort of thing pytest
cannot see and a screenshot shows instantly. (`text-wrap: pretty` was
already in `main.css`, so the family of properties had precedent here.) A
browser without it wraps the way it did before.

That screen can afford to evoke rather than explain, and this is why:
`request_account.html` and `accept_invite.html` carry their own
explanatory subtitles for anyone arriving by invitation, and nobody else
reaches `/login` who does not already know what it is.

The nav brand was also hidden there (`.page-login .site-nav__brand`). The
name was rendering twice, a hundred pixels apart, on the one screen where
it is the whole point — and that brand is the only thing in the nav with
nothing to do before you log in, since it links to the timeline, which
bounces straight back. The theme toggle, the flame and the language picker
stay; all three are useful from the door.

### Names change, identifiers do not

The default title is a translated string like any other, so all four
fallback sites go through `_()` and none of them hardcodes a language:
`create_app`'s `app_title` template global, `/manifest.webmanifest`,
`/book.epub`, and the MCP server's `_configured_title`. Product-name prose
in module docstrings and CSS banners moved with it.

What deliberately did **not** move: `STORYBOOK_*` environment variables,
the `storybook-lang` cookie, the `window.Storybook*` JS globals, and the
MCP server's `"storybook"` id. Those are identifiers, not names. Renaming
them would invalidate the configuration of every install that already
exists — a `.env` that silently stops working, an MCP client entry that
stops resolving — and buy nothing a reader would ever see. The README says
which is which, and why, rather than treating it as an unfinished job.

`test_the_apps_own_name_is_a_translated_string_not_a_hardcoded_one` pins
both values, and `test_a_reader_meets_the_name_in_their_own_language`
checks the login page actually shows each one. The two tests that used the
old subtitle as their canary for "this page is in French" now use the new
one.

`pytest` (1526) and `ruff check .` green; login checked in a real browser at
390px in English, French, light and dark.
