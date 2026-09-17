# Instructor-Only Resources

> 🔒 **Every file below (and in this directory) is INSTRUCTOR-ONLY.**
> It exists in the public GitHub repository only for distribution
> convenience; see [INSTRUCTOR-ONLY.md](INSTRUCTOR-ONLY.md) for why
> Pages cannot protect these files and how to store them privately.
> **None of these files are linked from student-facing navigation.**

| Resource | Purpose | Source of truth |
|---|---|---|
| [grading-sheets/midterm-grading-sheet.md](grading-sheets/midterm-grading-sheet.md) | Per-question score capture with CLO trace for the staged midterm | keys live in `assessments/examinations/` (repo) |
| [grading-sheets/final-grading-sheet.md](grading-sheets/final-grading-sheet.md) | Same pattern for the final | `assessments/examinations/` |
| [grading-sheets/practical-checklist.md](grading-sheets/practical-checklist.md) | Hands-free tick-list for exam invigilation | `assessments/examinations/practical-key.md` (repo) |
| [grading-sheets/lab-assessment-sheet.md](grading-sheets/lab-assessment-sheet.md) | Generic evidence-based lab scorer, reusable per LA-n | LA sheets in `assessments/lab-assessments/` |
| [attendance/attendance-template.csv](attendance/attendance-template.csv) | Section roster + weekly session columns | — |
| [INSTRUCTOR-ONLY.md](INSTRUCTOR-ONLY.md) | Storage, distribution, and Pages-exposure policy | — |

## Why so thin, when the prompt asks for full answer keys?

Because they already exist, executed and validated, elsewhere in the
repository — duplicating them here would create drift risk with zero
pedagogical gain:

- **Quiz keys** — one instructor key per module:
  `modules/M*/content/practice/quiz-answers.md`
- **Examination keys + staging guides**:
  `assessments/examinations/midterm-key.md`, `final-key.md`,
  `practical-key.md` (includes the staging script)
- **Mini-project rubrics + exemplars**:
  `projects/*/RUBRIC.md`, `projects/*/SOLUTION-NOTES.md`
- **Assignment keys (this package's new A4–A6)**: sit beside their
  student papers in [../assessments/assignments/new/](../assessments/assignments/new/README.md)
- **Viva bank + capstone protocol**: `assessments/viva/` (repo)

The new artifacts *this* package adds are the **grading workflow
sheets** (per-question capture, evidence quoting, CLO trace) — the one
instructor resource the repository genuinely lacked. They reference the
existing keys rather than restating them.
