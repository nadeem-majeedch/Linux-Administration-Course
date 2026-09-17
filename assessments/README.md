# Assessments — Linux Administration Course

> Centralized assessment bank for BS Data Science students.
> **Design contract:** every instrument tests *understanding under
> constraint* — diagnosis, prediction, justification, evidence
> interpretation — never transcription. A student who memorized a
> cheatsheet should fail these; a student who understands should
> pass them without one.

## What's here

| Directory | Contents | Use |
|---|---|---|
| [quizzes/](quizzes/) | Exemplar bank: M12 format standard + the per-module index; per-module reasoning quizzes live in `modules/*/content/practice/` (595 questions) | weekly/biweekly |
| [lab-assessments/](lab-assessments/) | Graded 20–30-min lab checks (LA-1…LA-5): task + 10-pt evidence rubric per level | end of each unit |
| [exams/](exams/) | Midterm (Units 1–3), final (Units 4–7), practical exam — papers, keys, staging guide | midterm & end |
| [assignments/](assignments/) | Three assignment specs (The Organized Analyst / Automated Pipeline / Remote Operator) | distributed |
| [practical/](practical/) | The staged-server practical exam (also indexed under exams/) | end of term |
| [project-rubric.md](project-rubric.md) | Pointer to the capstone rubric (full pack: `projects/capstone/instructor/`) | capstone |
| [viva-questions.md](viva-questions.md) | Consolidated oral-exam bank (derived from `projects/capstone/instructor/VIVA.md`) | viva/defense |

## The anti-memorization rules (enforced across all instruments)

1. **No question may be answerable by pattern-matching a cheatsheet.**
   Allowed: "here is output/a symptom — diagnose". Disallowed: "which
   flag lists hidden files?".
2. **Every scenario question ships with the evidence**, not the
   command list: students receive error messages, `ls -l` excerpts,
   log lines, and must reason from them.
3. **"Why" outranks "what".** For any command asked, the marks sit in
   the *justification* and the *verification*, not the invocation.
4. **Safe-by-default grading:** no instrument ever requires a student
   to damage a system to answer; where breakage is part of a lab, it
   is staged and reversible (per-module lab rules).
5. **Explain-the-output** is a question type: given a real command
   output, students annotate it — catching both misconceptions and
   command-hallucination.

## Grading philosophy

- **Evidence over claims.** "I set it up" scores nothing; the
  command + output + interpretation scores.
- **Partial credit for correct method.** Wrong diagnosis with a
  *sound* evidence chain earns more than a lucky right guess.
- **Safety is graded.** Destructive-command misuse is a deduction in
  every instrument, not just the security module's.
