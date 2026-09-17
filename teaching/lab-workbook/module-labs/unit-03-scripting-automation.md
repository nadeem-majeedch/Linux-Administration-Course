# Unit 3 Labs — Scripting & Automation (M10–M11)

> Sessions S9–S10 · the skeleton becomes muscle memory here.

| Lab | Module | Duration | Difficulty | Deliverable | Link |
|---|---|---|---|---|---|
| First guarded scripts | M10 | 30' | ★★ | 3 scripts with guards + `shellcheck` clean | [M10 lab 1](../../../modules/M10-bash-scripting/content/labs/README.md) |
| Fix-the-bug set (8 scripts) | M10 | 45' | ★★★ | each script fixed + one-line bug diagnosis | [M10 lab 2](../../../modules/M10-bash-scripting/content/labs/README.md) |
| Automation bench | M11 | 30' | ★★★ | idempotent batch processor + per-file logs | [M11 labs](../../../modules/M11-advanced-shell-automation/content/labs/README.md) |
| Mini-Project A | M10 | HW | ★★★ | experiment-directory generator | [M10 practice](../../../modules/M10-bash-scripting/content/practice/challenges.md) |

## Session mapping

- **S9**: first guarded scripts (lab 1 starts in class)
- **S10**: fix-the-bug set (the method demo precedes it) + automation
  bench; Mini-Project A is HW alongside **A1 release**

## What "done" means here

- `set -euo pipefail` present *and* explained in a checkpoint answer
- Every script: argument guard → work → explicit exit status
- `shellcheck` clean is the release bar — the linter is the reviewer
- Fix-the-bug: the *diagnosis line* is graded as heavily as the fix

## Checkpoints that matter most

- The `|| true` exemption question (lab discussion) — separating
  `set -e` belief from mechanism
- The bug-diagnosis lines: "quoting: `$f` splits on spaces" beats "fixed
  it"

## Extension routing (★★★)

- M10: strict-mode refactor challenge; the shellcheck-zero mandate
- M11: the idempotent-deploy challenge

## Instructor staging

None — VMs only. The fix-the-bug scripts ship in the module lab.

## After this unit

**A1 (Assignment 1)** builds directly on this unit + Unit 2 — its
script section grades the skeleton and guards; released S10, due end
of week 6 ([assessment calendar](../../teaching-plan/assessment-schedule.md)).
