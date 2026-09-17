# Module 20 — systemd, Services & Boot · Content Index

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 6 · Services, Networking & Security](../../../COURSE-ROADMAP.md#unit-6--services-networking--security-m20m25).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-6--services-networking--security-m20m25) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> **Status:** Content complete — 4 lessons, 2 labs, quiz + key, 8
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Advanced.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-systemd-units-concepts.md](lessons/01-systemd-units-concepts.md) | PID 1, unit types, targets, enable vs start, dependencies |
| 2 | [02-systemctl-operations.md](lessons/02-systemctl-operations.md) | systemctl verbs, status reading, journalctl -u basics, user services (the lab's spine) |
| 3 | [03-unit-files.md](lessons/03-unit-files.md) | anatomy of a unit file, key directives, writing your own user service |
| 4 | [04-boot-process-recovery.md](lessons/04-boot-process-recovery.md) | firmware → bootloader → kernel → systemd; boot targets, systemd-analyze, recovery paths; **system identity & hardware discovery** (hostnamectl, uptime, lscpu, lsblk, dmidecode-lite) as the admin's morning routine |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-service-circuit.md](labs/lab-01-service-circuit.md) | Inspect, stop/start/restart/enable real services; the hello user service |
| 2 | [lab-02-break-and-fix.md](labs/lab-02-break-and-fix.md) | Break a user unit three ways, diagnose from status + journal, fix each |

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M17 storage](../../M17-storage-and-filesystems/content/README.md) —
  fstab becomes mount units; automount is systemd-native.
- [M18 processes](../../M18-processes-jobs-signals/content/README.md) —
  services are processes with supervision; OOM/limits return here as
  unit directives.
- [M19 cron/timers](../../M19-scheduling-cron-timers/README.md) —
  timers vs cron.
- [M24 logs](../../M24-logs-journald-monitoring/README.md) —
  journalctl deep dive.
- [M29 deployment](../../M29-web-servers-databases/README.md) — your API
  server ships as a unit file.
