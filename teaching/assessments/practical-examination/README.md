# Practical Examination — Delivery Notes

> The staged-server circuit: 90 minutes, 12 tasks over 6 planted
> faults, transcript-graded. Paper, key, and the **staging script**
> live in the exam bank.

- **Student paper:** [assessments/practical/practical-exam.md](../../../assessments/practical/practical-exam.md)
- **Answer key + staging script:** `assessments/practical/practical-key.md` — **instructor-only** ([inventory](../../instructor-resources/README.md))
- Weight: **15%** · Pass ≥ 70 with **no zero-score items** · open-notes
  on the student's *own* module notes only (no internet)

## Environment requirements (checklist summary)

- Instructor-staged Ubuntu VM snapshot, **one per seat**, restored
  between sittings — the staging script plants the six faults in ~10
  minutes on a clean template
- Staged faults are *student-VM-local*: user-level units, loopback
  artifacts, sandboxed configs — nothing touches real system services
- One cold-spare prepared machine per room (snapshot failure = move
  the student, not the fix)
- Timer visible; the `script practical.log` instruction is on the
  paper's first line — the transcript is the submission

## Evidence requirements (what the transcript must show)

| Requirement | Why |
|---|---|
| `script` started before any task | method visibility is the graded currency |
| Each task's diagnosis commands in order | rung/method discipline is scored, not just outcomes |
| Verification per fix (original symptom re-tested) | step 7 of the method, always |
| Teardown/cleanup where a task created state | the census reflex, under pressure |

## Zero-score triggers (published to students in advance)

- Any destructive command outside the sanctioned scope (mkfs on real
  devices, rm outside own paths)
- A missing transcript
- Evidence of sharing/integrity breach
These are in the paper's header — nobody meets them by surprise.

## Rubric summary

10 points × 12 tasks; per-task marks split between *end state* and
*method/evidence* (the key carries the split). Partial credit follows
the circuit-wide rule: a sound evidence chain with a wrong diagnosis
outscores a lucky guess without one.

## Instructor logistics & common incidents

- A seat's snapshot fails mid-exam → move the student to the cold
  spare; note the time adjustment
- A student's transcript wasn't started → apply the published method
  cap (the key documents it); do not improvise
- Network-dependent fault fails in the room → the key documents the
  alternate task set; switch per the key, not ad hoc
- Post-exam: restore all seats from the clean template *before*
  leaving — the staging script's teardown does this

## CLO alignment

Primary: CLO-4, CLO-5, CLO-6 (method under pressure) — the full
mapping and the practical's role in the capstone pipeline are in the
[alignment matrix](../../../accreditation/CLO-ASSESSMENT-ALIGNMENT.md).
