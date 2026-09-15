# Lesson 4 — Symbolic & Hard Links: Inodes Made Visible

> Module 07 · Unit 2 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 2 — Metadata detective](../labs/lab-02-metadata-detective.md)
> Up next: [M09 Lesson 1 — Streams & redirection](../../../M09-pipes-and-redirection/content/lessons/01-stdin-stdout-stderr-redirection.md)

---

## 1. The two-part truth about files

Here is the filesystem's best-kept beginner secret: **a file's name is not the
file.** Every file's data lives in a numbered warehouse box called an **inode**
(the number `stat` showed you in Lesson 2), and directory entries are just
*name → inode-number* mappings.

```
directory table                 inode table              disk blocks
sales.csv        ────────►  inode 1183457  ────────►  [the actual bytes]
customers.csv    ────────►  inode 1183458  ────────►  [the actual bytes]
```

You saw this indirectly already: `ls -l`'s second column is the **link count** —
how many names currently point at that inode. `mv` within a filesystem is instant
precisely because it only rewrites a name mapping, never the bytes. And this
model enables the two tools of this lesson: giving one data-block **more names**
(hard links) and giving it a **shortcut pointer** (symbolic links).

## 2. Hard links: two names, one data

```console
$ stat -c '%h links, inode %i' data/raw/sales.csv
1 links, inode 1183457

$ ln data/raw/sales.csv data/raw/sales-linked.csv    # ln = make a hard link
$ stat -c '%h links, inode %i' data/raw/sales.csv data/raw/sales-linked.csv
2 links, inode 1183457
2 links, inode 1183457
```

Same inode → both names are *equally the original file*. Not copies — two doors
into the same room:

```console
$ echo "appended" >> data/raw/sales-linked.csv
$ tail -1 data/raw/sales.csv
appended                              # the other name sees the change
```

Delete one name:

```console
$ rm data/raw/sales-linked.csv
$ stat -c '%h' data/raw/sales.csv
1                                     # data survives until the LAST name goes
```

That's the real meaning of `rm`: it removes a *name*, and decrements the link
count; the data only dies when the count hits zero. (This, precisely, is why
"deleted" files are recoverable-ish and why "secure deletion" is its own topic.)

**Hard-link rules:** same filesystem only; no directories (sane systems forbid
it); no crossing into other partitions — because inode numbers are only unique
*per filesystem*.

## 3. Symbolic links: pointers with a path inside

```console
$ ln -s data/raw/sales.csv latest-sales.csv    # -s = symbolic
$ ls -l latest-sales.csv
lrwxrwxrwx 1 dsstudent dsstudent 23 Sep 15 22:10 latest-sales.csv -> data/raw/sales.csv
```

Read that line: the first character is **`l`** (link), and the arrow shows the
*stored path*. A symlink is a tiny file whose content is "where to go". Unlike
hard links, it can point at directories, across filesystems — and it can dangle:

```console
$ rm data/raw/sales.csv
$ cat latest-sales.csv
cat: latest-sales.csv: No such file or directory    # the target is gone
$ ls -l latest-sales.csv                            # but the link itself still exists
lrwxrwxrwx ... latest-sales.csv -> data/raw/sales.csv
```

Broken links are normal life, easily audited: `find -xtype l` (M09) lists them.

## 4. The comparison table (this is the exam)

| | Hard link (`ln`) | Symbolic link (`ln -s`) |
|---|---|---|
| Is | a second name for the *same inode* | a small file containing a *path* |
| Survives target rename/move | **yes** (inode unchanged) | no (stored path now stale) |
| Survives target deletion | **yes** — data lives till last link | becomes dangling/broken |
| Crosses filesystems/partitions | no | yes |
| Can point to a directory | no | yes |
| Typical use | backup-style aliasing, snapshot-ish tricks | **shortcuts, version pointers, the FHS /bin merge you verified in M06** |

## 5. Why DS work cares: three real patterns

**1. The "latest" pointer** — the classic:

```console
$ ln -sfn experiments/2026-09-15 experiments/latest
$ ls experiments/latest/
plots  models          # always the newest run, one stable path for scripts
```

Scripts and cron jobs (M19) read `experiments/latest/` and never change; you flip
the pointer when a new run succeeds. `ln -sfn` (force, no-deref) is the idiom —
`-n` treats an existing symlink-to-directory as a file so it gets *replaced*, not
nested-into. Without `-n`, repeating the command builds `latest/2026-09-16/...`
matryoshka links — a rite-of-passage bug.

**2. Big datasets, many views** — a 40 GB corpus used by three projects: hard
link (or symlink) it into each project's `data/` instead of three 40 GB copies.
Disk full at 2 a.m. during training (M17/M27's disaster) is often just
un-learned linking.

**3. Reading the system's own links** — you've *used* these already without the
vocabulary: `/bin -> usr/bin` (M06 Lab 2). Now you can *read* that arrow as what
it is: one set of binaries, two names, history preserved.

## 6. Exercises (lab-log.md)

1. Hard-link two names to one file; append via name B; read via name A. Record
   inode and link counts at each step (`stat -c '%h %i %n' ...`).
2. Delete name B; check count and that data survives. Now delete name A — what
   does `ls` say? Where did the bytes go, really?
3. Symlink `ln -s experiments/2026-09-15 experiments/latest`; `ls -l` it (note
   the `l` and the arrow). Rename the target directory; what is the link now?
   Fix by rebuilding. Which table row predicted this?
4. Try `ln -sfn experiments/2026-09-15 experiments/latest` twice in a row.
   Then try it *without* `-n` twice. Show the matryoshka. Explain `-n` in one
   sentence.
5. Can a hard link cross from your home to `/tmp`? Try it, read the error, and
   connect it to the "per-filesystem inode" rule.
6. Find the system's own symlinks: `ls -l / | grep '\->'`. Pick three arrows and
   explain each in a line.
7. Design decision: a nightly job writes `runs/2026-09-15/`; twelve scripts
   read `runs/current/`. Which link type, why, and what happens the night the
   writer fails? (Think dangling pointers, M19 foreshadowed.)

## Check yourself before M09

- I can explain inode, link count, and "rm removes a name".
- Hard vs symbolic: I can fill the 7-row comparison table from memory.
- `ln -sfn` for the latest-pointer — including what breaks without `-n`.
- I can spot a symlink in `ls -l` output and read its target.

## Further reading (official sources)

- `man ln`, `man 2 link`, `man 2 symlink`
- GNU Coreutils manual — <https://www.gnu.org/software/coreutils/manual/>

Next: [M09 Lesson 1 — stdin, stdout, stderr & redirection](../../../M09-pipes-and-redirection/content/lessons/01-stdin-stdout-stderr-redirection.md)
