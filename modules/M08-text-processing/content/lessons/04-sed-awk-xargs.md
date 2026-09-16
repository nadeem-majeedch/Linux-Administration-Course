# Lesson 4 — sed, awk, xargs & Command Substitution

> Module 08 · Unit 2 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: continues [Lab 3](../labs/lab-03-column-clinic.md)
> Prerequisites: [Lesson 3](03-columns-sort-uniq.md)

> 🔒 Safety: sed's `-i` **rewrites files in place, with no undo**. This
> lesson's rule: every sed `-i` is *rehearsed without `-i` first* (print
> the would-be result), and only then applied — and Lab 3 works on *copies*
> of the datasets. `sed -i.bak` is the cautious variant (keeps a backup).

---

## 1. sed: the stream editor

`sed` transforms text line-by-line. Its bread and butter is
**substitution** — `s/old/new/flags`:

```console
$ sed 's/widget/WIDGET/' transactions.csv | sed -n '2p'   # first match per line
TX1003,2019-01-01,emea,thingamajig,325.06     # (picked a non-widget line: unchanged)
$ sed 's/widget/WIDGET/g' transactions.csv | grep -c WIDGET   # g = global, all matches
267
```

Reading that: `s///` = substitute; `g` = every occurrence in the line,
not just the first; the delimiter can be any char — `s|a|b|g` when data
contains slashes (dates, URLs, paths).

**Ranges and addresses** — apply commands to selected lines only:

```console
$ sed -n '2,5p' students.csv               # -n + p: print lines 2–5 only (head -4 minus header)
$ sed '/^u003/d' students.csv              # delete matching lines (stream, not file)
$ sed -n '/ERROR/p' server.log | wc -l     # sed as grep (don't — but know it)
$ sed '2,4s/,DS/,DATA-SCI/' students.csv   # substitute only on lines 2–4
```

**Real data cleaning** — the students.csv dirt, fixed in one pass each:

```console
$ sed 's/ AT /@/' students.csv | grep u008        # repair the malformed email
u008,Hana Sato,hana.sato@uni.edu,DS,1,3.02,30
$ sed 's/Okafor /Okafor/' students.csv | grep u001   # trim the trailing space (verify!)
```

Careful: that second one *also* matches any other "Okafor " — in real
data you'd anchor: `sed 's/\(Okafor\) $/\1/'` (ERE with -E:
`s/(Okafor) $/\1/`). **Rehearsal rule in action:** run it without -i,
eyeball the diff, *then* apply.

**In-place (the powerful, dangerous mode):**

```console
$ cp students.csv students.csv.work        # lab discipline: work on copies
$ sed -i 's/ AT /@/' students.csv.work     # NOW in place — file rewritten
$ diff students.csv students.csv.work      # prove exactly what changed
2,3c2,3
```

`-i.bak` = in-place *with* automatic backup — the professional default
when touching anything you can't regenerate:

```console
$ sed -i.bak 's/thingamajig/thingumajig/g' transactions.csv.work
$ ls transactions.csv.work*                # .bak alongside — one command to roll back
```

---

## 2. awk: fields, records, and mini-programs

`awk` splits each line into fields (`$1, $2, …`, `$0` = whole line) and
runs a small program per record. `NF` = number of fields, `NR` = record
number, `$NF` = last field.

```console
$ awk '{print $3}' server.log | head -3    # field 3 of space-separated logs
ERROR
WARN
INFO
$ awk -F',' '{print $1, $6}' students.csv | head -3   # -F sets the delimiter
student_id gpa
u001 3.46
u002 3.21
```

**Selection with conditions** — awk is grep + cut + arithmetic:

```console
$ awk -F',' '$3 == "DS"' students.csv                     # all DS students
$ awk -F',' '$6 ~ /^[0-9.]+$/ && $6+0 >= 3.5 {print $2, $6}' students.csv
                                                          # honors: name + gpa
                                                          # (the regex guard skips u009's quoted GPA)
Grace Mensah 3.74
$ awk -F'\t' '$3+0 > 60 {print NR, $2, $3}' sensor-telemetry.tsv | head -3  # the spikes
3570 s3 65.6
3573 s3 65.6
```

That last one found the two declared +40 °C sensor spikes by *value* —
no regex, no reading 5,000 lines. Conditions plus columns is where awk
stops being a filter and becomes a **query engine**.

**Aggregation** — awk accumulates across records:

```console
$ awk -F',' 'NR > 1 && $6 ~ /^[0-9.]+$/ {sum += $6; n++} END {printf "mean GPA: %.4f\n", sum/n}' students.csv
mean GPA: 3.0433      # (9 clean rows; u009's quoted GPA excluded by the guard)
$ awk -F',' 'NR > 1 && $6 ~ /^[0-9.]+$/ {c[$4]++; gpys[$4] += $6} END {for (p in c) print c[p], p}' students.csv | sort -rn
5 DS
2 CS
1 STAT
1 PHYS
1 MATH
$ awk -F',' 'NR > 1 {s += $5} END {print "total revenue:", s}' transactions.csv
total revenue: 267496        # includes the -42.50 — flag it: s only if $5 >= 0
```

