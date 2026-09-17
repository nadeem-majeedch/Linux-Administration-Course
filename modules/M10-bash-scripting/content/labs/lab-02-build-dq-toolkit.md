# Lab 2 — Build `dq.sh`: From Pipeline to Tool

> Module 10 · Unit 3 · Difficulty: Intermediate
> Time: ~50 min · Environment: your own VM, `~/lab10/`
> Prerequisites: [Lab 1](lab-01-fix-the-bugs.md),
> [M09's pipeline](../../../M09-pipes-and-redirection/README.md),
> [M08's datasets](../../../M08-text-processing/content/README.md)
> ⚠️ Reads datasets, writes only `~/lab10/reports/`. No deletions at all.

You built one-off data-quality pipelines in M09. Now they graduate:
same logic, wrapped in the Lesson 3 skeleton, growing through five
stages — each stage *works* before the next begins. The result,
`dq.sh`, is the seed of [Mini-Project A](../mini-project-a-dataset-qc-toolkit.md).

## Setup

```console
$ mkdir -p ~/lab10/reports && cd ~/lab10
$ cp ~/datasets/sales_2026.csv .        # any CSV from M08's data works
$ head -3 sales_2026.csv
```

## Stage 1 — capture the pipeline (10 min)

Inside a script, reproduce a one-line quality summary — total rows,
duplicated rows, rows with any empty field (adapt to your dataset's
columns):

```bash
#!/usr/bin/env bash
# dq.sh — stage 1: pipeline captured
set -euo pipefail

file="$1"
total=$(tail -n +2 "$file" | wc -l)
dupes=$(tail -n +2 "$file" | cut -d, -f1 | sort | uniq -d | wc -l)

printf 'file: %s\nrows: %d\nduplicate ids: %d\n' "$file" "$total" "$dupes"
```

Run: `bash -n dq.sh && ./dq.sh sales_2026.csv`. Nothing new — M09
pipelines, captured. **That's the point:** a script is a named
pipeline before it's anything cleverer.

## Stage 2 — the contract (10 min)

Make Stage 1 fail *properly* per Lesson 3: usage function, argument
count check (exit 64), file-exists check (exit 66 via a `fail`
function), errors on stderr. Verify all paths with `echo $?`:

```console
$ ./dq.sh                    # → usage on stderr, exit 64
$ ./dq.sh nope.csv           # → error + exit 66
$ ./dq.sh sales_2026.csv     # → report + exit 0
```

## Stage 3 — log the steps (10 min)

Add the `log`/`fail` pair (Lesson 3 §6): `log "reading $file"`,
`log "found $dupes duplicate ids"`, `log "done"`. Then prove the
stdout/stderr split — the stage's real lesson:

```console
$ ./dq.sh sales_2026.csv > report.txt       # report.txt: data only
$ cat report.txt
$ ./dq.sh sales_2026.csv 2> run.log         # run.log: narration only
```

Data and narration on separate streams is what makes the tool
composable (`dq.sh f | sort`) *and* auditable (M24 greps the logs).

## Stage 4 — validate the data, not just the file (10 min)

Empty-file and header sanity — the Lesson 2 tests in a loop-free
check:

```bash
[[ -s "$file" ]] || fail "empty file: $file"
header=$(head -1 "$file")
[[ "$header" == *","* ]] || fail "no commas in header — is this CSV? got: $header"
```

Feed it an empty file and a text file; confirm both refusals. Then
the report's last line: `printf 'checked: %s\n' "$(date -Iseconds)"`.

## Stage 5 — shellcheck to zero (10 min)

```console
$ shellcheck dq.sh
```

Fix every finding — reading each code's wiki page, per Lesson 5's
workflow. Expect SC2086-adjacent findings if any quote slipped. When
silence: `bash -n dq.sh && ./dq.sh sales_2026.csv` one final time,
transcript to `lab-log.md`.

## The bar

| Requirement | Stage |
|---|---|
| Shebang + strict mode + header comment | 1 |
| Usage + argument + file guards, distinct exit codes | 2 |
| log/fail on stderr, data on stdout | 3 |
| Content validation (empty, header) | 4 |
| `shellcheck` + `bash -n` silent | 5 |

## Done when

- [ ] All five stages' transcripts in `lab-log.md`
- [ ] All four failure paths demonstrated (64, 66, empty, bad header)
- [ ] report.txt / run.log split demonstrated
- [ ] shellcheck: zero findings (paste the last clean run)
