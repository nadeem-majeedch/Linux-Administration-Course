# Lesson 1 — Packages, dpkg & apt: the Fundamentals

> Module 16 · Unit 5 · Difficulty: Beginner-Intermediate
> Reading time: ~35 min · Lab: [Lab 1 — package explorer](../labs/lab-01-package-explorer.md)
> Up next: [Lesson 2 — repositories, security & PPAs](02-repositories-security-ppas.md)

> 🔒 Safety: everything in this lesson is safe on your own VM. The two
> commands that *change* anything (`apt install`, `apt remove`) are
> introduced with the check-first workflow (§4) — and every lab command is
> previewed before it's run. Nothing here needs root until §5, and nothing
> is destructive when the workflow is followed.

---

## 1. The problem packages solve

Installing software by hand means: download, extract, put binaries on
PATH, libraries somewhere findable, man pages in the right section, config
in /etc — and then *repeat all bookkeeping on every update and removal*.
A **package** bundles a program with its files, metadata, and
**dependencies** (what else must be present), and the **package manager**
automates install, upgrade, removal, and dependency resolution from a
curated, signed **repository**.

The layered vocabulary for Debian/Ubuntu (memorize these three roles):

| Layer | Tool | Role |
|---|---|---|
| **repository** | (a server + metadata) | thousands of packages, kept current and *signed* |
| **apt** | `apt`, `apt-get`, `apt-cache` | high level: finds packages, resolves dependencies, downloads, orchestrates |
| **dpkg** | `dpkg` | low level: actually installs/removes `.deb` files, owns the database of what's on disk |

apt *uses* dpkg; dpkg never talks to the network. When something breaks
mid-install, knowing which layer failed is the diagnosis (Lesson 2, Lab 3).

### DS framing

Every data science tool you'll touch this term — `python3`, `jupyter`,
`git`, `build-essential`, GPU drivers — arrives through this system (or a
language-level cousin like pip/conda; Lesson 3 maps who owns what). The
course rule: **system libraries via apt, language packages via
pip/conda** — that division is the difference between a maintainable
machine and a broken one.

---

## 2. dpkg: the database under everything

`dpkg` answers "what is installed, and what does it own?"

```console
$ dpkg -l | head -3                                  # inventory
Desired=Unknown/Install/Remove/Purge/Hold
| Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-instig/Err?=(none)/Reinst-required
ii  adduser          3.137ubuntu1   all    add and remove users...
```

The `ii` prefix: desired=install, status=installed. Other codes
(`iU`, `iF`, `rc`) indicate *unfinished business* — `dpkg -l | grep -v "^ii"`
is the "anything broken?" census.

```console
$ dpkg -l git                    # is a specific package installed?
$ dpkg -L curl                   # which FILES did curl install?
$ dpkg -S /usr/bin/curl          # which package owns this file? (reverse lookup)
$ dpkg -s curl                   # status/detail incl. dependencies
```

`dpkg -S` is the everyday superpower: "which package provides this
missing library?" Also: `dpkg --get-selections` (machine-readable
inventory) and `dpkg --audit` (half-installed packages).

You can technically `sudo dpkg -i file.deb`, but it does **no dependency
resolution** — for anything with deps you get errors. The right command
for a local .deb is `sudo apt install ./file.deb` (note the `./`), which
resolves deps from configured repos. dpkg stays a *query* tool in
practice.

---

## 3. apt: finding, understanding, and installing

**The three search/info commands (all safe, no sudo):**

```console
$ apt search "json parser" | head        # name+description match
$ apt show jq                            # details: version, deps, size, description
$ apt list --installed | grep -i python  # installed inventory via apt
$ apt list --upgradable                  # what updates are pending
```

Reading `apt show` output like a professional:

```text
Package: jq
Version: 1.7.1-3build1
Depends: libc6, libjq1, libonig5
Download-Size: 66.0 kB
```

- `Depends:` — apt will install these too; this is the tree you accept
  when you accept a package.
- `Download-Size` + Installed-Size — the disk bill.

**The lifecycle verbs (sudo required, each explained):**

```console
$ sudo apt update                 # refresh package LISTS from repos (no installs!)
$ sudo apt upgrade                # upgrade installed pkgs within current versions
$ sudo apt install jq             # install (and its dependencies)
$ sudo apt remove jq              # uninstall, LEAVES config files
$ sudo apt purge jq               # uninstall + config files (clean removal)
$ sudo apt autoremove             # remove now-orphaned dependencies
```

**`update` vs `upgrade` — the classic confusion:** `update` only refreshes
apt's *catalog* (the lists in `/var/lib/apt/lists/`); `upgrade` does the
actual installing. `apt install` on a stale catalog is why you sometimes
get "Unable to locate package" for software you know exists → fix:
`sudo apt update` first. Make `update && upgrade` one reflex.

