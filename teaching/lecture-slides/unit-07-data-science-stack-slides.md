# Unit 7 Lecture Slides — The Data Science Stack (M26–M29)

> **Delivery:** Sessions 25–28 · Speaker notes:
> [../speaker-notes/unit-07-data-science-stack-notes.md](../speaker-notes/unit-07-data-science-stack-notes.md)

---

# Slide 1 — Title

## Slide Content
**Unit 7 — The Data Science Stack**
Git · Python/Jupyter on Linux · Docker · Web servers & databases (M26–M29)
*Where administration becomes your daily work*

## Instructor Delivery Notes
Framing: "Units 1–6 taught the machine. This unit installs *your
profession* on it — and every tool here is administered with the verbs
you already own."

## Visual or Demonstration Suggestion
The capstone architecture diagram, all four layers lit up.

## Student Question
"Which of the four tools have you used *without* knowing how it runs on Linux?"

---

# Slide 2 — Git: history as infrastructure

## Slide Content
- A commit = a snapshot **pointer** (not a copy) — history is cheap
- Core loop: `status → add → commit` (the triangle)
- Branch = a movable label — branching is *not* copying
- Remotes: `clone/pull/push` — GitHub is *a copy*, not the origin of truth
- `.gitignore`: datasets, `.venv/`, checkpoints — **never** in history

## Instructor Delivery Notes
The pointer-vs-copy idea kills the branch fear before it forms. The
.gitignore slide is also a *policy* slide: "no bulk data in Git" is a
capstone rubric line.

## Visual or Demonstration Suggestion
`git log --graph --oneline` on a repo with branches — labels pointing at commits, visible.

## Student Question
"You branched and committed 3 times. What got copied? (Trick: nothing big.)"

---

# Slide 3 — Git on Linux: SSH remotes & hygiene

