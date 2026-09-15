# Module 14 Labs — sudo & the Root Principle

> Two labs. Both run **inside your own VM/WSL2 instance**. Nothing in this
> module requires or touches a shared server.

| # | Lab | Focus |
|---|-----|-------|
| 1 | [lab-01-sudo-practice.md](lab-01-sudo-practice.md) | Policy, logging, redirection wall, scoped drop-in, safe break-and-repair |
| 2 | [lab-02-sudo-incidents.md](lab-02-sudo-incidents.md) | Diagnose three real-world sudo failure tickets |

General safety notes:

- Record all work in `lab-log.md`; evidence over memory.
- Never disable or re-password the root account as part of an experiment.
- `visudo`/`visudo -f` only — never a plain editor on sudoers.
- If sudo breaks in your VM: recovery mode (GRUB) or `wsl -u root` —
  practiced once in Lab 1 Part E so it's routine, not panic.
