# Troubleshooting — Module 08

Symptom → cause → check → fix → prevention. The ten failure modes that
eat student afternoons.

## 1. Regex "matches here, not there"

- **Cause:** CRLF line endings (`\r\n`) — `$` anchors before `\r`, so
  patterns like `[0-9]$` fail on Windows-touched files.
- **Check:** `file f` (says "with CRLF"); `od -c f | head` shows `\r \n`.
- **Fix:** `sed -i 's/\r$//' f` or `tr -d '\r' < f > fixed`. (Generated
  course data is LF-clean; your *own* exports may not be.)
- **Prevention:** `file` any foreign CSV before regexing.

## 2. `sort` output looks wrong for numbers

- **Cause:** lexicographic sort — "10" < "9".
- **Check:** does your `sort` lack `-n`?
- **Fix:** `sort -n` (or `-h` for human sizes, `-V` for versions).
- **Prevention:** numeric column ⇒ `-n`, always.

## 3. `uniq -c` shows duplicates anyway

- **Cause:** input wasn't sorted — uniq only merges *adjacent* lines.
- **Check:** pipe `sort` before `uniq`.
- **Fix:** `sort f | uniq -c`.
- **Prevention:** the invariant: no uniq without sort (until proven).

## 4. `cut -d, -f5` returns empty on some rows

- **Cause:** those rows have fewer fields (ragged file) — or quoted
  fields shifted the count.
- **Check:** `awk -F',' '{print NF}' f | sort | uniq -c`.
- **Fix:** repair rows or switch to awk with NF guards.
- **Prevention:** field-count distribution is check #2 of recon (Lab 1).

## 5. `grep pattern file` — "No such file" inside a pipeline

- **Cause:** wrong cwd, or a `find` result with spaces split into
  pieces by xargs.
- **Check:** `pwd`; run the find alone.
- **Fix:** `xargs -d '\n'` (or `-0` with `find -print0`).
- **Prevention:** build pipelines stage by stage, not in one leap.

## 6. sed -i destroyed the file (or "which half-applied state is this?")

- **Cause:** untested in-place substitution, or a pattern that matched
  more lines than intended.
- **Check:** `.bak` present? (Course discipline says it always is.)
- **Fix:** `mv f.bak f` — then rehearse without `-i` this time.
- **Prevention:** the ritual: rehearse → `-i.bak` → `diff` → keep or
  restore. Work on `.work` copies in labs.

## 7. awk prints nothing for a CSV column

- **Cause:** default field separator is whitespace, not comma — `$5`
  doesn't exist (NF=1: whole line in $1).
- **Check:** `awk -F',' '{print NF}' f | head`.
- **Fix:** add `-F','` (or `-F'\t'`).
- **Prevention:** -F is part of *every* awk-on-CSV invocation; absence
  is the bug.

## 8. Locale noise: sort order "random" on special chars

- **Cause:** locale-aware collation (en_US.UTF-8 ignores punctuation
  differently than C).
- **Check:** `echo $LC_ALL`; compare `sort` vs `LC_ALL=C sort`.
- **Fix:** `LC_ALL=C sort` for byte-order determinism (scripts, logs).
- **Prevention:** scripts set `export LC_ALL=C` when sort order must be
  reproducible.

## 9. `xargs` hangs or runs with no input

- **Cause:** empty input → xargs runs the command anyway (waiting on
  stdin); or unquoted globs matched nothing.
- **Check:** feed it `echo -n | xargs wc -l` — it runs on *nothing*.
- **Fix:** `xargs -r` (GNU: no run on empty).
- **Prevention:** `-r` in every script's xargs; the mini-project
  enforces this.

## 10. Pipeline "works" but output is subtly wrong

- **Cause:** stage-order bugs — e.g., `tail -n +2` *after* sort (header
  sorted into the data), or uniq before sort.
- **Check:** run each stage alone; compare counts (`wc -l` between
  stages — the count should change only where you expect).
- **Fix:** re-order stages; re-verify with the census idiom on a known
  answer (our datasets have *declared* counts — use them as oracles).
- **Prevention:** build pipelines incrementally with `| head` between
  stages; the dataset READMEs' declared dirt is your unit test.
