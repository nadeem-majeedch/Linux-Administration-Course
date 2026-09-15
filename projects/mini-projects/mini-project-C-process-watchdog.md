# Mini-Project C — Process Watchdog (M18)

> Module: M18 — Processes, Jobs and Signals · Unit 5 · Difficulty: Intermediate
> Prerequisites: M10, M11, M18 in progress

## Brief

Long-running jobs (training scripts, exporters, small daemons you write) need
*evidence*: what did the process consume, when did it spike, did it die quietly?
Build a watchdog that observes a target process and records its behavior over time.

## Deliverables

1. **`watchdog.sh`** — usage: `watchdog.sh [-i INTERVAL] [-d DURATION] PID`
   - samples the target every INTERVAL seconds (default 5): CPU %, RSS memory,
     state, and timestamp, appending CSV rows to `watchdog-<pid>.csv`
   - writes a parallel human-readable log line per sample to `watchdog.log`
   - on overrun: if CPU % exceeds a threshold (`-c`, default 90) for N consecutive
     samples, writes an alert line to the log and stdout — and keeps collecting
   - exits cleanly if the process disappears (reports its lifetime in the log)
   - `trap`-based cleanup of temp files; `--dry-run` prints one sample to stdout
     and exits
2. **`README.md`** — usage, output formats (CSV header documented), an example
   session against a deliberately CPU-hungry test script (provided in class), and
   how you would read the CSV later (pointer to M27 plotting).

## Constraints

- Only your own processes (no elevated signal sending, no other users' PIDs).
- `set -euo pipefail`, argument validation, `-h` help, `shellcheck` clean.
- The CSV must be append-safe: stopping with Ctrl+C must not truncate or lose
  already-written rows (test this and document the behavior).
- Interval < 1s not required; keep sampling cheap (no forking a dozen processes
  per sample — prefer reading `/proc/<pid>/stat` or one `ps` call).

## Rubric

| Criterion | Weight |
|---|---|
| Correct sampling and CSV format | 35% |
| Robust process-disappearance handling + trap cleanup | 20% |
| Alert logic correct (threshold + consecutive samples) | 15% |
| Style, strict mode, shellcheck | 15% |
| README and example session | 15% |

## Stretch goals

- Detect process *death by signal* (report which signal from exit status).
- Add a `-o` option to write CSV elsewhere, enabling capstone reuse.
- Plot one watchdog CSV with matplotlib in a follow-up notebook (M27 preview).
