# Lesson 4 — Creating Your Project Layout: mkdir & touch

> Module 06 · Unit 2 · Difficulty: Beginner
> Reading time: ~20 min · Lab: [Lab 1 — Navigation drills](../labs/lab-01-navigation-drills.md) (uses this) · [Lab 2](../labs/lab-02-fhs-scavenger-hunt.md)
> Up next: [M07 Lesson 1 — Files & directories: cp, mv, rm](../../../M07-files-and-directories/content/lessons/01-file-operations-cp-mv-rm.md)

---

## 1. From navigating to building

Lessons 1–3 taught you to *walk* the tree. Today you start *building* in it: the
two commands that create empty structure — directories with `mkdir`, empty files
with `touch` — and the brace-expansion trick that scaffolds a whole project in
one line.

Creating empty things sounds trivial; it is exactly the right first creation
tool, because empty files and directories are **impossible to break**: nothing
inside them yet. (The dangerous era begins with `cp`/`mv`/`rm` — next module.)

## 2. `mkdir`: make directories

```console
$ mkdir ~/projects/eds-01
mkdir: cannot create directory '/home/dsstudent/projects/eds-01': No such file or directory
```

`mkdir` refuses to build a floor under a missing staircase: if the parent
(`~/projects`) doesn't exist, the command fails. Two honest responses:

```console
$ mkdir ~/projects          # build the parent first
$ mkdir ~/projects/eds-01   # then the child
```

or the one-step way:

### `mkdir -p`: build the whole ladder

```console
$ mkdir -p ~/projects/eds-01/data/raw
$ ls -R ~/projects          # -R recurses: shows the tree you just built
/home/dsstudent/projects:
eds-01

/home/dsstudent/projects/eds-01:
data
...
```

`-p` creates **every missing parent** on the way — and, crucially, **says nothing
and exits 0 if the target already exists** (no error, no harm). That property
makes `mkdir -p` the *idempotent* workhorse of scripts (Module 11): safe to run
again, safe to schedule (M19). When a lab script's first line is
`mkdir -p "$OUT"`, that's the reason.

Naming conventions worth locking in now: lowercase, hyphens not spaces
(`eds-01`, not `EDS 01!`) — spaces are legal but force quoting forever
(M07 Lesson 4), and no spaces is the free habit that prevents a whole class of
script bugs.

## 3. `touch`: create empty files, and update timestamps

```console
$ touch ~/projects/eds-01/README.md
$ ls -l ~/projects/eds-01
-rw-r--r-- 1 dsstudent dsstudent 0 Sep 15 21:40 README.md
```

Two behaviors, one command:

1. **File doesn't exist → create it, empty.** This is the scaffold use: READMEs,
   `.gitignore`s, placeholder logs.
2. **File exists → do NOT touch its contents; update its modification time.**
   (`stat file` before/after shows mtime jump — M07 Lesson 3.)

That second behavior is why `touch`'s name is perfect — and why it is *not* a
file editor. An empty `README.md` you fill in with an editor (M07 Lesson 2);
`touch` just ensures it exists.

## 4. Brace expansion: scaffold a project in one line

The shell can generate word lists from a pattern — `{a,b,c}` becomes `a b c`:

```console
$ echo {raw,processed}
raw processed
$ echo file{1..3}.csv
file1.csv file2.csv file3.csv
```

Combine with `mkdir -p` and a directory tree appears in one command:

```console
$ mkdir -p ~/projects/eds-01/{data/{raw,processed},logs,notebooks}
$ tree ~/projects/eds-01
/home/dsstudent/projects/eds-01
├── data
│   ├── processed
│   └── raw
├── logs
└── notebooks

5 directories
```

That single line replaced five `mkdir` calls. Brace expansion is pure shell
convenience (it happens *before* the command runs — `mkdir` only ever sees the
expanded list), and it is the same trick you'll use for per-experiment output
folders:

```console
$ mkdir -p ~/projects/eds-01/experiments/{2026-09-01,2026-09-02}/{plots,models}
```

**Caution with `..` ranges:** `{1..1000000}` really does create a million
arguments. Braces expand *silently*; the command after them inherits the blast
radius. For now, ranges stay small.

## 5. The DS pattern: one dataset project, end to end

The convention this course uses from here on (you'll build it in Lab 1):

```
eds-01/
├── README.md            # what this project is, how to re-run it
├── data/
│   ├── raw/             # original files, NEVER modified
│   └── processed/       # derived, regenerable
├── notebooks/           # exploration (M27)
├── logs/                # run logs (M11, M24)
└── experiments/         # dated output folders
```

Three rules that make this layout *work* rather than merely *exist*:

1. **`raw/` is read-only by discipline.** Originals never change; everything
   derived lands in `processed/` and can be rebuilt from raw. (You will enforce
   this with permissions for real in M12–M13.)
2. **Experiments are dated folders, not overwritten files.** `experiments/
   2026-09-02/` beats `results-final-FINAL2.csv` — the filesystem already gives
   you versioning if you let it.
3. **Logs live in `logs/`, always written, never deleted** — Module 24's
   incident analysis will read them.

## Exercises (lab-log.md)

1. Build (don't reuse) a practice tree: `mkdir -p ~/projects/scratch/{a,b}/c`.
   Show `tree` output, then run the *same* `mkdir -p` line again — what happened,
   and why is that behavior precious in scripts?
2. Create `~/projects/eds-01/README.md` with `touch`; `ls -l` it — what is the
   size? Then `touch` it again 30 seconds later; what changed on the `ls -l`
   line, what didn't?
3. One command, full scaffold: use brace expansion to create
   `~/projects/eds-02/{data/{raw,processed},logs}`. Paste the line and its
   `tree` output.
4. Predict: what does `mkdir -p ~/x` do if `~/x` exists *as a file*? Try it
   (create `~/x` with `touch` first if needed). Read the error — what is it
   telling you?
5. Why does `raw/` get a "never modify" rule when nothing in Linux *forces* it
   yet? What changes in M12–M13 to make it enforceable?
6. Give two reasons the course bans spaces in directory names you create — and
   name the technique that *would* make spaces safe (next module).
7. Time-travel drill: `mkdir -p ~/projects/eds-01/experiments/2026-09-{01,02}`
   — what tree results? Verify.

## Check yourself before M07

- `mkdir` vs `mkdir -p`: I can explain both, including the idempotency of `-p`.
- I know `touch` creates *or* re-stamps — never edits.
- I can scaffold a nested project with one brace-expansion line.
- My `~/projects/eds-01` skeleton exists and follows the course convention.

## Further reading (official sources)

- `man mkdir`, `man touch`; GNU Coreutils manual —
  <https://www.gnu.org/software/coreutils/manual/>
- bash manual: Brace Expansion — <https://www.gnu.org/software/bash/manual/>

Next: [M07 Lesson 1 — Files & directories: cp, mv, rm](../../../M07-files-and-directories/content/lessons/01-file-operations-cp-mv-rm.md)
