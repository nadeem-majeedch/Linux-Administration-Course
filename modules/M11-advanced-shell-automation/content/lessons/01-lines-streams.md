# Lesson 1 — Lines, Streams and Field Splitting

> Module 11 · Unit 3 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 1 — harden dq.sh](../labs/lab-01-harden-dq-toolkit.md)
> Up next: [Lesson 2 — signals, temp files & cleanup](02-signals-temp-cleanup.md)

---

## 1. Why line-processing deserves a whole lesson

M10 introduced `while IFS= read -r` as an idiom. Automation work
promotes it to *the* tool for: merging datasets that arrive in
parallel files, reconciling two logs, streaming a 10 GB file you dare
not load into memory, and validating every line of an export. The
gap between "knows the idiom" and "can drive it" is exactly what this
lesson closes — IFS, field splitting, and the two-file patterns that
make bash surprisingly good data plumbing.

## 2. IFS — the field separator, demystified

**IFS** (Internal Field Separator) is the character set bash uses to
split *words* — in expansion, in `read`, in `for`. Default:
space, tab, newline.

```bash
line="alice,42,DS"
IFS=',' read -r name age program <<< "$line"
echo "name=$name age=$age program=$program"    # name=alice age=42 program=DS
```

Three forms you must be able to tell apart:

| Form | Meaning |
|---|---|
| `IFS=, read ...` | split fields on commas, **for this command only** |
| `IFS= read -r line` | split on *nothing* — the whole line, verbatim |
| `IFS=','` (bare assignment) | change the *shell's* splitting — affects everything after; **avoid outside temporaries** |

The `<<<` (here-string) feeds one string as stdin — the cleanest way
to test read-logic without files. The `IFS=, read -r a b c` prefix
pattern is *scoped* (comma-splitting dies with the command) — the
safe way to parse CSV-ish lines without corrupting the script's
global splitting behavior.

