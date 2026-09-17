# Week 13 Dry-Run Report — The Data Science stack (M26, M27)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S25–S26** · Materials: unit-07 deck slides 1–6 · unit-07 notes · workbook unit-07 rows 1–4.
> **Status: PASS WITH WARNINGS (end-to-end lab retarget + Proposal milestone anchored)**

---

## 1. Executive summary

S25 (Git) and S26 (Python/Jupyter) install the profession on the machine. The pointer-model teaching, the venv/PATH mechanism resolution, and the tunnel demo are technically correct. The week's key fix was the end-to-end lab misattribution (F4): the lab is M26 lab 3, not M27 lab 3 — plan and workbook now point at the real file. Capstone Proposal milestone anchored to S25's HW.

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S25–S26 rows; Proposal milestone added)`
- `teaching/lecture-slides/unit-07-data-science-stack-slides.md (slides 1–6)`
- `teaching/speaker-notes/unit-07-data-science-stack-notes.md (§S25/S26 parts)`
- `teaching/lab-workbook/module-labs/unit-07-data-science-stack.md (rows 1–4, M26-lab-3 retarget applied)`
- `modules/M26-git-dev-workflows/content/labs/lab-01-version-your-work.md (existence)`
- `modules/M26-git-dev-workflows/content/labs/lab-02-break-repair-clinic.md (existence)`
- `modules/M26-git-dev-workflows/content/labs/lab-03-end-to-end-ds-workflow.md (existence + title verified)`
- `modules/M27-python-jupyter-data/content/labs/README.md (existence)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 13 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (clean history; pinned env; Jupyter-as-service), prerequisites (M15 PATH mystery, M22 keys, M20 verbs — all explicitly reused), demos (merge conflict, which-python3, tunnel), labs (version-your-work, break-repair, end-to-end, env drills), formative (which-environment round), HW (M26/M27 quizzes, A2 due S26), SN timing guidance.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S25 — Git model + hygiene lecture | 45 | 40–45 | medium | pointer-vs-copy is load-bearing — spend the time (SN) |
| S25 — version-your-work lab (+ break-repair HW) | 30 | 30–45 | low | clean-graph deliverable |
| S26 — Python/Jupyter lecture + demos | 40 | 40 | high — dense | SN: nbconvert is the cuttable slice; never the which-python3/tunnel demos |
| S26 — end-to-end DS workflow lab (M26 lab 3) + env drills | 35 | 40–50 | high | the centerpiece; env drills compress to spot-checks if needed |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- Commit-as-pointer, branch-as-label, `.gitignore` policy, SSH remotes vs HTTPS tokens, `git config` identity — correct.
- venv lifecycle, `python3 -m pip` rationale (right interpreter's pip; shebang shadowing), pinned requirements, `which python3`/`type -a` — correct.
- Jupyter as a supervised server (ports/logs/kernels), tunnel = port forwarding, nbconvert batch — correct.
- **FIXED (F4):** 'End-to-end DS workflow' retargeted from M27 lab 3 (actually 'Batch Scheduling') to M26 lab 3 ('The End-to-End Data Science Workflow on Linux' — title verified); plan S26's lab pointer corrected likewise.

## 6. Safety review

- System python is untouchable — the `externally-managed-environment` message is taught as protection (workbook safety architecture).
- Datasets never enter Git; secrets never in history — the deck's mistake slide names the irreversible ones (pushed secrets/history rewrite).
- All labs VM-local; the tunnel reaches the student's own VM only.

## 7. Lab review

- M26 lab 1 (45′) + lab 2 HW; end-to-end (50′) + env drills (20′) — the S26 load is the unit's heaviest; the SN cuts + env-drill compression keep it feasible.
- The three-suspects diagnosis (wrong env / wrong kernel / not-installed-here) is the checkpoint that proves venv fluency.
- M27 lab 3 (batch scheduling) is NOT lost — it returns in W14/A2 context; the workbook row now says what each lab actually is.

## 8. Assessment review

- A2 due S26 (plan; schedule agrees) — the unit's own labs are its rehearsal.
- M26/M27 quizzes as HW; capstone Proposal (phase 1) milestone anchored at S25's HW (plan edit applied).
- Deck's Q3 (no listener on 8888) deliberately reuses the W10 rung logic — cross-unit transfer verified.

## 9. Consistency findings

- Deck slides 1–6 ↔ SN ↔ workbook rows 1–4 ↔ plan S25/S26 — aligned after the F4 retarget.
- Checklist Week 13 rewritten (F3) and now carries the Proposal checkpoint (gap 3 closure).

## 10. Corrections applied

- Plan S26 lab pointer → M26 lab 3 (F4).
- Workbook U7 end-to-end row + session mapping → M26 lab 3 (F4).
- Plan S25 HW: Proposal milestone line added (gap 3).
- Checklist Week-13 block rewritten (F3).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- venv + Jupyter + tunnel on a fresh VM (H/G checklist rows prepared for the pre-term pass).
- Live merge-conflict demo timing.

## 13. Remaining risks

- S26 is the unit's density peak — protect the two never-cut demos (which-python3, tunnel).
- Students who skipped M15 will wobble at PATH shadows — route them to the M27 troubleshooting page (SN's routing).

## 14. Recommendations for the following week

- W14 is containers/serving — verify Docker on lab images (checklist Week 14 prep; SETUP.md now has the Docker section).
- Non-Docker fallback path announced before S27.
- PostgreSQL + nginx present on lab images for S28.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
