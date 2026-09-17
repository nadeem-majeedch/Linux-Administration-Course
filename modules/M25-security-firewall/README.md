# M25 — Security and Firewall

> Unit 6 · Services, Networking and Security
> Difficulty: Advanced · Prerequisites: M21, M22, M24

**Status: content complete** — 6 lessons, 2 labs (the hardening lab + the
secrets audit), quiz + key, 8 challenges, troubleshooting guide, and the
**server hardening checklist**. Start at the [content index](content/README.md).

## What this module covers

Security principles (least privilege, authN vs authZ, attack surface, defense in
depth); firewalls from the netfilter model to ufw fluency (default-deny,
source-scoped rules, app profiles, `limit`; firewalld recognized for RHEL);
sshd hardening *applied* with the two-terminal rule and rehearsed rollback;
service audits and patch management (unattended-upgrades, GPG/checksums,
supply-chain hygiene); secrets management (env vars, .env discipline, leak
response playbook); and the monitoring layers — auditd, AppArmor vs SELinux,
fail2ban, malware concepts, backups as recovery — all consolidated in a
printable hardening checklist.

The full specification — learning objectives, concepts, command-line skills,
laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 6.

## Before you start

- [ ] Prerequisites complete: M21, M22, M24
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Module links

- Content index: [content/README.md](content/README.md) — lessons, labs, checklist, practice

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-6--services-networking--security-m20m25)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
