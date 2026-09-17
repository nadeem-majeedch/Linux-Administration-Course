# FINAL-AUDIT.md — Pre-Release Instructor Review

> **Date:** 2026-09-17 · **Reviewer stance:** expert university instructor evaluating
> release-readiness for BS Data Science students with zero Linux experience.
> **Scope:** entire repository (526 markdown files, 32 module directories, full
> assessments/labs/projects/cheatsheets trees, publication workflow).
> **Method:** this audit is **read-only**. Every technical claim below was re-verified
> by execution during this audit (link crawler, fence counter, YAML parser, targeted
> greps, document sampling) or cites the executed QA audit of the same date
> (QA-REPORT.md, entry 22 of resources/validation-checklist.md). No files were
> modified; nothing committed or pushed.
>
> **Verdict: APPROVED FOR RELEASE** — 0 CRITICAL, 1 HIGH, 6 MEDIUM, 5 LOW findings.
> The single HIGH finding is a known, documented content gap (one module still
> scaffolded); everything else is polish.

---

## Executive summary

This is an unusually complete, pedagogically coherent course. The zero-to-hero arc
is real (M01 assumes literally nothing; M30 requires a defended, operating server),
every one of the 22 requested Linux topics and 11 Data Science topics is covered in
dedicated teaching material, safety discipline is consistent throughout (sandboxed
labs, fenced destructive commands, no-secrets hygiene), and the assessment apparatus
(quizzes with keys, two exams, practical exam with instructor staging script, lab
assessments, assignments, rubric, viva bank, injectable incidents) is
publication-grade. The technical substrate is clean: 0 broken links, 0 unbalanced
fences, 0 real shell-syntax defects across 1,090 checked blocks, 0 secret-pattern
hits, and a least-privilege, current-version GitHub Pages workflow.

---

## Findings register

