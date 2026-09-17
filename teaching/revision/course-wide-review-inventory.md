# Course-Wide Review Inventory — Weeks 2–16

> **Date:** 2026-09-18 · **Method:** repository inspected before any change;
> every finding below cites file evidence gathered this session. Week 2 was
> already dry-run reviewed ([week-02-dry-run-report.md](week-02-dry-run-report.md))
> and is **preserved unchanged** — its corrections are treated as the baseline.
> This inventory governs the Weeks 3–16 pass and the package-level reviews.

## 1. Week → session → module map (verified against the plan)

| Week | Sessions | Modules | Unit deck/notes | Workbook file |
|---|---|---|---|---|
| 2 ✅ reviewed | S3–S4 | M04 | unit-01 | unit-01 (reviewed) |
| 3 | S5–S6 | M05, M06, M07 | unit-02 (slides 1–8) | unit-02 |
| 4 | S7–S8 | M08, M09 | unit-02 (slides 9–16) | unit-02 |
| 5 | S9–S10 | M10, M11 | unit-03 | unit-03 |
| 6 | S11–S12 | M12–M15 | unit-04 | unit-04 |
| 7 | S13–S14 | review + **midterm** | (no deck — exam week) | — |
| 8 | S15–S16 | M16, M17 | unit-05 (S15–16) | unit-05 |
| 9 | S17–S18 | M18, M19 | unit-05 (S17–18) | unit-05 |
| 10 | S19–S20 | M20, M21 | unit-06 | unit-06 |
| 11 | S21–S22 | M22, M23 | unit-06 | unit-06 |
| 12 | S23–S24 | M24, M25 | unit-06 | unit-06 |
| 13 | S25–S26 | M26, M27 | unit-07 | unit-07 |
| 14 | S27–S28 | M28, M29 | unit-07 | unit-07 |
| 15 | S29–S30 | M31, M32 + revision | unit-08 | unit-08 |
| 16 | S31–S32 | **practical + final + viva** | — | — |

Deck/notes session splits verified: U2 S5→slides 1–6, S6→7–8, S7→9, S8→10–13;
U3/U4 two sessions each; U5 S15–18; U6 S19–24; U7 S25–28; U8 S29–30.

## 2. Teaching resources available (verified to exist)

- 30 module lab READMEs + M31 `ds-server-lab.md` + M32 four incident labs
- All referenced assessments exist: LA-1…LA-5 (`assessments/lab-assessments/`),
  A1–A3 (`assessments/assignments/`), midterm/final + keys
  (`assessments/exams/`), practical + key (`assessments/practical/`),
  capstone RUBRIC/INCIDENTS/VIVA (`projects/capstone/instructor/`)
- 10 demos, demo index with session mapping and fallbacks
- Grading sheets, attendance template, INSTRUCTOR-ONLY policy (instructor side)
- Quiz bank v2 (optional enrichment) — keys separated

## 3. Known gaps (course-wide)

| Gap | Evidence | Impact |
|---|---|---|
| `datasets/` ships only README + STATUS (delivered datasets live in `modules/M08…/data/`, 2 pending incl. `syslog-sample.log`) | `datasets/STATUS.md` | Workbook U2 staging note says "repo `datasets/` copy or lab share" — instructors must know data actually ships from M08's generator dir; documentation fix, not a content bug |
| `SETUP.md` has no Docker section | `grep -i docker SETUP.md` → 0 hits | Workbook U7 requires "Docker installed per SETUP.md (verify before S27)" — a dangling instruction until M28's own `lab-00-install.md`; **fix: add a short Docker section to SETUP.md** |
| Plan has no capstone milestone rows (Proposal/Build/Operate/Document) | `grep -i capstone 16-week-course-plan.md` → only S32 | U8 deck + rubric phase weights + schedule row "phases 1–5 across W11–W16" need anchors; **fix: add milestone notes to S25/S28/S29/S30 rows** |

## 4. Consistency issues found (findings register)

