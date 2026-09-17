# Module 10 — Bash Scripting · Content Index

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 3 · Shell Scripting & Automation](../../../COURSE-ROADMAP.md#unit-3--shell-scripting--automation-m10m11).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-3--shell-scripting--automation-m10m11) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> **Status:** Content complete — 5 lessons, 2 labs (incl. 8 fix-the-bug
> scripts), quiz + key, 8 challenges, troubleshooting guide, Mini-Project A.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate.

> 🟡 **Module safety contract:** every script in this module operates
> only on files under the student's `~/lab10/` (or the course's
> `datasets/` copies). No script deletes outside its own scratch
> directory; `rm` appears only with a guard pattern explained at
> first use; `shellcheck` must pass before any script is called done.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-first-scripts.md](lessons/01-first-scripts.md) | shebang, running scripts, variables, quoting rules, echo vs printf, command substitution |
| 2 | [02-control-flow.md](lessons/02-control-flow.md) | exit status, `if/elif`, test/`[[ ]]`, file & string tests, `case`, `for`/`while`/`until`, `read` |
| 3 | [03-arguments-exit-codes.md](lessons/03-arguments-exit-codes.md) | positional parameters, `$@`/`$#`, usage checks, strict mode (`set -euo pipefail`), fail-loudly logging |
| 4 | [04-functions-arrays-tests.md](lessons/04-functions-arrays-tests.md) | functions & `local`, arrays, arithmetic, structuring a real script |
| 5 | [05-debugging-quality.md](lessons/05-debugging-quality.md) | `bash -n`, `bash -x`, the shellcheck workflow, script style, reusable-script habits |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-fix-the-bugs.md](labs/lab-01-fix-the-bugs.md) | Eight broken scripts — classic quoting, exit-code, and word-splitting bugs to diagnose and fix |
| 2 | [lab-02-build-dq-toolkit.md](labs/lab-02-build-dq-toolkit.md) | Build `dq.sh` step by step: a data-quality wrapper over the M09 pipeline, with usage help, strict mode, logging |

## Mini-Project

- [Mini-Project A — Dataset QC toolkit](mini-project-a-dataset-qc-toolkit.md):
  `dq.sh` + `summary.sh` (+ optional `clean.sh`) over the course
  datasets, documented, shellcheck-clean.

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 script symptoms → causes → fixes

## Cross-references

- [M09 pipes](../../M09-pipes-and-redirection/README.md) —
  every pipeline from that module becomes a script line here.
- [M08 text processing](../../M08-text-processing/content/README.md) —
  the data files dq.sh works on come from there.
- [M07 files](../../M07-files-and-directories/README.md) — globs and
  file ops get batched.
- [M11 automation](../../M11-advanced-shell-automation/content/README.md) —
  the next step: traps, dry-runs, idempotency.
- [M19 cron](../../M19-scheduling-cron-timers/README.md) — where
  working scripts get scheduled.
