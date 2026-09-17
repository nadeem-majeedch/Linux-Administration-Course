# Memory & Swap — `free` Decoded, Page Cache, and the OOM Sequence

> Performance Clinic · Module 24 · Difficulty: Advanced
> Reading time: ~25 min · Drill: [Load Clinic](lab-load-clinic.md) (Part B)
> Up next: [Disk I/O](03-disk-io.md)

---

## 1. `free`: the most misread number in Linux

```console
$ free -h
               total   used   free   shared  buff/cache   available
Mem:            7.8Gi  2.1Gi  3.9Gi   118Mi       1.8Gi      5.4Gi
Swap:           2.0Gi     0B  2.0Gi
```

The trap: *"free is low, we need more RAM!"* — read the **right**
columns:

- **`free`** — memory nobody at all is using. Linux hates waste, so it
  grabs spare RAM for the **page cache** (copies of disk blocks, so
  re-reads of your 2 GB dataset come from memory, not disk). That cache
  is `buff/cache`.
- **`available`** — the honest number: what could be handed to a new
  process *right now* without swapping, counting reclaimable cache.
  **Diagnose memory pressure from `available`, never from `free`.**
- **`used`** — genuinely allocated (minus cache). High `used` + high
  `available` = healthy busy; low `available` = real pressure.

`watch -d free -h` while a workload runs shows the page cache growing —
that's Linux *accelerating* your next read, not a leak.

## 2. Swap: size on disk, *activity* in memory

The swap row is two different diagnoses:

- **Swap *size* used** (`used` > 0) — some pages were swapped out at
  some point. On a long-running box this can be old, cold pages: not
  automatically a problem.
- **Swap *activity*** (`vmstat`'s `si`/`so` columns — swapped-in /
  swapped-out per second) — pages **moving** right now. Nonzero `si/so`
  sustained = the machine is actively thrashing memory to disk, and
  everything feels slow. **Activity is the symptom; size is history.**

```console
$ vmstat 2 5
procs -----------memory---------- ---swap-- -----io---- ...
 r  b   swpd   free  buff cache   si   so    bi    bo
 1  0      0 4.0G  ...    0    0    12    20     ← si/so = 0: no thrash
 2  0 1048576  200M  ...  240    8   300   210     ← moving: pressure
```

(`swpd` > 0 with `si/so` = 0: dormant. Fine. `si/so` churning: the
symptom that means *now*.)

## 3. The OOM sequence: how memory exhaustion actually ends

Memory pressure escalates in stages, and knowing the order turns a
mystery into a timeline:

1. **Page cache reclaimed** — cache shrinks to make room (harmless).
2. **Anonymous pages swapped out** — `si/so` activity begins
   (everything slows).
3. **kswapd churn** — the kernel's reclaim daemon saturates a core.
4. **OOM killer** — no reclaimable memory left; the kernel SIGKILLs the
   process with the highest "badness" score — usually your
   40 GB `groupby`.

The post-mortem is the M24 Lesson 1 skill, now aimed at the kernel:

```console
$ journalctl -k --since -1h | grep -iE "oom|out of memory"
Out of memory: Killed process 5432 (python3) total-vm:42381760kB ...
$ dmesg -T | grep -i oom          # the same, timestamped
$ journalctl -k -g "oom-kill" -o short-precise   # -g: message grep
```

The OOM line names the victim, its PID, and its size — which is how a
"my notebook just died" ticket becomes a documented finding in one
command. (M28's container exits 137 are the cgroup-flavored version of
this same killer.)

## 4. Reading a workload's memory character

```console
$ ps aux --sort=-%mem | head -8          # top memory residents, one-shot
$ pidstat -r 2 3                         # per-process: RSS, major/minor faults
$ /usr/bin/time -v python3 job.py | grep Maximum   # peak RSS for the run
```

- **RSS** (resident set) — what the process holds in RAM *now*.
- **VSZ/total-vm** — its *address space*, including mmapped files and
  untouched reservations — always bigger, often meaningless for
  diagnosis (a 42 GB total-vm may mmap a large file it barely touches).
  Quote RSS; be suspicious of VSZ-based panic.
- **Major faults** (pidstat `-r`'s `majfl/s`) — page-ins from disk: the
  process is re-reading swapped-out or file-backed pages. Rising during
  a run = the memory/disk boundary in motion.

Python-specific intuition: pandas/numpy RSS is *spiky* — a `groupby`
can double a process's footprint for one operation. Peak RSS (not
current) is the number that must fit the box; that's why `time -v`
belongs in every DS workload's toolkit.

## 5. Bottleneck signatures (memory edition)

| Symptom | Likely story | Confirm with |
|---|---|---|
| `available` trending to 0 | genuine pressure building | `watch -d free -h` |
| `si/so` sustained non-zero | **thrashing** — the box is swapping actively | `vmstat 2` |
| process vanished mid-run | OOM killer | `journalctl -k -g oom` |
| box sluggish, CPU mostly idle, load high | swap churn (waiting on swap I/O) | vmstat `si/so` + `wa` |
| `used` high but cache high too, `available` fine | healthy — page cache at work | free -h |
| RSS creeps up over hours, never falls | true leak (or growing cache of results) | `pidstat -r` trend |

**Swap strategy in one paragraph (admin conversation, not a lab task):**
swap exists to absorb spikes and to let the kernel evict genuinely cold
pages; on SSD-backed VMs modest swap + default swappiness is sane. The
clinic's rule is behavioral: *if `si/so` is sustained, the box is over
committed* — the fix is a smaller workload, a capped container
(`--memory`, M28), or more RAM — decided with the numbers, and the
numbers come from this lesson's instruments.

---

## Key takeaways

- Diagnose from **`available`**, not `free`; page cache is Linux being
  efficient, not a leak.
- Swap **size** is history; swap **activity** (`si/so`) is the symptom.
- The OOM sequence ends in a kernel log line that names the victim —
  `journalctl -k -g oom` converts mystery death into documented finding.
- Quote **RSS** (and peak RSS from `time -v`), not VSZ; pandas spikes
  make peak the operative number.

## Check yourself

1. `free -h` shows `free: 300M`, `available: 5.2G`. Memory problem?
   Justify in one sentence.
2. `swpd` = 1 GB but `si/so` = 0 for minutes. What happened, and is it
   a problem?
3. A teammate's notebook "disappeared" overnight. Which command pair
   finds the verdict, and what would the key line look like?
4. Why is VSZ a misleading number for pandas workloads, and which two
   numbers do you quote instead?

*Answers:* (1) No — `available` is what matters; most of `free` was
page cache that can be reclaimed instantly. (2) Pages were swapped out
at some point and are now dormant (cold); activity is zero, so it's
history, not pressure. (3) `journalctl -k --since last night | grep -i
oom` (or `dmesg -T | grep -i oom`); expect `Out of memory: Killed
process <pid> (python3) …`. (4) VSZ includes mmapped files and reserved
address space never touched; quote RSS for "now" and `time -v`'s
maximum resident set for "peak".

Up next: [Disk I/O](03-disk-io.md) — where `wa` comes from, and what
`await` really means.
