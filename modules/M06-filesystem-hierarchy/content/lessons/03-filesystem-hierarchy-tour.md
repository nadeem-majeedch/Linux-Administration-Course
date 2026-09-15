# Lesson 3 — The Filesystem Hierarchy Tour

> Module 06 · Unit 2 · Difficulty: Beginner
> Reading time: ~30 min · Lab: [Lab 2 — FHS scavenger hunt](../labs/lab-02-fhs-scavenger-hunt.md)
> Up next: [Lesson 4 — Creating your project layout](04-project-layout-mkdir-touch.md)

---

## 1. Why the tree is arranged this way

The layout is not arbitrary — it is a standard: the **Filesystem Hierarchy
Standard** (FHS). Each top-level directory has a *contract*: what belongs there,
who owns it, and whether it survives a reboot. You don't memorize the tree; you
learn the **three questions** each area answers:

1. **Who owns it?** (the system, or you?)
2. **What lives there?** (config? data? programs? transient junk?)
3. **Is it safe to touch?** (read-only for you? wiped on reboot? sacred?)

That third question is the safety frame for the whole course.

## 2. The map

```
/                 the root: everything begins here
├── bin   sbin    essential programs (bin), admin programs (sbin)  → usually symlinks into /usr
├── boot          kernel + bootloader files
├── dev           devices as files
├── etc           system-wide configuration (text!)
├── home          user home directories (/home/dsstudent)
├── lib  lib64    shared libraries
├── media  mnt    mounted drives: automounted (media), manual (mnt)
├── opt           optional/add-on software bundles
├── proc          kernel + process information (virtual)
├── root          root user's home (not / — people mix these up)
├── run           runtime state since boot (virtual, wiped)
├── srv           data for services (rarely used directly)
├── sys           kernel device/driver view (virtual)
├── tmp           scratch space, anyone may write, wiped on reboot
├── usr           the installed system: programs, libraries, docs
└── var           variable data: logs, spools, caches, databases
```

Ten of these you will *use* this course; the tour below goes deepest where your
work goes deepest.

## 3. The directories you'll live in or against

### `/home` — your territory

```console
$ ls /home
dsstudent
$ ls -a ~
.  ..  .bashrc  .profile  .ssh  data  projects  archive
```

One directory per user. Everything you create this course lives under yours.
*Who owns it:* you. *Safe to touch:* yes — your own home is your lab; the course's
few risky labs still happen inside VMs.

### `/etc` — the system's text memory

System-wide **configuration**, almost all plain text — which is why Modules 8–9's
text tools work on the operating system itself.

| File | What it configures | Used in |
|---|---|---|
| `/etc/os-release` | distro identity (you read it in M01) | M01, M02 |
| `/etc/hostname` | machine name | M01 |
| `/etc/passwd`, `/etc/group` | users and groups (not passwords!) | M12 |
| `/etc/fstab` | which filesystems mount at boot | M17 |
| `/etc/crontab` | system-wide schedule | M19 |

*Who owns it:* root. *Safe to touch:* **read yes, write no** — edits need sudo and
a reason; the course always edits with backups and a stated why (M14, M17).

### `/var` — the system's diary

"Variable" data — the stuff that *changes while the system runs*:

```console
$ ls /var/log
alternatives.log  apt/  boot.log  btmp  journal/  syslog  ...
```

