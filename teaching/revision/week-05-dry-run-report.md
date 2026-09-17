# Week 05 Dry-Run Report — Scripting (M10, M11)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S9–S10** · Materials: unit-03 deck · unit-03 notes · workbook unit-03.
> **Status: PASS WITH WARNINGS (A1 window fixed course-wide)**

---

## 1. Executive summary

S9–S10 convert fluency into responsibility (guarded, idempotent scripts). The deck's skeleton and the `${1:?}` guard teaching are technically correct and well-sequenced; the SN's timing cuts are explicit. Course-wide corrections that land on this week: the A1 due-window contradiction (F1) was resolved in the plan and schedule (due end of W6), and the checklist Week-5 block was rewritten to match M10/M11.

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S9–S10 rows; S10 HW line corrected)`
- `teaching/lecture-slides/unit-03-scripting-automation-slides.md`
- `teaching/speaker-notes/unit-03-scripting-notes.md`
- `teaching/lab-workbook/module-labs/unit-03-scripting-automation.md`
- `modules/M10-bash-scripting/content/labs/README.md (existence)`
- `modules/M11-advanced-shell-automation/content/labs/README.md (existence)`
- `assessments/assignments/assignment-1-organized-analyst.md (A1 window)`
- `teaching/teaching-plan/assessment-schedule.md (A1 row corrected)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 5 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (debug with `bash -x`, idempotent automation), sequence (anatomy → quoting → exit codes → control flow → skeleton → debugging → patterns), prerequisites (W4 pipelines), activities (spot-the-bug, skeleton recitation), demos (guard, quoting, trace, set-e trap), labs (M10 lab 1/2, M11 bench), formative (exit-code quiz), HW (Mini-Project A, A1 release), timing cuts, SN guidance.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S9 — scripting core lecture (anatomy→control flow) | 45 | 40–45 | high | SN: the lab MUST start by 50′; cut S7-Q3 pair prediction if behind |
| S9 — first guarded scripts lab | 30 | 30 | low | guards + shellcheck clean as the release bar |
| S10 — functions/skeleton + live debug demo | 40 | 35 | medium | never cut the live debug (SN) — it's the transferable skill |
| S10 — fix-the-bug set + automation bench lab | 35 | 35–40 | medium | 8 scripts × diagnosis lines; bench can spill to HW |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Skeleton `set -euo pipefail`, `${1:?usage}`, `chmod u+x`, `[[ ]]` over `[ ]`, `while read -r`, `case` — all correct bash.
- The `|| true` set-e exemption (deck S7 + SN) is accurately stated — a common teaching error avoided here.
- Idempotency framing (append-vs-rewrite, run-thrice demo) is technically sound.
- shellcheck availability: present in SETUP.md's course toolchain (verified); workbook's 'shellcheck clean' bar is executable as written.

## 6. Safety review

- No destructive operations in W5 labs; the fix-the-bug scripts ship broken-on-purpose in the module and run in student VMs.
- The `rm -rf "$TARGET/"` unset-variable question (deck S6) is exactly the right safety thought experiment — guarded by `set -u` in the skeleton.
- Automation bench: per-file logs + failure isolation — safe batch patterns taught before cron (W9).

## 7. Lab review

- M10 lab 1 (guarded scripts 30′) and lab 2 (fix-the-bug 45′) + M11 bench (30′) — achievable with the SN cuts.
- Diagnosis-line grading ('quoting: $f splits on spaces' beats 'fixed it') — excellent, evidence-based.
- Mini-Project A links verified to M10 practice challenges.

## 8. Assessment review

- A1 due window: the three-way contradiction (plan W8 vs spec/schedule/workbook W6) was resolved this review — plan S10 now says 'released — due end of week 6', matching the assignment spec, schedule row (5–6), and workbook U3.
- A1's script section grading the skeleton + guards (workbook 'After this unit') matches the assignment spec's emphasis.
- M10/M11 quizzes assigned as HW; keys instructor-side (leak scan clean).

## 9. Consistency findings

- Deck ↔ SN ↔ workbook ↔ plan — aligned; the only drift was the A1 window (fixed course-wide).
- Checklist Week 5 rewritten this review (stale block described text-processing content).
- SN §'Sessions 9–10 overview' correctly references A1's release at S10.

## 10. Corrections applied

- Plan S10 HW line: 'due W8' → 'due end of week 6' (F1).
- Plan S15 HW line: 'A1 due this week' → pointer to the schedule (F1).
- Assessment-schedule A1 row header 'Week 4–7' → '5–6' (F2).
- Checklist Week-5 block rewritten (F3).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Execution of the fix-the-bug scripts (module-shipped; syntax-validated in the earlier QA battery).
- Live skeleton-recitation timing.

## 13. Remaining risks

- S9 lecture-heavy overrun is the known risk — the 50-minute lab-start rule is the mitigation.
- Students who skip the skeleton memorization pay for it in A1 and M19/M23 — the recitation exists for a reason.

## 14. Recommendations for the following week

- Open S11 with the shared-machine question (U4's designed hook).
- Stage demo users demo1/demo2 for W6's shared-dir work (checklist Week 6 prep).
- A1 checkpoints: review drafts mid-W6, due end of W6 (now unambiguous everywhere).

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
