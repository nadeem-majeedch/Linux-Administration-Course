# Unit 2 Teaching Guide — Command Line Fluency (M05–M09)

> Sessions S5–S8 · companions: [speaker notes](../../speaker-notes/unit-02-command-line-notes.md) · [deck](../../lecture-slides/unit-02-command-line-slides.md)

## M05 Terminal & Shell (S5)

**Objectives.** Command anatomy reading; help-system independence
(`man` reflex); shell basics (variables, history, aliases at reading
level).

**Sequence.** Three-boxes diagram → anatomy → man-page synopsis
reading → FHS begins (M06 folds into this session's second half).

**Difficult concepts.** SYNOPSIS notation (`[...]`, `...`) — teach it
as grammar and every man page opens forever after.

**Common mistakes.** Ctrl+S freezing the terminal (teach Ctrl+Q day
one); man-page navigation panic.

**Demo plan.** `man ls` synopsis decode; `type -a` reveals.

**Activity.** Path flash-cards (pairs).

**Assessment hook.** M05 quiz; M05's practice file covers aliases/history.

**Extension.** ★★★: the `type` census challenge from M05's practice —
classify 12 commands by resolution kind.

**Troubleshooting.** Keyboard layout mishaps in VMs (dead keys) —
SETUP.md fix; don't debug live for long.

## M06 Filesystem Hierarchy (S5 second half)

**Objectives.** FHS as vocabulary; absolute/relative path fluency;
`~`, `-`, `..` mechanics.

**Difficult concepts.** Relative-path resolution after multiple `cd`s —
the two-terminal demo is the fix.

**Common mistakes.** `~` confusion with `/`; `..` chains miscounted.

**Assessment hook.** M06 quiz (path resolution from descriptions).

**Extension.** ★★★: "which FHS directory would hold X?" for ten unusual
X values (kernel docs, tmpfiles, user crontabs).

## M07 Files & Directories (S6)

**Objectives.** Workhorse verbs with safety reflexes; inode/name
distinction; glob prediction.

**Difficult concepts.** Glob expansion happens *in the shell* — the
`rm` safety talk hangs entirely on this mechanism; teach the mechanism,
the reflex follows.

**Common mistakes.** Spaces in filenames meeting unquoted scripts
(previewed); `rmdir` vs `rm -r` confusion.

**Demo plan.** `ls -li` hard links; ls-first-then-rm choreography.

**Activity.** Glob-prediction: six globs, write matches first.

**Assessment hook.** M07 quiz (glob prediction + inode consequences);
feeds A1's organization section.

**Extension.** ★★★: the M07 challenge set's link-farm exercise.

**Troubleshooting.** Students deleting lab trees prematurely — the
teardown census ritual is introduced *this* week.

## M08 Text Processing (S7–S8, two sessions)

**Objectives.** Streaming-first data reflexes; the core toolkit; then
grep/sed/awk composition into the signature pipeline.

**Sequence.** S7: cat/less/head/tail/wc + sort/uniq/cut/tr + the
profiling challenge. S8: grep families + sed s/// + awk fields → the
file→grep→cut→sort→uniq→awk pipeline built one stage at a time with
predictions.

**Difficult concepts.** sort-before-uniq (mechanism, not rule);
pipeline stage *shape* thinking (what type of data does each stage
expect/emit).

**Common mistakes.** CRLF files breaking field extraction (module
troubleshooting covers the fix); regex scope creep.

**Demo plan.** The 50 MB-profile-without-opening challenge; pipeline
built live with predicted intermediates.

**Activity.** Pipeline relay (S8 formative).

**Assessment hook.** M08 quiz (pipeline design); mini-project; LA-2
pipeline circuit in week 8.

**Extension.** ★★★: M08 challenges — the log-forensics items.

**Troubleshooting.** Dataset distribution failures — keep a local copy
of `datasets/` on the instructor machine.

## M09 Pipes & Redirection (S8)

**Objectives.** The x-y table as internalized semantics; stdin vs
argument; the truncation trap.

**Difficult concepts.** Redirection *opens before exec* — the gasp demo
(`ls > full-file`) does more than any diagram.

**Common mistakes.** `2>&1` ordering; `sort < f > f` corruption.

**Assessment hook.** M09 quiz (where-do-the-bytes-go); feeds A2's
pipeline section.

**Extension.** ★★★: process substitution pointer (reading-level).

---

## Unit-level notes

- **The wall is relative paths (S5) then composition (S8).** Budget
  flexibility accordingly; M06 second-half and M09 can each shed 10
  minutes if the walls need more time.
- **LA-1 lands in week 4** — announce it in S6 (not later); students
  practice the [navigation circuits](../../../modules/M05-terminal-and-shell/content/labs/README.md) as HW.
- **DS framing discipline:** every S7/S8 example uses course datasets
  (logs, CSVs, sensors) — resist generic foo/bar examples; the DS
  thread is the motivation engine.
