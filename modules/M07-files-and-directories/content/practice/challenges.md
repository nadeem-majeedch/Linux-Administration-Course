# Module 07 — Challenge Problems

Log attempts in `lab-log.md`. Destructive steps only on sacrificial trees, with
echo checks shown in the log.

## ★ C1 — The janitor script (manual run)

`~/scratch/janitor/` contains 30 files you create: `run-{1..10}.log`,
`run-{1..10}.tmp`, `data-{1..10}.csv` (brace expansion!). Delete *only* the
`.tmp` files using: ls → echo-check → `rm -i`. Log all three stages. Then
rename `run-*.log` → `archive/` (mkdir first) with one glob.

## ★ C2 — Metadata timeline

Create `event.txt`; stat it. Sleep 5 seconds, append a line, stat again.
Then `mv event.txt event2.txt` — stat: which timestamps survived the rename,
and *why* (inode thinking)? Then `touch event2.txt`: what's the forensic
consequence for "when was this really written?" One paragraph.

## ★★ C3 — The deduplication probe

Create 3 copies of one file (`cp`) and 3 hard links (`ln`). Compare:
`ls -li`, `du -sh .` before/after each round. Write the table: disk cost of
copies vs links; link-count evidence. When would copies be *correct* instead
(mutable second dataset!)?

## ★★ C4 — Rescue the pointer

A teammate's nightly job (M19 preview) writes to `runs/<date>/` and their
scripts read `runs/current`, but the link is dangling. Diagnose (`ls -l`,
`readlink runs/current`), repair, and write the 4-line runbook you'd leave
them (including the `-sfn` rule and a test command).

## ★★ C5 — Glob golf

In a folder with `sales-2026-0{1..9}.csv`, `sales-2025-0{1..9}.csv`,
`returns-2026-0{1..9}.csv`: write globs that select (a) all 2026 sales,
(b) sales+returns for 2026 but *not* 2025, (c) exactly Q1 2026 files. Verify
each with `echo`. Maximize precision, minimize characters — then argue in one
line whether character-count is ever the real objective (no).

## ★★★ C6 — The inode interview

`ls -i /etc/hostname` and `stat` it. Then hard-link it into your home
`ln /etc/hostname ~/hostname-link` — read the error carefully: why did it
fail *before* inode exhaustion even enters the picture? (Hint: same
filesystem? Check `df /etc ~/ | head`.) Write the three-line rule for when
hard links are legal, and the symlink alternative that *would* work — plus
the semantic difference that makes it not-quite-a-replacement.
