# Lesson 2 — Running Work: tmux, Tunnels, and Watching Your Job

> M31 · Unit 8 companion · Difficulty: Advanced
> Reading time: ~30 min · Up next: [Data & reproducibility](03-data-reproducibility.md)
> Prerequisites: M18 (processes/signals), M22 lesson 4 (tmux/DS workflow), M24-clinic (instruments)

---

## 1. The survival problem: jobs outlive connections

SSH drops. Laptops sleep. Trains go through tunnels. On a workstation,
a killed job costs minutes; on the ML server it costs a week of
training. The survival toolkit, in escalating formality — all M18/M22
skills, now load-bearing:

| Tool | Survives disconnect | Best for | The one command |
|---|---|---|---|
| `nohup … &` | yes | fire-and-forget scripts | `nohup python train.py > train.log 2>&1 &` |
| **tmux** (or `screen`) | yes, *interactively* | everything real | `tmux new -s train` … `Ctrl-b d` … `tmux attach -t train` |
| systemd user unit | yes, + supervision/restart | recurring services | M20's units |

**tmux is the DS server's native habitat**, and its model is worth
restating as the course's: a *session* holds *windows* holds *panes*;
detach (`Ctrl-b d`) leaves it running server-side; reattach from any
SSH session (`tmux attach -t name`) — your terminal becomes a window
onto a session that never noticed you left. The working pattern from
M22 lesson 4, on the ML server:

```console
$ tmux new -s train
$ python train.py 2>&1 | tee train.log        # log to disk AND screen
Ctrl-b d                                       # detach — job keeps running
$ tmux ls                                      # later, from anywhere:
train: 1 windows (created Mon 14:02)
$ tmux attach -t train
```

`screen` is the older twin — same concept, different keys (`Ctrl-a d`
detach) — named here because you'll meet it on older clusters; the
concept transfers, the prefix key doesn't.

**The pairing rule:** tmux gives the *terminal* survival; `tee` (M09)
gives the *evidence* survival. A job in tmux whose output only went
to the screen died to history — the M24 evidence contract applies to
your own runs.

## 2. Launching jobs that behave

Before any long job: the pre-flight (M32-clinic's evidence habit,
turned inward):

1. **Estimate the footprint** — peak RSS from a scaled-down run
   (`time -v`), so the job can't OOM (M24-clinic lesson 2) or evict a
   colleague's cache half the box.
2. **Nice the batch** — `nice -n 10 python …` (M18): interactive users
   keep latency; the scheduler ranks you politely.
3. **Log unconditionally** — `| tee logs/train-$(date +%F).log` with
   the M27 nightly-script conventions (absolute paths, no bare
   `python`).
4. **Checkpoint** — the truncate-then-rename pattern (M27 Q21) per
   epoch; a job that can resume is a job that can share the box.

GPU flavor: check `nvidia-smi` *first* (free memory, who's on which
GPU), and pin your job if the box has a selection convention
(`CUDA_VISIBLE_DEVICES=1`) — the shared-GPU equivalent of not
sprawling across the table.

## 3. Jupyter server concepts on a shared box

M27 lesson 2 taught headless Jupyter with tunnels; the shared server
adds the *administrative* view:

- **Server vs kernel, revisited** — the *server* (one process, one
  port, bound `127.0.0.1`) hosts many *kernels* (one per running
  notebook, each a Python process). On a shared box, kernels are the
  resource leak: an idle notebook holds its kernel's RAM (and GPU, if
  allocated). **Shut kernels down** — the Jupyter "Running" tab is the
  resource manager; lesson 1 §4's caching-allocator point makes GPU
  kernels the priority.
- **The tunnel is the access path** — `ssh -L 9999:127.0.0.1:8888
  ds@server -N` then `localhost:9999`; binding `0.0.0.0:8888` is
  never the answer (M27 Q7's posture, M25's firewall discipline).
