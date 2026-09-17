# M15 — Environment Variables & Dotfiles

> Unit 3 · Command Line Fluency · Difficulty: Beginner → Intermediate
> Prerequisites: [M06](../M06-filesystem-hierarchy/README.md) (paths),
> [M09](../M09-pipes-and-redirection/README.md) (streams)
> Est. time: ~4.5 h (lessons ~95 min, labs ~85 min, practice ~95 min)

**Status: content complete.**

## Learning objectives

By the end of this module you can:

1. **Explain** the environment as per-process, copy-on-inherit
   name=value state, and prove both properties with experiments.
2. **Manipulate** variables precisely — export, unset, empty-vs-
   unset, one-shot injection — and modify `PATH` with prepend/append/
   repair patterns, explaining first-match-wins.
3. **Route** configuration through the correct dotfile using the
   startup matrix (login / non-login / non-interactive), including
   the `profile.d` drop-in pattern for machine-wide defaults.
4. **Apply** environment thinking to secrets (delivery mechanism,
   not vault) and virtualenvs (activation as PATH surgery), with the
   explicitness hierarchy for automation.
5. **Diagnose** any environment bug with the universal method:
   identify the process → read `/proc/PID/environ` → choose the
   injection point.

## What's inside

| Path | Contents |
|------|----------|
| [content/README.md](content/README.md) | Module guide + prerequisite map |
| [content/lessons/](content/lessons/) | 4 lessons: the environment · export & PATH · dotfiles · secrets & venvs |
| [content/labs/](content/labs/) | Lab 1: environment safari · Lab 2: the PATH clinic |
| [content/practice/](content/practice/) | Quiz (+ key) · challenges C1–C6 |
| [content/troubleshooting.md](content/troubleshooting.md) | Eight environment/PATH symptom patterns |

## Definition of done

- [ ] Both labs completed with evidence logs
- [ ] PATH clinic's amputation-and-recovery performed in a subshell
- [ ] Quiz ≥ 16/20; C4 (cron inheritance case file) completed
- [ ] Your dotfiles have a dated backup and pass `bash -n`

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-2--command-line-fluency-m05m09)
- Next: [M16](../M16-package-management/README.md) ·
  Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
