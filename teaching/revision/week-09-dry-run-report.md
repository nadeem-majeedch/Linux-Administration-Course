# Week 09 Dry-Run Report — Time and processes (M18, M19)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S17–S18** · Materials: unit-05 deck slides 7–13 · unit-05 notes · workbook unit-05 rows 4–7.
> **Status: PASS WITH WARNINGS (checklist realignment)**

---

## 1. Executive summary

S17 (processes/signals) and S18 (cron/timers) complete the resource unit. The signal ladder and the cron environment-trap teaching are technically correct; the deck's cron examples verify against crontab(5). Corrections landing here: the checklist Week-9 block (stale sudo/processes content) and the A2 release-week alignment (schedule corrected to match the plan's S17 release).

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S17–S18 rows; A2 release verified)`
- `teaching/lecture-slides/unit-05-software-storage-time-slides.md (slides 7–13)`
- `teaching/speaker-notes/unit-05-software-storage-time-notes.md (§S17/S18 parts)`
- `teaching/lab-workbook/module-labs/unit-05-software-storage-time.md (rows 4–7)`
- `modules/M18-processes-jobs-signals/content/labs/README.md (existence)`
- `modules/M19-scheduling-cron-timers/content/labs/README.md (existence)`
- `teaching/demonstrations/module-demos/04-processes-and-signals.md (demo verified)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 9 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (choose signals politely; scheduled jobs that log), sequence (process anatomy → jobs → signals → cron → timers), prerequisites (skeleton from W5 — explicitly reused in cron jobs), demos (trap script, unescaped %), labs (triage, signal ladder, cron trap, timer comparison), formative (exit ticket decode `30 3 * * 6`), HW (M18/M19 quizzes, backup-script scheduling).

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S17 — process anatomy + load-average lecture | 45 | 40–45 | medium | load-average computation is the DS survival skill — protect it |
| S17 — process triage + signal ladder labs | 30 | 30 | low | trap demo precedes any real kill (workbook) |
| S18 — cron/timers lecture + environment trap | 40 | 35–40 | medium | timer section compresses per SN if the lab start slips |
| S18 — cron trap lab + timer comparison | 35 | 35 | medium | trap diagnosis trio is the graded checkpoint |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- PID/PPID/states (R/S/D/Z), `ps aux`/`top`/`htop`/`pstree`, load-average vs CPU% with core-count decoding — correct.
- Signal semantics: SIGINT(2)/SIGTERM(15)/SIGKILL(9)-uncatchable/SIGHUP reload framing — correct; TERM→wait→KILL ladder sound.
- Cron: five fields, `crontab -e`, `%` escaping, environment trap (minimal PATH, no profile) — all correct; `0 4 * * 1-5` and `30 3 * * 6` verify.
- systemd timers as journald-logged alternative — correctly motivated (M20 synergy).

## 6. Safety review

- Signal teaching is explicitly ladder-disciplined: the trap demo proves KILL skips cleanup BEFORE anyone kills a real process.
- `pkill -f` proximity-fusing story (two python3s) — the aimed-weapon warning is in both deck and notes.
- Cron labs run scheduled jobs inside student VMs with explicit logging — no shared-host scheduling.

## 7. Lab review

- Triage 25′ / signal ladder 20′ / cron trap 30′ / timer comparison 15′ — fit with the SN compressions.
- The cron-trap diagnosis trio (PATH, tilde, logging) is the week's evidence checkpoint — measurable.
- Backup-script scheduling HW directly seeds W10+ habits and A2.

## 8. Assessment review

- A2 (Automated Pipeline) released S17 — plan and corrected schedule now agree (release W9, due W13).
- M18/M19 quizzes as HW; the deck's exit-ticket items are final-exam-shaped (evidence-first) — good transfer.
- The 'which mistake would you notice latest' item (unlogged cron job) previews the capstone observability rubric — consistent.

## 9. Consistency findings

- Deck slides 7–13 ↔ SN ↔ workbook rows 4–7 ↔ plan S17/S18 — aligned.
- Checklist Week 9 rewritten (was 'sudo + processes (M13, M14→M17–M18)' — stale).
- A2 release: plan S17 ↔ schedule row — now consistent (was F2-adjacent drift).

## 10. Corrections applied

- Checklist Week-9 block rewritten (F3); schedule A2 row verified against plan (F2 fix landed here).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Cron job execution on a fresh VM (environment-dependent; module lab previously syntax-audited).
- Live trap-demo timing.

## 13. Remaining risks

- Cron's environment trap is invisible until it bites — the lab inflicts it deliberately; keep the trap (don't pre-warn it away).
- Timers compress: if cut, keep the journald-logging rationale sentence (it's the W12 bridge).

## 14. Recommendations for the following week

- W10 opens services — pre-stage the broken user unit (checklist Week 10 prep).
- Six-rung ladder poster ready for S20.
- Watch A2 checkpoints: quoting/guards from W5 are its graded spine.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
