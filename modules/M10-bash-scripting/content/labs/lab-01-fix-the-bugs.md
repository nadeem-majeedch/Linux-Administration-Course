# Lab 1 — Fix the Bugs: Eight Classic Script Failures

> Module 10 · Unit 3 · Difficulty: Intermediate
> Time: ~50 min · Environment: your own VM, `~/lab10/`
> Prerequisites: [Lessons 1–5](../README.md) (especially 5's debugging ladder)
> ⚠️ One script (#6) contains a *guarded* `rm` — its lesson is that
> unguarded versions are dangerous. You'll fix it BEFORE it can delete
> anything, and the fix is the point.

Eight tiny scripts, each with one classic bug. For every one:

1. **Predict** what's wrong before running anything (write it down).
2. **Reproduce** — run it (safely: all files are in `~/lab10/scratch/`).
3. **Diagnose with tools** — `bash -n`, `bash -x`, `shellcheck`.
4. **Fix the cause.** 5. **Classify** — name the *class* of bug, so
   you recognize the next dozen instances.

Setup:

```console
$ mkdir -p ~/lab10/scratch && cd ~/lab10/scratch
$ printf 'a,b,c\n1,2,3\n4,5,6\n' > ok.csv
$ printf '' > empty.csv
$ printf 'x\ny\n' > "my file.csv"       # note: space in the name
```

## Bug 1 — the vanished variable

```bash
#!/usr/bin/env bash
# bug1.sh — should copy the CSV to a backup name
dataset = "my file.csv"
cp "$dataset" "$dataset.bak"
```

Symptom: `bug1.sh: line 3: dataset: command not found` — and then a
*second* surprise from `cp`. Fix, then classify. (Which rule from
Lesson 1 §3 does line 3 violate — and why did `cp` ALSO misbehave?)

## Bug 2 — word splitting in the wild

```bash
#!/usr/bin/env bash
# bug2.sh — count lines in every CSV
for f in $(ls *.csv); do
    echo "$f: $(wc -l < "$f")"
done
```

Runs... mostly. The space-named file breaks it *twice*. Diagnose with
`bash -x`, then fix — the course-approved loop-over-glob (Lesson 2
§6), not `$(ls)`. Classify: why is `$(ls)` in a for-loop doubly wrong?

## Bug 3 — the exit-code lie

```bash
#!/usr/bin/env bash
# bug3.sh — validate a file exists, then count rows
[[ -f "$1" ]]
echo "counting rows..."
wc -l < "$1"
echo "validation complete, all good!"
```

Run `./bug3.sh missing.csv`. The script *says everything is fine*.
What's the exit code, who believes that message, and what happens
when this pattern is scheduled under cron (M19's preview)? Fix with
the check-complain-exit guard (Lesson 3 §3), classify.

## Bug 4 — read without armor

```bash
#!/usr/bin/env bash
# bug4.sh — print every line of ok.csv numbered
n=0
while read line; do
    n=$((n+1))
    echo "$n: $line"
done < ok.csv
```

Looks right. Now feed it backslash-containing data:

```console
$ printf 'C:\\data\\2026\n' | ./bug4.sh      # line becomes stdin
```

What happened to the backslashes? Add the two missing tokens from
Lesson 2 §7 (`IFS=` and `-r`), re-run, classify. (This bug is silent
on clean CSVs — which is exactly why it survives in the wild.)

## Bug 5 — the arithmetic ambush

```bash
#!/usr/bin/env bash
# bug5.sh — countdown under strict mode
set -euo pipefail
count=3
while (( count > 0 )); do
    echo "T-minus $count"
    (( count-- ))
done
echo "liftoff"
```

It prints `T-minus 3`, then dies. Why does `(( count-- ))` — which
just evaluated to 3, then 2 — kill the script at `count=1`? Re-read
Lesson 4 §3's footnote, fix, classify. (SC2064 will happily explain.)

## Bug 6 — the rm that must never be careless

```bash
#!/usr/bin/env bash
# bug6.sh — clean a scratch directory passed as $1
set -u
target="$1"
rm -rf "$target"/*
```

**Before running anything:** with `set -u` only — NOT `set -u` inside
strict mode's protection of `-e`... think: what happens with
`./bug6.sh ""`? With `./bug6.sh " "`? With the variable name
misspelled at line 3? The class here is bigger than quoting: it's
*"a variable you assumed is non-empty reaching rm -rf."* Fix by
combining three guards — the `${var:?}` pattern (Lesson 5 §4), a
`[[ -d && -w ]]` check, and refusing paths that contain `..` or start
in `/` — then verify all three refusals fire. Classify: this is the
most important bug in the lab.

## Bug 7 — the swallowed status

```bash
#!/usr/bin/env bash
# bug7.sh — summarize a dataset via a function
set -euo pipefail
summarize() {
    local rows=$(wc -l < "$1")
    echo "rows: $rows"
}
summarize ok.csv
summarize missing.csv        # should fail loudly...
echo "still running!"        # ...but doesn't
```

Why did `summarize missing.csv` not stop the script despite `-e`?
(SC2155 knows.) Fix by splitting capture from declaration — `local
rows; rows=$(...)` — re-run, and note the *new* behavior: `-e` now
sees the failure. Classify.

## Bug 8 — the quoted substitution

```bash
#!/usr/bin/env bash
# bug8.sh — archive the CSV with a date-stamped name
set -euo pipefail
stamp='$(date +%F)'            # single quotes... on purpose?
cp ok.csv "ok_${stamp}.csv"
```

The filename will contain a literal `$(date +%F)`. Why? (Lesson 1 §4's
table knows.) Fix the quote *type*, not the command; then shellcheck
the whole file and classify.

## Wrap-up — the pattern census

Your `lab-log.md` closes with a table: bug # → class of bug → the
shellcheck code (if any) that names it. Two of the eight have no
shellcheck code — note which and why (they're *logic* bugs, not
syntax-class bugs: tools catch classes, understanding catches the
rest).

## Done when

- [ ] All eight fixed in place, `bash -n` + `shellcheck` clean
- [ ] Predictions written *before* each reproduction
- [ ] Classification table completed
- [ ] Bug 6's three guards each demonstrated refusing
