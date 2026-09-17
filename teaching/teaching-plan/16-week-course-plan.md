# 16-Week Course Plan

> **Model:** 16 weeks × 2 sessions × 90 min. Every session lists all 15
> required fields. Module links point into the real content; labs are the
> repository's own labs; assessments are the repository's own instruments.
> Estimated split assumes 90 min; adjust, don't skip, the formative check.
>
> **Conventions:** *Prep* = student pre-work · *Formative* = in-class check
> (ungraded or low-stakes) · *HW* = homework · *Deck* = slide-deck section
> in [../lecture-slides/](../lecture-slides/README.md) · *SN* = speaker notes.

---

## WEEK 1 — Foundations: what Linux is

### Session 1 — Course introduction + M01 What Is Linux?

1. **Topic:** course contract; what an operating system is; what Linux is; why DS students must own this layer
2. **Module:** [M01](../../modules/M01-what-is-linux/README.md)
3. **Objectives:** explain OS/kernel/distro; place "Linux" in the stack; articulate why servers & ML run on it
4. **Lecture activities:** layer-cake whiteboard build; myth-vs-fact card sort (VM/container/distro confusion)
5. **Demonstrations:** boot the instructor VM live; `uname -a`, `cat /etc/os-release` — "this is the kernel talking"
6. **Practical lab:** none (no VM yet) — guided SETUP.md walkthrough begins in-class
7. **Student preparation:** read SETUP.md; bring laptop
8. **Formative:** 3-question exit poll (what's the kernel? what's a distro? what runs on servers?)
9. **HW:** complete SETUP.md VM creation at home; screenshot login prompt; run SETUP.md's post-install toolchain command (one copy-paste) so the S2 8-check passes offline-free
10. **Required tools:** instructor VM image, projector, SETUP.md
11. **Time allocation:** 20 intro/contract · 45 lecture · 15 setup walkthrough · 10 formative
12. **Instructor notes:** [SN unit 1 §1](../speaker-notes/unit-01-foundations-notes.md) — enforce the "questions after setup" norm early
13. **Revision resources:** [glossary](../../resources/glossary.md) entries: kernel, distribution, OS

### Session 2 — M02 Distributions + M03 Architecture

1. **Topic:** distro families (Debian/Red Hat/arch); Ubuntu LTS choice; the seven-layer stack; kernel vs user space
2. **Modules:** [M02](../../modules/M02-linux-distributions/README.md), [M03](../../modules/M03-linux-architecture/README.md)
3. **Objectives:** identify a distro from evidence; draw the stack; explain why the syscall boundary is a security boundary
4. **Lecture activities:** distro-identification from terminal evidence; stack-tracing "where does this problem live?"
5. **Demonstrations:** `apt` vs `dnf` slide contrast; live `ls /proc` — "the kernel's diary"
6. **Practical lab:** 8-check verification (setup guide, 15′) then first-login tour — [M01 lab 1](../../modules/M01-what-is-linux/content/labs/lab-01-identify-your-system.md) (20′, evidence transcript)
7. **Student preparation:** VM working (HW from S1); M02 quiz attempted
8. **Formative:** pair-drawing: the boot path from memory
9. **HW:** M02 lab 1 full circuit at home; M02+M03 quizzes; skim M04 lesson 1
10. **Required tools:** deck, student VMs
11. **Time allocation:** 30 M02 · 35 M03 · 35 verification+lab · 10 formative (buffer is the slack — see dry-run report §4)
12. **Instructor notes:** SN unit 1 §3–4 — the "macOS is UNIX" question will come; don't dodge it
13. **Revision resources:** cheatsheet [1 — command line] irrelevant yet; glossary: kernel space, user space, LTS

---

## WEEK 2 — Installing and controlling the machine

### Session 3 — M04 Installing Ubuntu in a VM (hands-on)

1. **Topic:** VM concepts; guided Ubuntu install; first-boot orientation
2. **Module:** [M04](../../modules/M04-installing-linux-vms/README.md)
3. **Objectives:** create a correctly-sized VM; complete install; explain what a snapshot buys you
4. **Lecture activities:** 15-min VM-sizing mini-lecture; then hands-on
5. **Demonstrations:** instructor installs alongside, projector on the partitioning screen ("we are NOT touching the real disk")
6. **Practical lab:** install completes in-session; [M04 lab 1](../../modules/M04-installing-linux-vms/content/labs/README.md)
7. **Student preparation:** VirtualBox installed (SETUP.md step 1); ISO
   downloaded+verified (Path A) or Desktop ISO ready (Path B) — from S1
   HW