| ID | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | HIGH | **A1 due-window contradiction:** plan S10 "released — due W8" + plan S16 "A1 due this week" (W8) vs assignment spec "due end of week 6", assessment-schedule logistics "due end W6", workbook U3 "released S10, due end of week 6" | 3 artifacts say W6; the plan's two rows are the outlier |
| F2 | MEDIUM | assessment-schedule A1 row header "Week 4–7" contradicts its own logistics ("released W5; due end W6"); A3 row header "Week 14–15" contradicts "released W12" (plan: released S22 = W11) | schedule rows vs their own logistics columns |
| F3 | HIGH | **delivery-checklist Weeks 4–15 blocks describe a stale module numbering** (e.g. W4 "Scripting I (M08)" vs plan W4 = M08/M09 text processing; W6 "review" vs plan W6 = M10/M11 scripting; W9 "sudo+processes" vs plan W9 = M18/M19; W10 "packages/storage" vs plan W10 = M20/M21; W12 "services+logs+security" vs plan W12 = M24/M25; W13 "performance clinic" vs plan W13 = M26/M27; W14 "Git/Docker/transfer" vs plan W14 = M28/M29; W15 "capstone build" vs plan W15 = M31/M32 + revision) | full checklist read vs plan week list |
| F4 | MEDIUM | **End-to-end DS workflow lab misattributed:** workbook U7 row "End-to-end DS workflow · M27 · M27 lab 3" — but M27 lab 3 is "Batch Scheduling"; the end-to-end lab is **M26 lab 3** (`lab-03-end-to-end-ds-workflow.md`). Plan S26 repeats it ("M27 end-to-end lab") | M26/M27 lab listings |
| F5 | LOW | U2 deck slide 16: "LA-1 **next week**" — LA-1 lands at the end of this same unit (W4, per schedule + workbook U2) | deck S16 vs schedule row 4 |
| F6 | LOW | U6 deck slide 12: `journalctl --since -1h` needs quoting: `--since "-1h"` | M24 lesson documents quoted form |
| F7 | MEDIUM | U4 deck slide 2: "System users (uid < 1000)" stated as absolute — Debian/Ubuntu convention, not kernel law | Ubuntu passwd(5) convention |
| F8 | LOW | "beforenoon" (not a word) ×3: lab-delivery-guide.md, workbook U4, workbook U8 | grep |
| F9 | — | Withdrawn during verification: the "typo list" first recorded here was checked by grep against the source files and found to exist only in this inventory note, not in the teaching materials — no such typos were present. Only "beforenoon" (F8) was real. Recorded as a caution: findings must be grep-verified before fixing, this one was | verification grep |
| F10 | MEDIUM | Checklist W10 "Assignment 3 window opens" — A3 releases S22 (W11) per plan + schedule | plan S22 |
| F11 | MEDIUM | Checklist W12 "M32 performance clinic scheduled as the incident drill" — W12 is M24/M25; the clinic/drill is S29 (W15) | plan week list |
| F12 | LOW | U8 deck slide 8 "practical exam = 6 faults, 12 tasks; final Sections A–D" — **verified correct** (practical has T1–T12 across 4 parts + 6 planted faults; final has Sections A–D) | practical-exam.md, final.md |
| F13 | LOW | Capstone rubric table in U8 deck slide 3 verified **line-accurate** vs RUBRIC.md (all 10 areas + points) | RUBRIC.md lines 26–35 |
| F14 | LOW | U8 workbook M31 lab "2 sessions" duration — intentional (two-actor lab spans S29–S30 prep); documented, not an error | ds-server-lab.md exists |

## 5. Environment-dependent checks (planned treatment)

- All Week 2–16 lab commands: verified by **inspection** against in-repo
  module labs (which were execution-audited in the pre-publication QA);
  no fresh VM provisioned this session → environment-dependent behavior
  (installer screens, `wsl --shutdown`, Docker pulls, systemd user-unit
  lingering) marked **NOT RUN** in the final report.
- Commands requiring elevation found only inside student-VM contexts
  (apt, ufw, user staging) — appropriate and already guarded in module labs.

## 6. Planned corrections (phased)

- **Phase A (W3–4):** F5 (LA-1 timing line); U2-side checklist W3/W4 rewrite (part of F3)
- **Phase B (W5–8):** F1 (plan A1 rows), F2 (schedule row headers), F4 (plan S26 + workbook U7 lab target), checklist W5–W8 rewrite
- **Phase C (W9–12):** F6, F7, F8, F9, checklist W9–W12 rewrite (incl. F10, F11)
- **Phase D (W13–16):** checklist W13–W15 rewrite with capstone milestones; SETUP.md Docker section (gap 2); plan capstone milestone notes (gap 3); datasets note in workbook U2 (gap 1)
- **Package documents:** fresh-environment verification checklist, timing observation sheet, session-deck splitting recommendation, printable workbook recommendation, CLO evidence packet plan
- **Reports:** week-03…week-16 individual reports, FINAL-COURSE-WIDE-TEACHING-REVIEW.md

## 7. Validation strategy

After each phase: link + fence check on touched files → after all phases:
full link scan of `teaching/`, `bash -n` on extracted bash blocks, anchor
spot-checks, MkDocs strict build, nav/leak/secret scans, `git status`
deletion check (target: 0). All results reported as executed/inspection/NOT-RUN.
