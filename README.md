# Linux Administration Course — From Zero to Hero

> A complete, university-level Linux course built for **BS Data Science students**.
> Start with zero Linux experience; finish able to administer servers, automate data
> workflows, and deploy data-science workloads on Linux.

---

## Why This Course Exists

Modern data science runs on Linux. Jupyter servers, GPU training clusters, cloud
instances, Docker containers, CI systems, and most production ML deployments are
Linux machines. Yet most data science programs never teach students how to actually
*operate* these systems.

This course closes that gap. By the end you will be able to:

- Work fluently and safely in a Linux terminal
- Administer your own Ubuntu system: users, permissions, packages, services
- Build robust shell pipelines to process datasets of any size
- Automate recurring data workflows with Bash scripts and cron
- Administer remote servers over SSH, including GPU training machines
- Serve data and models with web servers, databases, and containers
- Monitor, troubleshoot, and secure a Linux system
- Understand how cloud and DevOps practices build on Linux administration

---

## Who This Is For

- **Primary audience:** BS Data Science students — no prior Linux experience required.
- **Secondary audience:** CS/SE students, analysts, and self-learners who want a
  practical, project-driven path into Linux administration.
- **Prerequisites:** Basic computer literacy. Basic Python is helpful but not required;
  Python is introduced gently where needed. No command-line experience is assumed.

---

## Course Facts

| Item | Detail |
|---|---|
| Primary environment | **Ubuntu LTS** (24.04 LTS or newer) |
| How you'll run it | VirtualBox VM (recommended), WSL2 (Windows alternative), native install (optional) |
| Total modules | **30 numbered modules** (M01–M30) in 8 units, **plus 2 companion modules** (M31 Data Science Server, M32 Performance & Troubleshooting Clinic) — 32 module directories in total |
| Suggested pace | 1 module/week → 2 semesters; 2 modules/week → 1 semester |
| Capstone | M30: a complete, deployed, documented data-science system |
| Root access | **Not assumed** — the course works on shared and lab machines (see [SETUP.md](SETUP.md)) |
| Language | English |

---

## Repository Map

```
Linux-Administration-Course/
├── README.md                ← you are here
├── COURSE-ROADMAP.md        ← full curriculum: units, modules, objectives, DS links
├── SETUP.md                 ← environment setup (VM, WSL2, tools)
├── WEBSITE.md               ← how this repo publishes its website (MkDocs + Pages)
├── accreditation/           ← proposed CLOs, alignment matrices, course one-pager
├── CONTRIBUTING.md          ← how to contribute content, style, review process
├── LICENSE                  ← MIT license
├── mkdocs.yml               ← website configuration (navigation, theme)
├── requirements-docs.txt    ← pinned website build dependencies
├── .github/workflows/
│   └── publish.yml          ← builds & publishes the website on push to main
├── scripts/
│   └── build-site.sh        ← assembles the website sources from repo content
├── modules/
│   ├── M01-what-is-linux/
│   ├── ...                  ← 30 numbered modules, M01–M30
│   ├── M31-data-science-server/   ← companion: DS server operations
│   └── M32-linux-performance-troubleshooting/ ← companion: the clinic
├── projects/
│   ├── mini-projects/       ← standalone mini-project briefs
│   └── capstone/            ← student pack + instructor pack (rubric, viva)
├── assessments/             ← quizzes, exams, lab assessments, assignments, viva
├── labs/                    ← progressive practical labs, Levels 1–5
├── cheatsheets/             ← 20 one-page command references (by topic)
├── datasets/                ← small datasets used in exercises and labs
├── resources/               ← unit cheatsheets, glossary, references, reading list
└── assets/                  ← diagrams and figures
```

---

## How to Use This Course

### The module pattern

Every module follows the same structure. See
[modules/M01-what-is-linux/README.md](modules/M01-what-is-linux/README.md) for the
canonical template:

