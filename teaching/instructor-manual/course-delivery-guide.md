# Course Delivery Guide

> For the instructor of record and anyone inheriting the course. Pairs
> with the [16-week plan](../teaching-plan/16-week-course-plan.md) (the
> *what/when*) and the [speaker notes](../speaker-notes/README.md) (the
> *how, per session*). This file is the *why and the policy*.

## 1. Course purpose & outcomes

The course takes BS Data Science students from zero Linux experience to
**defending an administered server** — the capstone is a working,
documented, backed-up, security-hardened DS environment. The proposed
CLOs (pending instructor review) and their assessment mapping live in
[../../accreditation/CLO-ASSESSMENT-ALIGNMENT.md](../../accreditation/CLO-ASSESSMENT-ALIGNMENT.md);
refer to them as *proposed* in all syllabi until institutionally approved.

## 2. Target students & prerequisites

- BS Data Science (semesters 2–4 typical); programming basics assumed;
  **no Linux assumed, no CLI assumed, no VM experience assumed**
- The first two weeks exist to guarantee a working, snapshotted VM —
  protect that time even when content pressure argues otherwise
- The cohort reliably splits: a confident third, an anxious middle, a
  silent struggler tail. The [teaching methodology](teaching-methodology.md)
  has specific moves for each band.

## 3. Teaching philosophy (the course's operating rules)

1. **Evidence over claims.** Every lab grades transcripts (`script`
   logs), not end-states. Grade the method, not just the result.
2. **Mistakes are the method.** Snapshot-protected breakage is *the*
   pedagogy; never demonstrate perfection without recovery.
3. **Anti-memorization.** Every assessment presents evidence/scenarios —
   a student who memorized a cheatsheet fails; one who understands
   passes without one. (The rule set is documented in
   [../../assessments/README.md](../../assessments/README.md).)
4. **Linux first, DS always in sight.** Every unit ends with the DS
   connection; the capstone pays it off. Do not let the course drift
   into a Python course.
5. **Safety is graded, not preached.** Destructive-command misuse is a
   deduction in *every* instrument.

## 4. Delivery model

- **2 × 90-min sessions/week**: lecture+demo first half, hands-on second
  half (exact splits per session in the plan)
- **Flipped-ready**: all modules are readable pre-class; each session's
  *prep* line names the reading. If you flip entirely, use the decks'
  Student Question sections as classroom agenda.
- **Labs**: the repository's 72 module labs + 5 graded LA circuits +
  Level 1–5 ladder. The [lab workbook](../lab-workbook/README.md) routes
  students; you never re-author labs.
- **Assessment cadence**: [schedule](../teaching-plan/assessment-schedule.md)
  — one heavy instrument per week maximum.

## 5. Required infrastructure (per seat)

- Student laptop able to run VirtualBox + Ubuntu 24.04 VM (4 GB RAM
  allocation; 8 GB host recommended) — SETUP.md covers install
- USB stick with two Ubuntu ISOs (instructor) — ISO corruption is a
  weekly event
- Lab share or repo copy of `datasets/` for text-processing work
- Loopback disk images (100 MB) pre-staged for M17; snapshot template
  for M12/M14 multi-user labs; staged snapshots for LA-3/LA-4/practical
  exam (staging scripts live in the assessment keys — instructor-only)
- Details and per-lab staging policy: [../setup-and-delivery/lab-infrastructure.md](../setup-and-delivery/lab-infrastructure.md)

## 6. Student support strategy

- **Office hours = VM hours**: require students to bring the machine;
  diagnosis *with* them beats fixes *for* them
- **The fuzzy pipeline**: exit tickets feed next session's warm-up —
  the loop is weekly and visible
- **Recovery policy**: a lost/broken VM is never a grade event before
  week 8 (rebuild from snapshot); after that, snapshots *are* the
  lesson (the backup unit arrives deliberately later)
- **Peer scaffolding**: pair work in labs from week 3; rotating pairs so
  the confident third teaches the middle band
- **Silent-struggler protocol**: LA-1 results identify them by week 4 —
  a 15-minute 1:1 (VM triage) usually resets the trajectory

## 7. Inclusive teaching considerations

- All materials are text (screen-reader friendly); decks convert to
  large-print handouts directly from Markdown
- Color never carries sole meaning (permission tables use letters+numbers)
- Keyboard-only terminal use is taught as *equivalent*, not workaround —
  it's also the power-user path
- Timing accommodations: LA circuits have a published 1.5× extension
  policy; exams follow institutional policy
- Examples avoid cultural assumptions; usernames in materials are
  gender-balanced and international (check new contributions)

## 8. Classroom management for practical labs

- **The two-minute rule**: before any lab command that mutates state,
  students say what it will do — aloud or in the transcript
- **The teardown census**: `ls` before any cleanup `rm`; only
  self-created paths, exact names (this is *taught* as ritual, and it
  is graded in LA circuits)
- **The second-session habit**: firewall/auth labs open a second session
  before enabling anything restrictive — rehearse until reflex
- **Snapshot checkpoint**: instructor calls "snapshot point" at lab
  milestones; restore-permission is always available
- Lab rules are student-facing in [../lab-workbook/student-lab-rules.md](../lab-workbook/student-lab-rules.md) — hand it out in week 1

## 9. Handling different skill levels

| Band | Signature | The move |
|---|---|---|
| Confident | finishes labs early, gets bored → disruptive | extension challenges (every module has ★★★ items); make them lab deputies |
| Middle | follows well, stalls at synthesis | pair rotation + "predict before run" drills |
| Struggler | copy-pastes, trails labs, silent | 1:1 VM triage by week 4; skeleton code with TODOs; oral check-ins instead of written quizzes where needed |

The extension activities are marked ★★★ in every module's
`practice/challenges.md` — never invent new ones on the fly.

## 10. What to do when it goes wrong

[troubleshooting-teaching.md](troubleshooting-teaching.md) covers the
classroom-level failures: mass VM breakage, a lab that runs long, the
demo that fails on stage, academic-integrity incidents in transcripts,
and mid-semester module rescheduling. The unit teaching guides
([module-teaching-guides/](module-teaching-guides/README.md)) cover the
technical failures per topic.
