# M28 — Docker and Containers

> Unit 7 · The Data Science Stack
> Difficulty: Intermediate-Advanced · Prerequisites: M16, M20, M27 (M26 recommended)

**Status: content complete.** Five lessons, four labs (install + three hands-on),
an 8-challenge practice set, and a ten-pattern troubleshooting index — all in
your own VM, official pinned images only, loopback ports, targeted cleanup.

## What this module covers

Containers vs VMs; Docker Engine, images, volumes, networks, and Compose; containerize a reproducible ML job.

**Start here:** [content/README.md](content/README.md) — the module index with the recommended path.

| Piece | What you get |
|---|---|
| [Lesson 1](content/lessons/01-container-fundamentals.md) | VMs vs containers, namespaces/cgroups, images/layers/registries, architecture |
| [Lesson 2](content/lessons/02-docker-cli-lifecycle.md) | The core CLI, lifecycle states, stop-vs-kill, ports, cleanup discipline |
| [Lesson 3](content/lessons/03-dockerfiles-and-builds.md) | Dockerfile instructions, layer caching, image hygiene, multi-stage awareness |
| [Lesson 4](content/lessons/04-data-networks-limits.md) | Volumes vs bind mounts, container DNS networking, env vars, resource limits |
| [Lesson 5](content/lessons/05-compose-security-mistakes.md) | Compose stacks with healthchecks; container security; the ten classic mistakes |
| Labs 0–3 | Official-repo install + the docker-group question · first containers · build/persist/debug · Jupyter container + Compose API+Postgres stack |
| [Practice](content/practice/quiz.md) | 22-question quiz + key, challenges C1–C8 |
| [Troubleshooting](content/troubleshooting.md) | 10 symptom→cause→fix patterns |

The full specification — learning objectives, concepts, command-line skills,laboratory, exercises, mini-project, and the Data Science connection — lives in
[COURSE-ROADMAP.md](../../COURSE-ROADMAP.md), Unit 7.

## Before you start

- [ ] Prerequisites complete: M16, M20, M27 (M26 recommended)
- [ ] Lab environment working ([SETUP.md](../../SETUP.md))
- [ ] `lab-log.md` exists in your home directory

## Definition of done

- [ ] Docker Engine installed from the official repo; `docker` works without
      sudo, and you can say what the group membership granted
- [ ] Labs 1–3 completed; evidence in `lab-log.md`
- [ ] Volume-vs-writable-layer persistence experiment (Lab 2/3) proven both ways
- [ ] Compose stack survived `down`/`up` (data intact) and `down -v` (data gone)
- [ ] Quiz attempted before the key; ≥2 challenges done

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-7--the-data-science-stack-m26m29)
- Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
- Fixes and questions: open an issue per [CONTRIBUTING.md](../../CONTRIBUTING.md)

