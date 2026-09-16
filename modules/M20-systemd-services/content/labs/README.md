# Module 20 Labs — systemd, Services & Boot

> Two labs. Lab 1 builds competence (inspect, operate, create); Lab 2
> builds diagnosis (break → read → fix, three times). Everything
> happens **inside your own VM**, mostly as **user units** (no root).

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-service-circuit.md](lab-01-service-circuit.md) | Inspect real services; operate (start/stop/enable); write + run your first user service | ~50 min |
| 2 | [lab-02-break-and-fix.md](lab-02-break-and-fix.md) | Three deliberate breakages (typo, restart-loop, daemon-reload miss) — diagnose from status + journal, fix each | ~45 min |

Standing safety rules (recap):

- System-level `start/stop/restart` only on your own VM; on shared
  machines use `systemctl --user` (that's what it's for).
- `systemctl status` before every change and after every change —
  evidence, not vibes.
- Never edit vendor files in `/lib/systemd/system`; overrides in
  `/etc` (system) or `~/.config/systemd/user` (user).
- `journalctl` output pasted into `lab-log.md` is the graded evidence.
