# Demo 3 — Users & Groups: The Shared Folder

> **Session:** S11 (after demo 2) · **Duration:** ~10 min · **Risk:**
> low — VM, staged users, planned-failure choreography · **Objective:**
> show *why* SGID and sticky exist by letting the failure happen first.

## Prerequisites

- Staged demo users (see Setup) — **never use real student accounts**
- Snapshot taken before the demo (named `pre-shared`)

## Setup (before class — two fake teammates)

```console
$ sudo useradd -m -s /bin/bash alice
$ sudo useradd -m -s /bin/bash bob
$ sudo groupadd project
$ sudo usermod -aG project alice
$ sudo usermod -aG project bob
$ mkdir -p /srv/demo-shared && sudo chgrp project /srv/demo-shared
$ sudo chmod 770 /srv/demo-shared
```

*(If sudo rules block user creation on the room's image, run the whole
demo inside your instructor VM — nothing here needs student machines.)*

## Procedure

**Step 1 — alice writes.**

```console
$ sudo -u alice bash -c 'echo alice-work > /srv/demo-shared/a.txt'
$ ls -l /srv/demo-shared/a.txt
-rw-r--r-- 1 alice alice 11 Sep 17 10:30 a.txt
```

*Narration:* "Group is `alice` — the *project* never got it. Tomorrow
bob can't collaborate; in six months the tree is a mess of personal
groups."

**Step 2 — the planned failure: bob can't help.**

```console
$ sudo -u bob bash -c 'echo edit >> /srv/demo-shared/a.txt'
bash: /srv/demo-shared/a.txt: Permission denied
```

*Narration:* "Same folder, both in the group — and still broken. The
design is missing something."

**Step 3 — the one-digit fix: SGID.**

```console
$ sudo chmod 2770 /srv/demo-shared
$ sudo -u alice bash -c 'echo alice-work2 > /srv/demo-shared/b.txt'
$ ls -l /srv/demo-shared/b.txt
-rw-r--r-- 1 alice project 12 Sep 17 10:31 b.txt
```

*Narration:* "Group `project` *inherited*. New files belong to the
team. The `2` did that."

**Step 4 — the second failure: alice deletes bob's work.**

```console
$ sudo -u bob  bash -c 'echo bobs-data > /srv/demo-shared/c.txt'
$ sudo -u alice bash -c 'rm /srv/demo-shared/c.txt'     # 770 lets her!
$ sudo -u alice bash -c 'ls /srv/demo-shared'           # c.txt is gone
```

**Step 5 — the sticky digit.**

```console
$ sudo chmod 1770 /srv/demo-shared
$ sudo -u bob  bash -c 'echo again > /srv/demo-shared/c.txt'
$ sudo -u alice bash -c 'rm /srv/demo-shared/c.txt'
rm: cannot remove '/srv/demo-shared/c.txt': Operation not permitted
```

*Narration:* "Write access lets alice *edit* bob's file. The sticky bit
says deletion belongs to the *file's owner* — teammates protected from
each other. That's `/tmp`'s design on every Linux box you'll touch."

## Expected output

As shown; usernames/timestamps vary.

## Questions to ask

1. Between step 1 and 2: "alice and bob are both in `project` — why
   did the group come out wrong?"
2. After step 4: "which single digit fixes this — and what does it
   cost?" (7770-style aside: sticky is orthogonal, not a trade)
3. "Where have you *met* the sticky bit already?" (`/tmp` — `ls -ld
   /tmp` shows the `t`)

## Common errors & recovery

- `useradd` missing flags (no `-m`) → no home dir; harmless here, note
  it
- Group membership needs **re-login** for the user to activate it —
  `sudo -u` sidesteps this in the demo; mention the real-world trap
- If the planned failure *doesn't* fail (acls/umask surprises on the
  room image), diagnose aloud — the evidence path is the lesson

## Recovery

Snapshot `pre-shared` restores everything; or cleanup below and re-run.

## Cleanup (census)

```console
$ sudo rm -r /srv/demo-shared && ls /srv 2>&1
$ sudo userdel -r alice; sudo userdel -r bob; sudo groupdel project
$ ls /home        # confirm only dsstudent remains
```

## Optional extension

`getfacl /srv/demo-shared` after the sticky demo — the ACL view of
what default permissions can't express; M13's clinic continues from
here.
