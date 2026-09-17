# Delivery Checklist — Week by Week

> Operational checklist keyed to the
> [16-week plan](../teaching-plan/16-week-course-plan.md). Each week:
> **B**efore (prep), **D**uring (the non-negotiables), **A**fter
> (admin). Time estimates assume the two-90-min-sessions cadence.

## Standing items (every week)

- **B:** VM restored to the week's entry snapshot · demo artifacts
  created *on screen*, not pre-baked · projector font ≥ 20 pt
- **D:** start with a 3-min recap question · every new command gets
  its why-before-syntax · students run along, not watch
- **A:** attendance · quiz in the quiz-bank window (if scheduled) ·
  note any misconception for the next recap

## Week 1 — Foundations: setup & first login (M01–M03)

- **B:** BIOS-key cheat sheet ready · SETUP.md printed backup ·
  `pristine` snapshot demo rehearsed · card-sort deck printed (SN S1)
- **D:** S1 — SETUP.md walkthrough starts in-class, VM creation is HW
  (incl. the post-install toolchain line) · S2 — 8-check verification
  gate ([student setup guide](student-environment-setup.md)), M01 lab 1
  in-class · **first snapshot taken before any lab touch** · safety
  card read aloud
- **A:** list students on Paths A/B/C/D · office-hours slots for
  setup stragglers · fuzzies from exit poll triaged before S3

> **Numbering note:** where a week block's module list disagrees with the
> [16-week plan](../teaching-plan/16-week-course-plan.md), the plan governs.
> Weeks 2–3 were realigned to the plan (plan Week 2 = M04 install/snapshots;
> M05–M07 begin in plan Week 3) in the week-2 dry-run revision.

## Week 2 — Installing Ubuntu & snapshots (M04)

- **B:** two spare ISOs on USB (Server *and* Desktop, since SETUP.md
  routes Path A → Server, Path B → Desktop) · install-demo VM reset to
  pre-install state · loaner-VM list current
