# M29 — Web Servers, Databases and Deployment

> Unit 7 · The Data Science Stack
> Difficulty: Advanced · Prerequisites: M20, M21, M25, M27

**Status: content complete** — 4 lessons, 2 labs, quiz + key, 8 challenges,
troubleshooting guide. Start at the [content index](content/README.md).

## What this module covers

HTTP fundamentals and the full request path; nginx as static server and reverse
proxy (server blocks, locations, logs, the config-test-reload discipline; Apache
recognized by comparison); PostgreSQL essentials (roles/databases/privileges,
psql, `\copy` CSV loading, `pg_dump` + verified restore, MySQL/MariaDB
comparison); and the deployment model — the app as a systemd user unit with
env-file config and health endpoint, TLS concepts with a self-signed demo —
assembled in the deployment lab (nginx → FastAPI → Postgres) with an operations
runbook.

The full specification — learning objectives, concepts, command-line skills,
laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 7.

## Before you start

- [ ] Prerequisites complete: M20, M21, M25, M27
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Module links

- Content index: [content/README.md](content/README.md) — lessons, labs, practice

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-7--the-data-science-stack-m26m29)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
