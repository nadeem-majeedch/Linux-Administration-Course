# Week 08 Dry-Run Report — Software and storage (M16, M17)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S15–S16** · Materials: unit-05 deck slides 1–6 · unit-05 notes · workbook unit-05 rows 1–3.
> **Status: PASS WITH WARNINGS (A1 residue fix + checklist realignment)**

---

## 1. Executive summary

S15 (apt lifecycle + df/du triage) and S16 (loopback disk lifecycle) are the resource-stewardship core. The df/du contradiction teaching and the loopback safety architecture are technically correct and well-guarded. Corrections landing here: the plan's S15 A1 pointer (F1 residue) and the checklist Week-8 block (stale users/permissions content).

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S15–S16 rows; S15 HW line corrected)`
- `teaching/lecture-slides/unit-05-software-storage-time-slides.md (slides 1–6)`
- `teaching/speaker-notes/unit-05-software-storage-time-notes.md (§S15/S16 parts)`
- `teaching/lab-workbook/module-labs/unit-05-software-storage-time.md (rows 1–3)`
- `modules/M16-package-management/content/labs/README.md (existence)`
- `modules/M17-storage-and-filesystems/content/labs/README.md (existence)`
- `teaching/demonstrations/module-demos/09-storage-and-backups.md (loopback demo, fallback verified)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 8 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (lifecycle verbs, fstab field-by-field), prerequisites (snapshot habit from W2 — explicitly used), demos (apt negotiation, loopback lifecycle, df/du), labs (apt drills, triage, loopback 40′), formative (fstab field quiz), HW (M16/M17 quizzes, loopback documentation), SN timing cuts (source-install slide becomes reading).

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S15 — apt lifecycle + repos/PPA trust lecture | 40 M16 | 35–40 | medium — two modules | SN: cut the source-install concept slide to reading if behind |
| S15 — df/du/lsblk triage (M17 part 1) | 30 M17 | 30 | low | the contradiction is planted, not solved — by design |
| S16 — filesystems lecture (mkfs/mount/fstab) | 30 | 30 | low | loopback safety framing 60″ (SN) |
| S16 — loopback disk lifecycle lab | 45 | 45 | medium | umount-busy beat is expected — diagnose live (SN) |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- apt update/upgrade distinction, sources.list.d, PPA trust framing, `apt policy` — correct for Ubuntu.
- `lsblk`/`df -h`/`du -sh`, deleted-but-open explanation, `lsof +L1` mention — correct.
- fstab six fields, `nofail`, pass-order rationale — correct; mkfs.ext4 on loopback properly destructive-flagged.
- Quiz item `0 4 * * 1-5` (W9 deck) verified — cron fields correct in this unit's materials.

## 6. Safety review

- The unit's headline safety architecture: mkfs on loopback ONLY; the four-line rule recited at the lab brief (workbook).
- Snapshot before apt labs announced as ritual (workbook) — a broken half-removal is a restore, not a crisis.
- Demo 09 carries medium risk with a recording fallback (demo index) — verified.

## 7. Lab review

- apt drills 20′ / triage 20′ / loopback 40′ — fit the sessions; loopback is S16's centerpiece as designed.
- 100 MB loopback images staging verified in checklist + infrastructure item.
- Deliverables (format→mount→write→fstab→remount transcript) are evidence-first.

## 8. Assessment review

- M16/M17 quizzes as HW; A2 window opens S17 (W9) per the corrected schedule — no double-heavy week.
- The A1 due-date residue in plan S15 was corrected this review (pointer to the schedule instead of a wrong week).

## 9. Consistency findings

- Deck slides 1–6 ↔ SN ↔ workbook rows 1–3 ↔ plan S15/S16 — aligned.
- Checklist Week 8 rewritten (was 'Users & permissions (M10–M12)' — stale).

## 10. Corrections applied

- Plan S15 HW: 'A1 due this week' → schedule pointer (F1 completion).
- Checklist Week-8 block rewritten (F3).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Loopback lifecycle on a fresh VM (module lab was syntax-audited in the pre-publication QA; not re-executed here).
- apt install on a live network (environment-dependent).

## 13. Remaining risks

- The umount-busy teaching beat depends on a student shell being the cause — happens naturally; do not fake it.
- Stale package lists can make apt drills noisy — `apt update` first is already the labs' first step.

## 14. Recommendations for the following week

- W9 opens with signals (trap demo rehearsed — checklist Week 9 prep).
- Crontab sandboxes on lab VMs before S18.
- A2 releases S17 — announcement ready.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