Line by line: `c[$4]++` counts occurrences per program (an associative
array — a hash built in two characters); `END` runs after the last
record. The census from Lesson 3, now without sort|uniq (and you get
arithmetic for free). Note `program` is gone from this census — `NR > 1`
guards the header, and the regex guard keeps u009's quoted GPA from
being summed as text.

**Computed columns / reformatting:**

```console
$ awk -F',' 'NR > 1 && $6 ~ /^[0-9.]+$/ {print $1, $6 * 25}' students.csv | head -3   # gpa × 25
u001 86.5
$ awk -F'\t' '{t += $3; n++} END {printf "mean temp: %.2f C\n", t/n}' sensor-telemetry.tsv
mean temp: 23.05 C     # (includes the two 65° spikes — discuss: threshold first?)
```

`printf` gives real formatting — worth knowing exists; details in `man awk`.

---

## 3. xargs: from lines to arguments

Pipes pass *data streams*; some tools need *argument lists*. xargs
converts:

```console
$ find . -name "*.log" | xargs wc -l       # wc on every find hit
  41 ./experiment.log
 500 ./access.log
 600 ./server.log
1141 total
$ grep -l "ERROR" *.log | xargs grep -c "refused"   # which of those logs, and how many
$ cut -d, -f1 students.csv | tail -n +2 | xargs -I{} echo "processing {}"
processing u001
processing u002
...
```

- `xargs` batches arguments (like find -exec ... +).
- `-I{}` substitutes per-line — one invocation per input.
- **Safety flag:** `xargs -d '\n'` treats whole lines as arguments
  (filenames with spaces survive); `xargs -r` (GNU) = *don't run on
  empty input* — always add it in scripts, or an empty find result runs
  `wc -l` on nothing and hangs on stdin.

---

## 4. Command substitution: the shell's own glue

`$(command)` runs a command and substitutes its output *as text* — the
difference between piping and embedding:

```console
$ echo "There are $(grep -c ERROR server.log) errors in the log"
There are 107 errors in the log
$ wc -l $(find . -name "*.csv")            # dynamic file list
$ echo "Largest log: $(du -b *.log | sort -rn | head -1 | cut -f2)"
Largest log: server.log
```

Versus backticks: `` `command` `` is the legacy syntax — same idea, but
doesn't nest. **Course rule: `$( )` always.**

Where it shines in data work — parameterized pipelines:

```console
$ ERRORS=$(grep -c ERROR server.log)
$ echo "error rate: $(( ERRORS * 100 / $(wc -l < server.log) ))%"
17%
```

That's a two-variable computation from raw files, no interpreter booted.
(M10 turns these into proper scripts with `set -euo pipefail`.)

---

## 5. The processing ladder: when to climb

| Need | Tool | Why |
|---|---|---|
| Filter lines | grep | fastest, simplest |
| Extract fixed columns | cut | trivial, single-char delimiter |
| Count/dedupe categories | sort + uniq | the census idiom |
| Conditional columns, math, last field | awk | fields + logic |
| Rewrite/normalize text | sed | substitutions, scripted edits |
| Lines → arguments | xargs | bridging streams to commands |
| Embed output in a command | `$( )` | shell-level glue |
| Anything relational, >3 columns of logic, joins | **pandas** (Lesson 6) | you've hit awk's ceiling |

---

## Exercises (lab-log.md)

1. sed rehearsal drill: on a *copy* of students.csv, fix u008's email
   with `-i.bak`, then `diff` original vs .bak vs work file. Three-way
   diff explained in one sentence each.
2. awk census: re-derive the program counts (§2) *without* sort/uniq.
   Then add a second array counting DS students with GPA ≥ 3.5 — one
   program, two aggregations.
3. Sensor clinic: find the mean temp *per sensor* with three awk runs
   (one per sensor id) — then in ONE awk program using an array keyed by
   `$2`. Report both results; they must agree.
4. xargs safety: run `find . -name "*.nonexistent" | xargs wc -l`
   (observe the hang — Ctrl-C), then with `-r`. Write the one-line
   lesson.
5. Command substitution: build `echo` sentences reporting (a) the number
   of 404s in access.log, (b) the busiest endpoint (Lesson 3's pipeline,
   embedded), (c) the date of the biggest transaction (sort -t, -k5 -nr
   embedded).
6. (Stretch) sed range edit: in experiment.log, change `status=FAIL` to
   `status=FAIL-RETRIED` only on lines containing `epoch=23`, using an
   address + substitution. Verify with grep.

## Check yourself before Lesson 5

- [ ] I rehearse every sed -i (no -i first, or .bak), and diff after.
- [ ] I can write an awk one-liner with a condition, an array, and END.
- [ ] I know xargs -r and why scripts need it.
- [ ] I reach for `$( )` naturally when a number must live inside a
      sentence/command.

## Further reading (official sources)

- `man sed` (GNU sed manual: https://www.gnu.org/software/sed/manual/)
- `man awk` / the One True awk vs gawk (https://www.gnu.org/software/gawk/manual/)
- `man xargs` (GNU findutils: https://www.gnu.org/software/findutils/)
