# Lesson 7 — Command Syntax: Options & Arguments

> Module 01 · Unit 1 · Difficulty: Beginner
> Reading time: ~25 min · Lab: [Lab 3 — First commands](../labs/lab-03-first-commands.md)
> Up next: [Lesson 8](08-setup-vms-wsl2-ubuntu.md)

---

## 1. The anatomy of a command line

Every command you type this course has the same grammar:

```
prompt>  command   -options   --long-options   arguments
         ───┬───   ────┬────   ──────┬──────   ────┬────
            │          │            │            │
        what to run   modifiers    modifiers    what to act on
        (a program    (usually     (usually     (files, text,
        or builtin)   change       change       usernames…)
                      behavior)    behavior)
```

Words are separated by **spaces** (any number of them — the shell collapses runs of
spaces). The shell splits your line into words, finds the program, and hands it the
rest as *options* and *arguments*.

**You do not type the prompt.** When this course shows:

```console
$ whoami
dsstudent
```

…you type `whoami` and press Enter. `$` is the prompt (Lesson 5); the line below is
the output.

## 2. Reading a SYNOPSIS (the grammar notation, decoded)

Man pages compress the grammar into a SYNOPSIS line. Its punctuation is a language:

```
ls [OPTION]... [FILE]...
date [OPTION]... [+FORMAT]
cp [OPTION]... SOURCE DEST
cp [OPTION]... SOURCE... DIRECTORY
```

| Notation | Meaning |
|---|---|
| plain word (`ls`) | type exactly this |
| `[brackets]` | optional — you may omit it |
| `...` | repeatable — one or more allowed |
| italics/UPPERCASE (`FILE`, `+FORMAT`) | you substitute your actual value |
| `a \| b` | choose one |
| no brackets (`SOURCE DEST`) | required |

Read `cp [OPTION]... SOURCE DEST` aloud: "cp, optionally some options, then a
required SOURCE and a required DEST." That is why `cp` with one argument fails with
a usage error — the synopsis told you it needs two. You now can read every man page's
grammar on any server you ever touch.

## 3. Options: short, long, combined

**Short options:** one letter, one dash. **Long options:** a word, two dashes.

```console
$ ls -a        # short: -a
$ ls --all     # long: same meaning, more readable
```

