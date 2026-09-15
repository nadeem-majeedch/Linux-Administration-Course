# Lab 2 — Pipeline Workshop

> Lesson 2 · Time: ~50 min · Risk: zero

## Goal

Answer eight analytical questions with pipelines only — no editors, no Python.
Then bank the best ones as aliases and history. This is the "shell as analytics
engine" experience in miniature.

## Part 0 — Corpus (5 min)

```console
$ mkdir -p ~/scratch/m09b && cd ~/scratch/m09b
$ printf 'order,customer,region,amount\n1001,ada,north,250\n1002,ben,south,90\n1003,ada,north,310\n1004,chen,west,45\n1005,ben,south,700\n1006,ada,east,120\n' > sales.csv
$ printf '%s\n' INFO-start ERROR-db WARN-slow INFO-stop ERROR-api DEBUG-x ERROR-timeout > app.log
```

## Part 1 — The eight questions (30 min)

Write each as **one pipeline**; log command + output:

1. Row count excluding the header.
2. Distinct customers, alphabetically.
3. Orders per customer, biggest first. (*the counting idiom*)
4. Top spender row(s) by amount — numeric sort matters; show the wrong sort
   first, then the right one.
5. Customer totals idea-test: can `cut`+`sort`+`uniq -c` compute the *sum* per
   customer? Attempt it honestly; log why it can't (collapse ≠ aggregate) —
   this is exactly the wall M08's awk will demolish.
6. ERROR lines only, timestamps aside — count them.
7. All lines *except* DEBUG, saved to `kept.log` **and** displayed, in one
   command (`tee`).
8. Every distinct log *level* (the 2nd field) with counts.

## Part 2 — Bank your work (10 min)

```console
$ alias orders='tail -n +2 sales.csv | cut -d, -f2 | sort | uniq -c | sort -rn'
$ orders
$ alias errors='grep ERROR app.log | wc -l'
$ errors
```

Then history: press **Ctrl+R**, type `sort -rn`, re-run your best pipeline.
Record: which alias earns a permanent place in `~/.bashrc` (M15 makes it
persistent), and which is a once-only pipeline not worth naming — and your
criterion for telling them apart.

## Part 3 — Chain discipline (5 min)

```console
$ mkdir -p out && cp sales.csv out/ && echo DONE
$ cp missing.csv out/ && echo DONE        # read carefully: what prints?
$ cp missing.csv out/ ; echo DONE         # and now?
```

Log the three outcomes; one line on which chaining operator belongs in a
pipeline *script* and why.

## Wrap-up checklist

- [ ] Eight questions: pipeline + output logged each
- [ ] Q5's wall articulated (uniq counts ≠ sums)
- [ ] Two aliases defined and used; one judged not-worthy, with criterion
- [ ] Chain-triangle outcomes explained
- [ ] Zero commands typed blind: every destructive-capable step was pure read
