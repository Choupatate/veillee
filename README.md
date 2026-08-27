# Veillée

> *la veillée* — the evening the family gathered by the fire, and someone
> told the stories worth keeping. From *veiller*: to stay awake, to keep
> watch over someone.

A **private, self-hosted family memory journal**. A parent writes dated
stories — words and photographs — for a child to read years from now. The
family reads them back as a chronological timeline, as book-like printed
pages, or as an EPUB on an e-reader.

It is deliberately not a social network. No feed, no reactions, no comment
threads, nothing engineered to be scrolled. A book, written slowly, for a
handful of people who already love each other.

Everything is stored as plain **markdown files and images on disk** — no database.
If you delete the app entirely and keep the `stories/` folder, every story is still
fully readable with nothing more than a file browser and a text editor. The data is
meant to outlive the software that wrote it.

### What's in it

- **Stories and Instants** — a full dated entry with photos, or just a picture
  and one line for the small moments.
- **The cast** — everyone in the book, with a **family tree** that works out
  "great-aunt" by itself, plus birthdays, weddings, deaths and a
  month-by-month almanac.
- **Sealed letters** — write something today that stays locked, even to you,
  until a date you choose.
- **Firsts and Growing up** — a register of milestones, and the photo nearest
  each birthday laid side by side.
- **Voice memos** — a child's actual voice, kept next to the words.
- **Who reads what** — family accounts, invitations, and audience groups for
  the stories that aren't for everyone.
- **Reading it back** — timeline, printable book view, EPUB export, one-tap zip
  backup, optional offline transcription.
- **Yours alone** — self-hosted on your own machine, no cloud service, no
  analytics, no tracking, and **zero network requests at runtime**. Python and
  Flask, mobile-first, no build step, no JavaScript framework.

> **A note on the name.** The app calls itself *Veillée* in English and
> *La Veillée* in French — that is the title you see until your family sets
> its own, on the Settings page or with `STORYBOOK_TITLE`.
>
> The *internals* are still `STORYBOOK_*`: every environment variable, the
> language cookie, a handful of JavaScript globals, the MCP server's id.
> Those are identifiers, not names — renaming them would invalidate the
> configuration of every install that already exists, and buy nothing a
> reader would ever see. They stay as they are.

A colour toggle sits in the top-left corner. Tapping it cycles the schemes
the current theme offers — for the one the app ships with, that's dark (the
default), light, and manuscript, a warm aged-paper look with a subtly grained
texture (a self-contained inline SVG filter, no image assets or network
requests) where the timeline, story, and editor each render as a page resting
on a desk. The editor follows whichever one you pick: the writing surface is
the theme's own paper, in the same serif the finished story page uses.
*Holding* the same button opens a small panel with those schemes listed by
name, a "System" option that follows your phone or computer again, and the
book's whole *art direction*, which is swappable too — see "Themes" below.

Next to the theme toggle, a **flame button** turns *firelight* off and on — a
wash of warm light over the page whose brightness drifts up and down as if a
fire were burning in the room. The flame is lit and amber, in a ring of the
same colour, while the firelight is on, and small and grey once it's off. It's
on by default, off for anyone whose system asks for reduced motion, and the
choice is remembered per browser.

### What you actually have to set up

**Nothing, in a file.** Start it, and it prints a one-time code to its own
logs:

```
┌─────────────────────────────────────────────┐
│  This book is waiting to be claimed.        │
│  Open it in a browser and enter this code:  │
│                                             │
│      K7QP-3MRW-92XD                         │
└─────────────────────────────────────────────┘
```

Open the book in a browser, type that code, and choose the password your
family will use. The code only exists in the logs of the machine you
started it on, so the person who installed it is the only person who can
claim it — and it stops existing the moment they do.

There used to be two things to set here: a password and a session-signing
key, and the app refused to start without either. Both are generated now.
You can still supply `STORYBOOK_PASSWORD` and `STORYBOOK_SECRET_KEY`
yourself, and they win when you do — which is why an install that has been
running for a year notices none of this.

Everything else about the book happens **in the browser**. The first time
you log in, the app asks you four questions — what the book is called, who
it's for, when they were born, who writes in it — and then gets out of the
way. After that, the family runs it from the pages themselves: adding
people, drawing the family tree, making accounts and inviting relatives,
grouping who can read what, making a theme, taking backups. There is no
config file to come back to, and nothing here needs a restart.

Already running an older version? **Nothing changes and nothing is asked
of you.** A book with stories in it counts as already set up; your existing
environment variables keep working exactly as they did, and the new
Settings page simply shows them, should you ever want to change one without
editing a file.

See `PLAN.md` for the full design specification this app was built from, and
`REVIEW.md` for the production-readiness review it was subsequently audited
against.

## Running it

> **Not a developer?** [**docs/install.md**](docs/install.md) is the page
> for you — one command, no repository to clone, and an honest section on
> the router problem before you spend money on a domain. What follows here
> is for running it from a checkout.

### Locally (dev server)

Requires Python 3.12+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # optional: nothing in it is required
python run.py
```

The dev server runs at `http://127.0.0.1:5000` with debug mode on. `run.py`
defaults `STORYBOOK_PASSWORD` to `dev` — only there, so that a checkout you
run twenty times a day doesn't ask to be claimed each time it gets a fresh
stories folder.

**Serve this app over HTTPS, or only on a trusted LAN.** The single shared
password is sent as a plain form field on every login; without HTTPS (or a
network you already trust) it travels in cleartext.

To try it out with sample content:

```bash
python scripts/seed_demo.py ./stories
```

### Locally (production-style, waitress)

```bash
python serve.py
```

Serves on `http://0.0.0.0:5011` by default (set `PORT` to change it).

### Docker

The published image, which is what [docs/install.md](docs/install.md) uses
and what a family should install — no clone, no build:

```bash
docker run -d --name veillee --restart unless-stopped \
  -p 5011:5011 \
  -v "$PWD/stories:/data/stories" \
  ghcr.io/choupatate/veillee:latest
```

Read the claim code it prints with `docker logs veillee`. To put it on your
own domain with a real certificate, `compose.https.yml` runs it behind Caddy
— set `DOMAIN=` in `.env` and nothing else.

Or build it yourself from a checkout:

```bash
docker build -t storybook .
docker run -p 5011:5011 \
  -v storybook-data:/data/stories \
  storybook
```

The container stores stories under `/data/stories`; mount a volume there so content
survives container recreation. **Mount it before the first start**: that is
also where the generated signing key is kept, and a container without a
volume makes a new key every time it restarts, logging the family out on
each update. The app refuses to start rather than do that silently.

