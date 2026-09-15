# Lesson 1 — Ownership & the Shared-Directory Pattern

> Module 13 · Unit 4 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 1 — Build the shared tree](../labs/lab-01-build-shared-tree.md)
> Up next: [Lesson 2 — ACLs & the permission clinic](02-acls-permission-clinic.md)

---

## 1. The problem this lesson exists to solve

M12 gave you the mode bits. Real shared servers add one more dimension: **files
keep being created**, and every newborn file brings a fresh owner and fresh mode.
The question that breaks naive setups:

> Alice writes `results.csv` into the team folder. Bob can't edit it. Why — and
> how do we make this *never happen again* without anyone re-chmodding anything?

Answering that takes three tools: **chown/chgrp** (fix ownership), **setgid
directories** (make newborns inherit the team group), and a **collaborative
umask** (make newborns group-writable). Together they are the shared-directory
pattern — the access model of every well-run research server.

## 2. chown & chgrp: moving ownership

```console
$ sudo chown alice report.csv            # change owner
$ sudo chgrp labteam report.csv          # change group
$ sudo chown alice:labteam report.csv    # both at once
$ sudo chown -R alice:labteam ~/project-alice/   # recurse (M07's -R rules apply)
```

Why `sudo`: you may freely *give away* files you own to groups you're in, but
changing a file's **owner** is root business — otherwise users could launder
quota and audit trails. (`chgrp` to a group you *belong to* needs no sudo:
`chgrp labteam mine.txt` works — try it in the VM.)

M12's numeric world connects here: `ls -l`'s owner/group columns are exactly
what chown edits, and `ls -ln` shows the underlying numbers (UID/GID) —
useful when a deleted user's files show up as `1007` instead of a name.

## 3. The primary-group stamp (why group design matters)

New files inherit the creator's **primary group**:

```console
$ id -gn        # alice: 'alice' by default on Ubuntu
```

So Alice's new files are group `alice` — no team member can touch them no
matter what the directory says. Two fixes exist; the right one is structural:

1. **Put users' primary group = team** (user-level redesign: works, but
   blurs "personal" vs "team" for everything they touch).
2. **Setgid directories** (directory-level: team group inherits *only inside
   the shared tree*) — the professional choice.

## 4. Setgid on directories: the inheritance switch

The **SGID** bit on a directory means: *new files/subdirs created inside take
the directory's group*, not the creator's primary group.

```console
$ sudo chgrp labteam /srv/lab
$ sudo chmod 2770 /srv/lab
$ ls -ld /srv/lab
drwxrws--- 2 alice labteam 4096 Sep 15 23:10 /srv/lab
```

Read that mode: `2` = **setgid**, `770` = team-full, others-nothing. The `s`
in the group-triplet (`rws`) is the same bit visible in symbolic form. Now:

```console
$ touch /srv/lab/alice-data.csv        # as alice
$ ls -l /srv/lab
-rw-rw-r-- 1 alice labteam 0 ... alice-data.csv    # group = labteam, not alice!
```

Setgid *propagates* through subdirectories created with it set — build the
top once, the whole tree inherits the team group forever.

## 5. Group-writable newborns: the umask half

Setgid fixes the *group stamp*; newborn *mode* comes from the creator's umask
(M12: default 002 on Ubuntu → files 664, dirs 775 — already group-writable).

The full pattern on a server whose users have private defaults is a
**directory-scoped umask** via ACLs (Lesson 2) — or the team norm
`umask 0002` in members' profiles (M15). The design point: mode+group of
newborns must be *automatic*, or the sharing silently decays — every
"why can't Bob edit this?" ticket is a decayed pattern, not a user error.

## 6. The sticky bit: shared but safe

The **sticky bit** (`t`) on a directory says: *you may delete only files you
own* — neutralizing §1's "directory-w deletes anything" rule *inside that
directory*:

```console
$ ls -ld /tmp
drwxrwxrwt 17 root root 40960 ... /tmp      # that 't' — you've seen it since M06
```

