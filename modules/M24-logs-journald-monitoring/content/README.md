# Module 24 — Logs, journald & Monitoring · Content Index

> **Status:** Content complete — 5 lessons, 4 labs + 6 backup exercises, Mini-Project E,
> quiz + key, 8 challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Advanced.

> 🟡 **Module safety contract:** labs read logs (sudo where needed),
> generate load only from M18's controlled scripts, and back up **user
> data only** to virtual/loopback targets. No log files are edited or
> deleted; no system services are modified beyond the user-scope units
> carried over from M20.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-journald-journalctl.md](lessons/01-journald-journalctl.md) | journald storage & priorities, journalctl queries (-u/-f/-b/-p/--since/-g), structured fields, DS server use |
| 2 | [02-classic-logs-rotation.md](lessons/02-classic-logs-rotation.md) | /var/log tour, syslog/auth/kernel logs, dmesg, log levels, logrotate & retention, greppable application logs |
| 3 | [03-monitoring-toolkit.md](lessons/03-monitoring-toolkit.md) | uptime/load, free, vmstat, iostat, sar/sysstat, df/du recap, the utilization–saturation–errors frame |
| 4 | [04-incident-methodology.md](lessons/04-incident-methodology.md) | the six-step incident method, five recurring DS-server incidents, evidence discipline, postmortems |
| 5 | [05-backups-recovery-deep-dive.md](lessons/05-backups-recovery-deep-dive.md) | full/incremental/differential, tar + gzip/bzip2/xz, rsync --link-dest snapshots, retention & rotation, off-site, restore runbooks, disaster recovery |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-log-forensics.md](labs/lab-01-log-forensics.md) | Two prepared incidents (broken user service, OOM death) solved purely from journal evidence |
| 2 | [lab-02-live-tail-circuit.md](labs/lab-02-live-tail-circuit.md) | Live-tail journald while events happen; write a greppable logger; watch a service's own log |
| 3 | [lab-03-monitoring-under-load.md](labs/lab-03-monitoring-under-load.md) | Run M18's stress load and read it three ways (vmstat, iostat, sar), interpreting each in the lab log |
| 4 | [lab-04-backup-test-restore.md](labs/lab-04-backup-test-restore.md) | tar snapshot → rsync mirror to a second virtual disk (M17) → **full test-restore** with sha256 verification |
| + | [backup-exercises.md](labs/backup-exercises.md) | The six backup exercises: scheduled cleanup, dataset/experiment/config backups, deleted-dataset restore drill (RTO timed), scheduled integrity verification |

## Mini-Project

- [Mini-Project E — Server health & backup kit](mini-project-health-backup-kit.md):
  `health.sh` (one-page report), `backup.sh` (3-2-1 targets + restore
  mode), plus a written incident report from Lab 1.

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Performance Clinic (extension)

The four resource streams in depth — CPU, memory/swap, disk I/O, network —
with bottleneck signatures and a diagnose-first load clinic:
[performance/README.md](performance/README.md).

## Cross-references

- [M20 systemd](../../M20-systemd-services/content/README.md) —
  journalctl -u begins where systemctl status ends.
- [M18 processes](../../M18-processes-jobs-signals/content/README.md) —
  the stress script and OOM post-mortem return as evidence sources.
- [M17 storage](../../M17-storage-and-filesystems/content/README.md) —
  the second virtual disk and df/du skills come from there.
- [M08 text processing](../../M08-text-processing/content/README.md) —
  every classic-log query is a grep/cut/sort/uniq pipeline.
- [M29 deployment](../../M29-web-servers-databases/README.md) —
  production services log here; the health kit fronts the capstone.