### Docker Compose (e.g. Synology)

Clone this repo directly into the folder where you want everything to live,
e.g. `/volume2/Media/StoryBook`, then:

```bash
cp .env.example .env   # optional: nothing in it is required
docker compose up -d --build
```

`docker-compose.yml` reads `STORYBOOK_PASSWORD`, `STORYBOOK_SECRET_KEY` and
`STORYBOOK_COOKIE_SECURE` from `.env` in the same directory — **all three
optional**: with none of them set, the book generates its own signing key
and is claimed from the browser (Compose loads it
automatically — no `env_file:` needed) and bind-mounts the `stories/` subfolder
of that same clone to `/data/stories` in the container — keeping code and data
under one folder without mixing story files into the git working tree. On
Synology, either run this from an SSH session with Docker installed, or point
Container Manager's project at this repo folder. Adjust the host path in
`docker-compose.yml` if you cloned somewhere other than
`/volume2/Media/StoryBook`.

### Configuration

**Most of this is optional, and the second table is settable in the app.**
The first table describes the *machine* — where files live, what the
password is, whether a proxy sits in front — and those can only come from
the environment, since the app needs them before it can serve a page.

The second describes the *book*, and can be set from **Settings** in the
nav (or the first-run questions) by whoever administers it. Setting one
there overrides the variable and takes effect immediately; the variables
stay supported, and are what a fresh install starts from.

See `.env.example`:

| Variable | Purpose |
|---|---|
| `STORYBOOK_STORIES_DIR` | Where story folders live (default `./stories`) |
| `STORYBOOK_PASSWORD` | The one shared password. **Optional** — leave it unset and the book is claimed from the browser instead, using a code printed to the logs on first start. Set it and it wins, as it always did. |
| `STORYBOOK_SECRET_KEY` | Flask session-signing secret. **Optional** — leave it unset and the app generates one on first start and keeps it in the stories folder as `secret_key` (mode `0600`, and it travels in no backup zip). Set it to manage the key yourself; a value here wins. |
| `STORYBOOK_COOKIE_SECURE` | Set to `1` when serving over HTTPS to mark the session cookie `Secure` and send an HSTS header. Default off, for local/LAN HTTP use. |
| `STORYBOOK_TRUSTED_PROXIES` | How many reverse proxies sit in front of the app (default `0`). Set to `1` behind nginx/Caddy/a NAS reverse proxy so the login lockout sees each visitor's real IP. See "Opening it to the internet". |
| `STORYBOOK_ACCOUNTS` | Optional. Set to `1` for per-person username/password accounts with an admin role, instead of one shared password (see below). Unset by default. |
| `STORYBOOK_OPEN_REQUESTS` | Optional. Set to `1` to let someone request an account without knowing the invite code, waiting for an admin instead (see below). Requires `STORYBOOK_ACCOUNTS=1`. Unset by default. |

And the book's own, all optional, all changeable later from **Settings**:

| Variable | In Settings as | Purpose |
|---|---|---|
| `STORYBOOK_TITLE` | Name of the book | The display name — nav, page titles, install manifest, book cover. Defaults to `Veillée` / `La Veillée`, following the reader's language. |
| `STORYBOOK_BIRTHDATE` | Birth date | The child's birth date (`YYYY-MM-DD`). Shows their age at each memory, and turns on the Growing up page. |
| `STORYBOOK_CHILD` | The book is about | The person the family tree's kinship words ("aunt", "cousin") are worked out relative to. |
| `STORYBOOK_AUTHORS` | Narrators | `Name:#hexcolor` pairs for several narrators. In Settings, one `Name #hexcolor` per line. |
| `STORYBOOK_LANGUAGE` | Language | The book's own language (`en` or `fr`) for a visitor who hasn't picked one and whose browser expresses no preference. Each reader's own choice always wins. |
| `STORYBOOK_THEME` | Theme | The book's art direction — a pack that ships with the app (`ranch`, `orbit`) or one your family made. Each reader can still pick another for their own screen. See "Themes". |

### Family accounts (optional, off by default)

Set `STORYBOOK_ACCOUNTS=1` to replace the one-shared-password login with
real per-person accounts: an **admin** role that creates accounts and
binds each one to a family member's person page, and a **family** role
that can read/write the whole book like today, plus manage its own
password. Leaving it unset keeps the app exactly as it's always been —
this is additive, not a replacement, for families who don't need it.

The book's shared secret never logs anyone in once this is on — instead it
becomes the invite code required on the **Request an account** page
(whether that secret came from `STORYBOOK_PASSWORD` or was chosen when the
book was claimed)
(linked from the login page), so a stranger who finds the URL can't queue
requests without knowing it. Anyone who submits one picks their own
username and password up front; an admin then reviews it from
**Accounts** in the nav (visible to admins only) and either approves it —
binding it to an existing family member or creating a new one on the
spot, with an admin or family role — or rejects it. Admins can also create
an account directly, skipping the request queue, for a family member who
won't submit their own. The very first request ever submitted is special:
with no admin yet to review it, it auto-approves immediately as admin,
bound to a brand-new person page built from the display name — if that
duplicates a person who already existed, an admin can re-link the account
to the existing person page from **Accounts** at any time, leaving the
duplicate in place but unbound rather than deleting anything.

#### Inviting someone, instead of waiting to be asked

Approving a request means the newcomer chose their own username and
password before you ever saw them. Going the other way — **Accounts** →
**+ Invite** — an admin picks who the account is for (an existing person
page, or a new one created on the spot) and what role it gets, and gets
back a one-off link to send them. The recipient opens it, chooses their
own username and password, and lands on the login page ready to sign in.
Nobody ever has to type someone else's password or send one over a chat
app.

An invitation expires after 14 days by default (adjustable, or never),
works exactly once, and can be withdrawn at any time from **Accounts**,
where every outstanding one is listed. Issuing a fresh invitation for the
same person quietly withdraws the previous one, so a link that went to the
wrong place stops working the moment you replace it. The link is shown
once, at creation — only a hash of it is ever stored, so there's no way to
look it up again later.

#### Letting people ask without the code

Set `STORYBOOK_OPEN_REQUESTS=1` and the invite code on the request form
becomes optional: a relative who was never given it can still ask, and
simply waits for an admin. Two things stay true, both deliberately:
submitting a *wrong* code still fails (only leaving it blank is newly
allowed, so the code never becomes guessable one attempt at a time), and a
codeless request can never be the auto-approved first admin — bootstrapping
the book still requires proving you know the code. The queue holds at most
25 unreviewed requests, so an open form can't be used to grow a file on
your disk without limit.

