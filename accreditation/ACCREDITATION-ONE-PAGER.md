# Course One-Pager — Linux Administration: Zero to Hero

> **Document status:** prepared from the repository's actual contents
> for departmental course review, curriculum committee, and the course
> file. Every factual claim below is traceable to a repository path;
> institutional approval is *not* claimed anywhere in this document.
> Companion: [CLO-ASSESSMENT-ALIGNMENT.md](CLO-ASSESSMENT-ALIGNMENT.md) ·
> [CLO-MAPPING-MATRIX.md](CLO-MAPPING-MATRIX.md)

---

## 1. Course identity

| Item | Detail |
|---|---|
| Course title | Linux Administration: Zero to Hero |
| Repository | `Linux-Administration-Course` |
| Target program | BS Data Science |
| Course level | Undergraduate; assumes **zero Linux experience**, progresses to advanced practical administration |
| Scope | 30 numbered modules (M01–M30) in 8 units, plus 2 content-complete companion modules (M31 Data Science Server, M32 Performance & Troubleshooting Clinic) — 32 module directories in total |
| Suggested pace | 1 module/week → two semesters; 2 modules/week → one semester ([COURSE-ROADMAP.md](../COURSE-ROADMAP.md)) |
| Primary environment | Ubuntu LTS (24.04 or newer) in a student-owned VirtualBox VM; WSL2 documented as the Windows alternative; Docker used from M28 |
| Root access | Not assumed; safe-administration practices enforced throughout ([SETUP.md](../SETUP.md)) |

## 2. Course rationale

Data Science work is executed *on Linux machines* — laptops, university
GPU servers, and cloud instances alike — yet most DS curricula treat the
operating system as invisible until it fails. This course makes that
layer explicit, because every downstream DS competency depends on it:

- **Python environments** — virtual environments, `pip` isolation, and
  environment diagnosis are Linux filesystem and `$PATH` skills (M15, M27).
- **Data processing** — shell text tools (`grep`/`sed`/`awk`/`sort`) do
  the first-pass triage on large files before pandas is even imported (M08–M09).
- **Remote servers** — GPU/compute access is SSH: keys, tunnels, tmux,
  and file transfer are the daily interface, not optional extras (M22, M23, M31).
- **Jupyter** — running, tunneling, and administering notebook servers
  is a service-management task (M20, M27, M31).
- **Git** — version control, remotes, and SSH authentication are taught
  on Linux with Linux-native tooling (M26).
- **Containers** — Docker is introduced as Linux primitives (namespaces,
  cgroups conceptually) with reproducible ML environments as the payoff (M28).
- **System administration** — permissions on shared datasets, service
  lifecycle, logs, and monitoring are exactly the duties of the person
  who owns the lab's data server (M12–M14, M20, M24).
- **Reproducibility** — checksums, pinned environments, provenance
  sidecars, and verified backups form a chain practiced across modules
  and demanded by the capstone (M19, M23, M29, M30).

## 3. Course learning outcomes (PROPOSED — pending institutional approval)

Seven CLOs, derived from the module objectives written in
[COURSE-ROADMAP.md](../COURSE-ROADMAP.md) and clearly labeled *proposed
for instructor review* — no institutional CLO template was supplied:
**CLO-1** command line, filesystem & text processing · **CLO-2** Bash
scripting & automation · **CLO-3** users, groups, permissions &
least-privilege shared access · **CLO-4** packages, storage, services &
scheduling · **CLO-5** networking, SSH, secure transfer & firewall ·
**CLO-6** logs, monitoring & evidence-first incident response ·
**CLO-7** the Linux DS stack: Python/Jupyter, Git, containers,
reproducible servers. Full statements and Bloom levels:
[CLO-ASSESSMENT-ALIGNMENT.md](CLO-ASSESSMENT-ALIGNMENT.md).

## 4. Course content (from the actual module inventory)

| Unit | Modules | Core content |
|---|---|---|
| 1 Foundations | M01–M04 | what Linux is, distros, architecture, install Ubuntu in a VM |
| 2 Command Line Fluency | M05–M09 | terminal & shell, filesystem hierarchy, files & directories, text processing, pipes & redirection |
| 3 Scripting & Automation | M10–M11 | Bash scripting, advanced automation |
| 4 System Administration | M12–M15 | users/groups/permissions, shared access, sudo, environment variables |
| 5 Software, Storage & Time | M16–M19 | package management, storage/filesystems, processes & signals, cron & timers |
| 6 Services, Networking & Security | M20–M25 | systemd, networking, SSH & remote administration, file transfer (SCP/SFTP/rsync), logs/journald/monitoring, security & firewall |
| 7 The Data Science Stack | M26–M29 | Git & dev workflows, Python/Jupyter & data workloads, Docker & containers, web servers/databases/deployment |
| 8 Capstone | M30 (+M31/M32 companions) | deploy & administer a Linux-based DS server; the DS server module; performance & troubleshooting clinic |

