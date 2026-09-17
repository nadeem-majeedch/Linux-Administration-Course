# Module 11 Troubleshooting — Automation Symptoms → Fixes

> Ten patterns for the failure modes automation introduces. Each:
> **symptom → cause → diagnosis → fix → prevention**. The M10 ladder
> (verbatim → `bash -n` → `bash -x` → `shellcheck`) still opens every
> investigation.

## 1. The dry-run showed a plan; the real run did something else

**Cause:** a modifying command bypassed the `run()` doorway.
**Diagnosis:** `grep -nE '\b(rm|mv|cp|mkdir|ln)\b' script.sh` — every
hit must be inside `run` or behind a guard. Compare dry-run narration
to a `bash -x` trace of the real run, line by line.
**Fix:** route the strays through `run()`.
**Prevention:** the audit habit (C5); one doorway, reviewed once.

## 2. Variables vanish after a loop (counts print 0)

**Cause:** the `cat | while` subshell swallow. **Diagnosis:** `bash
-x` shows increments happening... then the variable empty after
`done`. **Fix:** `done < file` redirection, or process substitution.
**Prevention:** the pipe form is banned in course scripts; Lesson 1
§4.

## 3. Temp files pile up in /tmp — script "mostly" cleans up

**Cause:** cleanup on the success path only, or the trap defined
after an early-exit point, or `mktemp` called but its result never
assigned. **Diagnosis:** interrupt at *several* different points
(early, middle, late); list `/tmp` deltas after each. **Fix:** one
`trap cleanup EXIT` defined immediately after `tmpdir=`, guarded
handler. **Prevention:** the Lesson 2 ordering: create temp → define
trap → work. Interrupt drills as a standing test.

## 4. Output file is a mixture of two runs

**Cause:** direct writes to the final path (`> "$target"`), so a
failure mid-run leaves partial content. **Diagnosis:** check the
script for `>` into the target; check timestamps — the file changed
despite rc≠0. **Fix:** write-temp-then-rename, temp on the *same*
filesystem as the target. **Prevention:** outputs are only ever
promoted, never written in place.

## 5. Re-running the script fails — `mkdir: File exists`, `ln: File exists`

**Cause:** non-idempotent commands doing their *job* on the second
run. **Diagnosis:** run twice; the first error names the offender.
**Fix:** the conversion table (Lesson 3 §3): `mkdir -p`, `ln -sfn`,
exists-guards, `mv -n`. **Prevention:** "second run is a no-op" as a
written acceptance test for every automation script.

## 6. Script hung overnight — no output, no error, 100% innocent-looking

**Cause:** an interactive `read` (no stdin in cron/pipeline), a
missing input file making it wait on something, or an `until`
loop whose condition never becomes true. **Diagnosis:** find the
process (M18: `ps -o pid,etime,wchan,cmd -p PID`); `bash -x` a
reproduction; check what it's waiting *on* (wchan, /proc/PID/fd).
**Fix:** arguments instead of prompts, `read -t` timeouts, loop
bounds (`for i in {1..30}` + sleep instead of bare `until`).
**Prevention:** Lesson 3's rule — anything scheduled never prompts;
bounded waits everywhere.

## 7. `getopts` prints bash's own error, then mine (or: options leak to the operand)

**Cause:** optstring without the leading `:` (noisy mode), or
forgetting `shift $((OPTIND - 1))` so `$1` is still `-n`.
**Diagnosis:** read the error's provenance — bash's `illegal option`
vs your handler's. **Fix:** silent mode + the shift line + explicit
`\?`/`:` arms. **Prevention:** copy the Lab 1 option block as a
unit; option parsing is boilerplate — reuse it identically.

## 8. mv across filesystems is slow — and briefly doubles disk usage

**Cause:** the atomicity assumption broken: temp on `/tmp`, target
on `$HOME` (different filesystems) — `mv` = copy+delete.
**Diagnosis:** `df` both paths — different devices? **Fix:** `mktemp
--tmpdir="$(dirname "$target")"`. **Prevention:** the same-
filesystem rule is a checkable property — audit for it (C5's list).

## 9. Cron runs it; it fails with "command not found" for a command you use daily

**Cause:** cron's PATH is minimal (`/usr/bin:/bin`); your
interactive PATH (M15) has extras (`~/.local/bin`, nvm python...).
**Diagnosis:** log `echo $PATH` from *inside* the cron run.
**Fix:** absolute paths for everything invoked; or set `PATH=` at
the script's top. **Prevention:** the "works from `env -i`"
standard: `env -i bash script.sh args` as a local test before
scheduling (M19 adopts this).

## 10. Two instances of the script ran at once — output corrupted or doubled

**Cause:** no single-instance guarantee — cron overlapped a slow
run with the next one. **Diagnosis:** timestamps in the log showing
overlapping runs; doubled lines in outputs.
**Fix:** a lock: `mkdir`-based lockdir (atomic create-or-fail) at
start, removed by the EXIT trap; or `flock`:
`exec 9>lockfile; flock -n 9 || { echo "already running" >&2; exit 1; }`.
**Prevention:** idempotency *plus* locking for anything scheduled;
M19's scheduling notes assume both.

## When to escalate

| Situation | Escalate to |
|---|---|
| Dry-run and real run disagree *after* the doorway audit | TA — subtle bash behavior, worth a conversation |
| Lock contention on a shared server | Whoever owns the schedule — coordination, not code |
| mktemp/trap pattern you can't make reliable | Reviewer with your interrupt traces |
| A script that must run against shared data and can't be made idempotent | Admin — batch jobs on shared data need owner sign-off |

> The property set (dry-run, idempotency, trap, quality gate) is
> what makes scripts *escalatable* — a reviewer can trust the
> envelope even when the middle is yours.
