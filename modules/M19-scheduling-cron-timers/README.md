# M19 — Scheduling: cron and systemd Timers

> Unit 5 · Software, Storage and Time
> Difficulty: Advanced · Prerequisites: M10, M11, M18

**Status: content complete** — 3 lessons, 2 labs, quiz + key, 8 challenges,
troubleshooting guide. Start at the [content index](content/README.md).

## What this module covers

Cron fundamentals and five-field fluency with `systemd-analyze calendar`
validation; the cron environment trap (PATH, cwd, tty) and the env-proof script;
logging scheduled jobs (redirect layers, quiet-success, the mail spool);
systemd timer+service pairs with `Persistent=true`; the production pattern —
locks, fail-loudly, idempotency; and the verify-it-ran discipline: scheduling
the M11-hardened pipeline both ways, with logs as proof.

The full specification — learning objectives, concepts, command-line skills,
laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 5.

## Before you start

- [ ] Prerequisites complete: M10, M11, M18
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Module links

- Content index: [content/README.md](content/README.md) — lessons, labs, practice

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-5--software-storage--time-m16m19)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
