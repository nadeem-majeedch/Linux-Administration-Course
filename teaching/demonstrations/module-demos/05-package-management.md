# Demo 5 — Package Management: The Dependency Negotiation

> **Session:** S15 · **Duration:** ~8 min · **Risk:** low (VM, snapshot
> taken) · **Objective:** make `apt` visible as a *trust-and-dependency
* engine*, not an app store — students read its negotiation like text.

## Prerequisites

- Demo VM, **snapshot taken** (`pre-apt-demo`)
- Network working (apt update succeeds) — have `--dry-run` ready as the
  offline fallback

## Setup (20 seconds)

```console
$ sudo apt update          # the catalogue refresh — narrate the URI hits
$ apt show htop | head     # what the catalogue knows about it
```

## Procedure

**Step 1 — the dry-run rehearsal (course reflex from day one).**

```console
$ sudo apt install --dry-run htop
```

*Narration:* read the output as three parts: **The following NEW
packages will be installed** (the negotiation result), **Need to get**
(the bytes), **After this operation** (the footprint). "We just
simulated the install. Nothing changed. This reflex returns with
rsync's `--dry-run` — same discipline, different domain."

**Step 2 — the real thing, read like a story.**

```console
$ sudo apt install -y htop
Reading package lists... Done
Building dependency tree... Done
The following additional packages will be installed:
  libnl-3-200 libnl-genl-3-200 ...
The following NEW packages will be installed:
  htop libnl-3-200 ...
```

*Narration:* "htop asked for friends. apt resolved *which versions*,
*where* they come from (the repo we trust), and only then touched the
system. `dpkg -i` alone skips this entire negotiation — that's why it's
the manual override, not the path."

**Step 3 — provenance: who vouches for this?**

```console
$ apt policy htop
```

*Narration:* read the candidate line + the repo URL — "the signature on
the package traces to the repository's key; that's what `apt update`
was *checking* when it hit those URIs."

**Step 4 — removal, and what it leaves.**

```console
$ sudo apt remove -y htop && apt show htop 2>/dev/null | head -3
$ sudo apt purge -y htop         # remove + config
$ sudo apt autoremove -y         # the orphaned friends go home
```

*Narration:* "remove leaves config (a reinstall keeps your settings);
purge forgets everything; autoremove tidies the friends nobody needs
now. Three verbs, three levels of forgetting."

## Expected output

Package/version strings vary by release — say so and read *shapes*, not
exact numbers (evidence over memorization, modeled).

## Questions to ask

1. Before step 1: "what will `--dry-run` change on this system?"
   (nothing — and *why* the reflex matters)
2. After step 2: "why did installing one small tool pull five
   packages?" (libraries are shared; the dependency tree is the point)
3. "You ran `upgrade` without `update` — what did you get?" (a stale
   catalogue's idea of current)

## Common errors & recovery

- Another apt is running (`Could not get lock /var/lib/dpkg/lock-frontend`)
  — someone's unattended-upgrades woke up; wait, or diagnose `fuser
  /var/lib/dpkg/lock-frontend`. A teachable moment: locks protect the
  database.
- `apt update` signature warning — *never* bypass on stage; narrate it
  as the trust model working, then fix from the module's repo section.

## Recovery

Snapshot `pre-apt-demo` restores a pristine state; autoremove in step 4
normally suffices.

## Cleanup (census)

```console
$ which htop || echo "htop gone"
$ apt list --installed 2>/dev/null | grep -c htop   # 0
```

## Optional extension

`aptdepends`-style tree view: `apt rdepends htop | head` (who *depends
on* it) — the reverse edge of the dependency graph, reading level.
