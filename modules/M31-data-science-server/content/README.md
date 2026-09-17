# M31 — The Data Science Server · Content Index

> Unit 8 companion · Difficulty: Advanced · Time: ~8 hours total
> Environment: your own VM, CPU-only (GPU concepts taught administratively)
> Prerequisites: M20, M22, M24-clinics, M26, M27, M28, M29 core + extensions

Twenty-nine modules of skills; one working week to fuse them. This
module's premise: *the ML server is where administration stops being a
subject and becomes the job.* Everything here is the daily reality of a
data scientist on a shared Linux box — told as a single narrative (13
scenarios) and practiced as one lab.

## Files

| Path | Contents |
|---|---|
| [lessons/01-server-anatomy.md](lessons/01-server-anatomy.md) | Workstation vs shared server; the DS directory contract; environments (venv/pip/conda concepts); GPU & CUDA at the administrative level |
| [lessons/02-running-work.md](lessons/02-running-work.md) | tmux/screen; background jobs; Jupyter server & tunnels; process & resource monitoring; shared-server etiquette |
| [lessons/03-data-reproducibility.md](lessons/03-data-reproducibility.md) | Datasets & shared permissions; experiment directories & model files; logs; reproducibility via Git + Docker |
| [lessons/04-scenario-walkthrough.md](lessons/04-scenario-walkthrough.md) | **The 13 scenarios** — the student's first week, narrated with commands and evidence |
| [labs/ds-server-lab.md](labs/ds-server-lab.md) | **"Data Science Linux Server Administration Lab"** — the full practical, 6 phases, CPU-only |
| [practice.md](practice.md) | Quiz + key, challenges C1–C6 |

## The thread (and where each strand comes from)

| The DS reality | The module that taught it |
|---|---|
| Getting on the box, staying connected | M22 (SSH, keys, tmux) |
| Project layout, datasets, permissions | M06/M13/M27 (hierarchy, SGID, project trees) |
| Environments that reproduce | M27 (venv/pip), this lesson 1 (conda concepts) |
| Jupyter headless, tunnels | M27 lesson 2, M21/M22 |
| Long jobs, monitoring, etiquette | M18, M24-clinic, M22 lesson 4 |
| Results, backups, cleanup | M24 lesson 5, M19, this module's scenario 13 |
| Proving it all reproduces | M26, M28, M29 extensions |

## How to use this module

1. Read the three lessons (they consolidate; nothing is genuinely new).
2. Walk the 13 scenarios *as a story* — then the lab makes you do it
   for real, with a second user playing your colleagues.
3. The lab's evidence chain is the deliverable; the quiz tests the
   *why* behind each scenario's commands.
4. Feed your working setup into the [capstone](../../M30-capstone-project/README.md) —
   this module is its warm-up, and its etiquette rules are the
   capstone's operating constraints.