Volume (counted, not estimated): 114 lesson pages, 72 module labs,
30 student quizzes (~620 questions), 30 challenge sets, 29
troubleshooting references, 20 cheatsheets, plus centralized
assessments, a five-level progressive lab ladder, and generated
datasets for text-processing work.

## 5. Teaching and learning strategy

- **Lessons** — narrative, example-first pages with expected output,
  self-checks, and Data Science connections in every module.
- **Demonstrations & labs** — hands-on, loopback/VM-sandboxed
  exercises; labs produce *evidence transcripts* (`script logs`),
  not end states alone. The course-level [labs/](../labs/README.md)
  ladder runs Level 1 (beginner) → Level 5 (DS server operations).
- **Troubleshooting practice** — every module has a
  symptoms→causes→fixes page; the M32 clinic consolidates an 8-step
  incident method and a staged Drill Book of independent failures.
- **Projects** — four mini-projects (A–D) embedded at unit
  boundaries; the capstone integrates all of them.
- **Capstone** — "Deploy and Administer a Linux-Based Data Science
  Server": five phases (proposal → build → operate → document →
  defend), executable on a local VM, WSL2, or Docker; cloud/GPU
  optional ([projects/capstone/](../projects/capstone/README.md)).

## 6. Assessment strategy

Instruments (all anti-memorization audited — scenario/evidence-based,
never cheatsheet-answerable): per-module quizzes with instructor-held
keys; five graded lab-assessment circuits (LA-1…LA-5); three
assignments; midterm (Units 1–3, 20%), final (Units 4–7, 25%), and a
staged-server practical exam (15%) with instructor staging script and
keys; capstone rubric (100 points, evidence-graded, five phases) plus
a 29-question viva bank. Full CLO→instrument mapping with honest gap
flags: [CLO-ASSESSMENT-ALIGNMENT.md](CLO-ASSESSMENT-ALIGNMENT.md).

## 7. Practical infrastructure

Documented and supported in [SETUP.md](../SETUP.md) and M04: VirtualBox
Ubuntu VM (primary, 4 GiB/2 vCPU/25 GB guidance), WSL2 (Windows path,
with noted limitations where systemd/loopback labs differ), native
install (optional), Docker (from M28 onward). All lab breakage is
student-staged inside the student's own VM or user-level units; no
shared or production system is required anywhere in the course.

## 8. Security and responsible administration

- **Least privilege** is a graded theme: sudo policy (M14), shared
  access design (M13), key-only SSH (M22), minimal firewall (M25).
- **Safe lab design**: destructive commands only inside student-created
  directories with printed-path teardown; `--delete` never without a
  prior dry-run; break-and-repair performed on snapshots/user units.
- **Credential safety**: no secrets in repositories (capstone rule:
  `600` env files outside the repo, rotate-first policy); lab keys are
  never personal keys; password auth disabled *conceptually* with
  rollback documented.
- **Controlled operations**: firewall changes justified port-by-port;
  hardening checklist in M25 applied with evidence at the capstone.

## 9. Graduate skills

By graduation from this course, students can: work fluently in a Linux
shell; process and verify datasets from the command line; automate
recurring work with robust Bash scripts; manage users, permissions,
services, storage, and scheduling on a server; administer remote
machines over SSH with keys and encrypted transfer; read logs and
monitor a system and methodically diagnose failures; run Python,
Jupyter, Git, and Docker workflows on Linux; and deploy, document,
back up, and defend a reproducible data-science server — the
operating reality of any junior data scientist or ML engineer.

## 10. Evidence and quality assurance

**Completed verification** (execution-based, logged in
[resources/validation-checklist.md](../resources/validation-checklist.md)):
1,800+ internal links checked (0 broken, file-level and heading-anchor
level); shell code blocks syntax-checked (`bash -n`); Python blocks
compiled; secrets scan clean; strict MkDocs site build (0 warnings);
GitHub Actions Pages workflow with least-privilege permissions; a
pre-publication QA audit ([QA-REPORT.md](../QA-REPORT.md)) and an
instructor-standard final audit ([FINAL-AUDIT.md](../FINAL-AUDIT.md))
whose HIGH/MEDIUM findings were closed in the repository's audit-closure
report (`FINAL-AUDIT-CLOSURE.md`, repository root).

**Not claimed:** institutional approval of the proposed CLOs (§3);
accreditation status of any kind; weekly contact hours or grade
weightings beyond those documented in the repository's own assessment
files; any commercial cloud dependency.
