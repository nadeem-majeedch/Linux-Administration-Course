# Drill Card 1 — "The Server Is Slow"

> Scenario family: System · Difficulty: ●●○
> Source modules: [M24 Performance Clinic](../../../M24-logs-journald-monitoring/content/performance/README.md), [M18](../../../M18-processes-jobs-signals/README.md)

## Symptom

"Everything takes forever" — shell prompts lag, notebooks spin, no
specific error. The most common and most vague ticket in existence.

## Decision tree

```text
uptime  →  load vs cores?
├─ load ≪ cores        → not CPU; check disk & memory first
├─ load ≈ cores, wa≈0  → genuinely busy: WHO owns it? → pidstat/top
├─ load ≫ cores, wa hi → disk masquerading as CPU → iostat
└─ load ≫ cores, CPU idle, si/so churning → swap thrash → memory
```

## Evidence (read-only, in this order)

```console
$ uptime; nproc                        # trend + the divisor
$ vmstat 2 3                           # r, b, si/so, wa — all four resources' tells
$ top -b -n1 | head -12                # us/sy/ni/id/wa + who owns CPU
$ free -h                              # available, not free
$ iostat -xz 2 3                       # await, aqu-sz, %util
```

## The fork

| The numbers say | Go to |
|---|---|
| one process, high `%us` | [CPU saturated](04-cpu-saturation.md) |
| `si/so` sustained | [Memory exhausted](03-memory-exhausted.md) |
| `await`/`%util` pinned | [Disk full](02-disk-full.md) or I/O-bound |
| CPU/memory/disk all quiet | [Network](08-connectivity-failure.md) — "slow" was felt latency |

## Fix pattern

Follow the fork — the general ticket's job is *to become a specific
one*. The fix is whatever card the evidence names.

## Verify

The original complaint was subjective; the verification is
objective: re-run the *user's action* ("open the notebook", "run the
cell") and time it; re-capture the four-instrument sweep. Before/after
numbers in the journal.

## Document

One line worth keeping: *"slow = resource until proven otherwise —
and the four-command sweep names it in under a minute."*

**Done when:** you can fork this ticket to a specific card in ≤ 5
commands, citing load/`wa`/`si/so`/`await` for the branch taken.
