# Mini-Project F — Reproducible Mini-ML (M27)

> Module: M27 — Python, Jupyter and Data Workloads · Unit 7 · Difficulty: Intermediate
> Prerequisites: M16, M15, M10, M26; M27 in progress

## Brief

Prove you can do a complete, *reproducible* ML task on Linux the way it would run
on a shared server: pinned environment, scripted execution, logged run, saved
artifact, clean history — and no sudo anywhere.

## Deliverables

A Git repository (your own, hosted where your class specifies) containing:

1. **`requirements.txt`** — pinned versions (`pip freeze` of a venv you built);
   recreating the venv from it must work on a fresh account.
2. **`train.py`** — a small supervised task on `datasets/sensor-telemetry.tsv`
   (e.g., next-reading regression or a two-class synthetic target derived from
   thresholds): scikit-learn only, runs in < 2 minutes on CPU.
3. **`run.sh`** — the one-command entry point:
   - creates/uses `.venv`, installs from `requirements.txt` if missing
   - activates, runs `train.py`, tees output to `logs/train-<timestamp>.log`
   - copies the final model artifact to `artifacts/model-<timestamp>.joblib`
   - strict mode, argument validation, `shellcheck` clean
4. **`logs/` and `artifacts/`** — one real run's evidence (log + model file;
   the log must show versions and timing).
5. **`README.md`** — task, data, environment, how to run, what the artifacts are,
   and a short "reproducibility statement": what is pinned, what is not, and why.
6. **Clean Git history** — small commits with real messages; `.gitignore`
   excluding `.venv/`, `logs/`, `artifacts/`, data bulk files.

## Constraints

- **No sudo anywhere.** Everything lives in your home directory — this mirrors
  shared-server reality and is part of the grade.
- No notebooks in the deliverable (notebooks are for exploration; this is the
  runnable pipeline). You may explore in a notebook first, then convert.
- The run must be repeatable: a classmate running `./run.sh` on a fresh clone
  gets the same artifact (up to library nondeterminism, which your README notes).

## Rubric

| Criterion | Weight |
|---|---|
| Environment pinning actually recreates (tested on a fresh account) | 25% |
| run.sh robustness (idempotent, strict mode, shellcheck) | 20% |
| Run evidence: log + artifact present and consistent | 20% |
| README + reproducibility statement | 15% |
| Git hygiene | 20% |

## Stretch goals

- Wrap the whole thing in a Docker image (M28 preview): `docker build` + `run`
  producing the same artifact.
- Add a watchdog CSV (Mini-Project C) of the training run to `artifacts/`.