8. **Formative:** peer-check: three things wrong with this VM config (screenshot)
9. **HW:** finish any incomplete install; take first snapshot
10. **Required tools:** VirtualBox, Ubuntu 24.04 LTS ISO, USB spare ISOs
11. **Time allocation:** 15 lecture · 55 hands-on · 15 formative — 5′
    of the hands-on hour is buffer for slow installers; students whose
    installs do not finish in-session complete the remaining gates as
    HW (nothing after Gate 3 in S3 depends on live class time)
12. **Instructor notes:** SN unit 1 §5 — keep two spare ISOs on USB; the RAM-sizing misconception is in the guide
13. **Revision resources:** M04 quiz

### Session 4 — M04 snapshots & recovery + bridge to terminal

1. **Topic:** snapshot/restore discipline; boot-to-shell tour; what happens when you type
2. **Module:** [M04](../../modules/M04-installing-linux-vms/README.md) (+ M03 recap)
3. **Objectives:** take/restore snapshots confidently; describe firmware→bootloader→kernel→init→shell
4. **Lecture activities:** four-act boot play; typed-command anatomy
5. **Demonstrations:** break-and-restore: rename a file, restore snapshot; "watch the snapshot eat the mistake"
6. **Practical lab:** [M04 lab 1 Part D](../../modules/M04-installing-linux-vms/content/labs/lab-01-provision-the-vm.md) — the snapshot drills (lab 2 is the WSL2 track)
7. **Student preparation:** VM snapshotted (S3 HW)
8. **Formative:** restore race — first pair to recover a "broken" login wins
9. **HW:** M04 quiz; on WSL2/desktop paths, run the M04 lab-2 parity circuit — next week is text-only
10. **Required tools:** VMs
11. **Time allocation:** 30 lecture · 45 lab · 15 formative
12. **Instructor notes:** SN unit 1 §5–6 — anxiety peaks here; the snapshot is the safety blanket, sell it
13. **Revision resources:** M04 quiz key (instructor), glossary: initramfs, snapshot

---

## WEEK 3 — Terminal fluency and the filesystem

### Session 5 — M05 Terminal & Shell + M06 Filesystem Hierarchy

1. **Topic:** shell vs terminal vs console; command anatomy; paths; FHS tour
2. **Modules:** [M05](../../modules/M05-terminal-and-shell/README.md), [M06](../../modules/M06-filesystem-hierarchy/README.md)
3. **Objectives:** explain command anatomy (command/options/arguments); navigate with absolute/relative/`~`/`-` paths; predict where files belong in FHS
4. **Lecture activities:** command-anatomy dissection on board; FHS map annotation ("where does the kernel's diary live?")
5. **Demonstrations:** live FHS walk: `/etc /var /home /tmp /proc`; `type -a` reveals
6. **Practical lab:** [M05 lab 1](../../modules/M05-terminal-and-shell/content/labs/README.md) navigation drills
7. **Student preparation:** M05 lesson 1 read
8. **Formative:** path-resolution flash cards (10 rounds)
9. **HW:** M05+M06 quizzes; `man` reading exercise
10. **Required tools:** VMs
11. **Time allocation:** 35 M05 · 35 M06 · 20 lab start
12. **Instructor notes:** SN unit 2 §1–2 — the `cd -` trick buys goodwill; relative-path confusion is THE week-3 wall
13. **Revision resources:** cheatsheets/command-line.md, files-and-directories.md

### Session 6 — M07 Files, Directories & Text Files

1. **Topic:** file operations (`cp/mv/rm` family); links & inodes; hidden files
2. **Module:** [M07](../../modules/M07-files-and-directories/README.md)
3. **Objectives:** organize datasets with mkdir/cp/mv; explain inode vs filename; predict glob expansion
4. **Lecture activities:** glob-prediction game; inode demo de-mystification
5. **Demonstrations:** `ls -li` on hard links — two names, one inode; safe `rm` patterns
6. **Practical lab:** [M07 lab 1](../../modules/M07-files-and-directories/content/labs/README.md)
7. **Student preparation:** M07 lesson 1
8. **Formative:** "what does this glob match?" rapid round
9. **HW:** organize a messy dataset tree (M07 exercise); M07 quiz
10. **Required tools:** VMs, messy-tree starter in datasets/
11. **Time allocation:** 35 lecture · 40 lab · 15 formative
12. **Instructor notes:** SN unit 2 §3 — `rm` fear vs `rm` respect: teach the `ls`-first reflex
13. **Revision resources:** cheatsheets/files-and-directories.md

---

## WEEK 4 — Text processing: the DS superpower

### Session 7 — M08 Text Processing (core tools)

