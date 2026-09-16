# Lesson 5 — Data Science Pipelines: the Canonical Workflows

> Module 08 · Unit 2 · Difficulty: Intermediate
> Reading time: ~35 min · Labs: [Lab 2](../labs/lab-02-log-forensics.md),
> [Lab 3](../labs/lab-03-column-clinic.md)
> Prerequisites: Lessons 1–4 — this lesson *composes* them.

> All commands run from `modules/M08-text-processing/content/data/`.

---

## 1. The canonical pipeline

Every workflow in this lesson is a variation of one shape:

```text
file → grep → cut → sort → uniq → awk → output
```

Read as questions: *narrow to what matters* (grep) → *take the columns
that matter* (cut) → *group* (sort) → *aggregate* (uniq) → *compute*
(awk) → *capture* (redirect to a file, or wc for a headline number).
Learn the shape once; the rest of your career is swapping which stage
answers today's question.

---

## 2. Workflow A — log forensics (server.log)

**Question: "the API was slow yesterday afternoon — who and what?"**

```console
$ grep "WARN" server.log | cut -d' ' -f4 | sort | uniq -c | sort -rn | head -3
     24 worker-queue
     23 data-loader
     23 auth-service
$ grep "ERROR" server.log | grep "auth-service" | cut -d' ' -f1 | cut -d: -f1 | \
    sort | uniq -c
      3 2026-03-10
```

