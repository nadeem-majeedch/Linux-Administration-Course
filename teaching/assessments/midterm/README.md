# Midterm Examination — Delivery Notes

> The paper and key live in the repository's exam bank; this page adds
> the delivery layer: CLO/module mapping, difficulty distribution, and
> logistics. **Nothing here changes the paper.**

- **Student paper:** [assessments/exams/midterm.md](../../../assessments/exams/midterm.md) — 2 h, 100 pts, Units 1–3 (M01–M13)
- **Answer key & grading guide:** `assessments/exams/midterm-key.md` — **instructor-only** ([inventory](../../instructor-resources/README.md))
- Weight: **20%** of the course grade (repository scheme)

## CLO / module mapping (proposed CLOs — [alignment matrix](../../../accreditation/CLO-ASSESSMENT-ALIGNMENT.md))

| Section | Typical content | CLOs | Modules |
|---|---|---|---|
| A — Reasoning | OS/distro/architecture concepts applied to statements | CLO-1 | M01–M04 |
| B — Output tracing | command output annotated; pipeline prediction | CLO-1 | M05–M09 |
| C — Live terminal | navigation, file ops, pipeline on a fresh VM | CLO-1, CLO-2 (emerging) | M05–M13 |
| (across) | permissions/identity items | CLO-3 | M12–M13 |

**Coverage boundary (deliberate):** M14 (sudo policy) and M15 are taught
in week 6 and are *in* the M01–M13 scope as module targets, but the
deepest sudo-policy items are held for the final — reviewers should
note the midterm does not carry the full CLO-3 load (documented gap in
the alignment matrix §4).

## Difficulty distribution (as shipped)

Easy recall-in-context ≈ 25% · intermediate mechanism/evidence ≈ 50% ·
transfer/design ≈ 25%. The design intent: a student who did the labs
passes; a student who memorized cheatsheets fails Section B.

## Logistics

- **Environment:** fresh VM snapshot per seat (Section C runs live);
  `script midterm.log` started *before* Section C — the transcript is
  graded with the answers
- **Prep policy:** students may bring their own **one-page prep sheet**
  (S12 homework) — own handwriting/typing, no printed module text
- **Timing guidance for students:** Section C is worth doing *first*
  if the room's machines are slow — announce a personal-strategy
  reminder, not a rule change
- **After marking:** release the anonymized exemplar answers per
  section (the fastest calibration), then the common-failure debrief

## Common failure patterns (for the post-exam debrief)

1. Section B: predicting `uniq -c` without `sort` — the pipeline order
   misconception, every cohort
2. Section C: transcript not started (method cap applies) — announced
   repeatedly, still happens; grade per the published cap
3. Permission items: owner-triplet misread when group membership
   matches (A7-style)
