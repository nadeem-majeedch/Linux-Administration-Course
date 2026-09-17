# Drill Card 3 — "Memory Exhausted"

> Scenario family: System · Difficulty: ●●●
> Source modules: [M24 Clinic lesson 2](../../../M24-logs-journald-monitoring/content/performance/02-memory-swap.md), [M18](../../../M18-processes-jobs-signals/README.md)

## Symptom

Two presentations, different urgency: **(a)** the box is mush — every
interaction lags, disk light (or iostat) busy, CPU idle-ish; **(b)** a
process *died* mysteriously mid-run. (a) is pressure *now*; (b) is the
OOM killer's signature — it already happened.

## Decision tree

```text
free -h → available?
├─ available low, si/so churning (vmstat)  → active pressure: WHO? → ps --sort=-%mem
├─ available fine                          → not memory; back to card 1's fork
└─ process died: journalctl -k -g oom      → the kernel's verdict
```

## Evidence

```console
$ free -h && watch -d free -h        # available trend (Ctrl-C to exit)
$ vmstat 2 5                         # si/so — activity, the real symptom
$ ps aux --sort=-%mem | head -8      # the residents
$ sudo journalctl -k --since -2h | grep -iE "oom|out of memory"   # verdict for (b)
$ dmesg -T | grep -i oom             # same, kernel-ring flavor
```

## Fix pattern

- **Pressure now (a)**: identify the resident (usually one pandas job
  dwarfing the rest); the admin-tier options, *in order of
  politeness*: let it finish if close, ask the owner, `renice` (helps
  interactivity, not RAM), and only then termination — the owner
  decides their job's fate, not the person with the terminal. State
  the blast radius before any SIGTERM (M18's rules).
- **Died mid-run (b)**: read the OOM line (victim, PID, size). The fix
  is the *workload's*: chunk the processing (M27 C7's strategies),
  cap the container (`--memory`, M28), or size the instance up —
  decided with peak RSS from `/usr/bin/time -v`, not vibes.
- **Prevention**: the canary is a threshold alert (cron'd check on
  `available` — M24's health kit) plus the peak-RSS habit in every
  production script.

## Verify

(a): `si/so` returns to 0 and `available` recovers *while the
workload still runs* (that's the proof the fix was structural).
(b): the job re-run in its fixed form completes, with the peak-RSS
number logged against the box's capacity.

## Document

The OOM line itself is the evidence crown jewel — quote it verbatim.
Root-cause vocabulary: *"unbounded in-memory aggregation"*, *"swap
absorbed the spike then thrashed"*, *"no memory cap on the container"*.

**Done when:** you can produce the OOM verdict for a staged kill
(mem_grow with a raised cap) and write the two-line prevention note.
