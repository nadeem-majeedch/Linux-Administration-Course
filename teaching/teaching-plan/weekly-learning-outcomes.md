# Weekly Learning Outcomes

> One outcome block per week: what a student can *do* by Friday, and the
> evidence that proves it. Outcomes are phrased as abilities (not topic
> lists) and each names its evidence artifact and its proposed-CLO links
> ([accreditation/CLO-ASSESSMENT-ALIGNMENT.md](../../accreditation/CLO-ASSESSMENT-ALIGNMENT.md)
> — CLOs remain **proposed**, pending instructor review).

| Week | By Friday, a student can… | Evidence artifact | CLOs |
|---|---|---|---|
| 1 | Explain what an OS/kernel/distro actually are, and correct three common Linux misconceptions in conversation | M01–M03 quiz + in-class whiteboard layer-cake | CLO-1 |
| 2 | Install and boot an Ubuntu LTS VM, take/restore a snapshot, and explain why snapshots make safe experimentation possible | Working VM + snapshot restore demo in `script` log | CLO-4 |
| 3 | Navigate the whole filesystem hierarchy from any directory using absolute/relative paths, and manage files with glob patterns confidently | LA-1 Navigation & Files Circuit (graded) | CLO-1 |
| 4 | Build text pipelines over real datasets (`grep → cut → sort → uniq → awk`) and predict what a pipeline does before running it | Pipeline prediction quiz + M08 mini-project | CLO-1 |
| 5 | Write a guarded Bash script (`set -euo pipefail`, argument checks, exit codes) and debug a broken script systematically | Script + `shellcheck` pass; fix-the-bug set | CLO-2 |
| 6 | Design permissions for a shared dataset (users/groups/modes/SGID), apply least privilege, and justify every sudo rule they add | Mini-Project B design sheet + LA-3 | CLO-3 |
| 7 | *(consolidation + midterm)* Demonstrate Units 1–3 fluency under exam conditions | **Midterm** (20%) | CLO-1–3 |
| 8 | Install/remove/query packages safely and create/format/mount a loopback disk, explaining each fstab field | Storage lab evidence + M16–M17 quiz | CLO-4 |
| 9 | Read `ps`/`top`/`signals` output to manage processes, and schedule a correct, logged, environment-safe cron job | Working crontab + process-triage quiz | CLO-4, CLO-6 |
| 10 | Manage a systemd user service across start/stop/enable/failure, and diagnose a network problem layer-by-layer | Service journal evidence + network ladder worksheet | CLO-4, CLO-5 |
| 11 | Establish key-based SSH to their own VM, transfer and *verify* files both directions, and explain the host-key decision they made | SSH session + sha256-verified transfer log (LA-5 groundwork) | CLO-5 |
| 12 | Trace a failure through journald/`/var/log` and monitoring tools to a root cause using the 8-step evidence method; apply a minimal UFW policy | Incident report with quoted evidence; hardening checklist | CLO-6, CLO-5 |
| 13 | Run a complete DS loop on Linux: clone repo → venv → pinned deps → dataset → Jupyter → commit | End-to-end lab transcript + repo history | CLO-7 |
| 14 | Containerize a small workload and explain volumes/ports; serve a dataset through nginx and load a PostgreSQL table | Container + service evidence | CLO-7 |
| 15 | Operate a mini DS server: durable sessions, monitoring circuit, backup/restore with checksums, cleanup census (M31/M32 + revision) | Level-5-style run sheet + revision checklist | CLO-6, CLO-7 |
| 16 | Perform under exam conditions: staged-server practical, final exam, capstone defense | **Practical (15%) · Final (25%) · Capstone** | all |

## Reading the table

- **Evidence column** names where the proof already exists in the course
  (graded LA circuits, quizzes, mini-projects, exams) — weeks do not
  invent new graded artifacts; they route students to the ones the
  repository ships with.
- **CLO codes** reference the proposed set; no week claims coverage the
  underlying assessments don't support (the alignment matrix is the
  authority).
- Weeks 1–2 intentionally front-load *environment success*: the strongest
  predictor of week-3 survival is a working, snapshotted VM.
