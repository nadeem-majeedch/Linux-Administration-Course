# Module 26 — Git and Development Workflows

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 7 · The Data Science Stack](../../../COURSE-ROADMAP.md#unit-7--the-data-science-stack-m26m29).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-7--the-data-science-stack-m26m29) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> Unit 7 · The Data Science Stack · Difficulty: Intermediate
> Time: ~6 hours total · Environment: your own VM (nothing here needs sudo after install)
> Prerequisites: [M10](../../M10-bash-scripting/README.md) (shell fluency), [M13](../../M13-ownership-shared-access/README.md) (permissions), [M22](../../M22-ssh-remote-admin/README.md) (SSH keys)

Git is the version-control system of modern data science: every dataset
pipeline, notebook, and model lives in a repository, and every collaborative
workflow — from a two-person project team to a thousand-engineer company —
runs on the same small set of operations you'll master here. This module
teaches Git as a *Linux tool*: installed with `apt`, configured in dotfiles,
authenticated with the SSH keys you already own, and driven entirely from the
terminal.

**Why this comes late, not early.** You've spent 25 modules building things
worth versioning. Git's commands are trivial to type and meaningless to
memorize; what matters is the *model* — three states, commits as snapshots,
branches as labels. You now have enough Linux experience for the model to
land.

## What you'll be able to do

- Explain Git's three-state model (working tree → index → HEAD) and predict
  what any command moves where
- Create, commit, branch, merge, and resolve conflicts from the command line
- Push to and pull from remotes — including a *local* bare repository, so no
  external hosting account is needed for any lab
- Write a `.gitignore` that keeps datasets, venvs, and outputs out of history
- Authenticate to a remote over SSH (the university-server pattern) and know
  why HTTPS-with-token is the alternative
- Choose and run a workflow: feature-branch for teams, trunk-based for solo

## Files in this module

| Path | Contents |
|---|---|
| [lessons/01-git-model-core-loop.md](lessons/01-git-model-core-loop.md) | What Git really stores; init, add, commit, log, status; the mental model |
| [lessons/02-branching-merging.md](lessons/02-branching-merging.md) | Branches as pointers; fast-forward vs three-way merges; conflict resolution |
| [lessons/03-remotes-gitignore-auth.md](lessons/03-remotes-gitignore-auth.md) | clone/push/pull; bare repos; `.gitignore` for data science; SSH auth; workflow patterns |
| [labs/README.md](labs/README.md) | Lab index: two labs + the end-to-end capstone walk |
| [practice/quiz.md](practice/quiz.md) → [quiz-answers.md](practice/quiz-answers.md) | 22 questions, reasoning-graded key |
| [practice/challenges.md](practice/challenges.md) | Eight challenges, C1 (drills) → C8 (design) |
| [troubleshooting.md](troubleshooting.md) | Ten real-world Git failure patterns |
| [labs/lab-03-end-to-end-ds-workflow.md](labs/lab-03-end-to-end-ds-workflow.md) | **The course's thread-through**: SSH → Git → venv → data → Jupyter → analysis → output → Git |

## The safety contract (same as every module)

- All repositories live under your home directory; nothing here touches
  system paths or other users.
- No external hosting account is required — Labs use a **local bare
  repository** as the remote, so `push`/`pull` are real operations with zero
  network dependence and zero risk to any real project.
- Nothing in this module asks you to commit to *this course's* repository;
  your practice repos are entirely yours.
- Force-push, `reset --hard`, `filter-branch`, and history rewriting are
  taught as *recovery tools with blast radii* — always inside a practice repo
  you can afford to lose.

## Suggested path

1. Lessons 1–2, then **Lab 1** (build a real history in your own repo)
2. Lesson 3, then **Lab 2** (remotes + the break/repair clinic)
3. Quiz; do C1–C4 at minimum
4. **Lab 3** — the end-to-end data science walk that ties M22, M27, and this
   module into one sitting
5. Keep the C8 design challenge for your portfolio

Up next in Unit 7: [M27 — Python, Jupyter & Data Workloads](../../M27-python-jupyter-data/README.md)
