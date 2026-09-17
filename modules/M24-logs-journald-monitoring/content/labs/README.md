# Module 24 Labs — Logs, Monitoring & Backups

> Four labs, all on your own VM. Logs are read (sudo where needed),
> load is generated only by M18's controlled stress script, and the
> backup lab touches **only user data you create**, on a loopback disk
> from [M17](../../../M17-storage-and-filesystems/content/README.md).

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-log-forensics.md](lab-01-log-forensics.md) | Two prepared incidents (broken service, OOM death) solved purely from journal evidence | ~45 min |
| 2 | [lab-02-live-tail-circuit.md](lab-02-live-tail-circuit.md) | Live-tail journald during events; write a greppable logger; follow a live log | ~40 min |
| 3 | [lab-03-monitoring-under-load.md](lab-03-monitoring-under-load.md) | Read load three ways (vmstat, iostat, sar) with a controlled CPU + I/O workload | ~45 min |
| 4 | [lab-04-backup-test-restore.md](lab-04-backup-test-restore.md) | tar snapshot → rsync mirror to a virtual disk → full test-restore with checksums | ~50 min |

Standing rules (recap):

- Nothing in `/var/log` is edited, moved, or deleted — read-only, always.
- The six-step method from [Lesson 4](../lessons/04-incident-methodology.md)
  structures every incident answer: evidence, then verdict.
- Every lab ends in `lab-log.md` transcripts; the labs grade evidence,
  not speed.
- Broken services are the *user-scope* units you own from M20 — system
  units are never disabled.
