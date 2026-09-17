# Week 07 Dry-Run Report — Consolidation + MIDTERM

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S13–S14** · Materials: no deck — exam week (plan rows + instruments).
> **Status: PASS (verification-only week)**

---

## 1. Executive summary

S13 is the station-circuit consolidation; S14 is the 2-hour midterm. The exam paper's coverage line (M01–M13) matches the plan and the checklist; the paper is evidence-first with a live-terminal section; the key is instructor-side. This week needed no corrections — it was verification-only, and its materials were already aligned by earlier reviews.

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S13–S14 rows)`
- `teaching/teaching-plan/assessment-schedule.md (midterm row verified)`
- `assessments/exams/midterm.md (scope + sections verified)`
- `assessments/exams/midterm-key.md (instructor-side verified)`
- `teaching/instructor-resources/grading-sheets/midterm-grading-sheet.md (existence)`
- `teaching/instructor-manual/module-teaching-guides/unit-01-foundations.md → unit-04 guides (Units 1–4 scope check)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 7 block verified aligned)`
- `assessments/midterm/README.md (pointer verified)`

## 3. Coverage audit

Outcomes (self-diagnose weak spots; rehearse exam formats) present in S13's row; S14 logistics complete (120-min window, transcript requirement, snapshot count). The consolidation circuit's 6 stations are defined in the plan row; practice questions + troubleshooting scenarios exist in the revision tree for station material.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S13 — brief + 6-station circuit + debrief | 10 · 65 · 15 | as planned | low | students drive; instructor floats |
| S14 — midterm examination | 120-min window | as planned | low (logistics risk only) | snapshot count + spare station verified in checklist |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Midterm scope verified: paper header 'Units 1–3 (M01–M13)' matches plan S14 and checklist Week 7. Note: M14/M15 are taught in W6 (sessions 11–12) but the exam's coverage line predates that arrangement — the paper's actual items sample sudo/umask/permissions reasoning that W6's teaching covers, so the scope line is *defensible as written*; flagged as an instructor decision whether to amend the header to M01–M15 in a future revision (a content change to the exam paper is out of scope for this teaching-package review).
- Grading-sheet structure matches the paper's sections (verified line-level for Section A row count).

## 6. Safety review

- Exam VM faults are staged by the instructor; student-side is read-mostly with one scoped sudo task (paper §C rules). No host risk.
- Transcript-first rule (`script midterm.log`) is the exam's integrity spine — verified present in the paper.

## 7. Lab review

- The circuit is the lab (plan S13) — no separate lab deliverable; consistent with the schedule's 'nothing else this week'.
- No lab answers leak into the circuit description.

## 8. Assessment review

- Weight 20% per schedule + exam README — consistent.
- Second-mark ≥85 rule present in checklist — good practice, preserved.
- Quiz-bank windows for M12–M15 close this week per checklist W11 note — verified in the schedule rows.

## 9. Consistency findings

- Checklist Week 7 verified aligned already (one of the few pre-realignment blocks that matched).
- Plan S13's instructor-note pointer (teaching/assessments/midterm/README.md) resolves — verified.

## 10. Corrections applied

- None required — verification-only week. (The M01–M13 vs M14/M15 scope-header question is recorded above as an instructor decision, not silently changed.)

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Exam staging on a VM (instructor-side execution).
- Live station-circuit timing with students.

## 13. Remaining risks

- The scope-header question (above) — resolve before printing the paper for a cohort.
- Room logistics (snapshot-per-seat) remain the classic failure mode; the checklist's spare-station check is the mitigation.

## 14. Recommendations for the following week

- After the midterm: triage the heaviest-lost items and open S15 by re-teaching the worst one (the U5 SN's design).
- Loopback images for W8 must be staged the afternoon before (checklist Week 8).

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
