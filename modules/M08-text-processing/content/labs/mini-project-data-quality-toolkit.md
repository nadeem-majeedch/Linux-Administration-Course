# Mini-Project — `dq.sh`: a Data-Quality Toolkit

> Module 08 · Unit 2 · **Graded deliverable** · Est. 2 h (+ polishing)
> Prerequisites: all three labs
> Maps to the course roadmap's M08 mini-project and to mini-project A's
> spirit ([projects/mini-projects](../../../../projects/mini-projects/README.md)).

**Brief.** Every lab in this module produced *one-off* pipelines. Real
teams re-run them daily — on new files, in cron, before loading into
pandas. Build `dq.sh`: a small CLI that runs the module's data-quality
checks against any text dataset and prints a report.

## Requirements

```console
$ ./dq.sh FILE [--delimiter CHAR] [--fields N] [--top N]
```

Behavior:

1. **Profile** (always): file type (`file`), size, line count, header
   detection (does line 1 differ in shape from the rest?), delimiter
   echo.
2. **Shape check:** with `--fields N`, count rows whose field count ≠ N
   (awk), report worst offenders with line numbers (first 5).
3. **Duplicate check:** exact-duplicate rows (excluding header): count +
   up to 3 examples via `sort | uniq -d | head`.
4. **Category census:** with `--top N`, show the N most common values of
   each categorical-looking column *if* the file is small (≤ 5000
   lines); skip with a note otherwise (scale awareness!).
5. **Numeric sanity:** columns that look numeric — report min/max via
   awk; flag any negative in a column whose header suggests a quantity
   (`amount`, `count`, `temp`) — heuristic, documented.
6. **Exit codes:** 0 = clean-ish (no hard failures), 1 = duplicates or
   shape violations found, 2 = usage error. (Scripts that cron runs need
   exit codes — M19 depends on this habit.)

## Constraints (the pedagogical point)

- **POSIX-ish bash**, `set -euo pipefail` at top (M10 previews this).
- Every check = **one pipeline**, commented with the question it answers.
- Graceful on empty/missing files (friendly error, exit 2, no stacktrace).
- Works on ALL six module datasets *and* on a fresh mystery file your
  instructor will supply (test command: run it on `students.csv`,
  `sensor-telemetry.tsv`, and any CSV you can invent).
- README.md section (in your submission doc): usage, sample output on
  two datasets, and **known limits** — the Lesson 6 boundary: where does
  this tool *stop* being enough and pandas *start*? (Minimum two
  concrete examples.)

## Sample interaction (target)

```console
$ ./dq.sh students.csv --delimiter , --fields 7 --top 3
== dq report: students.csv ==
file:    CSV ASCII text, 11 lines, 628 bytes
header:  yes (7 fields; body rows: 10/10 match)
dupes:   0 exact duplicate rows
cats:    program: DS=4 CS=2 MATH=1 PHYS=1 STAT=1
numeric: gpa min=2.48 max=3.74 (9 values, 1 non-numeric: line 10)
flag:    line 10 'gpa' = '"3,77"' — non-dot decimal (quoted)
exit:    1 (issues found)
```

## Rubric (20 points)

| Criterion | Pts |
|---|---|
| Correctness: checks work on all six datasets + mystery file | 6 |
| Pipeline quality: each check is one clean, commented pipeline | 4 |
| Safety/robustness: no in-place edits, graceful errors, exit codes | 3 |
| Scale awareness: refuses the expensive census on big files, says why | 3 |
| Report: usage + sample outputs + honest limits section | 4 |

## Hand-in

`dq.sh` + `dq-report.md` (usage, outputs on ≥2 datasets, limits) in
`~/lab08/`, with `lab-log.md` narrating your build decisions. The best
submissions read like tools, not homework: `--help` text, consistent
flags, an opinionated default.

**Stretch (ungraded):** a `--json` flag emitting machine-readable
output (awk printf, or hand off to `python3 -c "import json,sys; ..."`
— Lesson 6's Pattern 3, in the wild).
