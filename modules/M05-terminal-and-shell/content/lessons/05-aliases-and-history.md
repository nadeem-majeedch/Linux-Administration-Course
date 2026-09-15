# Lesson 5 — Aliases & History: Making Fluency Compound

> Module 05 · Unit 2 · Difficulty: Beginner
> Reading time: ~25 min · Lab: [Lab 3 — Personalize your shell](../labs/lab-03-personalize-your-shell.md)
> Companion: M09 Lesson 2 §6 (first contact with both, in pipeline context)

---

## 1. The idea: stop re-typing, start re-calling

Everything you type well this course, you'll type *hundreds* of times. The shell
ships with two acceleration layers — **history** (recall the past) and **aliases**
(rename the frequent) — that together turn a 60-character pipeline into six
keystrokes. This lesson makes both deliberate instead of accidental.

## 2. History: the mechanism

Bash keeps your commands in a per-session list and writes them to
`~/.bash_history` when the session ends. Facts worth knowing:

- **↑/↓** walks the list; **Ctrl+R** searches it interactively (type a fragment,
  repeat Ctrl+R to cycle hits, Enter to run, arrows to edit).
- The `history` command lists everything with line numbers.
- The list lives in *memory* until exit (default: 500–1000 entries; configurable
  via `HISTSIZE`/`HISTFILESIZE` — M15's dotfile work).
- Commands from *other* terminals don't appear until they exit (or
  `history -a` forces an append) — the classic "where did my command go?"
  mystery between two windows.

### History expansion: the `!` family

```console
$ history | tail -3
  512  free -h
  513  grep ERROR logs/job.log | wc -l
  514  date
$ !512              # run #512 again
$ !!                # previous command — the classic: sudo !!
$ !free             # most recent command STARTING with 'free'
$ !grep:p           # PRINT what it would run, don't run it (the :p modifier)
```

**The `:p` modifier is the safety latch**: any `!` expansion can be previewed by
appending `:p`. History expansion happens *before* the command runs — that is
its power and its danger. M07 Lesson 1's warning about `sudo !!` applies in
full: **preview with `:p` until the reflex is trained.**

## 3. Aliases: naming your reflexes

An alias maps a short name to a longer command — expanded *by the shell at
typing time*:

```console
$ alias ll='ls -lh'
$ alias lht='ls -lht'
$ alias gs='git status'          # (previewing M26)
$ ll
$ alias | grep ll                # inspect what you've defined
$ unalias ll                     # remove one
```

Rules and physics:

- Alias expansion is the *first* thing that happens to a line — before globs,
  variables, history expansion. The alias's *value* is then processed as a
  normal command line (quotes inside it were resolved at definition).
- **Interactive shells only.** Scripts never see your aliases (they run
  non-interactive shells) — that's why M09's quiz called alias-based safety a
  trap and pointed functions' way (M10).
- **Persistence is dotfile work:** today's aliases die with the session unless
  written into `~/.bashrc` (M15 does this properly, with backups). Lab 3 gets
  you a *temporary-till-M15* taste of persistence.

### What deserves an alias?

A decision heuristic worth writing down: alias it if (a) you type it daily,
(b) it has flags you *always* pass, and (c) the expansion is safe to re-run
blind (`ll`: yes; something deleting things: no). One-command, read-only,
muscle-memory builders — that's the honest territory. Multi-step or
parameterized logic belongs to functions (M10), scripts (M10), and eventually
Makefiles/tools.

### The dangerous corner

`alias rm='rm -i'` feels protective and *is* — on this machine, in this shell,
until the day you work on a server where it isn't set and your guard is down.
Aliases are per-environment sugar; safety must survive environments. Course
position: aliases for convenience, habits for safety.

## 4. The two together: the daily loop

The compound workflow this lesson exists to install:

1. Type the long form once, carefully.
2. Use it via **Ctrl+R** for days.
3. Notice you type it daily → alias it (Lab 3).
4. Notice the alias needs arguments/branching → *that's* the moment for M10.

Fluency compounds: each artifact you build becomes one keystroke.

## Exercises (lab-log.md)

1. `history | wc -l` — how many commands this session? Find your longest
   command via `history | awk '{print length, $0}' | sort -rn | head -3`
   (paste-and-run is fine — decode it in M08).
2. `!`-family drill: run `date`, then `!!:p` (prints, doesn't run — verify
   nothing *new* executed), then `!!`. Log the difference `:p` made.
3. Define `alias lht='ls -lht'`; use it in `~/projects/eds-01`. Then
   `unalias lht` and confirm it's gone. Which one *would* you persist?
4. In a script file (`echo 'lht' > t.sh && bash t.sh`): does the alias work?
   Quote the error and write the one-line rule this proves.
5. Ctrl+R archaeology: recover your longest M09 pipeline. How many keystrokes
   from search-hit to re-run?
6. Design review: a classmate proposes `alias backup='cp -r data/ /tmp/backup'`.
   Two criticisms from this lesson (hint: /tmp's contract, M06 Lesson 3; and
   what happens when data/ doesn't exist — M09's `&&` thinking).

## Check yourself before the next module

- I can list, define, and remove aliases — and state their persistence story.
- I can use `!!`, `!n`, `!prefix`, and preview with `:p`.
- I know aliases don't reach scripts — and why that killed the safety-alias idea.
- My daily loop (type → Ctrl+R → alias → function) is conscious now.

## Further reading (official sources)

- bash manual: Aliases & History Interaction —
  <https://www.gnu.org/software/bash/manual/> (§6.6, §9.3)
- `help alias`, `help history` (builtins — Lesson 3 taught which help applies)

Next: [M06 — Filesystem Hierarchy & Navigation](../../../M06-filesystem-hierarchy/content/lessons/01-navigation-pwd-ls-cd.md)
