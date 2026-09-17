# 20 — Linux for Data Science

> Learn it: [M31 — Data Science Server](../modules/M31-data-science-server/content/README.md) ·
> Lookup, not understanding — this page chains sheets 5, 7, 11, 16, 17
> into one workflow.

## The workstation → server contract

| On your laptop (owner) | On a shared server (guest) |
|---|---|
| install whatever, wherever | venvs in `$HOME`, nothing system-wide |
| one project at a time | nice your jobs, cap your memory |
| kill by closing the terminal | jobs must **outlive** logins (tmux/unit + `nohup`) |
| files are yours | permissions are the commons (SGID dirs, reference-don't-copy datasets) |

Directory contract on ML servers: `$HOME` (code, venvs, small
results) · `/data` (read-only shared datasets) · `/scratch`
(fast, per-user, *purged* — nothing precious lives there).

## The first-week sequence (13 steps, one line each)

```console
$ ssh mlsrv                                    # 1–2  access & connect
$ mkdir -p ~/projects/ds-lab && cd $_          # 3    project directory
$ python3 -m venv .venv                        # 4    environment
$ python3 -m pip install -r requirements.txt   # 5    pinned dependencies
$ git clone git@gitlab.uni.edu:team/repo.git   # 6    the code
$ wget URL && sha256sum -c data.sha256         # 7    dataset, verified
$ jupyter lab --no-browser --ip 127.0.0.1 --port 8889
$ ssh -L 8889:localhost:8889 mlsrv             # 8    tunnel from laptop
$ tmux new -s train && nice -n 10 python train.py   # 9   the run (pre-flight: estimate, nice, log, checkpoint)
$ watch -n30 'free -h; uptime'                 # 10   monitor (second pane)
$ cp -r runs/20260917-0914 ~/results/          # 11   store results
$ rsync -a ~/results/ laptop:backup/           # 12   back them up (then RESTORE-TEST one)
$ pkill -f train.py; tmux kill-session -t train    # 13  cleanup — census first
```

## Pre-flight before any long job

1. **Estimate** runtime & memory (`/usr/bin/time -v python train.py --dry-run`)
2. **Nice** it (`nice -n 10`) — you're a guest
3. **Log** it (`… 2>&1 \| tee logs/run.log`)
4. **Checkpoint** it — periodic state so a kill isn't a restart

## Run directories & evidence (reproducibility)

```text
runs/20260917-0914-cnn-baseline/     # date-time-name, stamped by a launcher script
├── metrics.csv                      # the contract: one row per epoch/step
├── config.json                      # hyperparameters as RUN
├── git_sha.txt                      # code identity
├── requirements.lock                # env identity (pip freeze)
└── data.sha256                      # data identity
```
Six links of reproducibility: code SHA → env pins → data checksum →
stamped config → run dir → **fresh-clone proof** (a classmate
re-runs from the repo alone).

## Monitoring circuit (while it trains)

| Command | Watch |
|---|---|
| `htop` (or `top`) | your PID's CPU%; state `D` = stuck on I/O |
| `free -h` | `available` falling toward 0 = OOM incoming |
| `df -h` | checkpoints eat disk — silent killer #1 |
| `tail -f logs/run.log` | loss/progress actually moving |
| `pgrep -af train.py` | it's alive — and only one of it |

GPU twins (when present): `nvidia-smi` for memory/utilization,
`watch -n1 nvidia-smi`; driver-vs-toolkit mismatch is an
administrative problem (see M31 Lesson 1), CPU-only paths always
exist in this course.

## Long jobs that survive you

| Need | Tool |
|---|---|
| interactive, reattachable | `tmux new -s work` → detach `Ctrl+b d` → `tmux attach` |
| fire-and-forget | `nohup nice -n 10 python train.py > run.log 2>&1 &` |
| real service semantics | systemd **user unit** + `loginctl enable-linger` |
| checkpoint & resume | script checkpoints to `/scratch`, launcher resumes |

## Sharing data the admin way

```console
$ sudo chgrp dsteam /srv/datasets && sudo chmod 2750 /srv/datasets
$ chmod -R g-w /srv/datasets          # datasets: group-READ, never group-write
$ sha256sum dataset.csv > dataset.sha256    # provenance beats copy-trust
```
Reference datasets from `/data` in code — a copy per student is a
storage incident with a delay.

## Backups & cleanup (the habits that end courses)

| Rule | Practice |
|---|---|
| what | code (git), small results (`rsync`/tar), configs — **not** venvs or raw datasets (re-downloadable) |
| verify | a backup is real only after a **restore test** with checksums |
| cleanup (step 13) | kill kernels (`pgrep -af jupyter`), empty `/scratch`, report what remains — leaving zombie processes on a shared server is how you lose lab privileges |

## Pull-together pipeline (the M08 triage move, one line)

```console
$ tail -n +2 results.csv | awk -F, '$3>0 {print $2}' | sort | uniq -c | sort -rn | head
```
Shell triage on the big file *before* pandas ever loads it.
