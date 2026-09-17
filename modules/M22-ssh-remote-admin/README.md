# M22 — SSH and Remote Administration

> Unit 6 · Services, Networking and Security
> Difficulty: Advanced · Prerequisites: M21, M20

**Status: content complete** — 4 lessons, 2 labs (key workflow + 5-patient
SSH diagnosis clinic), quiz + key, 8 challenges, troubleshooting guide, and
Mini-Project D. Start at the [content index](content/README.md).

## What this module covers

SSH fundamentals and host-key trust (TOFU, known_hosts); Ed25519 key pairs,
ssh-agent, passphrases and key hygiene; `authorized_keys` deployment;
`ssh_config` (aliases, `IdentitiesOnly`, ProxyJump) and `sshd_config` at
reading level (password vs key auth, root login, least privilege); remote
command execution, scp and rsync-over-ssh; local/remote port forwarding;
tmux durable sessions; and the complete DS remote-workstation loop — remote
Jupyter over tunnels, dataset push/result sync, model transfers — culminating
in Mini-Project D with a written operations runbook.

The full specification — learning objectives, concepts, command-line skills,
laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 6.

## Before you start

- [ ] Prerequisites complete: M21, M20
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Module links

- Content index: [content/README.md](content/README.md) — lessons, labs, mini-project, practice

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-6--services-networking--security-m20m25)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
