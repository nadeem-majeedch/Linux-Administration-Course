# CPU Performance — Load Average, Run Queues, and Bottleneck Signatures

> Performance Clinic · Module 24 · Difficulty: Advanced
> Reading time: ~25 min · Drill: [Load Clinic](lab-load-clinic.md) (Part A)
> Up next: [Memory & swap](02-memory-swap.md)

---

## 1. Load average: the number everyone quotes and few decode

```console
$ uptime
 14:32:01 up 6 days,  3:14,  2 users,  load average: 2.85, 1.40, 0.62
```

Three numbers = exponentially decayed averages over **1, 5, and 15
minutes**. The shape tells a story before the magnitude does: `0.62 →
1.40 → 2.85` (rising toward now) means load is *arriving*; the reverse
means it's *draining*; flat means steady state. Read them right-to-left
as a trend line, not as three separate facts.

**The only rule that makes load average meaningful: divide by cores.**

```console
$ nproc                      # your VM: e.g. 4
```

- load < cores → there is headroom; work is being scheduled fluidly.
- load ≈ cores → the CPU is fully employed — busy but healthy.
- load ≫ cores (say 2×+) → **saturation**: runnable work is queueing.

Critical subtlety (and the reason load average is *not* "CPU usage"): on
Linux, load counts **uninterruptible tasks too** — processes stuck in
disk (or network) waits count as load. A load of 8.0 on 4 cores with
`top` showing 20% CPU is not a paradox; it's a *disk* story queueing
tasks into the load figure. Lesson 3's traffic-analogy holds: load is
"cars on the road", including the ones stuck at a red light that isn't
the CPU's.

```console
$ cat /proc/loadavg          # the raw source uptime reads
2.85 1.40 0.62 3/987 12345   # 1m 5m 15m running/total-tasks latest-pid
```

That middle field — `3/987` — is the run queue in its most honest form:
3 runnable now out of 987 tasks on the box.

## 2. top and htop: the CPU cockpit

Lesson 3 introduced `top`; the CPU-specific rows deserve decoding:

```
%Cpu(s): 12.5 us,  3.1 sy,  0.0 ni, 82.1 id,  1.8 wa,  0.0 hi,  0.5 si,  0.0 st
```

| Field | Meaning | Why you care |
|---|---|---|
| `us` | user CPU (your code) | pandas, Python — "the workload itself" |
| `sy` | system CPU (kernel) | high `sy` = syscall-heavy or contention |
| `ni` | niced CPU | M18's nice-19 burners show up *here* |
| `id` | idle | headroom |
| `wa` | **iowait** | CPU idle *with* pending disk I/O — the "it's the disk" tell |
| `hi/si` | hardware/software interrupts | usually noise; spikes = driver/NIC work |
| `st` | steal | hypervisor took our time (cloud VMs) |

**The signature to memorize:** high load + high `wa` + moderate `us` =
the CPU isn't the bottleneck; it's *waiting on the disk* — take the
diagnosis to Lesson 3's iostat. High `us` with low `id` and a short run
queue = a genuine CPU-bound workload.

Per-process lines: `top -b -n1 | head -20` or better, sort views:

```console
$ top -o %CPU -b -n1 | head -15        # sorted by CPU, one snapshot
$ htop                                  # F6 sort, F5 tree — PIDs as a family tree
$ ps aux --sort=-%cpu | head -8         # the one-shot, scriptable view
$ pidstat -u 2 3                        # (sysstat) per-process CPU over intervals
```

htop's tree view (F5) earns its keep when a *child* burns CPU but the
*parent* is the decision-maker: kill the parent, orphans usually follow.

## 3. `time`: measuring a workload, not a moment

`top` samples; `time` bills a whole run. The three fields:

```console
$ /usr/bin/time -v python3 analysis.py      # the full-featured build (not the shell builtin)
  User time (seconds): 41.23                 # CPU spent in your code
  System time (seconds): 8.01                # CPU spent in the kernel for you
  Percent of CPU this job got: 198%          # ~2 cores' worth — it parallelized
  Elapsed (wall clock) time: 24.85           # what the user felt
  Maximum resident set size: 1843120 KB      # peak memory — the OOM-adjacent number
```

The ratio tells the workload's character:

