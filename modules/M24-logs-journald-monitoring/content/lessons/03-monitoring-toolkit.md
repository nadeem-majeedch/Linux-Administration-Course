# Lesson 3 — The Monitoring Toolkit

> Module 24 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 3](../labs/lab-03-monitoring-under-load.md)
> Up next: [Lesson 4 — the incident methodology](04-incident-methodology.md)

---

## 1. Logs tell you what was said; monitoring tells you what was true

A service can log "job started" and still be starving for CPU; memory
can vanish without a single warning line. **Monitoring** is the
practice of reading the machine's actual state — CPU, memory, disk,
I/O — through tools that *measure* rather than *narrate*.

The organizing frame (from systems-thinking, and worth memorizing):

| Axis | Question | Symptom when saturated |
|---|---|---|
| **Utilization** | How busy is the resource? | High % is fine *if* work flows |
| **Saturation** | Is there queued work waiting? | Latency climbs, load > cores |
| **Errors** | Is the resource failing? | I/O errors, OOM kills, throttling |

"CPU at 95%" alone is *not* a problem — a training run should pin the
CPU. "CPU at 95% **and** load average 12 on 4 cores **and** load
climbing while jobs stall" is a diagnosis waiting in Lesson 4. One
number never tells the story; the axes do.

## 2. uptime and load average — the first glance

```console
$ uptime
 21:32:07 up 3 days,  4:11,  2 users,  load average: 1.85, 2.10, 0.90
```

- **up** — uptime; reboots reset it (and reset `journalctl -b` numbering).
- **load average**: three decayed averages (1, 5, 15 min) of
  *runnable + uninterruptible* tasks. Rule of thumb: compare to core
  count (`nproc`). Load ≈ cores → saturated-but-flowing; load ≫ cores
  → queue growing; load falling across the three numbers → the spike
  already passed.

The 1/5/15 spread is a *trend arrow*: `0.9 → 2.1 → 1.85` means
something spiked ~5 minutes ago. On a DS server, that's your "did the
nightly job run yet?" tell before you read a single log.

## 3. free — memory without illusion

```console
$ free -h
               total    used    free   available  buff/cache
Mem:           7.7Gi   2.1Gi   3.9Gi   5.2Gi      1.7Gi
Swap:          2.0Gi      0B   2.0Gi
```

The column that matters is **available** — memory free *plus* what the
kernel can reclaim instantly (page cache). Linux deliberately uses
spare RAM for file cache, so `free` being small is *healthy*, not
alarming. The mistaken panic — "free is 0, we're out of memory!" — is
the single most common monitoring misread.

Real pressure looks like: available shrinking toward zero **and**
swap `used` climbing **and** (from `vmstat`, §4) steady `si/so`
swapping activity. At that point the kernel's OOM killer (M18, Lesson
3) is the next stop — and your training job is its favorite meal.

**DS connection:** `free -h` before launching a job, `watch -n5 free
-h` during. A job that grows available-memory toward zero in a
straight line has a leak; catching the slope at minute 5 beats
discovering the OOM at hour 5.

## 4. vmstat — the five-second system biography

```console
$ vmstat 2 5            # sample every 2s, 5 samples, then stop
procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa
 2  0      0 3991000 180000 1700000    0    0    12    40  240  410 12  2 85  1
 1  0      0 3988000 180000 1701000    0    0     0   120  230  380 11  2 86  1
```

Columns worth their screen space:

- `r` — runnable tasks wanting CPU. Sustained `r` > cores = CPU saturation.
- `b` — blocked on I/O. Sustained nonzero with high `wa` = disk-bound.
- `si/so` — swap-in/swap-out per second. *Any* sustained activity is
  a memory-pressure alarm (the `free` confirmation of §3).
- `bi/bo` — blocks in/out: disk read/write throughput.
- `us/sy/id/wa` — CPU split: user, system, idle, **iowait**. High
  `wa` = CPU *idle but waiting on storage* — the "why is my data
  load so slow" signature (see [Lab 3](../labs/lab-03-monitoring-under-load.md)).

One command, all four axes — utilization (`us`), saturation (`r`,
`si/so`), and errors surface as anomalies you then chase in logs.

## 5. iostat — per-device I/O (sysstat)

`vmstat` totals the system; `iostat` breaks I/O out **per device** —
essential when one dataset disk is the bottleneck while the system
disk idles. Install once (M16): `sudo apt install sysstat`, then:

