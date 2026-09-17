# Week 16 Dry-Run Report — Assessment week (practical + final + viva)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S31–S32** · Materials: no deck — instruments (plan rows + papers + keys).
> **Status: PASS (verification-only week)**

---

## 1. Executive summary

The exam week: a 90-minute staged practical (6 faults, 12 tasks, 100 pts, transcripts required), the 3-hour final (A–D, 100 pts), and capstone defenses. All instruments verified present with instructor-side keys and separate grading sheets; the checklist Week 16 was already aligned. Verification-only week — no corrections required.

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S31–S32 rows)`
- `teaching/teaching-plan/assessment-schedule.md (W16 rows verified)`
- `assessments/practical/practical-exam.md (structure verified: 4 parts × 25 pts, T1–T12, 6 planted faults, transcript rules)`
- `assessments/practical/practical-key.md (instructor-side verified)`
- `assessments/exams/final.md (Sections A–D verified)`
- `assessments/exams/final-key.md (instructor-side verified)`
- `projects/capstone/instructor/VIVA.md (existence)`
- `teaching/instructor-resources/grading-sheets/practical-checklist.md + final-grading-sheet.md (existence)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 16 block verified aligned)`

## 3. Coverage audit

Plan rows complete (logistics, scheduling of vivas in parallel per cohort size); instruments exist and match every teaching-layer description of them (deck counts verified in W15's report; schedule weights verified); grading sheets match the papers' sections; the practical's zero-score triggers (dangerous commands, no transcript) are published in the paper itself — no surprise rules.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S31 — practical examination | 90 min staged | as planned | medium (room logistics) | two sittings if the room demands — checklist carries it |
| S32 — final examination | 3 h | as planned | low | live-terminal section runs on the staged snapshot |
| S32 — capstone defenses | parallel scheduling | per cohort | medium | viva bank + protocol instructor-side (verified) |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Practical paper's fault list (services, permissions, disk, network/workflow) matches the course's lab spine; the 'curl from the VM to itself is not proof' task enforces the course's evidence discipline.
- Final's Section D live-terminal runs on the staged snapshot — consistent with the practical's staging pattern.
- Weights (practical 15%, final 25%) verified against the schedule and exam READMEs.

## 6. Safety review

- All exam faults are staged on instructor snapshots; student actions are sandboxed to their own exam VM.
- The integrity rules (no deleting evidence, transcript always running) are printed in the papers — verified.
- No host-system risk at any point; keys and staging scripts are instructor-only.

## 7. Lab review

- No labs — assessment week; the mock practical (S30) was the rehearsal.
- The staged-fault pattern matches LA-3/LA-4's staging (same muscle, higher stakes) — verified by structure.

## 8. Assessment review

- All four instruments' weights verified consistent: quizzes pool, labs pool, A1–A3 5% each, midterm 20%, practical 15%, final 25%, capstone rubric — the schedule's sum is coherent with the assessment README.
- Viva protocol (evidence + trade-offs) present in the capstone instructor pack (VIVA.md verified).
- Second-marking and grade-sheet flow present in the checklist.

## 9. Consistency findings

- Checklist Week 16 verified aligned already.
- Deck/notes descriptions of the exams (W15 report) match the actual papers — the last cross-check in the chain.
- No student-facing file links to any key (course-wide leak scan).

## 10. Corrections applied

- None required — verification-only week.

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Staging-script execution (instructor-side, on a clean template).
- Live practical exam timing with students.
- Viva sessions.

## 13. Remaining risks

- Room logistics remain the only meaningful failure mode — snapshot-per-seat + spare station + two-sittings rule are all in the checklist.
- Post-term: run the CLO evidence packet collection (plan exists) while transcripts are still fresh.

## 14. Recommendations for the following week

- Post-term retrospective: fold timing-observation sheets back into the plan's allocations.
- Instructor decisions list (FINAL report §18) — including the midterm scope-header question.
- Archive the VM-keep note to students (their first server's rehearsal).

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