World-writable `/tmp` works *because* of the sticky bit: everyone may write,
nobody may delete others' files. Where research servers use it: group drop-boxes
(`chmod 1773 inbox`) — students submit, staff collects, students can't
sabotage each other's submissions.

## 7. The complete shared-tree recipe

```console
$ sudo groupadd labteam
$ sudo usermod -aG labteam alice; sudo usermod -aG labteam bob   # (relogin!)
$ sudo mkdir -p /srv/lab/{datasets,results,inbox}
$ sudo chgrp -R labteam /srv/lab
$ sudo chmod 2770 /srv/lab /srv/lab/datasets /srv/lab/results   # setgid + team-rwx
$ sudo chmod 3770 /srv/lab/inbox                                 # setgid + sticky
```

| Layer | Tool | Contribution |
|---|---|---|
| Identity | `groupadd`, `usermod -aG` | who's on the team |
| Group inheritance | setgid dirs (2/`s`) | newborns carry the team group |
| Newborn modes | umask 002 / ACL default (L2) | newborns are group-writable |
| Deletion safety | sticky bit (`1`/`t`) where needed | drop-box etiquette |
| Others | `o=` nothing | the world isn't invited |

## 8. DS framing: research-project access maps

| Directory | Mode | Why |
|---|---|---|
| `/srv/lab/datasets` | 2770 | team reads/writes shared data; others blind |
| `/srv/lab/results/<student>` | 2730 | student writes; *team reads* (supervision) |
| `/srv/lab/inbox` | 3770 | students drop; can't retract others' |
| `~/jupyter-work` | 700 | personal notebooks — nobody's business (M27) |
| model artifacts dir | 2750 | team reads (serving, M29), only trainer writes |

Model files and experiment directories deserve the same thinking as datasets:
a 4 GB checkpoint nobody but the trainer may read strands the team; one the
whole internet may read may be the lab's IP. **Choose modes from the access
contract, and let setgid keep them true as files arrive.**

## Exercises (lab-log.md)

1. In your VM: create users `t-alice`, `t-bob` and group `t-lab` (M12
   toolkit); give each `-aG t-lab`. Verify with `id` — after a *fresh* login
   (`sudo -iu t-alice`).
2. The naive failure, demonstrated: shared dir `chmod 770 t-lab` **without**
   setgid; as t-alice create a file; as t-bob attempt to *append* to it.
   Record the exact failure and its cause chain (primary-group stamp + umask).
3. Rebuild with `chmod 2770` and repeat. Verify the newborn's group stamp with
   `ls -l`. What changed, exactly?
4. Sticky-bit lab: `chmod 3770 inbox`; as t-alice create `mine.txt`; as t-bob
   attempt `rm inbox/mine.txt` — quote the error. Then remove the sticky bit
   and repeat: what's now possible, and why is that dangerous in a drop-box?
5. `chown` without sudo: try `chown t-bob mine.txt` as t-alice — read the
   error; then `chgrp` it to a group t-alice belongs to — that worked? State
   the rule you just discovered.
6. Numeric decoding: modes `2770`, `3770`, `2750`, `1733` — write each in
   words (what each digit class does).
7. Design: a 6-person lab shares datasets (team-rw), one supervisor-only
   grades folder, and a public exports dir (world-readable, team-writable).
   Write the mkdir/chgrp/chmod recipe, and justify each mode in one line.

## Check yourself before Lesson 2

- I can chown/chgrp (and know which direction needs sudo).
- Setgid: I can explain what it changes about newborn files, and build one.
- Sticky bit: I know its contract and where /tmp already uses it.
- The shared-tree recipe is something I can produce from memory for a new team.

## Further reading (official sources)

- Ubuntu Server docs: file permissions & user management —
  <https://documentation.ubuntu.com/server/how-to/security/users/>
- `man chown`, `man chgrp`, `man chmod` (special-bits section)
- Lesson 2 extends this with ACLs for the cases groups can't express

Next: [Lesson 2 — ACLs & the Permission Clinic](02-acls-permission-clinic.md)