## Slide Content
- SSH remote (M22's keys!) vs HTTPS tokens — course standard: keys
- `git config --global user.name/email` — your commits need identity
- Small, described commits — messages are letters to future-you
- Recovery verbs: `restore`, `reset` (soft/mixed), `revert` — know which rewrites history

## Instructor Delivery Notes
M22's key setup *is* the GitHub auth mechanism — connect the units
explicitly. Commit-message hygiene gets its 60 seconds: subject line +
why-not-what.

## Visual or Demonstration Suggestion
`git log --oneline` of a *good* repo vs a "update stuff"×40 repo — the difference is the lecture.

## Student Question
"Which command reverses a pushed commit *without* rewriting history?"

---

# Slide 4 — Python environments on Linux

## Slide Content
- System python is **for the system** — never pip-install into it
- `python3 -m venv .venv` → `source .venv/bin/activate` → *isolated*
- `python3 -m pip install` beats bare `pip` (right interpreter, right pip)
- `requirements.txt` with pinned versions = reproducibility
- Which python? `which python3` · `type -a` (M15's PATH lesson returns)

## Instructor Delivery Notes
The M15 PATH mystery resolves here: the venv *prepends* itself to PATH —
that's the whole mechanism. The two failure modes `python3 -m pip`
avoids: wrong interpreter's pip, and scripts shebang-shadowing.

## Visual or Demonstration Suggestion
`which python3` inside vs outside a venv — the path swap on screen.

## Student Question
"'ModuleNotFoundError: pandas' — it's installed! Name three suspects."

---

# Slide 5 — Jupyter on a Linux server

## Slide Content
- `jupyter lab` is a *server process* — it has logs, ports, a PID (M20/M21 verbs apply!)
- Runs on the VM's 8888; reach it via browser or **SSH tunnel** (M22)
- Kernels = running processes — a "stuck notebook" is a *process* problem
- Data directories: permissions from Unit 4 apply to your notebooks' world
- Batch alternative: `jupyter nbconvert --execute` (scripted runs)

## Instructor Delivery Notes
Reframe Jupyter as a service: "you already know how to supervise this."
The tunnel demo closes the Unit 6 loop: local browser → forwarded port →
remote kernel. That's the *actual* GPU-server workflow.

## Visual or Demonstration Suggestion
Start jupyter on the VM; tunnel from host; browser opens — trace the path on the architecture diagram.

## Student Question
"Your remote notebook lost its variables. Is that a bug or a kernel event?"

---

# Slide 6 — Knowledge check

## Slide Content
1. Where does `pip install` put packages *without* a venv — and who hates that?
2. `requirements.txt` has `pandas` unpinned. What breaks six months later?
3. `ss -tlnp | grep 8888` shows nothing. What's wrong with the Jupyter 'network'?

## Instructor Delivery Notes
Q3 reuses Unit 6's rung-4 logic — cross-unit transfer is the point;
students who answer "no listener, it's not networking" have integrated
the course.

## Visual or Demonstration Suggestion
—

## Student Question
(Q3 is the check)

---

# Slide 7 — Containers: the reproducibility machine

## Slide Content
- VM = whole computer emulated; container = **isolated process** sharing your kernel (fast, light)
- Image = frozen filesystem template; container = running instance
- `docker run -p 8888:8888 -v "$PWD/data:/data" image` — ports & volumes
- Dockerfile = the recipe; layer caching = rebuilds are cheap
- Compose: multi-service apps described in one YAML

## Instructor Delivery Notes
The kernel-sharing point explains *why* containers start in milliseconds
— no BIOS, no boot. Volumes connect to M17 (mounts) and M13
(permission of mounted dirs) — the course is a web, keep pulling threads.

## Visual or Demonstration Suggestion
`docker images` before/after a build — layers listed, cached layers "CACHED" on rebuild.

## Student Question
"Delete the container. Is the data in /data gone? What design choice made that true?"

---

# Slide 8 — Serving data: nginx + PostgreSQL

## Slide Content
- nginx: static files & reverse proxy; config in `/etc/nginx/`; logs in `/var/log/nginx/`
- `systemctl` verbs apply — nginx is *just another service* (M20!)
- PostgreSQL: `systemctl`-managed, `psql` client, **roles & databases**
- Load a CSV: `\copy table FROM 'file.csv' CSV HEADER`
- Back up: `pg_dump db > dump.sql` — and *test the restore* (M19's rule)

## Instructor Delivery Notes
The through-line: "nginx and PostgreSQL are user units you already know
how to start, read logs of, and enable." Nothing new — just more
residents in the house Unit 4 built.

## Visual or Demonstration Suggestion
`\copy` a course CSV live; `SELECT count(*)` proves it; `pg_dump` size vs CSV size noted.

## Student Question
"Where does nginx's *actual* answer to 'why 502' live?"

---

# Slide 9 — Knowledge check

## Slide Content
1. Image vs container — one sentence each.
2. `502 Bad Gateway` from nginx — what does the *log* say first?
3. `pg_dump` ran nightly. When is the backup real?

## Instructor Delivery Notes
Q3 is M19/M24's fusion — "after a tested restore" is the only passing
answer; it's also the capstone's backup non-negotiable (restore performed
or score 0).

## Visual or Demonstration Suggestion
—

## Student Question
(Q3 is the check)

---

# Slide 10 — Common mistakes (Unit 7)

## Slide Content
- pip into system python (broken apt-packages ensue)
- Datasets committed to Git (history bloats forever)
- Unpinned requirements — the environment that "worked last semester"
- `-p 8888:8888` forgotten — "container running, page won't load"
- pg_dump without a restore test — the rumor backup

## Instructor Delivery Notes
All five are capstone rubric deductions with names — show the rubric
rows; the stakes are not hypothetical.

## Visual or Demonstration Suggestion
A `.git` directory ballooned by a dataset commit — the forever-cost visual.

## Student Question
"Which mistake is irreversible *even with snapshots*?" (history rewrite; pushed secrets)

---

# Slide 11 — Data Science connection: the integrated loop

## Slide Content
```
clone → venv → pin → data (rsync'd, permissions set)
  → Jupyter/tunnel → experiment → results → commit
  → containerize → serve → monitor → backup
```
- Every arrow is a *verb you've practiced* — the loop is the course
- M31 (next week) runs it as a day-in-the-life; the capstone grades it

## Instructor Delivery Notes
Walk the loop twice: once naming the tool, once naming the *unit* that
taught it. The second pass is the "you were never learning tools, you
were learning a system" moment.

## Visual or Demonstration Suggestion
The loop diagram with unit numbers on each arrow.

## Student Question
"Which arrow are you least sure of? (That's your revision checklist seed.)"

---

# Slide 12 — Summary & exit ticket

## Slide Content
**Summary:** Git pointers & hygiene · venv/pin discipline · Jupyter as a
supervised service + tunnels · containers = kernel-shared isolation ·
nginx/PostgreSQL = familiar verbs, new residents
**Exit ticket:** one-line each: why `python3 -m pip`? image vs
container? when is a backup real?
**HW:** M26–M29 quizzes · A3 due W15 · capstone Operate phase

## Instructor Delivery Notes
Exit answers map 1:1 to final-exam Section A phrasing — collect and
adjust S30's revision emphasis accordingly.

## Visual or Demonstration Suggestion
—

## Student Question
(exit ticket is the question)

---

## Deck references
- Modules: [M26](../../modules/M26-git-dev-workflows/README.md) · [M27](../../modules/M27-python-jupyter-data/README.md) · [M28](../../modules/M28-docker-containers/README.md) · [M29](../../modules/M29-web-servers-databases/README.md)
- Next deck: [Unit 8 — Capstone](unit-08-capstone-slides.md)
