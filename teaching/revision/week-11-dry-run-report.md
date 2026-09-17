# Week 11 Dry-Run Report — Remote work (M22, M23)

> **Date:** 2026-09-18 · **Course-wide review pass** (method per
> [course-wide-review-inventory.md](course-wide-review-inventory.md); Week-1/2
> standard preserved). Sessions **S21–S22** · Materials: unit-06 deck slides 6–8 · unit-06 notes · workbook unit-06 rows 4–7.
> **Status: PASS WITH WARNINGS (checklist realignment)**

---

## 1. Executive summary

S21 (SSH keys, config, TOFU) and S22 (scp/sftp/rsync + the sync circuit) are the remote-work core. Key anatomy, slash semantics, the --delete dry-run gate, and the interrupt-and-resume race are all technically correct and safely constrained to loopback. Corrections landing here: the checklist Week-11 block and the A3 release-week consistency (now released S22/W11 everywhere).

## 2. Files reviewed

- `teaching/teaching-plan/16-week-course-plan.md (S21–S22 rows; S22 A3 release verified)`
- `teaching/lecture-slides/unit-06-services-network-security-slides.md (slides 6–8)`
- `teaching/speaker-notes/unit-06-services-network-security-notes.md (§S21/S22 parts)`
- `teaching/lab-workbook/module-labs/unit-06-services-network-security.md (rows 4–7)`
- `modules/M22-ssh-remote-admin/content/labs/lab-01-key-workflow.md (existence)`
- `modules/M22-ssh-remote-admin/content/labs/lab-02-diagnosis-clinic.md (existence)`
- `modules/M23-file-transfer/content/labs/lab-01-dataset-sync-circuit.md (existence)`
- `modules/M23-file-transfer/content/labs/lab-02-transfer-automation.md (existence)`
- `teaching/setup-and-delivery/delivery-checklist.md (Week 11 block rewritten this review)`

## 3. Coverage audit

All 13 elements present: outcomes (key into own VM; choose the transfer tool), prerequisites (loopback networking from S20), demos (interrupt-and-resume race, slash-trap reveal), labs (key workflow, SSH clinic, sync circuit, transfer automation), formative (speedup interpretation), HW (M22/M23 quizzes, clinic/automation as HW), instructor staging notes.

## 4. Timing analysis

| Activity | Planned | Recommended | Risk | Proposed adjustment |
|---|---|---|---|---|
| S21 — SSH lecture (keys/TOFU/config) | 45 | 40–45 | medium | key anatomy as lock/key; host-key choreography narrated |
| S21 — key workflow lab (+ clinic as HW) | 30 | 30 | low | lab keys only, passphrase-protected |
| S22 — transfer lecture + tool selection | 40 | 35–40 | medium | the race demo is the sell — run it honestly at 200 MB |
| S22 — dataset sync circuit lab | 50 | 45–50 | medium | sacrificial --delete with dry-run gate; automation as HW |

*Estimates are analyst judgments grounded in the plan's time allocations and
the speaker notes' own pacing/cuts guidance — not observed deliveries.
Record actuals with the [timing-observation sheet](timing-observation-sheet.md).*

## 5. Technical review

- `ssh-keygen -t ed25519`, authorized_keys, ssh-agent, ssh_config Host aliases, TOFU, known_hosts alarm-on-change — correct.
- scp-vs-sftp-vs-rsync selection table; `src/` vs `src` slash semantics; `--delete` never without `--dry-run`; speedup interpretation — all correct.
- authorized_keys permission question (640 accepted; group/world-WRITE refused) — correct as posed.
- All remote work is localhost inside the student's VM — the course's loopback policy holds.

## 6. Safety review

- Lab keys are generated fresh, never personal keys (workbook safety architecture) — verified in the lab files.
- The host-key-changed choreography is planned and rehearsed with recovery — not improvised.
- The sync circuit's --delete runs on a sacrificial tree after a READ dry-run — the gate is graded language.

## 7. Lab review

- Key workflow (30′) + clinic HW; sync circuit (50′) + automation HW — heavy but the split keeps S22's core achievable.
- Both M22 lab files and both M23 lab files verified to exist with the referenced names.
- sha256-verified manifests and resume evidence are the deliverables — evidence-first.

## 8. Assessment review

- A3 releases S22 (plan; schedule corrected) — one heavy instrument per week preserved.
- M22/M23 quizzes as HW; the tool-selection scenarios (5 cards) are formative gold — aligned with outcomes.
- Deck's Q1 (authorized_keys) welds Unit 4 onto SSH — cross-unit coherence verified.

## 9. Consistency findings

- Deck slides 6–8 ↔ SN ↔ workbook rows 4–7 ↔ plan S21/S22 — aligned.
- Checklist Week 11 rewritten (F3); A3 release line now matches plan/schedule (F2/F10 closure).

## 10. Corrections applied

- Checklist Week-11 block rewritten (F3; A3 release S22 stated).

## 11. Validation results

### Executed this session (course-wide battery, consolidated in [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md))

- Relative-link resolution across every file this review corrected — 0 broken (session checker, run per phase and at the end).
- Code-fence balance on all touched files — 0 odd counts.
- MkDocs `--strict` build after all phases — exit 0.
- Leak scans (answer-key strings, key files) and nav separation — clean.
- `git status` deletion check — 0 deleted files.



## 12. Checks not run, and reasons

- SSH key workflow on a fresh VM (lab keys; environment-dependent).
- Live interrupt-and-resume race timing.

## 13. Remaining risks

- The sync circuit's 50′ is the unit's longest lab — protect it; automation becomes HW by design.
- Students reusing personal keys is the habit to break — the lab-key rule is the enforcement.

## 14. Recommendations for the following week

- W12 is observability/defense — stage the crash-looping unit + bloated journal for LA-4 (checklist Week 12 prep).
- UFW demo VM restore point (firewall-ON snapshot) before S24.
- The --delete dry-run recitation is now graded language from here to the capstone — keep reciting it.

---

*Course-wide pass note: shared artifacts (delivery checklist, assessment
schedule, 16-week plan, SETUP.md) were corrected once course-wide rather than
per week; each weekly report lists the corrections that land on its sessions.
Consolidated results: [FINAL-COURSE-WIDE-TEACHING-REVIEW.md](FINAL-COURSE-WIDE-TEACHING-REVIEW.md).*
