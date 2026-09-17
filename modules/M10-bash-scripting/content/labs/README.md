# Module 10 Labs — Bash Scripting

> Two labs, everything under `~/lab10/`. Scripts write only inside
> their scratch directory; the one `rm` in the course of the labs is
> guarded by the `${var:?}` pattern taught in
> [Lesson 5](../lessons/05-debugging-quality.md). Every finished
> script: `bash -n` clean, `shellcheck` clean.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-fix-the-bugs.md](lab-01-fix-the-bugs.md) | Eight broken scripts: quoting, word splitting, exit codes, while-read traps — diagnose, fix, explain | ~50 min |
| 2 | [lab-02-build-dq-toolkit.md](lab-02-build-dq-toolkit.md) | Build `dq.sh` from zero: arguments, guards, strict mode, logging — the Lab 1 lessons in a working tool | ~50 min |

Standing rules (recap):

- Strict mode (`set -euo pipefail`) in every script from the first line on.
- `bash -n` before first run; `shellcheck` before calling it done.
- Transcripts in `lab-log.md`: the bug *symptom*, the diagnosis
  command, the fix, and a one-line "class of bug" note.
- No downloads, no system changes, no files outside `~/lab10/`.