1. **Topic:** cat/less/head/tail/wc; sort/uniq/cut/tr; text as streams
2. **Module:** [M08](../../modules/M08-text-processing/README.md)
3. **Objectives:** profile a dataset with one-liners; explain sort's field/unique interplay
4. **Lecture activities:** dataset profiling challenge on board; sort/uniq gotcha demo
5. **Demonstrations:** "profile this 50 MB CSV without opening it" live
6. **Practical lab:** [M08 labs](../../modules/M08-text-processing/content/labs/README.md) part 1
7. **Student preparation:** M08 lessons 1–2
8. **Formative:** predict-the-output: 3 pipelines
9. **HW:** M08 exercises set A
10. **Required tools:** VMs, course datasets
11. **Time allocation:** 40 lecture · 35 lab · 15 formative
12. **Instructor notes:** SN unit 2 §4 — sell this as "pandas before pandas"; the sort|uniq-≠-unique misconception
13. **Revision resources:** cheatsheets/text-processing.md

### Session 8 — M08 grep/sed/awk + M09 Pipes & Redirection

1. **Topic:** regex hunting; stream editing; awk columns; redirection; pipelines
2. **Modules:** [M08](../../modules/M08-text-processing/README.md), [M09](../../modules/M09-pipes-and-redirection/README.md)
3. **Objectives:** extract/filter/transform with grep/sed/awk; wire multi-stage pipelines; predict where bytes go (`> >> 2> |`)
4. **Lecture activities:** build the day's "top-N" pipeline live; redirection x-y table
5. **Demonstrations:** the file→grep→cut→sort→uniq→awk workflow on real logs
6. **Practical lab:** [M09 labs](../../modules/M09-pipes-and-redirection/content/labs/README.md)
7. **Student preparation:** M08 lesson 3–4, M09 lesson 1
8. **Formative:** pipeline building relay in pairs
9. **HW:** M09 quiz; mini-project (M08) started
10. **Required tools:** VMs, datasets, logs
11. **Time allocation:** 45 lecture+demo · 30 lab · 15 formative
12. **Instructor notes:** SN unit 2 §5 — `> ` vs `>> ` data-loss story; regex scope creep warning
13. **Revision resources:** cheatsheets/text-processing.md

---

## WEEK 5 — Scripting

### Session 9 — M10 Bash Scripting (core)

1. **Topic:** shebang, variables, quoting, substitution, exit codes, `if/test`
2. **Module:** [M10](../../modules/M10-bash-scripting/README.md)
3. **Objectives:** write a guarded script; explain quoting rules; use exit status correctly
4. **Lecture activities:** disassemble a real script line-by-line; quoting prediction quiz
5. **Demonstrations:** `echo $UNQUOTED` vs `"$QUOTED"` live failure modes
6. **Practical lab:** [M10 lab 1](../../modules/M10-bash-scripting/content/labs/README.md)
7. **Student preparation:** M10 lessons 1–2
8. **Formative:** spot-the-bug: 3 five-line scripts
9. **HW:** script a personal dataset backup helper (skeleton given)
10. **Required tools:** VMs, editor
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 3 §1 — quoting is the wall; slow down here
13. **Revision resources:** cheatsheets/bash-scripting.md

### Session 10 — M10 cont. + M11 Advanced Automation

1. **Topic:** functions, loops, arrays, debugging, `set -euo pipefail`, reusable patterns
2. **Modules:** [M10](../../modules/M10-bash-scripting/README.md), [M11](../../modules/M11-advanced-shell-automation/README.md)
3. **Objectives:** debug with `bash -x`; write idempotent automation; structure a script someone else can read
4. **Lecture activities:** live-debug a broken script (guided); idempotency discussion
5. **Demonstrations:** fix-the-bug script fixed live with `bash -x`
6. **Practical lab:** [M10 lab 2](../../modules/M10-bash-scripting/content/labs/README.md) fix-the-bug set
7. **Student preparation:** M10 lessons 3–5, M11 lesson 1
8. **Formative:** exit-code quiz
9. **HW:** Mini-Project A; Assignment 1 (A1) released — due end of week 6
10. **Required tools:** VMs
11. **Time allocation:** 40 lecture+demo · 35 lab · 15 formative
12. **Instructor notes:** SN unit 3 §2–3 — shellcheck as a teaching tool, not a gate
13. **Revision resources:** cheatsheets/bash-scripting.md

---

## WEEK 6 — Identity and access

### Session 11 — M12 Users/Groups/Permissions + M13 Shared Access

