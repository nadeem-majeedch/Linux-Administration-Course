# Unit 3 Lecture Slides — Scripting & Automation (M10–M11)

> **Delivery:** Sessions 9–10 · Speaker notes:
> [../speaker-notes/unit-03-scripting-notes.md](../speaker-notes/unit-03-scripting-notes.md)

---

# Slide 1 — Title

## Slide Content
**Unit 3 — Shell Scripting & Automation**
From one-liners to scripts that run tired at 2 a.m. (M10–M11)

## Instructor Delivery Notes
Framing: "Last week you wrote pipelines. This week they learn to
*survive without you*."

## Visual or Demonstration Suggestion
A pipeline on screen, morphing into a script file.

## Student Question
"What's the difference between a command you type and a command you automate?"

---

# Slide 2 — Your first script: anatomy

## Slide Content
```bash
#!/usr/bin/env bash        # shebang: which interpreter
# counts errors in a log   # comments are for your future self
LOG="${1:?usage: $0 <logfile>}"   # argument + guard
grep -c 'ERROR' "$LOG"
```
- `chmod u+x script.sh`, run `./script.sh app.log`
- `${1:?msg}` — fail loudly if the argument is missing

## Instructor Delivery Notes
Type it live, run it wrong (no argument) on purpose — the guard message
is the teaching moment: *failures you designed are friendly*.

## Visual or Demonstration Suggestion
Side-by-side: same script with and without the guard, both run bare.

## Student Question
"Why `./script.sh` and not just `script.sh`?"

---

# Slide 3 — Quoting: the source of 90% of bugs

## Slide Content
- `"$VAR"` — expands, **keeps spaces** (almost always what you want)
- `$VAR` — expands, then splits on spaces (the bug factory)
- `'$VAR'` — literal, no expansion
- Backticks are legacy: `$(...)` for command substitution

## Instructor Delivery Notes
Live proof: a filename with spaces through both forms. The rule to
chant: *"quote your variables."*

## Visual or Demonstration Suggestion
`f="my data.csv"; wc -l $f` vs `wc -l "$f"` — watch one explode.

## Student Question
"Which form would you use in a `for f in *.csv` loop?"

---

# Slide 4 — Exit status: how programs tell the truth

## Slide Content
- Every command returns **0 = success**, nonzero = failure
- `$?` holds the last status · `exit 1` from a script
- `&&` runs on success · `||` runs on failure
- Silent failures are lies: *scripts that continue on error are dangerous*

## Instructor Delivery Notes
Demo: `ls /exists && echo ok` vs on a missing dir. Then the moral: the
backup script that keeps going after a failed copy is *worse* than one
that dies loudly.

## Visual or Demonstration Suggestion
`false || echo "caught"` · `true && echo "chained"` — semantics made visible.

## Student Question
"Your script copies 100 files; file 7 fails. What should happen?"

---

# Slide 5 — Control flow: if, test, loops

## Slide Content
```bash
if [[ -f "$LOG" ]]; then echo "log exists"; fi    # file tests: -f -d -r -s
for f in *.csv; do echo "$f"; done
while read -r line; do echo "$line"; done < input
case "$1" in start) echo go ;; stop) echo halt ;; esac
```
- `[[ ]]` over `[ ]` in bash — fewer quoting traps

## Instructor Delivery Notes
The `while read` + redirect pattern unlocks line processing — foreshadow
it as "sed/awk's scripted cousin." File tests get a quick drill
(`-s` = exists *and* nonempty; students guess wrong).

## Visual or Demonstration Suggestion
Live file-test table: touch/copy files of varying states, test each.

## Student Question
"How would you skip empty files in a processing loop?"

---

# Slide 6 — Functions & the standard skeleton

