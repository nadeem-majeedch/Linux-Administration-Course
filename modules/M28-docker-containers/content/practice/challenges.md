# Module 28 Challenges — Docker and Containers

> Eight challenges, C1 (drills) → C8 (design). All inside your own VM;
> every object you create is lab-prefixed (`c*`) and removed by exact
> name at the end. No registry pushes, no `latest`, no host data outside
> lab directories, evidence in `lab-log.md`.

## C1 — Lifecycle state machine, witnessed (drill)

Drive one image (`alpine:3.20`) through every state from Lesson 2 §2,
recording the transition command and `docker ps -a` STATUS each time:
created (`docker create`) → running (`start`) → paused (`pause`) →
unpaused → stopped → running again → removed. Deliverable: the
nine-row transition table. (Bonus: what does `docker inspect -f
'{{.State.Status}}'` report during each row, and which state *cannot*
be reached directly from created?)

## C2 — Layer archaeology

Build the Lesson 3 §5 image, then explain your own image: `docker
history ds-capstone:1.0` — map each line back to the Dockerfile
instruction that created it, identify the two largest layers, and
answer in one sentence each: why is the pip layer large, and why didn't
`--no-cache-dir` shrink the *apt* layer? Then rebuild after editing
*only* the `USER` line's comment and record which layers re-ran.
(Cache invalidation from a one-line diff — evidence for Q13's answer.)

## C3 — The persistence gauntlet

One Postgres container (`postgres:16.4`), three runs, one table:
(1) no volume — create a table, `rm` the container, re-run: table gone?
(2) anonymous volume (`-v /var/lib/postgresql/data`) — same experiment:
does an *anonymous* volume survive `rm`? Where does it show up
(`docker volume ls`)? (3) named volume `c3-pgdata` — table survives
`rm` and re-run; prove it. Then remove all three artifacts **by exact
name/ID**, including any anonymous volume you found. Deliverable: the
three transcripts + a three-row verdict table.

## C4 — Image diet

Take any image you've built this module and cut it down: switch the
base to `-slim`, merge RUN layers with same-step cleanup, add
`.dockerignore` for `.git/` and `.venv/`, and pip's `--no-cache-dir`.
Record `docker images` before/after sizes and `docker system df`
before/after — then explain in two sentences which change bought the
most and why. (No alpine libc experiments required — `slim` is the
course default for a reason.)

## C5 — Network topology lab

Build by hand what Compose automates: a user-defined network `c5net`;
a `postgres:16.4` container `c5-db` with volume + healthcheck command
(run `pg_isready` yourself via `docker exec` until it succeeds); a
`python:3.12-slim` container `c5-app` that `pip install`s `psycopg` and
connects **by service name** (`host="c5-db"`). Deliverable: the
connection transcript proving DNS-by-name, plus the negative test —
recreate both containers on the *default* bridge and show the name
resolution fail.

## C6 — Resource limits under observation

Run a deliberately memory-hungry container (Lesson 4 §5's loop) with
`--memory=256m --memory-swap=256m`, watching `docker stats` in a
second terminal. Record: the stats ceiling, the exit code at the cap
(`inspect .State.OOMKipped`), and the same job with `--cpus=0.5` — how
does wall-time change? Deliverable: transcripts + one paragraph on
which limit you'd set for a shared-server training job and why.

## C7 — The cache-time experiment

Write two Dockerfiles that install an identical large-ish dependency
set (say, `pandas` + `matplotlib`), one with deps-first/code-last, one
with code-first/deps-last. Time three builds each: cold (no cache),
code-only change, requirements change. Deliverable: the six timings in
a table + one sentence per row explaining the cache behavior. (This is
the roadmap's ordering puzzle, quantified on your own disk.)

## C8 — Design: the reproducible research container (design challenge)

No execution required — a written design, the way M26/M29 cap other
units. A four-person research group must share: a pinned analysis
environment, a 50 GB dataset, per-member notebooks, and a small results
API with Postgres. Specify: the image design (base, layers, USER,
healthcheck), the volume/mount layout with *which* pieces are image vs
named volume vs bind mount and why, the compose file structure with
health-checked ordering and resource limits, the port publication
posture on the shared server, and the two M28 mistakes most likely to
bite this group (with their preventions). Deliverable: the one-page
design + three risks you'd flag to the professor.

**Stretch** — personal cheatsheet: one page. Lifecycle states + the six
core commands; the layer-caching ordering rule; volume-vs-bind table;
the compose healthcheck pattern; the five-line security baseline
(pin, non-root, loopback, limits, no baked secrets). If it doesn't fit
one page, you don't know it yet.

---
*All challenges: own VM, lab-prefixed objects, exact-name cleanup,
evidence in `lab-log.md`.*
