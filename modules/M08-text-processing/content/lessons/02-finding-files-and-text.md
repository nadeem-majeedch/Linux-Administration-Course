# Lesson 2 — Finding Files & Text: find, locate, grep & Regex

> Module 08 · Unit 2 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 2 — log forensics](../labs/lab-02-log-forensics.md)
> Prerequisites: [Lesson 1](01-viewing-counting.md)

> 🔒 Safety: `find -delete` is a loaded weapon — this lesson teaches it
> *read-only* (`-print`, `-ls`) and explicitly defers deletion patterns
> to [M07's safeguards](../../../M07-files-and-directories/content/lessons/01-file-operations-cp-mv-rm.md).

---

## 1. find: files by property

`find` walks a directory tree and tests each file against criteria —
name, size, age, type. The syntax is `find WHERE WHAT TODO`:

```console
$ find . -name "*.csv"                     # by name (glob, quoted!)
$ find . -name "*.log" -size +10k          # name AND size: logs over 10 KB
$ find . -name "*.tsv" -mtime -7           # modified within 7 days
$ find . -type d                           # directories only
$ find . -name "*.tmp" -ls                 # detailed listing of matches
```

The three tests you'll use weekly: `-name` (quote the glob or your shell
eats it), `-size` (`+`/`-` prefix: more/less than), `-mtime` (days; `-7`
= recent). For datasets: "where did that 2-GB intermediate file go?"
`find . -size +1G -ls` answers instantly.

**-exec: act on each match** (introduced read-only here):

```console
$ find . -name "*.csv" -exec wc -l {} +    # line counts of every CSV
   11 students.csv
 1062 transactions.csv
 1073 total
```

`{}` = the file path; `+` = batch as many as possible per command
(faster); `\;` = one process per file (slower but needed for commands
that take single args). `xargs` (Lesson 4) is the other half of this
pattern.

**locate:** queries a prebuilt index (`/var/lib/plocate/plocate.db`) —
instant results for *anywhere on disk*, but only as fresh as the last
index update (`updatedb`, usually a daily cron). Use locate for "does
this file exist somewhere?", find for "what's here *right now*?":

```console
$ locate -i transactions | head -3         # case-insensitive; needs the db
$ sudo updatedb                            # refresh (own VM only)
```

---

## 2. grep: the text filter

`grep` prints lines matching a pattern — the single most-used data tool
in this course. Working repertoire:

```console
$ grep "ERROR" server.log                  # basic: lines containing ERROR
$ grep -c "ERROR" server.log               # count matching lines
$ grep -v "INFO" server.log | wc -l        # -v: everything EXCEPT INFO
$ grep -i "error" server.log | head -2     # -i: case-insensitive
$ grep -n "TX240" transactions.csv         # -n: line numbers (13 in our file)
$ grep -r "ERROR" ../ --include="*.log"    # -r: recursive + filter by name
```

**Context flags — the debugging gift:**

```console
$ grep -A2 "FAIL" experiment.log           # 2 lines After the match
$ grep -B1 "500  " access.log              # 1 line Before
$ grep -C2 "404" access.log | head -8      # 2 lines of Context
```

**The two most useful "meta" flags:**

```console
$ grep -l "ERROR" *.log                    # just the FILENAMES that match
$ grep -oE "10\.0\.[0-9]+\.[0-9]+" server.log | head -3    # print only the match
10.0.4.4
10.0.2.4
10.0.4.1
$ grep -oE "10\.0\.[0-9]+\.[0-9]+" server.log | sort -u | wc -l   # unique IPs
44
```

`-o` turns grep from a *line filter* into a *token extractor* — the
bridge to Lesson 3's counting pipelines (extract tokens → sort | uniq -c).

---

## 3. Regex fundamentals — grep's real language

Patterns, not strings. The vocabulary that covers 90% of data work:

| Atom | Matches | Example |
|---|---|---|
| `^` / `$` | start / end of line | `^TX` (lines starting TX) |
| `.` | any single char | `2026-03-..` |
| `*` | 0+ of the previous | `10*` (1, 10, 100…) |
| `[abc]` | one of those chars | `[Ee]rror` |
| `[a-z0-9]` | ranges | hex codes `[0-9a-f]` |
| `\.` | literal dot | `\.edu` |
| `\{n,m\}` | repeat count (BRE) | `[0-9]\{4\}` |

**Basic vs extended regex (`grep` vs `grep -E`):** plain grep is BRE
where `?`, `+`, `|`, `()` are literal — you'd escape them (`\?`). `grep
-E` (what egrep historically was; egrep itself is deprecated but aliased)
turns them into metacharacters:

```console
$ grep -E "WARN|ERROR" server.log | wc -l        # either — union
229
$ grep -E "s[12]" sensor-telemetry.tsv | head -2 # s1 or s2, not s3
$ grep -E "^u00[1-5]" students.csv               # ids u001–u005
$ grep -E "accuracy=0\.[89]" experiment.log      # high-accuracy epochs
```

Both work; **course convention: use `grep -E` and write modern syntax** —
fewer escaping bugs, portable to every tool that speaks ERE (awk, sed -E).

*What regexes deliberately don't cover:* they can't count arbitrary
nesting or parse HTML/JSON reliably. CSV in Lesson 3's note — regexes
match *lines*, not *grammar*. That's why awk exists (Lesson 4).

### DS framing

grep+regex is the log-and-data scalpel: "find every 500 response from
ml-inference after 14:00" is one grep -E away — no Python startup, no
imports, works on a 40-GB file over SSH without loading it into memory.

---

## 4. Putting find and grep together

The full "search everything" move — find feeds grep:

```console
$ find . -name "*.log" -exec grep -l "ERROR" {} +
./access.log
./server.log
```

Or grep's own recursion (`-r --include`) when the tree is simple. Rule
of thumb: `grep -r` for convenience, `find -exec` for control (filtering
by size/age first keeps big trees fast).

---

## Exercises (lab-log.md)

1. Find all CSVs in this module's tree and line-count each with ONE
   command. Which file has the most lines — and is it the biggest file
   in bytes? (Check with `ls -l`; explain any mismatch.)
2. In server.log: count lines that are ERROR, then lines that are
   neither INFO nor WARN (two greps; same answer? prove it).
3. Extract all unique IP addresses from server.log using grep -o (count
   them with sort/uniq — Lesson 3 preview: `grep -o ... | sort | uniq -c
   | sort -rn | head`). How many unique IPs?
4. Write ERE patterns that match in students.csv: (a) DS students, (b)
   emails ending `.edu`, (c) year 3 or 4. Verify counts against the
   dataset README's declared row count.
5. `grep -E "temp_c|s3" sensor-telemetry.tsv | head -3` — why does the
   header row match, and how would you exclude it cleanly?
6. (Stretch) find + grep: every .log file containing "refused" — output
   as `filename: count` per file (hint: grep -c and -exec together).

## Check yourself before Lesson 3

- [ ] I quote find globs and know -size/-mtime/-type.
- [ ] I can filter, count, invert, and extract tokens with grep.
- [ ] I write ERE (`-E`) by default and know why.
- [ ] I know regex matches lines, not grammars — awk comes next.

## Further reading (official sources)

- `man find`, `man grep` (GNU findutils/grep manuals:
  https://www.gnu.org/software/findutils/ , https://www.gnu.org/software/grep/)
- `man 7 regex` — POSIX ERE grammar
- plocate: https://plocate.sesse.net/
