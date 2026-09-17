# Week 12 Dry-Run Report — Observability and defense (M24, M25)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S23–S24** · Materials: unit-06 deck slides 9–15 · unit-06 notes · workbook unit-06 rows 8–10.
> **Status: PASS WITH WARNINGS (deck quoting fix + checklist realignment)**

---

## 1. Executive summary

S23 (journald/monitoring) and S24 (security/ufw) close the serving unit. The journalctl-as-interface teaching, the available-vs-free misread fix, and the two-terminal ufw habit are technically correct. One deck fix landed here: the `--since -1h` knowledge-check line now carries the quotes it needs. Checklist Week 12 rewritten (stale block + the M32-clinic misplacement F11).

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S23–S24 rows)`
- `teaching/lecture-slides/unit-06-services-network-security-slides.md (slides 9–15)`
- `teaching/speaker-notes/unit-06-services-network-security-notes.md (§S23/S24 parts)`
- `teaching/lab-workbook/module-labs/unit-06-services-network-security.md (rows 8–10)`
- `modules/M24-logs-journald-monitoring/content/labs/README.md (existence)`
- `modules/M25-security-firewall/content/labs/README.md (existence)`
- `teaching/instructor-resources/grading-sheets/lab-assessment-sheet.md (LA-4 support verified)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 12 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (query, don't grep; vital signs; default-deny with justification), prerequisites (W9 logging rules), demos (crash-loop forensics, memory-hog, ufw two-terminal), labs (log forensics, monitoring under load, hardening), formative (exit ticket), HW (M24/M25 quizzes, LA-4/LA-5 prep, A3 progress), SN cuts (checklist walk never cuts).

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S23 — journald + monitoring lecture | 45 | 40–45 | medium | free's available column is the decisive misread fix |
| S23 — log forensics lab (+ monitoring starts) | 25 | 25 | low | staged journal |
| S24 — security lecture + hardening checklist | 40 M24 · 35 M25 | 30 + 30 | medium | checklist walk never cuts (SN) |
| S24 — hardening lab | 30 | 30 | low | two-terminal habit before ufw enable |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- journald structure, `journalctl -u/-f/-p/--since/-n`, persistent vs volatile, the grep-raw-journal anti-pattern — correct.
- **FIXED:** deck knowledge-check line `--since -1h` now `--since "-1h"` with the shell-quoting reason (matches the M24 module docs).
- `free -h` available-vs-used, `vmstat 1` si/so, load trend — correct interpretation taught.
- ufw default-deny + justified allows, key-only SSH with rollback documented, secrets 600 outside repo — correct hardening core.

## 6. Safety review

- The ufw self-lockout is REHEARSED (second session opened before enabling) — the safest possible treatment of the riskiest student action.
- Secrets hygiene (600 env files outside the repo, never in history) is planted here and graded in the capstone.
- All firewall work is on the student's own VM; no external scanning anywhere in the unit.

## 7. Lab review

- Log forensics (25′), monitoring under load (25′), hardening (30′) — fit with the SN cuts.
- Every allow rule carrying a justification line (workbook checkpoint) is the least-privilege teaching made operational.
- LA-4's staged faults (crash-loop unit + bloated journal) verified as instructor staging in the workbook + checklist.

## 8. Assessment review

- LA-4/LA-5 windows open per the corrected schedule (W12–13); A3 progress continues — no double-heavy week.
- M24/M25 quizzes as HW; the exit-ticket items (enable vs start; refused vs timeout; why 600 on keys) are practical-exam warm-ups — consistent.
- The deck's Q2 (which rule keeps you in) is the practical exam's staged trap — verified in the practical paper's firewall task.

## 9. Consistency findings

- Deck slides 9–15 ↔ SN ↔ workbook rows 8–10 ↔ plan S23/S24 — aligned.
- Checklist Week 12 rewritten (F3 + F11: the M32 clinic is W15, not W12).

## 10. Corrections applied

- Deck slide 12: `--since "-1h"` quoting fix (F6).
- Checklist Week-12 block rewritten (F3 + F11).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- ufw rehearsal on a fresh VM (staged snapshot path verified in the checklist).
- Live memory-hog timing.

## 13. Remaining risks

- S24's checklist walk is the graded artifact's rehearsal — it cannot compress without pedagogical cost; the memory-hog demo can.
- Journal-persistence settings vary by image (volatile acceptable if documented) — the fresh-env checklist rows F8 record this.

## 14. Recommendations for the following week

- W13 opens the DS stack — stage the merge-conflict repo and rehearse the venv/Jupyter demo (checklist Week 13 prep).
- Capstone Proposal (phase 1) checkpoint lands W13 — environment choice + team roles recorded.
- Keep LA-4 staging intact for the W12–13 window.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
