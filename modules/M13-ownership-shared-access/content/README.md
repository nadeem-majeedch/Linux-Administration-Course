# Module 13 — Ownership & Shared Access · Content Index

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

> **Status:** Content complete — 2 lessons, 2 labs (incl. permission
> clinic), quiz + key, 10 challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-ownership-chown-shared-dirs.md](lessons/01-ownership-chown-shared-dirs.md) | chown/chgrp mechanics, shared dirs, sticky bit, constitutional tree |
| 2 | [02-acls-permission-clinic.md](lessons/02-acls-permission-clinic.md) | ACLs, mask, default ACLs, permission clinic method |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-build-shared-tree.md](labs/lab-01-build-shared-tree.md) | Build the constitutional shared tree |
| 2 | [lab-02-permission-clinic.md](labs/lab-02-permission-clinic.md) | Diagnose-and-fix 6 real patients (incl. NFS ticket) |

## Practice & Support

- [Quiz](practice/quiz.md) (20 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (10, C1–C10)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M12 permissions](../../M12-users-groups-permissions/content/lessons/02-permissions-chmod-umask.md) —
  prerequisites (bits, umask, identity).
- [M18 processes](../../M18-processes-jobs-signals/README.md) —
  daemons and who they run as.
- [Capstone](../../../projects/capstone/student/SPEC.md) — shared trees and least
  privilege are scored in RUBRIC §2.
