# Lab 1 — Organizing Datasets Safely

> Lessons 1, 3 · Time: ~50 min · Risk: LOW — destructive commands practiced on a
> **sacrificial tree** you build for this lab; every destructive step is preceded
> by its echo-check

## Goal

Run the full copy → move → glob → delete workflow on a fake-but-realistic dataset
dump, using the pwd/ls/rm ritual until it's muscle memory. Everything disposable;
nothing real at stake; every habit transferable to real data.

## Part 1 — Build the sacrificial dump (10 min)

```console
$ mkdir -p ~/scratch/dump-2026-09/{raw,processed,logs}
$ cd ~/scratch/dump-2026-09
$ touch raw/sales-{mon,tue,wed,thu,fri}.csv raw/README.md
$ touch raw/customers.csv raw/returns.csv
$ touch raw/sensor-01.tmp raw/sensor-02.tmp raw/sensor-03.tmp
$ touch logs/app-{2026-09-01,2026-09-02,2026-09-03}.log logs/app-current.log
$ ls -l raw logs
```

Record the `ls` output — this is your **baseline**; the lab's deletions are graded
against it (what *should* remain at the end: README.md, customers.csv, returns.csv,
5 weekday CSVs, 3 dated logs, app-current.log).

## Part 2 — Copy with intent (10 min)

```console
$ cp raw/sales-mon.csv raw/sales-mon.original.csv
$ cp -r raw raw-snapshot          # directory copy needs -r
$ ls raw-snapshot
```

Checkpoint: does `raw-snapshot` contain the `.original` file too? Why? (Copy is a
moment-in-time duplicate — including the duplicate.)

Restore-scenario drill: delete the copy of one original's *contents* is not
available (files are empty) — instead simulate recovery: `rm` (with `-i`) the
`sales-mon.csv` from `raw/`, then restore it from `raw-snapshot/`:

```console
$ rm -i raw/sales-mon.csv
$ cp raw-snapshot/sales-mon.csv raw/
```

One log line: what role did the snapshot play that a recycle bin would normally?

## Part 3 — Move & rename with globs (10 min)

Predict **on paper**, echo-check, then execute:

```console
$ echo mv raw/sales-*.csv processed/
$ mv raw/sales-*.csv processed/
$ echo mv raw/sensor-0*.tmp logs/
$ mv raw/sensor-0*.tmp logs/
$ ls processed logs
```

Surprise check: did `sales-mon.original.csv` also move? (Glob `sales-*` matched
it!) Fix the pattern thought: re-glob precisely
(`echo mv raw/sales-mon.original.csv raw/` → execute) or note that
`sales-[a-z]*.csv` vs `sales-mon.original.csv` distinction matters. Write the
lesson: **globs match what they match, not what you meant.**

## Part 4 — The deletion ritual (15 min)

Target: every `.tmp` in `logs/`. Perform the full professional form:

```console
$ pwd                              # where am I?
$ ls logs/*.tmp                    # see the exact targets
$ echo rm logs/sensor-0*.tmp       # dry-run the expansion
$ rm -i logs/sensor-0*.tmp         # interactive first pass: answer y 3×
$ ls logs/                         # verify what remains
```

Then, earned-confidence pass on a *directory*:

```console
$ ls raw-snapshot/                 # the whole snapshot tree, verified
$ rm -r raw-snapshot
$ ls
```

(No `-f`: `-r` alone still prompts for write-protected files — today you *want*
the guardrails.)

Final state check against the baseline:

```console
$ ls raw processed logs
```

Log the deltas: what's gone, what survived — and confirm `app-current.log` and
`README.md` survived *because the globs were precise*.

## Part 5 — The accident rehearsal (5 min, eyes only)

Read this command and **write** what it would do before ever running it:

```console
rm -rf raw/[st]*
```

(Then *verify your prediction* with `echo rm -rf raw/[st]*` — do NOT run the
rm. If your prediction and echo disagree, write why. That gap is exactly what
the echo ritual is for.)

## Wrap-up checklist

- [ ] Baseline and final-state `ls` outputs both recorded; deltas explained
- [ ] The glob-surprise (`sales-mon.original.csv`) caught, explained, fixed
- [ ] Every destructive command preceded by pwd/ls/echo in the log
- [ ] Part 5 prediction written *before* its echo verification
- [ ] `~/scratch/dump-2026-09` left in the expected end state (or deleted as a
      final echo-checked `rm -r` — your choice, logged)
