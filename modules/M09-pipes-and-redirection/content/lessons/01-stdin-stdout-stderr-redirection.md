# Lesson 1 — stdin, stdout, stderr & Redirection

> Module 09 · Unit 2 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 1 — Log wrangling with redirection](../labs/lab-01-log-wrangling.md)
> Up next: [Lesson 2 — Pipes, chaining & command substitution](02-pipes-chaining-substitution.md)

---

## 1. Every program speaks three streams

Since Lesson 5 you've seen programs *print*. The precise model: every process
opens three standard streams at birth:

| Stream | # | Default connection | Purpose |
|---|---|---|---|
| **stdin** | 0 | your keyboard | input the program reads |
| **stdout** | 1 | your screen | normal output |
| **stderr** | 2 | your screen | errors, warnings, diagnostics |

The numbers matter: streams are *file descriptors* — kernel-level handles — and
the redirection operators are literally spelled with them.

Why stdout and stderr are separate: so you can capture a program's *results*
without its *noise* (and vice versa). A script that processes 10 GB of CSV and
also emits progress messages must be able to send those two things different
places — that's the whole point.

## 2. Redirection: reconnecting the streams

`>` sends stdout into a file (creating it, or **truncating** it):

```console
$ date > now.txt
$ cat now.txt
Tue Sep 15 22:41:03 UTC 2026
```

`>>` **appends** instead of truncating — the difference between "I lost the
log" and "I grew the log":

```console
$ date >> now.txt
$ cat now.txt
Tue Sep 15 22:41:03 UTC 2026
Tue Sep 15 22:41:11 UTC 2026
```

`<` feeds a file into stdin:

```console
$ wc -l < /etc/os-release
10
```

(`wc -l` counts lines; here it read the *file's contents* via stdin rather than
opening the file itself — subtle now, meaningful when the "file" is really a
device or generated stream.)

### The stderr operators

```console
$ ls /nonexistent > out.txt          # stdout captured... but:
ls: cannot access '/nonexistent': No such file or directory   # stderr leaked to screen!

$ ls /nonexistent 2> errors.txt      # 2> captures stderr
$ cat errors.txt
ls: cannot access '/nonexistent': No such file or directory

$ ls /nonexistent > all.txt 2>&1     # both into one file (order matters!)
$ ls /nonexistent &> all.txt         # bash shorthand, same effect
```

Read `2>&1` carefully — it's "send stream 2 to *wherever stream 1 currently
goes*", which is why it must come **after** `> all.txt`. Getting this backwards
is a classic script bug; `&>` is bash-only but unambiguous.

### `/dev/null`: the discard stream

```console
$ ls /nonexistent 2> /dev/null       # errors: gone, on purpose
$ echo $?
2
```

`/dev/null` accepts and discards everything written to it (M06's /dev tour).
Silencing *stderr* deliberately — after you've seen it once — is standard
professional hygiene in scripts that must run quietly.

## 3. `tee`: split the stream — watch AND keep

`>` sends output one place only. `tee` copies stdout to *both* a file and
onward to the screen (and to a pipe — Lesson 2):

```console
$ free -h | tee mem-snapshot.txt
               total        used        free      ...
Mem:           3.8Gi       612Mi       2.1Gi ...
$ cat mem-snapshot.txt               # same lines, now on disk
```

`tee -a` appends. The pattern is everywhere in operations: *watch a long job
live while preserving its transcript* — training runs (M27), pipeline logs
(M11), incident debugging (M24).

## 4. Swapping which stream is which

One more professional move: separate *results* from *noise* in opposite
directions:

```console
$ grep -r TODO . > found.txt 2> grep-errors.txt    # results here, noise there
$ sort data.txt > sorted.txt 2> sort-failures.log
```

A pipeline that ends clean, with an audit trail of what failed and why —
this is the seed of every logging strategy this course builds (M11, M19, M24).

## 5. DS walk-through: wrangling a log stream

The scenario: a nightly job appends to `job.log`; you want the errors today,
and a growing archive overall.

```console
$ cd ~/projects/eds-01/logs
$ echo "INFO job started" >> job.log
$ echo "ERROR disk nearly full" >> job.log
$ echo "INFO rows=1000" >> job.log

$ grep ERROR job.log > errors-today.txt        # errors only, on disk
$ cat errors-today.txt
ERROR disk nearly full

$ grep -v INFO job.log | tee problems.txt      # non-INFO lines: seen AND saved
ERROR disk nearly full
```

And the CSV case — *headers* and *data* are both lines; redirection lets you
split them without an editor:

```console
$ head -1 data/raw/sales.csv > processed/header.csv    # header preserved
$ tail -n +2 data/raw/sales.csv > processed/body.csv   # +2 = "from line 2 on"
$ wc -l processed/header.csv processed/body.csv
```

(`tail -n +2` is "start at line 2" — the standard CSV body extraction.)

## 6. When redirection lies to you (preview of pitfalls)

- `> file` with the *same* file as input truncates it to zero **before** the
  command reads it: `sort notes.txt > notes.txt` destroys `notes.txt`.
  (Write-to-temp-then-move is the cure — M11.)
- Order matters: `cmd 2>&1 > file` sends stderr to the *screen* (stream 1's
  old target) and stdout to the file — usually not what you meant.
- Redirection happens *before* the command runs: a failed command still
  creates (possibly empty) output files. `ls` them before assuming success.

## Exercises (lab-log.md)

1. Build `streams.txt` with three `echo ... >>` lines. Then one command that
   saves its output AND appends to the same file (`tee -a`). Verify.
2. Run three commands that produce stderr (`ls /root`, `ls /nonexistent`,
   `cat /etc/shadow`). For each: capture stderr to a file, then stdout-only
   to another. Show both files' contents.
3. `wc -l /etc/os-release` vs `wc -l < /etc/os-release` — outputs differ how?
   Why does stdin-form lose the filename from the report?
4. Combine: one command writing stdout to `out.log`, stderr to `err.log`,
   *and* proving with `echo $?` that the command failed. Which order did the
   operators go?
5. The truncation trap: `printf 'a\nb\nc\n' > trap.txt` then
   `sort trap.txt > trap.txt` — what's in it now, and why? Fix with a temp
   file; verify.
6. DS drill: split any CSV (or the M01 dataset list) into header + body via
   `head -1` and `tail -n +2`; then rejoin with `cat header body >
   rejoined.csv` and diff against the original (`diff` or `cmp`).
7. A script's output is *supposed* to be silent but spams your screen. Name
   the two operators that make it silent-and-archived, and the one you'd
   check first (`echo $?`) to know whether silence hides failure.

## Check yourself before Lesson 2

- I can name the three streams, their numbers, and default connections.
- `>`, `>>`, `<`, `2>`, `2>&1`, `&>`: I can use all six correctly.
- I know what `tee` and `tee -a` split, and when to reach for them.
- I know the same-file truncation trap and its temp-file cure.

## Further reading (official sources)

- bash manual: Redirections — <https://www.gnu.org/software/bash/manual/>
- `man tee`, `man wc`, `man tail`
- M06 Lesson 3's quoting rules govern *what* gets redirected — worth a re-read

Next: [Lesson 2 — Pipes, chaining & command substitution](02-pipes-chaining-substitution.md)
