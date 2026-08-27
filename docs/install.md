# Installing Veillée

This page assumes you can copy a command into a terminal and follow it with
your eyes. It does not assume you know Docker, Python, or what a reverse
proxy is.

Veillée runs on **your own machine**. There is no account to make, no
company to sign up with, and nothing to pay. The photographs stay on a disk
you own.

- [What you need](#what-you-need)
- [Install it](#install-it)
- [First start: claiming the book](#first-start-claiming-the-book)
- [Reaching it from other houses](#reaching-it-from-other-houses)
- [The router problem, honestly](#the-router-problem-honestly)
- [Backups](#backups)
- [Updating](#updating)
- [When something is wrong](#when-something-is-wrong)

---

## What you need

**A computer that stays switched on.** That is genuinely the only
requirement, and it is the one worth thinking about, because the book is
only readable while that machine is awake.

| | Good for | Watch out for |
|---|---|---|
| **Raspberry Pi** (4 or newer) | Cheapest. Silent, tiny, ~3W. | SD cards die without warning — use an SSD, and read [Backups](#backups). |
| **A NAS** (Synology, QNAP…) | Already on, already has disks and redundancy. | Its own web interface usually occupies the ports HTTPS needs. See the note below. |
| **An old laptop** | Free. Has a battery, which is a small UPS. | Set it to *not* sleep when the lid closes. |
| **A small VPS** (Hetzner, Scaleway…) | Always on, real HTTPS with no router fiddling, reachable from anywhere. | A few euros a month, and the photographs sit on someone else's disk. |
| **Your own Mac or Windows PC** | Nothing new to buy. | The book is readable only while that computer is awake, which usually means "sometimes". Fine for trying it out. |

You also need **Docker**. On a Pi, a VPS or a laptop running Linux:

```bash
curl -fsSL https://get.docker.com | sh
```

On a Mac or Windows PC, install **Docker Desktop** from docker.com. On a
Synology or QNAP, install **Container Manager** (or **Container Station**)
from the built-in package centre.

---

## Install it

Make a folder for the book and go into it:

```bash
mkdir veillee && cd veillee
```

Then, for a book on your home network:

```bash
docker run -d --name veillee \
  --restart unless-stopped \
  -p 5011:5011 \
  -v "$PWD/stories:/data/stories" \
  ghcr.io/choupatate/veillee:latest
```

That is the whole installation. Open `http://<the machine's address>:5011`
in a browser — on the machine itself, `http://localhost:5011`.

> **`-v "$PWD/stories:/data/stories"` is the important part.** It is what
> makes the `stories` folder next to you *be* the book. Everything Veillée
> keeps is in there as ordinary files: a folder per story, with a markdown
> file and the photographs. Delete Veillée entirely and that folder is
> still perfectly readable with a file browser and a text editor. That is
> the point of the whole design.

If you want it on your own domain with a real certificate, skip the command
above and use [Reaching it from other houses](#reaching-it-from-other-houses)
instead.

---

## First start: claiming the book

Look at what the book printed when it started:

```bash
docker logs veillee
```

You will see this:

```
┌─────────────────────────────────────────────┐
│  This book is waiting to be claimed.        │
│  Open it in a browser and enter this code:  │
│                                             │
│      K7QP-3MRW-92XD                         │
└─────────────────────────────────────────────┘
```

Open the book in a browser. It will ask for that code and for a password.
Type them, and the book is yours: it asks four questions about what it is
called and who it is for, and then gets out of the way.

**Why a code?** Because from the moment the book starts, anyone who can
reach it could otherwise claim it first. That code exists only in the logs
of your own machine, so only somebody sitting at it can. It stops existing
the second you use it, and there is no way to ask for another — if you lose
it before claiming, stop the container, delete the `claim_code` file in
your `stories` folder, and start it again.

The password you choose is the one your whole family will use to read the
book. You can give relatives their own logins later, from **Accounts** in
the menu, and decide which stories each of them can see.

---

## Reaching it from other houses

So far the book is readable at home. To let a grandmother read it from her
own sofa, it needs a name on the internet and a certificate.

**You need a domain name.** Any registrar, a few euros a year. Then point a
record at your home:

| Record | Name | Value |
|---|---|---|
| `A` | `livre.example.com` | your home's public IP address |

Find your public IP with `curl -4 ifconfig.me`. If it changes from time to
time — most home connections — see [the router problem](#the-router-problem-honestly)
below, which is the section that decides whether any of this can work at
all. **Read it before buying a domain.**

Then, in your `veillee` folder, fetch the two files that run it behind a
web server:

```bash
curl -O https://raw.githubusercontent.com/Choupatate/veillee/main/compose.https.yml
curl -O https://raw.githubusercontent.com/Choupatate/veillee/main/Caddyfile
echo "DOMAIN=livre.example.com" > .env
echo "EMAIL=you@example.com"   >> .env
docker compose -f compose.https.yml up -d
```

That is all. Caddy gets a real Let's Encrypt certificate for your domain by
itself, renews it forever, and sends anyone who types `http://` to `https://`.
Your claim code is in `docker compose -f compose.https.yml logs veillee`.

The `EMAIL` line is optional and worth setting: it is the only warning you
would ever get if renewal broke.

> **On a NAS**, this usually will not work as written, because the NAS's own
> web interface is already using ports 80 and 443. Use your NAS's own
> reverse-proxy panel instead (Synology: *Control Panel → Login Portal →
> Advanced → Reverse Proxy*), point it at port 5011, and set
> `STORYBOOK_COOKIE_SECURE=1` and `STORYBOOK_TRUSTED_PROXIES=1` on the
> container. Both matter: the first keeps the login cookie off plain HTTP,
> and the second lets the book see each visitor's real address, without
> which one person guessing passwords locks out everybody.

---

## The router problem, honestly

Your home router has to be told to send visitors to the machine running the
book. That is a **port forward**: ports 80 and 443 to the machine's local
address. Every router's menus are different; look for "Port forwarding",
"Virtual server", or "NAT".

**But first, check that it can work at all.** Many internet providers —
especially on fibre and on 4G/5G home broadband — put their customers
behind something called **CGNAT**, where you do not have a public address of
your own. No port forward can ever work in that situation. It is not
something you can configure your way out of, and there is nothing you did
wrong.

**The two-minute check:**

1. Find what the internet sees:

   ```bash
   curl -4 ifconfig.me
   ```

2. Log into your router and find its **WAN** or **Internet** IP address.

3. Compare them.

   - **The same** → you have a public address. Port forwarding will work.
   - **Different** → you are behind CGNAT (or a second router). Port
     forwarding will not work.
   - The router's WAN address starts with `100.64.` to `100.127.` → that is
     CGNAT, definitively.

**If you are behind CGNAT**, you have three real options:

- **Run the book on a small VPS instead.** A few euros a month, it has a
  public address, and everything on this page works with no router
  involved. The trade is that the photographs live on a rented disk.
- **Ask your provider for a public IP.** Many will, sometimes free,
  sometimes for a small monthly amount. Ask for "une adresse IP publique"
  or "a public IPv4 address".
- **Use a VPN instead of a domain.** [Tailscale](https://tailscale.com) is
  the least work: install it on the machine and on each relative's phone,
  and the book is reachable at a private address with no ports opened
  anywhere. This is the *safest* option in the list — strangers cannot
  reach the login page at all — at the cost of every relative installing an
  app.

**Dynamic addresses.** Even with a public IP, most home connections change
it every so often, which breaks your domain record until you update it. Fix
it with a dynamic-DNS updater — many routers have one built in, and most
registrars support it. Set the record's TTL low (300 seconds) so a change
propagates quickly.

**One thing to know before you open a port.** Once the book is on the open
internet, strangers will find the login page — not because they are after
you, but because everything on the internet gets scanned within hours.
Veillée is built for that: passwords are hashed with scrypt, repeated
guesses are locked out per address, the session cookie is `Secure` and
`HttpOnly`, and a fresh book cannot be claimed without a code from your own
logs. It is still a decision worth making deliberately, and a VPN avoids
having to make it.

---

## Backups

**The `stories` folder is everything.** Copy it somewhere else — an external
drive, another computer, a cloud drive if you accept that trade — and you
have a complete backup that will still be readable in twenty years without
Veillée or anything else.

From inside the book, **Download everything (.zip)** does the same thing in
one tap, and **Import a backup** puts one back.

The book will remind you: when writing has piled up for six months without
ever being copied anywhere, a line appears on the timeline. It stays quiet
when there is nothing new to lose.

Do this. A Raspberry Pi's SD card fails with no warning at all, and the
whole point of this project is a book someone reads in fifteen years.

---

## Updating

```bash
docker compose -f compose.https.yml pull
docker compose -f compose.https.yml up -d
```

or, for the plain `docker run` install:

```bash
docker pull ghcr.io/choupatate/veillee:latest
docker rm -f veillee
# then the same `docker run` command as before
```

Your stories, your settings and your logins are in the `stories` folder, not
in the container, so nothing is lost by replacing it. Everyone stays logged
in, because the signing key lives in that folder too.

To pin a version instead of following the latest, use a tag:
`ghcr.io/choupatate/veillee:1.2.3`. The version you are running is at the
bottom of the **Licences** page in the menu.

---

## When something is wrong

**The page will not load.** Is the container running? `docker ps` should
list `veillee`. If not, `docker logs veillee` will say why.

**"This book is waiting to be claimed" but I already claimed it.** You are
almost certainly running against a different folder than last time — check
that the `-v` path in your command is the folder you mean.

**Everyone got logged out after an update.** The signing key is missing,
which means the `stories` folder was not mounted. The book refuses to start
without somewhere to keep that key, so check the `-v` line.

**HTTPS is not working.** `docker compose -f compose.https.yml logs caddy`
will say exactly what Let's Encrypt refused and why. The usual answer is
that the domain does not yet point at you, or port 80 is not reaching the
machine — Let's Encrypt needs it, even though the book itself only uses 443.

**I lost the claim code.** Stop the container, delete `claim_code` from the
`stories` folder, start it again, and read the new one from the logs.

**I forgot the book's password.** Stop the container, delete
`book_password.json` from the `stories` folder, and start it again — the
book becomes unclaimed and prints a fresh code. Your stories are untouched.
