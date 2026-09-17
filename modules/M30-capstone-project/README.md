# M30 — Capstone Project

> Unit 8 · Capstone
> Difficulty: Advanced · Prerequisites: M01–M29 (M31 recommended in parallel)

**Status: complete.** The full capstone pack lives in [`projects/capstone/`](../../projects/capstone/README.md) — student specification, starter guide, and a separate instructor pack (rubric, viva bank, injectable incidents). This README is the module's contract; the pack is the project.

## Theme

**"Deploy and Administer a Linux-Based Data Science Server."**

One machine — a local Ubuntu VM (primary), WSL2 (supported), or Docker (concept translations graded) — operating as a small but complete DS platform: dataset feed → validation → Postgres → scheduled model job → API behind nginx, ringed by ufw, systemd user units, logs, backups, and Bash automation. Cloud/GPU is optional and uncredited; every requirement is satisfiable locally.

## What it demonstrates

The entire course as one operating, defensible system: installation & provisioning (M04), users/groups/permissions (M12–M14), storage (M17), processes (M18), scheduling (M19), systemd services (M20), networking (M21), SSH (M22), logs & monitoring (M24), security hardening (M25), Python/Jupyter environments (M27), Git (M26), Docker (M28), plus Bash automation (M10–M11) and the troubleshooting methodology (M23) as the assessment currency.

## The pack

| Document | Audience | Contents |
|---|---|---|
| [README](../../projects/capstone/README.md) | both | pack index, document map, "the one rule" (evidence, not claims) |
| [SPEC](../../projects/capstone/student/SPEC.md) | student | 18 required tasks with module mapping, milestones & weights, deliverables, security/troubleshooting/documentation requirements, extension challenges |
| [STARTER](../../projects/capstone/student/STARTER.md) | student | repo layout, per-track first-hour setup, first-week checklist |
| [RUBRIC](../../projects/capstone/instructor/RUBRIC.md) | instructor | 100-point evidence rubric, demo protocol, non-negotiable deductions |
| [VIVA](../../projects/capstone/instructor/VIVA.md) | instructor | 29-question oral exam bank |
| [INCIDENTS](../../projects/capstone/instructor/INCIDENTS.md) | instructor | 7 injectable incidents with staging commands and answer keys |

## Before you start

- [ ] All module prerequisites complete; the [Level 5 lab](../../labs/level-5-ds-server.md) is the closest rehearsal
- [ ] Your environment track chosen (VM / WSL2 / Docker) and the STARTER first-hour setup done
- [ ] Capstone Git repo created **with no committed secrets** (SPEC §security)

## Definition of done

- [ ] All 18 SPEC tasks evidenced in the capstone repo
- [ ] One instructor-injected incident resolved with an eight-step method report
- [ ] Restore test executed and evidenced (an untested backup scores zero)
- [ ] Peer-tested runbook, architecture diagram, and incident report committed
- [ ] Live demo + viva completed per [RUBRIC](../../projects/capstone/instructor/RUBRIC.md)

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-8--capstone-m30)
- Cheatsheets: [cheatsheets/](../../cheatsheets/README.md) · capstone ops card: [capstone-ops.md](../../resources/cheatsheets/capstone-ops.md)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)
