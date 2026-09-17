# Module 10 Quiz — Answer Key

> Code questions graded on *reasoning*, not wording. Command answers:
> "would it work if typed".

## Section A — foundations

**A1.** The first line's `#!` tells the kernel *which interpreter*
executes the file when run as `./script.sh`. `/usr/bin/env bash`
finds bash on `PATH` — portable across systems where bash isn't at
`/bin/bash` (BSDs, containers, Nix).

**A2.** Bash parses `count = 5` as the **command** `count` with
arguments `=` and `5`. Assignments require no spaces around `=`
(`count=5`).

**A3.** Word splitting: `cp` receives **two** arguments `my` and
`report.csv` (plus `backup/`) — it tries to copy two nonexistent
files. Fix: quote the expansion — `cp "$name" backup/`.

**A4.** E.g. `echo "today: $(date +%F)"` → `today: 2026-09-15`, while
`echo 'today: $(date +%F)'` prints the literal — **double** quotes
expand `$(...)`; single quotes make everything literal.

**A5.** The line count as a string. With `<`, wc reads stdin so the
output is *only* the number (no filename padding) — cleaner to
capture and compare.

**A6.** (1) Explicit format string with `%s`/`%d` — no ambiguity
about how values render; (2) consistent, portable behavior (echo's
`-e`/`-n`/backslash handling varies), and no accidental newline
semantics.

## Section B — control flow

**B7.** `0`. `if` reads the command's **exit status**: 0 → then-
branch, non-zero → else/next elif.

**B8.** File tests: `-e` exists, `-f` regular file, `-d` directory
(also `-r/-w/-x` readable/writable/executable, `-s` non-empty).
Empty string: `[[ -z "$var" ]]` (non-empty: `-n`).

**B9.** (1) `[[ ]]` doesn't word-split or glob its contents —
unquoted-empty and globs behave; (2) it allows `&&`, `||`, and glob
pattern matching (`== *pattern*`) inside, without nested test
commands.

**B10.**
```bash
case "$ext" in
    csv) ... ;;
    tsv) ... ;;
    *)   ... ;;
esac
```

**B11.** The literal, unexpanded string `*.csv`. Handling:
`shopt -s nullglob` (glob expands to nothing → loop body never runs),
or the in-loop guard `[[ -f "$f" ]] || continue/exit`.

**B12.** `IFS=` prevents stripping leading/trailing whitespace from
the line; `-r` prevents backslash interpretation (`\n`, `\t` eaten).
The loop ends when `read` hits EOF and returns failure — `while`
consumes that failure.

## Section C — arguments, exit codes, strict mode

**C13.** `$0` = `./dq.sh`, `$1` = `a.csv`, `$#` = 2. Pass onward as
`"$@"` — quoted, boundaries preserved.

**C14.**
```bash
[[ $# -eq 1 ]] || { usage >&2; exit 64; }
```

**C15.** So pipelines/captures receive **only data** on stdout while
narration lands where logs/diagnostics live — `out=$(tool.sh)` stays
clean, `tool.sh 2>run.log` captures the story.

**C16.** `-e`: any failing command aborts the script (silent
continuation past errors becomes impossible). `-u`: using an unset
variable is an error (typo → crash at the typo, not empty-string
chaos). `-o pipefail`: pipeline status = rightmost non-zero (a broken
stage can no longer hide behind a successful last stage).

**C17.** (a) runs to completion — failures in `&&`/`||` chains are
*handled* by design, `-e` exempts them; (b) aborts — a bare failing
command outside a condition triggers `-e`; (c) runs to completion —
without pipefail the status is `wc`'s (0), masking `false`'s failure.
(The (b)/(c) contrast is the whole exam point.)

**C18.** 66 (EX_NOINPUT convention used in the course; any distinct
non-zero acceptable if documented). 0 tells every caller — `&&`
chains, cron, systemd, tests — that the work succeeded.

## Section D — functions, arrays, quality

**D19.** Scopes the variable to the function. Without it, the
variable is global — a helper's loop variable tramples the caller's
same-named variable ("works alone, corrupts the caller").

**D20.** Count: `echo "${#arr[@]}"`; second element:
`echo "${arr[1]}"`; iterate: `for x in "${arr[@]}"; do ...; done` —
quoted, so `"b c"` survives as one element.

**D21.** `((...))`'s exit status follows C semantics: expression
value 0 = *failure* status; `count--` evaluating to 0 therefore fails,
and `-e` aborts. Fixes: `(( count-- )) || true`, or restructure
(`for ((i=3; i>0; i--))`, or `count=$((count-1))` assignment form,
which has no test semantics).

**D22.** `bash -n`: parse-only syntax check (executes nothing) —
catches unbalanced quotes/if/fi. `bash -x`: trace mode — prints every
command after expansion, showing what actually ran. The rm-guard
class: **SC2115** (plus the `${var:?}` defense it recommends).

## Bonus (Q23) — model answer

The bug: `rm -v $filename` uses the variable **unquoted**, so bash
word-splits `my data.csv` into two arguments. Proof: the trace line
`+ rm -v my data.csv` shows the command bash *actually* ran —
post-expansion, two separate words where the source had one quoted
value.

## Score guide

| Score | Meaning |
|---|---|
| 20–23 | Ready for Mini-Project A |
| 15–19 | Reread the flagged lesson sections; redo the matching Lab 1 bug |
| < 15 | Repeat lessons 1–3 before the project — quoting and exit codes are load-bearing |