- **One server per user, per box** — with `root_dir` pinned to your
  project (M27 Lab 2 §A) and the duplicate-server trap (M27
  troubleshooting #8) in mind: `ss -tlnp | grep 8888` before
  launching.
- **JupyterHub exists** — the multi-user server some departments run
  (one server, everyone gets a spawned single-user Jupyter); its
  *your-side* experience is identical: it's still kernels and
  notebooks over the browser. Recognize it; the admin runs it.

## 4. Watching the job: the monitoring circuit

M24-clinic's instruments, run as a *habit loop* while your job
progresses — in the tmux window, from the second pane:

```console
Ctrl-b %        (split pane; left = job, right = instruments)
$ htop                    # CPU/RAM, your job's share (sorted by CPU)
$ watch -d free -h        # available — the OOM-adjacent trend
$ nvidia-smi              # (GPU boxes) utilization, memory, your PID
$ iostat -xz 2 3          # if it's I/O-heavy: await/util
$ tail -f logs/train-*.log   # the job's own voice — loss curves, epochs
```

The interpretation ladder is M24-clinic's: `us` vs `wa` (compute vs
data-starved), `si/so` (thrash = shrink the workload), peak RSS vs the
box's capacity, and — on GPUs — the memory column vs your allocation
etiquette. **Progress evidence beats vibes**: the log's epoch lines +
the RSS trend + the checkpoint files are the job's heartbeat; when a
colleague asks "how's it going," the answer is a command, not an
adjective.

## 5. The etiquette, mechanized

Lesson 1's list, as checkable rules — each with its instrument:

| Rule | Instrument | Threshold habit |
|---|---|---|
| Look before launching | `htop`, `nvidia-smi` | free cores/RAM/GPU-MiB noted in the log |
| Nice the batch | `nice`/`renice` | +10 for anything >10 min |
| Cap the footprint | `time -v` pre-flight, cgroup/`--memory` if containerized | peak ≤ your fair share |
| Release idle resources | Jupyter Running tab, `nvidia-smi` PID list | no kernel older than your last run |
| Log + checkpoint everything | `tee`, checkpoint files | resume possible after any kill |
| Clean up when done | scenario 13 | outputs archived, scratch purged, tmux sessions killed |

The meta-rule: **your visibility is shared.** Everything you run
appears in everyone's `top`; the researcher who runs pre-flighted,
niced, logged, cleaned-up jobs is the one whose next request gets a
yes.

---

## Key takeaways

- **tmux for everything real** (interactive survival), `nohup` for
  one-shots, user units for services; `tee` alongside tmux so the
  evidence survives too.
- Pre-flight before launch: estimate footprint, nice, log, checkpoint;
  on GPUs — check and pin before you claim.
- Jupyter on shared boxes: one server per user (loopback + tunnel),
  **kernels are the leak** — shut them down; JupyterHub is the same
  experience, administered.
- Monitor as a habit loop (second pane): the log, RSS, `nvidia-smi`;
  etiquette is mechanized — every rule has an instrument.

## Check yourself

1. Your SSH drops 40 minutes into a tmux run. What state is the job
   in, and what do you do on reconnect — precisely?
2. Why is `nohup` insufficient for a training run you want to
   *watch*, and what does the tmux+`tee` pair give that either alone
   doesn't?
3. Colleagues complain the GPU is "full" but `nvidia-smi` shows 3%
   utilization. What is the likely mechanism, and which lesson-2
   rule addresses it?
4. What does the pre-flight estimate (peak RSS) prevent that nice
   does not?

*Answers:* (1) Running — tmux sessions are server-side; reconnect via
SSH and `tmux attach -t train`; the job never noticed. (2) nohup
detaches output from any terminal (and you from the process); tmux
keeps the *interactive* view alive across disconnects while `tee`
duplicates it to disk — tmux alone loses history to the scrollback,
`tee` alone loses the interactive pane. (3) The caching allocator:
idle notebooks/kernels hold GPU memory without using it (3% util, high
MiB); the "release idle resources" rule — shut down kernels, exit
processes. (4) OOM and cache-eviction on the *host* — nice changes
scheduling priority, not memory footprint; the estimate sizes the job
before it evicts a colleague's work or dies at epoch 14.

Up next: [Data & reproducibility](03-data-reproducibility.md) — where
the datasets, models, and proofs live.
