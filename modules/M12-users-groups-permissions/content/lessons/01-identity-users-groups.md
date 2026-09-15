# Lesson 1 — Identity: Users, Groups, UID & GID

> Module 12 · Unit 4 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 1 — Read the identity files](../labs/lab-01-identity-forensics.md)
> Up next: [Lesson 2 — Permissions: chmod & umask](02-permissions-chmod-umask.md)

---

## 1. Why multi-user is the ground truth

Your laptop pretends you're the only user. Servers don't pretend. A university
GPU box hosts professors, PhD students, MSc students, and service accounts —
*simultaneously*. Everything in this lesson exists to answer one question:

> **Who is allowed to do what, to which files, and how does the kernel know?**

For data science this isn't trivia — it's the difference between a shared dataset
server that works and one that leaks, between a Jupyter instance only you can
reach (M27) and one the whole internet can.

## 2. Users and the magic of numbers

A **user** is an identity the kernel tracks — and it tracks it as a **number**:

- **UID** (user ID): the kernel's actual key. Your name is a courtesy.
- **GID** (group ID): same idea for **groups** — named collections of users used
  to grant access to *sets* of people at once.

```console
$ id
uid=1000(dsstudent) gid=1000(dsstudent) groups=1000(dsstudent),27(sudo)
```

Read it fluently: your UID is 1000, your *primary* group is your own group
(1000), and you're *also* a member of group 27, named `sudo`. (Human users start
at 1000 by convention; system accounts live below — more below.)

**Primary vs supplementary groups:** every process runs with exactly one primary
GID (what new files get stamped with — M13 uses this hard), plus any number of
supplementary groups (which simply grant additional access).

## 3. The three identity files

### `/etc/passwd` — the account catalog (world-readable!)

One line per account, seven colon-separated fields:

```console
$ grep dsstudent /etc/passwd
dsstudent:x:1000:1000:DS Student,,,:/home/dsstudent:/bin/bash
```

| Field | Here | Meaning |
|---|---|---|
| username | `dsstudent` | login name |
| password | `x` | "look in /etc/shadow" (historical placeholder) |
| UID | `1000` | the kernel's number |
| GID | `1000` | primary group |
| GECOS | `DS Student,,,` | full name/comment (commas = legacy fields) |
| home | `/home/dsstudent` | where login lands |
| shell | `/bin/bash` | the shell started at login |

Note the system accounts while you're in there:

```console
$ head -5 /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
...
```