`/var/log` is where logs accumulate: your future troubleshooting life happens here
and in the journal (Module 24). Other `/var` residents: package caches
(`/var/cache/apt`), mail spools, database files (PostgreSQL defaults under
`/var/lib/postgresql` — M29). *Safe to touch:* read your own logs; never hand-edit
logs (that's evidence tampering, in every sense).

### `/tmp` — the world's whiteboard

Scratch space every user (and every program) may write; **typically wiped on
reboot**; often size-limited (it may live in RAM).

| Use | OK? |
|---|---|
| Intermediate files a script needs for minutes | ✅ its job |
| Anything you want tomorrow | ❌ it may not survive the night |
| Anything secret | ❌ world-writable by design (sticky bit — M12) |

Module 11's scripts use `mktemp` — which makes safe, private names *inside* /tmp —
rather than hoping their filename is unique.

### `/usr` — the installed system

The bulk of the software: programs in `/usr/bin`, libraries in `/usr/lib`,
docs in `/usr/share/doc`. You already tab-completed through it in Lesson 1.
*Who owns it:* the package manager (apt, M16). *Safe to touch:* **no** — this is
apt's territory; hand-edits here get clobbered or break packages.

> **The `/bin` merge, de-mystified:** on modern Ubuntu, `/bin`, `/sbin`, `/lib`
> are **symbolic links** into `/usr` (check: `ls -ld /bin` shows
> `bin -> usr/bin`). Historically `/bin` held the minimal tools needed at boot;
> the modern layout merged them. Know both spellings — old documentation uses
> `/bin` freely — and know that `which ls` answering `/usr/bin/ls` is normal.

### `/opt` — the guest room

Self-contained third-party software bundles, one directory per product
(`/opt/google/chrome`, `/opt/teamviewer`). Unlike `/usr`, nothing owns `/opt`
but the packages that install themselves there (often `.deb` vendors or
things you install by hand — M16's "outside apt" path). *Safe to touch:* no,
unless *you* installed it.

### `/dev` — devices as files

"Everything is a file" made literal: disks (`/dev/sda`), partitions
(`/dev/sda1`), terminals (`/dev/tty`), random numbers (`/dev/random`,
`/dev/urandom`), and the two you'll use in M09: `/dev/null` (the discard) and
`/dev/zero`. *Safe to touch:* **look with your eyes, never with commands that
write** — `cat /dev/sda` is harmless-ish reading; `dd`-ing onto a device node
(M17) is how disks get erased.

### `/proc` — the kernel's window

Virtual: no disk behind it; the kernel *generates* content as you read.
`/proc/cpuinfo`, `/proc/meminfo` (M01), one directory per running process
(`/proc/<pid>/` — M18). *Safe to touch:* reading is always safe; some files
accept writes to tune kernel behavior — far beyond today.

### `/sys` — the kernel's device control panel

Also virtual: the structured view of devices, drivers, buses — the modern
successor to chunks of `/proc`. M03/M17 peek here (`ls /sys/block`). *Safe to
touch:* read freely; writing is kernel-tuning territory.

### `/run` — since-boot state

PID files, sockets, locks — things daemons create at startup and that lose
meaning at shutdown (wiped on boot). You'll meet it reading `systemd` state
(M20). *Safe to touch:* hands off; it belongs to the system's runtime.

## 4. Who owns what — the one table to keep

| Area | Owner-in-chief | You may… | You may not… |
|---|---|---|---|
| `/home/you` | you | do anything | — |
| `/tmp` | everyone | write scratch | expect it to survive, store secrets |
| `/etc`, `/usr`, `/opt`, `/bin`, `/sbin` | root / apt | read | write without sudo+reason |
| `/var/log` | root (+journald) | read (mostly) | edit, delete |
| `/dev`, `/proc`, `/sys`, `/run` | kernel | read | write (M17/M18 caveats later) |

This table *is* the permission system's daily shape (M12 formalizes the how).

## 5. `tree`: seeing structure without walking it

`tree` draws a directory as the diagram it is (install once with apt — M16:
`sudo apt install tree`):

```console
$ tree ~/projects/eds-01
/home/dsstudent/projects/eds-01
├── data
│   ├── raw
│   └── processed
├── logs
└── README.md

4 directories, 1 file
```

Useful flags: `-L 2` (depth limit — tour the top two levels, not the abyss),
`-a` (include hidden), `-d` (directories only). For datasets with hundreds of
files, `tree -L 2` is the honest picture; bare `tree` on `/usr` is a firehose.

## 6. Data Science mapping: where your things *would* live on a real server

| On your VM (this course) | On a shared lab/GPU server | Why the difference matters |
|---|---|---|
| `~/data` | `/data` or `/srv/datasets` (group-writable, M13) | shared datasets are admin-managed territory |
| `~/projects` | `~/projects` (yours alone) | code stays personal; clusters *are* multi-user (M12) |
| `/tmp` for scratch | `/tmp` or `/scratch` (wiped, don't trust) | never park results there — M24's backups don't cover it |
| results in `~/archive` | group results under `/data/projects/<team>` | shared science needs shared, permissioned space |

The habit being built: **put things where their contract says they belong**, and
you can predict what survives reboots, who else can read it, and what gets backed
up — before anything goes wrong.

## Exercises (lab-log.md)

1. `ls /` — compare against the Lesson-2 map. Name three directories present on
   your system that were *not* in the map (e.g., `snap`, `lost+found`), and
   `ls -ld` them to guess their story.
2. Verify the `/bin` merge: `ls -ld /bin /sbin` — what do the arrows say?
3. Which directory would hold: (a) the config for the SSH server, (b) a database's
   files, (c) a USB stick you just plugged in, (d) the kernel's live view of your
   CPUs, (e) a script's two-minute intermediate file? Answers from the map only,
   then verify two with `ls`.
4. `ls -ld /tmp /var/tmp /run` — all three are "system scratch-ish". Using the
   first field (type+permissions) and the map, state in one line each: who may
   write it, and what its relationship to *reboot* is.
5. `tree -L 2 ~/projects` (or `tree -L 2 /usr/share/doc | head -30`). What does
   the depth limit save you from?
6. A teammate proposes storing nightly results in `/tmp` "because it's big".
   Give the two-line objection from this lesson.
7. Using the map only: which areas does `sudo apt upgrade` (M16) most likely
   write? Which does a matplotlib plot under your home write? Why the asymmetry?

## Check yourself before Lesson 4

- I can name the contract of /etc, /var, /tmp, /usr, /opt, /dev, /proc, /sys,
  /run, /home in one line each.
- I can state, for any top-level dir: who owns it and whether it survives reboot.
- I know /bin is a symlink into /usr on modern Ubuntu — and why old docs say /bin.
- I can draw a 3-level `tree` of my own home convention.

## Further reading (official sources)

- Filesystem Hierarchy Standard 3.0 —
  <https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html>
- Ubuntu Server docs: storage/log layout references —
  <https://documentation.ubuntu.com/server/>
- `man hier` — the hierarchy, from your own machine

Next: [Lesson 4 — Creating your project layout](04-project-layout-mkdir-touch.md)
