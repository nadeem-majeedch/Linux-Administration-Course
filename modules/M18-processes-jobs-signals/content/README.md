# Module 18 — Processes, Jobs & Signals · Content Index

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 5 · Software, Storage & Time](../../../COURSE-ROADMAP.md#unit-5--software-storage--time-m16m19).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-5--software-storage--time-m16m19) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> **Status:** Content complete — 3 lessons, 3 labs, quiz + key, 8
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-processes-inspection.md](lessons/01-processes-inspection.md) | PID/PPID, fork/exec, process states, ps, top, htop, pstree, CPU/memory reading |
| 2 | [02-jobs-and-signals.md](lessons/02-jobs-and-signals.md) | Job control (&, Ctrl-Z, jobs, bg, fg, nohup, disown), signals, kill/killall/pkill, TERM vs KILL |
| 3 | [03-priority-and-resources.md](lessons/03-priority-and-resources.md) | nice, renice, load average vs CPU%, memory pressure, OOM, process troubleshooting playbook |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-process-zoo.md](labs/lab-01-process-zoo.md) | Build a process zoo; map it with ps/pstree/top |
| 2 | [lab-02-signal-handshake.md](labs/lab-02-signal-handshake.md) | Trap, observe and escalate signals safely |
| 3 | [lab-03-priority-clinic.md](labs/lab-03-priority-clinic.md) | Nice/renice drills; protect a "Jupyter session" from a batch job |

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M05 terminal & shell](../../M05-terminal-and-shell/content/lessons/05-aliases-and-history.md) —
  job control basics met there; formalized here.
- [M13 shared access](../../M13-ownership-shared-access/content/README.md) —
  who a process runs as.
- [M19 scheduling](../../M19-scheduling-cron-timers/README.md) — automation
  of what you learned to run by hand here.
- [M24 monitoring & logs](../../M24-logs-journald-monitoring/README.md) —
  continuous observation vs point-in-time snapshots.
