# Module 18 Labs — Processes, Jobs & Signals

> Three labs, escalating. All run as your normal user on your own
> VM/WSL2; the only sudo is one optional `renice` check marked in Lab 3.
> Everything self-generates its workload — no downloads.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-process-zoo.md](lab-01-process-zoo.md) | Build & map a process tree with ps/pstree/top | ~40 min |
| 2 | [lab-02-signal-handshake.md](lab-02-signal-handshake.md) | Trap, observe and escalate signals; safe kill drills | ~40 min |
| 3 | [lab-03-priority-clinic.md](lab-03-priority-clinic.md) | nice/renice drills; protect a "Jupyter" from batch load | ~35 min |

Standing safety rules (recap from the lessons):

- TERM before KILL; `pgrep -a` before any pattern kill.
- Every kill in these labs targets a process **you started**, by PID you
  verified twice.
- Burner scripts are pre-nicened where marked; keep them in their own
  terminal so Ctrl-C is always available.
- Record evidence in `lab-log.md` — this module's labs are graded on the
  transcript, not the outcome.
