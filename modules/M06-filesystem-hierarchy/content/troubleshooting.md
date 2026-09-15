# Module 06 — Troubleshooting Guide

Navigation and layout problems at this stage — diagnosis first, fix second.

## 1. "No such file or directory" — but I *see* the file!

**Diagnose in order:** (1) `pwd` — are you where you think? (2) exact case:
`ls` the parent and compare character-by-character; (3) hidden file? plain
`ls` skips dotfiles — `ls -a`; (4) trailing space in a filename (a classic
from GUI downloads): `ls -b` shows escapes like `file\ .csv`.

## 2. "Permission denied" on `cd` or `ls`

The path exists; your user may not traverse/enter it. This is the permission
system working (M12). For the course: expected on `/root`, `/etc/shadow`,
other users' homes. Not a bug — log it as a finding (Lab 2 does).

## 3. Tab completion does nothing (or beeps)

Multiple matches: double-**Tab** lists them — type one more letter and retry.
No matches: your prefix is wrong (case? typo?). If Tab inserts a literal
`\`-escaped mess, the filename contains spaces/specials — Tab is *protecting*
you by escaping; quoting (M07) handles it.

## 4. I'm lost — which directory am I actually in?

`pwd`. If the prompt disagrees with `pwd`, trust `pwd` (prompts abbreviate;
some show `~` for any dir under home, some truncate long paths). `cd -`
toggles back; `cd` alone goes home — the two "reset" moves.

## 5. `cd` prints nothing and changes nothing

You were already there (or you `cd`'d to the same path by another spelling).
Verify with `pwd`, not by vibes.

## 6. `mkdir: cannot create directory ...: File exists`

Plain `mkdir` refuses existing targets — that's correct behavior. If your
intent is "make it if missing", that's `mkdir -p` (idempotent). If it *still*
errors with `-p`, the target exists as a **file** — `ls -ld` the path: a file
where a directory should be is a real problem to resolve by renaming, not
forcing.

## 7. `tree: command not found`

`tree` is optional software: `sudo apt install tree` (M16 formalizes; in
lab-restricted settings, `ls -R` is the fallback — noisier but present
everywhere).

## 8. `~` printed literally in output

`~` inside quotes or in some tools' config isn't expanded ("~/data" stays
"~/data"). In shell commands, leave it unquoted or use `$HOME` (M15). In the
course's scripts: absolute paths end the debate.

## 9. I created files but can't see them in the GUI file manager

Either they're hidden (dot-prefixed), or you're in a different directory than
the GUI shows (the GUI has its own current directory!). `pwd` + `ls -a` in the
terminal is the truth; M07's `find` will locate strays.

## 10. Deleted/renamed my project directory by accident (early panic)

M07 hasn't armed you with `rm` yet, but GUI deletions happen. Do **not** write
new data to the disk. Tell the instructor immediately; restore from the VM
snapshot (M01 Lab 4) if it's a VM; on WSL2, check the Windows Recycle Bin for
`/mnt/c` files. Prevention: the course's `raw/`-never-modified rule plus
snapshots — this is why both exist.
