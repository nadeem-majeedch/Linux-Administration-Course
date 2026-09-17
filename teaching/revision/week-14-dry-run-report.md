# Week 14 Dry-Run Report — Containers and serving (M28, M29)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S27–S28** · Materials: unit-07 deck slides 7–12 · unit-07 notes · workbook unit-07 rows 5–8.
> **Status: PASS WITH WARNINGS (SETUP gap closed + Build milestone anchored)**

---

## 1. Executive summary

S27 (Docker) and S28 (nginx/PostgreSQL) complete the DS stack. Container/kernel-sharing, volume persistence, the 502-log reading, and the restore-test rule are technically correct. The week's gap closed: SETUP.md now has the Docker section the workbook's staging note assumed (with the M28 lab-0 as the authoritative path). Capstone Build checkpoint anchored to S28's HW.

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S27–S28 rows; Build milestone added)`
- `teaching/lecture-slides/unit-07-data-science-stack-slides.md (slides 7–12)`
- `teaching/speaker-notes/unit-07-data-science-stack-notes.md (§S27/S28 parts)`
- `teaching/lab-workbook/module-labs/unit-07-data-science-stack.md (rows 5–8)`
- `modules/M28-docker-containers/content/labs/README.md (existence)`
- `modules/M28-docker-containers/content/labs/lab-00-install.md (existence)`
- `modules/M29-web-servers-databases/content/labs/README.md (existence)`
- `SETUP.md (Docker section added this review)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 14 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (run/build containers; serve data; load/dump a DB), prerequisites (M17 mounts, M13 ownership, M20 verbs — explicitly reused), demos (Jupyter-in-container, 502-log, pg_dump round-trip), labs (first containers, build/compose, nginx serve, \copy+dump), formative (image-vs-container round; request-path tracing), HW (M28/M29 quizzes, Build checkpoint), SN cuts (reverse-proxy theory compresses).

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S27 — containers lecture (VMs vs images/layers/volumes) | 45 | 40–45 | medium | kernel-sharing explains startup speed — the hook |
| S27 — first containers lab (+ build/compose HW) | 30 | 30 | low — Docker fallback exists | non-Docker path announced before the session |
| S28 — serving lecture (nginx + PostgreSQL) | 40 | 35–40 | medium | 502-log reading is the transfer moment — protect it |
| S28 — nginx serve + \copy/dump labs | 35 | 35 | medium | restore-test proven live |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- VM-vs-container model (namespaces/cgroups conceptual), image/layer caching, `docker run -p/-v`, Compose basics — correct.
- nginx server blocks, `/etc/nginx/`, logs; `\copy table FROM 'file.csv' CSV HEADER`; `pg_dump db > dump.sql` + restore-test — correct.
- **Gap fixed:** SETUP.md gained the Docker section (docker.io install, docker group + logout note, WSL2 pointer to M28 lab 0) — the workbook's 'Docker installed per SETUP.md' instruction now resolves.
- Volume-permission gotcha (M13 verbs) — correctly surfaced as the classic cohort failure.

## 6. Safety review

- `docker system prune` caution (SN) and the docker-group-is-root-equivalent note (SETUP.md, framed as an M25 discussion) — honest privilege framing.
- Container-rm data-loss demo runs WITH a mount deliberately — the save moment is witnessed (checklist + SN).
- DB credentials in 600 env files outside the repo — the M25 rule applied (workbook safety architecture).

## 7. Lab review

- First containers (30′), build/compose (30′ HW), nginx (25′), \copy+dump (30′) — fit with the fallback path keeping S27 safe for non-Docker rooms.
- M28 lab 0 (install) verified to exist — the SETUP.md section points to it as authoritative.
- The restore-verification checkpoint (not just the dump) is the capstone's backup rubric line in miniature — preserved.

## 8. Assessment review

- M28/M29 quizzes as HW; capstone Build (phase 2) checkpoint anchored at S28's HW (plan edit applied — rubric areas 1–4 evidence).
- A3 (remote operator) continues — due W15; no new instrument this week (cadence principle holds).
- Deck's Q3 ('when is the backup real?') matches the final exam's backup reasoning item — verified against the final paper's design section.

## 9. Consistency findings

- Deck slides 7–12 ↔ SN ↔ workbook rows 5–8 ↔ plan S27/S28 — aligned.
- Checklist Week 14 rewritten (F3) with the Build checkpoint (gap 3).
- SETUP.md ↔ workbook ↔ M28 lab 0 — the Docker instruction chain now resolves end-to-end.

## 10. Corrections applied

- SETUP.md Docker section added (inventory gap 2).
- Plan S28 HW: Build milestone line added (gap 3).
- Checklist Week-14 block rewritten (F3).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- Docker pull/run on this session's host (no container runtime exercised; H-row checks prepared in the fresh-env checklist).
- nginx/PostgreSQL labs on a fresh VM.
- Live 502 demo timing.

## 13. Remaining risks

- Docker-on-the-room is the week's binary risk — the fallback path (workbook) and the pre-pulled images (checklist) are the mitigations; verify both before S27.
- Volume-permission failures will happen — treat them as the M13 rehearsal they are (SN's framing).

## 14. Recommendations for the following week

- W15 is the DS server + drills — verify drill scripts on the lab image the afternoon before S29 (typo fixed earlier this review).
- A3 due S29; Operate checkpoint graded live in S29.
- Rubric self-assessment exercise (deck S3) collected at S29's brief.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
