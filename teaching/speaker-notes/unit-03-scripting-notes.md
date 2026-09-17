# Unit 3 Speaker Notes — Scripting & Automation (M10–M11)

> Companion to [../lecture-slides/unit-03-scripting-automation-slides.md](../lecture-slides/unit-03-scripting-automation-slides.md).

## Sessions 9–10 overview

**Teaching purpose.** Convert command-line fluency into *responsibility*:
scripts that guard their inputs, fail loudly, and can be trusted unattended.
This is the unit where assessment most rewards method over luck — the
fix-the-bug lab and A1's script section both grade the guards, not the output.

**Opening question (S9).** "What's the difference between a command that
works and a command you'd bet your dataset on?" Collect adjectives
(tested, guarded, logged, repeatable) — they *are* this unit's rubric.

## Per-slide guidance

- *S2 (anatomy):* run the guard version bare on purpose. The `${1:?}`
  message appearing feels like the script *talking back* — that's the
  intended emotional beat: scripts can be taught to refuse politely.
- *S3 (quoting):* the word-splitting demo with a spaced filename is the
  session's core. Ask "what did the shell *think* you meant?" — the
  answer (two files: `my` and `data.csv`) is the misconception made
  visible.
- *S4 (exit codes):* the 100-file copy scenario is a values probe, not a
  syntax drill. Both "continue and report" and "die immediately" are
  defensible; what matters is *choosing* and *logging*. Pull for that
  explicitly.
- *S6 (skeleton):* have them memorize it *now* — flash it at the start
  of S10 and have the class recite. It returns in M19 cron labs, M23
  sync script, A2, and the capstone; familiarity compounds.
- *S8 (debugging):* demonstrate the method on ONE script, slowly. The
  trace line where the variable expansion betrays the bug deserves a
  slow-motion re-read. shellcheck: run it on the same script *after*
  manual fixing — "the machine agrees" closes the loop.
- *S9 (idempotency):* run each sample script three times; the
  non-idempotent one visibly corrupts state. Cron-preview the stakes:
  "nightly means nobody's watching."

## Misconceptions (unit-wide)

1. "`set -e` makes my script safe" — it's one layer; `|| true`, command
   substitution, and `if` conditions all have exemptions. The lab's
   Q-discussion covers this honestly.
2. "Scripts and commands are different languages" — same shell, same
   grammar; a script is a *file of* what they already know.
3. "bash -x is for when it breaks" — teach trace-first development for
   anything with variables.
4. "shellcheck is pedantic" — reframe: it's a senior reviewer who never
   sleeps.

## Expected student responses

- S4 scenario: most vote "continue and report" — push on *how* the
  report happens (exit code? log line? both?). Lazy answers evaporate
  under that follow-up.
- S9 idempotency definitions: expect paraphrases of "run twice = run
  once"; sharpen with the append-vs-overwrite example.

## Live demo instructions & error table

| Demo | Command shape | Failure to show | Recovery |
|---|---|---|---|
| guard | `./s.sh` (no arg) | usage message, exit 1 | add argument |
| quoting | `wc -l $f` with spaces | two-file error | `"$f"` |
| trace | `bash -x broken.sh` | expansion reveals bug | fix + shellcheck |
| trap of set -e | `false \|\| echo ok` | exit 0 despite false | explain exemption |

## Classroom activities

- Spot-the-bug trio (S9 formative): keep each script ≤6 lines; one bug
  each — quoting, missing guard, unhandled failure.
- Skeleton recitation (S10 warm-up): 60 seconds, whole class.

## Timing and cuts

S9 is lecture-heavy; the lab *must* start by 50 minutes. If behind:
cut S7 Q3 (pair prediction) — the labs cover it. S10: never cut the
live debug; it's the unit's transferable skill.

## Transition

"You can write scripts the machine can trust. Unit 4: who is allowed to
run them — and with whose authority?" (identity → permissions → sudo).
