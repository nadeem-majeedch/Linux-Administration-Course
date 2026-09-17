# LA-1 — Navigation & Files Circuit (20 min)

> Assesses: M05–M07 labs · 10 points · evidence transcript required.
> Environment: student's own VM, scratch directory `~/la1` (fresh).

## Tasks

**T1 (3).** In one command each, from anywhere:
- print your current directory;
- jump to `/usr/share/doc` and back to where you were using the
  shortest forms taught in class;
- list `/etc` showing *only* directories, hidden included.

**T2 (4).** Build exactly this tree under `~/la1`, then verify:

```text
~/la1/
├── datasets/
│   ├── raw/          (3 files: a.csv, b.csv, c.csv — one line each)
│   └── processed/    (empty)
├── scripts/
└── notes.md
```

Then, using a **single glob**, copy the three CSVs into
`processed/` and prove the copy with a recursive listing that shows
file counts per directory.

**T3 (3).** A staged file `~/la1/.env` exists (instructor or T2
setup). Without printing its contents: show that it exists, show
its size and permissions only, then rename it to `~/la1/env.backup`
and prove the rename with one listing that displays *hidden files*.

## Rubric

| Points | Requirement |
|---|---|
| 1 | T1: `pwd` |
| 1 | T1: `cd -` (or equivalent) used for the return trip |
| 1 | T1: `ls -d /etc/*/` or `find /etc -maxdepth 1 -type d` |
| 1 | T2: tree matches exactly (no extra dirs) |
| 1 | T2: single-glob copy (`cp datasets/raw/*.csv datasets/processed/`) |
| 1 | T2: proof listing (`ls -R` / `find | wc -l` style) |
| 1 | T3: `ls -l .env` (or `stat`) — contents never printed |
| 1 | T3: `mv` used (not cp+rm) |
| 1 | T3: proof with hidden files visible (`ls -la`) |
| 1 | Transcript completeness, commands readable |

## Common failures

- T1 third item answered with `ls /etc | grep ':'` — not a
  directory test; cap 1.
- T2 copying files one-by-one — the objective is glob fluency.
- T3 using `cat`/`head` "just to check" — contents printed = 0 for
  T3 (privacy habit is the point of the `.env` file).