- **D:** projector on the partitioning screen ("we are NOT touching the
  real disk") · OpenSSH server ticked during install · the
  `clean-install-<date>` snapshot exists before S4's first lab touch
- **A:** install-completion + snapshot-evidence check · BIOS-locked
  laptops routed to loaner VMs · WSL2 students run M04 lab 2 as HW

## Week 3 — Command line I (M05–M07)

- **B:** navigation drills loaded · `tree` installed in demo VM ·
  redirection puzzle staged · `less` demo ready
- **D:** the "path is an address" model before any cd flag ·
  streams diagram drawn before `2>&1` ever appears ·
  nobody types `rm` until the safety card's rule is quoted
- **A:** check lab-01 submissions exist (end state, not beauty) ·
  Module quiz M05/M06 window opens

## Week 4 — Text processing: the DS superpower (M08, M09)

- **B:** course datasets present ([M08 generator data](../../modules/M08-text-processing/content/data/) or
  lab share) · the "profile this CSV without opening it" challenge staged
- **D:** build the day's top-N pipeline live, predicting each stage ·
  the redirection truncate-before-running demo on a sacrificial file ·
  regex scope creep warning before sed/awk appear
- **A:** M08 exercises set A collected · mini-project (M08) started as HW

## Week 5 — Scripting (M10, M11)

- **B:** shellcheck installed in demo VM · the fix-the-bug scripts from
  [M10 lab 2](../../modules/M10-bash-scripting/content/labs/README.md) ready · Assignment 1 released S10
- **D:** `set -euo pipefail` introduced as "the seatbelt" · the skeleton
  recited at S10's start · live debug method demoed on ONE script before
  the fix-the-bug lab
- **A:** Mini-Project A assigned as HW alongside A1

## Week 6 — Identity and access (M12, M13 + sudo/env preview)

- **B:** demo users `demo1/demo2` verified present · shared-dir staging
  script distributed · quiz bank export ready
- **D:** SGID demo with a *file created before* vs *after* — the
  before/after IS the concept · **A1 due end of this week** — checkpoints
  reviewed in session
- **A:** Mini-Project B assigned · midterm prep-sheet HW announced (S12)

## Week 7 — MIDTERM (Units 1–3, M01–M13)

- **B:** [grading sheet](../instructor-resources/grading-sheets/midterm-grading-sheet.md)
  printed per student · staging verified on spare station
- **D:** transcript collection is part of submission
- **A:** grade within one week; second-mark any ≥ 85

## Week 8 — Software and storage (M16, M17)

- **B:** apt-cacher note ready (offline contingency) · 100 MB loopback
  images staged · **snapshot the room before both labs**
- **D:** update-vs-upgrade catalogue metaphor · df-vs-du disagreement
  demonstrated, not asserted · mkfs framed as "harmless HERE because
  loopback"
- **D:** loopback lifecycle is S16's centerpiece — demo 09 rehearsed
- **A:** Assignment 2 released S17 (per plan; schedule W9–12 window)

## Week 9 — Time and processes (M18, M19)

- **B:** watchdog demo ready · trap-script demo rehearsed · crontab
  sandboxes on lab VMs
- **D:** TERM-before-KILL ladder with the trap demo ("SIGKILL is the fire
  axe") · the unescaped-`%` crontab horror demo · cron's environment trap
  set up as S18's lab
- **A:** Assignment 2 released S17 (due W13, per plan) · M18/M19 quizzes

## Week 10 — Services and networks (M20, M21)

- **B:** broken user unit pre-staged (S19's opening fault) ·
  loopback-only networking policy stated on the board · six-rung ladder
  poster ready
- **D:** enable ≠ start drawn as two graphs · `ss -tlnp` watched growing
  and shrinking with a throwaway listener · **no external scanning — say
  it explicitly**
- **A:** M20/M21 quizzes · A2 checkpoints

## Week 11 — Remote work (M22, M23)

- **B:** loopback SSH self-connection rehearsed · key-pair demo prepared
  as a pair (generate once, copy once) · host-key-changed choreography
  rehearsed · rsync demo data staged
- **D:** the interrupt-and-resume race (scp vs rsync) run honestly ·
  `--delete` never without `--dry-run` — recite it as policy ·
  **Assignment 3 released S22** (due W15)
- **A:** M22/M23 quizzes

## Week 12 — Observability and defense (M24, M25)

- **B:** UFW demo VM restored (firewall-ON state snapshot) · journal
  forensics sample staged · crash-looping unit + bloated journal staged
  for LA-4
- **D:** hardening checklist walked against a live VM, line by line ·
  two-terminal ufw habit taught as professional muscle · memory-hog demo
  (available vs used, si/so wake)
- **A:** M24/M25 quizzes · LA-4/LA-5 windows open (per schedule)

## Week 13 — The Data Science stack (M26, M27)

- **B:** merge-conflict demo repo staged (small, controlled) · venv +
  Jupyter demo rehearsed · **Capstone Proposal (phase 1) checkpoint** —
  environment choice + team roles recorded
- **D:** branch-≠-copy drawn as pointers, moved live · the tunnel demo
  closes Unit 6's loop (local browser → forwarded port → remote kernel) ·
  system-python is untouchable, said plainly
- **A:** M26/M27 quizzes · A2 due S26 (per plan)

## Week 14 — Containers and serving (M28, M29)

- **B:** Docker demo images pre-pulled (offline insurance) · non-Docker
  fallback path announced · PostgreSQL + nginx present on lab images
- **D:** container-rm data-loss demo run *deliberately* with a mount —
  the save moment must be witnessed · 502-read-from-nginx-logs demo ·
  pg_dump restore-test proven live
- **A:** M28/M29 quizzes · capstone Build checkpoint (services + users
  live, per rubric phase 2)

## Week 15 — The DS server + revision (M31, M32)

- **B:** drill scripts verified on this semester's lab image (the
  afternoon before S29) · incident-drill VM staged · office hours doubled
- **D:** S29 = M31 13-scenario walk + one drill incident live (method
  narrated) + teams run incidents · S30 = student-driven revision circuits
  — instructor floats for triage only
- **A:** **A3 due S29** · capstone Operate checkpoint (phase 3, the
  drill-book incident graded live) · rubric on the course page

## Week 16 — Final + practical + viva

- **B:** [practical checklist](../instructor-resources/grading-sheets/practical-checklist.md)
  printed · viva slots booked · final papers staged
- **D:** practical in two sittings if the room demands; viva in the
  format from the protocol (evidence + trade-offs)
- **A:** final grade sheets to second-mark · post-term snapshot
  cleanup · **send the "what to keep from your VM" note** (a year
  from now, this VM is their first server's rehearsal)