Whichever way a request arrives, the review screen flags a pending request
whose name matches someone already in the book — loudly if that person can
already log in, since approving it would give one human two accounts. This
app has no email address to key an identity on, so this is a prompt for the
admin's judgement rather than something the code can refuse outright;
invitations avoid the question entirely, since the seat is set aside for a
specific person up front.

#### Groups — telling some stories to fewer people

By default every account reads every story, and that stays the default. A
**group** is a named handful of people a story can be kept to, for the
things that are for a wife and a son and nobody else. Anyone can make one
from **Groups** in the nav: give the group a name, then tick who's in it. A
story with no group is for everyone; a story with one is visible only to
that group's members (any of them, if it lists several).

Three rules worth knowing before you rely on it:

- **Membership governs reading; role governs managing.** An admin who
  isn't in a group can't read its stories — not on the timeline, not by
  URL, not in the book, not by fetching a photo directly, and not through
  the editor or the API. An admin can of course add themselves to the
  group and then read it, but that's a visible change to the group rather
  than a silent power.
- **A group is changed by the people in it** (or by an admin). Anyone can
  create one, but only its members can rename it or change who's in it —
  otherwise anyone could add themselves to *Just us* and read it. Making a
  group puts you in it, so you can always maintain what you made; take
  yourself out and you hand it over for good. Adding someone opens every
  story kept to that group, including other people's, so the page says how
  many of those there are before you do it.
- **The author always sees their own story**, even if they scoped it to a
  group they aren't in. That's a safety rail against a mis-tap, not a
  permission — and it's switched off for both of them if two people in the
  book share a display name, since a name alone can't tell them apart.
  Rename one and it comes back.

Two groups can't cover exactly the same people — identical membership is
one circle under two names, and a story kept to one would look protected
from people who can read it through the other. Nor can two groups share a
name. A book holds up to 40 groups, because every group is a chip in the
editor's audience row and that row has to stay readable on a phone.

In the editor (and the instant composer), a **Who can see this** row of
chips picks the groups. Nothing lit means everyone — and because an
invisible default is the kind that gets someone in trouble, the current
audience is always spelled out underneath in words: *Everyone*, or *Only
Just us*. A scoped story then says **Kept to Just us** under its title,
and carries a small *kept to a group* marker on the timeline, so you can
tell at a glance which stories are for the whole family and which aren't.

Restoring an older version of a story brings back its old *words* and
leaves its audience alone — widening who can read something stays a
deliberate act, never a side effect of undoing an edit.

**Backups are scoped to what you can see.** If some stories are kept to
groups you're not in, the zip you download leaves them out, and the import
page says so. A complete backup has to come from someone who can see every
story. Restoring a backup is admin-only.

**And a backup carries no logins unless an admin took it.** Account files
— password hashes, invitations, write links — sit in the same folder as
the memories, so a plain family member's zip would otherwise hand them
every account's hash to work on offline, where the login lockout can't
see them. Only an admin's export includes them, and no import ever
restores them (below).

Groups need `STORYBOOK_ACCOUNTS=1`. With one shared password there's a
single identity and nothing to scope a story away from, so the whole
feature is invisible and no existing install changes.

The MCP server (below) is **not** scoped — it's a local stdio process
running as whoever starts it, with the `stories/` folder already readable
to that user, so its tools see every story regardless of group.

#### Managing accounts

Disabling an account, resetting its password, or changing its role (from
the same page) all take effect immediately, not whenever its browser
session would otherwise expire — and there's always at least one admin
left standing: demoting or disabling the last one is refused rather than
locking everyone out. Every account holder can change their own password
from **Account** in the nav, which also logs out any other device they're
signed into; there's no email in this app, so if someone forgets their
password an admin resetting it from **Accounts** is the only way back in.

Any account holder can also generate a **write link** from **Account** →
**Write links** — a one-off URL that lets someone write a single story for
them without an account of their own (no username, no password, nothing
else in the book visible to them). Links can be single-use or reusable,
optionally expire, and are revocable at any time by whoever created them
or by an admin.

With accounts on, every story a family member writes is automatically
attributed to them — no picker needed, and it can't be spoofed by another
account. Each person can set their own byline color on their person page
(**Byline color**), replacing what `STORYBOOK_AUTHORS` does below; a
family member with no color set yet gets a neutral default rather than no
color at all.

### Several narrators

Set `STORYBOOK_AUTHORS` (e.g. `"Papa:#d9a441,Maman:#7ba7d9"`) to let more than
one family member write in the same shared timeline. Each story picks up an
author from a row of chips in the editor — remembered per device after the
first pick, so it's zero-tap after that — and the two voices are then clearly
split by color on the timeline (colored dot, name, and a small legend) and on
the story page (a colored byline and title flourish). Pick mid-brightness
colors that read well on both the dark and light themes.

There are still no accounts or per-author passwords — one shared login, same
as always. The author is just a label on the story. This whole section is
superseded automatically the moment `STORYBOOK_ACCOUNTS` is on — see above —
`STORYBOOK_AUTHORS` is simply never read in that mode, whether or not it's
still set. Leaving `STORYBOOK_AUTHORS` unset (and accounts off) disables the
whole feature: no picker, no bylines, no legend, identical
to running without it. Renaming an author in this variable does not rewrite
already-saved stories; a story whose `author` no longer matches a configured
name still shows its byline, just in the neutral default color.

### Instants — a lighter way to capture

"+ Instant" (next to "+ New story") is a deliberately tiny capture form: one
photo, one optional line, done in about fifteen seconds on a phone. Instants
render as compact, quieter entries on the timeline (small thumbnail, no
title styling) and as small captioned figures in `/book` — interludes, not
chapters — while a full story page (and the full editor, for touch-ups)
still works normally at their direct URL. They're just a story with one
extra frontmatter key (`kind: instant`); nothing new to back up.

### Taking a photo in the app

Anywhere you can add a photo — the Instant form, the story editor's
"Photo" section, and a person's Photo panel — there's also a "Take a
photo" button that opens the camera right in the page: live preview,
shutter, then "Retake" or "Use photo" before anything is saved. On a
phone you can flip between the front and back camera; a selfie previews
mirrored and saves the way everyone else sees you. A photo taken this way
is treated exactly like an uploaded one (re-encoded, numbered
`photo-NNN.jpg`, cropped and toned for portraits).

**Camera capture only works in a secure context** — HTTPS, or
`localhost` — the same limitation as voice-memo recording below. Over
plain LAN HTTP the "Take a photo" buttons simply don't appear, and
choosing an existing file (which on a phone still lets you use the
camera app) works as it always has.

