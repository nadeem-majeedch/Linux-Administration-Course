# Unit 8 Speaker Notes — Capstone (M30–M32)

> Companion to [../lecture-slides/unit-08-capstone-slides.md](../lecture-slides/unit-08-capstone-slides.md).

## Sessions 29–30 overview

**Teaching purpose.** Assemble the course into an operating whole:
launch the capstone properly (S29 runs M31/M32 content *as* capstone
preparation), then hand students a revision strategy they can execute
alone.

**Opening question (S29).** "What's the difference between a system that
works and a system that's *operated*?" Collect: monitoring, backups,
incident response, documentation, time passing. Those five are the
session.

## Per-slide guidance

- *S2 (phases):* the Operate weight (30%) gets read aloud twice. Explain
  the cap logic honestly: an unattended-run disaster caps the grade even
  with perfect week-5 polish — because the course grades *administration*,
  not assembly.
- *S3 (rubric):* the circling exercise is the real activity. Two weak
  areas + one mitigation each, written, collected. Use them: your
  mentoring queue for the fortnight is now sorted.
- *S4 (M31 narrative):* the 13 steps as a timed day. Make students call
  out the source unit at each step — the retrieval practice is the
  revision. Step 13 (cleanup) gets the professional nuance: *census
  first, delete only your own scratch*.
- *S5 (method):* run one drill incident live, strictly narrating step
  numbers. Grade yourself aloud against the drill rubric (read-only
  before mutating; one change at a time; quoted evidence) — modeling
  your own discipline is the point.
- *S7 (Operate):* name the deliberate container-kill plainly. Students
  who know the course will break things overnight meet the morning
  report as a puzzle, not a betrayal.
- *S8 (revision):* show the practical exam's zero-score triggers
  verbatim. The rules are published; surprises at exam time are a
  teaching failure.

## Misconceptions (unit-wide)

1. "Build is the project" — Operate outweighs it; documentation
   outweighs Git hygiene by more than double.
2. "The method is for exams" — it's for the *drill*, the morning
   report, and every real incident after the course.
3. "Revision = re-reading modules" — triage via checklist + evidence
   formats; re-reading is the lowest-yield hour in the plan.
4. "Snapshots make backups unnecessary" — the capstone requires
   *restore-performed, diff-verified* backups; a snapshot on the same
   disk fails the design question.

## Expected responses & probes

- S5 step-skipping exit question: the common honest answer is step 2
  ("evidence") — probe what gets skipped *inside* it (writing
  timestamps down). The journal is evidence only if quoted before it
  rotates.
- S7 "first thing when the morning report looks wrong": passing answers
  start with *read-only* evidence (journal window, health.sh) — any
  answer beginning with restart gets the room's collective coaching.

## Demo choreography

| Session | Demo | Teaching beat |
|---|---|---|
| S29 | one Drill Book incident, method narrated | grade yourself with the rubric, aloud |
| S29 | morning-after report skeleton | timestamps + quoted lines + timeline |
| S30 | mock practical task (ungraded) | transcript habit: `script` before anything |

## Classroom activities

- S29: teams attempt the phantom-hang drill (one per team, 25 minutes)
  with rubric scoring — the practical exam's dress rehearsal.
- S30: revision circuit — 6 stations, student-led; instructor floats for
  triage conversations only.

## Timing & cuts

S29's drill never cuts. S30 is fully student-paced — your only fixed
role is the opening triage brief (10 min) and the exam-logistics close
(5 min).

## Transition

"There is no next unit. There is a defended server and an oral
examination — and you've been rehearsing both since week 2's first
snapshot."
