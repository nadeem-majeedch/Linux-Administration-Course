# Module 14 — Sudo & the Root Principle · Content Index

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 4 · System Administration](../../../COURSE-ROADMAP.md#unit-4--system-administration-m12m15).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-4--system-administration-m12m15) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> **Status:** Content complete — 1 lesson, 2 labs, quiz + key, 7
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate.
> ⚠️ All practice is scoped to your own VM/WSL2; see safety notes in every
> file.

## Lesson

| # | File | Topic |
|---|------|-------|
| 1 | [01-root-sudo-sudoers.md](lessons/01-root-sudo-sudoers.md) | root (UID 0), su vs sudo, sudoers rules, visudo, drop-ins, NOPASSWD, Defaults, the five-beat sudo workflow |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-sudo-practice.md](labs/lab-01-sudo-practice.md) | Mechanics, audit trail, redirection wall, scoped drop-in, safe break-and-repair |
| 2 | [lab-02-sudo-incidents.md](labs/lab-02-sudo-incidents.md) | Three diagnose-and-repair tickets (timeout policy, includedir breakage, dpkg lock) |

## Practice & Support

- [Quiz](practice/quiz.md) (18 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C7)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M12 identity](../../M12-users-groups-permissions/content/lessons/01-identity-users-groups.md) and
  [M13 shared access](../../M13-ownership-shared-access/content/README.md)
  — prerequisites; sudo builds directly on both.
- [M20 services](../../M20-systemd-services/README.md) — `sudo -u` for
  inspecting daemons' environments.
- [M24 logs](../../M24-logs-journald-monitoring/README.md) — where
  sudo's audit trail lives and how to query it.