`root` is **UID 0** — the superuser (Lesson 4 of this unit is devoted to it).
Accounts with `/usr/sbin/nologin` shells can't log in interactively: they exist
to *own* services (M20's daemons), not to host humans. Low UIDs = system, 1000+
= humans, on Ubuntu.

### `/etc/shadow` — the password vault (root-only)

Hashed passwords and aging policy live here, deliberately separated from the
world-readable `passwd` so ordinary users can't even *attempt* offline hash
cracking:

```console
$ cat /etc/shadow
cat: /etc/shadow: Permission denied        # expected! you are not root
$ sudo grep dsstudent /etc/shadow          # (VM only — see M14's warnings)
dsstudent:$y$j9T$...hash...:20321:0:99999:7:::
```

Fields after the hash: last-change day, min/max age, warn days... password
*policy*, not just the hash. You will read this file exactly once in this
course (above) and otherwise respect it as root territory.

### `/etc/group` — the group catalog

```console
$ grep -E 'sudo|students' /etc/group
sudo:x:27:dsstudent
students:x:1500:dsstudent,ben,chen
```

`group:password:GID:members`. The `x` is a vestige (group passwords are
effectively dead). The members list is *supplementary* membership — your
primary group doesn't list you here. Notice how a shared-server design reads:
one `students` group, membership = access (M13 builds the whole pattern).

## 4. The account-management toolkit

All of these need root power (via `sudo` — Lesson 4 explains the discipline;
in your VM you have it). **Run these in your VM only, on throwaway users.**

### `useradd` / `adduser` — create an account

```console
$ sudo useradd -m -s /bin/bash ben        # low-level: -m makes home, -s sets shell
$ sudo adduser chen                       # Ubuntu's friendly wrapper: prompts for everything
```

Ubuntu gives you both: `useradd` (the portable primitive every Linux has) and
`adduser` (Debian-family convenience that also sets password, asks questions,
creates the home *with* skeleton files). Course habit: `adduser` interactively,
`useradd` in scripts where flags beat prompts.

### `passwd` — set/change passwords

```console
$ sudo passwd ben          # admin sets another user's password
$ passwd                   # a user changes their OWN (asks current password first)
```

The self-service form is the everyday one; it also enforces policy (length,
dictionary checks — `man passwd`).

### `usermod` — modify

```console
$ sudo usermod -aG students ben     # -aG: Append to supplementary Group (MEMORIZE)
$ sudo usermod -s /bin/zsh ben      # change shell (if zsh existed)
$ sudo usermod -L ben               # lock the account (prefixes the hash with !)
```

**The `-a` in `-aG` is load-bearing:** `usermod -G students ben` (without `-a`)
*replaces* all supplementary groups with just `students` — silently revoking
`sudo`. This one flag omission is a classic production incident.

### `userdel`, and the group triple

```console
$ sudo userdel -r ben            # -r removes home + mail spool too
$ sudo groupadd analysts         # create
$ sudo groupmod -n data-analysts analysts   # rename (-n new name)
$ sudo groupdel analysts         # delete (refuses if it's someone's primary)
```

## 5. Read-only identity commands (safe everywhere)

| Command | Answers | Example |
|---|---|---|
| `whoami` | my username | `dsstudent` |
| `id` | my numbers + all groups | above |
| `id ben` | *ben's* numbers (may query others) | |
| `groups` | my (or `groups ben`'s) group names | `dsstudent sudo` |
| `who` | who's logged in *right now*, from where | multi-user made visible |
| `w` | same + what they're doing | |

```console
$ who
dsstudent tty1         2026-09-15 20:40
ben     pts/0          2026-09-15 21:15 (10.0.2.2)
```

On a shared server, `who` is your situational awareness; `w` adds CPU-usage per
session — M18 will connect that to "who is slowing the box down?".

## 6. DS framing: identities on a research server

| Account type | Example | Lives as | Gets access via |
|---|---|---|---|
| Humans | prof, postdoc, PhD, MSc | UIDs ≥1000, real shells | groups (`lab`, `students`) |
| Service accounts | `jupyter`, `postgres`, `www-data` | `nologin` shells, low UIDs | own the service's files (M20/M29) |
| Robots/automation | CI runner, backup job | often `nologin` too | minimal group sets (least privilege, Lesson 3) |

The design reflexes being built: **humans in groups, services in nologin,
access granted to groups not individuals** (renames/departures then touch one
group, not twelve datasets — M13's whole architecture).

## Exercises (lab-log.md)

1. Decode your full `id` output field by field. Which of your groups is
   *primary*, and how can you tell from `id`?
2. `grep -E 'nologin|false' /etc/passwd | wc -l` — how many non-login accounts
   does your system carry? Name three and guess (then verify with `ps`) what
   each might own.
3. Read `/etc/group` and find the GID of your primary group. Cross-check with
   `id -g`.
4. In your VM: `sudo adduser testuser` (accept defaults, note the password
   prompt), then `id testuser`. Confirm the new UID; then `sudo userdel -r
   testuser` and prove removal. Log every command.
5. The `-aG` incident: in the VM, create `t2`, add it to a test group *without*
   `-a` after giving it a second group — what did `id t2` lose? (Then clean
   up.) One paragraph on why this belongs in every sysadmin's scar tissue.
6. `who` and `w` on your VM: how many sessions, from where? (WSL2 users:
   interpret your pts lines.)
7. Design: a 10-person research lab needs accounts for 8 humans, Jupyter as a
   service, and a nightly backup robot. Specify account *types* (shell? UID
   range? groups?) for each — no commands needed, just the identity plan.

## Check yourself before Lesson 2

- I can read all seven `/etc/passwd` fields and all three identity files' roles.
- I know UID 0 = root, humans ≥ 1000, `nologin` = service accounts.
- `-aG` is memorized, including the disaster its omission causes.
- `id`, `groups`, `who`, `w` are read-only and I use them for awareness.

## Further reading (official sources)

- Ubuntu Server docs: user management —
  <https://documentation.ubuntu.com/server/how-to/security/users/>
- `man 5 passwd`, `man 5 shadow`, `man 5 group`, `man 8 useradd`, `man 8 usermod`
- M13 builds today's primary-group stamping into the shared-directory pattern

Next: [Lesson 2 — Permissions: chmod & umask](02-permissions-chmod-umask.md)
