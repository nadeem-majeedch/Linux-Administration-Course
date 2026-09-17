# Lesson 4 — Functions, Arrays and Arithmetic

> Module 10 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Up next: [Lesson 5 — debugging & quality](05-debugging-quality.md)

---

## 1. Functions — named actions

A function is a **named block of commands**, defined once, called
many times — the difference between a script that grows into a wall
and one that reads like an outline:

```bash
#!/usr/bin/env bash
set -euo pipefail

log() {
    printf '%s [dq] INFO  %s\n' "$(date -Iseconds)" "$*"
}

summarize_file() {
    local file="$1"                        # local: won't leak out
    local rows
    rows=$(wc -l < "$file")
    printf '%-28s %5d rows\n' "$file" "$rows"
}

log "starting"
for f in *.csv; do
    summarize_file "$f"
done
```

Mechanics that matter:

- **Definition** `name() { ... }` must precede the first call — bash
  reads top-to-bottom.
- **Arguments** arrive as positional parameters *inside* the
  function: `$1` is the function's first argument, not the script's.
- **`local`** scopes a variable to the function. Without it, the
  variable is *global* — a loop variable `file` leaking out of a
  helper is the classic "works alone, corrupts the caller" bug. Use
  `local` for every function variable (except deliberate returns).
- **Return status:** `return 0..255` (or the last command's status).
  `return` ends the function; `exit` ends the script. Data comes back
  by **stdout** (`rows=$(summarize "$f")` captures it) — the shell's
  division of labor: *status* for success/failure, *stdout* for data.
- **Scope note:** a function can call your real commands, other
  functions, and even *override* a command for its scope — which is
  how the testing trick in [Mini-Project A](../mini-project-a-dataset-qc-toolkit.md)
  works (stub out `scp` to test the paths around it without
  transferring anything).

The `rows=$(...)` then `printf` split above also demonstrates the
two-variable dance: capture first, print second — clearer than
nesting substitutions inside printf.

## 2. Arrays — lists of things

Bash variables can hold **lists**:

```bash
readonly DATASETS=(train.csv validation.csv test.csv)
readonly CLEANERS=(dedupe.sh normalize.sh report.sh)

echo "${DATASETS[0]}"          # first element — braces REQUIRED
echo "${DATASETS[@]}"          # all elements, as separate words
echo "${#DATASETS[@]}"         # element count
```

Iterate like any list:

```bash
for ds in "${DATASETS[@]}"; do
    [[ -f "$ds" ]] || { echo "missing dataset: $ds" >&2; exit 1; }
done
```

The quoting rule compounds here: `"${DATASETS[@]}"` (quoted) keeps
each element whole even if it contains spaces; unquoted `${DATASETS[@]}`
re-splits everything. `"${...[@]}"` is the form to build reflexes on.

Growing and slicing:

```bash
files=()                       # empty array
for f in *.csv; do files+=("$f"); done    # append
echo "collected ${#files[@]} files"

printf '%s\n' "${files[@]:0:3}"           # first three elements
```

**When to reach for arrays:** configuration lists (the datasets this
pipeline touches), collected results (files that failed validation),
argument queues. When *not*: parallel numeric series usually want
files on disk or `paste`/M08 tools, not array gymnastics.

## 3. Arithmetic — (( )) and $(( ))

```bash
count=3
count=$((count + 1))           # arithmetic expansion → assignment
echo "$count"                  # 4

if (( count >= 4 )); then echo "quota met"; fi     # condition form

epoch=1
while (( epoch <= 5 )); do
    echo "epoch $epoch"
    (( epoch++ )) || true      # see the footnote below!
done
```

Operators: `+ - * / %` (integer only — no decimals; for percentages,
use `awk` from M08: `awk "BEGIN {printf \"%.1f\", $rows*100/$total}"`).
Division truncates: `7/2` is `3`.

**The `((...))` exit-status footnote** (a genuine bash oddity): an
arithmetic expression evaluating to **0** has *failure* status (it's
"false" like in C). Under `set -e`, a decrement to 0 — `((count--))`
when count was 1 — aborts your script. Hence `(( epoch++ )) || true`
when the expression can hit zero. Shellcheck flags this one for you —
Lesson 5 shows it in action.

## 4. File tests at scale — the validation function

Lesson 2's tests, wrapped as a reusable function — the shape most
Mini-Project A scripts use:

```bash
require_readable() {
    local path="$1"
    if [[ ! -f "$path" ]]; then
        echo "not a file: $path" >&2; return 66
    fi
    if [[ ! -r "$path" ]]; then
        echo "not readable: $path" >&2; return 66
    fi
    return 0
}

# usage — status flows to the caller:
for ds in "${DATASETS[@]}"; do
    require_readable "$ds" || { echo "aborting: $ds" >&2; exit 66; }
done
```

Return codes as *error classes* (66 = input problem) let the caller
decide: retry, skip, or abort.

## 5. String operations — the everyday toolkit

Not tests — *transformations*, all prefix-based, no external tools:

```bash
name="report_final.csv"
echo "${#name}"                 # 16 — length
echo "${name%.csv}"             # report_final      (strip shortest suffix)
echo "${name%.csv}.tsv"         # report_final.tsv  (extension swap)
echo "${name#report_}"          # final.csv         (strip shortest prefix)
echo "${name^^}"                # REPORT_FINAL.CSV  (uppercase)
echo "${name//_/-}"             # report-final.csv  (replace all _ with -)
```

The suffix-strip `${var%.ext}` is the rename-to-new-extension idiom
that powers batch converters; `${var:-default}` (Lesson 1) and its
sibling `${var:=default}` (assign *and* use) round out the family.

## 6. Putting it together — organize_datasets.sh

Every lesson-4 element in one realistic automation:

```bash
#!/usr/bin/env bash
# organize_datasets.sh — sort CSVs into by-kind/ subdirectories
set -euo pipefail

log() { printf '%s [org] INFO  %s\n' "$(date -Iseconds)" "$*"; }

TARGETS=(raw processed archive)             # array: the kinds we know

for f in *.csv; do
    [[ -f "$f" ]] || { echo "no CSVs found" >&2; exit 66; }

    case "$f" in                            # decide the kind
        raw_**)      kind="raw" ;;
        processed_*) kind="processed" ;;
        archive_**)  kind="archive" ;;
        *)           kind="raw" ;;          # default bucket
    esac

    if [[ ! -d "$kind" ]]; then
        mkdir -p "$kind"                    # -d guard: idempotent-ish (M11 deepens)
        log "created directory $kind"
    fi

    dest="${kind}/${f#*_}"                  # strip the kind_ prefix
    mv -n -- "$f" "$dest"                   # -n: never overwrite; --: end of options
    log "moved $f -> $dest"
done

log "organized ${#TARGETS[@]} known kinds; done"
```

Nothing here is new — arrays, case, functions, `${var#...}`, `mv -n`
(the no-clobber flag; clobbering a dataset is not recoverable) — but
assembled, it's the "organize my dataset dumps" chore, automated in
25 honest lines.

## 7. Try it now (15 minutes)

1. Build `organize_datasets.sh`; create
   `raw_sales.csv`, `processed_sales.csv`, `random.csv` in `~/lab10`
   and run it. Then run it *again* — the `-d` guard makes re-runs
   safe. (Sneak preview of M11's idempotency.)
2. Write `epochsim.sh`: simulate 5 "epochs" with `(( ))`, printing a
   fake loss per epoch; then make it crash by decrementing to 0 —
   and fix it with `|| true`.
3. Arrays: build `missing.sh` over the DATASETS pattern — given three
   filenames, exits 66 naming the first missing one, 0 if all exist.
4. String ops drill: in one line, turn
   `2026-09-15_experiment_final.csv` into `experiment_final.tsv`.

## 8. Common mistakes

- Forgetting `local` — helpers trample the caller's variables.
- `${arr[0]}` without braces, or unquoted `"${arr[@]}"`.
- `(( x = 3 ))` inside `if` without knowing 0 = false.
- Decimal arithmetic in `(( ))` — silently truncates; use awk.
- `mv` without `-n`/`--` in scripts — overwrites and dash-prefixed
  filenames are both real hazards.

> **Up next:** [Lesson 5 — debugging & quality](05-debugging-quality.md):
> `bash -x`, `bash -n`, and the shellcheck workflow that turns script
> debugging from séance into science.