| # | Severity | Finding | Where | Notes |
|---|---|---|---|---|
| 1 | **HIGH** | M23-file-transfer has **no lesson/lab content** — a scope contract only | `modules/M23-file-transfer/README.md` ("Status: scaffolded") | Listed as a normal module in README's Module Index; a student following the index week-by-week hits an empty module. Roadmap and module README disclose this, the main README does not. Fix: write the module (scp/sftp/rsync, delta syncs, verified transfers) or add a visible "content pending" banner to the README index row. |
| 2 | **MEDIUM** | Module-numbering collision: two directories share the `M23` prefix (`M23-file-transfer`, `M23-linux-performance-troubleshooting`) and the two "companion" modules (M31, performance clinic) sit outside the M01–M30 numbering | `modules/`, README Course Facts | The roadmap documents both companions, but "module N = directory MN" breaks; references like "M23-clinic" require local knowledge. Renumber companions as `C1/C2` or `M32/M33` in a future release. |
| 3 | **MEDIUM** | README "Course Facts: Total modules **30**" vs 32 module directories shipped | `README.md` | Companions are mentioned in the repo map but the count invites semester-planning confusion (see #2). |
| 4 | **MEDIUM** | M05's quiz embeds its answer key **in the same file**, directly after the questions | `modules/M05-terminal-and-shell/content/practice/quiz-aliases-history.md` ("## Answer key" at line 23) | Every other module separates `quiz.md` from `quiz-answers.md`; self-assessment value is lost when answers are one scroll away. |
| 5 | **MEDIUM** | Learning-objective placement is inconsistent: 8 content READMEs carry objectives inline; 22 point to the roadmap | `modules/M*/content/README.md` | Objectives **exist for all 30 roadmap sections** (verified: 30/30 `**Learning objectives**` blocks in COURSE-ROADMAP.md), so nothing is missing — but a student browsing `content/` won't see them on 22 modules. Standardize in a content pass. |
| 6 | **MEDIUM** | No explicit **outcome × assessment alignment matrix** (CLO map) | `README.md` (10 outcomes), `assessments/` | Assessments map to modules, and the capstone SPEC maps tasks to modules, but no single table ties each course learning outcome to the assessments that measure it. Expected by accreditation reviewers; ~1 page to produce. |
| 7 | **MEDIUM** | The centralized `assessments/quizzes/` holds one exemplar (M12) plus an index that points to per-module quizzes | `assessments/quizzes/` | The README explains the split, but an instructor expecting a full centralized bank will be briefly misled. Either mirror all 30 quizzes here or retitle the directory "Exemplar". |
| 8 | **LOW** | M02 and M05 predate the full module template (shorter quizzes — 16 and 10 questions vs 20–22; M05's labs live in M01, linked) | `modules/M02*`, `modules/M05*` | Content is complete and cross-linked; documented in QA-REPORT.md. |
| 9 | **LOW** | Difficulty vocabulary wobbles: 3 modules use "Intermediate-Advanced" while the rest use the 3-level scale | README difficulty survey | Cosmetic. |
| 10 | **LOW** | Prerequisite list ordering is not canonicalized ("M20, M21" vs "M21, M20" both occur) | README prereq survey | Cosmetic; no pedagogical effect. |
| 11 | **LOW** | First Pages deploy fails until the one-time "Settings → Pages → Source: GitHub Actions" is set | `.github/workflows/publish.yml` (header comment), `WEBSITE.md` | Correctly documented in two places; failure mode is a clear message. Informational. |

---

## 1. COURSE DESIGN

**Progression — PASS.** The arc is genuinely zero-to-hero and internally consistent:

- Difficulty labels across modules (grep-verified): 6 Beginner → 9 Intermediate →
  4 Intermediate-Advanced → 11 Advanced, in strictly increasing module order.
- Prerequisites form a clean DAG (verified for all 32 modules; e.g. M22 requires
  M21/M20; M25 requires M20/M21/M25-chain; capstone requires M01–M29). No module
  requires something not yet taught.
- M01 Lesson 1 defines an operating system from first principles (~20 min reading
  time, no assumed vocabulary); SETUP.md promises a working environment "even if
  you start with nothing installed and no administrator rights."
- Summit is appropriate: M31 (DS server operations) + M30 capstone (deploy,
  operate, *defend* under injected incidents + viva).

**Difficulty pacing — PASS.** Two-to-four lessons per module, ~20–35 min each,
labs 30–90 min, weekly module pace documented for 1- and 2-semester plans. The
jump from M04 (install) to M05 (terminal) is gentle; the M17–M20 storage/services
block is the steepest climb and is preceded by the strongest practice ladder
(Levels 1–4 progressive labs).

**Assessment of this section:** 1 HIGH (finding 1), 1 MEDIUM (finding 3), rest PASS.

## 2. LINUX COVERAGE (all 22 requested topics — PASS)

Verified by topic→file grep across `modules/` (file counts are evidence of
distributed reinforcement, not single-mention coverage):

| Topic | Home module(s) | Reinforcement (files mentioning) |
|---|---|---|
| CLI / filesystem / permissions | M05–M07, M12–M14 | chmod in 75 files |
| users/groups | M12–M14 | useradd/usermod in 28 files |
| processes | M18 (+M24 monitoring) | ps/top/htop in 320 files |
| packages | M16 | apt in 160 files |
| storage | M17 | lsblk/fstab/mount in 85 files |
| networking | M21 | ip/ss/dig in 325 files |
| services/systemd | M20 | systemctl in 84; journalctl in 77 |
| SSH | M22 (+M25 hardening) | 51 files |
| security | M25 (+M22 §2, M14) | ufw in 30 files |
| logs/monitoring | M24 (+performance clinic) | 77 + dedicated `performance/` tree |
| automation/Bash | M10–M11 (+M19 cron/timers) | cron in 102 files |
| backups | M24 §5 + backup lab + mini-project E | backup in 118, restore in 80 files |
| troubleshooting | M23-clinic (methodology + 12 drill cards) | dedicated `scenarios/` tree |
| servers | M29 (+server-admin extension) | 4-lesson extension incl. fleet/config-mgmt |
| containers | M28 (5 lessons, 4 labs) | docker in 32 files |
| cloud | M29 extension `cloud/` (3 lessons + local cloud-init lab) | provider-neutral, no spend |
| DevOps | M29 extension `devops/` (loop, CI/CD, IaC + local CI lab) | Ansible/Terraform/Actions conceptual |

No gaps. The two "extension" topics (cloud, DevOps) are correctly scoped as
conceptual-plus-local-lab rather than pretending to cloud access.

## 3. DATA SCIENCE COVERAGE (all 11 requested topics — PASS)

| Topic | Evidence |
|---|---|
| Python | M27 (4 lessons: system Python, venvs, pip discipline, CLI Python) |
| Virtual environments | venv/venv mentions in 80 files; pinned-requirements habit enforced in capstone |
| Jupyter | 64 files; M27 remote-headless lab; M31 server patterns |
| Git | M26 (model → branching → remotes/auth), e2e DS workflow lab |
| Datasets | `datasets/` tree; CSV handling in 123 files; M08 text-processing toolkit |
| Large files | M08 pipelines-over-Python lesson; streaming/sed/awk treatment |
| Remote servers | M22 (SSH, tunnels, tmux) + M31 server module |
| ML workloads | M31 (GPU/CUDA *administrative* stack, CPU-only lab twins, checkpoints) |
| Resource monitoring | M24 monitoring toolkit + performance clinic (CPU/mem/disk/net) |
| Docker | M28 incl. Jupyter-Compose lab; reproducibility strong form in M31 |
| Reproducibility | 41 files; M31's six-link chain (code SHA → env pins → data checksum → stamped config → run dir → fresh-clone proof) |

The DS thread is not decorative: each unit's roadmap section carries an explicit DS
connection, and the capstone requires an operating data product, not a demo.

## 4. PRACTICAL QUALITY

**Lab realism — PASS.** Sampled labs (M06 navigation drills, M13 shared-tree build,
M17 loopback disk lab, M27 remote Jupyter, M31 two-actor DS server lab) use
realistic artifacts: project directory conventions, `sales-analysis` venvs, shared
`/srv` trees with six-person team scenarios, loopback devices instead of real
disks, a colleague account instead of a shared server.

**Commands executable — PASS.** Full-repo `bash -n` over 1,090 extracted
bash/console blocks: 0 real defects (99 flags triaged to transcript-output
artifacts and 4 intentional broken-teaching examples — QA-REPORT.md). All Python
blocks pass `py_compile`. Spot-sampled console lines are valid, current commands
(`mkdir -p ~/projects/…/{data/{raw,processed},…}` etc.).

**Dangerous operations identified — PASS.** `rm -rf` appears only as danger
explanations, scoped teardown of lab-created paths (`/srv/t-lab`,
`/scratch/$USER`), or container idioms — never as host-destructive instruction.
`dd`/`mkfs` only against loopback images. 53 explicit ⚠️/WARNING markers; M17's
disk lab references snapshots 5 times; the "FORMAT (loopback-safe!)" annotation
pattern is used consistently.

**Progressive difficulty — PASS.** Challenges carry ★/★★/★★★ gradations (6 modules
use the star ladder; drill cards use ●●○); lab assessments escalate from
permission surgery to service-and-log forensics; the labs/ tree runs Levels 1–5.

**Troubleshooting realism — PASS.** The 12 drill cards are authentic failure
families (deleted-but-open files, the full-disk-that-isn't, DNS vs connectivity
splits, phantom hangs) with decision trees; the practical exam plants six staged
faults with an instructor staging script; the capstone injects incidents.

## 5. ACADEMIC QUALITY

- **Learning objectives:** 30/30 roadmap module sections have explicit objective
  blocks (verified). Placement inconsistency noted as finding 5.
- **CLO alignment:** README defines 10 program-level outcomes; capstone SPEC
  defines LO1–LO9 mapped to modules. Missing alignment matrix noted as finding 6.
- **Assessments inventory (verified on disk):** 30 module quizzes + 29 separate
  answer keys (+1 embedded key = finding 4); consolidated quiz bank index with
  one exemplar (finding 7); midterm + final with keys; practical exam + key +
  staging script; 5 lab assessments; 3 assignment specs; project rubric;
  consolidated viva bank → capstone instructor VIVA.md (29 questions with
  follow-up probes and full-credit markers, format verified).
- **Labs:** 74 module labs + 5 progressive levels + 3 performance-clinic labs.
- **Projects:** 6 mini-projects (A–F) + capstone student/instructor packs
  (SPEC, STARTER, RUBRIC, VIVA, INCIDENTS with answer keys).
- **Assessment philosophy is enforced and unusual:** questions are scenario- and
  evidence-based; the three cheatsheet-answerable recall questions found in the
  QA pass were rewritten (M14/M16/M18). Midterm/final explicitly prohibit
  copy-from-cheatsheet answers.

## 6. TECHNICAL QUALITY

| Check (executed) | Result |
|---|---|
| Internal links (crawler) | **1,820 checked, 0 broken** |
| Markdown fences (counter) | **0 unbalanced across 526 files** |
| Shell syntax (`bash -n`, Git Bash binary) | **0 real defects** (see QA-REPORT for triage) |
| Python syntax (`py_compile`) | **0 failures** |
| Workflow YAML (parsed + structure-asserted) | **valid**; push+dispatch triggers, least-privilege permissions, two-job graph |
| GitHub Pages configuration | correct: strict MkDocs build → artifact → deploy-pages; site URL matches repo (project pages, no `site_url` mismatch); strict-mode validation prevents publishing broken links |
| Obsolete commands | none taught as current; `ifconfig`/`route`/`arp` appear **only** in a deprecated-vs-modern replacement table (M21 §2) — good pedagogy |
| Distribution assumptions | Ubuntu LTS declared primary; 51 dnf/zypper/pacman + 43 RHEL/Fedora/Alpine references keep families distinguished; M02 troubleshooting card covers "apt: command not found" on RPM systems |
| Secrets scan (AWS/GH/Slack/private-key patterns) | **0 hits** (re-verified in QA pass) |

## 7. SECURITY

- **Unsafe practices — PASS.** No exploitation content; all security labs run in
  student-owned VMs; hardening checklist ships with M25; `chmod 777` appears only
  as an anti-pattern ("a confession, not a repair") including an autopsy exercise.
- **Root/sudo discipline — PASS.** Root access never assumed (README Course Facts,
  SETUP.md); sudo introduced in M14 with the "root principle" framing
  (irreversibility, logging, scoped grants); destructive commands carry
  safeguards and recovery notes; VM snapshots before risky labs.
- **Credential handling — PASS.** Secrets-hygiene `.gitignore` rules; M15 §4
  (secrets in env vs files), M25 §5, M26 never-commit-credentials drill
  (fabricated `API_KEY=pretend` leak-and-rotate scenario), M28 dedicates a lesson
  section to why `ENV API_KEY=…` leaks and teaches Compose secrets; M29 warns
  against secrets in unit files. Capstone deducts for committed secrets and
  requires rotation-first remediation.
- **SSH security — PASS.** Key-only auth, `PasswordAuthentication no` hardening
  lesson + quiz coverage (M22 §2/M25 §3), host-key-verification choreography
  taught via the HOST KEY CHANGED drill, root-login risk explained, rollback
  documented in capstone requirements.
- **Firewall guidance — PASS.** Explicit `ufw default deny incoming` posture
  (M25), justify-every-open-port requirement in the capstone, services bound to
  loopback/tunnel in Jupyter/Postgres labs rather than exposed.

---

## Release recommendation

**Release with the current one HIGH finding disclosed** (finding 1), or after
writing M23-file-transfer's content — it is the only gap a student can actually
fall into. Findings 2–7 are a one-day polish pass (README counts, one quiz-key
split, one alignment matrix, companion renumbering decision). Findings 8–11 can
ride along whenever convenient.

*This audit modified nothing; FINAL-AUDIT.md is the only file created, as
requested. No commits, no pushes, no history changes.*