1. **Topic:** users/groups; rwx for files vs directories; numeric/symbolic modes; umask; SGID/sticky for teams
2. **Modules:** [M12](../../modules/M12-users-groups-permissions/README.md), [M13](../../modules/M13-ownership-shared-access/README.md)
3. **Objectives:** read `ls -l` fluently; design a shared-dataset permission scheme; predict `umask` results
4. **Lecture activities:** permission-bit decoding sprints; design-a-shared-tree on paper
5. **Demonstrations:** `chmod` numerically vs symbolically; sticky-bit "job folder" demo
6. **Practical lab:** [M12 lab](../../modules/M12-users-groups-permissions/content/labs/README.md)
7. **Student preparation:** M12 lesson 1–2; M12 quiz attempted
8. **Formative:** mode-decoding flash round
9. **HW:** Mini-Project B (shared dataset server design); M13 quiz
10. **Required tools:** VMs (multi-user lab accounts pre-staged)
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 4 §1 — "777 as confession" lands; directory-x confusion is universal
13. **Revision resources:** cheatsheets/permissions.md, users-and-groups.md

### Session 12 — M14 Sudo & Root + M15 Environment Variables

1. **Topic:** sudo policy; least privilege; sudoers drop-ins; env vars; PATH
2. **Modules:** [M14](../../modules/M14-sudo-root-principle/README.md), [M15](../../modules/M15-environment-variables/README.md)
3. **Objectives:** write a scoped sudoers drop-in (with `visudo -c`); trace PATH resolution; explain why `sudo` and env interact dangerously
4. **Lecture activities:** sudo incident reading (from M14 incidents); PATH murder-mystery
5. **Demonstrations:** `sudo command > file` — the redirection trap, live
6. **Practical lab:** [M14 labs](../../modules/M14-sudo-root-principle/content/labs/README.md)
7. **Student preparation:** M14 lesson 1; M15 lesson 1
8. **Formative:** "will this sudoers line do what they intend?" round
9. **HW:** M14+M15 quizzes; **midterm prep sheet** (one page, own notes)
10. **Required tools:** VMs
11. **Time allocation:** 40 M14 · 30 M15 · 20 formative
12. **Instructor notes:** SN unit 4 §2–3 — root fear→respect arc completes; PATH mystery is the highlight
13. **Revision resources:** cheatsheets/users-and-groups.md

---

## WEEK 7 — Consolidation + MIDTERM

### Session 13 — Midterm consolidation

1. **Topic:** Units 1–3 review circuit
2. **Modules:** M01–M13 (review)
3. **Objectives:** identify personal weak spots; rehearse exam-format tasks
4. **Lecture activities:** station circuit: 6 evidence-interpretation stations
5. **Demonstrations:** none — students drive
6. **Practical lab:** circuit is the lab
7. **Student preparation:** one-page prep sheet (S12 HW); practice questions
8. **Formative:** circuit scoring (self)
9. **HW:** sleep; know the exam logistics
10. **Required tools:** station printouts, VMs
11. **Time allocation:** 10 brief · 65 stations · 15 debrief
12. **Instructor notes:** [midterm exam README](../assessments/midterm/README.md) — read key BEFORE the session
13. **Revision resources:** [revision/final-revision-checklist.md](../revision/final-revision-checklist.md) Units 1–3 rows

### Session 14 — MIDTERM EXAMINATION

1. **Topic:** [midterm.md](../../assessments/exams/midterm.md) — Units 1–3, 100 pts
2. **Modules:** M01–M13
3. **Objectives:** assessed, not taught
4. **Format:** A reasoning · B output-tracing · C live terminal (`script` transcript)
5. **Demonstrations:** —
6. **Practical lab:** —
7. **Student preparation:** prep sheet + station circuit
8. **Formative:** —
9. **HW:** —
10. **Required tools:** exam VM snapshot per seat, timer
11. **Time allocation:** 120 min exam window
12. **Instructor notes:** staging per [practical-key pattern](../../assessments/exams/midterm-key.md); snapshots between seats
13. **Revision resources:** —

---

## WEEK 8 — Software and storage

### Session 15 — M16 Package Management + M17 Storage (part 1)

1. **Topic:** apt/dpkg; repositories & trust; PPAs; disks/partitions/`lsblk`
2. **Modules:** [M16](../../modules/M16-package-management/README.md), [M17](../../modules/M17-storage-and-filesystems/README.md)
3. **Objectives:** manage packages with dependency awareness; read `lsblk`/`df`/`du` and resolve their disagreements
4. **Lecture activities:** dependency-tree reading; df-vs-du mystery setup
5. **Demonstrations:** `apt install` with the dependency resolution shown; `lsblk` anatomy
6. **Practical lab:** [M16 labs](../../modules/M16-package-management/content/labs/README.md) (search/install/remove only — nothing system-critical)
7. **Student preparation:** M16 lesson 1–2
8. **Formative:** "which package command when?" round
9. **HW:** M16 quiz; (A1 was due end of week 6 — see the [assessment schedule](assessment-schedule.md))
10. **Required tools:** VMs (snapshotted before package labs)
11. **Time allocation:** 40 M16 · 30 M17 · 20 formative
12. **Instructor notes:** SN unit 5 §1–2 — PPA risk story; snapshot before labs, always
13. **Revision resources:** cheatsheets/package-management.md, storage.md