Stage by stage: filter to WARN → extract the *service* column → census →
rank. The second pipeline narrows errors to one service and extracts
just the date. Add hours (field 1's time portion):

```console
$ grep "ERROR" server.log | cut -d' ' -f2 | cut -d: -f1 | sort | uniq -c | sort -k2 -n
      8 00
      4 01
      8 02
      ...
```

Hourly error histogram — the thing you'd build a Grafana panel for,
already in four commands.

**Top offenders by message (the -o trick from Lesson 2):**

```console
$ grep -oE "took [0-9]+ms" server.log | awk '{print $2}' | sort -rn | head -3
8942ms
8103ms
7688ms
$ grep "slow query" server.log | grep -oE "[0-9]+ms" | sed 's/ms//' | \
    awk '{s+=$1; n++} END {printf "mean slow query: %.0f ms over %d queries\n", s/n, n}'
mean slow query: 5245 ms over 122 queries
```

The last one composes *four* lessons: grep → -o extraction → sed strip →
awk aggregation. Real mean latency, no spreadsheet.

---

## 3. Workflow B — web analytics (access.log)

**Question: "what's our traffic profile?"**

```console$ awk '{print $9}' access.log | sort | uniq -c | sort -rn    # status codes
    350 200
     61 404
     60 301
     29 500
$ awk '$9 == 404 {print $7}' access.log | sort | uniq -c | sort -rn | head -3
   12 /api/v1/queries
    9 /health
    9 /api/v1/reports/daily
```

Line two is the support-ticket answer: *which endpoints 404, ranked* —
awk selects rows **and** the column in one pass (no grep|cut needed once
you're in awk).

**Bandwidth by endpoint:**

```console
$ awk '{b[$7] += $10} END {for (e in b) printf "%8d  %s\n", b[e], e}' access.log | sort -rn | head -3
 1130360  /api/v1/reports/daily
 1123104  /api/v1/queries
  931376  /api/v1/datasets/upload
```

Arrays keyed by endpoint accumulating bytes — awk as a one-line
group-by-sum. (Every one of these maps 1:1 onto `df.groupby(...)`
— Lesson 6 makes the mapping explicit.)

---

## 4. Workflow C — transactions (CSV quality + business Qs)

**The data-quality sweep, in order of discovery:**

```console
$ tail -n +2 transactions.csv | wc -l                       # records: 1061
1061
$ tail -n +2 transactions.csv | sort | uniq -d | wc -l      # exact dupes: 4
4
$ awk -F',' 'NR > 1 && $5 < 0' transactions.csv             # negative amounts
TX240,2019-02-26,emea,widget,-42.50
$ awk -F',' 'NR > 1 {r[$3] += $5} END {for (k in r) printf "%-6s %10.2f\n", k, r[k]}' transactions.csv | sort -k2 -rn
latam    73848.14
amer     68053.30
apac     66522.74
emea     59071.43
```

Dupes, negatives, revenue per region — a three-line audit any reviewer
can re-run. **That re-runnability is the point:** the audit *is* the
documentation.

**The top-N drill:**

```console
$ awk -F',' 'NR > 1 {print $5, $1}' transactions.csv | sort -rn | head -3
2564.28 TX2419
1879.82 TX2671
1866.54 TX3242
```

Note the column *order swap* before sort — sorting by a column that
isn't first is two extra flags; sometimes restructuring is simpler.

---

## 5. Workflow D — sensors (TSV, gaps and spikes)

```console
$ awk -F'\t' 'NR > 1 {print $2}' sensor-telemetry.tsv | sort | uniq -c
   1800 s1
   1769 s2
   1800 s3
```

s2 is missing 31 samples — the declared outage, *discovered by census*
(s1 and s3 recorded all 1800). Bracket the gap:

```console
$ awk -F'\t' '$2 == "s2" && $1 >= "2026-03-10T12:11:00" && $1 <= "2026-03-10T12:12:00"' sensor-telemetry.tsv
2026-03-10T12:11:00	s2	20.7	45.6
2026-03-10T12:11:01	s2	20.9	47.1
...
```

(String comparison on ISO timestamps works — they're lexicographically
ordered. A freebie worth knowing. Most seconds in the window have *no*
s2 row at all — the outage is absent lines, which is why the census,
not eyeballing, finds it.)

**Spike detection by deviation:**

```console
$ awk -F'\t' '$2 == "s3" && $3+0 > 60 {print $1, $3}' sensor-telemetry.tsv
2026-03-10T12:20:00	65.6
2026-03-10T12:20:01	65.6
```

Two readings 40+ degrees over baseline — the sensor fault, found by
value. (Why `> 60` and not `> 25`? Because s3 *drifts through* 25–26
degrees normally — the threshold must clear the whole plausible range.
Threshold-setting is a modeling decision; statistical rigor is pandas'
department, Lesson 6.)

Two readings over a 25 °C threshold — the sensor fault, found by value.
*(Why not z-scores? You could — awk can do means first, pass two. But
threshold logic is usually the actual question; statistical rigor is
pandas' department, Lesson 6.)*

---

## 6. Workflow E — experiment logs (key=value streams)

ML training logs aren't CSV — they're `key=value` streams. awk handles
them by splitting on the same field machinery:

```console
$ grep "status=OK" experiment.log | awk '{for(i=1;i<=NF;i++) if ($i ~ /^accuracy=/) print $i}' | \
    cut -d= -f2 | sort -rn | head -3
0.8561
0.8537
0.8514
```

Extract → isolate the accuracy field → cut the value → rank. The
`for(i=1;i<=NF;i++)` scan handles key=value lines of *any* field order —
robust where a fixed `$7` would silently grab the wrong field after a
format tweak.

**Training curve summary:**

```console
$ awk '/^epoch=/ {acc=substr($3,10)+0; if (acc>best) {best=acc; ep=$1}} END {print ep, best}' experiment.log
epoch=38 0.8561
```

`substr` peels the `accuracy=` prefix; the running-max pattern is a
two-variable awk program — your first *stateful* one-liner.

---

## 7. The data-quality checklist (assembled)

From every workflow above, the standard pre-pandas audit for ANY
tabular file:

1. `file data.csv` — text? encoding sane?
2. `head -3 data.csv` — header? delimiter? quoted fields?
3. `wc -l data.csv` — scale check before loading
4. `awk -F',' 'NF != 7 {c++} END {print c+0}' data.csv` — ragged rows
   (wrong field counts)
5. `tail -n +2 data.csv | sort | uniq -d | wc -l` — exact duplicates
6. `awk -F',' 'NR>1 && $NF !~ /^[0-9.]+$/ {print NR}' data.csv | head` —
   non-numeric values in the numeric column
7. `sort | uniq -c | sort -rn` on categorical columns — unexpected
   category levels (the "MEM" vs "MEm" hunt)

Lab 1 runs this checklist against all six datasets; the mini-project
turns it into a tool.

---

## Exercises (lab-log.md)

1. Rebuild Workflow A's hourly error histogram *including a zero-line
   for hours with no errors* (hint: seq 0 23 | paste with the histogram
   — or accept the gap and explain why the graph would mislead).
2. Business Q: mean transaction amount *per product*, ranked. One
   pipeline; report the top product and its margin over second.
3. Sensor Q: which sensor has the highest humidity variance? (mean per
   sensor is two variables; variance is a second pass — threshold-based
   approximation is fine: max−min per sensor.)
4. Write the §7 checklist as 7 commands against students.csv — which
   rows fail check 6, and why is it *two* rows? (u008's ` AT ` email
   breaks the 7-field shape; u009's quoted comma GPA is non-numeric
   without its quotes — both live in your checks' crossfire.)
5. Compose your own pipeline answering a question *you* have about any
   dataset here. Constraint: at least four stages. Explain each stage in
   one line.
6. (Stretch) The `uniq -c | sort -rn | head` on endpoints hides
   long-tail. Compute: how many endpoints appear exactly once?

## Check yourself before Lesson 6

- [ ] I can assemble the canonical pipeline without notes for a new
      question on a known file.
- [ ] I've used awk arrays as group-by at least three times.
- [ ] I know where shell *ends* (joins, regressions, plots) — and am
      ready to argue both sides of "why not just pandas?"

## Further reading (official sources)

- GNU coreutils + grep + gawk manuals (linked per lesson)
- *Data Science at the Command Line* (Janssens, O'Reilly — command-line
  DS pipeline design; uses the same toolbox): https://datascienceatthecommandline.com/
