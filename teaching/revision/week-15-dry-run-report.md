# Week 15 Dry-Run Report — The DS server + revision (M31, M32)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S29–S30** · Materials: unit-08 deck · unit-08 notes · workbook unit-08.
> **Status: PASS WITH WARNINGS (milestones anchored; heavy-by-design week)**

---

## 1. Executive summary

S29 runs the DS-server day and the drill-book incidents; S30 is student-driven revision. The deck's rubric table verifies line-accurate against RUBRIC.md, the 8-step method is consistent course-wide, and the practical-exam description (6 faults, 12 tasks, transcripts) matches the actual paper. Corrections landing here: the Operate/Document capstone milestones anchored in the plan, and the 'beforenoon' typo in the workbook's staging line.

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S29–S30 rows; Operate/Document milestones added)`
- `teaching/lecture-slides/unit-08-capstone-slides.md`
- `teaching/speaker-notes/unit-08-capstone-notes.md`
- `teaching/lab-workbook/module-labs/unit-08-capstone.md`
- `modules/M31-data-science-server/content/labs/ds-server-lab.md (existence)`
- `modules/M32-linux-performance-troubleshooting/content/labs/README.md + 4 incident labs (existence)`
- `projects/capstone/instructor/RUBRIC.md (10 areas verified line-accurate vs deck slide 3)`
- `projects/capstone/instructor/INCIDENTS.md (existence)`
- `labs/level-5-ds-server.md (existence)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 15 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (operate observably; run the method end-to-end), prerequisites (the whole course — by design), activities (13-scenario walk, team drills, revision circuits), demos (instructor drill with method narrated; morning-after skeleton), labs (M31 two-actor lab, M32 incidents 1–4, Level 5 optional), formative (method-step ordering round), HW (A3 due, capstone polish, revision checklist), SN timing (the drill never cuts; S30 student-paced).

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S29 — M31 13-scenario walk (as a timed day) | 35 M31 | 35 | low | students call the source unit per step — retrieval practice |
| S29 — one drill incident live + teams run 1–2 | 40 M32 | 40 | high — dress rehearsal | the drill never cuts (SN); pre-recorded fallback if tech fails |
| S30 — revision circuits (student-driven) | full session | full session | low | instructor's fixed roles: 10′ triage brief + 5′ logistics close (SN) |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Capstone rubric table (10 areas, 15/8/8/12/12/10/10/8/12/5) — verified line-accurate against projects/capstone/instructor/RUBRIC.md.
- 8-step incident method — consistent with M24's lesson and the practical exam's grading rules.
- Practical-exam description in deck slide 8 ('6 faults, 12 tasks, transcripts graded') — verified against the actual paper (T1–T12 across 4 parts; 6 planted faults).
- 'Final Sections A–D' — verified against final.md's section structure.

## 6. Safety review

- Drill incidents are student-staged by module scripts on their own VMs (workbook safety architecture).
- The two-actor M31 lab uses a colleague account on the student's own VM — shared-permission practice without shared infrastructure.
- Cleanup census (print, read, delete only own scratch) — the professional deletion habit, taught not assumed.
- The deliberate container-kill during Operate is disclosed to students in advance (SN) — honest staging, no betrayal.

## 7. Lab review

- M31 lab (2-session span, by design) + 4 M32 incidents (30′ each) + optional Level 5 — the heaviest lab week, correctly load-bearing for the practical exam.
- Method-fidelity scoring (ranked hypotheses, quoted evidence, step-7 verification) — the drill rubric names each; aligned with the practical exam's rules.
- All referenced lab files verified to exist (M31 ds-server-lab.md; M32's four incident labs; labs/level-5-ds-server.md).

## 8. Assessment review

- A3 due S29 (plan; schedule agrees) + Operate checkpoint graded live in S29 (milestone added to the plan this review).
- Document/Demo+viva milestones anchored to S30's HW (plan edit) — the defense scheduling note now has a home.
- Mock practical task (S30, ungraded) enforces the transcript habit before it counts.

## 9. Consistency findings

- Deck ↔ SN ↔ workbook ↔ plan — aligned; the rubric/exam cross-references verified at line level.
- Checklist Week 15 rewritten (F3) — now carries Operate checkpoint + A3 due.
- Workbook U8 staging line typo fixed ('afternoon before S29').

## 10. Corrections applied

- Plan S29 HW: Operate milestone line added; S30 HW: Document/Demo+viva milestone line added (gap 3).
- Workbook U8 'beforenoon' typo fixed (F8).
- Checklist Week-15 block rewritten (F3).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Drill-script execution on this semester's lab image (instructor-side, the afternoon before — now correctly ordered in the text).
- The Level-5 overnight run (optional; explicitly out of session scope).

## 13. Remaining risks

- S29 is the practical exam's dress rehearsal — if tech fails, the pre-recorded fallback keeps the method demo; never skip the teams' attempt.
- Students arriving without A3 done will try to do it during drills — the S30 structure (student-paced) absorbs it, but flag it in the brief.

## 14. Recommendations for the following week

- W16 is the exam week — practical checklist printed, viva slots booked, papers staged (checklist Week 16).
- Zero-score triggers shown verbatim in S30's close (SN) — no surprises at exam time.
- Post-term: the 'what to keep from your VM' note (checklist) + CLO evidence packet collection begins (clo-evidence-packet-plan.md).

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
