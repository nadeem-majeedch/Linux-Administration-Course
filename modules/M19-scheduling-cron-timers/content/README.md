# Module 19 — Scheduling: cron & systemd Timers · Content Index

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 5 · Software, Storage & Time](../../../COURSE-ROADMAP.md#unit-5--software-storage--time-m16m19).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-5--software-storage--time-m16m19) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> **Status:** Content complete — 3 lessons, 2 labs, quiz + key, 8
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Advanced.

> 🟡 **Module safety contract:** every scheduled job runs against
> `~/lab19/` scratch data; `crontab -r` is banned without a preceding
> `crontab -l` (and used only with an explicit backup of the crontab
> in the transcript); jobs write logs and are idempotent (M11's
> bar). User crontabs and user timers only — no `/etc/cron*` edits.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-cron-fundamentals.md](lessons/01-cron-fundamentals.md) | why scheduling, the daemon, five-field syntax, crontab management (`-e/-l`), @shortcuts, `systemd-analyze calendar` |
| 2 | [02-cron-environment-logging.md](lessons/02-cron-environment-logging.md) | the cron environment trap (PATH, HOME, cwd, tty), mail spool, absolute paths, logging & quiet-success, env differences diagnosed |
| 3 | [03-systemd-timers-production.md](lessons/03-systemd-timers-production.md) | systemd timer+service pairs (`OnCalendar`, `Persistent=true`), cron vs timers, locks & fail-loudly, verify-it-ran discipline |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-schedule-the-pipeline.md](labs/lab-01-schedule-the-pipeline.md) | Schedule M11's hardened `dq.sh`: cron version, timer version, logs prove both ran |
| 2 | [lab-02-cron-debugging.md](labs/lab-02-cron-debugging.md) | Deliberately break the PATH assumption; diagnose "works in my terminal, fails in cron" from evidence |

## Practice & Support

- [Quiz](practice/quiz.md) (20 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M10/M11 scripting](../../M11-advanced-shell-automation/content/README.md) —
  the idempotent, logged, strict-mode script this module schedules.
- [M18 signals](../../M18-processes-jobs-signals/content/README.md) —
  overlapping runs and `nohup` vs timers.
- [M20 systemd](../../M20-systemd-services/content/README.md) —
  units, `journalctl -u`, user services — the timer's machinery.
- [M24 monitoring](../../M24-logs-journald-monitoring/content/README.md) —
  scheduled jobs' logs feed the health kit; the absence alarm runs
  *from* cron.
- [M25 security](../../M25-security-firewall/content/README.md) —
  the patch report and backup jobs scheduled here.
