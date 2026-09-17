# Unit 2 Speaker Notes — Command Line Fluency (M05–M09)

> Companion to [../lecture-slides/unit-02-command-line-slides.md](../lecture-slides/unit-02-command-line-slides.md).

## Session 5 (Slides 1–6: shell, FHS, paths)

**Teaching purpose.** Fluency foundations: the shell as *program*, the
FHS as *map*, paths as *addresses*. By the end, `cd` should feel like
walking, not typing.

**Opening question.** "What happens between pressing Enter and seeing
output?" Collect guesses; by unit's end they can answer precisely
(parse → PATH lookup → fork/exec → output). Today: the parse only.

**Per-slide guidance.**

- *S2:* the three-box diagram (terminal/shell/kernel) is the reference
  image all unit — draw it once, point at it often.
- *S4 (FHS):* walk live, not slideware. Pause at `/tmp` for the
  reboot-wipe design discussion — "why would designers WANT a self-
  cleaning folder?" (expected: temporary state, safety).
- *S5 (paths):* the relative-path wall. Run the two-terminal demo
  personally — same commands, different starting points. Then the
  `~../bin` trick question; resolve it on a drawn tree, never in air.

**Terminology.** *prompt, expansion, working directory, mount point*.
Insist on "working directory" over "current folder" — it maps to `pwd`
and to how every tool resolves paths.

**Misconceptions.**
1. "Home directory = the disk's root" (`~` vs `/`).
2. "`cd` in one terminal changes the other" (sessions are separate processes).
3. "Absolute paths are 'better'" — teach *when* each wins (scripts: absolute or explicit; humans: relative).

**Live demo instructions.** FHS walk: `/etc` (open one config, show it's
just text), `/var/log`, `/proc`, `/dev`. Under 8 minutes; wonder beats
exhaustion.

**Possible errors.** Students typing into a *frozen* terminal (Ctrl+S
pressed) — teach Ctrl+Q now, it happens weekly. Someone will `cd` into a
file — the error message itself is the lesson ("Not a directory").

**Classroom activity.** Path flash-cards (10 rounds, pairs) — one shows a
path, the other traces it on a paper tree.

**Timing.** If behind, drop the `cd -` delight exercise (they'll meet it
in the lab anyway). Never cut the two-terminal demo.

**Transition.** "You can go anywhere. Next: do things to what you find."

---

## Session 6 (Slides 7–8: files, rm safety)

**Opening question.** "How would you organize 400 raw CSVs that arrive
daily?" — collect structures on the board; validate date-based trees.
Their designs become the M07 lab.

**Key guidance.**

- *S7:* `mv`-as-rename demoed twice. Inode talk capped at 3 minutes —
  `ls -li`, two names one inode, "the name is a label on the file, not
  the file."
- *S8 (rm):* this is a safety lecture wearing a demo costume. The
  glob-expansion point (shell expands first) is the deepest idea — after
  it, the `ls`-first reflex is *obvious*, not a rule to obey.

**Expected responses.** "Why no trash can?" — embrace it: servers have no
trash can either; this course teaches production reality. Someone will
say `rm -rf /` is a myth — have the recovery story ready (it is not a
myth; snapshots exist precisely because typing happens).

**Classroom activity.** Glob-prediction: six globs on screen, students
write matches before running. The `*.*` vs `*` one always surprises.

**Timing & transition.** Lab after 35 min of content. Exit: "name the
reflex that precedes every `rm` with a wildcard."

---

## Session 7 (Slides 9: text core) and Session 8 (Slides 10–13)

**Teaching purpose.** The DS centerpiece: datasets as text streams.
Session 7 builds vocabulary tools; Session 8 composes them into the
signature pipeline.

**Opening question (S7).** "A 50 GB CSV arrives. Your laptop has 8 GB
RAM. What now?" Sit in the silence. The answer this unit builds: *sample,
count, and filter in streaming mode — never load*.

**Key guidance.**

- *S9:* sort/uniq interplay is the first genuine composition barrier.
  Demo the wrong order deliberately; the doubled lines make the point
  better than any rule.
- *S10:* the "grep finds, sed changes, awk reports" heuristic prevents
  tool-soup. Scope police: no `sed` scripts, no `awk` loops — Unit 3's
  bash owns logic.
- *S11 (redirection):* the x-y table is built *with* the class, not
  shown. The truncate-before-running demo (`ls > f` with fat `f`)
  produces audible gasps — use them.
- *S12 relay:* four students each contribute one stage. Grade the
  *composition thinking* aloud — "why sort before uniq?" etc.

**Misconceptions.**
1. "`>` writes after the command finishes" (it truncates first).
2. "grep and find are related" (different universes — files vs line contents).
3. "awk is old, pandas replaces it" — profiling a 5 GB file in RAM-bound pandas says otherwise; show the M08 numbers.

**Live demo choreography (S8 centerpiece).**
Build `file → grep → cut → sort → uniq -c → sort -rn → head` one stage
at a time on real course logs, *predicting each intermediate shape
before running*. The prediction habit is the actual skill being taught.

**Errors during labs.** `sed: -e expression #1, char N: unterminated 's'`
(unclosed delimiter), `awk` field refs on the wrong `-F` separator, CRLF
files making `$2` carry `\r` — all documented in module troubleshooting;
point students there rather than solving for them.

**Timing.** Session 8 is the unit's densest: if behind, the relay becomes
a demo; the x-y table never gets cut.

**Transition.** "You've composed commands. Friday's homework: compose
them into something that survives." (Unit 3.)

---

## Unit-level instructor checklist

- [ ] Course datasets present on lab share or in `datasets/` copy
- [ ] Two-terminal demo rehearsed (it's the unit's best 4 minutes)
- [ ] LA-1 scheduled and staging checked ([lab-assessment-01](../../assessments/lab-assessments/lab-assessment-01.md))
- [ ] Read [module teaching guide U2](../instructor-manual/module-teaching-guides/unit-02-command-line.md)
