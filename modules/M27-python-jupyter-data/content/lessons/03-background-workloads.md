# Lesson 3 — Background Workloads: Training Runs as Linux Jobs

> Module 27 · Unit 7 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 3 — batch workload](../labs/lab-03-batch-scheduling.md)
> Up next: [Lesson 4 — command-line Python](04-cli-python.md)

---

## 1. The training run is a Linux process

An ML training job is nothing mystical: a Python process that runs
for hours, reads files, writes checkpoints, and dies — occasionally
by accident. Everything
[M18](../../../M18-processes-jobs-signals/content/README.md) taught
about processes applies to it: signals, priorities, memory caps,
and the OOM killer's appetite. This lesson assembles the DS-specific
pattern: **run long jobs in the background, with logs, under
caps, and provably recoverable.**

## 2. The three ways to run it — nohup, tmux, user unit

| Mechanism | Survives logout | Reattach/interact | Best for |
|---|---|---|---|
| `nohup ... &` | ✅ | ❌ output only (the log) | fire-and-forget scripts |
| **tmux** | ✅ | ✅ full session | jobs you'll check on ([M22 Lesson 4](../../../M22-ssh-remote-admin/content/README.md)) |
| **systemd user unit** | ✅ (+ boot) | `journalctl`, restart policies | recurring/production jobs |

The nohup pattern, dissected once:

```console
(.venv) $ nohup python train.py > train.log 2>&1 &
[1] 4521
$ disown                                 # detach from this shell's job table too
$ tail -f train.log                      # watch it work
```

`nohup` (no hangup — ignores the SIGHUP a closing terminal sends),
`> train.log 2>&1` (both streams to the log — Lesson 2 of
[M19](../../../M19-scheduling-cron-timers/content/README.md)'s
redirect order), `&` (background). The PID is captured at launch —
**write it down**; it's the handle for everything later. The
choice rule from M22 stands: *tmux for work you rejoin, nohup for
work you don't*, user units for anything recurring.

## 3. The script that deserves the background — logging progress

A background job's only voice is its log. The pattern (M24's
greppable contract, running for hours):

```python
# train.py — the DS batch job, Linux-aware
import logging, time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger("train")

for epoch in range(1, 51):
    loss = 1.0 / epoch                                  # the "work"
    log.info("epoch=%d loss=%.4f rss_mb=%d", epoch, loss, mem_mb())
    time.sleep(1)
    if epoch % 10 == 0:
        log.info("checkpoint saved epoch=%d", epoch)
```

Live progress lines (`epoch=`, `loss=`, memory) mean `tail -f
train.log` *is* the training dashboard — and the log is the
post-mortem artifact when it dies overnight
([M24](../../../M24-logs-journald-monitoring/content/README.md)
Lesson 4's incident #2, pre-instrumented). Checkpoint lines make
the restart story cheap: the job that dies at epoch 30 resumes
from 30, not zero.

## 4. Resource caps — dying politely, on purpose

Two caps every background job should carry:

**The M18 courtesy** — batch work yields: `nice -n 19 python
train.py &` keeps interactive use snappy while your job churns
(renice *down* is impossible for non-root — start nice when it's
batch).

**The memory cap** — the OOM killer (M18 Lesson 3) kills the
*fattest* process when RAM runs out, which on a shared server is
often your training job — or worse, someone else's. The
self-limiting forms:

```console
$ systemd-run --user --scope -p MemoryMax=2G python train.py   # one-shot, capped
```

or the [M20](../../../M20-systemd-services/content/README.md) unit
(`MemoryMax=2G` under `[Service]`) for recurring jobs — and for
GPU servers, `CUDA_VISIBLE_DEVICES=1 python train.py` pins the job
to one GPU (the politeness that prevents two jobs fighting over
device 0).

## 5. The overnight-run checklist

The ritual that makes "training died overnight" a five-minute
diagnosis instead of a lost day — each line already taught, now
assembled:

1. **tmux/nohup** — the session survives disconnects (M22).
2. **Log with progress lines** — `tail -f` is your dashboard.
3. **Nice + cap** — batch courtesy, enforced ceiling.
4. **Checkpoints** — resumability at epoch granularity.
5. **The dry-run** — one epoch, foreground, before the 8-hour run
   (M11's dry-run doctrine, ML edition).
6. **Disk headroom** — `df -h` where checkpoints land (M24's
   disk-full incident, pre-empted).
7. **The PID/log path written down** — or in the runbook.

## 6. GPU vocabulary — reading the remote GPU server

Named for recognition (labs are CPU):

```console
$ nvidia-smi                    # the GPU world's top: devices, memory, processes
$ watch -n2 nvidia-smi          # the live view during training
```

Columns that matter: per-GPU memory usage and the *process list*
(your python with its allocation — or someone else's, which is a
coordination conversation, [M24 incident #4](../../../M24-logs-journald-monitoring/content/README.md)
style, not a kill). `CUDA` is the runtime layer PyTorch/TensorFlow
speak; `CUDA_VISIBLE_DEVICES` selects devices; "CUDA out of
memory" in a log is the GPU-flavored OOM — batch size is the usual
dial. On a GPU server, everything else in this lesson (tmux, logs,
caps, checkpoints) transfers unchanged.

## 7. Try it now (20 minutes)

1. The full pattern: write the 50-epoch `train.py` (§3), launch
   under nohup with the checklist's discipline, `tail -f` for three
   epochs, then leave it and come back — log proves continuity.
2. Polite stop: find the PID, `kill` (TERM) it, confirm the log's
   last line and the process table's emptiness — the M18 ladder on
   your own training run.
3. The cap: rerun under `systemd-run --user --scope -p
   MemoryMax=100M` — watch it be killed at the ceiling
   (`journalctl --user` names the cgroup event), and the log's
   abrupt end. Caps witnessed, not theoretical.
4. tmux variant (M22 muscle memory): same job in a tmux session,
   detach, close SSH, reattach, re-detach. The overnight pattern,
   rehearsed in miniature.

## 8. Common mistakes

- Running the 8-hour job in a bare SSH session — the logout-HUP
  (M18) is the classic lost run; tmux/nohup before launch, always.
- `print` instead of logging, unredirected — a background job with
  no log is a job you're guessing about.
- No checkpoints on long runs — the OOM at epoch 49 restarts from
  epoch 0; checkpoint lines are the insurance premium.
- Launching without the dry-run — discover the epoch-3 crash at
  epoch 3, not hour 7.
- Forgetting disk headroom for checkpoints — `df -h` first; M24's
  incident #3 arrives mid-training otherwise.
- Fighting another user's GPU job — `nvidia-smi` shows *who*;
  coordinate (nice/reschedule), never kill (M24 incident #4's
  rule).

> **Up next:** [Lesson 4 — command-line
> Python](04-cli-python.md): the interpreter joining the Unix
> pipeline — one-liners, `-m` idioms, and exit codes.
