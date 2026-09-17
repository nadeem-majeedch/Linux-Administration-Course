# Level 3 — Advanced: The Automation Bench

> Assumes M16–M19 · ~3 h · your own VM · `script level-3.log` first.
> You've scripted before; today you *operate* scripts. Build a small
> unattended system, break it in three scheduled ways, and leave
> behind something that survives your absence.

## Setup (5 min)

```console
$ curl -O https://course-portal.uni.edu/labs/level3-data.tar.gz
$ tar xzf level3-data.tar.gz -C ~ && cd ~/level3
```

Contents: `incoming/` (hourly data drops, 48 files, three poisoned
in three different ways), `expected-schema.txt` (the column
contract), and a `notes/` directory for your build.

## Build 1 — The pipeline with standards (50 min)

`process-drop.sh <file>` — per file: validate against the schema
(header exact, field count per row, non-empty), then append a
one-line verdict to `notes/processed.log`:
`<file> OK|BAD(<reason>) rows=<n>`.

Non-negotiable standards (each is a rubric line):

- `set -euo pipefail`; explicit usage/exit-2 path; every variable
  quoted; **no** `cd` without subshell-or-restore; log lines go
  through a `log()` function so format changes are one-line edits.
- Poisoned files are moved to `quarantine/` with their reason —
  deletion anywhere is an instant fail.
- **Re-run safety:** processing the same file twice must not
  duplicate verdicts (state your mechanism: marker dir, log grep,
  anything defensible).

Test the three poison classes + one good file + a non-existent
file. Five runs, five correct outcomes, all in the transcript.

## Build 2 — The unattended loop (40 min)

1. Schedule `process-drop.sh` over `incoming/` via a **for-loop
   driver script** (`run-all.sh`) — one cron entry or systemd timer
   runs the driver, not the single-file script.
2. Prove firing with a compressed schedule (`*/2 * * * *`), capture
   one real unattended run's log line, restore the real schedule.
   The *unattended* log line must differ visibly from your manual
   runs (timestamp proves it).
3. **Environment trap:** deliberately remove your venv
   initialization from the driver and observe the cron-run failure
   in the log; restore and re-prove. This is the "works in my shell,
   fails in cron" lesson inflicted on purpose, with the wound
   documented in `notes/incident-cron.md`.

## Build 3 — The backup that can prove itself (50 min)

1. `backup.sh`: tar+gzip `notes/` + `processed.log` to
   `backups/level3-YYYYMMDD-HHMM.tar.gz`; keep exactly 5, prune
   older; write a per-archive sha256 into `backups/MANIFEST.sha256`.
2. Schedule it nightly. Then **restore drill**: move the live
   directory aside, restore the newest archive *by the book* (the
   README you write in Build 4 is the book), verify checksums, move
   live data back. Untested backup = no backup; the drill is the
   deliverable.
3. **Restore from partial loss:** delete (move aside) *one file*
   from the live tree, restore just that file from the archive
   (`tar --extract --wildcards` or equivalent), verify. Two
   restore modes, both drilled.

## Build 4 — Leave it operable (30 min)

`README.md` in `notes/` — the operator's page for a stranger:

- What runs when (table: script, schedule, log path, failure mode).
- The restore procedure (both drills), numbered, copy-pasteable.
- The "add a new drop directory" change in ≤ 3 steps.
- One paragraph: *what this system cannot survive* (honest limits —
  full disk, corrupted archive, silent schema change) and the
  detection you'd add next.

## Rubric (10 pts)

| Pts | Requirement |
|---|---|
| 2 | Build 1: five-run matrix correct; quarantine-not-delete |
| 1 | Build 1: re-run safety mechanism stated and shown |
| 2 | Build 2: unattended run proven with timestamped log |
| 1 | Build 2: cron-environment incident documented |
| 1 | Build 3: rotation keeps exactly 5 + MANIFEST present |
| 2 | Build 3: both restore drills with checksum verification |
| 1 | Build 4: stranger-followable README with honest limits |

## Watch-for

- The driver loop that swallows per-file failures (`for f in …;
  process || true`) — one poisoned file then hides every other
  failure. If you wrote `|| true`, say *why* in the README or take
  the point off.
- Backups scheduled but never fired by marking time: the compressed-
  schedule proof from Build 2 is the accepted substitute — claims
  aren't.
