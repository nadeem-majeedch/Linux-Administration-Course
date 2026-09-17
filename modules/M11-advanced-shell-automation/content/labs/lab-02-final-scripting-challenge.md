# Lab 2 — The Final Scripting Challenge: `organize.sh`

> Module 11 · Unit 3 · Difficulty: Advanced (Unit 3's capstone lab)
> Time: ~60 min · Environment: your own VM, `~/lab11/`
> Prerequisites: all M10 + M11 lessons and labs
> ⚠️ Moves files — the module's first bulk-modifying lab. That's why
> the dry-run, the overwrite guard, and the self-test are *graded
> deliverables*, not extras.

One tool, all the properties. Build **`organize.sh`** — a dataset
organizer that sorts files from a messy directory into type-based
subdirectories, safe enough to run on a colleague's data without
supervision.

## The contract

**Usage:** `organize.sh [-n] [--dry-run] [-t TARGET] [--ext csv,tsv] [-h] DIR`

Behavior:

1. Reads every `*.csv`/`*.tsv` (per `--ext`) in DIR.
2. Classifies each by *content sniff* of the header line: comma
   header → `csv/`, tab header → `tsv/`, mismatched-extension files
   → `mislabeled/` (never guessed at — moved and named).
3. Non-matching extensions are left strictly alone and *counted*.
4. Moves into TARGET (default: DIR itself), never overwriting
   (`mv -n` + pre-check), logging every action.
5. Finishes with a summary to stdout: moved / skipped-existing /
   mislabeled / ignored counts.

Contract exits: 0 all processed · 64 usage · 66 DIR missing/not a
directory · 67 any move failed.

## Required properties (the rubric)

| Property | Requirement | Proof |
|---|---|---|
| **Dry-run** | `-n`/`--dry-run`: full plan on stderr, zero changes, "N actions planned" summary | dry-run then `find DIR -name 'csv'` shows no dirs |
| **Idempotency** | second real run: everything `skipped (exists)`, exit 0 | two run logs |
| **Graceful death** | `mktemp` journal file + `trap cleanup EXIT`; interrupt mid-run (add a debug sleep) leaves no debris, rc=130 | interrupt trace |
| **No clobber** | a same-named file in the destination is *skipped and counted*, never overwritten | collision test |
| **Options** | getopts short forms + `--dry-run` long alias + `--ext` list parsing | all error paths (64) |
| **Config** | `ORGANIZE_TARGET` env override for TARGET | two runs, two targets |
| **Quality** | `bash -n`, `shellcheck` silent; `main "$@"` structure | last clean outputs |
| **Self-test** | `--selftest` (see below) | PASS lines |

## The self-test (what separates tools from scripts)

`organize.sh --selftest` builds its own sandpit — temp dir (mktemp!),
a handful of known files (good csv, mislabeled csv, tsv, collision
pair) — then asserts, via the tool's *own* exit codes and the
filesystem:

1. dry-run changed nothing (`diff -r` before/after — [Lesson 1 §5's](../lessons/01-lines-streams.md)
   process-substitution pattern)
2. real run moves exactly the right files (names + counts)
3. second run is a no-op (idempotency, asserted)
4. collision file survives untouched at both ends
5. exit codes are 0/0/0/0 across the four phases

Print `PASS`/`FAIL` per assertion, exit non-zero on any FAIL, clean
the sandpit via the trap. You've now written the tests *and* the
tool — and the next refactor is fearless.

## Suggested build order

1. Argument parsing + guards (64/66) — 10 min
2. Classification pass (read-only; print the plan) — 15 min
3. `run()` doorway + real moves + counters — 10 min
4. Idempotency + no-clobber — 5 min
5. mktemp/trap + interrupt drill — 10 min
6. Self-test — 10 min (hardest; leave time)

## Done when

- [ ] Rubric table filled with proof pointers (transcript line
      references)
- [ ] All four contract exits demonstrated
- [ ] Self-test passes end-to-end (paste output)
- [ ] `shellcheck` zero findings
- [ ] 150-word README section: what the tool does NOT handle (nested
      dirs, quoted-CSV commas, same-file-both-types) — limitations
      are part of the contract
