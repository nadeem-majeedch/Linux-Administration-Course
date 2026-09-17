# Assignment 4 — The Survivor Script

> Covers M10–M11 + M19 (scripting, idempotency, scheduling) ·
> optional replacement for A2 (same 5% weight) · individual work ·
> evidence transcripts required.
>
> **The premise:** your script will run unattended. Nobody will watch
> it. The grade is not "did it work once" — it is "what happens when
> conditions are hostile."

## Learning objectives assessed

- Guarded-script design (argument checks, `set -euo pipefail`, exit codes)
- Idempotency and state hygiene across repeated runs
- File-verification discipline (checksums, not assumptions)
- Scheduling with correct environment handling and *auditable logging*

## The task

Write `dataset-custodian.sh` — a script that maintains a dataset
directory in four phases. You will be given a scratch directory with
deliberately hostile content.

**Phase 1 — intake.** Files arrive in `incoming/` with unpredictable
names (spaces, uppercase, duplicates). Move each `.csv` into
`data/` renamed to a safe, lowercase, date-prefixed form
(`2026-09-17-originalstem.csv`). Non-CSV files stay in `incoming/` but
are *listed* in the log.

**Phase 2 — verification.** For every file in `data/`, record
`sha256sum` into `manifest.sha256`. A file whose hash changed since the
last manifest (you keep the old manifest) is *quarantined*: moved to
`quarantine/` with a note in the log — never deleted.

**Phase 3 — hygiene.** Remove zero-byte files *only from* `incoming/`.
Cap `data/` at 50 files: the oldest (by mtime) move to `archive/`. Never
delete.

**Phase 4 — report.** Append one human-readable summary line per run to
`custodian.log`: timestamp, counts (moved/quarantined/archived), and
exit status.

## Hostile conditions you must survive

Run the script **three times back-to-back** — it must be idempotent
(run 3 ≡ run 1: no duplicates, no drift). Then it must survive: an empty
`incoming/`; a missing `archive/` (create it); a *filename with spaces*;
being run from a different working directory (absolute paths or
cd-to-script-root discipline — your choice, but it must *work*).

## Deliverables

1. `dataset-custodian.sh` (the course skeleton: guards, functions,
   `set -euo pipefail`)
2. `custodian.log` from at least three runs + one hostile run
3. The **transcript** (`script a4.log`) including: first run, second
   run (proving idempotency), one hostile run, the `shellcheck` pass
   (zero warnings)
4. A half-page `NOTES.md`: your design decisions — what the guards
   prevent, why quarantine instead of delete, where this script would
   break anyway

## Constraints & hard rules

- No deletions except zero-byte files in `incoming/` (and *that* must
  be ls-verified first in the transcript)
- No interactive prompts (it will run under cron — BatchMode thinking)
- Every mutation is logged; the log is append-only
- Scheduled-run bonus (up to +1 pt, capped at assignment max): the
  crontab line *and* the logging line that make it auditable under
  cron's environment — with the two cron traps named and handled
  (path, environment)

## Rubric (20 pts)

| Area | Pts | Full credit |
|---|---|---|
| Guards & skeleton | 4 | argument checks, `set -euo pipefail`, functions, exit statuses |
| Intake correctness | 4 | renaming rules applied incl. spaces; non-CSVs logged, not moved |
| Verification & quarantine | 4 | manifest diffing; quarantine path; no deletion drift |
| Idempotency proof | 3 | three-run transcript shows zero drift |
| Hostile-condition survival | 3 | empty dir, missing archive, cwd change — all evidenced |
| Notes & logging quality | 2 | design decisions articulate the *why* |

## Academic integrity

Your transcript is personal evidence — identical command histories
across submissions are examined at the decision level (see the
[framework](../README.md#academic-integrity-guidance)). Cite any
snippet source in NOTES.md; the *guards and structure* must be yours.
