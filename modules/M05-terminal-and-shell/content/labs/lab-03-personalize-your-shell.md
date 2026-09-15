# Lab 3 — Personalize Your Shell (Aliases & History)

> Lesson 5 · Time: ~30 min · Risk: low — writes only session state and one new
> file in `~/scratch`; no dotfile edits (M15 does that with backups)

## Goal

Build, test, and *justify* an alias set; drill the history-expansion family with
its safety latch. Everything reversible; nothing persistent yet by design.

## Part 1 — Build the alias set (10 min)

```console
$ alias ll='ls -lh'
$ alias lht='ls -lht'
$ alias proj='cd ~/projects/eds-01'
$ alias
```

Test each (`proj` then `ll`). Log: which three *you* would actually keep, using
Lesson 5's three-part test (daily? flags-always? safe-to-rerun-blind?).

## Part 2 — Prove the script boundary (10 min)

```console
$ mkdir -p ~/scratch/m05 && cd ~/scratch/m05
$ echo 'proj' > t.sh
$ bash t.sh
```

Quote the failure (hint: `proj` isn't a command inside the script). Then
demonstrate the *interactive* world it works in: run `proj` in the terminal
itself. Write the one-line rule — and predict what M10's functions will add
(hint: arguments, and scripts can see them).

## Part 3 — History family, with the latch (10 min)

```console
$ date +%F
$ !!:p          # print, don't run — read it before Enter
$ !!            # now run it
$ history | tail -3
$ !date:p       # most recent command starting with 'date': printed only
```

Then the deliberate near-miss: `!l` — **before pressing Enter**, predict which
command `!l` would match (`ls`? `less`? `lht`?). Use `!l:p` to check. Log any
surprise; that gap is exactly why `:p` exists.

## Part 4 — The session file (5 min)

```console
$ history -a                 # force-append to ~/.bash_history
$ tail -3 ~/.bash_history
```

Open a second terminal, run `history | tail -3` there — what's missing and
why (Lesson 5 §2)? Then `history -a` again in terminal 1 and re-check. Log the
mechanism in one line.

## Wrap-up checklist

- [ ] Alias set defined, tested, and *justified* (three-part test per alias)
- [ ] Script-boundary failure quoted and explained
- [ ] `!!`, `!n`, `!prefix`, `:p` each demonstrated in the log
- [ ] `:p` caught at least one would-be surprise
- [ ] Session-file mechanics observed across two terminals
- [ ] Nothing outside `~/scratch` and shell state was modified
