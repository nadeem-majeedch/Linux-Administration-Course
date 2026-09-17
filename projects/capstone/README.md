# Capstone — M30: "Deploy and Administer a Linux-Based Data Science Server"

The course's final deliverable: design, deploy, secure, operate, and defend a
complete Linux-based data-science server — pipeline, model, service, and all
the administration around them — as one integrated project.

**Runs on:** a local Ubuntu VM (primary), WSL2 (supported track), or Docker
(all-in-one track). Cloud/GPU strictly optional.

## Document map

### Student pack (`student/`)

| Document | Contents |
|---|---|
| [student/SPEC.md](student/SPEC.md) | **The project specification**: theme, learning outcomes, architecture, required tasks, milestones, week-by-week instructions, deliverables, security/troubleshooting/documentation requirements, environment tracks, extension challenges |
| [student/STARTER.md](student/STARTER.md) | Repository layout, first-week checklist, per-track setup |

### Instructor pack (`instructor/`)

| Document | Contents |
|---|---|
| [instructor/RUBRIC.md](instructor/RUBRIC.md) | The 100-point evidence-based rubric, grade bands, non-negotiables, demo protocol |
| [instructor/VIVA.md](instructor/VIVA.md) | Oral examination question bank (with grading notes), organized by outcome |
| [instructor/INCIDENTS.md](instructor/INCIDENTS.md) | Injected-incident scripts (Phase 3), one per failure class, each with setup commands and an answer key |

## The one rule

**Operational evidence beats polish.** Logs, performed restore tests, runbooks
peers can follow, and clean history are the graded artifacts — a simple,
reliable, monitored pipeline outscores a fancy broken one, deliberately.

## Timeline (suggested 5 weeks)

proposal → build → operate → document → present (details in
[student/SPEC.md](student/SPEC.md) §Milestones).
