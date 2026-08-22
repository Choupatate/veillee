# CLAUDE.md

Guidance for Claude Code (or any AI agent) working in this repository.

## What this is

Storybook is a private, self-hosted memory journal: a parent writes stories
(text + photos) for their child, and the family reads them later as a
chronological timeline and book-like story pages. It's a Flask app with
**no database** — every story is a folder of a markdown file (with
frontmatter) plus its images/audio, living under `stories/`. Delete the app
entirely and the `stories/` folder is still fully readable with a text
editor and a file browser.

Read these before making non-trivial changes, in this order:
- `README.md` — how to run it, configuration, feature tour.
- `PLAN.md` — the original design spec the app was built from.
- `FEATURES.md` — the running log of every feature added since, in F-number
  order (F0, F1, F2, ...). Each entry documents the feature, the design
  decisions, and often the edge cases handled. **This is the most detailed
  and current source of truth for how a given feature actually behaves.**
- `REVIEW.md` — a past production-readiness audit and the fixes it drove.
  Historical record, not necessarily reflecting the current code.
- `IMAGE-PROMPTS.md` — the house style and per-asset prompts for the
  default (*ranch*) pack's illustrations (F42). Read it before generating,
  adding or placing any ranch illustration, and add finished assets to
  F17's table.
- `IMAGE-PROMPTS-ORBIT.md` — the same thing for the *orbit* pack (F46),
  most of whose icons are still to be drawn. A house style belongs to one
  art direction: never mix the two files' style rules.

  Both files are **hand-written prompts for one specific pack**, and are
  the record of what was learned drawing it. `app/theme_catalog.py` (F50)
  is the generic version the app generates for a pack a family makes: same
  37 assets, described by the job each does rather than by what the ranch
  or orbit draws for it. A rule learned in either markdown file — no
  lettering, no corner watermark, a dark outline on icons, an object and
  not a scene — belongs in the catalogue too, or the next person to make a
  theme gets to rediscover it.

When you finish a feature or fix worth documenting, add a section to
`FEATURES.md` following the existing style rather than leaving it
undocumented.

## Philosophy (do not violate these without discussing it first)

- **The data outlives the app.** Plain markdown + image files, human-readable
  forever. Never introduce a database or a binary/proprietary storage format.
- **No runtime network dependencies.** Everything needed to run is vendored
  under `app/static/vendor/` or served locally — no CDN links, no external
  fonts, no analytics beacons. (`editor.js` explicitly disables Toast UI's
  `usageStatistics` ping for this reason — never re-enable it.) If you vendor
  a new third-party library, document its version and provenance in a banner
  comment the way `toastui-editor-all.min.js` does.
- **Boring, minimal dependencies; no build step; no JS framework.** Plain
  `<script>` tags, UMD modules where code needs to run in both the browser
  and Node (see `tree-logic.js`, `safe-storage.js`). Don't introduce a
  bundler, transpiler, or framework to solve a problem that plain JS/CSS
  already solves.
- **Mobile-first.** Every screen, especially the editor, must work from a
  phone. Check narrow viewports, not just desktop, for any UI change.
- **Book, not blog.** No feeds, reactions, comment sections, or engagement
  mechanics. Restraint and typography over features.
