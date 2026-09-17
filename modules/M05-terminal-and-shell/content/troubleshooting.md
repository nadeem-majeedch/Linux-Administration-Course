# Module 05 Troubleshooting — Terminal & Shell Symptoms → Causes → Fixes

> Six patterns from the first week at a keyboard. Each: **symptom →
> likely cause → diagnosis → fix → prevention**. Every diagnosis
> command is safe; nothing here needs sudo.

## 1. `command not found` for something you just read about

**Cause:** the tool isn't installed, or it is installed but not on
your `$PATH` ([M15](../../M15-environment-variables/README.md)), or
it's a *shell builtin* your alternative shell lacks.
**Diagnose:** `type -a commandname` — tells you nothing found vs a
path; `which commandname` for the executable case only.
**Fix:** install it ([M16](../../M16-package-management/README.md))
or fix the spelling; `type` output distinguishes the two.
**Prevent:** when pasting from any tutorial, read the command aloud
first — most "not found" errors are typos or package-name ≠
command-name mismatches.

## 2. The man page opens but you can't get out

**Cause:** `less` (man's pager) has keybindings, not mouse.
**Diagnose:** none needed — `h` inside the pager shows them.
**Fix:** `q` to quit; `/pattern` then `n`/`N` to search
forward/back; `g`/`G` to jump to top/bottom.
**Prevent:** [M01's man tour](../../M01-what-is-linux/content/labs/README.md)
makes the pager muscle-memory; do it once.

## 3. History "lost" a command you know you ran

**Cause:** each terminal writes its history only on exit; two open
terminals overwrite each other, and Ctrl-C'd commands may never be
written.
**Diagnose:** `history | tail -20` in the *other* terminal.
**Fix:** `history -a` (append now) before switching windows; search
interactively with Ctrl-R instead of relying on recall.
**Prevent:** [Lesson 5](lessons/05-aliases-and-history.md) explains
*when* history is written — treat it as per-session until you know
your shell's settings.

## 4. Aliased command behaves differently than the tutorial says

**Cause:** your distribution or dotfiles pre-alias common commands
(`ls` is often `ls --color=auto`; on some systems `grep` too).
**Diagnose:** `type -a ls` shows the alias shadowing the real binary.
**Fix:** `\ls` or `command ls` bypasses the alias for one invocation.
**Prevent:** when documenting for others, show the unaliased
behavior — it's what `type` reveals.

## 5. Terminal renders garbage after `cat`ting a binary

**Cause:** binary bytes reconfigured your terminal's character set.
**Diagnose:** your prompt looks like gibberish — that *is* the
diagnosis.
**Fix:** `reset` (or `clear` first, `reset` if that fails).
**Prevent:** don't `cat` binaries; use `file` ([M07](../../M07-files-and-directories/README.md))
to check what a file is before displaying it.

## 6. `--help` output scrolls away before you can read it

**Cause:** the terminal buffer scrolled, not lost — but beginners
don't know where it went.
**Diagnose:** none — this is a read-the-output problem.
**Fix:** pipe it: `command --help | less` — your first pipe
([M09](../../M09-pipes-and-redirection/README.md)) solves it.
**Prevent:** make `| less` a reflex for any long output.
