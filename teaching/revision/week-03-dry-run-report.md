# Week 03 Dry-Run Report — Terminal fluency and the filesystem (M05–M07)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S5–S6** · Materials: unit-02 deck slides 1–8 · unit-02 notes §S5/S6.
> **Status: PASS WITH WARNINGS (1 technical fix applied; otherwise aligned)**

---

## 1. Executive summary

Sessions 5–6 deliver M05 (shell/FHS/paths) and M06–M07 (files, globs, `rm` safety). The deck/notes/workbook triangle is coherent and the safety choreography (`ls`-before-`rm`) is excellent. One genuine technical defect found in the deck's knowledge check (the `~..` tilde-expansion question implies an expansion that bash does not perform) — corrected. Checklist Week 3 was already realigned in the week-2 review and was verified against the plan this pass.

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S5–S6 rows)`
- `teaching/lecture-slides/unit-02-command-line-slides.md (slides 1–8)`
- `teaching/speaker-notes/unit-02-command-line-notes.md (§S5, §S6)`
- `teaching/lab-workbook/module-labs/unit-02-command-line.md (rows 1–3)`
- `modules/M05-terminal-and-shell/content/labs/README.md (existence)`
- `modules/M06-filesystem-hierarchy/content/labs/README.md (existence)`
- `modules/M07-files-and-directories/content/labs/README.md (existence)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 3 block, realigned in week-2 review)`

## 3. Coverage audit

All 13 elements present: outcomes (plan S5/S6), beginner explanations (two-terminal path demo), sequence (navigate → mutate → safe-delete), prerequisites (Week 2 VM + snapshot), labs (M05–M07 lab indexes exist), formative (path flash-cards, glob-prediction), HW (M05–M07 quizzes, `man` exercise, organize-a-tree), timing, instructor notes (SN §S5/S6 with cuts). LA-1 is correctly framed as this unit's rehearsal.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S5 — recap + shell/terminal/console + FHS walk | 35 M05 · 35 M06 | 35 + 30 | medium — FHS walk overruns if unplanned | SN: cap the walk at 8′; drop the `cd -` delight exercise if behind, never the two-terminal demo |
| S5 — lab start (navigation drills) | 20 | 20 | low | start drills in-class, finish as HW |
| S6 — files/inodes/globs + rm safety lecture | 35 | 35 | low | inode talk capped at 3′ (SN) |
| S6 — M07 file-operations lab + glob drills | 40 | 35–40 | medium | globs drill can compress; the `ls`-first reflex demo never cuts |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Command anatomy, man synopsis reading, FHS roles, absolute/relative/`~`/`-` paths — all accurate.
- **DEFECT (fixed):** slide 6 knowledge check asks "what does `~../bin` (from your home) resolve to?" with an instructor note implying a `~/bin`-vs-`/home/bin` resolution. In bash, `~..` does not expand (no user named `..` — the tilde-prefix is left literal), so the question as posed has a different true answer than the note implies. Rewritten as a deliberate trap with the correct mechanism and note.
- `mv` = rename-and-move; `rmdir` as training wheels; hard-link `ls -li` demo — accurate.
- Environment assumptions: none beyond the Week-2 VM; no sudo, no network.

## 6. Safety review

- `rm` slide and SN treat deletion with the purpose/risk/recovery framing; the `ls`-before-glob reflex is taught before any lab uses `rm`.
- All W3 lab work is inside `~/` scratch trees in the student's own VM; no elevated commands.
- Ctrl+S/Ctrl+Q freeze recovery taught (SN) — small but real beginner safety net.

## 7. Lab review

- M05/M06/M07 lab indexes exist; durations (25′/20′/30′) fit the session mapping.
- Deliverables are evidence-based (path puzzles, found-files reasons, organized tree) — no solutions leak into student material.
- LA-1 (end of unit) verified present at assessments/lab-assessments/lab-assessment-01.md with its own rubric.

## 8. Assessment review

- M05–M07 quizzes exist per module practice dirs; plan assigns them as HW — consistent.
- Exit ticket (slide 16) — one-line pipeline: measurable and aligned with the unit's outcome.
- No answer-key exposure; quiz keys are separate files (verified in the course-wide leak scan).

## 9. Consistency findings

- Deck slides 1–8 ↔ SN §S5/S6 ↔ workbook rows 1–3 ↔ plan S5/S6 — aligned.
- Checklist Week 3 (M05–M07) — realigned in the week-2 review; re-verified against the plan this pass.
- F5 (LA-1 'next week' timing) belongs to W4's session close — see the W4 report.

## 10. Corrections applied

- Slide 6 Q2 (`~../bin`) rewritten to the technically correct trap + note (deck edit applied).
- No other W3-specific file defects; shared-artifact corrections that touch W3 (checklist Week 3) were applied and verified in the week-2 review.

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Fresh-VM execution of the navigation labs (no VM provisioned).
- Live classroom timing (estimates only; use the timing-observation sheet).

## 13. Remaining risks

- The relative-path wall remains the week's predictable pain — the SN's two-terminal demo is the mitigation; do not skip it.
- `~..` correction should be read once before teaching so the trap lands as intended.

## 14. Recommendations for the following week

- Open S7 with the '50 GB CSV on an 8 GB laptop' question — SN's designed hook for W4.
- Verify course datasets are present before S7 (M08 generator data) — W4's staging dependency.
- Print/collect the exit-ticket pipelines; the best two open Session 9.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
