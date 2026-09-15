# Lesson 3 — Wildcards, Globbing & Quoting

> Module 07 · Unit 2 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 1 — Organizing datasets safely](../labs/lab-01-organizing-datasets.md)
> Up next: [Lesson 4 — Symbolic & hard links](04-links-and-inodes.md)

---

## 1. One pattern, many files

Wildcards (globs) let one command address *many* files at once — the difference
between deleting ten experiment temp-files one by one and doing it in one line.
Because globbing multiplies power, it also multiplies blast radius; this lesson
pairs every pattern with its check-before-fire move.

**First, the mechanism:** the *shell* expands patterns *before* the command runs.
`rm *.tmp` never sees `*.tmp` — the shell hands it `plot-01.tmp plot-02.tmp ...`.
(Proof below, with `echo`, the safest possible command.)

## 2. The pattern vocabulary

| Pattern | Matches | Example |
|---|---|---|
| `*` | any string, including empty | `*.csv` — every CSV |
| `?` | exactly one character | `run-?.log` — run-1.log, run-A.log |
| `[abc]` | one of the listed chars | `sales-[123].csv` |
| `[a-z]`, `[0-9]` | one char in the range | `chunk-[0-9][0-9].parquet` |
| `[!abc]` | one char *not* listed | `data-[!0].csv` |

```console
$ echo *.csv
sales.csv customers.csv returns.csv        # the shell did this, not echo
$ echo run-{1..3}?.log
run-1?.log run-2?.log run-3?.log           # braces (M06) + globs compose
$ echo data-?.csv
data-1.csv data-2.csv data-3.csv data-A.csv
$ echo data-[0-9].csv
data-1.csv data-2.csv data-3.csv
```

**Behaviors worth knowing:**

- Hidden files (dotfiles) are **not** matched by `*` — `rm *` will not delete
  `.bashrc`. (This is a safety feature; use `.*` deliberately, carefully.)
- No match → the pattern is passed through **literally**: `rm *.xlsx` in a
  folder with none tries to remove a file literally named `*.xlsx` and fails
  with "No such file" — informative, not dangerous, but worth expecting.

## 3. Check-before-fire: the echo ritual

`echo` costs nothing and reveals exactly what the shell will do:

```console
$ echo rm experiments/2026-09-12/*.tmp
rm experiments/2026-09-12/plot-01.tmp experiments/2026-09-12/plot-02.tmp ...
```

Read the expansion. If the list is precisely your intent, run the real command
(press ↑, remove `echo`). If anything unexpected appears in that list — a
`models/`, a `.csv` you forgot — the echo just saved your experiment folder.
**Glob + destructive command without echo is how experiments die.**

## 4. Quoting: teaching the shell where words end

The shell splits your line on whitespace. Quoting controls that split — and each
quote type has different physics:

| Syntax | Expansion happens? | Special chars? | Use for |
|---|---|---|---|
| `'single'` | **no** — literal | none | text with `$`, globs you *don't* want expanded |
| `"double"` | **yes** — `$var`, `$(cmd)` expand | mostly preserved | text containing variables |
| no quotes | shell decides everything | split on spaces, globs expand | single simple words only |

```console
$ echo "my home is $HOME"
my home is /home/dsstudent
$ echo 'my home is $HOME'
my home is $HOME
$ echo *.csv
sales.csv customers.csv returns.csv
$ echo "*.csv"
*.csv
```

**The space rule (memorize):** quote anything with spaces. Unquoted:

```console
$ touch quarterly report.csv     # TWO files: 'quarterly' and 'report.csv'
$ ls
quarterly  report.csv            # and neither is what you meant
```

Quoted:

```console
$ touch "quarterly report.csv"   # ONE file — but now, forever, you must quote it
```

This is why M06 banned spaces in names: not because Linux can't handle them, but
because every future `cp`, `mv`, script and glob must then carry the quotes
correctly. Spaces in *data* files you download: fine (quote them). Spaces in
names *you* create: self-inflicted quoting debt.

## 5. Escaping: quoting's surgical alternative

A backslash makes the *next* character literal:

```console
$ echo \$HOME
$HOME
$ touch my\ file.txt        # works, but... you must keep doing this, forever
$ rm my\ file.txt
```

One-off escapes are fine; escaping the same filename across ten commands is the
moment to rename it (`mv "my file.txt" my-file.txt`) and end the tax.

The professional corner-case that escaping solves: a file *named like a flag*
(an unlucky export called `-r`, or `-f` output):

```console
$ rm -i -- -r               # '--' ends options; '-r' is treated as a filename
$ rm ./-r                   # a path prefix works too
```

`--` and `./`-prefixing are M01's Lesson-7 ideas made practical: options end,
operands begin.

## 6. DS patterns: taming data folders

```console
# All September CSVs into the month's folder (check with echo FIRST):
$ echo mv data/raw/2026-09-*.csv data/raw/2026-09/
$ mv data/raw/2026-09-*.csv data/raw/2026-09/

# Every experiment's .tmp, gone — after echo verification:
$ echo rm -i experiments/*/plots/*.tmp
$ rm -i experiments/*/plots/*.tmp

# Only the 'chunk-' numbered files, not 'chunk-final':
$ echo chunk-[0-9][0-9].parquet
chunk-01.parquet chunk-02.parquet

# Copy configs (hidden!) explicitly:
$ cp .env.example .env
```

Log-handling pattern (M24 will build on this): keep logs by date, glob by
prefix — `mv app-2026-09-*.log logs/archive/` — rather than by "everything",
which is how `*.log` eats the still-open active log.

## Exercises (lab-log.md)

1. In `~/scratch`: create `a.csv b.csv c.txt a.csv.bak`. Predict, then run:
   `echo *.csv`, `echo *.?sv`, `echo [ab].*`, `echo *.[^c]*`. Reconcile every
   surprise.
2. The echo ritual: expand `rm experiments/*/plots/*.tmp` with `echo` in your
   `eds-01` project. How many files would it hit? Any directories in the list
   (and why does that matter for `rm` without `-r`)?
3. Create `my notes.txt` (space intentional). Show three ways to `rm` it —
   quotes, backslash, Tab. Which will you use at 2 a.m.?
4. Explain the difference between `echo "$HOME"` and `echo '$HOME'` — then
   between `echo *` and `echo "*"` — in one table with four cells of output.
5. Why doesn't `*` match `.bashrc`? Demonstrate with `echo *` and `echo .*`
   (careful: what do `.` and `..` do in that expansion?).
6. A glob "fails" with `ls: cannot access '*.xlsx'` — what actually happened,
   and which command *before* `ls` would have shown you?
7. Compose: one brace+glob command that *copies* `data/raw/sales-{mon,tue}.csv`
   to `data/processed/` — but show the `echo` check first.

## Check yourself before Lesson 4

- I can predict glob expansions (`*`, `?`, `[]`) on paper before running.
- Echo-before-destructive is reflex for every globbed deletion.
- I can state all three quoting modes' physics and pick per case.
- I can handle spaces, escapes, and `--` for hostile filenames.

## Further reading (official sources)

- bash manual: Filename Expansion & Quoting —
  <https://www.gnu.org/software/bash/manual/> (§3.5.7–3.5.9)
- `man 7 glob` — the matcher's full rules

Next: [Lesson 4 — Symbolic & hard links: inodes made visible](04-links-and-inodes.md)
