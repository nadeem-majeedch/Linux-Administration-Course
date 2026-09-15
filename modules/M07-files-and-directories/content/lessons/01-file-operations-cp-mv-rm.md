# Lesson 1 — Files & Directories: cp, mv, rm (with Safety)

> Module 07 · Unit 2 · Difficulty: Beginner → Intermediate
> Reading time: ~35 min · Lab: [Lab 1 — Organizing datasets safely](../labs/lab-01-organizing-datasets.md)
> Up next: [Lesson 2 — Inspecting files](02-inspecting-files-file-stat.md)

---

## 1. The commands that can hurt — which is why they're first

Everything in M06 created empty structure: zero damage potential. Today you meet
the trio that *changes* data — copy, move, delete — and the professional
discipline wrapped around them.

The deal this course makes: you **will** learn these commands properly (refusing
to teach `rm` produces administrators afraid of their own shell), and you will
learn them **with the safeguards that make them safe**.

## 2. `cp`: copy

```console
$ cp SOURCE DEST
$ cp SOURCE... DIRECTORY
```

```console
$ cp data/raw/sales.csv data/raw/sales-backup.csv     # copy within a dir
$ cp data/raw/sales.csv ~/archive/                    # copy into a directory
$ cp -r ~/projects/eds-01 ~/archive/eds-01-snapshot   # -r for directories
```

**The rules:**

- Copying a **directory** requires `-r` (recursive). Without it:
  `cp: -r not specified; omitting directory 'eds-01'` — a polite refusal.
- **If DEST exists, it is silently overwritten.** This is `cp`'s sharpest edge:

```console
$ cp new-results.csv results.csv   # results.csv replaced. No warning. Gone.
```

- `-i` = *interactive*: asks before overwriting. `cp -i` is the training-wheels
  flag; by the end of this course you'll protect yourself with habits instead —
  but use it deliberately now.

**DS pattern — the immutable-raws habit:**

```console
$ cp data/raw/sales.csv ~/archive/raw-originals/sales-2026-09-15.csv
```

Copy the original to a dated archive *before* any processing begins. One command,
and "can we get the original data back?" always has the answer yes.

## 3. `mv`: move or rename

```console
$ mv OLD NEW
$ mv SOURCE... DIRECTORY
```

```console
$ mv draft-report.md report.md         # rename in place
$ mv results.csv experiments/2026-09-15/   # move into dated folder
$ mv -i processed.csv data/processed/  # ask if something's in the way
```

`mv` is one command with two effects: rename (same directory) or relocate
(different directory) — mechanically identical: the name changes location.

**The overwrite risk is identical to `cp`**: `mv x results.csv` where
`results.csv` exists destroys it without asking. `-i` interposes a prompt.

`mv` has one beautiful safety property worth knowing: *within the same
filesystem*, moving is instant regardless of file size — it's a rename in the
directory table, not a byte-copy. That's why `mv 500GB-dump.csv archive/` is
instant while `cp` of the same file takes minutes.

## 4. `rm`: remove — read this section twice

