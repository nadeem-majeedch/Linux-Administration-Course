# Lesson 2 — Inspecting Files: file, stat & Metadata

> Module 07 · Unit 2 · Difficulty: Beginner
> Reading time: ~25 min · Lab: [Lab 2 — Metadata detective](../labs/lab-02-metadata-detective.md)
> Up next: [Lesson 3 — Wildcards, globbing & quoting](03-wildcards-globbing-quoting.md)

---

## 1. Inspect before you touch

Professional file handling inverts the beginner instinct: **look first**. What
type of file is this? How big? When did it last change? Who owns it? The three
inspection tools here answer those questions before `cp`/`mv`/`rm` make them
moot.

## 2. `file`: what *is* this thing?

Extensions (`.csv`, `.png`, `.txt`) are **suggestions**, not facts — any file can
carry any name. `file` looks *inside* the bytes and reports what it actually finds:

```console
$ file data/raw/sales.csv ~/Downloads/photo.jpg /etc/hostname
data/raw/sales.csv:     CSV text
/home/dsstudent/Downloads/photo.jpg: JPEG image data, ...
/etc/hostname:          ASCII text
```

```console
$ mv /etc/hostname ~/mystery.dat      # (don't actually do this — demo below uses a copy)
$ file ~/sales-copy.dat
~/sales-copy.dat: CSV text            # renamed .dat, still CSV inside
```

The classic DS catch this tool exists for: a "CSV" that is really UTF-16 from a
Windows export, or gzip-compressed data wearing a `.csv` name. `file` detects
both in one command; a confused pandas session 20 minutes later is the
alternative. **New dataset → `file` it.** Every time.

## 3. `stat`: the full metadata card

```console
$ stat data/raw/sales.csv
  File: data/raw/sales.csv
  Size: 1184         Blocks: 8          IO Block: 4096   regular file
Device: 8,2   Inode: 1183457     Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/dsstudent)   Gid: ( 1000/dsstudent)
Access: 2026-09-15 20:41:03.551992811 +0000
Modify: 2026-09-15 20:40:57.213992811 +0000
Birth:  2026-09-15 20:40:57.213992811 +0000
```

Every field matters somewhere in this course; three you should read fluently now:

| Field | Meaning | Where it matters |
|---|---|---|
| `Size` | bytes | "will it fit on my volume?" (M17) |
| `Inode` | the file's *identity number* on this filesystem | Lesson 5 (links) |
| `Access:` | last **read** time (atime) | forensics: *was this file touched?* |
| `Modify:` | last **content** change (mtime) | **the timestamp that matters** — sorting, backups, "which run is newer?" |
| `Birth:` | creation time (crtime) | lineage questions |

**mtime is the timestamp of the data-science workflow.** `ls -lt` sorts by it,
backups (M24) key off it, and "why does my build think it's stale?" build-system
mysteries are mtime mysteries. Note what `touch` (M06 Lesson 4) does to `Modify:`
— now you can *verify* it:

```console
$ touch data/raw/sales.csv && stat -c '%y' data/raw/sales.csv
```

(`-c` picks the fields — `%y` mtime, `%s` size, `%i` inode — the script-friendly
way to query metadata; M10 uses this heavily.)

## 4. `ls -l` revisited: now the fields make sense

M06 taught the shape; with `stat`'s vocabulary you can read it fully:

```console
$ ls -l data/raw/sales.csv
-rw-r--r-- 1 dsstudent dsstudent 1184 Sep 15 20:40 sales.csv
```

| Field | Value | Now you know |
|---|---|---|
| size | `1184` | bytes — matches `stat` |
| date | `Sep 15 20:40` | **mtime**, by default |
| `1` (2nd column) | link count | one name → this inode (Lesson 5 makes this deep) |

And `ls -lt` vs `ls -lu`: sorting by mtime vs **atime** — the pair that answers
"which output did I *work with* most recently?" vs "which did I merely *look
at*?".

## 5. Hidden files, once more with meaning

`ls -a` showed dotfiles in M06. Now the metadata view:

```console
$ stat -c '%n %s bytes, modified %y' ~/.bashrc
.bashrc 3771 bytes, modified 2026-08-30 10:22:14.000000000 +0000
```

Hidden ≠ protected: dotfiles are fully readable, writable, deletable — the dot
affects only *listing by default*. Two practical notes: config backups
(`cp ~/.bashrc ~/.bashrc.bak`, M15) are themselves dotfiles; and `.ssh/`'s
permissions will one day *gate your logins* (M22). The convention to keep:
sensitive stuff is hidden stuff — but hiding is organization, not security.

## 6. DS workbench: the inspection drill

New dataset arrives. The professional first minute:

```console
$ ls -lh data/raw/sensor-dump.csv          # size, mtime
$ file data/raw/sensor-dump.csv            # real type
$ stat data/raw/sensor-dump.csv            # full card, inode for later
```

Add a directory-size note (`du -sh data/raw/` — disk usage, *summed, human*):

```console
$ du -sh data/raw/
16M     data/raw/
```

...and you know: type is genuine, 1184 bytes, last modified yesterday 20:40,
owned by you, 16 MB folder total. That's the "before" state, on record in
`lab-log.md` — the "after" of any accident now has a baseline to diff against.

## Exercises (lab-log.md)

1. `file` three files: one from `/etc`, one from `~/Downloads`, one you create
   with `touch`. What does `file` say about the empty one — and why is that
   answer honest?
2. Full `stat` on `~/projects/eds-01/README.md`. Record size, inode, mtime,
   birth. Are mtime and birth identical? Why/why not?
3. Touch the file again; `stat` it. Which timestamps moved, which didn't?
   Verify your M06 prediction.
4. `stat -c '%s %Y %n'` on three files — what changed about the output's
   *shape*? Why is this the form a script would use?
5. Rename a CSV copy to `.xyz` and `file` it. Now rename a `.png` to `.csv`
   (copy any image). What does `file` say? What would pandas/pip/cp have
   assumed instead?
6. `ls -l` vs `stat` on the same file: find *two* facts `stat` shows that
   `ls -l` hides, and one that `ls -l` shows more conveniently.
7. `du -sh ~/projects/eds-01` vs `ls -ldh` — why do they disagree? (Think:
   what does each measure?)

## Check yourself before Lesson 3

- I run `file` before opening anything unfamiliar.
- I can read every `stat` field: size, inode, links, atime/mtime/birth.
- I know mtime is the timestamp the workflow sorts by — and what touch moves.
- I can script-query metadata with `stat -c`.

## Further reading (official sources)

- `man file`, `man stat`, `man du`, `man ls`
- GNU Coreutils manual — <https://www.gnu.org/software/coreutils/manual/>

Next: [Lesson 3 — Wildcards, globbing & quoting](03-wildcards-globbing-quoting.md)
