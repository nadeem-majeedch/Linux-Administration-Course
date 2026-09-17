# Level 5 — Data Science Server: The Full Circle

> Assumes M26–M31 · full day (build 4–5 h + operate overnight) ·
> your own VM · `script level-5.log` first. This is the ladder's
> summit and the capstone's proving ground: one machine, the whole
> course, and an *overnight* requirement — because the difference
> between a demo and a system is what happens while you sleep.

## The mission

Stand up a single-node DS platform: dataset landing, nightly
processing, a Jupyter server for analysis, a containerized API for
results — then prove the platform survives a night unattended and a
crash without you.

## Phase 1 — Build the platform (2 h)

1. **Structure:** `/srv/ds/{inbox,datasets,runs,archive}` with the
   permissioned-commons pattern: group `dsteam`, SGID
   directories, service account `dsrobot` that owns nothing but
   writes where allowed.
2. **Ingest:** `ingest.sh` — moves any file landing in `inbox/` to
   `datasets/`, validating the CSV schema (M16/M17 standards:
   `set -euo pipefail`, quarantine-not-delete, re-run safe).
3. **Jupyter:** user-level systemd unit (or login-managed
   tmux + documented start) bound to **localhost only**, password
   or token set, lab extension reachable only through an SSH
   tunnel. Prove the local-only binding (`ss -tlnp`) and the
   tunnel reach (curl through `-L`).
4. **API:** the course's tiny results API containerized: read-only
   bind mount of `runs/`, non-root container user, published port
   ≥ 10000, `--restart unless-stopped`, memory limit set.

## Phase 2 — Automate the day (1.5 h)

1. **Pipeline:** nightly systemd timer (03:00): `ingest.sh` →
   summary statistics per dataset (awk or pandas — your choice,
   justify in one line) → append to `runs/summary.csv` → archive
   the day's inbox into `archive/` (tar+zstd/gzip) → prune archive
   to 7 days.
2. **Backups:** separate timer backs up `datasets/` +
   `runs/summary.csv` to a second disk image or directory with a
   sha256 manifest. **Restore drill before you sleep:** delete a
   test dataset, restore from backup, checksum-verify. No drill,
   no overnight phase.
3. **Health:** `healthcheck.sh` (Level-4 style: disk, memory,
   units, Jupyter HTTP probe, API probe) on a 15-minute timer,
   failures logged to journal under a dedicated unit name.

## Phase 3 — Overnight (hands-off)

Before disconnecting: full baseline evidence file
(`systemctl --user list-units`, timers list, `df -h`, `ss -tlnp`,
ufw status). Then log out completely. Overnight the system must:

- process any files a cron-scripted "feeder" drops into `inbox/`
  (the lab provides a 6-line feeder script for your own VM),
- archive and prune,
- run healthchecks,
- **survive one deliberate service kill** — the feeder's sibling
  script kills the API container once, at a random minute; your
  restart policy is the only thing standing.

## Phase 4 — The morning after (1 h)

1. Compare morning evidence to baseline: every unit's state, timer
   last-trigger times (`systemctl list-timers`), archive contents,
   healthcheck log — *gaps* are findings, not embarrassments.
2. The kill report: from container logs and journal, reconstruct
   the kill minute, downtime, recovery — to the minute, with
   evidence lines.
3. Reproducibility statement: someone else rebuilds your pipeline
   environment from your committed `requirements.txt`/Dockerfile on
   a fresh venv and runs one day's data through. Their success
   *is* your reproducibility grade.

## Rubric (10 pts)

| Pts | Requirement |
|---|---|
| 2 | Phase 1: structure + permissions proven; Jupyter local-only + tunnel |
| 1 | Phase 1: API container — non-root user, limits, restart policy all visible in inspect |
| 2 | Phase 2: pipeline + backup timers with real firing evidence |
| 1 | Phase 2: restore drill completed pre-overnight |
| 2 | Phase 4: overnight delta report with gaps explained |
| 1 | Phase 4: kill report reconstructed from logs |
| 1 | Phase 4: independent rebuild of the environment succeeds |

## Watch-for

- The Jupyter unit that "works" because you tested it in your
  session — user units die at logout without `loginctl
  enable-linger`. The overnight phase exists to find exactly this;
  finding it in the morning costs 1 point, finding it before you
  sleep costs nothing.
- Archive pruning that deletes *before* confirming the new archive
  exists — the ordering bug that empties backups. If your
  healthcheck checks archive freshness, you catch it; say so.