### In French, or in English

Two flags sit at the top of every page — including the login page, so
someone can switch before typing a password. The choice is remembered per
person, in a cookie that lasts a year and survives logging out, so each
family member reads the book in their own language on their own devices.
If nobody has chosen, the browser's own language preference decides; after
that the book's own `STORYBOOK_LANGUAGE` setting, and finally English. A
reader's own pick always beats all of it — so an English-speaking relative
visiting a French book still gets English, and one tap changes it either
way.

Only the **interface** is translated. What you write — titles, stories,
tags, people's names — is shown exactly as you typed it, in whatever
language you wrote it. Dates follow the reader's language too (`18 juin
2026` / `June 18, 2026`), as do ages (`3 ans` / `3 years old`).

Adding another language means adding one file like
`app/translations_fr.py` and one entry in `LANGUAGES`; there is no build
step and no gettext toolchain. A test walks every template and fails if
any interface string is missing a translation.

### Firsts — a register of milestones

Any story (or instant) can carry an optional milestone label — "First
steps", "First word", "First day of school" — a plain text field right
under Tags in the editor. Give one a label and it shows up as a small
pill on that story's page and on its timeline entry, and it takes its
place on `/firsts`: every milestone, oldest first, each linking back to
its story. There's no separate thing to write — it's the same story you
already wrote, just labeled.

### Growing up — a photo per birthday

When `STORYBOOK_BIRTHDATE` is set, `/growth` (linked from the timeline as
"Growing up", once at least one story has a cover photo) shows one photo
per year of the child's life — whichever story cover lands closest to
that birthday — in a simple grid, oldest first. Nothing new to write:
it's built entirely from cover photos you've already added.

### People — the cast of the book

"People" in the nav (always visible, whether or not you've added anyone
yet) is a small cast page: a portrait, a name, and how they relate to the
child — "your grandmother", "your godfather" — with a free-text page of
their own for a longer bio, in the same editor as stories. The grid on
`/people` shows everyone in the order they were added, each as a square
portrait (or a plain initial when there's no photo yet).

People live in `stories/people/<slug>/` — still inside the one stories
folder, still one backup. Stories link to a person by hand with an
ordinary Markdown link (`[Mamie](/people/mamie)`); there's no
auto-linking or `@mention` syntax, so a name in a story stays plain text
unless you deliberately link it. People don't show up on the timeline or
in `/book` — this is a reference page, not another kind of memory — and,
like stories, there's no way to delete one once added.

A portrait's crop is baked into the uploaded image itself: the person
editor's dedicated Photo panel lets you pan and zoom the source photo
against an oval guide (drag to pan, works with touch; a slider and +/-
buttons to zoom) before it's ever uploaded, so there's no separate stored
focus point to keep in sync across the very differently-shaped places a
portrait renders. A portrait can also optionally record `photo_sepia`
(0-100, defaults to 30 whenever a photo exists), a manually-set sepia tone
percentage — drag the slider or type a number in the same panel — applied
everywhere the portrait renders (the people grid, the person page, family
thumbnails, the tree) so real photos read as part of the same hand-drawn,
paper-and-ink book as the illustrations, instead of clashing with it.
Uploading a new photo always resets the tone back to the default, since a
new photo needs a fresh one.

### Life dates — birthdays, deaths, and unions

A person can optionally record a birth date, a death date, and one or
more unions (a wedding, a PACS, or a plain "together since" date) with an
existing partner — each union can also record when it ended. These show
up on the person's own page, and everywhere at once on `/almanac`
(linked from `/people`): every recorded date, month by month, like a real
family record book's calendar page, independent of year.

The timeline also gets quiet banners for a living person's birthday and
an ongoing union's anniversary, right next to the existing "X years ago
today". Death anniversaries and ended unions are recorded but never
banner-surfaced — they're something you can go look up, not something
that shows up uninvited.

### The family tree

Person pages can optionally record `parents` (up to two), `partners`
(symmetric — linking one side writes both), `friend_of`, and `gender`.
These are plain facts, never computed labels: relations like "uncle" or
"cousin" are always derived from them at read time, never stored. Fill
them in through the "Family" fieldset in the person editor — chip pickers
reusing the author-chip look, shown once at least one other person exists.

Set `STORYBOOK_CHILD` to the slug of your child's person page and every
"YOUR ___" line on a person page, and the whole `/tree` chart, computes
labels relative to that anchor ("your grandmother", "your great-uncle",
"your uncle's wife" for an in-law one hop out). Leave it unset and
everything still works, just without the "your ___" wording. When the
book is inherited, re-point this one line at the next generation.

`/tree`'s toolbar switches between **Direct line** (just your own
ancestors), one button per **ancestor branch** (aunts/uncles/cousins,
one small chart per couple), and **Everyone** — the whole family as a
single graph, generation by generation, every person exactly once
regardless of how many marriages or half-siblings connect them.

`GET /api/tree` (login required) is the seam future renderers plug into —
the vendored chart on `/tree` is just today's consumer:

```json
{
  "anchor": "milo",
  "people": [
    {
      "id": "papi-georges",
      "name": "Papi Georges",
      "gender": "m",
      "photo": "/people/papi-georges/media/photo-001.jpg",
      "photo_sepia": 30,
      "url": "/people/papi-georges",
      "kinship": "your grandfather",
      "rels": { "parents": [], "partners": ["mamie-lise"], "children": ["papa"] }
    },
    {
      "id": "ami-jean",
      "name": "Ami Jean",
      "gender": null,
      "photo": null,
      "photo_sepia": null,
      "url": "/people/ami-jean",
      "friend_of": ["papa"]
    }
  ]
}
```

`anchor` is `null` when `STORYBOOK_CHILD` is unset or points at a slug
that doesn't exist. Anyone linked into the family graph (has a parent,
partner, or child) gets a `kinship` label (`null` when there's no anchor
or they're unreachable from it) and a `rels` object. Everyone else —
friends and people with no links at all — gets a `friend_of` list instead
(empty for a fully unlinked person).

### Voice memos

A "Voice" section on the story editor lets you record directly in the
browser — record, pause/resume, stop — with no length limit; recordings
upload as soon as you stop and appear in the list right away, each with
its own delete button (the one deletion this app supports, undoable only
by re-recording). On the story page, a "Listen" section plays back every
memo in order. Files are ordinary `memo-001.webm`/`memo-002.m4a`/... in
the story folder, same numbering scheme as photos.

**Microphone capture only works in a secure context** — HTTPS, or
`localhost`. Over plain LAN HTTP the record button simply won't appear
(playback still works everywhere), so if you're running Veillée on your
home network rather than on the same machine as the browser, put a
reverse proxy with a certificate in front of it to use this feature.

While a recording is running the app asks the browser to **keep the screen
awake**, because a phone that locks its screen mid-sentence takes the
microphone with it — and, worse, doesn't stop the recording: it keeps
going, storing silence, with the timer still counting up. If the browser
won't hold that lock, or you lock the phone yourself, or another app takes
the microphone, the recording is ended on purpose and everything captured
up to that moment is uploaded and kept — you get a memo and a line saying
what happened, never silence and a lost story. Should the upload not get
through (the phone froze the page behind a lock screen, say), the audio
stays in the tab and is sent again the moment you come back to it; closing
the tab first is the only way to lose it, and the browser asks you to
confirm before that happens.

A **level bar** next to the timer moves with your voice, so a microphone
that has quietly died is visible while you're still talking rather than
discovered on playback. If it reads perfect silence for twenty seconds
straight — which a live microphone in a quiet room never does — the
recording is ended and saved on the assumption the microphone is gone.

Drop a plain-text file named after a memo with a `.txt` extension next to
it (e.g. `memo-001.txt`) and its contents show up as a "Transcript" under
that recording — the app never writes these itself, so anyone can type
one by hand, or generate them offline:

#### Offline transcription

`scripts/transcribe_memos.py` walks a stories folder, finds memos that
don't have a transcript yet, and writes one using
[faster-whisper](https://github.com/SYSTRAN/faster-whisper) — entirely
offline, nothing is uploaded anywhere:

```
pip install -r requirements-transcribe.txt
python scripts/transcribe_memos.py ./stories --language fr --model small
```

Its dependencies are intentionally kept out of `requirements.txt` and are
never imported by the app itself — this is a tool you run occasionally
from a laptop against the stories folder (or a copy of it; the resulting
`.txt` sidecars can be copied back), not something the server needs. The
first run downloads a model (hundreds of MB), so expect it to take a
while the first time.

### Age at each memory

Set `STORYBOOK_BIRTHDATE` to the child's birth date and every story and
timeline entry shows the age at that memory — `JUNE 18, 2023 · 2 YEARS OLD ·
PAPA` on the story page, `Jun 18 · Papa · 2 years old` (smaller, dimmer) on
the timeline. Ages before the birth date read "before you were born"; sealed
letters never show an age, keeping the envelope minimal. Leave the variable
unset to disable the feature entirely.

### Home-screen install

Veillée can be added to a phone's home screen like a native app (a
`manifest.webmanifest`, sized icons, and standalone display mode) — set
`STORYBOOK_TITLE` (e.g. `"Le livre de Milo"`) so it shows up under your own
title rather than "Veillée". There is deliberately **no service worker and
no offline caching** — every visit still talks to the server, it just looks
like an app when launched. Regenerate the icons with
`python scripts/make_icons.py` if you change the design; the outputs are
committed under `app/static/icons/`.

**Installing also puts Veillée in the phone's share sheet.** Once it's on
the home screen, sharing a photo from the camera roll (or from anywhere
else) offers Veillée as a destination: pick it, and the editor opens with
that photo already attached, as a **draft**. Write something, save, and it
becomes a story; leave it, and it stays on the Drafts page and never
reaches the timeline or the book.

This is the fastest way to get a moment into the book, and it only exists
once the app is installed — a browser tab can't appear in a share sheet.

### Sealed letters

Setting a "Seal until" date on a story in the editor turns it into a sealed
envelope until that date: the timeline shows only an envelope glyph and an
"opens on" date (no title, no photo), and the story page itself shows the
same envelope instead of the text. **The seal is ceremonial, not
cryptographic** — anyone with the shared password (or direct access to the
disk) can still open and read the file; the point is the ritual of an
unopened letter, not access control. Authors reach editing via `/edit/<id>`
directly, which keeps working on a sealed story — only the reading view is
blocked. Once the unlock date passes, the entry becomes a normal story
automatically, with no action needed.

### Archiving a story

The "Archive" chip in the editor (next to "Draft") is a softer alternative
to deletion, which this app deliberately doesn't have. An archived story
disappears from the timeline, drafts list, book, prev/next navigation, and
"years ago today" banner — same as a draft — but the file is never touched:
it's still fully readable at its direct URL (with a small "ARCHIVED" pill),
still listed on a dedicated `/archived` page (linked from the timeline when
at least one story is archived), and un-archiving is just toggling the chip
back off.

### Version history

Every save keeps the version it's about to overwrite: before writing new
content, the previous `index.md` is copied into a hidden `.versions/`
subfolder inside that story's own directory (the last 20 are kept; older
ones are pruned automatically). "View history" on the edit page lists them
newest-first with a one-tap Restore — restoring goes through the same save
path, so it snapshots the current version too, meaning you can never lose
content by restoring, only add another point to the timeline. This is a
local safety net for "I pasted over the wrong paragraph" or "I clicked save
before finishing a rewrite," not a full undo/redo history — there's no diff
view, just full-version snapshots.

### Autosave and crash recovery

Separately from server-side version history (which only records content
you've actually saved), the editor also autosaves the current title, date,
and body to the browser's `localStorage` a couple of seconds after you stop
typing. If you close the tab, lose your connection, or the browser crashes
before your first manual save, reopening that story (or `/new`, for a story
you never got to save at all) shows a small banner offering to restore it.
This never touches the server or other devices — it's purely a per-browser
safety net for the gap between typing and clicking Save.

### Opening a page at random

"Open a page at random" on the timeline, and "At random" on every story
page's footer, jump to a uniformly random readable story — drafts, sealed
letters, and instants are never picked (page-turning is for real stories).
The story-page link excludes the page you're already on, so tapping it
repeatedly always moves somewhere new.

### Writing prompts

A new story starts with a quiet idea to answer or ignore: a small italic
line above the editor ("Qu'est-ce qui t'a fait rire aux éclats cette
semaine ?" and 55 others in the same spirit), with a &#8635; button next to
it for another one. It only appears before a story's first save — editing
an existing story never shows it — and it is never inserted into the text
itself, it's just there for inspiration. To use your own list instead of
the shipped one, drop a `prompts.txt` file in the stories folder, one
prompt per line (blank lines and `#`-prefixed comments are ignored); it
replaces the default list entirely rather than adding to it.