| Section | What it contains |
|---|---|
| Overview | 1-paragraph purpose of the module |
| Prerequisites | Modules you should finish first |
| Learning objectives | What you will be able to *do* after the module |
| Concepts | The theory and mental models |
| Command-line skills | The commands and flags you must be able to use |
| Laboratory | Guided, hands-on activity with expected outputs |
| Exercises | Practice problems, with solutions withheld for self-check |
| Mini-project | A small, DS-flavored deliverable (when applicable) |
| Data Science connection | Explicit link between the module's skills and DS work |
| Common pitfalls | Mistakes beginners make, and how to avoid them |
| Self-check | Questions and skills to verify before moving on |
| Further reading | Official documentation links (Ubuntu, kernel.org, man pages) |

### Reading the material online

The whole course is browsable as a website — units as tabs, every module
linked to its lessons, labs, quizzes, and cheatsheets, with full-text search:

**https://nadeem-majeedch.github.io/Linux-Administration-Course/**

The site is rebuilt automatically from this repository on every push to
`main`; the pages you read there are the same Markdown files you see here.

### How to study

1. **Set up your lab first.** Follow [SETUP.md](SETUP.md): an Ubuntu VM is the
   recommended environment; WSL2 works on Windows. Do this before Module 01.
2. **Follow the units in order.** The
   [Course Roadmap](COURSE-ROADMAP.md) defines the sequence M01 → M30 and what
   each module assumes you already know. Modules build on each other —
   don't skip ahead.
3. **Work each module in the same rhythm:** read the lessons, do the labs,
   attempt the exercises and quiz *before* looking at answers, then check the
   module's self-check before moving on.
4. **Keep a lab log** (`lab-log.md`). Record what you ran, what happened, and
   one thing you'd do differently. The capstone grades evidence of practice.
5. **Use the safety rails.** Stay in your VM/WSL2 sandbox, take snapshots
   before risky labs, and never run a command you can't explain.
6. **Close the loop with the practice tiers:** the [progressive labs](labs/README.md)
   (Levels 1–5), [mini-projects](projects/mini-projects/README.md),
   [assessments](assessments/README.md), and finally the
   [capstone](projects/capstone/README.md).

### Practical expectations

- **Do everything in the labs.** Reading alone will not build terminal fluency.
- **Type commands yourself.** Do not paste blindly; predict what each command does first.
- **Keep a lab log** (a simple `lab-log.md` file) — the capstone grades evidence of practice.
- **Break things on purpose, in the right place.** The course tells you *where* it is safe
  to experiment (your VM or WSL2 instance) and how to recover.

### Assessment model (suggested)

| Component | Weight |
|---|---|
| Lab completion (lab logs, per module) | 30% |
| Mini-projects (M07, M10, M15, M22, M25) | 25% |
| Quizzes (units 1–4 and 5–8) | 15% |
| Skills check-offs (live terminal tasks) | 10% |
| Capstone project (M30) | 20% |

Instructors can adapt weights; the grading rubric for each component ships with the module.

---

## Module Index

