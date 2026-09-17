# CLO × Assessment Alignment Matrix

> **Status: PROPOSED for instructor review.** No institutional CLO set
> was supplied with this repository; the CLOs below are *derived* from
> the module learning objectives actually written in
> [COURSE-ROADMAP.md](../COURSE-ROADMAP.md) and the module READMEs,
> then grouped to the seven learning areas the course demonstrably
> teaches. They are offered as the course's proposed CLOs for
> curriculum-committee review — nothing here claims institutional
> approval. Companion documents: [CLO-MAPPING-MATRIX.md](CLO-MAPPING-MATRIX.md)
> (module × CLO grid) · [ACCREDITATION-ONE-PAGER.md](ACCREDITATION-ONE-PAGER.md).

---

## 1. Proposed Course Learning Outcomes

On successful completion of this course, a student will be able to:

| CLO | Statement (action verb → evidence) | Bloom level | Source evidence in course |
|---|---|---|---|
| **CLO-1** | Use the Linux command line, filesystem hierarchy, and text-processing toolchain (grep/sed/awk/sort/pipelines) to inspect, navigate, and transform files and datasets. | Apply / Analyze | Unit 2 objectives (M05–M09); M08 pipeline thesis; [Lab assessments LA-1, LA-2](../assessments/lab-assessments/README.md) |
| **CLO-2** | Write and debug robust Bash scripts with guards, logging, and safe error handling to automate recurring data and administration tasks. | Create / Evaluate | Unit 3 objectives (M10–M11); Mini-Projects A/B; [Assignment 2](../assessments/assignments/assignment-2-automated-pipeline.md) |
| **CLO-3** | Administer users, groups, permissions, and shared access on a multi-user Linux system using least-privilege principles. | Apply / Evaluate | Unit 4 objectives (M12–M14); Mini-Project B (shared dataset server); LA-3 |
| **CLO-4** | Manage system software, storage, services, and scheduling with `apt`, disks/filesystems, `systemd`, and cron/systemd timers. | Apply | Unit 5 objectives (M16–M19); Assignment 2; final exam Units 4–7 coverage |
| **CLO-5** | Configure and diagnose networking, SSH-based remote administration, and secure file transfer; apply host firewall and SSH hardening practices. | Apply / Analyze | Unit 6 objectives (M20–M25, incl. M23 transfer); Mini-Project D; LA-4/LA-5 |
| **CLO-6** | Operate and troubleshoot a running Linux system: read logs (journald, /var/log), monitor resources, and follow a systematic evidence-first incident methodology. | Analyze / Evaluate | M24 + M32-clinic methodology (8-step); Drill Book incidents; final exam Section B |
| **CLO-7** | Deliver Data Science work on Linux: manage Python environments and Jupyter, use Git, containerize workloads, and operate a reproducible, backed-up, documented DS server. | Create / Evaluate | Unit 7 objectives (M26–M29), M31 DS server, Level-5 lab, capstone |

