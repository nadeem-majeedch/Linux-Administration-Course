# 4 — Users and Groups

> Learn it: [M12 — Users, Groups & Permissions](../modules/M12-users-groups-permissions/content/README.md) ·
> [M14 — sudo & the Root Principle](../modules/M14-sudo-root-principle/content/README.md) ·
> Lookup, not understanding.

## Who am I / who's here

| Command | Purpose | Example output |
|---|---|---|
| `whoami` | effective username | `ana` |
| `id` | uid, gid, all groups | `uid=1001(ana) groups=1001(ana),27(sudo),1005(team)` |
| `id USER` | same, for someone else | `id bob` |
| `groups` | my group memberships | `ana sudo team` |
| `who` / `w` | logged-in sessions | plus load with `w` |
| `getent passwd USER` | resolve a user via system db | scripted lookup |

## Identity files (read them; don't hand-edit)

| File | Holds | Safe to read |
|---|---|---|
| `/etc/passwd` | user ↔ uid, home, shell | yes (no passwords since forever) |
| `/etc/group` | group ↔ gid, members | yes |
| `/etc/shadow` | password hashes, aging | root only |

## User administration (all need sudo)

| Command | Purpose | Key options | Example |
|---|---|---|---|
| `useradd` | create user | `-m` make home · `-s` shell | `sudo useradd -m -s /bin/bash bob` |
| `adduser` | friendly wrapper (Debian/Ubuntu) | interactive | `sudo adduser bob` |
| `usermod` | modify | **`-aG`** append groups · `-L`/`-U` lock | `sudo usermod -aG team bob` |
| `userdel` | delete | `-r` remove home | ⚠️ `sudo userdel -r bob` |
| `passwd` | set/change password | self, or `sudo passwd USER` | `sudo passwd bob` |
| `chage -l USER` | password aging info | — | audit |

⚠️ **`usermod -G` (no `-a`) *replaces* all supplementary groups** —
the classic "I lost sudo by adding myself to docker" incident.
Always `-aG` together.

## Group administration

| Command | Example |
|---|---|
| `sudo groupadd team` | create |
| `sudo groupmod -n newteam team` | rename |
| `sudo groupdel team` | delete (empty it first) |
| `sudo gpasswd -A ana team` | group administrator |

Membership changes apply to **new logins** — re-login, or
`newgrp team` for one shell.

## sudo — the working set

| Command | Purpose |
|---|---|
| `sudo CMD` | run one command as root |
| `sudo -i` | root login shell (full env) |
| `sudo -u USER CMD` | run as another user |
| `sudo -l` | **list what you may run** — first diagnostic |
| `sudo -v` | refresh credential timestamp |
| `sudo visudo` | edit policy **with syntax checking** |
| `sudo visudo -c` | check-only parse of the whole policy |

Policy lives in `/etc/sudoers` (edit only via `visudo`) plus
drop-ins in `/etc/sudoers.d/` — drop-in filenames must avoid `.`
and `~`.

Scoped grant example (`/etc/sudoers.d/deploy`):
```text
bob ALL=(root) /usr/bin/systemctl restart model-api.service
```

⚠️ Root bypasses permission bits, but services run as their own
users — correct ownership protects the *service*, not root. Least
privilege: grant the command, not the shell.

## su vs sudo

| | `su -` | `sudo CMD` |
|---|---|---|
| becomes | full root shell | executes one command |
| logs | who became root | **every command**, in journal |
| policy | target account's password | sudoers per-user/per-command |
