# Lesson 2 — Paths: Absolute, Relative, and ~

> Module 06 · Unit 2 · Difficulty: Beginner
> Reading time: ~25 min · Lab: [Lab 1 — Navigation drills](../labs/lab-01-navigation-drills.md)
> Up next: [Lesson 3 — The Filesystem Hierarchy tour](03-filesystem-hierarchy-tour.md)

---

## 1. A path is an address

A **path** is the route the filesystem tree takes to reach a file or directory.
Linux paths have exactly one syntax — components separated by `/`:

```
/home/dsstudent/data/sales-2019-q1.csv
│    │         │    └── file name
│    │         └── directory
│    └── your home
└── root of the tree
```

Every command that touches files takes a path. The skill is knowing the *three
kinds* of path and choosing deliberately.

## 2. Absolute paths: from the root

An **absolute path** starts with `/` and is spelled from the root of the tree. It
means the same thing **no matter where you currently are**:

```console
$ cd /var/log      # from anywhere: same place
$ cd /etc/hostname # this names one specific file
```

**When to use absolute paths:** in scripts and configuration (Module 10's rule:
*scripts use absolute paths* — they may run from any directory), in cron jobs
(M19), anywhere the "where am I?" question must not matter.

## 3. Relative paths: from where you stand

A **relative path** starts with anything *except* `/` and is interpreted from your
**current working directory** (`pwd`). Two spellings dominate:

| Path | Meaning |
|---|---|
| `data/file.csv` | the file inside the `data` folder *beneath me* |
| `./data/file.csv` | identical meaning — `./` says "beneath me", explicitly |
| `../notes.txt` | one level **up**, then `notes.txt` |
| `../../archive` | two levels up, then `archive` |

`.` (dot) = *this directory*; `..` (dot-dot) = *the parent*. Both are real entries
you saw with `ls -a` in Lesson 1.

Walk the example — starting in `/home/dsstudent/projects`:

```console
$ pwd
/home/dsstudent/projects
$ cd ../data            # up to home, down into data
$ pwd
/home/dsstudent/data
$ cd ../projects/eds-01 # up again, then down
$ pwd
/home/dsstudent/projects/eds-01
```

**When relative paths shine:** interactive work inside your own project ("the file
next to me"), and Tab completion, which works beautifully with them.

**The trap to memorize now:** the same relative path means different things from
different places. `rm -rf ../build` (Module 7 will teach this command properly —
do NOT run it now) executed from the wrong directory deletes a *different* `build`.
This is the #1 beginner catastrophe, and the cure is habit: **`pwd` before
consequences.**

## 4. `~` : your home, and other people's

`~` (tilde) is shell shorthand, expanded *by the shell* before the command runs:

| Spelling | Expands to |
|---|---|
| `~` | your home directory (`/home/dsstudent`) |
| `~/data` | your `data` folder |
| `~ben` | *Ben's* home — `/home/ben` (you may not be allowed to look — Module 12) |
| `~+` | current directory (rarely needed; `.` covers it) |

Two pieces of tilde trivia that prevent real confusion:

- `~` works at the **start** of a path (or standalone). In the *middle*
  (`/home/~ben`) it is just a directory literally named `~` — which nobody has.
- `~` is **not** understood by every program — it's the shell that translates it.
  Inside quotes with special contexts or in some config files you may need the full
  `$HOME` expansion instead (Module 15). For daily `cd`, `ls`, `cp` use: `~` is safe.

## 5. Resolving practice: one target, four spellings

Say your target is `/home/dsstudent/data/raw/sales.csv` and your current directory
is `/home/dsstudent/data/raw` (you know this because you ran `pwd` — right?).

| Spelling | Kind | Works from |
|---|---|---|
| `sales.csv` | relative | only *here* |
| `./sales.csv` | relative (explicit) | only *here* |
| `/home/dsstudent/data/raw/sales.csv` | absolute | anywhere |
| `~/data/raw/sales.csv` | tilde + relative | anywhere (if it's *your* home) |

All four address the same file. Fluency is matching spelling to situation:
quick interactive work → relative; scripts → absolute; cross-machine or
"always my stuff" → tilde.

## 6. When paths go wrong: reading the error, not guessing

```console
$ ls ~/Data
ls: cannot access '/home/dsstudent/Data': No such file or directory
```

Three lessons hiding in one error line:

1. **Case sensitivity** — `Data` ≠ `data`. Linux distinguishes; tab completion
   prevents.
2. The shell **expanded `~` for you** in the error (`/home/dsstudent/Data`) —
   errors quote the resolved path, which is diagnostic gold.
3. "No such file or directory" is *almost always literally true*: the path, as
   spelled, does not exist. `ls` the parent directory to see what *does* exist
   before re-typing.

```console
$ cd /etc/ssh/../..          # dot-dot chains work anywhere in a path
$ pwd
/                            # /etc/ssh/../.. = /etc/../.. wait—
```

Careful: `/etc/ssh/../..` = up from `ssh` to `etc`, up from `etc` to `/`. The rule
is mechanical — each `..` cancels the component before it. (`realpath` — Lesson
below — does this arithmetic for you.)

## 7. Two helpers: `realpath` and `basename`/`dirname`

```console
$ realpath ../data/../projects
/home/dsstudent/projects              # the cleaned-up absolute answer

$ basename /home/dsstudent/data/raw/sales.csv
sales.csv
$ dirname /home/dsstudent/data/raw/sales.csv
/home/dsstudent/data/raw
```

`realpath` resolves any path — including `..` chains and symbolic links (M07) — to
its true absolute form; `basename`/`dirname` split a path into name and directory.
They look like trivia today; they are the workhorses of Module 10's scripts
("which folder was that output written to?").

## Exercises (lab-log.md)

1. From your home, write the absolute path of `~/data` *without* running
   anything. Verify with `realpath ~/data`.
2. Starting at `/usr/share/doc`, what is the relative path to `/usr/share`?
   And the absolute one? Verify with `cd` + `pwd`.
3. What is `.` for? Run `ls .` and `ls` — same output? Then `ls -d .` and
   compare with `ls -d ..` — what do the two show?
4. Your classmate runs `cd ~/..` and lands in `/home`. Explain why, then predict
   `cd ~/../..` and verify.
5. Why do we say scripts must use absolute paths? Give the two-sentence argument
   (hint: the same file, two directories, one wrong `../build`).
6. `basename` and `dirname` on `/var/log/syslog` — record both outputs. When
   would a script need *each*? (Guess freely; M10 will confirm.)
7. Tab completion drill: navigate to `/usr/lib/python3/dist-packages` using Tab
   only. Count keystrokes. Now `cd -` back. Count again.

## Check yourself before Lesson 3

- I can write both spellings (absolute/relative) for a file from any starting point.
- I can trace `..` chains mechanically and explain `~`, `~user`.
- I know when each spelling is the right tool, and why scripts get absolutes.
- `pwd`-before-consequences is becoming reflex.

## Further reading (official sources)

- GNU Coreutils manual (pwd, realpath, basename, dirname) —
  <https://www.gnu.org/software/coreutils/manual/>
- bash manual: tilde expansion — <https://www.gnu.org/software/bash/manual/>

Next: [Lesson 3 — The Filesystem Hierarchy tour](03-filesystem-hierarchy-tour.md)
