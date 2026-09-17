# M12 — Users, Groups & Permissions: content guide

> Identity and the rwx model — the module where Linux stops being a
> single-player game.

**Lessons**

| # | Lesson | You will be able to |
|---|--------|---------------------|
| 1 | [01-identity-users-groups.md](lessons/01-identity-users-groups.md) | Read the account system (`/etc/passwd`, `/etc/shadow`, `/etc/group`), UID/GID semantics, and the account toolkit |
| 2 | [02-permissions-chmod-umask.md](lessons/02-permissions-chmod-umask.md) | Read `ls -l` fluently, apply `chmod` symbolic + numeric, use `umask`, and apply the check-order rule |

**Labs** — [labs/README.md](labs/README.md): identity forensics
(incl. VM account surgery and the `-aG` incident) · permission
surgery (incl. the group-stall proof).

**Practice** — [practice/quiz.md](practice/quiz.md) (+ key),
[challenges.md](practice/challenges.md) (6 challenges).

## Learning objectives

By the end of this module you can:

1. **Explain** Linux identity: users as UID numbers, groups as GID
   numbers, primary vs supplementary groups, and where the records
   live (`/etc/passwd`, `/etc/shadow` and *why* it's root-only,
   `/etc/group`).
2. **Administer** accounts safely on your own VM: `useradd`/
   `usermod`/`userdel`, `groupadd`/`groupmod`/`groupdel`, `passwd`,
   `id`, `whoami`, `groups`, `who` — including the classic `usermod
   -aG` accident and its prevention.
3. **Read** `ls -l` output fluently: type, owner, group, the three
   rwx triads, and what each bit means for files vs directories.
4. **Apply** permissions deliberately: `chmod` symbolic and numeric,
   `chown`/`chgrp`, `umask` as default-subtraction, and the
   check-order rule (owner → group → other, first match wins).
5. **Diagnose** permission failures from the error message backward:
   which triad was consulted, why, and the least-privilege fix —
   never "chmod 777 as a repair".
6. **Connect** the model to DS reality: shared datasets, project
   directories, and the seeds of M13's shared-access patterns
   (special bits and ACLs wait there).

## Command-line skills

`id` · `whoami` · `groups` · `who` · `useradd`/`adduser` ·
`usermod -aG` · `userdel` · `passwd` · `groupadd`/`groupmod`/
`groupdel` · `ls -l` (and `-a`, `-n` for numeric UID/GID) ·
`chmod` (symbolic `u/g/o/a` × `+/-/=` × `rwx`, numeric `NNN`) ·
`chown`/`chgrp` · `umask` (view + set) · `su -` (preview of M14).

## Prerequisite map

M04/M14 established *you* are a normal user with sudo; M12 explains
what that means mechanically. M13 extends the model to shared access
(SGID, sticky, ACLs, the shared-dataset designs); M14 builds the
sudo/privilege layer; M22 and M31 apply identity to remote servers
(SSH keys live in permission-strict files — you'll now understand
*why* sshd demands 600).
