# Answer Key — Module 18 Quiz

Each answer cites the lesson to revisit.

1. Program = file on disk; process = that program loaded and running with
   kernel bookkeeping; thread = execution unit *within* one process,
   sharing its memory. (L1 §1, §6)
2. PPID = the parent that spawned it; orphans are re-parented to PID 1.
   (L1 §1)
3. `ps aux` (system-wide, with %CPU/RSS/STAT) and `ps -ef` (full format,
   PPID visible) — plus `-o`/`--sort` for targeted queries. (L1 §2)
4. `Rs` = running + session leader; `D` = uninterruptible sleep (I/O).
   (L1 §3)
5. `D` waits in the *kernel* on hardware/NFS; signals queue but aren't
   delivered. Fix the I/O (free the disk/NFS), not the signal. (L1 §3)
6. `M`, `P`, `1`, `u`. (L1 §4)
7. Disk/NFS I/O; confirmed by the `D`-state census
   (`ps axo stat,cmd | grep ^D`) and `iostat %util`. (L1 §3–4, L3 §4)
8. Several — %CPU is per-core-normalized; `TIME` proves cumulative
   compute. (L1 §2, §5)
9. Linux uses spare RAM for cache; `available` is the honest figure.
   (L1 §5)
10. **`pgrep -af pattern`** — `-a` prints the full command line, `-f`
    matches against it, so `train.py --full` and a bare REPL are
    distinguishable *before* any signal. The habit it enforces:
    identify first, kill second (`pkill` without a prior `pgrep -af`
    is shooting in the dark). (L1 §2)
11. The *shape* — independent jobs vs one launcher's children — which
    decides whether you kill the parent, the children, or both. (L1 §6)
12. Sends SIGTSTP → job enters `T` (stopped), tracked by the shell as a
    job. (L2 §1)
13. `kill %2` (job spec). (L2 §4)
14. The terminal sends SIGHUP to its jobs on close; fixes: `nohup CMD &`
    or `disown %1`. (L2 §1–2)
15. nohup = HUP-immune; `> t.log` = stdout to file; `2>&1` = stderr joins
    stdout; `&` = background. (L2 §2)
16. TERM is catchable; a handler flushes buffers, saves checkpoints,
    closes connections cleanly. (L2 §3)
17. SIGINT — to the *foreground process group* of that terminal. (L2 §5)
18. `pgrep -af pattern` then scoped `pkill -u $USER -f pattern`; scoping
    prevents killing other users' identical processes (kernels of other
    people's notebooks). (L2 §4)
19. It's already dead; its parent must `wait()`/reap — kill the parent or
    make it reap; init reaps re-parented zombies. (L1 §3, Lab 1 Part D)
20. −20 (greedy) … +19 (kindest); a normal user may only *increase* nice
    (be kinder) — demanding more would let one user starve others.
    (L3 §1)
21. `renice: failed ... Permission denied`; paths: `sudo renice` (VM) or
    restart the process pre-nicened with `nice -n -5` under sudo.
    (L3 §3)
22. Steps 1–2–3: load (18/8 saturated), CPU (the 700% python is the
    burner), memory (RSS +1 GB/min → OOM trajectory); end state: OOM
    killer kills *someone* (maybe not the culprit). Intervene: renice,
    then chunk/limit, then kill if needed. (L3 §5–6)