### Session 16 — M17 Storage & Filesystems (part 2)

1. **Topic:** loopback disks; mkfs on a *virtual* disk; mounts; fstab fields
2. **Module:** [M17](../../modules/M17-storage-and-filesystems/README.md)
3. **Objectives:** create/format/mount a loopback disk safely; explain every fstab field
4. **Lecture activities:** fstab field-by-field dissection; mount/umount lifecycle
5. **Demonstrations:** full loopback-disk lifecycle live (the safe way to teach formatting)
6. **Practical lab:** [M17 loopback lab](../../modules/M17-storage-and-filesystems/content/labs/README.md)
7. **Student preparation:** M17 lessons; VM snapshotted
8. **Formative:** fstab field quiz
9. **HW:** M17 quiz; document your loopback disk's lifecycle
10. **Required tools:** VMs, 100 MB spare loopback images
11. **Time allocation:** 30 lecture · 45 lab · 15 formative
12. **Instructor notes:** SN unit 5 §2 — the "mkfs is harmless HERE because loopback" framing is the whole ballgame
13. **Revision resources:** cheatsheets/storage.md

---

## WEEK 9 — Time and processes

### Session 17 — M18 Processes, Jobs & Signals

1. **Topic:** PIDs, states; ps/top/htop; jobs; kill/SIGTERM/SIGKILL; nice
2. **Module:** [M18](../../modules/M18-processes-jobs-signals/README.md)
3. **Objectives:** triage a busy system's output; choose the right signal; control job placement
4. **Lecture activities:** signal-choice scenarios; process-triage on a live busy VM
5. **Demonstrations:** the SIGTERM-vs-SIGKILL cleanup difference, live on a trap-handling script
6. **Practical lab:** [M18 labs](../../modules/M18-processes-jobs-signals/content/labs/README.md)
7. **Student preparation:** M18 lessons 1–2
8. **Formative:** which-signal round
9. **HW:** M18 quiz; Assignment 2 (A2) released — due W13
10. **Required tools:** VMs
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 5 §3 — `kill -9` first-reflex gets named and shamed gently
13. **Revision resources:** cheatsheets/processes.md

### Session 18 — M19 Scheduling: cron & systemd timers

1. **Topic:** crontab fields; cron's environment trap; timers; logging scheduled jobs
2. **Module:** [M19](../../modules/M19-scheduling-cron-timers/README.md)
3. **Objectives:** write correct cron schedules; explain why "works in my shell" ≠ "works in cron"; log scheduled output
4. **Lecture activities:** cron-field parsing drills; the environment-trap story
5. **Demonstrations:** a cron job that fails in cron and works in shell — diagnose live
6. **Practical lab:** [M19 labs](../../modules/M19-scheduling-cron-timers/content/labs/README.md)
7. **Student preparation:** M19 lessons 1–2
8. **Formative:** cron-expression reading round
9. **HW:** M19 quiz; schedule your W5 backup script
10. **Required tools:** VMs
11. **Time allocation:** 40 lecture · 35 lab · 15 formative
12. **Instructor notes:** SN unit 5 §4 — % escaping in crontab; PATH-in-cron
13. **Revision resources:** cheatsheets/cron.md

---

## WEEK 10 — Services and networks

### Session 19 — M20 systemd, Services & Boot

1. **Topic:** unit files; systemctl lifecycle; enable vs start; journald first contact; user units
2. **Module:** [M20](../../modules/M20-systemd-services/README.md)
3. **Objectives:** manage a service across failure modes; read a unit file; enable correctly
4. **Lecture activities:** unit-file dissection; failure-triage from journal evidence
5. **Demonstrations:** break a user unit's ExecStart, watch restart-loop, diagnose from journal
6. **Practical lab:** [M20 labs](../../modules/M20-systemd-services/content/labs/README.md)
7. **Student preparation:** M20 lessons 1–2
8. **Formative:** systemctl verb-choice round
9. **HW:** M20 quiz
10. **Required tools:** VMs
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 6 §1 — enable≠start misconception; journal evidence habit starts here
13. **Revision resources:** cheatsheets/systemd.md

### Session 20 — M21 Networking Fundamentals

