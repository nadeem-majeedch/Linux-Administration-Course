# Examinations

> Formal assessment papers with instructor keys and, where relevant,
> staging guides. All papers follow the course assessment philosophy:
> **every question gives evidence or a scenario, and grades
> reasoning — nothing is answerable by copying a cheatsheet.**

| Paper | Duration | Weight | Format | Key |
|---|---|---|---|---|
| [Midterm](midterm.md) — Units 1–3 (M01–M13) | 2 h | 20% | A reasoning · B output-tracing · C live terminal | [midterm-key](midterm-key.md) |
| [Final](final.md) — Units 4–7 (M14–M31) | 3 h | 25% | A reasoning · B evidence diagnosis · C design · D live terminal | [final-key](final-key.md) |
| [Practical](../practical/practical-exam.md) — staged-server circuit | 90 min | 15% | 12 tasks over 6 planted faults, transcript-graded | [practical-key](../practical/practical-key.md) (incl. staging script) |

## How these differ from module quizzes

- **Scenario-first.** Every item hands the student terminal evidence
  (a `ls -l`, a journal fragment, a `ss` dump) or a fault to find —
  never "what does flag X do".
- **Transcript-graded.** Practical portions require `script` logs;
  end states alone cap below full marks because the *method* is the
  learning objective.
- **Fault-planted, snapshot-restore.** The practical exam runs on a
  staged VM restored per student; the staging script and answer key
  live together in [practical-key.md](../practical/practical-key.md).

## Weights in the course grade

Together with module quizzes (10%), lab assessments (10%), the
midterm (20%), final (25%), practical (15%) and the capstone project
(20% — see `projects/capstone/instructor/RUBRIC.md`), these papers
carry the formal grade. Suggested pass rule: ≥ 40% overall **and**
no zero-score trigger on the practical.

## Integrity

Closed book except the practical (own notes, no internet). All
papers share one rule: evidence quoted from the system outranks
memory. Any paper can be re-derivated per cohort by rotating the
planted faults in the staging script — the rubric structure stays.
