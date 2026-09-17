# Command Cheatsheets — Index

> The course keeps **nine canonical, unit-organized sheets** in
> [`resources/cheatsheets/`](../../../resources/cheatsheets/README.md) —
> maintained with the lessons they summarize, so they can't drift.
> This page is the revision-time index: what each covers, and which
> exam sections it helps you *not* need.

> **Course rule, worth repeating:** a cheatsheet is *lookup*, not
> understanding. Every exam here gives you evidence and asks for
> reasoning — no question is answerable by copying a command line.
> Use these to refresh syntax mid-practice, not as the study itself.

| Sheet | Covers | Helps with |
|---|---|---|
| [Unit 1 — Foundations](../../../resources/cheatsheets/unit1-foundations.md) | OS concepts, distros, VM/WSL2, terminal basics, man/help | Midterm A |
| [Unit 2 — Command line](../../../resources/cheatsheets/unit2-command-line.md) | navigation, paths, globs, file ops, links, pipes/redirection, quoting, aliases, history | Midterm B/C |
| [Unit 3 — Scripting](../../../resources/cheatsheets/unit3-scripting.md) | variables, tests, loops, functions, traps, `set -euo pipefail`, shellcheck | Final C, A4 |
| [Unit 4 — Admin](../../../resources/cheatsheets/unit4-admin.md) | users/groups, sudo, chmod/chown/umask, SGID, ACL basics | Midterm A, LA-2/3, practical II |
| [Unit 5 — Software, storage, time](../../../resources/cheatsheets/unit5-software-storage-time.md) | apt/dpkg, lsblk/df/du, mount/fstab (concepts), cron/timers, tar/rsync backups | Final A/B, practical III |
| [Unit 6 — Services, network, security](../../../resources/cheatsheets/unit6-services-networking.md) | systemctl, journalctl, ip/ss/dig, UFW, SSH keys/config | Final A/B/D, practical I/IV |
| [Unit 7 — Data science stack](../../../resources/cheatsheets/unit7-data-science-stack.md) | venv/pip, jupyter, git core loop, docker run/build/compose | Final C, A6, capstone |
| [Capstone ops](../../../resources/cheatsheets/capstone-ops.md) | cross-unit operations runbook for the final project | Capstone |
| [Safety card](../../../resources/cheatsheets/safety-card.md) | the destructive-command guard rules — read *first*, always | everything |

## Topic cross-index (when you remember the topic, not the week)

| Topic | Sheet | Topic | Sheet |
|---|---|---|---|
| permissions & ownership | Unit 4 | SSH & file transfer | Unit 6 |
| processes & signals | Unit 2 + Unit 4 | systemd services | Unit 6 |
| text pipelines (grep/sed/awk) | Unit 2 | logs & journalctl | Unit 6 |
| scripting control flow | Unit 3 | backups (tar/rsync) | Unit 5 |
| apt & packages | Unit 5 | Docker | Unit 7 |
| storage & mounting | Unit 5 | Python/venv/Jupyter | Unit 7 |
| networking & DNS | Unit 6 | Git | Unit 7 |
