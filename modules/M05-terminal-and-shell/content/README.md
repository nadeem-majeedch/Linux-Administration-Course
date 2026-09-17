# M05 — The Terminal & Shell: content guide

> Orientation: what the terminal is, how to get truth from it
> (`man`, `--help`), how commands are shaped — and the first
> personalizations (aliases, history) that make it yours.

**Lessons** — terminal vs shell vs console; CLI vs GUI; command
syntax (`command -options arguments`); the help system (`man`
sections, `apropos`, `--help`, `type`); lesson 5's
[05-aliases-and-history.md](lessons/05-aliases-and-history.md):
aliases and the history subsystem (recall, `!!`, interactive
search, when history is written).

**Labs** — [labs/README.md](labs/README.md): Lab 3
(personalize your shell — low risk, reversible). Labs 1–2 (first
login & orientation, man-page tour) live in
[M01's content](../../M01-what-is-linux/content/labs/README.md).

**Practice** — [practice/quiz-aliases-history.md](practice/quiz-aliases-history.md)
(10 Q with key) · [practice/challenges.md](practice/challenges.md)
(5 challenges, ★–★★★).

**Troubleshooting** — [troubleshooting.md](troubleshooting.md):
first-week terminal symptoms (command not found, pager panic,
history gaps, alias surprises) → causes → fixes.

## Learning objectives

By the end of this module you can:

1. **Distinguish** terminal, shell, and console — and explain why
   the CLI remains the administrator's interface (scriptability,
   remote use, precision, evidence).
2. **Parse** command syntax: program, options (short/long, bundled),
   arguments, and the `--` end-of-options convention.
3. **Self-serve** truth: `man` (and its SECTIONS — the skill is
   knowing section 1 vs 5 vs 8), `apropos`/`man -k`, `--help`,
   `type`/`which` for *what am I actually running*.
4. **Personalize** safely: define aliases (including the
   alias-in-scripts limitation), configure history
   (`HISTSIZE`/`HISTCONTROL`), and recall/edit history without
   re-typing.
5. **Adopt** the course's terminal habits: read the error before
   re-running, prefer reversible actions, and treat `man` as the
   first resort — not web search.

## Command-line skills

Terminal anatomy (prompt, cursor, keyboard shortcuts `Ctrl-C/D/L/R/A/E`)
· `man` (+ sections, search within `man` via `/`) · `apropos` ·
`--help` · `type` · `alias`/`unalias` · history (`history`,
`!!`, `!n`, `!string`, `Ctrl-R`, `HISTSIZE`, `HISTCONTROL`) ·
`clear`/`Ctrl-L`.

## Prerequisite map

M01–M04 put a working Linux in front of you; M05 teaches the
*interface to it*. Every later module types into this interface:
M06–M09 are its vocabulary, M15's dotfiles are this module's
personalization done properly, and M19's shell-alias-in-scripts
trap is foreshadowed by quiz question 8.