- Deliberately out of scope (see README's "Ideas for later"):
  comments/reactions, RSS, email, video, encryption at rest, offline
  support/service worker, story deletion. Don't add these speculatively —
  if one becomes worth doing, it belongs in a discussion first, not a
  surprise PR. **This list shrinks**: accounts (F19), search and tags, and
  a translated interface (F38) were all on it once and have shipped, so
  check the code before believing anything here is absent.

## Architecture

Data layer — pure functions, no Flask, each taking its directory explicitly
(no hidden global state), so they're easy to test against a tmp directory:

- `app/storage.py` — **all filesystem read/write for stories lives here**:
  `Story` dataclass, `list_stories`/`get_story`/`create_story`/`save_story`,
  image/memo upload and re-encoding, `.versions/` snapshot+restore, backup
  zip import. Also home to several small pure date-math helpers used by the
  timeline (`on_this_day`, `growth_photos` F29, `months_since_last_story`
  F30). This is the module to read before touching how stories/people/
  images are persisted.
- `app/people.py` — the "cast of the book" (F14): `Person` dataclass
  (including F27's `born`/`died`/`unions`), `list_people`/`get_person`/
  `create_person`/`update_person`. Mirrors `storage.py`'s shape.
- `app/kinship.py` — the family-tree graph + kinship-label computation
  (F18) built from `people.py`'s `parents`/`partners`/`friend_of` edges.
  Kinship words ("uncle", "cousin") are always derived here, never stored.
- `app/life_events.py` — pure date-math for F27: `birthdays_today`,
  `union_anniversaries_today`, `almanac_entries`.
- `app/accounts.py` / `app/write_links.py` — per-person login credentials
  and delegated one-off write links (F19), each layered on top of a
  `people.py` Person the same way `life_events.py` is, storing their own
  JSON sidecar files (`account.json`/`write_links.json`) next to a
  person's `index.md`.
- `app/groups.py` / `app/invites.py` — audience scoping (F40) and account
  invitations (F19). **Read `groups.py` before touching anything that
  lists stories.** A story can name an audience, and `can_see` is what
  keeps it from everyone else; page routes must reach the list through
  `routes_pages._visible_stories()` rather than `storage.list_stories`,
  and `tests/test_groups.py` walks the route files to make sure none of
  them does. Kinship to a group is recomputed per request from
  `groups.json`, never trusted from the client.
- `app/i18n.py` / `app/translations_fr.py` — the interface in English and
  French (F38), hand-rolled: one dictionary keyed by the English source
  string, no gettext toolchain and no build step. `JS_STRINGS` is the
  subset the browser gets as a JSON blob. A test walks every template and
  fails on an interface string with no translation, so adding a `_("...")`
  means adding a French line in the same commit.
- `app/throttle.py` — the per-IP login lockout (10 failures / 15 minutes),
  in memory and deliberately not persisted.
- `app/dates.py`, `app/prompts.py`, `app/rendering.py`, `app/epub.py` — age-
  label computation, the writing-prompts list, markdown-to-HTML rendering,
  and EPUB export, respectively.
- `app/themes.py` — theme packs (F46). A pack is a folder under
  `app/static/themes/<name>/`: a `theme.css` of colour variables and an
  `img/` folder. **No template ever names an image folder** — they call the
  `theme_img('name.png')` Jinja global, which serves the configured pack's
  copy or falls back to the default pack's. That fallback is load-bearing:
  it is what lets a pack ship with a palette and no artwork at all. Two
  conventions `tests/test_themes.py` enforces: the same filename means the
  same picture in every pack (a pack is a skin, not a rename), and the
  default pack (`ranch`) is the only one allowed no holes. A pack's
  optional `theme.json` declares its display name, the picker's swatch
  colours, and which colour schemes it offers; that last list reaches the
  page as `<html data-schemes>` and is what `theme-boot.js` and `theme.js`
  cycle, so neither hardcodes the scheme names. Which pack a request
  renders is resolved once per request by `pick_theme` into `g.theme`
  (F48: `STORYBOOK_THEME` is the book's, a cookie is one reader's) — read
  it through the `current_theme()` helper in `create_app`, never
  `config["THEME"]` directly, or a reader's choice will be ignored on
  whatever you add.
- `app/theme_packs.py` / `app/theme_catalog.py` / `app/palette.py` — making
  a pack from inside the app (F50). Packs now come from **two** roots:
  shipped ones under `app/static/themes/`, made ones under
  `<stories>/themes/` — in the data folder, so artwork a family drew
  survives an app update and travels in the backup zip. `themes.py`
  checks the built-in root first, so a made pack can never shadow `ranch`
  and break the fallback. Three rules to keep if you touch this: the only
  filenames that can ever be written into a pack are the 37 in
  `theme_catalog.CATALOG` (the allowlist *is* the catalogue), a palette is
  validated hex rendered into CSS by `palette.py` and never user-authored
  CSS, and uploads are re-encoded through Pillow like every other image
  here. The catalogue describes each picture by the *job* it does, never by
  what the ranch draws for it — that is what lets another world supply its
  own equivalent.

Web layer — Flask, split by resource; each `routes_api_*`/`routes_*`
sub-file registers its routes onto a blueprint object (`bp`) defined in
its non-suffixed counterpart rather than declaring its own blueprint, and
is imported at the bottom of that file purely for the route-registration
side effect (so `url_for(...)` references never care which file a route's
code actually lives in — see each file's module docstring for specifics):

- `app/__init__.py` — `create_app()` factory; all config comes from
  `STORYBOOK_*` env vars (see `.env.example`), nothing is hardcoded.
- `app/auth.py` — login (single shared password, or F19 per-person
  accounts when `STORYBOOK_ACCOUNTS=1`). `login_required` decorator gates
  every page and API route except `/manifest.webmanifest` (must stay
  public for home-screen install) and `/login` itself.
- `app/routes_pages.py` (+ `routes_accounts.py`, `routes_people.py`,
  `routes_groups.py`, `routes_themes.py`) — HTML page routes (Blueprint
  `pages`): timeline/story/book/firsts/growth/almanac pages, account
  management, the family tree and person pages, audience groups, and the
  theme-making pages (F50, behind `admin_required_in_accounts_mode`).
- `app/routes_api.py` (+ `routes_api_people.py`) — JSON API routes
  (Blueprint `api`, under `/api`), consumed by the editor and tree JS.
  Every mutating endpoint validates its inputs explicitly (see the
  `_validate_*` helpers) rather than trusting the client — follow that
  pattern for any new endpoint.

AI-tool layer:

- `app/mcp_server.py` (+ `mcp_server.py` launcher at the repo root) — an
  optional [MCP](https://modelcontextprotocol.io) server (F32) exposing
  story/person read-write tools to an AI assistant, built on the same
  `storage.py`/`people.py` functions the web routes use. A separate
  entrypoint from `run.py`/`create_app()` — the Flask app never imports
  it. Local stdio transport only; see README.md's "MCP server" section
  before changing its trust model.

Frontend:

- `app/static/js/tree-logic.js` — pure, dependency-free tree math (BFS
  ancestor walks, chain validation), unit-tested directly under Node via
  `tests/js/tree_logic_test.mjs`. Keep new pure tree logic here rather than
  inline in `tree.js`, so it stays testable without a browser.
- `app/static/js/theme-logic.js` — the scheme cycle and the press rules
  behind F49's theme menu (a tap cycles, a hold opens it, and the click a
  long press leaves behind must not also cycle). Pure, so those three
  lines of decision are tested under Node rather than by hand.
- `app/static/js/recorder-logic.js` + `wake-lock.js` — the voice
  recorder's survival kit (F47). Audio in a `MediaRecorder` exists only in
  the tab until it is stopped and uploaded, so a phone locking its screen
  loses it: the app holds a screen wake lock while recording, and treats
  every interruption (page hidden, track ended or muted, recorder error)
  as a reason to stop *deliberately* — which is what hands over the
  chunks — and upload. A finished recording that fails to upload stays
  queued and is retried on the way back to the page, and `beforeunload`
  guards it meanwhile. Don't add a code path that ends a recording
  without saving what it captured.
- `app/static/vendor/` — vendored third-party JS (family-chart, d3, Toast UI
  Editor). Treat as read-only/generated; if you need to update one, redo the
  vendoring process documented in its banner comment, don't hand-edit it.
- `app/static/css/editor-theme.css` — the only place Toast UI's own class
  names may be styled (F44). It re-dresses the vendored editor in the theme
  variables so the writing surface matches the rest of the app. Two rules
  its header explains at length and neither of which is optional: it must
  stay linked *after* the vendor sheets, and every selector must keep its
  `:root` prefix. `tests/test_editor_theme.py` fails if either slips.

## Data-safety conventions (follow these for any new filesystem/upload code)

- Never build a filesystem path from user input without validating it first.
  Use/extend `storage.is_valid_story_id` / `is_valid_filename` (strict
  allowlist regexes, reject `..`) — see `story_media`/`person_media` in
  `routes_pages.py` for the pattern: validate, then check existence, then
  serve via `send_from_directory`.
- Uploaded images are always re-encoded with Pillow (`storage.save_image_to`)
  before being written to disk — never save an uploaded file's bytes
  verbatim. Uploaded audio is restricted to an explicit extension allowlist
  (`MEMO_ALLOWED_EXTENSIONS`).
- Writes to `index.md` go through a write-tmp-then-`os.replace` pattern for
  atomicity, and `save_story` snapshots the previous version into
  `.versions/` first. Preserve both properties in any code that writes story
  content.
- Zip extraction (`import_backup`) validates every member path before
  extracting anything (zip-slip protection) and is all-or-nothing (a
  collision aborts with nothing written). Keep that all-or-nothing guarantee
  if you touch import/export.
- `story_media`/`person_media` set a one-year `Cache-Control` max-age on
  `.jpg`/`.png` files (`_media_max_age` in `routes_pages.py`), safe only
  because `save_image_to` never overwrites or reuses a photo's filename.
  Voice memos are deliberately excluded from that long cache: `delete_memo`
  can free up a `memo-NNN` number that a later upload then reuses for
  different audio, so their filename isn't a stable cache key. If you add a
  new media type, work out whether its filename is truly immutable before
  putting it in `_LONG_CACHE_EXTENSIONS`.

## Running it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then edit STORYBOOK_PASSWORD and STORYBOOK_SECRET_KEY
python run.py           # dev server, debug on, http://127.0.0.1:5000
```

`STORYBOOK_SECRET_KEY` (not `SECRET_KEY`) is the Flask session-signing key;
the app refuses to start without one once `STORYBOOK_PASSWORD` is set. See
`.env.example` for every other `STORYBOOK_*` variable.

## Testing

```bash
pytest              # full suite: Python tests + every tests/js/*.mjs file,
                    # each run via subprocess by test_tree_logic_js.py
node tests/js/tree_logic_test.mjs     # or run one directly, without pytest
```

- Python tests live in `tests/*.py`, one file per feature area; `conftest.py`
  has the shared app/client fixtures.
- Client-side logic that can be written dependency-free (no DOM) belongs in
  a UMD module under `app/static/js/` with a matching `tests/js/*.mjs` file,
  wired into pytest via a `subprocess.run(["node", ...])` wrapper
  (`pytest.mark.skipif` if Node isn't available) — see
  `tests/test_tree_logic_js.py` for the pattern. Don't write DOM-dependent
  logic that can't be unit tested this way if a dependency-free version is
  feasible.
- There is no browser/E2E test suite in CI. For UI changes, manually verify
  in a real browser (Playwright is preinstalled in this environment at
  `/opt/pw-browsers/chromium`) before calling a UI change done — pytest
  green does not mean the feature works.
- CI (`.github/workflows/tests.yml`) runs `pytest` on every push/PR. Keep it
  green.

## Working conventions

- `ruff check .` runs in CI (config in `pyproject.toml`) — run it locally
  before pushing Python changes. No formatter or JS/CSS linter is
  configured; match the existing style by hand elsewhere: 4-space Python,
  no trailing whitespace, docstrings on non-obvious modules/functions in
  the style already used (see `storage.py`), minimal comments elsewhere.
- Dependencies in `requirements.txt` are pinned to exact versions
  (`flask==3.1.3`, etc.) — pin any new dependency the same way, and prefer
  not adding one at all given the "boring, minimal dependencies" rule above.
- This repository is public. Never commit real story content, real photos,
  a populated `.env`, or any credential — `stories/*` is gitignored except
  `.gitkeep` specifically so a real family's data can never accidentally
  land in git history. If you ever need sample content, use
  `scripts/seed_demo.py`, not real data.
