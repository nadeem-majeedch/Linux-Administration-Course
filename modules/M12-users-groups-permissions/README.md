# M12 — Users, Groups and Permissions

> Unit 4 · System Administration
> Difficulty: Intermediate · Prerequisites: M10

**Status: content complete.** Full content in [content/](content/lessons/01-identity-users-groups.md):
2 lessons (identity: users/groups/UID/GID/passwd/shadow + the account toolkit;
permissions: rwx, chmod symbolic+numeric, umask, directory permissions, the
check-order rule), 2 labs (identity forensics incl. VM account surgery with the
`-aG` incident; permission surgery incl. the group-stall proof), quiz + key,
6 challenges, troubleshooting guide. Covers: users, root, UID, GID, groups,
/etc/passwd, /etc/shadow, /etc/group, useradd, usermod, userdel, passwd,
groupadd, groupmod, groupdel, id, who, whoami, groups, file ownership, chmod,
symbolic + numeric permissions, umask, directory permissions, least-privilege
seeds. Special bits/ACLs/shared dirs → M13; sudo/sudoers → M14.

This file remains the module's contract: scope, placement, and completion criteria.

## What this module covers

Users, groups, and the rwx permission model; read ls -l fluently; chmod and umask; permission debugging.

The full specification — learning objectives, concepts, command-line skills,
laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 4.

## Before you start

- [ ] Prerequisites complete: M10
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Definition of done

- [ ] Laboratory completed; outputs recorded in `lab-log.md`
- [ ] Exercises attempted without looking up every answer
- [ ] Roadmap self-check questions answered aloud
- [ ] Mini-project submitted (if defined for this module)

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-4--system-administration-m12m15)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
