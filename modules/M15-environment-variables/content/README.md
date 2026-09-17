# M15 — Environment Variables & Dotfiles

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

> The configuration layer of your shell — and the #1 source of "works
> in my terminal, fails in my script/notebook/cron" bugs. By the end,
> environment debugging is a three-command reflex.

**Lessons**

| # | Lesson | You will be able to |
|---|--------|---------------------|
| 1 | [01-the-environment.md](lessons/01-the-environment.md) | Explain what the environment is, how it inherits, and how to inspect it |
| 2 | [02-export-and-path.md](lessons/02-export-and-path.md) | Set/unset variables correctly, and dissect/debug `$PATH` like a surgical patient |
| 3 | [03-dotfiles.md](lessons/03-dotfiles.md) | Choose the right dotfile for the right change, and predict which changes survive which contexts |
| 4 | [04-secrets-and-venvs.md](lessons/04-secrets-and-venvs.md) | Apply env-var thinking to credentials, virtualenvs, and the DS workflow |

**Labs** — [labs/README.md](labs/README.md): the env-var safari plus
a staged PATH-debugging clinic.

**Practice** — [practice/quiz.md](practice/quiz.md) (20 Q),
[challenges.md](practice/challenges.md) (C1–C5).

**Prerequisite map:** M06 (paths), M09 (pipes/echo). Feeds M14 (sudo
preserves — mostly — your env), M19 (shell config), M22 (SSH drops
some of it), M25 (cron strips most of it), M27 (venv activation *is*
env manipulation).
