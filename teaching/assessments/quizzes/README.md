# Quiz Bank v2 — New Formats

> The per-module **scenario quizzes** in `modules/*/content/practice/`
> (~620 questions) remain the canonical quiz bank. This v2 bank adds
> three formats the course lacked — useful for LMS import, quick
> formative rounds, and exam warm-ups:
>
> 1. **Multiple-choice** — distractors built from the documented
>    misconception bank (every wrong option is a *real* wrong model)
> 2. **Command interpretation** — "what exactly did this command do?"
> 3. **Output reading** — annotate real command output
>
> Same anti-memorization rules apply: every item presents evidence or a
> scenario; nothing is answerable from a cheatsheet.

- **Student paper:** [quiz-bank-v2.md](quiz-bank-v2.md) — 40 items in 4
  sections, difficulty-tagged, module-mapped
- **Answer key:** `keys-instructor/quiz-bank-v2-key.md` — **instructor
  only**; explains each answer, names the misconception each distractor
  encodes, and lists what evidence would settle disputed answers

## Usage patterns

| Use | How |
|---|---|
| Session warm-up | run one section (10 items) as a 5-minute round |
| LMS quiz | import MCQ section (auto-gradable); short answers graded by hand |
| Exam preparation | S13/S30 consolidation circuits use the output-reading items |
| Distractor study | TAs write new items by mining [common misconceptions](../../instructor-manual/common-misconceptions.md) |

## Contribution standard

New items must name: the module they assess, the misconception the
distractors encode, and the evidence that settles the answer. The
[format exemplar](../../../assessments/quizzes/quiz-m12.md) governs
scenario items; this file governs MCQ/interpretation items.