## Slide Content
```bash
#!/usr/bin/env bash
set -euo pipefail            # fail loudly, no unset vars, pipe-safe
usage() { echo "usage: $0 <dir>"; exit 1; }
[[ $# -eq 1 ]] || usage
main() { echo "processing: $1"; }
main "$@"
```
- One skeleton, memorized, reused all course (and in M23's sync script)

## Instructor Delivery Notes
This skeleton *is* the course standard — it returns in M19 (cron jobs),
M23 (sync), the assignments, the capstone. Sell the memorization.

## Visual or Demonstration Suggestion
Annotated skeleton with each line's failure-prevention story.

## Student Question
"Which line prevents `rm -rf "$TARGET/"` disaster when `$TARGET` is unset?"

---

# Slide 7 — Knowledge check + activity

## Slide Content
1. What does `set -e` NOT protect against? (hint: `cmd || true`)
2. Write the guard line for a script requiring exactly 2 arguments.
3. Pairs: predict, then run, three quoting scenarios from the deck.

## Instructor Delivery Notes
Q1 is deep — `|| true` *defeats* set -e, and command failures in
`if`-conditions are exempt; that nuance separates strong students.

## Visual or Demonstration Suggestion
— (pair work)

## Student Question
(task 3 results)

---

# Slide 8 — Debugging: bash -x and shellcheck

## Slide Content
- `bash -x script.sh` — trace every expansion as it happens
- `shellcheck script.sh` — the linter that catches tomorrow's bug today
- Debug order: reproduce → trace → minimize → fix → **re-run the original failure**

## Instructor Delivery Notes
Fix-the-bug lab follows; demonstrate the *method* on one broken script
first — students copy your process, not your fix. `shellcheck` on a
classic `$VAR` bug: feel the machine catch it.

## Visual or Demonstration Suggestion
Live: broken script → `bash -x` → the expansion betrays the bug → fix → shellcheck clean.

## Student Question
"What's the difference between a syntax error and a logic error in a trace?"

---

# Slide 9 — M11: automation patterns

## Slide Content
- **Idempotency:** running twice = running once (mkdir -p, overwrite-not-append)
- Batch processing with per-file logs and failure isolation
- Environment setup scripts (why dotfile hygiene matters)
- Report generation: script → text/email/CSV artifact

## Instructor Delivery Notes
Idempotency is the assessment word for this unit — make them define it
in their own words. Cron-preview: "a job that runs nightly *must* be
idempotent — nobody's there to clean up the duplicates."

## Visual or Demonstration Suggestion
Non-idempotent append vs idempotent rewrite — run each 3× and diff.

## Student Question
"Which of your Unit 2 one-liners are already idempotent?"

---

# Slide 10 — Common mistakes (Unit 3)

## Slide Content
- Unquoted variables (spaces → word-split chaos)
- No exit codes — a cron job that always "succeeds" even when it fails
- Copy-paste scripts without reading: the shebang is missing, the paths are absolute to *someone else's* home
- Testing only the happy path — the empty file, the missing dir
- `set -e` cargo-culted without understanding what it guards

## Instructor Delivery Notes
The fix-the-bug lab is built from exactly these; this slide is its
answer key in disguise — keep it on screen during lab if needed.

## Visual or Demonstration Suggestion
A "bug zoo" collage: five two-line scripts, one bug each.

## Student Question
"Which bug is worst for a script nobody watches? Why?"

---

# Slide 11 — Data Science connection

## Slide Content
- The M10 mini-project: an experiment-directory generator — every run gets a stamped, structured folder
- Batch dataset validation before it reaches pandas
- The M23 sync script and capstone health-check are this skeleton, scaled
- Automation = reproducibility's engine

## Instructor Delivery Notes
Show the M23 `sync-results.sh` (they'll write it in week 11) — "same
skeleton you memorized today." The arc from guard-line to capstone is
visible and motivating.

## Visual or Demonstration Suggestion
Timeline: today's skeleton → cron job (W9) → sync script (W11) → capstone health check.

## Student Question
"What routine task on your own machine deserves a script?"

---

# Slide 12 — Summary & exit ticket

## Slide Content
**Summary:** skeleton · quoting · exit codes · control flow · debug method · idempotency
**Exit ticket:** 1) what does `set -euo pipefail` each flag do? 2) one bug from today you'll never write again?
**HW:** M10/M11 quizzes · Mini-Project A · Assignment 1 released

## Instructor Delivery Notes
Collect and skim the "never again" bug live — naming it publicly cements it.

## Visual or Demonstration Suggestion
— 

## Student Question
(exit ticket is the question)

---

## Deck references
- Modules: [M10](../../modules/M10-bash-scripting/README.md) · [M11](../../modules/M11-advanced-shell-automation/README.md)
- Next deck: [Unit 4 — System Administration](unit-04-system-administration-slides.md)
