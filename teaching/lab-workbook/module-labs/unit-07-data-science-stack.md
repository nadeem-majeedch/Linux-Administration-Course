# Unit 7 Labs — The Data Science Stack (M26–M29)

> Sessions S25–S28 · Git, Python/Jupyter, containers, serving — every
> tool administered with Unit 1–6 verbs.

| Lab | Module | Duration | Difficulty | Deliverable | Link |
|---|---|---|---|---|---|
| Version your work | M26 | 45' | ★★ | real history built by hand + clean graph | [M26 lab 1](../../../modules/M26-git-dev-workflows/content/labs/lab-01-version-your-work.md) |
| Break & repair clinic | M26 | 30' | ★★★ | recovery verbs with when-to-use notes | [M26 lab 2](../../../modules/M26-git-dev-workflows/content/labs/lab-02-break-repair-clinic.md) |
| End-to-end DS workflow | M27 | 50' | ★★★ | clone→venv→pin→data→Jupyter→commit loop | [M27 lab 3](../../../modules/M27-python-jupyter-data/content/labs/lab-03-batch-scheduling.md) |
| Environment drills | M27 | 20' | ★★ | venv lifecycle + failure diagnosis | [M27 labs](../../../modules/M27-python-jupyter-data/content/labs/README.md) |
| First containers | M28 | 30' | ★★ | run/exec/logs with port+volume mapping | [M28 labs](../../../modules/M28-docker-containers/content/labs/README.md) |
| Build & compose | M28 | 30' | ★★★ | Dockerfile + volume persistence proof | [M28 labs](../../../modules/M28-docker-containers/content/labs/README.md) |
| Serve a dataset (nginx) | M29 | 25' | ★★ | server block + access-log evidence | [M29 labs](../../../modules/M29-web-servers-databases/content/labs/README.md) |
| PostgreSQL `\copy` + dump | M29 | 30' | ★★ | loaded table + dump/restore round-trip | [M29 labs](../../../modules/M29-web-servers-databases/content/labs/README.md) |

## Session mapping

- **S25**: version-your-work (+ break-repair as HW)
- **S26**: end-to-end DS workflow — the unit's centerpiece
- **S27**: first containers (+ build/compose as HW)
- **S28**: nginx + PostgreSQL labs

## The unit's safety architecture

- **System python is untouchable** — venv before any pip; the
  `externally-managed-environment` message is explained as *protection*
- **Datasets never enter Git** — `.gitignore` is a deliverable, not a
  suggestion
- **Secrets hygiene starts**: DB credentials in `600` env files outside
  the repo (M25's rule, now applied)
- **Docker fallback path exists** for rooms where Docker can't run —
  announced before S27

## Checkpoints that matter most

- M26: "what did this command *change*" answers — history reasoning,
  not command recall
- M27: the three-suspects diagnosis (wrong env / wrong kernel / not
  installed here)
- M29: the 502 log-line reading; the restore *verification* after
  `pg_dump`

## Extension routing (★★★)

- M26: rebase-reading, bisect concept
- M28: compose-with-healthchecks
- M29: reverse-proxy-to-Jupyter configuration

## Instructor staging

- Docker installed per SETUP.md (verify the room before S27)
- PostgreSQL + nginx present on lab images (S28)
- [Infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md)
  item 9

## After this unit

**A3 (Assignment 3)** is due week 15 — its remote-operator brief
consumes this unit; the capstone's **Build** phase assumes all of it.
The integrated-loop slide (S28 close) seeds the S30 revision triage.
