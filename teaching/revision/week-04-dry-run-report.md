# Week 04 Dry-Run Report — Text processing: the DS superpower (M08, M09)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S7–S8** · Materials: unit-02 deck slides 9–16 · unit-02 notes §S7/S8.
> **Status: PASS WITH WARNINGS (timing density + 2 shared-artifact fixes)**

---

## 1. Executive summary

S7–S8 are the course's Data Science centerpiece (profile-before-compute, the signature pipeline, redirection). Materials are technically accurate and the truncation demo is pedagogically honest. The session-8 load is the heaviest in the unit; the SN already prescribes the correct cuts. Corrections this pass: the checklist Week-4 block (was describing scripting content) and the deck's LA-1 timing line (F5).

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S7–S8 rows)`
- `teaching/lecture-slides/unit-02-command-line-slides.md (slides 9–16)`
- `teaching/speaker-notes/unit-02-command-line-notes.md (§S7/S8)`
- `teaching/lab-workbook/module-labs/unit-02-command-line.md (rows 4–7)`
- `modules/M08-text-processing/content/labs/README.md (existence)`
- `modules/M09-pipes-and-redirection/content/labs/README.md (existence)`
- `modules/M08-text-processing/content/data/ (dataset delivery verified: server.log, access.log, transactions.csv, students.csv, sensor-telemetry.tsv, experiment.log)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 4 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (S7/S8), beginner-friendly build-one-stage-at-a-time pipeline teaching, prerequisites (W3 fluency), activities (profiling challenge, relay), demos (truncation, wrong-order uniq), labs (M08/M09), formative (predict-the-output), HW (M08 exercises, mini-project start), timing with SN cuts, instructor notes.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S7 — text core tools lecture + profiling challenge | 40 | 40 | low | the challenge is the lecture (SN) |
| S7 — M08 toolkit circuits lab | 35 | 35 | low | predict-intermediates inline |
| S8 — grep/sed/awk + redirection lecture/demo | 45 | 40 | high — densest in unit | SN: relay becomes a demo if behind; the x-y table never gets cut |
| S8 — pipeline construction + redirection drills lab | 30 | 30 | medium | mini-project becomes HW (plan) |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- sort/uniq interplay, `cut -d, -f3`, `grep -E`, sed `s///`, awk `-F, '{print $2,$4}'` — scope discipline (grep finds/sed changes/awk reports) is technically sound and correctly bounded.
- Redirection table (`> >> 2> 2>&1 < |`), truncate-before-running, `sort < f > f` corruption — all real and correctly explained.
- CRLF-in-`$2` troubleshooting pointer (SN) matches the M08 module docs.
- Dataset delivery: the labs' data ships from modules/M08-.../data/ (verified present); the workbook staging note now says so (edit applied this review — see inventory gap 1).

## 6. Safety review

- The truncation demo is run on a sacrificial file by design; the SN narrates the danger before students touch redirection.
- No elevated or network-dependent commands in W4 labs; everything is VM-local and reversible via snapshot.
- Mini-project starts on real logs with read-only analysis — safe.

## 7. Lab review

- M08 rows (toolkit circuits 30′, pipeline 35′, mini-project 45′ HW) + M09 row (25′) fit the sessions with the S8 cuts.
- The predict-each-intermediate checkpoint is the strongest evidence habit in the unit — preserved.
- Datasets present with declared dirt (datasets/STATUS.md); two pending items are documented (syslog-sample.log) — instructor substitution decision recorded in the fresh-env checklist (I3).

## 8. Assessment review

- M08/M09 quizzes + M08 mini-project = the week's graded load; aligned with outcomes.
- LA-1 lands at this unit's end (W4) — the deck's slide 16 previously said 'next week'; corrected this pass (F5).
- A1 (Organized Analyst) feeds on this unit; its window was corrected course-wide (due end of W6 — see plan/schedule fixes).

## 9. Consistency findings

- Deck slides 9–16 ↔ SN §S7/S8 ↔ workbook rows 4–7 ↔ plan S7/S8 — aligned.
- Checklist Week 4 rewritten this review (was stale scripting content) — now M08/M09-accurate.
- F5 correction applied to slide 16; SN §S8 header slide-range corrected (10–16).

## 10. Corrections applied

- Checklist Week-4 block rewritten (this review, Phase A).
- Deck slide 16 LA-1 line corrected (F5); SN session-8 header slide-range corrected.
- Workbook U2 staging note now points at the real dataset delivery path (inventory gap 1).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Execution of the profiling pipelines on a fresh VM (datasets verified present, not re-generated).
- Live relay-race timing.

## 13. Remaining risks

- S8 remains the unit's density peak — the SN cuts are the safety valve; honor them.
- Regex scope-creep is the predictable overreach; the SN's warning is the mitigation.

## 14. Recommendations for the following week

- Open S9 with yesterday's one-liners becoming scripts (the deck's designed bridge).
- Shellcheck must be present in the demo VM before S9 (SETUP.md toolchain includes it — verify on the lab image).
- Collect W4 exit tickets to seed A1's dataset section examples.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
