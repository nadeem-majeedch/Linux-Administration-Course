# Module 19 Labs — Scheduling

> Two labs under `~/lab19/`. All jobs are user-level (crontab +
> user timers), target scratch data only, and end with log-file
> proof. `crontab -r` appears only behind the backup-first rule.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-schedule-the-pipeline.md](lab-01-schedule-the-pipeline.md) | Schedule M11's hardened `dq.sh` three ways: cron, forced timer run, real timer — with the two-minute rule and log proof | ~55 min |
| 2 | [lab-02-cron-debugging.md](lab-02-cron-debugging.md) | Break the PATH assumption on purpose; diagnose "works in terminal, fails in cron" via mail spool, `env -i`, and env diff | ~45 min |

Standing rules (recap):

- `crontab -l > ~/lab19/crontab.backup` before any destructive
  crontab operation; transcripts show the backup.
- Every job: absolute paths, explicit PATH, strict mode, logs.
- Proof-of-run is the deliverable: log lines with timestamps, not
  "I think it ran".
- Two-minute rule for every new schedule before its real one.
