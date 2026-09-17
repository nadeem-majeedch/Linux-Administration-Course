# Module 11 Challenges — Advanced Automation

> Eight challenges under `~/lab11/`. Every modifying script carries
> the full property set (dry-run, idempotency, trap, shellcheck).
> Several build directly on M10's challenges — upgrade them, don't
> rewrite them.

## C1 — The honest deduper

Upgrade M10's `dupes.sh` to `dedup.sh`: same reporting, plus
`--write` producing `FILE.dedup` (first occurrence kept) via
temp+atomic-mv. Without `--write`: report only. Prove: dry-run on a
file with duplicates, real run, *second real run is a no-op*
(deduped input has no duplicates — say so in the log).

## C2 — The parallel reconciler

Extend M11 Lesson 1's `reconcile.sh` with `-v` (print the differing
IDs, not just counts), `--output FILE` (atomic write of the diff
lists), and a `--swap` flag reversing the comparison direction. All
new outputs via temp+mv; all narration via the log contract.

## C3 — The subshell detective

Write `varproof.sh` containing three loops that count lines of a
file: (a) `cat | while` pipe form, (b) `done < file` form, (c)
process-substitution form. Print the three counts — they will
differ. Then a 5-line explanation section in the header comment
teaching the reader *why*. (This is a teaching tool; its users are
future-you's teammates.)

## C4 — The config-driven scheduler-friendly batch job

`batch.sh -c batch.conf`: reads a config file of `key=value` lines
(you write both), performing per-dataset: validate (M10's dq logic),
summarize, archive to `archive/` (mv -n). Config vars: `SRC_DIR`,
`ARCHIVE_DIR`, `MIN_ROWS`, `DRY_RUN`. Requirements: refuse configs
that don't exist (66); never source blindly — parse with a while
read of `key=value` pairs, validating each key against a known-keys
list (why? — answer in the header). Idempotency: archiving moves;
re-running must skip already-archived files cleanly.

## C5 — The interruptibility auditor

`audit.sh SCRIPT`: static-checks a *given* script for the module's
property set using only grep/read-only commands: has shebang, has
`set -euo pipefail`, every `rm`/`mv`/`cp` line is inside a `run()`
call or followed by a guard (`||`/`if`), references `mktemp`,
contains `trap`, mentions `--dry-run`/`-n`. Output a checklist table
with PASS/FAIL per property and a final verdict. (It audited its own
author's workflow — run it on itself as the last test. Make it pass
its own audit.)

## C6 — The atomic log rotator

Mini-rotation for a growing `app.log` (M24 preview, user-scale):
`rotatelog.sh LOG [KEEP]` — if LOG exceeds 1 MB (configurable),
rename to `LOG.$(date +%F-%H%M%S)` (never overwriting an existing
rotation — exists-guard), then signal the *writer pattern* to start
fresh (in-lab: touch a new file; in production: logrotate/reopen —
say so in the header). Keep-count enforced by deleting **only files
matching the exact rotation pattern** (`LOG.20*`), oldest first,
count > KEEP — with the deletions dry-run-narrated by default.

## C7 — The environment bootstrapper, hardened

Upgrade M10's C5 `newproj.sh`: `-n` dry-run, idempotent (re-running
on an existing project *fills gaps only* — missing subdirs created,
existing files untouched, reported as `skip`), a `PROJ_ROOT` env
override, mktemp+trap for its report generation, and an `--selftest`
that builds a scratch project, asserts the tree, re-runs, asserts
no-op, cleans up.

## C8 — The two-tool handshake

Take C1's `dedup.sh` and M10's C2 `dupes.sh` (or your equivalents)
and write `pipeline.sh`: validates with one, writes with the other,
*only if* validation passes — with per-stage logging, distinct exit
codes per stage (66 validate / 67 write / 0 ok), a `--keep-going`
flag that runs all stages despite a failure (collecting all codes),
and a summary line naming the first failing stage. The design
question to answer in the header: when is `--keep-going` the *wrong*
default? (Hint: stages whose outputs are the next stage's inputs.)

## Stretch — C9, the property test

Write `props.sh` that runs [Lab 2's](../labs/lab-02-final-scripting-challenge.md)
`organize.sh --selftest` **five times** with five different sandpit
seeds (add a `--seed N` to the selftest, or vary file counts) and
asserts identical exit codes and summary *shapes* each time. You've
built a poor-man's property test — one sentence on what class of bug
this catches that a single run cannot (nondeterminism).
