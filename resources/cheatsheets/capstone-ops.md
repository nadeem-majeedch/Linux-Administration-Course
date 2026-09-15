# Cheatsheet — Capstone Operations

## Daily operator loop

```bash
systemctl --user status ingest.timer api.service   # what should be running
journalctl --user -u ingest.service --since today  # did it run?
./ops/health.sh                                     # one-page status
```

## Health report essentials (health.sh)

- uptime + load average (vs core count)
- `free -h` memory/swap; `df -h` disks — flag > 80%
- top 5 CPU and top 5 memory processes
- `systemctl --user --failed`
- last run of each scheduled job from its log

## Backup & restore

```bash
./ops/backup.sh                    # snapshot + sync to 2nd location
tar -tzf backups/2026-09-15/data.tgz | head   # VERIFY contents
./ops/backup.sh --restore backups/2026-09-15 /tmp/restore-test
diff -r /tmp/restore-test/projects ~/projects # byte-for-byte proof
```

A backup without a tested restore is a hope, not a backup.

## Runbook must answer (runbook.md)

1. How do I start / stop everything?
2. How do I check it's healthy right now?
3. Where are the logs and how do I read them?
4. How do I restore from backup (exact commands)?
5. How do I roll back a bad config change?
6. What breaks most often, and what do I do first?

## Incident workflow

```
1. Observe   — what exactly is broken? (service? data? disk? network?)
2. Evidence  — status, journalctl, logs, health.sh output
3. Hypothesis — one sentence: "X is failing because Y"
4. Test      — smallest command that confirms/refutes
5. Fix       — minimal change, documented
6. Postmortem — incident-report.md: symptom, evidence, cause, fix, earlier-catch
```

## Deployment checklist

- [ ] Pipeline scheduled (timer/cron) and logged for 3+ runs
- [ ] API healthy behind nginx; health endpoint answers
- [ ] Secrets in env files (600 perms), never in Git
- [ ] ufw: minimal allows only; SSH key-only (tested from second session)
- [ ] Backup restore test evidenced; watchdog CSV from training run
- [ ] `shellcheck` clean everywhere; fresh-clone runbook followed successfully