| # | Module | Unit |
|---|---|---|
| 01 | [What Is Linux?](modules/M01-what-is-linux/README.md) | 1. Foundations |
| 02 | [Distributions](modules/M02-linux-distributions/README.md) | 1. Foundations |
| 03 | [Linux Architecture](modules/M03-linux-architecture/README.md) | 1. Foundations |
| 04 | [Installing Ubuntu in a VM](modules/M04-installing-linux-vms/README.md) | 1. Foundations |
| 05 | [The Terminal & Shell](modules/M05-terminal-and-shell/README.md) | 2. Command Line |
| 06 | [Filesystem Hierarchy & Navigation](modules/M06-filesystem-hierarchy/README.md) | 2. Command Line |
| 07 | [Files, Directories & Text Files](modules/M07-files-and-directories/README.md) | 2. Command Line |
| 08 | [Text Processing Toolkit](modules/M08-text-processing/README.md) | 2. Command Line |
| 09 | [Pipes, Redirection & Filters](modules/M09-pipes-and-redirection/README.md) | 2. Command Line |
| 10 | [Bash Scripting](modules/M10-bash-scripting/README.md) | 3. Shell & Automation |
| 11 | [Advanced Shell & Automation](modules/M11-advanced-shell-automation/README.md) | 3. Shell & Automation |
| 12 | [Users, Groups & Permissions](modules/M12-users-groups-permissions/README.md) | 4. System Administration |
| 13 | [Ownership & Shared Access](modules/M13-ownership-shared-access/README.md) | 4. System Administration |
| 14 | [Sudo & the Root Principle](modules/M14-sudo-root-principle/README.md) | 4. System Administration |
| 15 | [Environment Variables & Configuration](modules/M15-environment-variables/README.md) | 4. System Administration |
| 16 | [Package Management](modules/M16-package-management/README.md) | 5. Software & Storage |
| 17 | [Storage, Disks & Filesystems](modules/M17-storage-and-filesystems/README.md) | 5. Software & Storage |
| 18 | [Processes, Jobs & Signals](modules/M18-processes-jobs-signals/README.md) | 5. Software & Storage |
| 19 | [Scheduling: cron, systemd timers](modules/M19-scheduling-cron-timers/README.md) | 5. Software & Storage |
| 20 | [systemd, Services & Boot](modules/M20-systemd-services/README.md) | 6. Services & Networking |
| 21 | [Networking Fundamentals](modules/M21-networking-fundamentals/README.md) | 6. Services & Networking |
| 22 | [SSH & Remote Administration](modules/M22-ssh-remote-admin/README.md) | 6. Services & Networking |
| 23 | [File Transfer: SCP, SFTP, rsync](modules/M23-file-transfer/README.md) — **content complete 2026-09** | 6. Services & Networking |
| 24 | [Logs, journald & Monitoring](modules/M24-logs-journald-monitoring/README.md) | 6. Services & Networking |
| 25 | [Security & Firewall](modules/M25-security-firewall/README.md) | 6. Services & Networking |
| 26 | [Git & Development Workflows](modules/M26-git-dev-workflows/README.md) | 7. Data Science Stack |
| 27 | [Python, Jupyter & Data Workloads](modules/M27-python-jupyter-data/README.md) | 7. Data Science Stack |
| 28 | [Docker & Containers](modules/M28-docker-containers/README.md) | 7. Data Science Stack |
| 29 | [Web Servers, Databases & Deployment](modules/M29-web-servers-databases/README.md) | 7. Data Science Stack |
| 30 | [Capstone Project](modules/M30-capstone-project/README.md) | 8. Capstone |

*(Unit 8 is the capstone itself. Two **companion modules** complete the set:
[M31 — The Data Science Server](modules/M31-data-science-server/README.md) and
[M32 — Performance & Troubleshooting Clinic](modules/M32-linux-performance-troubleshooting/README.md).)*

---

## The Data Science Thread

Every unit connects back to data science. This is not a generic Linux course with a DS
slapdash chapter — the DS thread is built into each module:

| Unit | Data Science connection |
|---|---|
| 1. Foundations | Understanding the OS your training clusters and cloud instances run on |
| 2. Command Line | Exploring datasets with `ls`, `cat`, `grep`, `wc`, `sort`, `uniq` |
| 3. Shell & Automation | Shell pipelines as fast data tools; scripted ETL and batch jobs |
| 4. System Administration | Users/groups on shared dataset servers; permissions on research data |
| 5. Software & Storage | Python environments, dataset storage, disk management, scheduled jobs |
| 6. Services & Networking | SSH to GPU servers, `rsync` datasets, logs from ML services, firewall basics |
| 7. Data Science Stack | Git, Jupyter, Dockerized ML, serving models, deployment |
| 8. Capstone | End-to-end: ingest → process → train → serve → monitor, on a Linux server |

---

## Learning Outcomes

By the end of this course, a student can independently:

1. **Install and administer Ubuntu** — VM or native, including updates, packages, storage.
2. **Operate the terminal fluently** — navigation, file ops, permissions, processes.
3. **Process data on the command line** — grep/sed/awk/sort/cut/tr pipelines over real datasets.
4. **Automate workflows** — robust Bash scripts with error handling, logging, cron/systemd timers.
5. **Administer users and access** — users, groups, ownership, sudo, shared data permissions.
6. **Run and manage services** — systemd units, journald logs, network servers, firewalls.
7. **Work remotely** — SSH key auth, config, SCP/SFTP/rsync to lab and GPU servers.
8. **Use the DS stack on Linux** — Git, Python venvs, Jupyter, Docker, databases, web servers.
9. **Diagnose and recover** — monitoring tools, log analysis, backups, safe recovery.
10. **Deploy a complete data product** — the M30 capstone, end to end.

