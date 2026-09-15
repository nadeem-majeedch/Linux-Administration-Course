# Module 01 — Labs

Four hands-on labs. Labs 1–3 run on any working Ubuntu system (yours, a lab
machine, or WSL2); Lab 4 builds the environment everything else depends on.

| Lab | Lesson | Title | Environment |
|---|---|---|---|
| [Lab 1](lab-01-identify-your-system.md) | 4 | Identify your system — first read-only commands | any Ubuntu, incl. WSL2 |
| [Lab 2](lab-02-man-page-tour.md) | 6 | Man page tour — documentation as a tool | any Ubuntu, incl. WSL2 |
| [Lab 3](lab-03-first-commands.md) | 7 | First commands — syntax, options, exit codes | any Ubuntu, incl. WSL2 |
| [Lab 4](lab-04-ubuntu-setup.md) | 8 | Ubuntu setup & first login — build your course VM | host machine + VirtualBox/WSL2 |

## The lab-log.md habit

Every lab writes evidence into `~/lab-log.md` (created in Lab 4; use any temporary
file until then). One entry per task: the command, the real output (trimmed is fine),
and one line of what you learned. This log is not bureaucracy — it is the *evidence
trail* the course grades in every module, and by the capstone it doubles as your
personal reference of what you did and why.

## Safety baseline for every lab

- All commands in these labs are **read-only or harmless** unless explicitly marked.
- No `sudo` is needed anywhere in this module (first `sudo` arrives properly
  explained in a later module).
- Destructive commands are never required; if you find yourself typing `rm`, `mkfs`,
  or anything you cannot explain — stop and ask (that rule is Course habit #1).