1. **Topic:** IP/MAC; ports/sockets; DNS resolution; the diagnosis ladder
2. **Module:** [M21](../../modules/M21-networking-fundamentals/README.md)
3. **Objectives:** run the six-rung connectivity diagnosis; read `ss` output; resolve names with dig
4. **Lecture activities:** ladder walk on a real failure; port-state reading
5. **Demonstrations:** localhost Jupyter "not reachable" → diagnose rung by rung
6. **Practical lab:** [M21 labs](../../modules/M21-networking-fundamentals/content/labs/README.md) (loopback only)
7. **Student preparation:** M21 lessons 1–3
8. **Formative:** which-rung round
9. **HW:** M21 quiz
10. **Required tools:** VMs (all network labs loopback)
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 6 §2 — no external scanning, ever; ladder discipline over tool soup
13. **Revision resources:** cheatsheets/networking.md

---

## WEEK 11 — Remote work

### Session 21 — M22 SSH & Remote Administration

1. **Topic:** keys vs passwords; agent; config; host keys; remote execution; tunnels
2. **Module:** [M22](../../modules/M22-ssh-remote-admin/README.md)
3. **Objectives:** key into their own VM; write a ssh_config alias; explain TOFU; forward a port
4. **Lecture activities:** key-anatomy lecture; config-file walkthrough
5. **Demonstrations:** host-key-changed choreography (planned, safe); tunnel to a localhost web app
6. **Practical lab:** [M22 lab 1 key workflow](../../modules/M22-ssh-remote-admin/content/labs/lab-01-key-workflow.md)
7. **Student preparation:** M22 lessons 1–2
8. **Formative:** "why did SSH refuse?" evidence round
9. **HW:** M22 quiz; lab keys set up
10. **Required tools:** VMs as both client & server (loopback)
11. **Time allocation:** 40 lecture · 35 lab · 15 formative
12. **Instructor notes:** SN unit 6 §3 — lab keys vs personal keys, non-negotiable
13. **Revision resources:** cheatsheets/ssh.md

### Session 22 — M23 File Transfer (scp/sftp/rsync)

1. **Topic:** tool selection; rsync semantics; `--delete` discipline; verification
2. **Module:** [M23](../../modules/M23-file-transfer/README.md)
3. **Objectives:** choose scp/sftp/rsync by workload; predict slash semantics; gate deletions with dry-run; verify with sha256 manifests
4. **Lecture activities:** tool-selection scenarios; speedup-line reading
5. **Demonstrations:** interrupt-and-resume vs scp restart; slash-trap dry-run reveal
6. **Practical lab:** [M23 lab 1 sync circuit](../../modules/M23-file-transfer/content/labs/lab-01-dataset-sync-circuit.md)
7. **Student preparation:** M23 lessons 1–2
8. **Formative:** which-tool round
9. **HW:** M23 quiz; build sync-results.sh (lab 2 preview)
10. **Required tools:** VMs, loopback sshd
11. **Time allocation:** 40 lecture · 35 lab · 15 formative
12. **Instructor notes:** SN unit 6 §4 — the `--delete` policy is assessed; dry-run reflex drilling
13. **Revision resources:** cheatsheets/ssh.md + module troubleshooting

---

## WEEK 12 — Observability and defense

### Session 23 — M24 Logs, journald & Monitoring (lessons)

1. **Topic:** journald; journalctl queries; classic logs; rotation; log levels
2. **Module:** [M24](../../modules/M24-logs-journald-monitoring/README.md)
3. **Objectives:** extract evidence from journal with unit/time/priority filters; navigate /var/log
4. **Lecture activities:** log-forensics on a planted failure; level-vs-audience discussion
5. **Demonstrations:** journalctl pipeline to a root cause, live
6. **Practical lab:** [M24 lab 1 log forensics](../../modules/M24-logs-journald-monitoring/content/labs/README.md)
7. **Student preparation:** M24 lessons 1–2
8. **Formative:** build-the-query round
9. **HW:** M24 quiz part 1
10. **Required tools:** VMs with bloated journals staged
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 6 §5 — never grep raw journal dirs; the query discipline
13. **Revision resources:** cheatsheets/logs.md

### Session 24 — M24 Monitoring + M25 Security & Firewall

