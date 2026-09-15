# Course Roadmap — Linux Administration: Zero to Hero

> **Audience:** BS Data Science students. No Linux experience assumed.
> **Environment:** Ubuntu LTS (24.04 LTS or newer). Commands are Ubuntu-specific where
> relevant; differences for other distributions are noted in module notes.
> **Root access:** never assumed. Every lab is safe in a VM/WSL2 sandbox or runs under a
> normal user account on a shared lab machine (see [SETUP.md](SETUP.md)).

---

## Contents

- [Curriculum Map](#curriculum-map)
- [Unit 1 — Foundations of Linux (M01–M04)](#unit-1--foundations-of-linux-m01m04)
- [Unit 2 — Command Line Fluency (M05–M09)](#unit-2--command-line-fluency-m05m09)
- [Unit 3 — Shell Scripting & Automation (M10–M11)](#unit-3--shell-scripting--automation-m10m11)
- [Unit 4 — System Administration (M12–M15)](#unit-4--system-administration-m12m15)
- [Unit 5 — Software, Storage & Time (M16–M19)](#unit-5--software-storage--time-m16m19)
- [Unit 6 — Services, Networking & Security (M20–M25)](#unit-6--services-networking--security-m20m25)
- [Unit 7 — The Data Science Stack (M26–M29)](#unit-7--the-data-science-stack-m26m29)
- [Unit 8 — Capstone (M30)](#unit-8--capstone-m30)
- [Appendix A — Required Topic Coverage Map](#appendix-a--required-topic-coverage-map)
- [Appendix B — Difficulty Scale](#appendix-b--difficulty-scale)

---

## Curriculum Map

Eight units build from "what is Linux" to a fully deployed, monitored, secure data-science
system. Difficulty ramps gradually; every unit has a Data Science anchor.

| Unit | Modules | Focus | DS anchor | Difficulty |
|---|---|---|---|---|
| 1. Foundations of Linux | M01–M04 | What Linux is, distros, architecture, installing Ubuntu in a VM | The OS behind every training server | Beginner |
| 2. Command Line Fluency | M05–M09 | Terminal, shell, filesystem, file ops, text processing, pipelines | Exploring and shaping datasets in the shell | Beginner → Intermediate |
| 3. Shell Scripting & Automation | M10–M11 | Bash scripting, robust scripts, automation patterns | Automated data pipelines and batch jobs | Intermediate |
| 4. System Administration | M12–M15 | Users, groups, permissions, ownership, sudo, environment | Shared dataset servers; safe multi-user data access | Intermediate |
| 5. Software, Storage & Time | M16–M19 | Packages, repos, disks, filesystems, mounting, processes, signals, cron/timers | Dataset storage, long-running training jobs, scheduled ETL | Intermediate → Advanced |
| 6. Services, Networking & Security | M20–M25 | systemd services, networking, SSH, transfer, logs, monitoring, security | Remote GPU servers, ML service logs, server hardening | Advanced |
| 7. The Data Science Stack | M26–M29 | Git, Python/Jupyter, Docker, web servers, databases, deployment | The full DS toolchain, Linux-native | Intermediate |
| 8. Capstone | M30 | End-to-end project integrating all units | A complete, deployed data product | Advanced |

**Suggested pace:** 1 module/week over two semesters, or 2 modules/week over one semester.
Unit 1 is the only unit with zero prerequisites — everything else chains forward.

**Cross-cutting threads** (revisited in most modules, not taught once):

- **Safety:** snapshots before risky work, dry-runs, backups, "never run what you can't explain."
- **Data Science connection:** an explicit section in every module linking skills to DS practice.
- **Reproducibility:** scripts, Git, documentation habits, environment pinning.

---

## Unit 1 — Foundations of Linux (M01–M04)

**Goal:** understand what Linux *is* (kernel vs OS vs distribution), how it's structured,
and get a working Ubuntu environment the student fully controls.

### M01 — What Is Linux?

- **Difficulty:** Beginner
- **Prerequisites:** none
- **Learning objectives**
  - Define an operating system and place the Linux kernel within it.
  - Distinguish kernel, distribution, desktop environment, shell, and terminal.
  - Explain why Linux dominates servers, cloud, and ML infrastructure.
  - Describe open source, free software, and common licenses at a high level.
- **Concepts:** kernel; userspace; GNU userland; POSIX; open source vs free software;
  server vs desktop vs embedded Linux; virtualization preview.
- **Practical skills:** boot a live Ubuntu session (from the VM prepared in M04, or the
  instructor's demo); identify OS version from the terminal.
- **Command-line skills:** first contact — `uname -a`, `cat /etc/os-release`, `lsb_release -a`
  (read-only exploration only).
- **Laboratory:** guided tour of a running Ubuntu system; locate kernel version, OS release,
  desktop environment; compare the same information from a VM vs the host OS.
- **Exercises:** match terms to definitions; identify which layer a component belongs to;
  short-answer "why is Linux used in data centers?"
- **Mini-project:** none (concept module).
- **DS connection:** every JupyterHub, GPU cluster node, and cloud instance the student
  will ever use runs Linux; knowing the vocabulary makes later server work legible.
- **Notes:** no administration; purely conceptual with light terminal exposure.
  **Content status: COMPLETE** — see [content/](modules/M01-what-is-linux/content/README.md):
  8 lessons (26 foundation topics incl. install/VM/WSL2/terminal/help/syntax),
  4 labs, quiz + answer key, 10 challenges, troubleshooting guide. The hands-on
  portion (install, VMs, WSL2) also serves M04; the terminal/help portion serves M05.

### M02 — Linux Distributions

- **Difficulty:** Beginner
- **Prerequisites:** M01
- **Learning objectives**
  - Explain what a distribution packages beyond the kernel.
  - Name the major family trees: Debian → Ubuntu; Red Hat → Fedora/RHEL; SUSE; Arch.
  - Contrast release models: LTS vs interim releases vs rolling releases.
  - Describe package ecosystems: deb/apt vs rpm/dnf, and Ubuntu-only extras (Snap).
- **Concepts:** distribution = kernel + userland + package manager + release policy;
  LTS meaning (5 years of support); release codenames and versioning; upstream/downstream.
- **Practical skills:** determine which distro/release a system runs; read release
  end-of-life dates; verify a download's checksum.
- **Command-line skills:** `cat /etc/os-release`, `lsb_release -a`, `uname -r`,
  `sha256sum` (checksum verification), `lsb_release -d`.
- **Laboratory:** identify the release and support window of the lab VM; compare Ubuntu
  LTS vs interim release timelines; verify the checksum of the Ubuntu ISO used in M04.
- **Exercises:** pick a distro for three scenarios (student laptop, university GPU server,
  appliance) and justify; decode a version string like `24.04.2 LTS`.
- **Mini-project:** "Distro report" — one page on a chosen distro: family, package
  manager, release policy, one real-world DS user.
- **DS connection:** most research clusters and cloud images run Ubuntu LTS or RHEL-family
  systems; knowing which ecosystem you're in tells you which package commands apply.
- **Notes:** distribution-aware framing starts here — apt vs dnf vs pacman named side by
  side, but the course *practices* apt/Ubuntu.

### M03 — Linux Architecture

- **Difficulty:** Beginner
- **Prerequisites:** M01, M02
- **Learning objectives**
  - Sketch the layers: hardware → kernel → system libraries → userland tools → shell → GUI.
  - Explain what the kernel manages: processes, memory, devices, filesystems, network.
  - Describe the role of system daemons and `systemd` at a beginner's level.
  - Explain "everything is a file" and why it matters.
- **Concepts:** monolithic kernel + modules; user space vs kernel space; system calls;
  daemons; virtual filesystem (`/proc`, `/sys`); device files; TTY vs terminal emulator.
- **Practical skills:** observe kernel state through `/proc` and `/sys` read-only files.
- **Command-line skills:** `cat /proc/cpuinfo`, `cat /proc/meminfo`, `uname -r`,
  `ls /sys/block`, `lsblk`, `lscpu`, `free -h`.
- **Laboratory:** map the student's own machine: CPUs, memory, block devices, kernel
  version; identify three daemons running on the system (via `ps` read-only peek; full
  process management comes in M18).
- **Exercises:** fill-in-the-layer diagrams; "which layer handles X?" questions;
  predict-then-verify for `/proc` file contents.
- **Mini-project:** none.
- **DS connection:** ML workloads stress exactly these resources — CPU, RAM, GPU, disk
  I/O. Architecture knowledge underpins every later monitoring and performance topic.
- **Notes:** keep `systemd` at "it's the init system and service manager" depth; M20 goes deep.

### M04 — Installing Ubuntu in a VM

- **Difficulty:** Beginner (hands-on)
- **Prerequisites:** M01–M03 (can run in parallel with M02/M03)
- **Learning objectives**
  - Install VirtualBox (or verify an instructor-provided alternative) and create a VM.
  - Install Ubuntu LTS inside the VM with sensible, safe defaults.
  - Take, restore, and delete VM snapshots.
  - Understand WSL2 as a lightweight alternative and when it is *not* equivalent.
- **Concepts:** virtual machines vs physical machines; hypervisor; disk image; snapshot
  vs backup; host vs guest; why sandboxing makes practice safe; WSL2 architecture
  (a real Linux kernel in a lightweight utility VM).
- **Practical skills:** full Ubuntu install: partitioning defaults, user creation
  (non-root admin user), updates; Guest Additions; snapshot workflow; shared folders.
- **Command-line skills:** inside the fresh install — `hostname`, `whoami`, `id`,
  `sudo apt update` (first apt exposure), `shutdown`/`reboot` awareness (VM context only).
- **Laboratory:** install Ubuntu 24.04 LTS in VirtualBox with a 2-CPU/4-GB spec, take a
  **snapshot named `M04-clean-install`**, update all packages, create a shared folder,
  and write the first `lab-log.md` entry.
- **Exercises:** recovery drill — break something trivial (e.g., remove a dotfile),
  restore the snapshot, document what was lost and why snapshots ≠ backups.
- **Mini-project:** none — but the VM built here is the course's primary laboratory.
- **DS connection:** the same workflow (create instance → snapshot → install stack →
  snapshot) is exactly how students will later manage cloud GPU instances.
- **Notes:** WSL2 alternative path documented in [SETUP.md](SETUP.md). Explicit warning:
  snapshots are instant rollbacks, not backups — the backup unit (M24/M17 context) returns
  to this. Students without admin rights on lab PCs use instructor-managed VMs or WSL2.

---

## Unit 2 — Command Line Fluency (M05–M09)

**Goal:** make the terminal the student's default tool. By the end of this unit, exploring
and reshaping a text dataset in the shell feels natural.

### M05 — The Terminal & Shell

- **Difficulty:** Beginner
- **Prerequisites:** M04
- **Learning objectives**
  - Explain shell vs terminal vs console, and the role of Bash.
  - Run commands with arguments and options; read command help and man pages.
  - Use tab completion, command history, and basic line editing.
  - Understand the prompt, the PATH lookup concept (intro level), and exit codes.
- **Concepts:** REPL model of the shell; `command [options] [arguments]` syntax;
  man page sections; `--help`; history; `Ctrl+C` vs `Ctrl+D`; shell as a programming
  language (preview for M10).
- **Practical skills:** fluent man navigation; `history` and reverse search (`Ctrl+R`);
  keyboard shortcuts; `echo $?` exit codes.
- **Command-line skills:** `man`, `info`, `whatis`, `which`, `type`, `history`,
  `clear`, `echo`, `date`, `exit`.
- **Laboratory:** man-page scavenger hunt; build a personal history of 20 commands and
  annotate each with what it does; exit-code exploration (`ls /`, `ls /nonexistent`, `echo $?`).
- **Exercises:** predict-the-output drills; find the man page for a given task; explain
  the difference between `man rm` sections and `rm --help`.
- **Mini-project:** none.
- **DS connection:** reading documentation is the core survival skill for any sysadmin or
  data engineer; man pages and `--help` are the first place to look on a compute server.
- **Notes:** introduces "type it, don't paste it" discipline that persists course-wide.
  **Content status: PARTIAL** — aliases & history complete in
  [content Lesson 5](modules/M05-terminal-and-shell/content/lessons/05-aliases-and-history.md)
  (+Lab 3, quiz); first-contact lessons 5–7 of M01 cover terminal/help/syntax;
  shell types/startup files/job-control remain for the content phase.

### M06 — Filesystem Hierarchy & Navigation

- **Difficulty:** Beginner
- **Prerequisites:** M05
- **Learning objectives**
  - Describe the single-tree filesystem and the purpose of the FHS top-level directories.
  - Navigate fluently with absolute and relative paths (`/`, `.`, `..`, `~`, `-`).
  - Distinguish absolute vs relative paths and construct both for any target.
  - Understand hidden files and user home layout.
- **Concepts:** FHS (`/bin`, `/etc`, `/home`, `/var`, `/tmp`, `/usr`, `/opt`, `/root`,
  `/proc`, `/dev`, `/mnt`, `/media`); mount points (concept); case sensitivity; hidden
  dotfiles; home directory conventions.
- **Practical skills:** confident movement anywhere in the tree without getting lost;
  explaining what each top-level directory is for.
- **Command-line skills:** `pwd`, `cd`, `ls` (`-l`, `-a`, `-h`, `-R`, `-t`), `tree`
  (if installed), `realpath`, `basename`, `dirname`.
- **Laboratory:** filesystem treasure hunt (find specific files under `/etc`, `/usr/share/doc`);
  draw the tree under the user's home; classify 15 real paths as absolute/relative.
- **Exercises:** path resolution drills (`cd` chains — where are you now?); FHS matching;
  hidden-file discovery.
- **Mini-project:** none.
- **DS connection:** datasets, code, and results each get their own place in the tree;
  students set up a personal convention (`~/data`, `~/projects`, `~/archive`) used for
  the rest of the course.
- **Notes:** `tree` may need `sudo apt install tree` — first deliberate install, foreshadowing M16.
  **Content status: COMPLETE** — see [content/](modules/M06-filesystem-hierarchy/content/lessons/01-navigation-pwd-ls-cd.md):
  4 lessons, 2 labs, quiz+key, challenges, troubleshooting.

### M07 — Files, Directories & Text Files

- **Difficulty:** Beginner
- **Prerequisites:** M06
- **Learning objectives**
  - Create, copy, move, rename, and delete files and directories safely.
  - Read text files with pager tools and understand text vs binary.
  - Use glob patterns to select multiple files.
  - Apply safe-deletion habits (trash-first thinking, `ls` before `rm`, quoting).
- **Concepts:** filenames and extensions (informational, not enforcing); globs `*`, `?`,
  `[...]`; brace expansion; text encodings (ASCII/UTF-8) and line endings (LF vs CRLF);
  paging; hard vs soft differences between copy and move; **why `rm` is permanent**.
- **Practical skills:** reliable file manipulation; reading files without editors;
  batch operations over many files via globs.
- **Command-line skills:** `touch`, `mkdir -p`, `cp` (`-r`, `-i`), `mv` (`-i`),
  `rm` (`-i`, `-r` — **with explicit safety framing**), `rmdir`, `cat`, `less`,
  `head`, `tail` (`-f`), `wc`, `file`, `stat`, `du`, `df` (first look).
- **Laboratory:** build a project skeleton from scratch (data/, code/, results/);
  operate on the `datasets/` samples: view heads/tails, count lines, check file types;
  **safety lab:** run `rm -i` on a test directory, observe prompts, then `rm -rf` on a
  *dedicated sandbox folder* while the instructor explains exactly what the flags mean.
- **Exercises:** glob challenges; file-type identification; line-ending conversion
  observation; `less` navigation checks.
- **Mini-project:** "Dataset audit" — produce `audit.md` describing every file in a given
  dataset directory: type, size, line counts, encoding notes (M07-level tools only).
- **DS connection:** datasets live as files; `head`/`tail`/`wc` are the first tools used
  on any new data file; `tail -f` is how you watch a training run's log later (M18/M24).
- **Notes:** the `rm` safety lab is mandatory. Destructive commands are taught *with*
  their safeguards, never withheld — the course explains them so students aren't helpless.
  **Content status: COMPLETE** — see [content/](modules/M07-files-and-directories/content/lessons/01-file-operations-cp-mv-rm.md):
  4 lessons, 2 labs, quiz+key, challenges, troubleshooting.

### M08 — Text Processing Toolkit

- **Difficulty:** Intermediate
- **Prerequisites:** M07
- **Learning objectives**
  - Search text with `grep` using literals, basic regex, and useful options.
  - Transform and extract with `sed`, `sort`, `cut`, `tr`, `uniq`, `comm`.
  - Understand CSV/TSV structure and the risks of naive splitting.
  - Combine two or three of these tools in a short manual pipeline.
- **Concepts:** regular expressions (literal, `.`, `*`, `[]`, `^`, `$`, `\d` vs `[0-9]`);
  line-oriented model; fields and delimiters; sorting keys and locale (`sort` options);
  stream vs file editing (`sed -i` caution); counting and deduplication patterns.
- **Practical skills:** locate rows of interest; extract columns; clean whitespace;
  sort and deduplicate; quick frequency counts.
- **Command-line skills:** `grep` (`-i`, `-v`, `-n`, `-c`, `-r`, `-E`, `-w`),
  `sed` (`s///`, `-n` + `p`, `-i.bak`), `sort` (`-n`, `-r`, `-k`, `-u`, `-t`),
  `cut` (`-d`, `-f`), `tr` (`-d`, `-s`, sets), `uniq` (`-c`, `-d`), `comm`, `diff`,
  `nl`, `column` (where available).
- **Laboratory:** on `datasets/sales-2019-q1.csv` and the logs: filter invalid emails,
  extract a column of IDs, sort by amount, top-10 frequency table for a categorical column,
  clean stray whitespace/line endings from a raw file (using `.bak` safety).
- **Exercises:** 12 regex extraction drills; "produce this report in one command" tasks;
  CSV gotcha spotting (commas inside quoted fields).
- **Mini-project:** "Data quality report" — a single-page summary of one dataset:
  row counts, distinct values of key columns, rows matching known bad patterns.
- **DS connection:** this *is* command-line data analysis: profiling, cleaning, and
  summarizing before any Python or pandas is involved. These skills scale to files too
  big to open in an editor (full treatment in M09/M11).
- **Notes:** regex taught at ERE level (`grep -E`, `sed -E`) with pointers to deeper
  references; no `awk` yet — M09 introduces it deliberately.

### M09 — Pipes, Redirection & Filters

- **Difficulty:** Intermediate
- **Prerequisites:** M08
- **Learning objectives**
  - Explain stdin/stdout/stderr and how pipes connect processes.
  - Redirect output and errors to files; append; use `tee`; feed input from files.
  - Compose multi-stage pipelines over large files efficiently.
  - Introduce `awk` as a field-aware filter and mini-language.
  - Apply `find` and `xargs` to operate on sets of files.
- **Concepts:** file descriptors (0, 1, 2); `|`, `>`, `>>`, `<`, `2>`, `2>&1`, `&>`;
  `tee`; pipelines as data streams (no intermediate files); filter pattern;
  `awk` fields/records, patterns and actions, BEGIN/END basics; `find` predicates
  and actions; `xargs` batching and `xargs -0`; command substitution `$(...)` preview.
- **Practical skills:** build 4+ stage pipelines; process files larger than RAM;
  find files by name/size/type and act on them; count and aggregate on the fly.
- **Command-line skills:** `awk` (fields `$1`, `-F`, `NF`, `NR`, `BEGIN/END`, simple
  sums/averages), `find` (`-name`, `-type`, `-size`, `-mtime`, `-maxdepth`, `-exec`),
  `xargs` (`-n`, `-I`, `-0`, `-P` intro), `tee`, `wc -l`, `sort | uniq -c | sort -rn`
  idiom, `time`.
- **Laboratory:** log analysis pipeline on `datasets/server.log` (requests/hour, top
  client IPs, error rates); find-and-report for oversized files in a fake tree; a
  pipeline that processes a 500 MB generated file interactively (measure with `time`).
- **Exercises:** 10 pipeline puzzles (from spec to one-liner); convert an `xargs` task
  to `-exec` and back; explain what breaks if `sort` is removed at a given stage.
- **Mini-project:** "One-liner analyst" — solve 5 data questions about a dataset where
  each answer is a single pipeline, saved in `answers.md` with explanations.
- **DS connection:** the Unix pipeline is the original streaming data tool: profile
  5 GB of logs with no editor, no notebook, no RAM blow-up. Piping into `sort`/`awk`/
  `uniq` is the quick first pass before loading data into pandas or Spark.- **Notes:** performance framing introduced (streaming vs loading everything into
  memory) — deepens in M18 (`nice`, background jobs) and M11 (scripted pipelines).
  **Content status: PARTIAL** — streams/pipelines core complete in
  [content](modules/M09-pipes-and-redirection/content/lessons/01-stdin-stdout-stderr-redirection.md)
  (2 lessons, 2 labs, quiz+key, challenges, troubleshooting); find/xargs/awk-depth
  lessons remain for the content phase.

---

## Unit 3 — Shell Scripting & Automation (M10–M11)

**Goal:** turn interactive one-liners into reusable, robust, automated scripts. This is
where "terminal user" becomes "administrator of their own data workflows."

### M10 — Bash Scripting

- **Difficulty:** Intermediate
- **Prerequisites:** M09 (M08 strongly recommended)
- **Learning objectives**
  - Write and run Bash scripts with a shebang, comments, and readable structure.
  - Use variables, quoting rules, and command substitution correctly.
  - Control flow with `if/elif/else`, comparisons (`[ ]`, `[[ ]]`), and `case`.
  - Iterate with `for` and `while` loops; use `read` for input and line processing.
  - Handle arguments with `$1..$n`, `$#`, `$@`, and basic usage checks.
  - Check exit codes (`$?`, `set -e`, `set -u`, `set -o pipefail`) and fail loudly.
  - Write scripts that log what they do.
- **Concepts:** shebang (`#!/usr/bin/env bash`); strict mode; quoting (weak vs strong);
  word splitting; exit statuses; functions; local variables; script vs interactive shell;
  `bash -n` syntax checking; `shellcheck` as a quality gate.
- **Practical skills:** write a script from a plain-language spec; debug with `bash -x`;
  install and act on `shellcheck` findings; make scripts executable (`chmod +x` — first
  permission exposure, formalized in M12).
- **Command-line skills:** `bash`, `bash -n`, `bash -x`, `chmod +x`, `shellcheck`
  (apt package `shellcheck`), `read`, `test`/`[[`, `printf`, `local`, `shift`, `getopts` (intro).
- **Laboratory:** build `resize_and_rename.sh` (batches the M07/M08 file ops over globs);
  build `dq.sh` — wraps the M09 data-quality pipeline in a script taking a file argument,
  with usage help, argument validation, strict mode, and a log line per step.
- **Exercises:** 8 fix-the-bug scripts (classic quoting/exit-code mistakes);
  convert 3 M09 one-liners into parameterized scripts; write tests-as-expectations
  ("given X input, script must produce Y") for one script.
- **Mini-project:** **Mini-Project A — "Dataset QC toolkit"**: a small script suite
  (`dq.sh`, `summary.sh`, optional `clean.sh`) over the course datasets, documented in
  `README.md` inside the project folder, all passing `shellcheck`.
- **DS connection:** data work is repetitive: cleaning, converting, and loading happen
  weekly. A script that re-runs your pipeline with one command is the first step toward
  reproducible, schedulable data engineering (realized in M19).
- **Notes:** shellcheck required from here on: any submitted script must pass it.

### M11 — Advanced Shell & Automation

- **Difficulty:** Intermediate
- **Prerequisites:** M10
- **Learning objectives**
  - Process files line-by-line and stream-by-stream correctly (`while read`, `IFS`).
  - Use traps for cleanup; manage temp files and temp directories safely.
  - Compose pipelines inside scripts and route errors to logs.
  - Apply safe-automation patterns: dry-run, backup-before-modify, idempotency.
  - Parse simple configs; use `getopts` for real CLI options.
  - Schedule scripts (awareness level) — full treatment in M19.
- **Concepts:** `while read` loops and `IFS`; process substitution `<(...)`; `trap`
  (`EXIT`, `INT`, `TERM`); `mktemp`; idempotency; dry-run pattern; lock files (concept);
  atomic-ish writes (write temp, then `mv`); structured log output; `nohup`/`&` awareness.
- **Practical skills:** write a script that is safe to re-run and safe to interrupt;
  add `--dry-run`; implement backup-before-edit via `cp` + timestamped suffix;
  `getopts` option parsing with help text.
- **Command-line skills:** `trap`, `mktemp`, `nohup`, `jobs`/`fg`/`bg` (preview of M18),
  `getopts`, `wait`, `rsync` (first look, backup pattern only — depth in M23).
- **Laboratory:** harden `dq.sh`: add `--dry-run`, `--out`, `-h`, trap-based temp cleanup,
  timestamped logs to `logs/`; break it mid-run with Ctrl+C and verify cleanup ran.
- **Exercises:** convert a fragile script into an idempotent one; find and fix three
  quoting bugs; write a dry-run for a rename task over 100 files.
- **Mini-project:** none (absorbed into Mini-Project A hardening).
- **DS connection:** production data pipelines are re-runnable and interruptible;
  the same hardening patterns apply to scripts that will later run under cron (M19)
  or inside containers (M28).
- **Notes:** `trap`/cleanup patterns here also prepare students for M18's signal handling.

---

## Unit 4 — System Administration (M12–M15)

**Goal:** multi-user thinking. Who may read, write, or execute what — and how an admin
grants access safely. Directly models a shared dataset server.

### M12 — Users, Groups & Permissions

- **Difficulty:** Intermediate
- **Prerequisites:** M10
- **Learning objectives**
  - Explain the permission model: user/group/other × read/write/execute.
  - Interpret `ls -l` output fully, including file types and permission bits.
  - Change permissions with symbolic and octal `chmod`.
  - Understand `umask` and predict permissions of new files.
  - Inspect users and groups (`/etc/passwd`, `/etc/group`, `id`, `getent`).
  - Distinguish root vs regular users; recognize sudo membership (`id`, `groups`).
- **Concepts:** UIDs/GIDs; rwx on files vs directories (execute-on-directory meaning);
  octal arithmetic; umask; special bits (setuid/setgid/sticky) at recognition level;
  system vs human users; primary vs supplementary groups.
- **Practical skills:** set and audit permissions; predict access outcomes; explain why
  a given access works or fails (permission debugging).
- **Command-line skills:** `chmod` (symbolic + octal), `umask`, `id`, `whoami`, `groups`,
  `getent passwd/group`, `ls -l` deep read, `stat` permission fields.
- **Laboratory:** build a multi-user sandbox: with instructor-provided test accounts (or
  documented `useradd` practice in the VM), create a shared group, a shared directory,
  and files readable/writable by different combinations; verify outcomes as different users.
- **Exercises:** 15 `ls -l` decoding drills; octal↔symbolic conversion; permission
  prediction puzzles; find-the-misconfigured-file in a prepared tree.
- **Mini-project:** none.
- **DS connection:** shared dataset directories on lab/GPU servers use exactly this
  model: group-writable dataset folders, read-only for everyone else. Understanding
  rwx is a prerequisite for the shared-data patterns in M13.
- **Notes:** user/group *modification* commands (`useradd`, `groupadd`, `chown`) are
  introduced here read-only and formally taught in M13/M14 where sudo context is available.

### M13 — Ownership & Shared Access

  **Content status: COMPLETE** — see [content/](modules/M13-ownership-shared-access/content/README.md):
  [Lesson 1](modules/M13-ownership-shared-access/content/lessons/01-ownership-chown-shared-dirs.md)
  (ownership, shared dirs, sticky bit, constitutional tree),
  [Lesson 2](modules/M13-ownership-shared-access/content/lessons/02-acls-permission-clinic.md)
  (ACLs, mask, default ACLs, clinic method),
  [Lab 1](modules/M13-ownership-shared-access/content/labs/lab-01-build-shared-tree.md)
  (build the shared tree),
  [Lab 2](modules/M13-ownership-shared-access/content/labs/lab-02-permission-clinic.md)
  (diagnose-and-fix clinic, patients A–F incl. NFS ticket),
  [quiz](modules/M13-ownership-shared-access/content/practice/quiz.md) +
  [challenges](modules/M13-ownership-shared-access/content/practice/challenges.md),
  [troubleshooting](modules/M13-ownership-shared-access/content/troubleshooting.md).

- **Difficulty:** Intermediate
- **Prerequisites:** M12
- **Learning objectives**
  - Change ownership and group with `chown`/`chgrp` (in VM sandbox with sudo).
  - Apply the shared-directory pattern: group ownership + setgid + group-writable.
  - Use ACLs to grant a specific user access beyond the classic model.
  - Design an access plan for a shared dataset server.
  - Use `sudo` to administer (introduced practically; principles deepened in M14).
- **Concepts:** user:group ownership model; setgid on directories (inheritance);
  sticky bit on shared-write dirs; access control lists (`getfacl`, `setfacl`, mask);
  default ACLs; "least privilege" as a design principle.
- **Practical skills:** implement group-shared dataset folders that stay group-writable
  as members add files; grant one extra user access via ACL without opening to world;
  audit a directory tree's ownership.
- **Command-line skills:** `chown`, `chgrp`, `chmod g+s`, `chmod +t`, `umask 0002` in
  shared contexts, `getfacl`, `setfacl` (`-m u:user:rwx`, `-d` default ACLs, `-x`, `-b`).
- **Laboratory:** in the VM: create `datasets` and `results` groups; build a shared
  tree where two test users collaborate on a dataset folder; verify setgid inheritance
  and default ACLs; deliberately misconfigure one file and fix it via audit.
- **Exercises:** design access plans for 3 scenarios (course staff + students; two
  research groups sharing one server; public-download folder); ACL syntax drills;
  predict-then-verify access matrices.
- **Mini-project:** **Mini-Project B — "Shared dataset server design"**: a document +
  scripted demo (`setup_shared_tree.sh`) that creates the users, groups, directories,
  and ACLs for a fictional 6-person research team, with a written rationale per decision.
- **DS connection:** research data is shared: TAs grade student folders, lab members
  write to common dataset dirs, public data must be world-readable. This module is the
  direct answer to "how do we share data without leaks?"
- **Notes:** all chown/setfacl work happens in the VM; on shared machines students only
  *inspect* (getfacl/ls) — modifying is admin-only. Least-privilege habit starts here.

### M14 — Sudo & the Root Principle

  **Content status: COMPLETE** — see [content/](modules/M14-sudo-root-principle/content/README.md):
  [Lesson](modules/M14-sudo-root-principle/content/lessons/01-root-sudo-sudoers.md)
  (root/UID 0, su vs sudo, sudoers + visudo + drop-ins, NOPASSWD, Defaults,
  five-beat workflow),
  [Lab 1](modules/M14-sudo-root-principle/content/labs/lab-01-sudo-practice.md)
  (mechanics, audit trail, redirection wall, scoped drop-in, safe
  break-and-repair),
  [Lab 2](modules/M14-sudo-root-principle/content/labs/lab-02-sudo-incidents.md)
  (three repair tickets),
  [quiz](modules/M14-sudo-root-principle/content/practice/quiz.md) +
  [challenges](modules/M14-sudo-root-principle/content/practice/challenges.md),
  [troubleshooting](modules/M14-sudo-root-principle/content/troubleshooting.md).
  All practice scoped to the student's own VM/WSL2.

- **Difficulty:** Intermediate
- **Prerequisites:** M12, M13
- **Learning objectives**
  - Explain root, sudo, and why direct root logins are discouraged.
  - Use sudo correctly for package, service, and user administration.
  - Read sudoers policy basics (`/etc/sudoers.d/`, groups `sudo`/`wheel`) read-only.
  - Apply least-privilege habits: escalate only the commands that need it.
  - Recognize how `sudo` changes file ownership pitfalls (root-owned artifacts).
- **Concepts:** superuser; sudo vs su; sudo groups; per-command authorization;
  `sudo -l`; password caching; environment sanitization; root-owned file traps;
  audit trail via sudo logs.
- **Practical skills:** run elevated commands deliberately; diagnose "permission
  denied" vs "not in sudoers"; avoid creating root-owned files in your own dirs.
- **Command-line skills:** `sudo` (`-i`, `-s`, `-u`, `-l`, `!!` idiom), `su` (concept),
  `pkexec` awareness, `visudo` (instructor demo only, never edited by students).
- **Laboratory:** guided sudo practice in the VM: install a package, create a test user,
  fix one root-owned file; inspect `sudo -l` and journalctl sudo entries; compare an
  admin user vs a non-admin test user.
- **Exercises:** classify 10 tasks as needing sudo or not; explain each sudo flag;
  spot-the-risk scenarios (piping curl to shell, `sudo rm` mistakes) with safer
  alternatives.
- **Mini-project:** none.
- **DS connection:** on GPU servers students will never get root — they'll use sudo
  sparingly, if at all. Knowing *what needs* elevation (and what doesn't) prevents both
  lockouts and reckless escalation; installing their own tools usually doesn't need it.
- **Notes:** course-wide rule stated here: sudo in the sandbox VM for practice; on real
  shared servers, ask an admin. Never disable password prompts; never edit sudoers by hand.

### M15 — Environment Variables & Configuration

- **Difficulty:** Intermediate
- **Prerequisites:** M10
- **Learning objectives**
  - Explain environment vs shell variables; inheritance and scope.
  - Inspect and set variables (`env`, `printenv`, `export`, `unset`).
  - Read and edit shell startup files (`.bashrc`, `.profile`) safely (with backups).
  - Understand PATH manipulation and diagnose "command not found."
  - Use env vars as configuration (keys, URLs, options) in scripts and Python.
  - Take aliases, functions, and dotfile backups into their personal setup.
- **Concepts:** process environment; `export` semantics; variable expansion in quotes;
  login vs non-login, interactive vs non-interactive shells and which rc files run;
  PATH order; `~/.local/bin`; dotfile management and versioning; secrets in env vars
  (basic hygiene: don't commit them).
- **Practical skills:** make persistent, reversible shell customizations; debug PATH;
  pass configuration into scripts and Python via environment (preview of venv activation
  in M27 and container env in M28).
- **Command-line skills:** `env`, `printenv`, `export`, `unset`, `alias`, `unalias`,
  `source`, `set`/`env | sort`, `hostnamectl` awareness; startup-file editing with
  backup-then-edit discipline (`cp .bashrc .bashrc.bak-$(date +%F)`).
- **Laboratory:** create a personal `~/.local/bin`, add it to PATH, write two aliases
  and one function; break PATH deliberately in a *subshell* and recover; back up and
  restore dotfiles; document a personal environment in `dotfiles.md`.
- **Exercises:** predict-the-env drills (what does the child see?); PATH debugging
  scenarios; spot the unquoted-variable bug; explain export vs plain assignment.
- **Mini-project:** none.
- **DS connection:** environment variables configure everything in data science:
  `VIRTUAL_ENV`, `PYTHONPATH`, API keys, `CUDA_VISIBLE_DEVICES`, `HF_HOME` for model
  caches, database URLs. Environment hygiene is the difference between "works on my
  machine" and reproducible runs.
- **Notes:** secrets hygiene introduced (no keys in committed files) — deepened in M25
  and M29; ties to Git-awareness in M26.

---

## Unit 5 — Software, Storage & Time (M16–M19)

**Goal:** keep a system current, manage its disks and processes, and make work happen
on schedule — the core "keep it running" skills.

### M16 — Package Management

  **Content status: COMPLETE** — see [content/](modules/M16-package-management/content/README.md):
  [Lesson 1](modules/M16-package-management/content/lessons/01-apt-dpkg-fundamentals.md)
  (packages, dpkg, apt lifecycle, dependencies, check-first workflow),
  [Lesson 2](modules/M16-package-management/content/lessons/02-repositories-security-ppas.md)
  (repository components, apt signing, PPAs & risks, security updates,
  unattended-upgrades),
  [Lesson 3](modules/M16-package-management/content/lessons/03-beyond-apt-rpm-source.md)
  (source builds + prefix hygiene, DEB↔RPM conceptual map, the DS
  toolchain: apt vs pip/conda vs Git),
  [Lab 1](modules/M16-package-management/content/labs/lab-01-package-explorer.md)
  (read-only explorer),
  [Lab 2](modules/M16-package-management/content/labs/lab-02-safe-lifecycle.md)
  (safe install→verify→remove),
  [Lab 3](modules/M16-package-management/content/labs/lab-03-repo-audit.md)
  (repo audit + PPA test-drive + security-debt dry-run),
  [quiz](modules/M16-package-management/content/practice/quiz.md) +
  [challenges](modules/M16-package-management/content/practice/challenges.md),
  [troubleshooting](modules/M16-package-management/content/troubleshooting.md).

- **Difficulty:** Intermediate
- **Prerequisites:** M04, M14
- **Learning objectives**
  - Explain packages, repositories, and dependency resolution.
  - Use `apt` to search, inspect, install, upgrade, and remove software.
  - Manage repositories and keys safely (understand what `add-apt-repository` does).
  - Install software outside apt: .deb files, `dpkg -i`, and when to avoid it.
  - Contrast deb/apt with rpm/dnf, pacman, and Snap/Flatpak at a working level.
  - Pin versions and read package metadata; audit what is installed.
- **Concepts:** package = binaries + metadata + dependency graph; signed repos and keyrings;
  `sources.list` and `sources.list.d/`; `apt update` vs `apt upgrade` vs
  `apt full-upgrade`; `apt-cache`; dpkg below apt; pinning/holding packages;
  snap/flatpak trade-offs; unattended upgrades (concept).
- **Practical skills:** confidently install and remove software without breaking the
  system; read apt output; fix "held broken packages" style problems by reading, not
  guessing; verify what version is installed and from where.
- **Command-line skills:** `apt update`, `apt search/show/list`, `apt install`
  (`--no-install-recommends` awareness), `apt upgrade`, `apt remove` vs `apt purge`,
  `apt autoremove`, `apt-cache policy`, `dpkg -l/-i/-r`, `apt-mark hold/unhold`,
  `add-apt-repository` (with explanation), `snap` (list, info) — plus a dnf/pacman
  translation table in notes.
- **Laboratory:** install the course toolchain (tree, shellcheck, htop, jq, tmux,
  build-essential, python3-venv, python3-pip) via apt; inspect before/after with
  `apt list --installed`; add a well-known repository and install from it; hold a
  package version; simulate and resolve one dependency conflict in the sandbox.
- **Exercises:** 10 "install me X" tasks with constraints (no recommends, specific
  version); read a real apt error and propose the fix; distro-translation drills.
- **Mini-project:** none — but the toolchain installed here powers everything after.
- **DS connection:** Python/R/cuda toolkits, database servers, and build tools all arrive
  via packages; on shared clusters you can't install system-wide but *can* use user-space
  alternatives (pip/conda/Micromamba — bridged in M27); repo trust and version pinning
  are reproducibility cornerstones.
- **Notes:** repository awareness includes *adding* third-party repos only after
  explaining trust and key checking; students practice in the VM only.

### M17 — Storage, Disks & Filesystems

- **Difficulty:** Intermediate → Advanced
- **Prerequisites:** M12, M16
- **Learning objectives**
  - Read `lsblk`/`df`/`du` output and map a system's storage topology.
  - Explain partitions, filesystems, mount points, and UUIDs.
  - Create, format, mount, and unmount a disk (in the VM, on a virtual disk).
  - Configure persistence via `/etc/fstab` safely (with `nofail`, backups, `findmnt --verify`).
  - Check and repair filesystems conceptually (`fsck` usage and danger framing).
  - Measure usage; find what consumes space; plan dataset storage.
  - Know LVM and logical volumes at concept level.
- **Concepts:** MBR vs GPT; partition types; ext4 vs xfs; swap; mounting; `/etc/fstab`
  fields; UUIDs vs device names; `nofail`/`noatime` options; filesystem checks;
  LVM (PV/VG/LV) concepts; network storage preview (NFS) for clusters; disk images.
- **Practical skills:** add a virtual disk to the VM, partition (`parted`), format
  (`mkfs.ext4`), mount, persist in fstab — and undo it all cleanly; audit disk usage;
  build a `datasets` volume layout for a fictional lab server.
- **Command-line skills:** `lsblk -f`, `blkid`, `df -h`, `du -h --max-depth`, `ncdu`
  (optional install), `parted` (print, mklabel, mkpart), `mkfs.ext4`, `mount`/`umount`,
  `findmnt`, `findmnt --verify`, `sudo blkid` + fstab editing with backup, `fsck`
  (concept + unmounted-only rule), `mount -o remount,ro` awareness, LVM
  (`pvs/vgs/lvs`) recognition only.
- **Laboratory:** the **disk lab** (snapshot first!): attach a 2 GB virtual disk,
  partition, format, mount at `/mnt/data`, copy datasets onto it, add fstab entry with
  `nofail`, verify with `findmnt --verify`, then cleanly remove the disk. Second lab:
  `du`-based space audit of the VM with a written cleanup plan.
- **Exercises:** storage topology reading drills; fstab line decoding; "where did my
  disk go" scenarios (unmounted volume, full /tmp, wrong UUID); plan storage for a
  2 TB dataset server.
- **Mini-project:** none (the disk lab is the artifact).
- **DS connection:** datasets are the biggest storage consumers in DS work; knowing how
  to mount a dedicated data volume, read `df` before a big download, and audit space
  with `du` prevents the classic "disk full mid-training-run" disaster on GPU servers.
- **Notes:** the most safety-sensitive module of the course: every destructive step
  (`parted`, `mkfs`) happens on a *dedicated virtual disk* after a snapshot, with the
  system disk explicitly named and avoided. fstab errors can block boot — backup +
  `findmnt --verify` + snapshot recovery demonstrated.

### M18 — Processes, Jobs & Signals

- **Difficulty:** Intermediate → Advanced
- **Prerequisites:** M05, M15
- **Learning objectives**
  - Explain processes, PIDs, parent-child trees, and process states.
  - Observe processes with `ps` and `top`/`htop`; interpret CPU/memory columns.
  - Run, pause, resume, and terminate foreground/background jobs.
  - Send signals; know the difference between SIGTERM and SIGKILL, and why to prefer TERM.
  - Adjust priority with `nice`/`renice`; understand load average vs CPU %.
  - Keep long jobs alive after logout (`nohup`, `setsid` intro) — SSH depth in M22.
  - Read `/proc/<pid>` for a live process.
- **Concepts:** process lifecycle; states (R/S/D/Z/T); signals as IPC; default signals
  for Ctrl+C/Ctrl+Z; TERM vs KILL semantics (KILL cannot be caught); exit codes;
  zombies; load average interpretation; OOM killer concept; cgroups awareness
  (M28 connection); `/proc` per-process files.
- **Practical skills:** diagnose a slow machine from `top`/`htop` evidence; run a
  training-like long job in the background and monitor it; stop a runaway process
  politely, then forcefully; renice a background job to keep the desktop responsive.
- **Command-line skills:** `ps aux`, `ps -ef`, `ps -u user`, `pgrep`/`pkill` (careful
  framing), `top`, `htop`, `kill` (`-TERM`, `-KILL`, `-HUP`), `killall` (caution),
  `jobs`, `bg`, `fg`, `Ctrl+Z`, `nohup`, `nice`, `renice`, `uptime`, `free -h`,
  `lsof` (intro), `watch`, `vmstat` (intro).
- **Laboratory:** run `stress`-like loops (a provided script) and watch htop; job-control
  circuit: start/suspend/resume/background/kill a long pipeline; TERM vs KILL lab with a
  trap-aware script (builds on M11); renice demo; `/proc/<pid>` exploration worksheet.
- **Exercises:** process-tree puzzles; "the laptop is slow" diagnosis scenarios;
  signal-choice drills (which signal, and why); predict exit codes.
- **Mini-project:** **Mini-Project C — "Process watchdog"**: a script that monitors a
  target process, logs CPU/MEM samples to CSV at intervals, and reports overruns —
  combining M10/M11 scripting with M18 observation (CSV output ready for plotting).
- **DS connection:** training runs *are* processes: check GPU/CPU/memory of your jobs,
  background a 6-hour fit, stop it cleanly without corrupting checkpoints, and keep it
  running after you log out. Load-average literacy prevents "the server is slow" panic.
- **Notes:** `pkill`/`killall` taught with explicit pattern-matching dangers (killing
  the wrong process); kill-your-own-processes only.

### M19 — Scheduling: cron, systemd timers

- **Difficulty:** Advanced
- **Prerequisites:** M10, M11, M18
- **Learning objectives**
  - Explain scheduling use cases and cron vs systemd timer trade-offs.
  - Read and write crontab syntax fluently; use `@reboot`/`@daily` shortcuts.
  - Manage user crontabs safely (`crontab -e`/`-l`, never edit files directly).
  - Redirect job output to logs; make scheduled jobs quiet when successful.
  - Create a systemd timer + service pair for a user-level job.
  - Schedule a real data pipeline end-to-end with logging, locking, and failure notices.
- **Concepts:** five-field cron syntax; user vs system crontabs; environment differences
  in cron (PATH!); cron's mail spool concept; `anacron` awareness; systemd timer
  (`OnCalendar`, `Persistent=true`), service integration; `journalctl -u` for timer logs;
  overlapping-run protection (lockfiles from M11); idempotency requirement.
- **Practical skills:** convert plain-language schedules into cron fields and back;
  write jobs that log and fail loudly; choose cron vs timer per use case; verify a job
  *actually ran* via logs rather than assuming.
- **Command-line skills:** `crontab -e/-l/-r` (with `-r` caution), `systemctl --user`,
  `systemd-analyze calendar` (validate schedules!), `journalctl --user -u <unit>`,
  `systemctl list-timers`.
- **Laboratory:** schedule the M11-hardened `dq.sh` via user crontab with proper
  logging; rebuild the same job as a systemd user timer with `Persistent=true`; verify
  both via logs; deliberately break the script's PATH assumption and diagnose it.
- **Exercises:** 10 schedule-translation drills; debug a cron job that "works in my
  terminal but not in cron" (env, paths, relative paths); choose cron vs timer for 4
  scenarios with reasons.
- **Mini-project:** none (pipeline artifact feeds the capstone directly).
- **DS connection:** daily dataset refreshes, nightly model retraining, weekly report
  generation, and log rotation checks are all scheduled jobs. "It ran, here's the log"
  is the difference between an automated pipeline and a hope.
- **Notes:** course rule: no `crontab -r` without listing contents first; all scheduled
  jobs must write logs. This module's artifact becomes part of the M30 capstone.

---

## Unit 6 — Services, Networking & Security (M20–M25)

**Goal:** run and manage services, understand how machines talk to each other, operate
remote servers, and keep systems observable and secure. This unit turns students into
junior server administrators — the role they'll play around shared GPU machines.

### M20 — systemd, Services & Boot

- **Difficulty:** Advanced
- **Prerequisites:** M18, M19 (M03 revisited)
- **Learning objectives**
  - Explain systemd's role: PID 1, units, targets, service lifecycle.
  - Inspect, start, stop, enable, and disable services with `systemctl`.
  - Read unit files (`systemctl cat`) and understand key directives.
  - Create a custom user service (with `--user`) from a template.
  - Diagnose a failed service using `systemctl status` and journal entries.
  - Describe the boot process at overview level (firmware → bootloader → kernel → systemd).
- **Concepts:** units (service, timer, socket, mount); targets vs runlevels;
  enable vs start; daemon-reload; `Type=` (simple, exec, forking, oneshot);
  `Restart=`; `WantedBy=`; user units vs system units; `systemctl --user` and lingering;
  dependency ordering (After/Requires) at reading level; boot targets
  (graphical/multi-user/rescue); safe recovery concepts.
- **Practical skills:** manage real services (ssh, cron, cups) deliberately; write a
  unit file for a personal long-running job; bring a broken unit back to health from
  status + journal evidence; verify a service restarts after failure.
- **Command-line skills:** `systemctl status/start/stop/restart/reload/enable/disable/`
  `is-active/is-enabled/cat/list-units/list-unit-files`, `systemctl --user` variants,
  `systemctl daemon-reload`, `journalctl -u <unit>` (deep in M24),
  `systemd-analyze verify` (unit lint), `systemd-analyze blame/critical-chain` (intro).
- **Laboratory:** service management circuit on the VM (inspect ssh/cron; stop, start,
  restart, verify); write `hello.service` user unit running the M18 watchdog; break a
  unit (bad ExecStart path), diagnose from status, fix; boot-time exploration via
  `systemd-analyze`.
- **Exercises:** status-output decoding drills; unit-file reading comprehension;
  "service won't start" scenarios (typo'd path, missing dependency, wrong User=);
  enable-vs-start reasoning questions.
- **Mini-project:** none.
- **DS connection:** JupyterHub, database servers, GPU schedulers, and every cloud VM
  daemon run as systemd services; deploying one's own API server (M29) means writing
  a unit; reading `systemctl status` is step one of every "is it up?" check.
- **Notes:** students create *user* units by default (no root); system-unit authoring
  shown by instructor demo. Disabled-vs-stopped distinction hammered via exercises.

### M21 — Networking Fundamentals

- **Difficulty:** Advanced
- **Prerequisites:** M18 (M20 helpful)
- **Learning objectives**
  - Explain IP addressing (IPv4 focus, IPv6 recognition), subnets, and gateways.
  - Trace DNS resolution; use dig/resolvectl to query records.
  - Interpret ports and sockets; map well-known ports to services.
  - Inspect a machine's network config; test connectivity in stages.
  - Read the client path: name → IP → port → connection → protocol.
  - Understand NAT and how VM networking relates to the host network.
- **Concepts:** IP, subnet mask, CIDR, private ranges, gateway, routing table basics;
  DHCP; DNS hierarchy, A/AAAA/CNAME/MX records, resolver config (`/etc/resolv.conf`,
  systemd-resolved), `/etc/hosts`; TCP vs UDP; ports; sockets; loopback; NAT and port
  forwarding (VM networking modes); firewall concept (formalized in M25).
- **Practical skills:** layered connectivity diagnosis (link → IP → DNS → port → app);
  find which process owns a port; simulate a small web request end to end.
- **Command-line skills:** `ip addr/route/link`, `ping`, `dig` (+host/nslookup
  recognition), `resolvectl status/query`, `ss -tulpn` (read; sudo for process names),
  `curl` (`-I`, `-v`), `hostname -I`, `traceroute`/`mtr` (intro), `nc` (demo),
  `ip -brief addr`.
- **Laboratory:** full diagnosis circuit on the VM: break DNS (lab-provided script),
  fix it stage by stage; map all listening ports and identify each; fetch a page with
  curl and explain every hop; compare VM NAT vs bridged mode addressing.
- **Exercises:** subnet/CIDR arithmetic basics; "why can I ping but not browse?"
  scenarios; dig-output reading; port-to-service matching; curl verb drills.
- **Mini-project:** none.
- **DS connection:** remote database hosts, API endpoints, package mirrors, DNS for
  shared clusters, and "which port does Jupyter run on?" are daily DS-networking
  questions; SSH (M22) builds directly on this vocabulary.
- **Notes:** no packet-capture depth (tcpdump mentioned as awareness); no firewall
  manipulation yet — that is M25, after the concept model is solid.

### M22 — SSH & Remote Administration

- **Difficulty:** Advanced
- **Prerequisites:** M21, M20
- **Learning objectives**
  - Explain SSH transport and authentication (passwords vs key pairs vs agents).
  - Generate, protect, and use Ed25519 keys; deploy public keys properly.
  - Configure per-host settings in `~/.ssh/config` (aliases, users, keys, ports).
  - Run remote commands non-interactively; tunnel ports; copy files (basic scp; depth in M23).
  - Understand server-side config (sshd) at reading level and its hardening options.
  - Keep long remote jobs alive: tmux/screen + `nohup` (ties M18 to remote work).
- **Concepts:** asymmetric keys, fingerprints, known_hosts (TOFU model), ssh-agent,
  passphrases; `authorized_keys`; Host blocks, keys, and wildcards in ssh config;
  jump hosts (ProxyJump); local/remote port forwarding; X11 (awareness only);
  tmux as persistent sessions; sshd_config reading (PermitRootLogin,
  PasswordAuthentication, PubkeyAuthentication); fail2ban awareness.
- **Practical skills:** passwordless, passphrase-protected, agent-backed SSH to the VM;
  an ssh-config file with two host aliases; remote one-liners; persistent remote
  sessions with tmux; key hygiene (permissions on `~/.ssh`, never commit keys).
- **Command-line skills:** `ssh`, `ssh-keygen` (`-t ed25519`), `ssh-copy-id`, `ssh-agent`
  + `ssh-add`, `scp`, `ssh -L/-R/-J`, `ssh-keyscan` (demo), `ssh -v` debugging,
  `tmux` (`new`, `detach`, `attach`, `ls`, scrollback), `exit codes` over ssh, `sshfs`
  (optional awareness).
- **Laboratory:** full key workflow against the VM (generate → deploy → disable nothing
  yet, but verify passwordless login); build `~/.ssh/config` with aliases; tunnel the
  VM's web port to the host; run a remote command pipeline; tmux attach/detach drill;
  deliberate-failure lab: wrong key permissions, and read the error.
- **Exercises:** key-troubleshooting scenarios (permissions, agent, wrong key); config
  translation tasks (plain command → config block); tunnel design questions;
  fingerprint-mismatch incident walkthrough (what to do, what never to do).
- **Mini-project:** **Mini-Project D — "Remote compute workstation"**: documented
  end-to-end setup of an SSH-accessible workstation — keys, config, tmux workflow,
  a persistent service (from M20) reachable through a tunnel, with a written
  operations runbook (connect, check service, deploy a file, recover).
- **DS connection:** this *is* the GPU-server workflow: ssh in, launch tmux, start
  training, detach, check later. Key-based auth, aliases for jump hosts, and port
  forwarding to reach Jupyter/TensorBoard are daily practice in DS teams.
- **Notes:** practice targets are the student's own VM; the university GPU server may be
  used read-only where policy allows. Password auth is taught (it exists) but keys are
  the required standard; sshd hardening config is *read*, not applied, until M25.

### M23 — File Transfer: SCP, SFTP, rsync

- **Difficulty:** Intermediate
- **Prerequisites:** M22
- **Learning objectives**
  - Move files securely with scp and interactive SFTP.
  - Synchronize directory trees with rsync: `-a`, `-v`, `--delete` (with safety),
    `--dry-run`, include/exclude filters.
  - Choose the right tool per job (one file vs tree sync vs resumable bulk).
  - Script a repeatable dataset transfer with verification.
  - Understand compression, partial transfer, and bandwidth options.
- **Concepts:** scp/sftp relationship to SSH; rsync's delta algorithm; archive mode
  semantics; `--delete` danger and `--dry-run` discipline; trailing-slash semantics;
  exclude patterns; partial/resumable transfer (`--partial`, `-P`); bandwidth limits;
  checksum verification after transfer.
- **Practical skills:** mirror a dataset folder VM↔host without clobbering; resumable
  transfer of a large file; scripted, logged, verified dataset sync used later in the
  capstone pipeline.
- **Command-line skills:** `scp` (`-r`, `-P`, `-C`), `sftp` (get, put, ls, cd, bye),
  `rsync` (`-av`, `--dry-run`, `--delete` with `--dry-run` first, `--exclude`,
  `--include`, `--partial --progress`, `-z`, `--bwlimit`, `-e ssh`), `sha256sum` for
  post-transfer verification, `stat` size comparison.
- **Laboratory:** dataset sync lab: create a 1 GB synthetic dataset, rsync VM↔host with
  dry-run → real → verify; re-run and confirm no-op delta; `--delete` demonstration on
  a *sacrificial* directory after dry-run evidence; SFTP session for a single file;
  interrupted large transfer resumed with `-P`.
- **Exercises:** command-selection scenarios (10 jobs: which tool and flags?);
  trailing-slash prediction puzzles; exclude-pattern writing; "transfer took forever"
  diagnosis (compression? bandwidth? many small files?).
- **Mini-project:** none (the scripted sync feeds Mini-Project D's runbook and the capstone).
- **DS connection:** datasets move constantly: laptop → server → cluster storage.
  rsync's delta sync saves hours on 100 GB corpora; verified transfers prevent
  silent corruption; exclude filters keep `node_modules`-style junk out of syncs.
- **Notes:** explicit rule: `--delete` never without a prior `--dry-run` showing intent;
  all labs target the student's own VM.

### M24 — Logs, journald & Monitoring

- **Difficulty:** Advanced
- **Prerequisites:** M20, M18
- **Learning objectives**
  - Explain logging sources: journald (binary, structured) vs classic text logs.
  - Query the journal by unit, time, priority, and pattern.
  - Read the essential classic logs (syslog/auth) with grep and pager skills from Unit 2.
  - Diagnose real incidents from logs: failed service, SSH attempt storm, disk-full.
  - Monitor system health: CPU, memory, disk I/O, network — live and historical.
  - Apply log hygiene: rotation (logrotate concept), retention, structured output
    from their own scripts.
  - State the backup 3-2-1 rule and implement a scripted user-data backup.
- **Concepts:** journald storage (volatile vs persistent), priorities, structured
  metadata, `journalctl` fields; syslog/rsyslog awareness; logrotate; log levels;
  monitoring axes (utilization, saturation, errors); `sar`/sysstat awareness;
  iostat/vmstat interpretation basics; dmesg and kernel messages; backups vs snapshots
  (closure of the M04 thread), 3-2-1 rule, restore testing.
- **Practical skills:** find the cause of a failure from logs in under 5 minutes;
  watch live logs during an event; produce a monitoring snapshot of a loaded system;
  write scripts whose logs are greppable (timestamps, levels, single-line events);
  implement and *test-restore* a backup of `~/projects` and `~/data`.
- **Command-line skills:** `journalctl` (`-u`, `-f`, `-b`, `-p`, `--since/--until`,
  `-g` pattern, `--disk-usage`, `-o json` intro), `dmesg` (read), `tail -f` on classic
  logs, `grep` over `/var/log` (read; sudo where needed), `logrotate` config reading,
  `htop`, `iostat` (sysstat), `vmstat`, `sar` (intro), `df`/`du` recap, `rsync`-based
  backup script, `tar` (`-czf`, `-xzf`, `-tzf`) for archives, `sha256sum` for verify.
- **Laboratory:** incident walkthroughs (three prepared broken-service scenarios:
  solve from journal evidence); live-tail lab (generate log lines, watch with -f);
  monitoring circuit under load (M18's stress script + iostat/vmstat readings,
  interpreted in the lab log); backup lab: tar snapshot + rsync mirror to a second
  virtual disk (from M17), then a full test-restore to a scratch directory.
- **Exercises:** journal query drills (find all ERRORs from a unit since boot);
  log-triage puzzles (given log excerpts, name the failure); monitoring-reading
  interpretation; design a retention policy for a fictional service.
- **Mini-project:** **Mini-Project E — "Server health & backup kit"**: a script set
  (`health.sh` producing a one-page system report; `backup.sh` with 3-2-1-structured
  targets and a restore mode), plus a written incident report for one of the lab's
  broken-service scenarios.
- **DS connection:** "model training died overnight" is a log problem; GPU servers
  report OOM kills, CUDA errors, and disk-full events through exactly these tools;
  Jupyter logs, service logs, and training logs are all journalctl/tail territory;
  losing a week of experiments to no backup is a rite of passage — this module prevents it.
- **Notes:** restores are rehearsed, not assumed: the backup lab is graded on a
  successful test-restore. Reading logs of other users' services on shared machines is
  admin-only — labs use the VM.

### M25 — Security & Firewall

- **Difficulty:** Advanced
- **Prerequisites:** M21, M22, M24
- **Learning objectives**
  - Apply a security checklist to a Linux host: updates, users, services, firewall, logging.
  - Explain firewall models; use ufw to allow/deny specific services and ports.
  - Harden SSH access (key-only, no root) on the lab VM, with a documented rollback.
  - Audit listening services and close what isn't needed.
  - Handle secrets responsibly: env vars, file permissions, no committed credentials.
  - Recognize common threats: brute force, phishing-style social engineering,
    malicious scripts, supply-chain risks (typosquatted packages).
- **Concepts:** least privilege (recap and enforcement); attack surface reduction;
  default-deny vs default-allow; ufw profiles and rules; nftables/iptables awareness;
  sshd hardening directives (PasswordAuthentication, PermitRootLogin, AllowUsers);
  fail2ban concept; updates as patch management (`unattended-upgrades` revisit);
  GPG/checksums for downloads; secret hygiene and `.gitignore` discipline (M26 bridge).
- **Practical skills:** take a fresh-ish VM from open to hardened with every change
  documented and reversible; verify each hardening step empirically (before/after);
  audit and justify every listening service.
- **Command-line skills:** `ufw` (`status`, `allow`, `deny`, `delete`, `limit`,
  `enable`, app profiles), `ss -tulpn` audit (recap), `sudo sshd -t` (config test),
  sshd_config editing with backup + rollback, `apt update && apt upgrade` discipline,
  `unattended-upgrades` check, `gpg --verify` (demo), `sha256sum` verification (recap).
- **Laboratory:** the **hardening lab**: snapshot → baseline audit (`ss`, users, updates)
  → ufw default-deny with explicit SSH allow → sshd key-only + no-root (tested from a
  *second* terminal before closing the first!) → service audit → post-hardening audit
  → all steps logged in `hardening.md` with before/after evidence and a rollback plan.
- **Exercises:** firewall rule design for 5 service scenarios (SSH from campus subnet
  only; web public; database loopback-only); risk-analysis short answers; spot-the-
  vulnerability configs; secret-hygiene audit of a provided (fake) repo.
- **Mini-project:** (absorbed into the hardening lab artifact + incident report from M24).
- **DS connection:** shared GPU servers are shared with strangers: your key hygiene,
  your firewall, and your secret handling affect everyone. Jupyter, TensorBoard, and
  database ports must be exposed deliberately (tunneled via M22), never flung open;
  API keys for data services belong in env vars, not notebooks pushed to Git.
- **Notes:** the hardening lab includes an explicit rollback plan and snapshot; students
  verify access *before* closing sessions to avoid self-lockout — the classic admin
  mistake, rehearsed safely. No real credentials are ever used in course materials.

---

## Unit 7 — The Data Science Stack (M26–M29)

**Goal:** assemble the complete, Linux-native data science toolchain — Git, Python
environments, Jupyter, containers, servers, databases — and deploy a real service.

### M26 — Git & Development Workflows

- **Difficulty:** Intermediate
- **Prerequisites:** M07, M15 (M10 helpful)
- **Learning objectives**
  - Explain version control concepts: repository, commit, history, remotes.
  - Use the core loop fluently: status → add → commit → log → diff.
  - Branch, merge, and resolve simple conflicts.
  - Work with remotes (clone, push, pull, fetch) and understand origin.
  - Ignore files correctly (`.gitignore`) and keep secrets out of history.
  - Write useful commits and readable history; understand `.git` at a tour level.
- **Concepts:** snapshots not diffs; the three areas (worktree, index, history);
  commit hashes and DAG shape; branches as pointers; merge vs rebase (concept level);
  remotes and tracking branches; HEAD/detached HEAD; tags; `.gitignore` patterns;
  Git on Linux (config in dotfiles — ties to M15); SSH remotes (ties to M22).
- **Practical skills:** a clean, small-commit workflow; conflict resolution without
  panic; recovering from common mistakes (`restore`, `reset` soft/mixed at concept
  level, reflog awareness); reviewing a diff before committing.
- **Command-line skills:** `git init/clone/status/add/commit/log/diff/show/branch/`
  `checkout/switch/merge/restore/remote/push/pull/fetch/stash/tag/config`,
  `.gitignore` authoring, `git log --oneline --graph`, `git reflog` (awareness),
  `git config --global` (user, default branch, editor).
- **Laboratory:** version the course's own scripts: init a repo in `~/projects`,
  make 10 meaningful commits over the M10/M11/M18 scripts; create a branch for an
  experiment, merge it, then create and resolve a real conflict; push to a class Git
  server or hosted remote (per instructor); write `.gitignore` for data/ and logs/.
- **Exercises:** history-reading puzzles (what happened here?); conflict-resolution
  drills; "undo this safely" scenarios; commit-message rewrites (before/after).
- **Mini-project:** none — Git becomes the default for all remaining work.
- **DS connection:** datasets, notebooks, models, and pipelines all live in Git
  (with data itself handled via ignore rules + external storage); review and
  reproducibility in DS teams run on Git; the capstone repo is graded on Git hygiene.
- **Notes:** data-in-Git pitfalls taught explicitly (never commit large datasets or
  secrets; `.gitignore` from day one; Git LFS named as awareness only).

### M27 — Python, Jupyter & Data Workloads

- **Difficulty:** Intermediate
- **Prerequisites:** M16, M15, M10 (Python basics helpful, taught as needed)
- **Learning objectives**
  - Manage Python versions and environments on Linux the right way:
    `python3 -m venv`, pip, and requirements pinning.
  - Explain why environments matter for reproducibility; create, activate,
    export, and recreate an environment from a lockfile.
  - Run and configure Jupyter Lab/Notebook on a Linux host, including
    remote access via SSH tunnel (ties to M22).
  - Process datasets on the command line with Python one-liners and scripts.
  - Run longer ML-ish workloads as background jobs with logs (ties to M18/M19).
  - Recognize GPU tooling vocabulary (nvidia-smi, CUDA) for remote GPU servers.
- **Concepts:** interpreters and `PATH` interplay; venvs as isolated trees;
  activation as environment mutation (recap M15); pip vs apt-installed Python
  packages (never mix for the same library); `pip freeze`/constraints; wheel vs
  sdist awareness; Jupyter architecture (kernel, server, browser); token auth and
  ports; notebook-to-script workflow (`jupyter nbconvert --to script` awareness);
  pandas/numpy as apt vs pip installs; `nvidia-smi` and CUDA runtime awareness;
  conda/micromamba as user-space alternatives when no sudo is available.
- **Practical skills:** build a pinned, reproducible environment for a small ML
  task; run Jupyter headless on the VM and reach it from the host browser through
  an SSH tunnel; launch a training-style script under `nohup`/tmux with logging;
  profile a dataset job's memory via M18's watchdog.
- **Command-line skills:** `python3 --version`, `python3 -m venv .venv`,
  `source .venv/bin/activate`, `pip install/freeze/list/show`,
  `pip install -r requirements.txt`, `python -m pip` idiom, `jupyter lab`
  (and `--no-browser`, `--port`), `jupyter nbconvert`, `python -m json.tool`,
  `python -c` one-liners, `nohup python train.py > train.log 2>&1 &` pattern,
  `nvidia-smi` (awareness), `conda`/`micromamba` recognition.
- **Laboratory:** environment lab: create `.venv`, install pinned pandas/numpy/
  matplotlib/scikit-learn, freeze to `requirements.txt`, recreate from scratch on
  a second user account and verify import; Jupyter lab: launch headless, tunnel,
  connect from host, run a notebook over `datasets/`, shut down cleanly; batch lab:
  run a provided `train.py` (small model, CPU) via tmux + nohup, watch its log,
  stop it politely (M18 signals), verify checkpoints survived.
- **Exercises:** environment-recovery scenarios (broken venv, wrong python on PATH,
  mixed apt/pip installs); Jupyter troubleshooting (port busy, token, refused
  connections); script-vs-notebook trade-off questions; convert a notebook cell
  into a scheduled script (bridging to M19).
- **Mini-project:** **Mini-Project F — "Reproducible mini-ML"**: a tiny end-to-end
  task — pinned environment + `train.py` + `run.sh` + log + saved model artifact +
  `README.md` — committed with clean Git history (M26 standards).
- **DS connection:** this module *is* the student's daily DS workflow, made
  Linux-native: environments, Jupyter on servers, background training runs with
  logs, GPU tooling vocabulary — every piece connects to an earlier admin skill.
- **Notes:** no sudo needed anywhere in this module (user-space only), demonstrating
  the shared-server reality; conda/micromamba covered as alternatives, not primary.

### M28 — Docker & Containers

- **Difficulty:** Intermediate → Advanced
- **Prerequisites:** M16, M20, M27 (M26 recommended)
- **Learning objectives**
  - Explain containers vs VMs vs the host kernel; images, layers, registries.
  - Install Docker Engine on Ubuntu properly (official repo) in the VM.
  - Run containers: `run`, `ps`, `logs`, `exec`, `stop`, `rm`; manage images.
  - Read and write simple Dockerfiles; build and tag images; understand layer caching.
  - Persist data with volumes and bind mounts; map ports; set environment variables.
  - Compose multi-container setups (app + database) with Docker Compose.
  - Apply containers to data science: pinned environments, reproducible runs.
- **Concepts:** namespaces and cgroups (recap M18) at concept level; image layers
  and caching; registry model (Docker Hub, tags, digests); container lifecycle;
  COPY vs bind mounts; named volumes vs anonymous; networks (bridge default);
  `docker compose` services; dev-vs-prod image thinking; rootless mode awareness;
  GPU passthrough vocabulary (`--gpus`, NVIDIA Container Toolkit) as awareness.
- **Practical skills:** containerize the M27 mini-project (image with pinned env);
  run a database container with a named volume; write a compose file for
  app+db; clean up images/containers/volumes deliberately; read a container's
  logs and shell into it for debugging.
- **Command-line skills:** `docker run` (`-d`, `-p`, `-v`, `-e`, `--name`, `--rm`,
  `-it`), `docker ps -a`, `docker images`, `docker pull/rmi`, `docker logs -f`,
  `docker exec -it`, `docker stop/kill/rm`, `docker build -t`, `docker volume ls/
  inspect`, `docker network ls`, `docker compose up/down/ps/logs`, `docker system df`,
  `docker system prune` (with explicit caution), `docker cp`.
- **Laboratory:** dockerize `train.py` from Mini-Project F (build, run, extract the
  model artifact with `docker cp`); database lab: Postgres container + volume +
  compose file + healthcheck; persistence lab: prove data survives container
  removal with volumes, and dies without them; debugging lab: exec into a
  container, inspect env and filesystem.
- **Exercises:** Dockerfile ordering puzzles (cache efficiency); volume-vs-bind
  scenario questions; "container exits immediately" diagnosis; image-size
  reduction thinking (slim base, layer hygiene); VM-vs-container trade-off answers.
- **Mini-project:** none (containerized artifact merges into the capstone).
- **DS connection:** reproducible ML = code + environment + data; Docker is the
  lingua franca for shipping that to servers and clusters; GPU containers are how
  modern training environments are distributed; Compose is how a DS API + its
  database get deployed together (M29/capstone).
- **Notes:** Docker install requires sudo in the VM (ties to M14/M16); the `docker`
  group discussion is a live least-privilege lesson (M13 echo). Rootless and
  Podman named as alternatives; no registry pushing required in the course.

### M29 — Web Servers, Databases & Deployment

- **Difficulty:** Advanced
- **Prerequisites:** M20, M21, M25, M27 (M28 recommended)
- **Learning objectives**
  - Explain how a web request reaches a service: DNS → port → reverse proxy → app.
  - Install, configure, and verify nginx as a reverse proxy (VM scope).
  - Run a small Python API (FastAPI or Flask via uvicorn) as a systemd service
    (user unit), fronted by nginx.
  - Administer PostgreSQL essentials: install, create db/user, load data, query,
    back up with `pg_dump`.
  - Connect an app to a database via environment variables (M15/M25 hygiene).
  - Define deployment: artifacts, config separation, restarts, health checks,
    logs, and a rollback path.
  - Write a runbook for the deployed service.
- **Concepts:** reverse proxy vs app server; ports and sockets recap (M21);
  proxy_pass, server blocks, static vs proxied; WSGI/ASGI vocabulary;
  systemd unit for a long-running app (recap M20) with `Restart=` and env files;
  relational basics (tables, SQL SELECT/INSERT), users and privileges in Postgres,
  localhost-only DB binding; config via environment; health endpoints; log
  locations for the stack (nginx + app + Postgres → M24 skills); backups of the
  DB (`pg_dump`) and of config; zero-downtime concept (reload vs restart).
- **Practical skills:** deploy a complete small service end to end in the VM:
  nginx → API → Postgres, all as services with logs, health checks, and a
  documented rollback; load a real dataset into Postgres from CSV (psql `
  copy`); serve a static page and a proxied API and verify both with curl.
- **Command-line skills:** `apt install nginx postgresql` (recap M16),
  `systemctl status/enable` for the stack, nginx config editing with backup +
  `nginx -t` test, `sudo systemctl reload nginx`, `curl` verification (recap M21),
  `sudo -u postgres psql`, `CREATE ROLE/DATABASE`, `GRANT`, `psql` essentials,
  `\copy` CSV loading, `pg_dump`/`pg_restore`, `ss -tulpn` to verify bindings,
  `ufw` rules for the new service (recap M25), `journalctl -u` for app logs.
- **Laboratory:** the **deployment lab**: serve a static dashboard page via nginx;
  deploy a provided FastAPI app as a user systemd service with an env file;
  proxy `/api/` to it; load `datasets/sales-2019-q1.csv` into Postgres; make the
  API query it; verify every hop with curl; write `runbook.md` (start, stop,
  check health, read logs, restore DB from dump, rollback config).
- **Exercises:** request-path tracing (browser → … → app) for 3 architectures;
  nginx location-block reading; SQL essentials drills; "API returns 502"
  diagnosis from logs; config-change-with-rollback rehearsal.
- **Mini-project:** none (this lab is a direct capstone rehearsal).
- **DS connection:** data products are services: a model behind an API, a dashboard
  over a database, a JupyterHub for a class. DS graduates who can deploy and
  troubleshoot their own service on Linux are rare and valuable; this module is
  the payoff of Units 4–6.
- **Notes:** everything binds to localhost or the VM's NAT interface — no public
  exposure; TLS is discussed (certbot named) but optional, since VM scope lacks
  real DNS. The runbook format here becomes the capstone deliverable standard.

---

## Unit 8 — Capstone (M30)

**Goal:** integrate everything into one real, deployed, documented, monitored
data-science system — the course's proof of competence.

### M30 — Capstone Project

- **Difficulty:** Advanced
- **Prerequisites:** M01–M29 (core: M10–M30 chain; M26–M29 strongly recommended)
- **Learning objectives**
  - Design and implement an end-to-end data pipeline on Linux:
    ingest → validate → process → store → train/score → serve → monitor.
  - Operate the pipeline as scheduled jobs with logs and failure handling (M19/M11).
  - Secure the host per the M25 checklist; document every change.
  - Deploy the serving layer as services (M20/M29) with health checks.
  - Produce an operations runbook: start/stop, health, logs, backup, restore, rollback.
  - Present evidence: repo history (M26), scripts passing shellcheck (M10),
    logs of runs, monitoring output (M24), and a live demo.
- **Concepts:** integration of all prior units; operational maturity
  (idempotency, logging, verification, recovery); documentation as a
  deliverable; reproducibility (pinned envs, containers where chosen).
- **Practical skills:** independent end-to-end execution on the student's own
  VM; time-boxed troubleshooting; writing for operators (runbook), not just
  for graders.
- **Command-line skills:** everything prior — the capstone deliberately
  re-exercises the full toolbox rather than introducing new commands.
- **Laboratory / project phases**
  1. **Proposal** (week 1): pick a dataset from `datasets/` (or an approved
     external one), define the pipeline and service, get sign-off.
  2. **Build** (weeks 2–3): pipeline scripts, environment, storage layout,
     scheduled runs, database, API/dashboard.
  3. **Operate** (week 4): hardening checklist, monitoring kit, backup +
     test-restore, incident simulation.
  4. **Document & present** (week 5): runbook, architecture diagram, demo,
     retrospective on what broke and how it was found.
- **Exercises:** none — the project is the exercise.
- **Mini-project:** the capstone *is* the deliverable (see
  [projects/capstone/](projects/capstone/README.md) for brief, rubric, and starter files).
- **DS connection:** the capstone is a miniature of a production DS system:
  data engineering + ML + serving + operations, all on Linux, all documented.
- **Notes:** grading emphasizes *operational evidence* (logs, runbooks,
  restore tests) over model accuracy; a simple, reliable, monitored pipeline
  outscores a fancy broken one — deliberately.

---

## Appendix A — Required Topic Coverage Map

Every topic required by the course brief, mapped to its primary module (and
reinforcing modules where relevant).

| Topic | Primary module | Reinforced in |
|---|---|---|
| What Linux is | M01 | M02, M03 |
| Linux distributions | M02 | M16 |
| Linux architecture | M03 | M18, M28 |
| Installing Linux | M04 | — |
| Virtual machines | M04 | M17, M22 |
| WSL2 | M04 (+SETUP.md) | M27 |
| Linux terminal | M05 | all later |
| Shell concepts | M05 | M10, M11, M15 |
| Bash | M10 | M11, M19 |
| Filesystem hierarchy | M06 | M07, M17 |
| Paths | M06 | M07, M09 |
| Files and directories | M07 | M23 |
| File operations | M07 | M09, M23 |
| Permissions | M12 | M13, M14, M25 |
| Ownership | M13 | M12 |
| Users and groups | M12 | M13, M14 |
| sudo | M14 | M16, M17, M25 |
| Environment variables | M15 | M27, M28, M29 |
| Processes | M18 | M20, M27 |
| Jobs | M18 | M11, M22 |
| Signals | M18 | M11 |
| Package management | M16 | M27, M28 |
| Software installation | M16 | M27 |
| Repositories | M16 | M02 |
| Text processing | M08 | M09, M24 |
| grep | M08 | M09, M24 |
| sed | M08 | M11 |
| awk | M09 | M08, M11 |
| sort | M08 | M09 |
| cut | M08 | M09 |
| tr | M08 | M09 |
| find | M09 | M11 |
| xargs | M09 | M11 |
| Pipes and redirection | M09 | M10, M11 |
| Shell scripting | M10 | M11, M19 |
| Bash automation | M11 | M19, M30 |
| Storage | M17 | M24 |
| Partitions | M17 | — |
| Filesystems | M17 | — |
| Mounting | M17 | M04 |
| Disks | M17 | M24 |
| System administration | M12–M15, M20 | all of Units 4–6 |
| systemd | M20 | M19, M29 |
| Services | M20 | M29 |
| Networking | M21 | M22, M29 |
| IP addressing | M21 | — |
| DNS | M21 | M29 |
| Ports | M21 | M22, M25, M29 |
| Sockets | M21 | M29 |
| Firewall | M25 | M29 |
| SSH | M22 | M23, M27 |
| Remote administration | M22 | M23, M27 |
| SCP/SFTP/rsync | M23 | M24 |
| Logs | M24 | M20, M29 |
| journald | M24 | M20 |
| Monitoring | M24 | M18, M30 |
| cron | M19 | M30 |
| Scheduling | M19 | M30 |
| Backups | M24 | M17, M29 |
| Recovery | M24 | M04, M17, M29 |
| Security | M25 | M14, M22, M29 |
| Web servers | M29 | M21 |
| Databases | M29 | M28 |
| Python environments | M27 | M15, M28 |
| Git | M26 | M30 |
| Linux development environments | M26, M27 | M15 |
| Docker | M28 | M29, M30 |
| Containers | M28 | M30 |
| Virtualization concepts | M04, M28 | — |
| Performance monitoring | M24 | M18 |
| Troubleshooting | M24 | M20, M21, M29 |
| Server administration | M20–M25, M29 | M30 |
| Cloud Linux administration | M22, M29 (+notes) | M30 |
| DevOps concepts | M26–M29 | M30 |
| Linux for data science | thread through all units | M27, M30 |
| Linux for Python/Jupyter | M27 | M22, M30 |
| Linux for ML workloads | M27, M18 | M28, M30 |
| Deployment concepts | M29 | M28, M30 |
| Capstone project | M30 | — |

## Appendix B — Difficulty Scale

| Level | Meaning | Typical student state |
|---|---|---|
| Beginner | New vocabulary, guided steps, low risk | Can follow a lab with the manual open |
| Intermediate | Multi-step reasoning, some autonomy | Can adapt a lab to a slightly different goal |
| Advanced | Independent diagnosis and design | Can face an unfamiliar failure and make progress |

Difficulty is per-module for the *median* student in this program; labs are
scalable (instructors can add stretch goals for experienced students).

