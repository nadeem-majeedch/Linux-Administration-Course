# Lesson 3 — Columns & Categories: cut, paste, sort, uniq, tr

> Module 08 · Unit 2 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 3 — the column clinic](../labs/lab-03-column-clinic.md)
> Prerequisites: [Lesson 2](02-finding-files-and-text.md)

> ⚠️ One honesty note before the toolkit: `cut` splits on a **single
> character**. Real CSVs with quoted fields ("Okoye, Ada") will break it.
> This module's CSVs are quote-free *by design* — and §7 tells you when
> to graduate to awk.

---

## 1. cut: extracting columns

```console
$ cut -d, -f2 students.csv                 # field 2, comma-delimited
name
Amara Okafor
Boris Ivanov
...
$ cut -d, -f1,6 students.csv               # fields 1 AND 6 (id, gpa)
$ cut -d, -f2-4 students.csv               # a RANGE: fields 2 through 4
$ cut -d: -f1 /etc/passwd | head -4        # the classic: usernames
$ cut -c1-4 transactions.csv | head -4     # character positions, not fields
```

`-d` delimiter, `-f` fields, `-c` characters. Server logs (space-
separated) cut cleanly too:

```console
$ cut -d' ' -f3 server.log | sort | uniq -c   # level column census (Lesson 2's -o, upgraded)
    107 ERROR
    371 INFO
    122 WARN
```

That three-command pipeline is the module in miniature — and worth
dissecting, because the *adjacency rule* below makes it work.

---

## 2. sort: the glue (and why uniq needs it)

`sort` sorts lines. Its flags do the real work:

| Flag | Effect | Data use |
|---|---|---|
| `-n` | numeric | amounts, years — `-n` or `10 < 9` alphabetically! |
| `-r` | reverse | top-N reports |
| `-k2` | key = field 2 | sort by a column |
| `-k3 -n` | field 3, numeric | sensor temps |
| `-t,` | delimiter , | CSV-aware keying |
| `-u` | unique | sort+dedupe in one |
| `-h` | human sizes | `du -h` output |

```console
$ sort -t, -k3 students.csv | head -3      # by program (field 3)
$ sort -t, -k6 -nr students.csv | head -1  # top GPA first (u009's quoted GPA sorts oddly — see below!)
u007,Grace Mensah,grace.m@uni.edu,CS,4,3.74,120
```

