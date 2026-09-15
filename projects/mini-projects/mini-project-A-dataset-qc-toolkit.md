# Mini-Project A — Dataset QC Toolkit (M10)

> Module: M10 — Bash Scripting · Unit 3 · Difficulty: Intermediate
> Prerequisites: M08, M09, M10 in progress

## Brief

You have been given a folder of retail sales exports (see `datasets/sales-2019-q1.csv`)
and asked to produce a *repeatable* data-quality check. Doing it by hand every week is
wasteful and error-prone — so you will build a small toolkit of Bash scripts that any
team member can run with one command.

## Deliverables

1. `dq.sh FILE` — runs a data-quality pass over a CSV and prints a report:
   - total rows and columns (header-aware)
   - duplicate row count (with the 5 first duplicates shown)
   - rows whose email column fails a basic pattern
   - rows with empty required fields
   - exit code `0` when clean, `1` when issues found (so it can drive automation later)
2. `summary.sh FILE` — one-screen summary: row count, distinct values of two chosen
   columns, min/max/mean of the amount column (awk is allowed and encouraged).
3. `README.md` — what the toolkit does, usage examples, what its exit codes mean.

## Constraints

- Strict mode in every script: `set -euo pipefail`.
- Both scripts validate arguments and print usage on error (`-h` shows help).
- Every action logs a timestamped line to a log file (your choice of location).
- Passes `shellcheck` with zero warnings.
- No hardcoded absolute paths; the script must work relative to its own location.

## Safeguards

The toolkit must be **read-only** toward the input data in this version — it reports,
it never modifies. (A cleaning mode arrives in M11 as an extension.)

## Rubric

| Criterion | Weight |
|---|---|
| Correctness on `sales-2019-q1.csv` (numbers match `expected/` outputs) | 40% |
| Robustness: bad args, missing file, empty file handled gracefully | 20% |
| Style: strict mode, quoting, comments, readable structure | 15% |
| shellcheck clean | 10% |
| Documentation quality (README, usage, exit codes) | 15% |

## Stretch goals

- `--csv` flag emitting the report as CSV (for later plotting in M27).
- Wire `dq.sh` into a `while read` loop over a directory of exports (M11 preview).
