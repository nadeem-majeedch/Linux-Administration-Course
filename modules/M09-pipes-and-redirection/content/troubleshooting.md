# Module 09 — Troubleshooting Guide

Streams, pipes, and substitution failures at this stage.

## 1. The pipe "does nothing" (no output, no error)

A command upstream produced nothing: `grep ERROR file` with zero matches sends
an empty stream onward — `wc -l` will honestly answer `0`. Diagnose stages
singly: run the first command alone, then add stages one at a time. Empty is
a *finding* (no errors today — good), not a malfunction.

## 2. Output file is empty but the command "ran"

You redirected the wrong stream: progress messages were stderr; your `>`
captured stdout only. Check: run without redirection, *see* which class of
line carries your data, then redirect accordingly (or `&>` both).

## 3. `command not found` for something you piped to

Typo after the pipe (`| wc -1` — digit one, not ell), or the tool isn't
installed (`tree`, `jq`). `which <name>` locates; M16 installs.

## 4. `ambiguous redirect` error

Quoting problem in the redirection target: `cmd > $FILE` where `$FILE`
contains spaces, or `cmd 2> > file` (double-redirect typo). Quote variables:
`cmd > "$FILE"` (M10 formalizes).

## 5. The `2>&1` order surprise

`cmd 2>&1 > file` left errors on the screen — because fd 1 pointed at the
screen when `2>&1` cloned it. Rule: file-first (`cmd > file 2>&1`) or bash's
`&>`. Re-read Lesson 1 §2's mechanism line whenever this bites.

## 6. Truncated a file I meant to sort/copy

`sort f > f` (or `cp f f`-style same-target) truncates before reading. If
empty now: recovery per M07's troubleshooting §3 (snapshot/backups). Cure for
next time: temp-then-move — `sort f > f.tmp && mv f.tmp f`.

## 7. Pipeline output differs between runs

Interleaving and buffering can reorder merged streams (`2>&1` cases); also
`tee`'s file may lag the screen by buffering. For *analysis*, don't merge
streams mid-pipeline; split them to files and analyze each.

## 8. `$(...)` printed nothing into my command line

The inner command produced no stdout (empty substitution = empty string), or
quoting swallowed it: `echo "$(date)"` vs `echo '$(date)'` — the single-quote
case is literal text (M07 Lesson 3's physics). Check the inner command alone
first.

## 9. Alias doesn't work in my script

By design: scripts run non-interactive shells without alias expansion (quiz
Q19). Convert the alias to a variable or function (M10) — or paste the
pipeline itself. This is the alias/function handoff moment.

## 10. History lost between terminals

Each terminal appends its own history at exit; closed abruptly (or several
open at once) can drop entries. `history -a` forces a save; persistent,
sized history is `~/.bashrc` configuration (M15: `HISTSIZE`, `HISTFILESIZE`).
