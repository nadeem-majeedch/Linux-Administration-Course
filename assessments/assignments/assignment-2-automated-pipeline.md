# Assignment 2 — The Automated Pipeline

> Covers M09–M10, M16–M19 (text processing, scripting, systemd,
> cron/backup) · 5% of course grade · due end of week 11 ·
> individual work. Environment: your own Ubuntu VM.

## The story

A fictional sensor array drops CSV readings into a spool directory
every hour. Build the small, boring, *reliable* system around it:
validate, summarize, archive — automatically, with evidence.

## Setup

```console
$ curl -O https://course-portal.uni.edu/a2/setup.sh   # (course-local URL)
$ bash setup.sh    # creates ~/a2/spool with 72 sample hourly files
```

Sample file: `readings-20260303T14.csv` — header
`timestamp,sensor_id,temp_c,humidity` plus rows; some files are
**poisoned** (missing columns, empty file, duplicated timestamp
block).

## Deliverables

### 1. `pipeline.sh` — the validator/summarizer (35%)

Invocation: `./pipeline.sh <spool-dir> <out-dir>`. Per input file:

- **Validate**: correct header, non-empty, row field-count matches
  header. Poisoned files are *moved* to `<out-dir>/quarantine/`
  (never deleted), with the reason appended to
  `<out-dir>/quarantine.log`.
- **Summarize** valid files: append one line per file to
  `<out-dir>/summary.csv` —
  `filename, rows, min_temp, max_temp, mean_humidity`
  (awk does this in one pass; anything correct allowed).
- **Idempotent**: running twice must not duplicate summary lines.
  The transcript must show the double-run proof.

Scripting standards enforced (from M16–M17): `set -euo pipefail`,
usage/exit-2 on missing args, quoting discipline, no `cd` without
restoration, comments explaining *why* at each stage.

### 2. `hourly.timer` or cron entry — the scheduler (20%)

- Schedule `pipeline.sh` hourly. cron **or** systemd timer (bonus
  reasoning if you explain which you chose and why).
- Prove it fires: shorten the interval, capture one real run in the
  log, then restore the schedule. Log must capture stdout+stderr
  and the exit status line.
- The unit/crontab is submitted as a file in the repo.

### 3. `archive.sh` + restore drill (25%)

- Nightly: tar+gzip the spool into
  `~/a2/archive/readings-YYYYMMDD.tar.gz`, keep the last 7, delete
  older **from the archive only** (the spool is never touched).
- **Restore drill**: in the transcript, delete (move aside) two
  spool files, restore them from the newest archive, verify
  checksums match the originals (`sha256sum` before/after). An
  untested restore claim scores zero — the drill is the proof.

### 4. `README.md` — the operator's page (20%)

One page: what runs when (diagram or table), the failure modes you
designed against (poison files, double-run, full disk), how to add
a sensor field without breaking the summary, and the restore
procedure in six numbered steps a stranger could follow.

## Submission

Repo with: `pipeline.sh`, `archive.sh`, `hourly.timer`/crontab
file, `README.md`, `evidence/` (transcript `a2.log`, one real
scheduler log, restore-drill section), plus the generated
`summary.csv` and `quarantine.log` from your proof runs.

## Grading (100 pts → 5%)

| Area | Pts | Hard rules |
|---|---|---|
| Validation logic | 15 | all three poison classes caught; quarantined, not deleted |
| Summarizer | 10 | numbers match instructor's reference within rounding |
| Idempotency | 10 | double-run proof in transcript |
| Script standards | 10 | `set -euo pipefail`, exit codes, quoting (shellcheck-clean = +2) |
| Scheduling | 10 | fires for real during the marking window |
| Archive rotation | 10 | keeps exactly 7; spool untouched |
| Restore drill | 15 | checksum-verified restore visible — claim without drill = 0 |
| README | 15 | stranger-followable restore steps |
| Transcript | 5 | complete, ordered |

**Penalties:** deleting poisoned files −30; archive job touching the
spool −30; cron line without output redirection −10.
