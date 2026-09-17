# Drill Card 4 — "CPU Saturated"

> Scenario family: System · Difficulty: ●●○
> Source modules: [M18](../../../M18-processes-jobs-signals/README.md), [M24 Clinic lesson 1](../../../M24-logs-journald-monitoring/content/performance/01-cpu-performance.md)

## Symptom

Load at or above core count, interactive things (shell, notebook)
stutter, or the "who is eating the CPU" question from a colleague.

## Decision tree

```text
uptime ÷ nproc → saturated?
├─ wa high            → not CPU: disk (card 2's fork / iostat)
├─ %ni ≈ all of us    → polite batch: WHO, and is ranking right?
├─ one PID ≈ 100×N    → who owns it, expected or runaway?
└─ %sy abnormally hi  → syscall storm (many small I/Os / socket churn)
```

## Evidence

```console
$ uptime; nproc                       # the ratio and its divisor
$ top -b -n1 | head -15               # the CPU row + top processes
$ ps aux --sort=-%cpu | head -8       # the one-shot ranking
$ pidstat -u 2 3 | tail -15           # per-process over intervals (sysstat)
$ cat /proc/loadavg                   # the run-queue field 3/987
```

## Fix pattern

- **Expected workload, wrong ranking** → `renice -n 10 -p PID` (M18):
  interactive work keeps latency, the batch absorbs contention. Verify
  the *differential* (C2's latency loop), not just the nice value.
- **Runaway/unattended** → confirm the owner (it's *their* process),
  then SIGTERM; escalate to SIGKILL only for the stuck. Census after
  (`pgrep -af`), per M18 habit.
- **The surprise multi-threader** (numpy at 400%) → conversation or
  cap: threadpool env vars (`OMP_NUM_THREADS`), container `--cpus`
  (M28), taskset awareness.
- **Not CPU at all** (wa high) → the fork in card 1; document the
  misdirection.

## Verify

Re-measure the *victim* experience: interactive loop latency (M18
Lab 3's metric) back to baseline while the workload still runs.
Load may legitimately stay high — saturation is fine; *starvation of
interactive work* was the incident.

## Document

Name the owner and the mechanism: *"un-niced 4-thread BLAS job"*
differs from *"fork-bomb in a notebook"*, and the prevention differs
(policy vs canary) accordingly.

**Done when:** you can go from "box feels slow" to *named PID, owner,
and disposition* in ≤ 6 commands — and write the one-sentence verdict.