Trailing-empty gotcha, worth knowing before it costs an hour:
`IFS=, read -r a b c` on `"a,b,c,"` gives `c=","`'s leftover —
bash assigns the remainder *including separators* to the last
variable. CSV columns with trailing empties need care (count fields
first, or use M08's awk for true CSV work).

## 3. read's everyday flags

```bash
read -r line          # raw: no backslash mangling (always)
read -r a b rest      # split on IFS: first field→a, second→b, remainder→rest
IFS=$'\t' read -r id val rest   # TSV: tab-separated (ANSI-C quoting $'\t')
read -r -n 1 key      # single keystroke (interactive menus)
read -r -t 5 answer   # timeout: fails after 5s (unattended-safe, M10 §10's hang fix)
```

The `rest` catch-all is the professional touch in field splitting:
the last variable absorbs the remainder *with separators intact* —
so text fields containing the delimiter don't truncate.

## 4. Streaming a big file — the memory-free pattern

```bash
#!/usr/bin/env bash
# scan.sh — count error-ish rows without loading the file
set -euo pipefail

total=0; bad=0
while IFS= read -r line; do
    (( total++ )) || true
    case "$line" in
        *,,,|*", ,"*) (( bad++ )) || true ;;      # empty-ish fields
    esac
done < "$1"

printf 'scanned=%d suspicious=%d\n' "$total" "$bad"
```

The loop reads line-by-line — constant memory, no matter the file
size. Compare: `data=$(cat big.csv)` loads everything (and loses
trailing newlines). For *pure* counting/filtering, M08 tools win on
speed; the loop earns its place when the per-line action needs bash —
variables, decisions, calls to your functions.

Two hard-won notes: the `|| true` guards the `((...))` zero-eval
trap (M10 Lesson 4), and `done < file` beats `cat file | while
done` — the pipe form runs the loop in a **subshell**, silently
discarding every variable it sets.

## 5. Two files, one loop — the merge patterns

**Paste-merge** (row i of A with row i of B) — the
synchronization pattern for dataset shards:

```bash
while IFS=$'\t' read -r id_b val && IFS= read -r id_a; do
    ...
done < <(paste ids.txt values.txt)
```

Better: let M08 do the merging and bash the *deciding*:

```bash
join -t, -1 1 -2 1 teams.csv scores.csv | while IFS=, read -r team members score; do
    (( score >= 80 )) && echo "$team qualified ($score)"
done
```

**Correspondence by key** (match rows across files) — the
reconcile pattern, via process substitution:

```bash
# which IDs appear in yesterday's export but not today's?
comm -23 \
    <(cut -d, -f1 today.csv | tail -n +2 | sort) \
    <(cut -d, -f1 yesterday.csv | tail -n +2 | sort)
```

**Process substitution `<(command)`** runs a command and presents
its output as a *file path* — the bridge that lets two-file tools
(`comm`, `diff`, `join`) consume pipelines directly. It also enables
in-line diffing of what *is* vs what *should be*:

```bash
diff <(sort actual.txt) expected.txt && echo "match"
```

That one-liner is half of testing shell tools — [Lab 2's](../labs/lab-02-final-scripting-challenge.md)
self-tests lean on it.

## 6. Putting it together — reconcile.sh

```bash
#!/usr/bin/env bash
# reconcile.sh — report IDs present in today's export but missing
#                from yesterday's, and vice versa
set -euo pipefail

log() { printf '%s [recon] INFO  %s\n' "$(date -Iseconds)" "$*"; }

[[ $# -eq 2 ]] || { echo "usage: reconcile.sh TODAY YESTERDAY" >&2; exit 64; }
for f in "$1" "$2"; do
    [[ -f "$f" ]] || { echo "missing input: $f" >&2; exit 66; }
done

ids() { cut -d, -f1 "$1" | tail -n +2 | sort -u; }   # header stripped, sorted, unique

log "comparing $(basename "$1") vs $(basename "$2")"
new_only=$(comm -23 <(ids "$1") <(ids "$2") | wc -l)
gone=$(comm -13 <(ids "$1") <(ids "$2") | wc -l)

printf 'new: %d\ndisappeared: %d\n' "$new_only" "$gone"
```

Note the pieces doing their jobs: an `ids()` helper (M10 functions),
two process substitutions feeding `comm`'s two files, `wc -l`
captures, counts to stdout. It's the "did yesterday's data survive
today's pipeline?" check — a weekly chore, now a command.

## 7. Try it now (15 minutes)

1. Field-split drill: with `IFS=, read -r a b rest <<< "one,two,three,four"`
   — predict `a`, `b`, `rest` *exactly*, then verify. (rest =
   `three,four`.)
2. Stream `scan.sh` (§4) against an M08 dataset; then time both it
   and a pure-`grep -c` equivalent — write one sentence on when each
   wins.
3. Reconcile: create two small CSVs (one ID moved between them);
   run `reconcile.sh` both directions and confirm the counts
   cross-check (`new` of A-vs-B = `disappeared` of B-vs-A).
4. Subshell trap: run a `cat file | while read...` loop that counts
   into a variable; print the count after `done`. Mystery: it's 0.
   Rewrite with `done < file`. This bug is challenge C3's patient.

## 8. Common mistakes

- Unscoped IFS assignments — change splitting for the whole script.
  Prefix it to `read`, always.
- `cat file | while read` — the subshell steals your variables.
- `read` without `-r` (backslash mangling) — SC2162.
- Trusting CSV with `IFS=,` when fields contain commas — awk or a
  real CSV tool for those; document the assumption.
- Forgetting `|| true` on `((...))` under `set -e` — the zero
  evaluation abort.

> **Up next:** [Lesson 2 — signals, temp files &
> cleanup](02-signals-temp-cleanup.md): scripts that die *gracefully*
> — trap, mktemp, atomic writes.