**The adjacency rule (the pipeline's load-bearing fact):** `uniq`
compares *adjacent* lines only. Unsorted input means duplicates scattered
everywhere survive. Hence the invariant: **`sort` immediately before
every `uniq`** — no exceptions until you've deliberately proven order
(which you can't, from grep output).

## 3. uniq: counting and deduplicating categories

```console
$ cut -d, -f4 students.csv | sort | uniq -c      # census: students per program (col 4!)
   2 CS
   5 DS
   1 MATH
   1 PHYS
   1 STAT
   1 program        ← the header; `tail -n +2` first to exclude (idiom #2)
$ cut -d, -f3 students.csv | sort | uniq -c | sort -rn    # ranked
$ cut -d' ' -f3 server.log | sort | uniq -c               # log-level histogram
$ sort transactions.csv | uniq -d                          # WHICH lines are duplicated
TX150,2019-01-09,emea,gadget,145.20
```

`uniq -d` = show duplicated lines; `-u` = show only-unique lines; `-c` =
prefix counts. The **sort | uniq -c | sort -rn** trio is the single most
reused pipeline in data work — a histogram in six characters of intent.

Applied to the *declared dirt* in our transactions:

```console
$ tail -n +2 transactions.csv | sort | uniq -d | wc -l     # how many dup rows?
4
```

Four duplicates — exactly the dirt the dataset README declared. This is
the data-quality reporting that Lesson 5 turns into a reusable recipe.

---

## 4. paste: merging streams side-by-side

```console
$ paste <(cut -d, -f1 students.csv) <(cut -d, -f2 students.csv) | head -3
student_id	name
u001	Amara Okafor
u002	Boris Ivanov
```

`paste` zips streams column-wise (tab default; `-d,` to match). Process
substitution `<(cmd)` (M09 §2) feeds a command's output as a *file* —
paste is where it earns its keep. DS use: pairing IDs with values from
two different extracts for a quick sanity diff.

---

## 5. tr: translating characters

`tr` rewrites character classes on a *stream* — the cleanup tool:

```console
$ echo "cairo" | tr 'a-z' 'A-Z'            # lower → upper
CAIRO
$ head -2 sensor-telemetry.tsv | tr '\t' ','   # TSV → CSV (when fields are clean)
timestamp,sensor_id,temp_c,humidity_pct
$ echo "  padded  " | tr -d ' '            # -d: DELETE characters
padded
$ echo "hello   world" | tr -s ' '         # -s: SQUEEZE repeats
hello world
```

Real data fixes — the students.csv dirt:

```console
$ cut -d, -f2 students.csv | cat -A | grep Nasser   # SEE the trailing space (u006)
u006,Farid Nasser ,farid.n@uni.edu,DS,2,3.23,60$
$ cut -d, -f2 students.csv | tr -s ' ' | sed -n 7p  # squeeze it (row 7 of the output)
Farid Nasser
```

And the comma-decimal GPA from u009 — which arrives *quoted* ("3,77"),
because unquoted it would have broken the 7-field shape (a real CSV
lesson):

```console
$ grep "^u009" students.csv               # the European decimal, quoted
u009,Igor Petrov,igor.p@uni.edu,STAT,3,"3,77",90
$ grep "^u009" students.csv | sed 's/"\([0-9]*\),\([0-9]*\)"/\1.\2/'   # normalized
u009,Igor Petrov,igor.p@uni.edu,STAT,3,3.77,90
```

(`tr` works on *whole classes* and can't edit fields — the quoted-GPA
fix above is sed's job, Lesson 4.)

---

## 6. The category-report template

You now own the full census pipeline. The reusable shape:

```console
$ <extract columns> | sort | uniq -c | sort -rn | head -N
```

against every dataset in this module:

```console
$ cut -d, -f4 students.csv | sort | uniq -c | sort -rn | head -3        # programs
$ cut -d' ' -f3 server.log | sort | uniq -c | sort -rn                  # log levels
$ awk '{print $7}' access.log | sort | uniq -c | sort -rn | head -3     # top endpoints
     67 /api/v1/reports/daily
     67 /api/v1/queries
     65 /api/v1/datasets
$ awk -F'\t' 'NR>1 {print $2}' sensor-telemetry.tsv | sort | uniq -c      # sensors (awk preview)
```

Five lines, five reports, zero Python startup time. *This* is "shell as
first-pass analytics."

---

## 7. When cut is not enough (the honest boundary)

`cut` fails when: fields contain the delimiter inside quotes; or you need
the *last* field (cut can't count from the right); or a log has
variable-width columns. awk handles all three (Lesson 4):

```console
$ awk -F',' '{print $NF}' students.csv     # $NF = last field — impossible in cut
```

Course rule: **cut for quick single-character splits; awk when fields
get clever.**

---

## Exercises (lab-log.md)

1. Build the program census (§6) but for *years* instead of programs.
   Which year has the most students?
2. Ranked transaction amounts by region: extract region, count, rank.
   Then the same for products. Which product dominates, and by how much
   over second place?
3. Find the 4 duplicated transaction rows with `uniq -d` — then confirm
   the *count* of each duplicate with `uniq -c | awk '$1 > 1'` (awk
   preview). Are all four duplicated exactly once?
4. u009's GPA is comma-decimal. Produce a *cleaned* students.csv where
   every GPA uses a dot, using tr — then verify with `grep -c ',[0-9][0-9]$,'
   <(...) || echo clean`. (Careful: email column contains an @ but no
   comma — check before assuming!)
5. Convert sensor-telemetry.tsv to CSV with tr, then count rows *per
   sensor* with your census pipeline. Sensor s2 should be missing 31
   rows (the declared outage) — confirm the exact number.
6. `paste` drill: make a two-column TSV of student_id → email, then
   reverse it (email → id). Why is one direction more useful for a
   lookup file? (Think sort + grep on the lookup.)

## Check yourself before Lesson 4

- [ ] I default to `sort | uniq -c | sort -rn` for any "how many X" question.
- [ ] I know why uniq demands sorted input (adjacency).
- [ ] I can reach for cut, paste, tr appropriately — and know cut's
      single-delimiter limit.
- [ ] I can do arithmetic-top-N with sort -k -n -r without pausing.

## Further reading (official sources)

- `man cut`, `man sort`, `man uniq`, `man paste`, `man tr`
- GNU coreutils manual (each tool has a chapter):
  https://www.gnu.org/software/coreutils/manual/
- POSIX definitions (portable flag semantics): https://pubs.opengroup.org/onlinepubs/9699919799/
