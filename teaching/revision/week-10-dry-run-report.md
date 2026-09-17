# Week 10 Dry-Run Report — Services and networks (M20, M21)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S19–S20** · Materials: unit-06 deck slides 1–5 · unit-06 notes · workbook unit-06 rows 1–3.
> **Status: PASS WITH WARNINGS (checklist realignment + A3 window fix)**

---

## 1. Executive summary

S19 (systemd) and S20 (networking) open the serving unit. The enable-vs-start distinction, the refused-vs-timeout hinge, and the six-rung ladder are technically sound; the http.server `ss` demo is safe and memorable. Corrections landing here: the checklist Week-10 block (stale packages/storage content, plus the A3-window error F10).

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S19–S20 rows)`
- `teaching/lecture-slides/unit-06-services-network-security-slides.md (slides 1–5)`
- `teaching/speaker-notes/unit-06-services-network-security-notes.md (§S19/S20 parts)`
- `teaching/lab-workbook/module-labs/unit-06-services-network-security.md (rows 1–3)`
- `modules/M20-systemd-services/content/labs/README.md (existence)`
- `modules/M21-networking-fundamentals/content/labs/README.md (existence)`
- `modules/M21-networking-fundamentals/content/labs/lab-01-local-network-lab.md (existence)`
- `modules/M21-networking-fundamentals/content/labs/lab-02-diagnosis-clinic.md (existence)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 10 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (supervise services; run the ladder), prerequisites (user-units ground from W12's env unit), activities (ladder worksheet), demos (broken ExecStart, ss grow/shrink), labs (unit lifecycle, local network lab, diagnosis clinic), formative (rung identification), HW (M20/M21 quizzes), instructor notes with the no-slack warning.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S19 — systemd units/verbs lecture + status reading | 45 | 40–45 | medium | enable≠start drawn as two graphs — never cut (SN) |
| S19 — unit lifecycle + failure triage lab | 30 | 30 | low | staged broken unit; journal evidence |
| S20 — networking lecture (layers/ports/sockets) | 45 | 40 | medium — no slack by design | tcpdump mention compresses to one sentence per SN |
| S20 — local network lab + diagnosis clinic | 25 + 25 | 40–45 combined | medium | pairs; rung ORDER is graded (workbook) |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Unit states, `systemctl status` fields, `enable --now`, user units without root — correct.
- MAC vs IP vs DNS layering, `/24` mask, loopback 127.0.0.1, DHCP/DHCP-vs-static — correct.
- `ss -tlnp`, well-known ports (22/80/443/5432/8888), refused=reachable-vs-timeout — correct and diagnostically framed.
- All network labs loopback-only — the course safety policy, stated as policy (workbook).

## 6. Safety review

- Loopback-only is enforced everywhere in W10's labs; no external hosts, no scanning.
- The checklist now carries the explicit 'no external scanning — say it' line (rewritten this review).
- User-unit work needs no root — privilege discipline consistent with the course's sudo posture.

## 7. Lab review

- Unit lifecycle (30′), local network (25′), diagnosis clinic (25′) — fit S19/S20 with the SN compression note.
- Rung-order grading ('right conclusion, wrong order scores half') — the best diagnostic-reasoning rubric in the course.
- Lab links verified to M21's two named lab files.

## 8. Assessment review

- M20/M21 quizzes HW; A2 checkpoints this week (checklist) — aligned with the corrected schedule.
- Deck Q3 ('ss shows nothing on 8888 — is it network?') is the transfer item the practical exam reuses — consistent.

## 9. Consistency findings

- Deck slides 1–5 ↔ SN ↔ workbook rows 1–3 ↔ plan S19/S20 — aligned.
- Checklist Week 10 rewritten (F3) including the A3-window fix (F10: A3 releases W11, not W10).

## 10. Corrections applied

- Checklist Week-10 block rewritten (F3 + F10).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- http.server + ss demo on a fresh VM (read-only verification only).
- Live clinic timing with planted faults.

## 13. Remaining risks

- Six sessions with no slack (U6) — S20 is the first squeeze point; the tcpdump compression is the valve.
- Students will debug networking when no listener exists — the deck's Q3 is the vaccine; run it as a poll.

## 14. Recommendations for the following week

- W11 is remote work — rehearse the loopback SSH self-connection and the host-key-changed choreography (checklist Week 11 prep).
- A3 releases S22 — brief ready.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
