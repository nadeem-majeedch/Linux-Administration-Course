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

## Week 1 — Setup & first login (M01–M02, M05 start)

- **B:** BIOS-key cheat sheet ready · SETUP.md printed backup ·
  `pristine` snapshot demo rehearsed
- **D:** everyone completes the 8-check verification table
  ([student setup guide](student-environment-setup.md)) · **first
  snapshot taken before Lab 1 touch #1** · safety card read aloud
- **A:** list students on Paths A/B/C/D · office-hours slots for
  setup stragglers

## Week 2 — Command line I (M05–M06)

- **B:** navigation drills loaded · `tree` installed in demo VM
- **D:** the "path is an address" model before any cd flag ·
  nobody types `rm` until the safety card's rule is quoted
- **A:** check lab-01 submissions exist (end state, not beauty)

## Week 3 — Command line II (M07)

- **B:** redirection puzzle staged · `less` demo ready
- **D:** streams diagram drawn before `2>&1` ever appears
- **A:** Module quiz M05/M06 window opens

## Week 4 — Scripting I (M08)

- **B:** shellcheck installed in demo VM · the three buggy scripts
  from lab ready
- **D:** `set -euo pipefail` introduced as "the seatbelt", before
  loops
- **A:** Assignment 1 window opens

## Week 5 — Scripting II + text processing (M09, M08 of text unit)

- **B:** pipeline demo data staged (the dataset tree)
- **D:** one pipeline built live from grep→cut→sort→uniq, then
  *broken* and diagnosed — the debugging IS the lesson
- **A:** A1 checkpoints reviewed

## Week 6 — Text processing II + review (M08)

- **B:** quiz bank export ready
- **D:** **MIDTERM REVIEW SESSION** — run the practice scenarios
  from [revision/troubleshooting-scenarios.md](../revision/troubleshooting-scenarios.md)
- **A:** midterm logistics sent (stations, snapshot count,
  `script` requirement)

## Week 7 — MIDTERM (Units 1–3, M01–M13)

- **B:** [grading sheet](../instructor-resources/grading-sheets/midterm-grading-sheet.md)
  printed per student · staging verified on spare station
- **D:** transcript collection is part of submission
- **A:** grade within one week; second-mark any ≥ 85

## Week 8 — Users & permissions (M10–M12)

- **B:** demo users `demo1/demo2` verified present · shared-dir
  staging script distributed
- **D:** SGID demo with a *file created before* vs *after* — the
  before/after IS the concept
- **A:** Assignment 2 window opens

## Week 9 — sudo + processes (M13, M14→M17–M18)

- **B:** M14 lab drop-in files staged · watchdog demo ready
- **D:** the "sudo is audited" moment: show the auth log line for
  a real attempt
- **A:** A2 checkpoints

## Week 10 — Packages, storage, time (M15–M19)

- **B:** apt-cacher note ready (offline contingency) · loopback
  device demo rehearsed
- **D:** df-vs-du disagreement demonstrated, not asserted
- **A:** Assignment 3 (remote operator) window opens

## Week 11 — Networking + SSH (M20–M22, M23)

- **B:** loopback SSH self-connection rehearsed · key pair demo
  *as a pair* (generate once, copy once)
- **D:** no external scanning — say it explicitly; ladder poster
  on screen
- **A:** A3 checkpoints; quiz windows M15–M22 close

## Week 12 — Services + logs + security (M20 systemd, M24, M25)

- **B:** UFW demo VM restored (firewall ON state snapshot) ·
  journal forensics sample staged
- **D:** hardening checklist walked against a live VM
- **A:** **M32 performance clinic** scheduled as the incident
  drill

## Week 13 — Performance clinic + DS stack (M32, M26–M27)

- **B:** incident drill VM staged (CPU hog + disk filler planted)
- **D:** students diagnose in pairs, narrating evidence-first
- **A:** Capstone phase 1 checkpoint (spec + environment)

## Week 14 — DS stack II: Git, Docker, transfer (M26, M28, M23)

- **B:** Docker demo images pre-pulled (offline insurance)
- **D:** container-rm data-loss demo run *deliberately* with a
  mount — the save moment must be witnessed
- **A:** capstone phase 2 checkpoint (services + users live)

## Week 15 — Capstone build week

- **B:** office hours doubled · rubric on the course page
- **D:** no new content; consults only
- **A:** capstone phase 3 checkpoint (automation + monitoring
  evidence)

## Week 16 — Final + practical + viva

- **B:** [practical checklist](../instructor-resources/grading-sheets/practical-checklist.md)
  printed · viva slots booked · final papers staged
- **D:** practical in two sittings if the room demands; viva in the
  format from the protocol (evidence + trade-offs)
- **A:** final grade sheets to second-mark · post-term snapshot
  cleanup · **send the "what to keep from your VM" note** (a year
  from now, this VM is their first server's rehearsal)
