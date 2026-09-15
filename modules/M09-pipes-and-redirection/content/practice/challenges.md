# Module 09 — Challenge Problems

Log attempts in `lab-log.md`. All safe; corpora are self-generated.

## ★ C1 — One-liner analyst

On `sales.csv` from Lab 2 (or M01's real datasets when they land): produce
(a) row count, (b) distinct-region count, (c) biggest amount, (d) the full row
of the biggest amount (hint: `sort -t, -k4 -rn | head -1` — decode `-t` and
`-k` from `man sort`). Four pipelines, logged.

## ★ C2 — The silent auditor

Write a single `&&` chain that: makes `audit/`, copies `/etc/os-release` and
`/etc/hostname` in, runs `wc -l` over both, and only then prints "audit
complete". Break it mid-chain (bad filename) and log the short-circuit.

## ★ C3 — Stream choreography

One command: `cmd` = `ls /etc /nope`. Produce three files — `ok.txt`
(stdout), `err.txt` (stderr), `both.txt` (interleaved) — using the same
command three times with different redirections. Then prove which of
`ok.txt`/`err.txt` is empty. Why is `both.txt` non-deterministic in *order*
across commands?

## ★★ C4 — The log rotation drill

Build `app-{1..5}.log` (different contents via `echo run-N > ...`). Create
one pipeline that finds the two *largest* logs by bytes (`ls -l | sort -k5 -n
| tail -2`) and one that finds all logs modified today (`ls -lt | head`).
Then the rotation: `mv`-archive the largest two into `archive/` — echo-checked
— and verify `archive/`. You've just done M24's rotation shape manually.

## ★★ C5 — The latest pointer, served by pipeline

Combine M07's symlink pattern with this module: `runs/` has three dated dirs
(build them). One command flips `runs/current` to the newest *by name*
(`ls runs | sort | tail -1` → substitution → `ln -sfn`). Then pipeline-build
the *flip log line* appended to `flip.log` with `date` + the new target.
Automation-grade: run it twice; `flip.log` grows twice.

## ★★★ C6 — xargs initiation

Preview the module's end: `ls *.log | xargs wc -l` — total lines per log plus
`total`. Compare with `wc -l *.log` (glob). Then the dangerous shape:
`ls | xargs echo rm` — observe what *would* run, in perfect safety because of
`echo`. Write the two-line safety rule for xargs + rm that M09's full module
will formalize (`-I`/`-0` and printing before doing).
