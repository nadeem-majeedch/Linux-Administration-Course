# M24 — Logs, journald and Monitoring

> Unit 6 · Services, Networking and Security
> Difficulty: Advanced · Prerequisites: M20, M18

**Status: content complete** — 4 lessons, 4 labs, Mini-Project E,
quiz + key, 8 challenges, troubleshooting guide. Start at the
[content index](content/README.md).

## What this module covers

journald storage, priorities and the full journalctl query set; the classic
`/var/log` world (syslog, auth, kernel/dmesg), log levels and rotation with
logrotate; monitoring with uptime/free/vmstat/iostat/sar under a
utilization–saturation–errors frame; the six-step incident methodology
rehearsed on five recurring DS-server incidents (dead service, overnight OOM,
disk full, CPU storms, silent pipeline failures); and the backup 3-2-1 rule
with a **test-restored** archive + mirror. Culminates in Mini-Project E:
`health.sh` + `backup.sh` + an evidence-based incident report.

The full specification — learning objectives, concepts, command-line skills,
laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 6.

## Before you start

- [ ] Prerequisites complete: M20, M18
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Module links

- Content index: [content/README.md](content/README.md) — lessons, labs, mini-project, practice
- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-6--services-networking--security-m20m25)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