### A gentle nudge after a quiet spell

If it's been a while (3+ months) since a story was last written, the
timeline shows one quiet italic line — "Nothing new in 4 months — a
little story?" — linking straight to a new story. Not a notification,
not a streak to keep: it only ever appears on the timeline itself, and
it's based on when you actually wrote, not the date the story is about,
so backdating a memory never triggers it.

### Finding a story

A search box above the timeline filters entries by title (and author) as
you type — purely client-side, filtering what's already rendered, no
server round-trip. A "Jump to the latest" link next to it scrolls straight
to the newest entry, useful once there are enough stories that reading
chronologically from the top isn't how you want to start.

### Reading it as a book

`/book` (linked from the bottom of the timeline as "Read as a book") renders
every readable story on one page, oldest first, with a title cover and a
small ornament between entries — drafts and sealed letters are excluded, same
as the timeline. It doubles as a print layout: the floating "Print / save as
PDF" button calls the browser's native print dialog, which (via a dedicated
print stylesheet) forces the light palette, hides all navigation and buttons,
and starts each story on its own page — "save as PDF" in the print dialog
gives a clean, book-like PDF of the whole thing. "Download as PDF" on the
timeline is the same flow made one tap shorter: it opens `/book` and
triggers that print dialog automatically, so you land straight on "save as
PDF" without needing to notice the floating Print button. There's no
server-generated PDF file — that would mean adding a real dependency (a PDF
library, or shelling out to a headless browser), which this project
deliberately avoids; the browser's own print-to-PDF is free, reliable, and
already produces the same clean layout.

