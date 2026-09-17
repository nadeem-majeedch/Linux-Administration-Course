# Lesson 1 — Viewing & Counting: cat, less, head, tail, wc

> Module 08 · Unit 2 · Difficulty: Beginner-Intermediate
> Reading time: ~25 min · Lab: [Lab 1 — data-quality recon](../labs/lab-01-data-quality-recon.md)
> Up next: [Lesson 2 — finding files & text](02-finding-files-and-text.md)

> Datasets: this module uses six files in [data/](../data/README.md) —
> generate them first:
> `python3 modules/M08-text-processing/content/data/generate_data.py`
> Then, for every command block below, assume you're in
> `modules/M08-text-processing/content/data/`.

---

## 1. Text streams: the raw material

Everything in this module treats a file as a **text stream**: lines
separated by newlines, nothing more. That's the superpower — `grep`,
`sort`, `awk` don't care whether the bytes came from a file, a pipe, or a
network socket. Log file, CSV, TSV, program output: all just streams of
lines. (The mechanics of pipes were built in
[M09](../../../M09-pipes-and-redirection/content/lessons/01-stdin-stdout-stderr-redirection.md);
here we put them to work on data.)

Two properties of your data files to check before any analysis (Lab 1
drills this):

```console
$ file sensor-telemetry.tsv          # what kind of text is this?
sensor-telemetry.tsv: ASCII text
$ wc -l sensor-telemetry.tsv         # how many lines?
5311 sensor-telemetry.tsv
```

CRLF (`\r\n`) endings, BOMs, and tabs-vs-spaces are the classic "why
doesn't my regex match" causes — `file` and `od -c | head` reveal them
(troubleshooting #1).

---

## 2. cat: concatenate (and when NOT to use it)

`cat` dumps files to stdout — its real job is *joining* streams:

```console
$ cat experiment.log | head -5        # works, but see the better way below
$ cat header.txt body.txt > full.txt  # the actual purpose: concatenation
```

**The anti-pattern worth naming:** `cat file | grep thing` is *useless
use of cat* — grep accepts filenames directly (`grep thing file`). The
pipeline costs a process and hides errors from the file. Use cat only
when you genuinely need a stream: multiple inputs, heredocs, or when a
tool can't read files itself.

---

## 3. less: reading files that don't fit your screen

`less` is a pager — opens the file, scrolls, searches, exits without
changing anything. On any real log you'll live here:

```console
$ less server.log
```

Inside less (memorize these six):

| Key | Action |
|---|---|
| `Space` / `b` | forward / back a page |
| `/pattern` | search forward (`?pattern` back), `n`/`N` next/prev match |
| `g` / `G` | top / bottom |
| `-N` | toggle line numbers |
| `F` | follow growth — live tail inside less (Ctrl-C to stop following) |
| `q` | quit |

The analyst's opener on any unfamiliar log is `less +F server.log` —
start *following* like `tail -f`, search backwards when something
interesting scrolls past.

---

## 4. head & tail: edges of the stream

```console
$ head -3 students.csv                 # first 3 lines — check the header
student_id,name,email,program,year,gpa,credits
u001,Amara Okafor,amara.okafor@uni.edu,CS,3,3.46,90
u002,Boris Ivanov,boris.i@uni.edu,DS,2,3.21,60
```

```console
$ tail -3 server.log                   # last 3 lines — the most recent events
$ head -1 transactions.csv             # THE ritual: is there a header? what columns?
```

The first command on any new dataset is `head -1` (schema) followed by
`head -5` (a few rows) — cheap, instant, and prevents the classic
pandas-blew-up-because-no-header incident.

`tail -f` follows a growing file — the live view of any log:

```console
$ tail -f server.log                   # Ctrl-C to stop
```

Two less-known gems:

```console
$ head -c 500 access.log               # first 500 *bytes* (binary-ish safety)
$ tail -n +2 students.csv              # from line 2 onward: header-stripped body
```

`tail -n +2` is *the* idiom for separating a CSV header from its body
(Lab 3 uses it; Lesson 5 builds on it).

---

## 5. wc: counting as a first question

```console
$ wc server.log                        # lines, words, bytes — in that order
  600   7800  60123 server.log
$ wc -l server.log                     # just lines
600 server.log
$ wc -l *.log                          # per-file counts + total
$ wc -l < server.log                   # 600 — filename omitted (stdin trick)
```

Counting lines is the DS reflex: *how many errors? how many rows after
filtering? how big is this before I load it?* Every pipeline in Lesson 5
ends or pivots on a `wc -l`.

---

## 6. The first pipelines: view → filter → count

Everything combines left-to-right:

```console
$ grep ERROR server.log | wc -l
107
$ grep -c ERROR server.log             # same count, one process
107
$ tail -n +2 students.csv | wc -l      # records (not rows!) in students.csv
10
$ grep -c " 404 " access.log           # how many 404s in the web log?
```

`grep -c` vs `grep | wc -l`: same result, but the pipeline generalizes —
insert `sort`, `uniq`, `cut` between the two and it becomes a report
(Lesson 3). Counting is the *simplest* pipeline; learn the shape once.

### DS framing

These five tools are the "look before you load" kit. Before `pd.read_csv`
on a mystery file: `head -1` (columns), `wc -l` (scale), `file` (health),
`less` (sampling). Thirty seconds of shell saves the 40-minute debugger
session when the 12-GB file has a 14-column header row at line 8,914
(they exist; I've met them).

---

## Exercises (lab-log.md)

1. Run the §1 checks on all six datasets. Which files does `file` call
   `ASCII text` vs something else, and why does transactions.csv differ?
2. `head -1` every dataset. Write down the schema of each in one line —
   this table becomes your Lab 1 cheat sheet.
3. Count ERROR and WARN lines in server.log two ways (grep -c; grep | wc
   -l). Confirm both agree, then compute the error *rate* (errors ÷
   total lines) with your own pipeline.
4. Show lines 2–4 of students.csv without head/tail ranges — using only
   `tail -n +2` and `head -3`. Pipeline them; explain the order.
5. What does `wc -l < server.log` print that `wc -l server.log` doesn't,
   and why does the redirect change it? (M09 §1 redux.)
6. (Stretch) `less +F` a copy of server.log after `cat experiment.log >>
   server.log` — wait, don't: instead explain in two sentences why
   appending to a log you're following is realistic (and why the course
   datasets are read-only).

## Check yourself before Lesson 2

- [ ] I reach for `head -1` and `wc -l` before anything else on new data.
- [ ] I know when `cat` is wrong (single-file streams).
- [ ] I can follow a growing log in less and search it backwards.
- [ ] I can strip a header with `tail -n +2`.

## Further reading (official sources)

- `man cat`, `man less`, `man head`, `man tail`, `man wc`
- GNU coreutils manual: https://www.gnu.org/software/coreutils/manual/
- less is more (upstream): https://www.greenwoodsoftware.com/less/