```console
$ iostat -x 2 3              # extended stats, every 2s, 3 samples
Device   r/s   w/s   rkB/s   wkB/s  await  %util
sda      2.0   120   64      15360   4.5    68.3
sdb      0.5    2    8       32      1.2     2.1
```

Read: **`%util`** ≈ fraction of time the device was busy (near 100%
= saturated link); **`await`** = average request wait in ms (spinning
disks: tens of ms is normal; if `await` climbs while `%util` pegs,
requests are queueing — saturation on the *device* axis). Compare
devices: in the sample, sda is doing the work and nearing busy; sdb
is idle.

**DS connection:** loading a large CSV or a dataset shard is pure
sequential read — `iostat` during a load tells you whether you're
disk-bound (`%util` pegged, `await` high) or CPU-bound (`wa` ~0, `us`
high). The fix differs completely (fast disk/batch reads vs more
CPU/efficient parsing), and guessing wrong wastes days.

## 6. sar — history when nothing is wrong *right now*

Every tool so far shows *now*. **sar** (also sysstat) replays
*history* — a background collector samples the system every ~10
minutes into `/var/log/sysstat/`:

```console
$ sar -u                     # CPU history for today
$ sar -r                     # memory history
$ sar -u -f /var/log/sysstat/sa15   # a specific day's file
$ sar -q                     # load averages over the day
```

The superpower: *post-hoc correlation*. "The slow period was 14:00–14:30"
becomes `sar -u -s 14:00:00 -e 14:30:00` — you can replay a window
that already ended. Two caveats: sysstat's collector is
**disabled by default** on Ubuntu (enable with
`sudo systemctl enable --now sysstat`; also fine to know it without
running it), and on shared servers history is admin territory — the
lesson's goal is *reading* sar output, which Lab 3 practices against
its own short run.

## 7. df / du — the recap that saves servers

From [M17](../../../M17-storage-and-filesystems/content/README.md), but
restated here because disk-full is the most common *avoidable* outage:

```console
$ df -h                      # filesystem-level: which mount is filling?
$ du -h --max-depth=1 ~ | sort -rh | head    # who inside is the pig?
```

The drill: `df` finds the filling filesystem → `du` narrows within it
→ decide: delete (safely, own files), compress, or move. Watch `df`
*during* big jobs too: a checkpointing training run can fill a disk
mid-run; then writes fail in confusing ways (Lesson 4, incident #3).

## 8. The 60-second health check

The habit this module builds — run top-to-bottom before any long job
on any server:

```console
$ uptime                          # load trend vs nproc
$ free -h                         # available, swap used?
$ df -h /home /tmp                # headroom where jobs write
$ vmstat 2 3                      # r, si/so, wa over 6 seconds
$ journalctl -b -p err.. --no-pager | tail   # anything already on fire?
```

Five commands, one page of output, every axis covered. It's the same
check [Lab 3](../labs/lab-03-monitoring-under-load.md) runs before and
under load, and the skeleton of
[Mini-Project E's](../mini-project-health-backup-kit.md) `health.sh`.

## 9. Try it now (5 minutes)

1. `nproc && uptime` — is your current load sane for your core count?
2. `free -h` — read *available*, not free. Note the difference.
3. `vmstat 2 3` — find `id` (idle) and `wa`. A quiet machine: id ≈
   95–100, wa ≈ 0.
4. `df -h ~` — percent used on your home filesystem. If > 80% on a
   server, that's a ticket to yourself.
5. If sysstat is installed: `sar -u | tail -12` — your machine's day
   in twelve lines. If not: `sudo apt install sysstat` is the M16
   five-beat workflow in action.

## 10. Common mistakes

- Reading `free` instead of `available` — buff/cache is not "used".
- Treating high CPU as an incident — check saturation (`r` vs cores)
  and *whose* CPU it is (M18's `ps` skills) before verdicts.
- Missing iowait: CPU "idle" with high `wa` is *not* idle — the
  machine is starved of data, not work.
- Running `du` on `/` or huge trees casually — it walks everything;
  scope it (home, project dir) or use `--max-depth`.
- Diagnosing from a single sample. Every tool here accepts a repeat
  interval — trends, not instants, are evidence.

> **Up next:** [Lesson 4 — the incident
> methodology](04-incident-methodology.md): turning these readings
> and logs into a repeatable six-step diagnosis, rehearsed on five
> real incidents.
