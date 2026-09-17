# Lab Delivery Guide (Instructor & TA)

> How lab time actually runs. Pairs with the [unit teaching guides](../instructor-manual/module-teaching-guides/README.md)
> (which lab, which checkpoints) and the [student rules](student-lab-rules.md)
> (the contract students follow).

## Session rhythm (the 90-minute lab slot)

| Phase | Time | What happens |
|---|---|---|
| Brief | 10 min | the lab's *mission* in plain words; today's safety notes; where the checkpoints are |
| Drive | 55–65 min | students work; TAs circulate with the stuck protocol (below) |
| Debrief | 10 min | one checkpoint dissected publicly (anonymized best + common error) |
| Close | 5 min | teardown census verification; transcript spot-checks; next lab's prep |

The course's labs are sized for this rhythm — if a lab chronically
overruns, its **cut slice** is documented in the unit teaching guide.

## Checkpoint handling

- Checkpoints are answered **inline in the transcript** — a checkpoint
  without quoted evidence scores as skipped
- Read checkpoints *before* the drive phase starts (they define
  "done")
- The debrief dissects one checkpoint, not all — depth beats coverage

## The stuck protocol (for TAs)

1. **Ask for the evidence**: exact command + exact error. If neither
   exists, the student isn't stuck — they haven't run anything; send
   them back one step.
2. **One question, then silence**: "what did you expect to happen?"
   (the predict-run-explain loop, TA edition)
3. **Finger off the keyboard**: guide by pointing at transcript lines;
   typing the fix for them erases the learning and the evidence
4. **Three-then-park**: after three interventions without progress,
   note the student for the instructor's 1:1 queue — it's a
   foundational gap, not a lab problem
5. **The MTX rule**: never type destructive commands on a student's
   machine — narrate; they type

## Transcript standards (what graders look for)

| Mark | Meaning |
|---|---|
| ✓ | checkpoint answered with quoted evidence |
| ▲ | end-state correct, method invisible (caps below full marks) |
| ✗ | checkpoint skipped or evidence contradicts the claim |
| ⚠ | unsafe sequence — survived this time, deduction regardless |

Start a transcript late → the whole lab caps at the transcript cap.
This rule is published in week 1; surprises are a teaching failure.

## Circulation patterns that work

- **First 10 minutes stay mobile**: the transcript-start habit dies
  without early enforcement
- **Two laps, different lenses**: lap 1 = safety + transcript starts;
  lap 2 = checkpoint progress
- **The bored expert**: route early finishers to the module's ★★★
  challenge — never "help your neighbors" as idle work (they drift into
  doing the lab *for* someone)

## Snapshot & staging logistics

- Instructor calls **snapshot points** at lab milestones (announce
  which command, wait for the pause)
- Pre-staged labs (multi-user M12/M14, bloated journals M24, staged
  faults LA-3/LA-4/practical) follow the
  [infrastructure checklist](../setup-and-delivery/lab-infrastructure.md) —
  run it the *beforenoon*, not the morning of
- Restore-permission is always yes; a student who restores is executing
  the course's most important reflex

## Grading rhythm for the graded circuits (LA-1…LA-5)

- 10 points each: method/result split per the circuit's rubric (e.g.
  LA-1's per-task points name both the outcome and the verification)
- Grade within 48 hours — checkpoint feedback is only useful while the
  session is warm
- Release one **anonymized exemplar transcript** per circuit after
  grading — the fastest calibration students ever receive

## Extension challenges

Every module's `practice/challenges.md` has ★★–★★★ items. Use them as:
the bored expert's queue, bonus credit where institutional policy
allows, and the honest answer to "I'm done — now what?" They never
appear in graded requirements — extension is opt-in by design.
