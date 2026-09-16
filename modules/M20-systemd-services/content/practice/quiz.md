# Module 20 Quiz — 22 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).

1. **R** What runs as PID 1 on Ubuntu, and name three of its
   responsibilities.
2. **R** Six unit types and what each manages — one line each.
3. **U** Where do unit files live (three directories), and which wins?
   Why never edit /lib?
4. **P** Decode: `Loaded: loaded (/usr/lib/systemd/system/cron.service;
   enabled; vendor preset: enabled)`.
5. **R** start vs enable — two orthogonal questions. What is
   `enable --now`?
6. **U** The four-state table (active/inactive × enabled/disabled):
   which quadrant is the "works now, vanishes after reboot" bug?
7. **R** What does `systemctl enable` actually do on disk? (One
   sentence — the symlink story.)
8. **P** The one command that answers "is anything broken right now?"
   on any server.
9. **U** The five status zones and the restart-loop tell (what does
   the Active line look like?).
10. **R** reload vs restart — operational difference, and why it
    matters when you're connected *through* the service.
11. **P** Command: last 20 journal lines for one unit; then follow it
    live; then errors-only since yesterday.
12. **U** What is `systemctl --user`, and what problem does lingering
    solve? What's the resource trade?
13. **P** Write the unit-file section that caps a user service at 2 GB
    memory and 50% CPU.
14. **R** The three unit-file sections and one directive each.
15. **U** Type=simple vs forking vs oneshot — what does each say about
    the ExecStart process? What's the beginner default and why?
16. **P** The bug: a self-daemonizing script + Type=simple +
    Restart=on-failure. What behavior results, and which log line
    reveals it?
17. **R** `daemon-reload`: when is it required, and what symptom
    appears if skipped?
18. **U** Name four hardening directives and what each protects.
    Where do you meet them in the wild?
19. **P** The supported way to change one directive of a vendor unit —
    command, file location, and the undo.
20. **R** The five boot stages, and which two earlier modules act at
    stages 3 and 4.
21. **U** GRUB one-shot edit: what does adding `systemd.unit=rescue.target`
    do, and why is it safe (nothing persists)?
22. **DS** Your training-queue daemon dies nightly. Write the unit
    (Section names + 6 directives) that makes systemd keep it alive,
    capped, and logged — and say where its stdout goes.

## Bonus

23. `systemd-analyze blame` vs `critical-chain` — why is the slowest
    unit not necessarily the one that delays boot?
