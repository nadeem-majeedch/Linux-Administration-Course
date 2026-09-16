# Lab 3 — The Column Clinic: Cleaning & Shaping Tabular Data

> Module 08 · Unit 2 · Difficulty: Intermediate
> Time: ~45 min · **Copies only**: `cp file file.work` before any
> in-place edit (Lesson 4's rule)
> Prerequisites: [Lesson 3](../lessons/03-columns-sort-uniq.md), [Lesson 4](../lessons/04-sed-awk-xargs.md)

Three patients: `transactions.csv` (dupes + negative), `students.csv`
(dirty emails/GPAs), `sensor-telemetry.tsv` (gap + spikes). Diagnose,
clean, and *prove* each fix — the proof is the deliverable.

## Patient 1 — transactions.csv

```console
$ cp transactions.csv transactions.csv.work
$ tail -n +2 transactions.csv.work | sort | uniq -d               # diagnosis: dupes
$ awk -F',' 'NR>1 && $5 < 0' transactions.csv.work                # diagnosis: negative
```

**Fix + prove:**

```console
$ awk -F',' '!seen[$0]++ || NR==1' transactions.csv.work > transactions.csv.dedup  # order-preserving dedupe
$ tail -n +2 transactions.csv.work | wc -l                        # before: 1061
$ tail -n +2 transactions.csv.dedup | wc -l                       # after: 1057
$ tail -n +2 transactions.csv.dedup | sort | uniq -d | wc -l      # proof: 0 dupes remain
$ awk -F',' 'NR>1 && $5 < 0' transactions.csv.dedup               # the negative: FLAG, don't delete
```

**Record:** the dedupe pipeline explained stage by stage (why
`!seen[$0]++` dedupes — one sentence on the awk idiom), and why the
negative amount is *flagged for review* rather than silently removed
(one sentence: what business process might a negative be?)

## Patient 2 — students.csv

```console
$ cp students.csv students.csv.work
$ grep -nE ' AT |"[0-9]+,[0-9]+"' students.csv.work    # find the dirt (quoted GPA + bad email)
```

Two fixes, each rehearsed then applied (sed -i.bak discipline):

```console
$ sed 's/ AT /@/' students.csv.work                # REHEARSE: stdout only
$ sed -i.bak 's/ AT /@/' students.csv.work         # apply with backup
$ diff students.csv.work.bak students.csv.work     # prove: one line changed
$ sed 's/"\([0-9]*\),\([0-9]*\)"/\1.\2/' students.csv.work   # REHEARSE: u009's GPA
$ sed -i.bak 's/"\([0-9]*\),\([0-9]*\)"/\1.\2/' students.csv.work
$ grep '^u009' students.csv.work                   # proof: 3,77 → 3.77, quotes gone
```

Notice the GPA fix anchors on the *quotes* — the quoted field is exactly
where "a comma is data, not a delimiter". **Record:** one sentence on
why the quotes make this fix safe (what would `s/,/./` on the whole
line have done?), and what the pandas version
(`pd.read_csv` handles quoted fields natively + `str.replace`) would
look like. Then the awk-side check that the file is now fully numeric
in column 6:

```console
$ awk -F',' 'NR>1 && $6 !~ /^[0-9.]+$/ {print NR, $6}' students.csv.work
```

## Patient 3 — sensor-telemetry.tsv

```console
$ cp sensor-telemetry.tsv sensor-telemetry.tsv.work
$ awk -F'\t' 'NR>1 {c[$2]++} END {for (s in c) print s, c[s]}' sensor-telemetry.tsv.work
$ awk -F'\t' '$2=="s2" && $1 >= "2026-03-10T12:11:00" && $1 <= "2026-03-10T12:12:10"' \
    sensor-telemetry.tsv.work                        # bracket the outage window
```

**Decision, not deletion:** the few s2 rows that *do* exist inside the
outage window (the outage drops ~95% of readings, not all) are real
readings — keep them; the gap is *documented*, not filled. **Record**
that choice and its one-sentence rationale (imputing sensor data is a
modeling decision, not a cleaning decision).

The spikes, by contrast, are *implausible values* (65+ °C vs a ~23–26
range): flag them:

```console
$ awk -F'\t' '$3+0 > 60 {print NR, $0}' sensor-telemetry.tsv.work
```

**Record:** the two spike rows and the "keep-but-flag" pattern you'd
hand pandas (`mask`/`clip`) — one sentence why shell *flags* and pandas
*imputes*.

## Wrap-up — the clinic report

For each patient: diagnosis pipeline → fix pipeline → proof pipeline →
one-sentence judgment (cleaned / flagged / documented). Three patients,
twelve lines, done.

## Done when

- [ ] All three `.work` copies exist with `.bak` backups alongside
- [ ] Dupes: before/after counts + zero-dupes proof
- [ ] Email + GPA fixes: rehearsed, applied, diffed, proven
- [ ] Sensor gap documented (not filled); spikes flagged (not deleted)
- [ ] Clinic report written with the keep/flag/fill judgments explicit