**`remove` vs `purge`:** remove keeps `/etc` config (nice when
reinstalling); purge deletes it. Neither touches *user data* in `/home` —
which is why "purge my database package" ≠ "delete my database files":
data dirs (e.g. `/var/lib/postgresql`) survive both, deliberately
(covered again in M29).

**No `apt update` every time you search:** search/show/read work off the
existing lists; daily `update` is plenty.

---

## 4. The check-first install workflow (course standard)

Root + install = one of the safest *reversible* operations on Linux —
*if* you read before you press Y. The five-beat standard:

```console
$ apt search <thing>              # 1. exact name? (guessing names = installing typos)
$ apt show <thing>                # 2. right software? deps acceptable? source? size?
$ sudo apt update                 # 3. fresh catalog
$ sudo apt install <thing>        # 4. READ the summary line:
                                  #    "The following NEW packages will be installed"
$ dpkg -l <thing> && which <thing> # 5. verify, learn where it landed
```

Step 4 is where discipline pays: if a tiny utility wants to drag in 200
MB across 40 packages, that's legal but worth a blink — and if it says
"The following packages will be **REMOVED**", stop and read twice
(removals during an install are almost always a dependency conflict you
want to understand, not accept blind).

Undo is the same system: `sudo apt remove <thing> ; sudo apt autoremove`.

---

## 5. The package cache & where software lands

Downloaded .debs live in `/var/cache/apt/archives/` (safe to clean:
`sudo apt clean`); package *lists* in `/var/lib/apt/lists/`; dpkg's
database in `/var/lib/dpkg/` (never hand-edit — [M06's FHS tour](../../../M06-filesystem-hierarchy/content/lessons/03-filesystem-hierarchy-tour.md)
maps all of these).

Typical install layout (why FHS matters — everything is *predictable*):

```text
/usr/bin/jq          the program
/usr/share/man/...   man pages
/etc/                config (if any)
/usr/share/doc/jq/   changelog, copyright
```

---

## 6. Dependency management: what apt does for you

Two classes of relationships make apt powerful:

- **Depends** — must be present; apt installs them automatically.
- **Recommends/Suggests** — optional extras. Ubuntu installs Recommends
  by default; `sudo apt install --no-install-recommends <pkg>` skips them
  (slimmer containers — Lesson 3, Docker notes in M28).

And the failure mode apt prevents: **dependency hell** — A needs libX
1.2, B needs libX 1.4, one library, two incompatible demands. Debian's
answer: strict versioned dependencies, shared-source libraries, and a
resolver that either finds a consistent set or refuses. When it refuses,
you get the famous fragments:

```text
The following packages have unmet dependencies:
 packageA : Depends: libX (>= 1.4) but 1.2 is to be installed
E: Unable to correct problems, you have held broken packages.
```

First aid, in order: `sudo apt update` → `sudo apt install -f` (fix
broken) → `sudo dpkg --configure -a` (finish half-configured) → check for
a held package (`apt-mark showhold`). Deep dives: [troubleshooting.md](../troubleshooting.md)
#1–3.

---

## Exercises (lab-log.md)

1. Use `dpkg -S` on `/bin/ls` and `/usr/bin/python3`. Which packages own
   them? Then `dpkg -L <owner>` for python3 — name two *kinds* of paths in
   the list.
2. `apt search editor`, then `apt show nano`. Record version, size,
   dependency count. Why does nano need zero non-core deps?
3. Without installing anything: `apt list --upgradable | wc -l` on your
   VM. How many pending? (This number is your machine's "security
   debt" — Lesson 2.)
4. Explain `update` vs `upgrade` in one sentence each, then predict: what
   does `sudo apt upgrade` do after `sudo apt update` reports "All
   packages are up to date"? (Nothing — why is that the *expected*
   outcome, not a bug?)
5. Why does `sudo dpkg -i someapp.deb` fail on anything non-trivial,
   while `sudo apt install ./someapp.deb` works? (One sentence, precise.)
6. Run the §4 workflow *through step 3 only* for a package you actually
   want (suggest: `tree` or `htop`). What did `apt show` reveal that the
   package name alone didn't?

## Check yourself before Lesson 2

- [ ] I can answer: is it installed? what owns this file? what does this
      package need?
- [ ] I never install before `apt show`; I read the NEW/REMOVED summary.
- [ ] I know remove vs purge vs autoremove, and that /home is never
      touched by any of them.
- [ ] update ≠ upgrade, and I know which error means "stale lists."

## Further reading (official sources)

- `man apt`, `man dpkg`, `man sources.list`
- Debian apt HOWTO (upstream of Ubuntu's system): https://www.debian.org/doc/manuals/apt-howto/
- Ubuntu Server Docs — package management: https://ubuntu.com/server/docs
