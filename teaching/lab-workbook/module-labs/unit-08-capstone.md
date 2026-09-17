# Unit 8 Labs — Capstone (M30–M32)

> Sessions S29–S30 + the defense window · the DS-server day and the
> incident drills — the practical exam's dress rehearsal.

| Lab | Module | Duration | Difficulty | Deliverable | Link |
|---|---|---|---|---|---|
| DS Server Administration Lab | M31 | 2 sessions | ★★★ | two-actor server run: 6 phases with evidence | [M31 lab](../../../modules/M31-data-science-server/content/labs/ds-server-lab.md) |
| Drill Book incident 1–2 | M32 | 30' each | ★★★ | 8-step method transcript per incident | [M32 labs](../../../modules/M32-linux-performance-troubleshooting/content/labs/README.md) |
| Drill Book incidents 3–4 | M32 | 30' each | ★★★ | method-fidelity scored (teams) | [M32 labs](../../../modules/M32-linux-performance-troubleshooting/content/labs/README.md) |
| Level 5 ladder (optional) | course | 1 day | ★★★ | full-circle DS platform + overnight run | [labs/level-5-ds-server.md](../../../labs/level-5-ds-server.md) |

## Session mapping

- **S29**: M31 scenario walk → one drill incident live (instructor
  narrates the method) → teams run incidents 1–2
- **S30**: incidents 3–4 + revision circuits; mock practical task
  (ungraded, transcript habit enforced)

## The unit's safety architecture

- **CPU-only, no spend**: every lab has GPU/cloud alternatives
  documented but never required
- **The two-actor lab** uses a *colleague account on the student's own
  VM* — shared-permission work without shared infrastructure
- **Drill incidents are student-staged** by scripts shipped in the
  module — all breakage on their own VM, nothing touches real services

## Checkpoints that matter most

- M31: the cleanup *census* (print, read, then delete own scratch) and
  the restore-verified backup — both are capstone rubric echoes
- M32: method-fidelity scoring — ranked hypotheses, quoted evidence,
  verification as step 7; the drill rubric names each

## Extension routing (★★★)

- M32: blind-diagnosis swap; on-call runbook design
- Level 5 ladder for teams wanting the full-circle experience (also the
  strongest capstone warm-up)

## Instructor staging

- Drill scripts are in the module — verify they run on *this* semester's
  lab image the beforenoon of S29
- [Infrastructure checklist](../../setup-and-delivery/lab-infrastructure.md)
  item 10

## After this unit

**Practical exam (S31)**, **final + capstone defense (S32)**. The drill
scoring, the transcript habit, and the two-actor etiquette are exactly
what those hours test — say it in S29's brief.
