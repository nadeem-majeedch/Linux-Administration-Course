# Unit 7 Teaching Guide — The Data Science Stack (M26–M29)

> Sessions S25–S28 · companions: [speaker notes](../../speaker-notes/unit-07-data-science-stack-notes.md) · [deck](../../lecture-slides/unit-07-data-science-stack-slides.md)

## M26 Git & Development Workflows (S25)

**Objectives.** Commit-pointer model; core loop fluency; branch/merge
without fear; SSH remotes; .gitignore *policy* (not just syntax).

**Difficult concepts.** Branch-as-pointer (the sticky-label drawing);
history *rewriting* vs *reverting* (which commands rewrite, and why
pushed history is different).

**Common mistakes.** Committing datasets/venvs (`.gitignore` after the
fact doesn't untrack); "update stuff" messages; merge conflict panic
(they've never *seen* one resolved).

**Demo plan.** The good-vs-bad `git log` contrast; a tiny, controlled
conflict resolved live with markers explained.

**Assessment hook.** M26 quiz (what did this command change); capstone
Git-hygiene area (5 pts, easy to lose).

**Extension.** ★★★: M26 challenges (rebase-reading, bisect concept).

**Troubleshooting (in class).** Students with global git config from
personal machines (wrong identity in commits) — check `git config
user.name` as the lab's step zero. HTTPS-token prompts when SSH config
incomplete — point at the M22 lab's key section.

## M27 Python, Jupyter & Data Workloads (S26)

**Objectives.** venv lifecycle on Linux; `python3 -m pip` reasoning;
pinned requirements; Jupyter as a *supervised service*; tunnels; kernel
management; batch execution.

**Difficult concepts.** The venv-is-a-PATH-prepend mechanism (M15's
mystery resolves); kernel-as-process (a stuck notebook is a process
problem — kill it like one).

**Common mistakes.** pip into system python; `requirements.txt`
unpinned; deleting `.venv` while a kernel uses it; data written to
`~` instead of the project's data dir (permissions + backups in M31
assume the contract).

**Demo plan.** which-python3 in/out of venv; tunnel to VM Jupyter with
the path traced on the architecture diagram.

**Activity.** Three-suspects drill on printed stack traces.

**Assessment hook.** M27 quiz (environment failure diagnosis); the
capstone model-job area (pinned env, provenance sidecar).

**Extension.** ★★★: conda-translation challenge from M31/M27 practice.

**Troubleshooting (in class).** ` externally-managed-environment` (PEP
668) errors on newer Ubuntus — the module covers it; frame as *the
system protecting itself*, not an obstacle. Port 8888 already bound
(last session's Jupyter) — `ss` diagnosis, kill the stale process.

## M28 Docker & Containers (S27)

**Objectives.** VM-vs-container mechanism (kernel sharing); image/
container lifecycle; volumes; ports; layer caching; Compose at reading
level.

**Difficult concepts.** Volume permission gotchas (the container user
vs host uid — M13 knowledge returns); image layers as filesystem
diffs (cache behavior follows from the model).

**Common mistakes.** `-p` forgotten ("running but unreachable" — the
M21 ladder in docker clothing); `docker system prune -a` enthusiasm
(nukes cached images mid-course); building huge contexts (no
.dockerignore).

**Demo plan.** Jupyter-in-a-container with a mounted volume; rebuild
showing CACHED layers; `ss` showing the mapped port.

**Assessment hook.** M28 quiz (lifecycle, volumes, cache reasoning);
the capstone's optional Docker track.

**Extension.** ★★★: compose-with-healthchecks from M28 challenges.

**Troubleshooting (in class).** Docker not installed/daemon dead —
SETUP.md's docker section; labs are designed with a non-Docker fallback
path (note it when releasing the lab).

## M29 Web Servers, Databases & Deployment (S28)

**Objectives.** nginx as a *user-unit you already manage*; server
blocks; log locations; PostgreSQL lifecycle, roles, `\copy`, `pg_dump`
+ restore-test discipline.

**Difficult concepts.** Reverse-proxy semantics (502 = upstream dead —
the log line that says so); `\copy` client-vs-server file access
distinction.

**Common mistakes.** Editing nginx config without `nginx -t` (the
sudoers-visudo lesson returns with a new syntax); DB credentials in
repo files; dumps without restore tests.

**Demo plan.** `\copy` a course CSV → `SELECT count(*)`; `pg_dump` →
drop table → restore → verify. The full evidence loop.

**Assessment hook.** M29 quiz (web/db diagnosis); capstone serving
stack area (user unit + nginx + health endpoint).

**Extension.** ★★★: reverse-proxy-to-Jupyter configuration challenge.

---

## Unit-level notes

- **A2 due S26, A3 due S15→W15 (calendar)** — check the [assessment
  schedule](../../teaching-plan/assessment-schedule.md) before these
  sessions; due-date logistics go in the announcement slot.
- **The integrated-loop slide (S28's close)** is the revision seed —
  have students mark their weakest arrow; that list feeds S30's triage.
- **Docker fallback:** if the room's Docker can't run, S27's lab has a
  documented non-Docker path; announce it *before* the session.