1. **Topic:** monitoring toolkit (top/free/vmstat/uptime); the 8-step incident method; threat model; UFW; hardening checklist
2. **Modules:** [M24](../../modules/M24-logs-journald-monitoring/README.md), [M25](../../modules/M25-security-firewall/README.md)
3. **Objectives:** read a system's vital signs; apply the method to a symptom; write a minimal UFW policy with justification
4. **Lecture activities:** vital-signs reading; hardening checklist walk; UFW rule justification drill
5. **Demonstrations:** under-load system triage; `ufw` default-deny with two justified allows
6. **Practical lab:** [M25 hardening lab](../../modules/M25-security-firewall/content/labs/README.md) (scoped)
7. **Student preparation:** M24 lesson 3–4; M25 lessons
8. **Formative:** next-step-in-the-method round
9. **HW:** M25 quiz; Assignment 3 (A3) released — due W15
10. **Required tools:** VMs
11. **Time allocation:** 40 M24 · 35 M25 · 15 formative
12. **Instructor notes:** SN unit 6 §5–6 — method over tool-soup; "allow with justification" is graded language
13. **Revision resources:** cheatsheets/logs.md, troubleshooting.md

---

## WEEK 13 — The Data Science stack

### Session 25 — M26 Git & Development Workflows

1. **Topic:** git model; core loop; branching; remotes; .gitignore; SSH auth
2. **Module:** [M26](../../modules/M26-git-dev-workflows/README.md)
3. **Objectives:** maintain a clean history; branch/merge without fear; configure SSH remotes
4. **Lecture activities:** commit-graph reading; .gitignore design for a DS project
5. **Demonstrations:** merge-conflict resolution live (small, controlled)
6. **Practical lab:** [M26 lab 1](../../modules/M26-git-dev-workflows/content/labs/README.md)
7. **Student preparation:** M26 lessons 1–2
8. **Formative:** "what did this command change?" round
9. **HW:** M26 quiz; put W5 script under git · *Capstone milestone: Proposal
   (phase 1) due this week — environment choice + team roles*
10. **Required tools:** VMs, git
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 7 §1 — branch≠copy misconception; datasets never committed
13. **Revision resources:** cheatsheets/git.md

### Session 26 — M27 Python, Jupyter & Data Workloads

1. **Topic:** venv/pip on Linux; `python3 -m pip`; Jupyter server; kernel management; batch workflows
2. **Module:** [M27](../../modules/M27-python-jupyter-data/README.md)
3. **Objectives:** build a pinned venv; run Jupyter on the VM and reach it correctly; explain why `python3 -m pip`
4. **Lecture activities:** environment-failure diagnosis (ModuleNotFoundError autopsy); venv lifecycle
5. **Demonstrations:** venv → Jupyter → kernel → data dir loop, live
6. **Practical lab:** [M26 lab 3 — end-to-end DS workflow](../../modules/M26-git-dev-workflows/content/labs/lab-03-end-to-end-ds-workflow.md) — synthesizes M26+M27; [M27 env drills](../../modules/M27-python-jupyter-data/content/labs/README.md) run alongside
7. **Student preparation:** M27 lessons 1–2
8. **Formative:** which-environment round
9. **HW:** M27 quiz; **Assignment 2 (A2) due**
10. **Required tools:** VMs
11. **Time allocation:** 40 lecture · 35 lab · 15 formative
12. **Instructor notes:** SN unit 7 §2 — Linux is primary, Python is the guest; env-hygiene habits
13. **Revision resources:** cheatsheets/python-environments.md, jupyter.md

---

## WEEK 14 — Containers and serving

### Session 27 — M28 Docker & Containers

1. **Topic:** VMs vs containers; images/layers; volumes; ports; Compose basics
2. **Module:** [M28](../../modules/M28-docker-containers/README.md)
3. **Objectives:** run/build simple containers; mount volumes; explain layer caching; justify a port mapping
4. **Lecture activities:** dockerfile line-by-line; VM-vs-container decision cases
5. **Demonstrations:** Jupyter-in-a-container with a data volume, live
6. **Practical lab:** [M28 labs](../../modules/M28-docker-containers/content/labs/README.md)
7. **Student preparation:** M28 lessons 1–2; Docker installed per SETUP
8. **Formative:** image-vs-container round
9. **HW:** M28 quiz · *Capstone milestone: Build (phase 2) checkpoint —
   core services + users live (rubric areas 1–4 evidence)*
10. **Required tools:** VMs with Docker
11. **Time allocation:** 45 lecture · 30 lab · 15 formative
12. **Instructor notes:** SN unit 7 §3 — `docker system prune` caution; volume-permission gotcha
13. **Revision resources:** cheatsheets/docker.md

### Session 28 — M29 Web Servers, Databases & Deployment