`rm` deletes. There is **no recycle bin**, no undo, no trash folder on a server.
What `rm` removes is gone; the only recovery is a backup you made earlier
(M24's whole religion).

```console
$ rm file.csv              # one file
$ rm -i file.csv           # ask first — the flag you should use while learning
$ rm -r old-experiments/   # directories need -r (recursive)
$ rm -f ...                # force: suppress prompts — discussed below, feared rightly
```

### The compound to respect: `rm -rf`

`rm -rf DIRECTORY` removes an entire tree, silently, instantly. It is a
legitimate, *necessary* tool (cleaning experiment folders, CI workspaces) — and
it is the single command most responsible for professional catastrophes. The
course rule for it:

1. **`ls` the target first.** See exactly what you're deleting:
   `ls old-experiments/` — is that really everything?
2. **Never use with variable paths you haven't verified.** `rm -rf "$DIR"` where
   `DIR` is empty becomes `rm -rf /` territory on some shells — the classic
   disaster story of sysadmin lore. Quote and check.
3. **Absolute or verified-relative paths only.** `pwd` before every `rm -r`.
4. **There is no flag that undoes it.** Backups (M24) or snapshots (M01) are the
   only safety nets.

```console
$ pwd
/home/dsstudent/projects/eds-01
$ ls experiments/2026-09-01/
plots  models
$ rm -rf experiments/2026-09-01     # verified: pwd + ls just above
```

That three-command ritual — *pwd, ls, rm* — is the professional form. Nothing
about it is slow; everything about it is why veterans still have their data.

### `rmdir`: the polite cousin

```console
$ rmdir empty-dir/      # works ONLY on empty directories
rmdir: failed to remove 'empty-dir/': Directory not empty
```

`rmdir` is a safety feature disguised as a limitation: it refuses anything with
contents. For scaffolding cleanups it's ideal; for real deletions you'll use
`rm -r` — deliberately.

## 5. The safe workflow, as a checklist

For any copy/move/delete on data you care about:

1. **`pwd`** — where am I?
2. **`ls` the exact targets** — do I see precisely what I intend to affect?
3. **Predict the outcome in words** ("this moves 3 CSVs into experiments/2026-09-15").
4. Then run it. Anything you can't predict → `-i` first, or ask.
5. **Verify after**: `ls` the destination. Trust the shell's silence only after
   you've confirmed.

## 6. DS walk-through: managing experiment outputs

The scenario this lesson exists for: `experiments/` is filling with runs.

```console
$ cd ~/projects/eds-01
$ ls -lht experiments/
2026-09-15/  2026-09-14/  2026-09-12/   # newest first

$ cp -r experiments/2026-09-12 ~/archive/eds-01-exp-2026-09-12
$ mv experiments/2026-09-12 experiments/archive-keep/
$ ls experiments/2026-09-14/*.tmp
plot-01.tmp  plot-02.tmp
$ rm -i experiments/2026-09-14/*.tmp    # remove: interactive first pass
rm: remove regular file 'experiments/2026-09-14/plot-01.tmp'? y
```

Note what happened: **archive-copy before removal** (raw-material safety),
**dated folders** (self-versioning), **`-i` while patterns are new**. Once
pattern confidence is earned (Lesson 4's globbing), the `-i` comes off — *earned*,
not skipped.

## Exercises (lab-log.md)

1. Copy `~/projects/eds-01/README.md` to `README-backup.md`; verify with `ls -l`
   both. Now copy *over* it again with `cp -i` and describe the prompt.
2. Rename `README-backup.md` → `docs/notes.md` (create `docs/` first). Which
   single command did it? Why didn't you need `cp` at all?
3. Build `~/scratch/` with three empty files; delete the *directory* with
   `rmdir` — read the error. Now with `rm -r`. Which worked, and why did the
   course make you try `rmdir` first?
4. The `mv`-across-filesystems experiment: time `mv` of a file from `~/projects`
   to `/tmp` (`time mv ...`), then a `cp` of the same file back. One line: why
   do the times differ in kind, not just magnitude?
5. Write the three-command ritual (pwd/ls/rm) as you'd perform it to delete
   `~/projects/eds-01/experiments/2026-09-02` — paste the exact commands you
   *would* run, with the `ls` output you'd demand first.
6. A teammate proposes `alias rm='rm -i'` as a permanent safety net (M15 covers
   aliases). Give one argument for, and the strongest argument against (hint:
   what happens on a machine where the alias doesn't exist?).

## Check yourself before Lesson 2

- I can copy files and directories (with `-r`), rename/move, and delete —
  reciting the safety ritual without notes.
- I know exactly when `cp`/`mv` destroy data silently, and the flag that interposes.
- I can explain `rm -rf`'s legitimate uses and its non-negotiable rules.
- `rmdir`'s limitation is, to me, a feature.

## Further reading (official sources)

- `man cp`, `man mv`, `man rm`, `man rmdir`
- GNU Coreutils manual — <https://www.gnu.org/software/coreutils/manual/>

Next: [Lesson 2 — Inspecting files: file, stat, and friends](02-inspecting-files-file-stat.md)