- **`%CPU ≫ 100%`** → multi-threaded (numpy BLAS eats cores by design).
  Your "Python script" on 4 cores may legitimately saturate the VM — and
  that's a *configuration* surprise for colleagues, not a bug.
- **wall ≫ user+sys** → the process spent most time *waiting* (I/O,
  network, sleep) — CPU tuning won't help; look at disk (Lesson 3) or
  the network stream.
- **user ≫ sys** → compute-bound; sys ≫ usual → syscall thrash (tiny
  I/O operations, socket churn).

`/usr/bin/time -v` beats the shell builtin because `-v` adds peak RSS —
the number that predicts OOM-killer encounters before they happen.

## 4. Bottleneck signatures (CPU edition)

| Symptom | Likely story | Confirm with |
|---|---|---|
| load ≫ cores, `%us` high, `wa` ≈ 0 | genuine CPU saturation | run queue `3/987` field; `pidstat -u` |
| load high, `wa` high, `%us` modest | **disk masquerading as CPU load** | iostat await/util (Lesson 3) |
| one process 100% × N, others starved | un-niced batch crowding interactive work | `renice` (M18) — measure Jupyter latency |
| `%sy` abnormally high | syscall storm (many small I/Os, socket churn) | `strace -c` awareness (admin's tool) |
| `%st` > 5–10% | noisy-neighbor steal on the cloud host | escalate to provider; not your fix |
| load high but CPU near-idle everywhere | uninterruptible waits (disk/NFS) | vmstat `b` column (next lesson) |

**The fix toolkit recap (M18, in CPU terms):** `nice`/`renice` to re-rank
by politeness; `taskset -c 0-1 <cmd>` awareness for pinning; cgroup caps
via containers (`--cpus`, M28) when ranking isn't enough. What this
clinic adds is knowing *which* of these the evidence calls for.

## 5. DS framing: the shared-server CPU conversation

You will be asked — by a PI, a colleague, yourself — "is the box too
busy for my job?" The evidence-first answer:

1. `uptime` → load vs cores (trend included).
2. `top`/`htop` → who owns the CPU; `us` vs `wa` (is it even the CPU?).
3. `/usr/bin/time -v` on *your* workload → does it need cores you'd be
   stealing? Would `nice` protect the interactive users?
4. The verdict cites numbers: "load 7.2/4 cores, 60% `us` from
   `train.py` (PID 5432), 3% `wa` — CPU-bound batch, I'll nice it +10
   and cap at 2 CPUs."

That paragraph is the difference between an admin and someone who once
typed `top`.

---

## Key takeaways

- Load average is a **trend + saturation gauge** (divide by cores), and
  on Linux it includes uninterruptible waits — high load ≠ CPU problem.
- `top`'s CPU row: `us/sy/ni/id/wa/st` — **`wa` is the disk's
  fingerprint on the CPU's report card.**
- `/usr/bin/time -v` bills the whole run: user/sys/wall ratio classifies
  the workload; peak RSS predicts OOM.
- Fix vocabulary: nice/renice for ranking, awareness of taskset/cgroup
  caps for hard caps — chosen by evidence, not habit.

## Check yourself

1. Load 6.0, 4 cores, `top` shows 15% `us`, 45% `wa`. CPU problem?
   Where do you look next?
2. Why does a single-threaded script show `%CPU` ≈ 100% while a numpy
   heavy-lift shows 400% — and which is the "surprise" on a shared box?
3. What does `3/987` in `/proc/loadavg` mean, in plain words?
4. Your nightly job got slower, but `time -v` shows user-time
   unchanged and wall-time doubled. What class of delay is this, and
   which instrument backs it?

*Answers:* (1) No — `wa` 45% is the disk queueing work while the CPU
idles; load counts those waits. Next: iostat await/util (Lesson 3).
(2) BLAS/numpy thread pools use all cores by design; the *surprise* is
the multi-core one — single-threaded 100% is expected, 400% on a shared
box needs a conversation (or cgroup caps). (3) 3 tasks runnable right
now, out of 987 total tasks on the machine. (4) Waiting, not computing
— I/O latency; `time -v`'s wall vs user gap + iostat await confirm it.

Up next: [Memory & swap](02-memory-swap.md) — where "free" is the most
misread number in Linux.
