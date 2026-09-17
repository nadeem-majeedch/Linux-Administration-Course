# Module 28 Labs — Docker and Containers

> Unit 7 · Difficulty: Intermediate → Advanced
> Four labs. All run **inside your own VM**. Docker practice only —
> nothing here touches host data outside lab-created directories.

| # | Lab | Focus | Est. time |
|---|-----|-------|-----------|
| 0 | [lab-00-install.md](lab-00-install.md) | Install Docker Engine from the official repo; verify; the `docker` group question | ~30 min |
| 1 | [lab-01-first-containers.md](lab-01-first-containers.md) | run/ps/logs/exec/stop/rm; lifecycle proof; loopback ports | ~45 min |
| 2 | [lab-02-build-persist-debug.md](lab-02-build-persist-debug.md) | Build the M27 environment as an image; volumes vs writable layer; exec debugging | ~60 min |
| 3 | [lab-03-jupyter-compose.md](lab-03-jupyter-compose.md) | Jupyter container with mounted datasets; Compose API + Postgres stack | ~75 min |

General rules for all four:

- **Official images, pinned tags only** (`python:3.12-slim`,
  `postgres:16.4`, `alpine:3.20`, `nginx:1.27-alpine`) — never `latest`.
- Everything you delete, you created: lab containers, lab volumes
  (`lab*`/project-prefixed names), lab directories. `docker volume rm`
  is treated as data deletion — list first, name exactly.
- Ports publish on `127.0.0.1` unless the lab says otherwise.
- Pulls only — no registry pushes in this course; builds are local.
- Evidence in `lab-log.md`: command + key output, per course convention.

Prerequisites: [Lesson 1](../lessons/01-container-fundamentals.md) for
Lab 0–1; Lessons 2–3 for Lab 2; Lessons 4–5 for Lab 3. The M27
`requirements.txt` from Lab 1 of that module is reused in Lab 2.
