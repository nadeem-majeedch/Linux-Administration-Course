# Final Examination — Delivery Notes

> Paper and key live in the exam bank; this page adds delivery: CLO/
> module mapping, difficulty distribution, logistics. Nothing here
> changes the paper.

- **Student paper:** [assessments/exams/final.md](../../../assessments/exams/final.md) — 3 h, 100 pts, Units 4–7 (M14–M31)
- **Answer key & grading guide:** `assessments/exams/final-key.md` — **instructor-only** ([inventory](../../instructor-resources/README.md))
- Weight: **25%** of the course grade (repository scheme)

## CLO / module mapping (proposed CLOs — [alignment matrix](../../../accreditation/CLO-ASSESSMENT-ALIGNMENT.md))

| Section | Typical content | CLOs | Modules |
|---|---|---|---|
| A — Reasoning | services, storage, network concepts applied | CLO-4, CLO-5 | M16–M21 |
| B — Evidence diagnosis | journal/df/ps artifacts → root cause | CLO-6 | M18, M24, M32 |
| C — Design | pipeline + backup + serving design choices | CLO-4, CLO-7 | M19, M23, M29, M31 |
| D — Live terminal | staged-VM tasks: services, transfer, monitoring | CLO-4, CLO-5, CLO-6 | M20–M25 |
| (across) | Git/venv/containers items | CLO-7 | M26–M28 |

The final also samples CLO-2 (scripting) via design-section items —
the full CLO-1 load stays with the midterm and LA-1/LA-2 (documented
in the alignment matrix's honest-gaps section).

## Difficulty distribution (as shipped)

Easy recall-in-context ≈ 20% · intermediate evidence/mechanism ≈ 55% ·
transfer/design ≈ 25%. Section B items are *method-graded*: a correct
conclusion from skipped evidence steps loses points — the transcript
discipline is the exam's hidden syllabus.

## Logistics

- **Environment:** staged VM snapshot per seat for Section D; the
  staging script ships in the answer key (instructor-only)
- **Transcript:** `script final.log` before Section D; method caps
  apply exactly as in the practical exam
- **Scheduling with the capstone:** run the final in the S32 window
  with capstone defenses in parallel blocks per cohort size — the
  [plan](../../teaching-plan/16-week-course-plan.md#session-32--final-examination--capstone-defenses)
  marks the split
- **After marking:** section-level cohort analytics (which rung/concept
  failed cohort-wide) feed next semester's emphasis — the exam bank is
  a curriculum instrument, not just a grade

## Common failure patterns

1. Section B: firewall/DNS blamed before checking listeners (rung order)
2. Section C: backup designs without a restore-test clause (M19's rule)
3. Section D: `systemctl enable` offered where `start`/`restart` was
   the failure (the enable≠start misconception, still alive in week 16)
