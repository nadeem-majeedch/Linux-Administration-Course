# Mini-Project E — Server Health and Backup Kit (M24)

> Module: M24 — Logs, journald and Monitoring · Unit 6 · Difficulty: Advanced
> Prerequisites: M20, M18, M17, M24 in progress

## Brief

You operate a small Ubuntu server (your VM) that runs a scheduled data job (from M19)
and a service (from M20). Two things are missing: a fast *health report* you can run
any time, and a *backup* you can actually restore. Build both.

## Deliverables

1. **`health.sh`** — one-page system report to stdout:
   - host, kernel, uptime, load average
   - memory and swap usage (`free -h`)
   - disk usage for `/` and any mounted data volumes (`df -h`), flagging > 80%
   - top 5 processes by CPU and by memory (one `ps` invocation each)
   - failed systemd units (`systemctl --failed`)
   - errors from the current boot's journal for your units (`journalctl -p err -b`)
   - status of your scheduled job's last run (from its log)
   - `--json` flag emitting the same report as JSON (for later automation)
2. **`backup.sh`** — data backup with restore mode:
   - default mode: `tar -czf` snapshot of `~/projects` and `~/data` into
     `backups/YYYY-MM-DD/`, then `rsync` the newest snapshot to a second location
     (second virtual disk from M17) — the 3-2-1 rule, student-scale
   - retention: keep the last N=7 snapshots, delete older *only after* the new
     snapshot verified (checksum check)
   - `--restore DIR TARGET` mode: restores a chosen snapshot to a target directory
     (never over the original), verifies checksums, prints what it restored
   - every action logged with timestamps; `set -euo pipefail`; `shellcheck` clean
3. **`restore-test.md`** — evidence that the backup works: you must delete a test
   directory's contents, restore from the snapshot, and show byte-for-byte recovery
   (`diff -r` output). **A backup that has never been restored is a hope, not a backup.**
4. **`incident-report.md`** — pick one of the module's broken-service scenarios and
   write it up: symptom, evidence you collected (commands + key log lines), root
   cause, fix, and what would have caught it earlier.

## Constraints

- Backups target only your own data; no system files, no other users' data.
- Restore mode refuses to write over a non-empty target unless `--force` is given.
- The 80% disk flag threshold is configurable via environment variable (M15 practice).

## Rubric

| Criterion | Weight |
|---|---|
| health.sh correctness and readability of its report | 25% |
| backup.sh: snapshot + rsync + retention + verification | 25% |
| Restore *test* performed and evidenced | 20% |
| Incident report quality (evidence-driven diagnosis) | 20% |
| Style: strict mode, logging, shellcheck | 10% |

## Stretch goals

- Schedule both scripts (cron or timer) — health every 15 min, backup nightly —
  and prove they ran via their logs (M19 recap).
- Add a `--mail`-style alert: append a WARNING line to a watched log that a
  classmate's health script could pick up (cross-student drill, instructor-arranged).
