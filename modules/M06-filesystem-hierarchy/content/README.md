# M06 — Filesystem Hierarchy & Navigation: content guide

> The tree you will live in for the rest of your career. Everything
> later — datasets, configs, logs, containers — is located by the
> skills in this module.

**Lessons**

| # | Lesson | You will be able to |
|---|--------|---------------------|
| 1 | [01-navigation-pwd-ls-cd.md](lessons/01-navigation-pwd-ls-cd.md) | Know where you are, see what's there (including hidden files), and move deliberately |
| 2 | [02-paths-absolute-relative-home.md](lessons/02-paths-absolute-relative-home.md) | Build and read absolute/relative paths; use `~`, `.`, `..` fluently |
| 3 | [03-filesystem-hierarchy-tour.md](lessons/03-filesystem-hierarchy-tour.md) | Explain what lives where under the FHS — and why — from `/etc` to `/proc` |
| 4 | [04-project-layout-mkdir-touch.md](lessons/04-project-layout-mkdir-touch.md) | Scaffold DS project trees in one command with `mkdir -p` and brace expansion |

**Labs** — [labs/README.md](labs/README.md): navigation drills and
the FHS scavenger hunt.

**Practice** — [practice/quiz.md](practice/quiz.md) (+ key),
[challenges.md](practice/challenges.md) (6 challenges).

## Learning objectives

By the end of this module you can:

1. **Navigate** any Linux filesystem without getting lost: report
   your position, list contents with meaningful detail, and move by
   absolute or relative path deliberately.
2. **Explain** the single-tree model and contrast it with drive-letter
   systems (C:\, mounts-as-letters).
3. **Reconstruct** the FHS map — the role of `/etc`, `/var`, `/home`,
   `/tmp`, `/usr`, `/opt`, `/bin`, `/sbin`, `/dev`, `/proc`, `/sys`,
   `/run` — and predict where a given kind of file lives.
4. **Distinguish** system territory (needs sudo, rare edits) from
   user territory (`$HOME`, freely editable), and justify the split.
5. **Scaffold** a well-formed data science project directory
   structure (`mkdir -p`, brace expansion) that later modules
   (M07, M19, M26, M31) assume.

## Command-line skills

`pwd` · `ls` (`-l -a -h -F -t -r`, combinations) · `cd` (absolute,
relative, `~`, `..`, `-`, bare) · `mkdir -p` · `touch` · `tree` ·
brace expansion `{a,b}` · hidden files (dotfiles) · `~user` forms.

## Prerequisite map

M05 gave you the terminal itself. This module's output feeds
everything: M07 operates *on* these files, M08 streams *through*
them, M13 permutes *access* to them, M08/M17's disks hold the tree,
and the M31 server layout (`$HOME` vs `/data` vs `/scratch`) is the
FHS applied to one machine.
