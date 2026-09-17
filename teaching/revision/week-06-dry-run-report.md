# Week 06 Dry-Run Report — Identity and access (M12–M15)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S11–S12** · Materials: unit-04 deck · unit-04 notes · workbook unit-04.
> **Status: PASS WITH WARNINGS (1 precision fix + checklist realignment)**

---

## 1. Executive summary

S11–S12 carry the course's permission core (triplet, umask, SGID/sticky, sudo policy, PATH). Technically the deck is accurate after one precision fix: the 'uid < 1000' system-user statement is a Debian/Ubuntu packaging convention, not kernel law — corrected. The sticky-bit scenario vote and the sudo redirection trap are excellent. Checklist Week 6 rewritten to match the plan (identity weeks).

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S11–S12 rows)`
- `teaching/lecture-slides/unit-04-system-administration-slides.md`
- `teaching/speaker-notes/unit-04-system-administration-notes.md`
- `teaching/lab-workbook/module-labs/unit-04-system-administration.md`
- `modules/M12-users-groups-permissions/content/labs/README.md (existence)`
- `modules/M13-ownership-shared-access/content/labs/README.md (existence)`
- `modules/M14-sudo-root-principle/content/labs/README.md (existence)`
- `modules/M15-environment-variables/content/labs/README.md (existence)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 6 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes, sequence (identity → modes → shared design → sudo → environment), prerequisites (scripting unit), activities (decode sprints, scenario vote), demos (dir-x, sticky flip, sudo redirect, PATH shadow), labs (four clinics + MP-B), formative (exit ticket decode 2770), HW (M12–M15 quizzes, MP-B, midterm prep sheet), timing cuts (ACL shrinks), instructor notes.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S11 — identity + triplet + modes lecture | 45 | 40–45 | high — densest | SN: if behind, ACL shrinks to one sentence; labs carry depth |
| S11 — permission clinic + shared-tree lab | 30 | 30 | low | staged snapshots per pair |
| S12 — sudo + environment lecture | 40 M14 · 30 M15 | 35 + 25 | medium | drop-in demo and PATH mystery never cut (SN) |
| S12 — sudo workshop + incidents + env forensics | 20 formative/lab | 20–25 | low | incidents are ticket-style; timeboxed |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Triplet decoding, numeric modes (640/755/600), umask bases (files 666/dirs 777 reasoning), SGID inheritance, sticky 1770 — all correct.
- **FIXED:** 'System users (uid < 1000)' now states the Debian/Ubuntu convention explicitly (deck edit applied).
- `sudo cmd > file` shell-opens-the-file trap and the `sudo sh -c` recovery — correct.
- umask 077 → 600/700 → teammate cannot run — correct; `sudo -l` and drop-in policy correct; `visudo -c` proof real.

## 6. Safety review

- The unit's labs run on staged per-pair snapshots; breakage is the pedagogy, restore is the reflex (workbook safety architecture).
- sudo work uses a drop-in file, never the main sudoers; `visudo -c` is a deliverable.
- The staging note's timing typo ('beforenoon') fixed to 'the afternoon before'.

## 7. Lab review

- Clinic (30′), shared-tree (30′), sudo drop-in workshop (25′), incidents (20′), env forensics (15′) — fit S11/S12 with the SN cuts.
- Justification-per-fix grading is the strongest anti-777 device in the course — preserved.
- MP-B links verified to M13 practice challenges.

## 8. Assessment review

- M12–M15 quizzes + MP-B + midterm prep sheet — the load is real but the prep sheet *is* consolidation; no added instrument needed.
- LA-3 (W12, staged) draws from exactly these labs — alignment stated in the workbook.
- Midterm (W7) includes M12–M13 permission reasoning; the deck's preview ('Q3 previews SGID') is consistent with the midterm's umask/777 items (verified in the exam paper).

## 9. Consistency findings

- Deck ↔ SN ↔ workbook ↔ plan — aligned.
- Checklist Week 6 rewritten (was a stale 'text processing II + review' block).
- Deck's uid convention precision fix applied; no other drift.

## 10. Corrections applied

- Deck slide 2: uid<1000 convention clarified (F7).
- Workbook U4 'beforenoon' typo fixed (F8).
- Checklist Week-6 block rewritten (F3).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Staged multi-user labs on a fresh VM (staging script inspected; execution is instructor-side).
- Live sticky-flip demo timing.

## 13. Remaining risks

- S11 density — honor the ACL shrink cut.
- Students leaving S12 without a personal snapshot habit will suffer in W8's storage labs — the checklist carries the reminder.

## 14. Recommendations for the following week

- Midterm week next: verify the grading sheet print count and station staging (checklist Week 7).
- Read the midterm key BEFORE S13 (plan's instructor note says so).
- Collect the prep sheets at S13; they are allowed into the exam per the midterm rules.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