Whenever the calendar year changes, a year chapter divider appears first —
the year, and (with `STORYBOOK_BIRTHDATE` set) the child's age at that
point — so a printed copy reads like a real book's chapters rather than one
long run of stories. It's purely a rendering grouping; nothing new is
stored.

### Downloading as an EPUB

"Download as EPUB" (next to "Read as a book" on the timeline) streams the
same readable stories as a real `.epub` file — a minimal, hand-built EPUB3
(stdlib `zipfile` and string templates, no new dependency) with a cover
page, a chapter per story, embedded photos, and a table of contents, openable
in Apple Books, Kindle (after conversion), calibre, or any other e-reader
app. Unlike `/book`, this needs no browser and no print step.

### MCP server — letting an AI help write

`app/mcp_server.py` (launched via `mcp_server.py` at the repo root) exposes
stories and people as tools an AI assistant (Claude Desktop, Claude Code,
or any other [MCP](https://modelcontextprotocol.io) client) can call
directly: `list_stories`, `get_story`, `create_story`, `update_story`,
`add_story_photo`, `list_people`, `get_person`, `create_person`,
`update_person`, `set_person_photo`, and `get_journal_context` (a snapshot
of what's recorded so far, today's birthdays/anniversaries, and whether
it's been a quiet spell since the last entry). It's an optional add-on,
not something the web app depends on.

#### Quick start

**If your MCP client runs on the same machine as `stories/`** (e.g. you run
Veillée on your own laptop), point it at the server directly:

```json
{
  "mcpServers": {
    "storybook": {
      "command": "/path/to/storybook/.venv/bin/python",
      "args": ["/path/to/storybook/mcp_server.py"],
      "env": { "STORYBOOK_STORIES_DIR": "/path/to/storybook/stories" }
    }
  }
}
```

Claude Code instead of Claude Desktop: `claude mcp add storybook
/path/to/storybook/.venv/bin/python /path/to/storybook/mcp_server.py --env
STORYBOOK_STORIES_DIR=/path/to/storybook/stories`.

**If Veillée runs on a home server/NAS and your client is on a laptop**,
the server itself doesn't need to change — since stdio just needs *some*
process's stdin/stdout, point the client's command at `ssh` instead of at
`python` directly, so the connection tunnels over an SSH session you
already control (key-based, non-interactive auth — the client can't
answer a password prompt):

```json
{
  "mcpServers": {
    "storybook": {
      "command": "ssh",
      "args": [
        "user@your-server",
        "STORYBOOK_STORIES_DIR=/path/to/storybook/stories /path/to/storybook/.venv/bin/python /path/to/storybook/mcp_server.py"
      ]
    }
  }
}
```

**A cloud-hosted client with no network path to your server at all**
(e.g. a remote coding session) genuinely can't reach it this way — stdio
requires the client to launch the process, locally or over SSH, not talk
to it over the open internet. Making that work would mean giving the
server an actual network listener instead of stdio, which is a deliberate
trust-boundary change (a network-reachable read-write endpoint into a
private journal) worth deciding on its own, not a quick-start item.

Once connected, just describe what you want in plain language — e.g. "add
my grandmother Jeanne as a person, born March 3rd 1950" or "does anyone
have a birthday today?" — the client figures out which tool(s) to call.

It reads the same `STORYBOOK_STORIES_DIR`/`STORYBOOK_AUTHORS`/
`STORYBOOK_BIRTHDATE`/`STORYBOOK_TITLE` variables the web app does, and
every write goes through the exact same `storage.py`/`people.py` functions
the editor uses — atomic writes, `.versions/` snapshots, Pillow
re-encoding for photos, symmetric partner/union syncing. **It has no login
of its own and only ever runs locally over stdio** (never a network
port): whoever can launch the process already has filesystem access to
`stories/`, same as running the app itself, so it's meant to run on the
same machine as your MCP client, not exposed remotely. Photo uploads take
base64-encoded image bytes as a tool argument instead of a multipart file;
voice memos and zip import/export aren't wired up as tools.

### Themes

A **theme pack** is the book's art direction: its palette, its
illustrations, its icons. Two ship with the app, chosen with
`STORYBOOK_THEME`:

- **`ranch`** (the default) — the hand-drawn western storybook the app was
  built around: amber lamplight, aged paper, rope and lantern.
- **`orbit`** — the same book kept off Earth: the night side is near-black
  shot through with marine blue under a tiled starfield; the day side is
  sky blue and marine, the same two colours the other way round. Instrument
  cyan throughout, and a distant star where the ranch has a fire.

`STORYBOOK_THEME` sets the book's own pack — what everyone sees unless
they say otherwise. **Anyone can put a different one on their own screen**,
from the `◐` button in the nav: a plain tap still cycles light and dark,
and **holding it down** opens a small panel with the colour schemes and
the installed packs. (Right-click, or the down arrow on a keyboard, opens
it too; with JavaScript off it is an ordinary disclosure that opens on a
tap.) That choice is a cookie, so it dresses that one browser and nobody
else's, and it outlives logging out. Deleting the cookie, or clearing site
data, puts the book's own pack back.

The same panel is the only way to *un*-choose a colour scheme: **System**
forgets your pick and follows your phone or computer again.

If you decide the other pack *is* the book, set `STORYBOOK_THEME` to it
and restart: that's the setting every reader who hasn't chosen will get.

**A pack also decides which colour schemes it offers.** The ranch has all
three; orbit has two, because aged paper is the wrong world out there — its
`theme.json` says `{"schemes": ["dark", "light"]}` and the nav toggle simply
has one fewer stop. A reader who chose manuscript in a ranch book and then
opens an orbit one is never handed a scheme that pack didn't design; they
fall back to their system preference.

A pack is just a folder under `app/static/themes/<name>/`: a `theme.css`
re-declaring whichever colour variables it wants to change, an optional
`theme.json` (its name, the two or three colours the picker shows for it,
and the list of colour schemes it offers), and an `img/` folder of
pictures. Drop a folder in and it appears in the picker. **A pack only has to draw what it wants to change** —
anything missing falls back to the default pack's copy. That's what makes a
new art direction practical: the palette is a complete, working theme on
day one, and the ~35 illustrations and icons can arrive one at a time.

That's exactly where `orbit` is today: its colours and its seventeen
illustrations are finished, and it still borrows most of its icons from
`ranch` while its own get drawn — so a few buttons are visibly western in
an otherwise off-world book. `IMAGE-PROMPTS-ORBIT.md` is the catalogue of
what each remaining picture has to show.

#### Making one from inside the app

Hold the `◐` button and pick **Make a theme** (admins only — in accounts
mode it takes the admin role, and with a single shared password it's
whoever has the password). Then:

1. **Name it and describe the world** in a sentence or two — *"a Japanese
   woodblock print world: indigo, rust and off-white paper, strong
   outlines, flat colour, soft mist"*. That description is what keeps
   thirty-five separate drawings looking like one book. **Describe a way
   of drawing, not a place**: what it's drawn with, how it's lit, what the
   lines are like. A world named as a setting — *"a neon city at night"* —
   makes a generator draw the setting instead of the thing you asked for,
   thirty-five times. Your palette's hex codes are added to every prompt
   automatically, so you don't need to name colours here.
2. **Pick three colours per scheme** — a background, a text colour, an
   accent — and tick only the schemes your world actually has. The app
   derives the other dozen variables from those three. A **live preview**
   above the fields shows a miniature of the book in whatever you've typed
   so far — nav, timeline, a story title, the card a picture sits in —
   with a tab per scheme and the three contrast ratios the palette is held
   to underneath. It's the derived palette, not an impression of it: the
   same maths the server runs, so what you see is what saving will give
   you. A text colour that can't be read on its background says so before
   you save rather than after.
3. **Fill in the pictures at your own pace.** The Pictures page lists all
   35 with a ready-to-paste prompt for each: what the picture is *for* in
   this book, plus the rules that keep what comes back usable (no
   lettering, no watermark, no border; icons outlined so they survive on
   both a light and a dark page). Copy one, paste it into an image
   generator in another window, bring the picture back, upload it. Every
   picture you haven't done is borrowed from `ranch`, so the theme works
   from the moment its colours are saved.

Uploads are re-encoded, resized and — for icons — cut out of their
background automatically, so what a generator hands you is usually usable
as-is. **Do the first picture, look at it, then do the rest**: if it comes
back as a scene rather than a single object, or in colours you didn't
choose, the description is what to change.

**A theme you make lives in your data folder** (`stories/themes/<name>/`),
not in the app: an update can't delete it, and it travels in the backup zip
with everything else. It's a `theme.json` of colours plus a folder of
pictures — readable, and still yours if you ever stop using this app.

To make one by hand instead, copy `app/static/themes/orbit/theme.css` as a
starting point — it re-declares every variable a pack can, with comments on
why each one is there.

### In-app help

Everything above is written for whoever sets Veillée up. The family
actually reading and writing in it day to day gets its own **Help** page
(linked in the nav) instead — not a shorter version of this tour but a
**glossary**: one plain-language line per word the interface actually uses,
grouped into writing a memory, who can read a story, the cast and the
family tree, reading it back, photos and voice memos, family accounts, and
keeping it safe. It explains what a thing *is* and when you'd want it, and
never what a button does — an icon of a camera does not need a sentence
saying it takes photos.

The section on **who can read a story** only appears when accounts are on,
since without them there is nobody to keep a story from. It leads with a
picture of a group standing inside a rope circle with the rest of the
family outside it, because the scoping rule is easier to see than to read.

## Opening it to the internet

The app ships hardened for exposure (see the list below), but the honest
first question is whether you need to expose it at all. If the family can
install a VPN app, **a VPN (WireGuard, or Tailscale for the least setup)
is meaningfully safer than an open port**: the login page simply isn't
reachable by strangers, so there is nothing to probe, guess at, or
exploit. Most NAS units can run one. If relatives need plain-browser
access and a VPN is too much friction, expose it — but do all of the
following:

1. **HTTPS only.** Put a reverse proxy with a real certificate in front
   (Caddy and NAS reverse-proxy suites do Let's Encrypt automatically)
   and never forward port 80 to the app. Without this, the password and
   every photo travel readable by anyone on the path.
2. **Set `STORYBOOK_COOKIE_SECURE=1`** — marks the session cookie
   HTTPS-only and turns on HSTS.
3. **Set `STORYBOOK_TRUSTED_PROXIES=1`** (or however many proxies you
   run) so the brute-force lockout counts each visitor's real IP rather
   than lumping the whole internet together as the proxy's address.
4. **Use a long password.** The lockout (10 failed attempts per IP per
   15 minutes) makes online guessing slow, but the password's length is
   still the real wall. A passphrase of several random words is both
   strong and typeable on a phone. With several family members, consider
   `STORYBOOK_ACCOUNTS=1` so each person has their own credentials and
   one can be reset without re-keying everyone.
5. **Keep the host patched.** The app's dependencies are pinned; the OS,
   Docker, and reverse proxy on the NAS are yours to update. Enable the
   NAS's automatic security updates if it has them.
6. **Never expose the MCP server.** It is stdio-only by design and
   bypasses the web login; it must not be wrapped in anything
   network-reachable (see the MCP section's trust model).
7. **Keep an off-box backup** (below). Security includes still having
   the stories if the NAS is stolen, ransomed, or dies.

What the app itself already does: every page and API route requires
login; repeated failed logins are refused per-IP before any password
check runs; all state-changing requests carry CSRF tokens; the session
cookie is signed, `HttpOnly`, `SameSite=Lax`; a strict
`Content-Security-Policy` (no external hosts, no inline scripts) means
even HTML smuggled into a story cannot run script; responses carry
`nosniff`/`frame-ancestors 'none'`/`Referrer-Policy` headers; pages are
never written to disk caches and photos are cacheable by your browser
only, not by shared caches; uploads are size-limited, re-encoded through
Pillow, and written under validated names; account passwords are
salted+hashed; write-link tokens are 32 random bytes stored only as
hashes. No software can promise "unhackable" — but the remaining risk
concentrates almost entirely on the strength of the password and the
TLS in front, which are the two items above only you control.

## Backing up

**Back up the `stories/` folder. That is everything.** There is no database, no
other state to preserve. Copying that one directory (e.g. with `rsync`, a nightly
`tar`, or syncing it to cloud storage) is a complete backup. Restoring is just
putting the folder back. For a one-tap copy from the app itself, the timeline's
"Download everything (.zip)" link (`/export`) streams the same directory as a
zip file.

To restore one, "Import a backup" (`/import`, also linked from the timeline)
uploads that same zip back in. It's deliberately strict: the import only
succeeds if **none** of the zip's stories already exist in this app's
stories folder — any collision aborts the whole import with nothing written,
rather than risk silently overwriting newer edits.

People are the exception to that strictness, because they are not memories:
anyone in the zip whose folder is already here is skipped (the living one is
the newer truth) and the rest are restored alongside the stories. A theme
your family made comes back the same way, for the same reason — someone
described a world and generated pictures for it, so it is content, not
state; one already here is left alone rather than overwritten. Their
**logins are never restored** — a zip is a portable file, and restoring one
taken from another book would otherwise install its accounts, admins
included, into yours. After a disaster recovery an admin re-issues
invitations; that is the intended cost. This makes it a good fit
for disaster recovery (restoring into a fresh, empty install) or merging in
stories from a different device that don't already exist here; it is not a
sync tool. Very large backups may exceed the app's 128 MB upload limit — for
those, copy the zip's contents directly onto the `stories/` folder (or the
Docker volume) instead of going through the web UI.

## Running the tests

```bash
pip install -r requirements.txt
pytest
```

CI also runs `ruff check .` (a linter, config in `pyproject.toml`) — run it locally
before pushing if you want to catch the same issues early.

## Dependencies

Every runtime dependency, and why it's there. Kept short deliberately — see
"Philosophy" below for why the list stays this short.

Python (`requirements.txt`, versions pinned exactly):

| Package | Purpose |
|---|---|
| `flask` | The web framework. |
| `flask-wtf` | CSRF protection (`CSRFProtect`) — every unsafe-method request needs a valid token. |
| `python-frontmatter` | Reads/writes each story's/person's `index.md` as YAML frontmatter + markdown body. |
| `markdown` + `pymdown-extensions` | Renders a story's markdown body to HTML — `pymdownx.mark`/`caret`/`tilde` add `==highlight==`/`^ins^`/`~del~`, plus `smarty`, `tables`, `sane_lists`. |
| `pillow` | Re-encodes every uploaded photo (resize, thumbnail, EXIF-transpose) — an upload's bytes are never saved verbatim. |
| `pillow-heif` | Teaches Pillow to open HEIC/HEIF photos (iPhone originals) so they go through the same re-encoding path as any other format. |
| `waitress` | The production-style WSGI server for `python -m waitress-serve ...` (see "Locally (production-style, waitress)" above). |
| `mcp` | Optional: the MCP server (`mcp_server.py`, see below) that lets an AI assistant read/write stories and people. Not imported by the Flask app at all — only needed if you actually run `mcp_server.py`. |

Dev-only (`requirements.txt`'s `# dev` section): `pytest` (test runner),
`ruff` (linter, also run in CI).

No JavaScript build step and no `package.json` — the browser code is plain
`<script>` tags plus three vendored, pinned third-party bundles under
`app/static/vendor/` (each with its `LICENSE`, a `VENDORED.md` recording
version, provenance and no-network audit, and a licence banner in every file
served to a browser — `tests/test_vendored_licences.py` fails without all
three): the [Toast UI Editor](https://github.com/nhn/tui.editor) (3.2.2, the
WYSIWYG markdown editor), and
[family-chart](https://www.npmjs.com/package/family-chart) 0.9.0 +
[D3](https://d3js.org) 7.9.0 (the family tree renderer, F18). The JS test
files (`tests/js/*.mjs`) run directly via `node`, no test framework or
`node_modules` needed.

The app reproduces all of those notices at **`/licences`**, linked from the
Help page — the vendored bundles' licence text in full (read from the files
above at request time, so the page cannot drift from the repository), and the
server-side packages listed for transparency. Veillée itself is Apache-2.0.

## Philosophy

- The data outlives the app: plain markdown + image files, human-readable forever.
- Boring, minimal dependencies; no build step; no JS framework.
- No runtime network dependencies — everything needed to run is vendored or local.
- Mobile-first: every screen, especially the editor, is designed to be used from a
  phone.
- Book, not blog: no feeds, no reactions, no comment sections. Restraint and
  typography.

## A note on the editor

The real [Toast UI Editor](https://github.com/nhn/tui.editor) (3.2.2) is vendored
at `app/static/vendor/toastui/` — a standalone browser bundle built from the
official npm package with `esbuild`, since the upstream CDN's `-all` bundle isn't
published on npm. Rebuild instructions and provenance are in the banner comment
at the top of `toastui-editor-all.min.js`. Its usage-analytics ping (a request to
`google-analytics.com` on every load) is disabled via `usageStatistics: false` in
`editor.js` — do not remove that option, it would violate the no-external-requests
principle (see `PLAN.md` §2.3 and the acceptance checklist in §10).

If `window.toastui` isn't available for any reason (e.g. the vendored files are
replaced with placeholders again), `editor.js` automatically falls back to a
plain `<textarea>` with a minimal formatting toolbar (heading, bold, italic,
strikethrough, quote, lists, link, highlight, and image upload) covering the same
functionality.

Supported photo formats: JPEG, PNG, WebP, AVIF, GIF, TIFF, BMP, and HEIC/HEIF
(iPhone and Android originals, via `pillow-heif`) — everything except PNG is
re-encoded to JPEG on upload; PNG is kept as PNG. The uploaded file is never
kept, only the re-encoded copy.

## Ideas for later

Out of scope, deliberately: comments/reactions, RSS, email, video,
encryption at rest, offline support (no service worker — see "Home-screen
install" above), and story deletion. If any of these become worth doing,
they belong here first, not as a surprise addition.

Several things that were on this list have since shipped, and are described
above rather than here: PDF/print export (the book view), the photo
lightbox (F7), home-screen install (F9), multi-user accounts (F19, still
optional and off by default), search and tags, and a translated interface
(F38). The list is what the app has decided against, not what it hasn't got
round to.
