# Module 11 — Advanced Shell & Automation · Content Index

> **Status:** Content complete — 3 lessons, 2 labs (incl. the final
> scripting challenge), quiz + key, 8 challenges, troubleshooting
> guide, plus Mini-Project A hardening.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate.

> 🟡 **Module safety contract:** the module's scripts are the first
> allowed to *modify* files (rename, move) — so every modifying
> script carries a `--dry-run`, refuses to overwrite, and cleans its
> temp files via `trap`. All practice stays under `~/lab11/`.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-lines-streams.md](lessons/01-lines-streams.md) | while-read mastery, IFS, field splitting, process substitution, comparing streams |
| 2 | [02-signals-temp-cleanup.md](lessons/02-signals-temp-cleanup.md) | trap (EXIT/INT/TERM), mktemp, safe temp files, atomic-ish writes, interruptible scripts |
| 3 | [03-dry-run-idempotency-options.md](lessons/03-dry-run-idempotency-options.md) | the dry-run pattern, idempotency, getopts, config parsing, the reusable-tool checklist |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-harden-dq-toolkit.md](labs/lab-01-harden-dq-toolkit.md) | Harden M10's `dq.sh`: `--dry-run`, `--out`, `-h`, trap cleanup, timestamped logs, Ctrl+C mid-run test |
| 2 | [lab-02-final-scripting-challenge.md](labs/lab-02-final-scripting-challenge.md) | **Final scripting challenge**: build `organize.sh`, a guarded dataset organizer with dry-run, idempotency, and self-test |

## Mini-Project

- [Mini-Project A hardening](mini-project-a-hardening.md) — the M10
  toolkit upgraded with everything this module taught; graded as a
  re-submission.

## Practice & Support

- [Quiz](practice/quiz.md) (20 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptoms → causes → fixes

## Cross-references

- [M10 scripting](../../M10-bash-scripting/content/README.md) —
  the foundation this module hardens.
- [M18 signals](../../M18-processes-jobs-signals/content/README.md) —
  trap's full grammar (process groups, kill ladder) arrives there.
- [M19 cron/timers](../../M19-scheduling-cron-timers/README.md) —
  idempotent scripts are what makes scheduling safe.
- [M24 logging](../../M24-logs-journald-monitoring/content/README.md) —
  the logging contract these scripts follow.
- [M17 storage](../../M17-storage-and-filesystems/content/README.md) —
  atomic writes rely on rename semantics on one filesystem.
