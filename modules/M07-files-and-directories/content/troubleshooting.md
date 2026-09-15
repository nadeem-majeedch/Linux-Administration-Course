# Module 07 — Troubleshooting Guide

File-operation failures and near-misses at this stage.

## 1. "No such file or directory" during cp/mv/rm

Classic causes: wrong cwd (`pwd` first); case mismatch (`ls` the parent);
the file was in a *different* directory than remembered; glob matched nothing
so the literal `*.csv` was passed (Lab 1 Part 3 behavior). Check all four in
that order.

## 2. "Permission denied" on delete/copy

You lack write permission on the *directory* containing the entry (deletion is
a directory-table operation) or read on the file. Expected for root-owned
areas (/etc, /var); unexpected in your own home means ownership oddities —
`ls -l` the file, note owner (M12's territory).

## 3. Overwrote a file with cp/mv — recovery

No trash can exists. Recovery ladder: (1) stop modifying; (2) VM snapshot
rollback (M01 Lab 4) if nothing valuable happened since; (3) editor backup
files (`ls *.bak`, `~file`), M08's `sed -i.bak` pattern, M15's dotfile backups;
(4) real backups (M24). Then fix the process: `-i` flags until habits harden,
dated archives before risky operations — Lab 1's workflow.

## 4. Deleted the wrong files with a glob

Immediately stop writing to the disk. Assess: `ls` the directory against any
baseline (your lab log *is* the baseline — this is why labs record it).
Restore from snapshot/archive; if on shared storage, tell the admin *before*
attempts (their backups have better odds than your improvisation). Prevention:
echo ritual, `-i`, and never globbing through variables unverified.

## 5. "Text file busy" when moving/replacing a running program's file

A process has the file open for execution. Stop the process (M18's tools) or
replace-then-swap (write new, `mv` over — atomic-ish, M11's trick).

## 6. Filename with spaces/specials breaks every command

`ls -b` reveals the truth (`my\ file.txt`). Quote it consistently — or rename
it out of its misery: `mv "my file.txt" my-file.txt`. For globbing such names:
globs match them fine; it's the *hand-typed* paths that need quoting.

## 7. `cp: cannot stat 'source': No such file` — but source exists!

Trailing-slash subtleties on directories, or you meant the *contents*
(`cp -r dir/. dest/` vs `cp -r dir dest/`); also Tab-completion silently
accepting a similarly-named sibling. `ls` both endpoints before re-running.

## 8. Dangling symlink breaks a script

`ls -l` shows the arrow, `cat` says "No such file or directory" — target moved
or deleted. `readlink FILE` prints the stored path; `find -xtype l` (M09)
audits a whole tree. Fix by rebuilding the link (`ln -sfn`) to the target's
new home; fix the *process* by pointing at stable paths.

## 9. Disk full but `du` says my folders are small

Something else ate the volume — logs, package caches, another user's
directory. `df -h` (which volume?), then `du -xh --max-depth=1 / 2>/dev/null |
sort -h | tail` style drilling (M17's full toolkit). Don't improvise deletions
in system areas.

## 10. `rm -i` asks for EVERY file — annoying!

Good — it's working. Reduce the friction by narrowing globs (fewer prompts =
tighter pattern), not by reaching for `-f`. The day `-f` feels *normal* on
shared data is the day to re-read Lesson 1 §4.
