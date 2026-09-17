# Assignment 4 Key — The Survivor Script

> **INSTRUCTOR ONLY.** Student paper: [assignment-4-shell-automation.md](assignment-4-shell-automation.md).
> Marking guidance, common failure patterns, and a reference approach.
> Do not distribute.

## Reference approach (accept variants that meet the contract)

```bash
#!/usr/bin/env bash
set -euo pipefail

usage() { echo "usage: $0 <root-dir>" >&2; exit 1; }
[[ $# -eq 1 ]] || usage
ROOT="$1"
[[ -d $ROOT ]] || { echo "not a directory: $ROOT" >&2; exit 1; }
IN="$ROOT/incoming"; DATA="$ROOT/data"; QUAR="$ROOT/quarantine"
ARC="$ROOT/archive"; LOG="$ROOT/custodian.log"
mkdir -p "$DATA" "$QUAR" "$ARC"

MOVED=0; QUARANTINED=0; ARCHIVED=0

log() { printf '[%s] %s\n' "$(date -Is)" "$*" >> "$LOG"; }

# Phase 1 — intake: safe names, date prefix; non-CSVs listed, not moved
for f in "$IN"/*; do
  [[ -e $f ]] || continue                        # empty dir guard
  base=$(basename "$f")
  if [[ $base == *.csv ]]; then
    stem="${base%.csv}"
    stem=$(printf '%s' "$stem" | tr '[:upper:] ' '[:lower:]_')
    dest="$DATA/$(date +%F)-$stem.csv"
    if [[ -e $dest ]]; then                       # idempotency: same content → skip
      if cmp -s "$f" "$dest"; then log "skip duplicate-by-content: $base"
      else mv "$f" "$QUAR/"; QUARANTINED=$((QUARANTINED+1)); log "quarantined name-clash: $base"; fi
      continue
    fi
    mv "$f" "$dest"; MOVED=$((MOVED+1))
  else
    log "non-csv left in place: $base"
  fi
done
```

*(Phase 2: rebuild manifest to a temp file, `diff`/compare against the
old manifest per-file, quarantine mismatches; Phase 3: `find "$IN" -
maxdepth 1 -type f -empty -delete` — but shown as ls-verified in the
transcript per the rules; oldest-50 by `ls -t | tail`; Phase 4: the
summary line.)* The key is the **shape**: guards → phases as functions
→ counters → one log line. Sample-solution full text stays in the
instructor's private copy — this key documents the grading targets.

## Grading notes

- **Guards (4):** run the script bare → usage + exit 1. Run with a
  nonexistent dir → clean error. `set -euo pipefail` present *and
  load-bearing* (ask: which line did `-u` save?).
- **Intake (4):** the spaces-in-filename case is the discriminator —
  unquoted `"$IN"/*` handling breaks exactly here. Uppercase→lowercase
  + date prefix verified by listing `data/`.
- **Verification (4):** the manifest must *diff against the previous*
  manifest, not just be recreated. Quarantine (not delete) on hash
  change; a note line in the log.
- **Idempotency (3):** run 2 and 3 must show zero re-moves. The
  content-duplicate case (same bytes, new name) is handled *somehow*
  explicit — skip or quarantine-with-note, not silent overwrite.
- **Hostile survival (3):** empty incoming (`[[ -e $f ]] || continue`
  or nullglob), missing archive (mkdir -p), different cwd (the script
  must not care). Any one failing = cap 1/3 for this area.
- **Notes (2):** look for the *why* of quarantine-vs-delete (M19's
  verification mindset), and an honest breakage admission ("breaks if
  a filename contains a newline").

## Common failure patterns (past-cohort equivalents)

1. Unquoted glob variables — spaces case explodes (the classic)
2. Non-idempotent rename: date prefix re-applied on run 2
   (`2026-09-17-2026-09-17-x.csv`)
3. Manifest rebuilt without diffing — quarantine never triggers
4. `find -delete` on `incoming/` without the empty-file test — violates
   the deletion scope rule (hard deduction)
5. Log written with `>` (overwrites history) instead of `>>`
6. The cron bonus: relative `~/bin` path or unescaped `%` — the trap
   named but not handled

## Quick-marking transcript marks

✓ = ls-verified before the zero-byte delete; ▲ = end state ok, census
absent; ✗ = drift between run 1 and 2; ⚠ = any deletion outside the
sanctioned scope (cap the assignment at 10/20 and flag).

## Viva probes (if adoption includes a spot-check)

- "Your hash changed for a file — walk me through what your script did
  next, and why not delete it."
- "Which of your guards is load-bearing for cron? What does cron not
  have that your shell has?"
- "Run 3 equals run 1 — prove it from the log without re-running."
