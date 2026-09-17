# M31-Clinic — The Data Science Server (Capstone Companion)

> Unit 8 · Capstone companion · Difficulty: Advanced
> Prerequisites: M18–M29 chain, the two clinics (Performance/Troubleshooting, M29 extensions)
> Note: *numbered* M30 is the Capstone Project — this directory is its
> hands-on companion: the whole course, walked as a data scientist's real
> first week on a shared ML server.

## What this module covers

The course's integration module: Linux administration *as* the daily
data-science workflow. One narrative — **13 scenarios from "you just
got an account on the ML server" to "your experiments are backed up and
the box is clean"** — threads every prior skill into one practice:
SSH, project layout, environments, data with permissions, Jupyter over
tunnels, experiments under tmux with resource monitoring, results,
backups, and cleanup. GPU/CUDA is taught at the *administrative* level
(detection, drivers, monitoring, sharing etiquette) with **CPU-only
alternatives throughout** — no expensive hardware required anywhere.

**Start here:** [content/README.md](content/README.md) — the module index.

| Piece | What you get |
|---|---|
| [Lesson 1 — anatomy of a DS server](content/lessons/01-server-anatomy.md) | Workstation vs shared server, the DS directory contract, environments (venv/pip/conda concepts), GPU/CUDA admin-level |
| [Lesson 2 — running work](content/lessons/02-running-work.md) | tmux/screen, background jobs, Jupyter server & tunnels, process/resource monitoring, etiquette |
| [Lesson 3 — data & reproducibility](content/lessons/03-data-reproducibility.md) | Datasets (shared + permissions), experiment directories, model files, logs, Git + Docker reproducibility |
| [The 13 scenarios](content/lessons/04-scenario-walkthrough.md) | The student's first week, narrated step by step |
| [The Lab](content/labs/ds-server-lab.md) | **"Data Science Linux Server Administration Lab"** — the full practical, CPU-only, staged in phases |
| [Practice](content/practice.md) | Quiz + key, challenges |

## Safety contract

- The "ML server" is **your own VM** (a second user account plays the
  other researchers); every scenario runs there — no shared university
  systems, no cloud spend, no GPUs required
- CPU-only paths provided for every GPU concept (`sklearn`/small
  `torch` workloads stand in for CUDA workloads)
- Nothing is installed outside venvs; no system services beyond your
  own user units; cleanup is an explicit, evidenced scenario (13)

Definition of done: all 13 scenarios walked in the lab with evidence;
the reproducibility chain (fresh clone → pinned env → same numbers)
demonstrated; quiz ≥ 16/22.

Module links: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md) ·
[M30 Capstone](../M30-capstone-project/README.md) ·
[projects/capstone/](../../projects/capstone/README.md)
