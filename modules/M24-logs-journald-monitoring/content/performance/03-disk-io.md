# Disk I/O — iostat, await, and the Slow-vs-Busy Distinction

> Performance Clinic · Module 24 · Difficulty: Advanced
> Reading time: ~25 min · Drill: [Load Clinic](lab-load-clinic.md) (Part C)
> Up next: [Network performance](04-network-performance.md)

---

## 1. Why disk is the invisible bottleneck

CPU saturation announces itself (load average, %us). Memory announces
itself (OOM lines). Disk saturation is quieter: everything just feels
*soggy* — notebooks take seconds to save, shell prompts lag, SSH
sessions stutter — and `top` shows the CPU nearly idle with `wa` creep
(Lesson 1's fingerprint). The instruments that turn "soggy" into a
diagnosis are iostat (sysstat, installed in M24 Lab 3) and the df/du
pair (M17, revisited here as triage).

## 2. iostat: the disk cockpit

```console
$ iostat -xz 2 3
Linux … avg-cpu:  %user %nice %system %iowait %steal %idle
                   2.1   0.0    1.9    38.4    0.0   57.6    ← wa 38%: look below

Device   r/s   w/s   rkB/s   wkB/s  rrqm/s wrqm/s %rrqm %wrqm
         await r_await w_await aqu-sz  %util
sda      4.5 120.1   90.2  96000     0.1   8.0   2.0   6.2
         45.20   8.10   45.80   5.62  98.4          ← the verdict line
```

The columns that matter, in the order you read them:

| Column | Meaning | The question it answers |
|---|---|---|
| `rkB/s, wkB/s` | throughput | *how much* data is moving |
| `r/s, w/s` | IOPS | *how many* operations |
| `await` | avg ms per request (queue + service) | *how fast does the disk feel* |
| `aqu-sz` | average queue depth | is work *piling up* |
| `%util` | fraction of time the device had ≥1 request | is the device *busy* |

**Throughput vs IOPS — the distinction that explains everything.** A
1 GB sequential read is *one* workload (few ops, many MB/s); a database
touching 10,000 tiny rows is another (many ops, few MB/s). Spinning
disks (and cheap virtual ones) handle few IOPS but plenty of MB/s — so
small-random workloads collapse `await` long before throughput looks
impressive. This is why "the disk is only at 10 MB/s!" can coexist with
"everything is slow": you're IOPS-bound, not bandwidth-bound.

## 3. The slow-vs-busy distinction

Two different diseases with different cures:

- **Busy disk** (`%util` high, `await` low-ish, queue draining) —
  saturated but *keeping up*: latency ≈ what the device can do. Fix =
  less I/O, faster device, or schedule around it. Busy is a capacity
  conversation.
- **Slow/unhealthy disk** (`await` high *relative to the device's
  normal*, queue deep, `aqu-sz` > 1–2 sustained) — requests are
  *waiting far longer than this device should take*. Compare against a
  known-good baseline (your Lab C run) — an `await` that doubled
  week-over-week at the same throughput is a hardware/VM-neighborhood
  story, not a workload story.

Practical reference points (order-of-magnitude, your Lab C numbers
override): a healthy SSD/virtual-disk `await` sits in the
sub-millisecond-to-few-ms range under load; double-digit-to-hundreds of
ms means queueing pain. And always read `await` *with* `%util` and
`aqu-sz`: 200 ms await at `aqu-sz` 8 and 99% util is a queue; the same
await with a shallow queue is a slow device.

The ratio `wkB/s ÷ w/s` (average write size) classifies the workload in
one glance: ~1 MB = sequential (big writes), ~4 KB = small-random
(metadata churn, database) — and small-random is the workload that
murders throughput-bound storage.

## 4. df / du: the capacity triage (M17 revisited as diagnosis)

"Disk full" is its own incident class (and the capstone's scenario
list has it). The two-step triage:

```console
$ df -h                                  # WHICH filesystem is full?
Filesystem  Size  Used Avail Use%  Mounted on
/dev/sda1    40G   38G  400M  99%  /          ← the patient

$ sudo du -xh --max-depth=1 / 2>/dev/null | sort -rh | head
38G  /
31G  /home                              ← then descend into the culprit
```

The `-x` (one filesystem) flag keeps `du` from wandering into mounted
media; `sort -rh` (M08's human sort) orders the giants. Two non-obvious
findings to know in advance:

- **Deleted-but-open files**: `df` full, `du` sums to less — a process
  still holds an unlinked log file open, and the space returns only
  when the process closes it (or restarts). `lsof +L1` (awareness) finds
  the holders. The fix order: stop the writer, then clean.
- **inode exhaustion**: `df -h` shows space free, but `df -i` shows
  IUse% at 100% — millions of tiny files (M17's inode lesson) and every
  `touch`/`pip install` fails with "No space left on device" despite
  free gigabytes. The message lies; `df -i` doesn't.

## 5. Bottleneck signatures (disk edition)

| Symptom | Likely story | Confirm with |
|---|---|---|
| high `wa` + high `%util` + deep queue | disk-bound workload | iostat -xz |
| high `await`, low throughput, small avg write | IOPS-bound (small-random) | wkB/s ÷ w/s ratio |
| `df` Use% climbing, nobody admits why | log/output growth | du walk + journald disk usage (M24 §2) |
| `df` says full, `du` disagrees | deleted-but-open files | lsof awareness |
| "No space left" but `df -h` is fine | **inode exhaustion** | `df -i` |
| everything slow, disk idle | it isn't the disk — re-read Lesson 1/2 | vmstat, uptime |

---

## Key takeaways

- Disk trouble hides behind an idle CPU; `wa` and load-without-CPU are
  its telltales (Lesson 1's fingerprint, explained).
- Read iostat as **await + queue + util together**; classify workloads
  by average write size; IOPS-bound ≠ throughput-bound.
- Busy is capacity; *slow* (await vs baseline) is health — different
  conversations.
- Capacity triage: `df` finds the filesystem, `du -xh --max-depth=1`
  finds the giant; know the deleted-open and inode-exhaustion traps
  before they cost an evening.

## Check yourself

1. `iostat -xz`: `await` 4 ms, `%util` 97%, `aqu-sz` 1.2, workload is
   a nightly import. Is the disk sick or just fully employed?
2. `wkB/s` is 8,000 with `w/s` of 2,000. Sequential or small-random,
   and what does that predict about this device's fate under load?
3. `df -h` shows 500M free; `du -xh / | sort -rh` accounts for 20G less
   than the filesystem size. What is the likely mechanism, and why
   doesn't deleting the file help while the writer runs?
4. `pip install` fails with "No space left on device" but `df -h`
   shows 12G available. What is the actual resource, and the check?

*Answers:* (1) Employed — util ~100% with shallow queue and few-ms
await is a busy-but-healthy device; the fix conversation is about
scheduling less I/O, not replacing hardware. (2) ~4 KB average write —
small-random; predict await blow-up (IOPS-bound) long before
throughput numbers look scary. (3) Deleted-but-open: the writer still
holds the unlinked inode open, so the space is allocated until it
closes/restarts; find holders via lsof awareness, stop the writer
first. (4) Inodes — `df -i`; IUse% ~100% from millions of small files.

Up next: [Network performance](04-network-performance.md) — the last
stream, and the one everyone blames first.