**Derivation note.** These seven CLOs are a *grouping* of the ~30
module-level objective sets already in the roadmap; no module content
was written or altered to fit them. Where a module objective did not
map cleanly to a CLO (e.g., M01's conceptual "explain what Linux is"),
it is treated as *enabling knowledge* under CLO-1 rather than forced
into an outcome of its own.

---

## 2. Alignment matrix — CLO → evidence

Legend: **I** = Introduced · **P** = Practiced · **A** = Assessed ·
**C** = Demonstrated through capstone. Every cell names the *actual*
artifact; empty means the course does not currently claim that
coverage (flagged in §4 rather than fabricated).

| CLO | Modules (introduce → practice) | Quizzes | Lab activities | Assignments / mini-projects | Exams | Capstone evidence |
|---|---|---|---|---|---|---|
| **CLO-1** CLI, filesystem, text processing | M05–M09 (P), M02/M01 context | per-module quizzes M01–M09 ([index](../assessments/quizzes/README.md)) | [Labs L1–L2](../labs/README.md); module labs M05–M09; [LA-1](../assessments/lab-assessments/lab-assessment-01.md), LA-2 | [A1 Organized Analyst](../assessments/assignments/assignment-1-organized-analyst.md) | [Midterm](../assessments/exams/midterm.md) Sections A–C | pipeline log triage (rubric areas 1, 6, 9) |
| **CLO-2** Bash scripting & automation | M10–M11 | quizzes M10, M11 | M10 fix-the-bug lab; [L3 Automation Bench](../labs/README.md) | A2 (pipeline script); Mini-Projects A, B | Final Section C (design); midterm scripting items | scheduled pipeline + `health.sh` (areas 1, 6) |
| **CLO-3** Users, groups, permissions | M12–M14, M13 shared access | quizzes M12 ([exemplar](../assessments/quizzes/quiz-m12.md)), M13, M14 | M12/M13 permission repair labs; [LA-3](../assessments/lab-assessments/lab-assessment-03.md) | A1 (permissioning task); Mini-Project B | Midterm (Unit 4 is *not* in midterm scope — assessed via LA-3 + final) | permission matrix vs `namei -l` reality (area 5) |
| **CLO-4** Packages, storage, services, scheduling | M16–M19 | quizzes M16–M19 | storage loopback lab; cron-environment trap lab (L3); M20 unit labs | A2 (systemd + cron coverage) | Final Section A/B | storage design + scheduled runs (areas 1, 2); DB via `\copy` |
| **CLO-5** Networking, SSH, transfer, firewall | M20–M25, M23 transfer | quizzes M21–M25, M23 | M21 local network lab; M22 key workflow + clinic; M23 sync circuit; [LA-5](../assessments/lab-assessments/lab-assessment-05.md) | [A3 Remote Operator](../assessments/assignments/assignment-3-remote-operator.md); Mini-Project D | Final (SSH/security sections) | SSH key-only + ufw minimal with evidence (area 5) |
| **CLO-6** Logs, monitoring, incident method | M24, M32-clinic, M18 signals | quizzes M18, M24, M32 | monitoring-under-load lab; [Drill Book incidents](../modules/M32-linux-performance-troubleshooting/README.md); LA-4 | A3 (log/monitoring coverage) | Final Section B (evidence diagnosis) | incident report, 8-step method with quoted evidence (area 9); "what happened at 02:00?" test (area 6) |
| **CLO-7** DS stack: Python/Jupyter, Git, Docker, reproducibility | M26–M29, M31 | quizzes M26–M29 | [L5 DS Server](../labs/level-5-ds-server.md); M27 end-to-end lab; M28 container labs | A3 (Python envs, Git, Docker) | Final (Python/Jupyter/Git/Docker sections) | pinned env, provenance sidecar, restore drill, fresh-clone rebuild (areas 3, 7, 8) |

---

## 3. Assessment coverage summary

Actual instruments in the repository (counts verified by execution):

| Instrument | Count / scope | Where | CLOs primarily assessed |
|---|---|---|---|
| Per-module quizzes | 30 student quizzes (~620 questions), M01–M32 | `modules/*/content/practice/quiz.md` (+ instructor keys) | all, module-aligned |
| Lab assessments LA-1…LA-5 | 5 graded circuits, 10 pts each | [assessments/lab-assessments/](../assessments/lab-assessments/README.md) | CLO-1, 2, 3, 5, 6, 7 |
| Assignments | 3 (A1/A2/A3), 5% each | [assessments/assignments/](../assessments/assignments/README.md) | CLO-1/3 (A1); CLO-2/4 (A2); CLO-5/6/7 (A3) |
| Midterm | 2 h, 100 pts, Units 1–3 (M01–M13) | [assessments/exams/midterm.md](../assessments/exams/midterm.md) | CLO-1, 2, 3 |
| Final | 3 h, 100 pts, Units 4–7 (M14–M31) | [assessments/exams/final.md](../assessments/exams/final.md) | CLO-2, 4, 5, 6, 7 |
| Practical exam | 90 min, staged 6-fault server | [assessments/practical/practical-exam.md](../assessments/practical/practical-exam.md) | CLO-4, 5, 6 (method under pressure) |
| Capstone | 5-phase project, 100-pt rubric + viva | [projects/capstone/instructor/RUBRIC.md](../projects/capstone/instructor/RUBRIC.md) | all seven (C = capstone column) |

**Weighting note.** The repository documents midterm 20% / final 25% /
practical 15% / assignments 15% (3 × 5%) / capstone per its own rubric
phase weights. Any institutional weighting reconciliation is a
committee decision, not a repository fact.

---

## 4. Gaps and coverage caveats (honest inventory)

Flagged rather than papered over:

1. **CLO-3's midterm coverage is partial by design.** Midterm scope
   ends at M13, so `sudo` policy (M14) is assessed by quiz + LA-3 +
   final only. Acceptable, but reviewers should know the midterm does
   not touch M14.
2. **CLO-1 has no dedicated *final-exam* section** — by design the
   final targets Units 4–7; CLO-1's terminal assessment happens at
   the midterm and LA-1/LA-2. If a committee wants every CLO
   re-assessed at term end, an LA-2 reprise in the practical exam
   would close it.
3. **M23 (file transfer) was completed 2026-09** and its quiz is in
   the index; its *lab-assessment* coverage is folded into LA-5's
   remote-workstation circuit rather than having a dedicated item.
4. **No pre/post standardized concept inventory exists.** The course
   assesses performance, not attitude/retention drift; that would be
   an instructor-added instrument.

---

## 5. How to use this document

- **Course file / accreditation binder:** pair this matrix with the
  one-pager; cite artifact paths as evidence.
- **Instructor of record:** review §1's *proposed* status, adjust
  wording to institutional templates, and record approval date.
- **Program reviewers:** §4 lists every known coverage gap; nothing
  is claimed beyond the artifacts named above.