---

## Safety First

- **No root required.** Labs run in VMs/WSL2 where you control the sandbox; on shared
  machines, everything works under your own account.
- **Destructive commands are fenced.** `rm -rf`, `dd`, `mkfs`, `fdisk`, and friends are
  introduced only with explicit warnings, safe alternatives, and recovery notes.
- **Snapshots before surgery.** You will take a VM snapshot before any risky lab, so you
  can always roll back.
- **Never run commands you can't explain.** If a lab asks you to run something you
  don't understand, stop and ask — that's a feature, not a failure.

---

## The Website (MkDocs + GitHub Pages)

The course publishes itself as a static website via [MkDocs](https://www.mkdocs.org/)
with the Material theme — chosen because the repository's plain Markdown stays
the single source of truth (files are copied verbatim, so relative links keep
working), and because the toolchain is two pinned Python packages a TA can
maintain. Details and rationale: [WEBSITE.md](WEBSITE.md).

### Local preview

```bash
# from the repository root — no admin rights, nothing outside the repo
python -m venv .docs-venv
source .docs-venv/bin/activate        # Windows: .docs-venv\Scripts\activate
pip install -r requirements-docs.txt
bash scripts/build-site.sh            # assembles site-src/ from repo content
mkdocs serve                          # live preview at http://127.0.0.1:8000
```

A production build (`mkdocs build --strict --clean`) writes `site/` and fails
on any broken internal link, so problems surface before publication.

### How publication works

- The publication workflow
  [`.github/workflows/publish.yml`](https://github.com/nadeem-majeedch/Linux-Administration-Course/blob/main/.github/workflows/publish.yml)
  triggers on
  every push to `main` (and manual *Run workflow* on the Actions tab).
- It builds the site in **strict mode** — any broken link fails the build —
  then deploys the artifact with the official GitHub Pages actions.
- Required one-time setting: **Settings → Pages → Build and deployment →
  Source: GitHub Actions**.
- Live site: <https://nadeem-majeedch.github.io/Linux-Administration-Course/>
- The workflow runs least-privilege (`contents: read`; only the deploy job has
  `pages: write`), uses no personal access tokens (OIDC), and pins current
  major versions of all `actions/*`.

---

## Documentation

- [COURSE-ROADMAP.md](COURSE-ROADMAP.md) — the full curriculum: objectives, concepts, labs, DS links.
- [SETUP.md](SETUP.md) — step-by-step environment setup (Windows/macOS/Linux).
- [WEBSITE.md](WEBSITE.md) — how this repository builds and publishes its website.
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute exercises, fixes, and new modules.
- [resources/glossary.md](resources/glossary.md) — plain-language glossary of terms.
- [resources/references.md](resources/references.md) — official documentation links.
- [resources/cheatsheets/](resources/cheatsheets/) — printable one-pagers per unit.
- [accreditation/](accreditation/) — proposed CLOs, CLO×assessment alignment
  matrix, module×CLO mapping, and the course one-pager for curriculum review.
- [teaching/](teaching/README.md) — **complete teaching package**: 16-week teaching
  plan (32 × 90-min sessions), unit slide decks with speaker notes, instructor
  manual, lab workbook, 10 in-class demonstrations, assessment framework
  (quiz bank v2, assignments A4–A6), student revision room, and environment
  setup/delivery guides. Instructor-only keys are excluded from site
  navigation — see [teaching/instructor-resources/INSTRUCTOR-ONLY.md](teaching/instructor-resources/INSTRUCTOR-ONLY.md).
- [LICENSE](LICENSE) — MIT.

---

## License

MIT — see [LICENSE](LICENSE). Course content may be freely used and adapted for
teaching with attribution.