Two equal forms are deliberate: short for fast typing, long for scripts and prose
(readability wins in scripts you'll re-read in Module 10).

**Combining** short options — one dash, several letters, identical to repeating them:

```console
$ ls -l -a -h
$ ls -lah        # the same thing; the common idiom
```

**Option arguments** — some options take a value of their own:

```console
$ ls -l --block-size=M       # long form: separate word after =
$ head -n 3 file.txt         # short form: value follows the flag
$ head -n3 file.txt          # short forms may also glue
```

**`--` the end-of-options marker** — everything after `--` is treated as an argument,
even if it *looks* like an option. You will use this in Module 7 to delete a file
that an unlucky rename called `-r`. For now: know the marker exists; it is the
professional habit that disarms a classic trap.

## 4. Arguments

Arguments are the *operands*: files, directories, text, usernames.

```console
$ echo hello                 # one argument
$ echo hello   world         # still two arguments; shell collapses the spaces
hello   world                # ...and echo joins them with ONE space when printing
$ echo "hello   world"       # quotes preserve the spacing: one argument, exact text
hello   world
```

Notice what quoting did: without quotes the shell split the line into two arguments;
with double quotes it became **one** argument containing the spaces. Quoting decides
where words end — a theme that dominates shell scripting (Module 10). For now:
**quote anything containing spaces.**

**Order:** most commands accept options before, between, or after arguments
(`ls -l /tmp` and `ls /tmp -l` both work), but the portable, read-always-first habit
is **options first, then arguments** — some commands and some non-GNU systems are
stricter, and strictness never hurts the reader.

## 5. Exit codes: the command's report card

Every command ends with a number sent back to the shell: **0 = success, anything
else = something failed.** Read it with `$?`:

```console
$ whoami
dsstudent
$ echo $?
0
$ whoami --no-such-option
whoami: unrecognized option '--no-such-option'
$ echo $?
1
```

You will live on exit codes from Module 10 (scripts deciding what to do next) and
Module 24 (jobs that "fail loudly" instead of silently). Meet it now as a fact of
the grammar: commands *report*, and the shell remembers.

## 6. A first toolkit (all safe, all read-only)

Run each, observe, and match to the synopsis you read in Lesson 6.

```console
$ date
Tue Sep 15 21:04:11 UTC 2026
$ date +%Y-%m-%d
2026-09-15
```

`date` with no options = now; with `+FORMAT` = your chosen shape (`%Y` year, `%m`
month, `%d` day). You will use this to timestamp backups and logs (M11, M24) —
filenames like `backup-$(date +%F).tar.gz` are born here.

```console
$ whoami
dsstudent
$ hostname
ubuntu-ds-lab
$ id
uid=1000(dsstudent) gid=1000(dsstudent) groups=1000(dsstudent),27(sudo)
```

`id` = who the system thinks you are: your numeric user id (`uid`), primary group
(`gid`), and group memberships. This user is in the `sudo` group — meaning it may
*borrow* admin rights (Module 14 explains how carefully we will do that). On a
shared server, `id` is how you verify you are who you think you are.

```console
$ uname -srm
Linux 6.8.0-45-generic x86_64
```

Kernel name, release, architecture in one line — the three facts you quote in every
"help me" forum post, in one command.

```console
$ ls
Desktop  Documents  Downloads  Music  Pictures  snap  Videos
$ ls -l /etc/hostname
-rw-r--r-- 1 root root 14 Aug 30 10:22 /etc/hostname
```

`ls` lists; `ls -l` *long-lists*: permissions (`-rw-r--r--`), owner (`root`),
group (`root`), size, date, name. You are not expected to decode that string yet —
Module 12 is devoted to it — but note that `/etc/hostname` belongs to `root`, not
to you: your first glimpse of the multi-user system.

## 7. Prediction drills (do these before the lab)

Write your prediction *before* running each. Then run, compare, and reconcile —
the reconciliation is where learning happens.

1. `date +%A` — what will print?
2. `echo one two three` — how many arguments did echo receive? How many words printed?
3. `echo "one two three"` — same question.
4. `id -un` — (check `id --help` first) what does it print?
5. `ls -l /etc/hostname /etc/os-release` — one command, two arguments: what happened?
6. `uname -a` vs `uname -srm`: which fields does the first show that the second omits?
7. `echo $?` immediately after a successful command; then after `date --bogus`.
   Two different numbers — which, and why?

## Exercises (lab-log.md)

1. Decode in one sentence each: `ls [OPTION]... [FILE]...` and
   `mkdir [OPTION]... DIRECTORY...` — how many arguments does each *require*?
2. Show three equivalent ways to run `ls` with long format, human sizes, and all
   files. Which would you use in a script? Why?
3. Run `date --help`. Write your own `date` command that prints
   `2026-09-15T21:04` — then the exact format string you used.
4. What does the `--` marker do? Describe a situation (even hypothetical) where it
   saves you.
5. Explain to a classmate why `echo $?` prints `0` after success *and* why that is
   not an error. What does 0 mean?
6. Run `id` and `hostname` on your machine; record your uid, your groups, and
   hostname. Are you in the `sudo` group?
7. The grammar is the contract: give one example where knowing the SYNOPSIS saves
   you from a mistake that trial-and-error alone might teach wrongly.

## Check yourself before Lesson 8

- I can name the four parts of a command line and never type the prompt.
- I can read `[OPTION]...`, required vs optional, and repeatable in a SYNOPSIS.
- I know short vs long options, combined shorts, and option arguments.
- I know what quoting changes and what `$?` reports.

## Further reading (official sources)

- GNU Coreutils manual (ls, date, echo…) — <https://www.gnu.org/software/coreutils/manual/>
- bash manual: exit status — <https://www.gnu.org/software/bash/manual/bash.html#Exit-Status>
- Lesson 6's man-page skills are the reference for every option used here

Next: [Lesson 8 — Setup: VMs, WSL2 & Ubuntu](08-setup-vms-wsl2-ubuntu.md)