1. **Topic:** nginx basics; server blocks; logs; PostgreSQL lifecycle; `\copy`; backups
2. **Module:** [M29](../../modules/M29-web-servers-databases/README.md)
3. **Objectives:** serve static data via nginx; load a CSV into PostgreSQL; dump/restore a small DB
4. **Lecture activities:** request-lifecycle walkthrough; DB-credentials hygiene
5. **Demonstrations:** serve a dataset via nginx; `\copy` a CSV; `pg_dump` round-trip
6. **Practical lab:** [M29 labs](../../modules/M29-web-servers-databases/content/labs/README.md)
7. **Student preparation:** M29 lessons 1–2
8. **Formative:** request-path tracing round
9. **HW:** M29 quiz
10. **Required tools:** VMs
11. **Time allocation:** 40 lecture · 35 lab · 15 formative
12. **Instructor notes:** SN unit 7 §4 — localhost-only services; secrets never in repo
13. **Revision resources:** cheatsheets + M29 troubleshooting

---

## WEEK 15 — The DS server + revision

### Session 29 — M31 DS Server + M32 Performance Clinic

1. **Topic:** the ML-server day-in-the-life (13-scenario narrative); 8-step method under pressure; drill book
2. **Modules:** [M31](../../modules/M31-data-science-server/README.md), [M32](../../modules/M32-linux-performance-troubleshooting/README.md)
3. **Objectives:** operate a server politely and observably (tmux, monitoring, cleanup); run the incident method end-to-end
4. **Lecture activities:** scenario walk; one drill-book incident attempted live in teams
5. **Demonstrations:** instructor runs a staged incident using the method, narrating evidence
6. **Practical lab:** [M31 DS Server lab](../../modules/M31-data-science-server/content/labs/ds-server-lab.md) (CPU-only phases)
7. **Student preparation:** M31 lessons 1–2
8. **Formative:** method-step ordering round
9. **HW:** **Assignment 3 (A3) due**; capstone final polish · *Capstone
   milestone: Operate (phase 3) checkpoint — the drill-book incident is
   graded live in S29 (rubric areas 5–7, 9)*
10. **Required tools:** VMs, drill-book staging
11. **Time allocation:** 35 M31 · 40 M32 clinic · 15 formative
12. **Instructor notes:** SN unit 8 §2 — the drill is the dress rehearsal for the practical exam
13. **Revision resources:** [revision/troubleshooting-scenarios.md](../revision/troubleshooting-scenarios.md)

### Session 30 — Final revision

1. **Topic:** whole-course revision room
2. **Modules:** all
3. **Objectives:** self-diagnose weak areas; rehearse exam formats
4. **Lecture activities:** rapid-fire evidence rounds; student-led topic recap
5. **Demonstrations:** —
6. **Practical lab:** revision circuits
7. **Student preparation:** [final-revision-checklist](../revision/final-revision-checklist.md) completed
8. **Formative:** mock practical-exam task (ungraded)
9. **HW:** rest · *Capstone milestone: Document (phase 4) + Demo/viva
   (phase 5) — runbook peer-test and defense scheduled with the exam week*
10. **Required tools:** VMs
11. **Time allocation:** full session, student-driven
12. **Instructor notes:** SN unit 8 §3 — triage table ready for common panic topics
13. **Revision resources:** revision/ tree + cheatsheets

---

## WEEK 16 — Assessment week

### Session 31 — PRACTICAL EXAMINATION

1. **Topic:** [staged-server practical](../../assessments/practical/practical-exam.md), 90 min
2. **Modules:** M14–M31 scope
3. **Format:** 12 tasks over 6 planted faults; transcript-graded; pass ≥70, no zero-score items
4. **Environment:** instructor-staged snapshot per seat — staging script in the key
5. **Instructor notes:** [practical-key staging guide](../../assessments/practical/practical-key.md); restore between sittings
6. **Revision resources:** —

### Session 32 — FINAL EXAMINATION + capstone defenses

1. **Topic:** [final.md](../../assessments/exams/final.md) — Units 4–7, 100 pts; capstone vivas run in parallel scheduling per cohort size
2. **Modules:** M14–M31
3. **Format:** A reasoning · B evidence diagnosis · C design · D live terminal
4. **Instructor notes:** [final-key](../../assessments/exams/final-key.md); viva bank and protocol in the [capstone instructor pack](../../projects/capstone/instructor/RUBRIC.md)
5. **Revision resources:** —

---

## Coverage check (against required topics)

Course introduction W1 · fundamentals W1–2 · command line W3 · files W3 ·
permissions W6 · users/groups W6 · processes W9 · packages W8 · scripting
W5 · networking W10 · SSH+transfer W11 · services/systemd W10 · logs &
troubleshooting W12, W15 · storage & backups W8, W14 (DB backups), W15 ·
security W12 · Docker W14 · DS workflows W13–15 · revision W15 · practical
assessment W16. Every required topic from the master brief has a week;
nothing is forced where content doesn't support it (compression choices
are documented in the [mapping](lecture-to-module-mapping.md)).
