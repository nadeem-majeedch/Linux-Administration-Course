# Lab 1 — Data-Quality Recon (Read-Only)

> Module 08 · Unit 2 · Difficulty: Beginner-Intermediate
> Time: ~40 min · **Zero writes**: nothing is modified, created, or moved.
> Prerequisites: [Lesson 1](../lessons/01-viewing-counting.md), [Lesson 2](../lessons/02-finding-files-and-text.md)

You're handed six unfamiliar datasets. Before any analysis (or any
pandas), run standard recon — and document findings like an analyst, not
a tourist.

## 0. Setup

```console
$ cd modules/M08-text-processing/content/data   # (or copy them to ~/lab08/)
$ ls -lh                                        # sizes at a glance
$ echo "=== LAB8 RECON $(date +%F) ===" >> ~/lab-log.md
```

## Part A — identity & scale (Lesson 1 kit)

For **each** of the six files:

```console
$ file FILE; wc -l FILE; head -3 FILE
```

**Record** in a table: name, format (per `file`), lines, header yes/no,
delimiter (tab/comma/space), one sentence on what the data *is*. Six
rows — this table is the foundation of every later lab.

## Part B — schema & shape

```console
$ head -1 transactions.csv
$ awk -F',' 'NF != 5 {print NR": "$0}' transactions.csv | head   # ragged rows?
$ awk -F'\t' '{print NF}' sensor-telemetry.tsv | sort | uniq -c  # field-count distribution
```

**Record:** do all rows of each structured file have the declared field
count (5 for transactions, 4 for sensor)? Any exception is a finding —
ours: does the *header* itself count? Note where NR=1 changes answers.

## Part C — category inventories (Lessons 2–3 kit)

```console
$ cut -d, -f3 students.csv | sort | uniq -c | sort -rn        # programs
$ cut -d, -f4 transactions.csv | sort | uniq -c | sort -rn    # products
$ awk '{print $3}' server.log | sort | uniq -c | sort -rn     # log levels
$ awk '{print $9}' access.log | sort | uniq -c | sort -rn     # HTTP statuses
$ awk -F'\t' 'NR>1 {print $2}' sensor-telemetry.tsv | sort | uniq -c  # sensors
```

**Record:** each census + one anomaly-hunting sentence. Expected
declared dirt: u009's comma GPA will *not* appear in clean GPA stats —
did your program census show it anyway? Where would it hide?

## Part D — the dirt hunt (declared, but *prove it*)

From the [dataset README](../data/README.md): 4 duplicate transactions,
1 negative amount, 1 malformed email, 1 comma-decimal GPA (quoted), 31 missing
sensor rows, 2 temperature spikes, 1 FAIL epoch.

Write **one pipeline per claim** that demonstrates it:

```console
$ tail -n +2 transactions.csv | sort | uniq -d                 # the dupes
$ awk -F',' '$5 < 0' transactions.csv                          # the negative
$ grep " AT " students.csv                                     # the email
$ grep -E "gpa|," students.csv | awk -F',' '$6 ~ /,/'          # comma GPA
$ awk -F'\t' 'NR>1 {c[$2]++} END {for (s in c) print s, c[s]}' sensor-telemetry.tsv  # the gap
$ awk -F'\t' '$3+0 > 60 {print}' sensor-telemetry.tsv          # the spikes (60 clears normal range)
$ grep "FAIL" experiment.log                                   # the failure
```

**Record:** each command + its output + verdict (claim confirmed /
partially / not found). *Not found is a valid finding* — say so and
show the check that would have caught it.

## Part E — the recon report (deliverable)

One page: the Part A table, the three most interesting Part D findings,
and a **go/no-go recommendation per dataset** for direct `pd.read_csv`
(`go` = clean enough to load; `no-go` = needs cleaning first, list
which). This is exactly the artifact a senior analyst writes before
touching data — you're writing it in hour one of the module.

## Done when

- [ ] Part A table complete (6 rows)
- [ ] Field-count distributions recorded (Part B)
- [ ] All five censuses + anomaly sentences (Part C)
- [ ] All seven dirt claims tested with pipelines + verdicts (Part D)
- [ ] Recon report written with go/no-go per dataset
