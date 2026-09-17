# Teaching Methodology

> The course's explicit pedagogical machinery — what to do, why it
> works, and how the assessments enforce it. The [delivery guide](course-delivery-guide.md)
> covers policy; this covers craft.

## 1. The core loop: Predict → Run → Explain

Every demonstration and most lab tasks follow the same three beats:

1. **Predict** — students write/say what the command will output before
   it runs (forces a model; reveals the misconception *before* the
   machine contradicts it)
2. **Run** — the command executes, output appears
3. **Explain** — the output is read back line-by-line against the
   prediction; differences are the lesson

This loop is why the course's assessments are evidence-interpretation
format — the exam *is* the loop under a clock. If you only adopt one
practice from this manual, adopt this one.

## 2. Misconception-driven lesson design

Each unit's speaker notes carry a misconception list harvested from real
cohorts. The teaching pattern is never "here's the right way"; it is:

- Elicit the wrong model (predict phase does this naturally)
- Run the disconfirming demo (the model breaks publicly)
- Rebuild with the correct mechanism (naming what changed)

Examples: `enable ≠ start` (boot graph drawn after the surprise),
`uniq` needs `sort` (run it wrong first), directory-`x` (chmod 000 on a
dir beats any explanation).

## 3. The evidence discipline

Students submit `script` transcripts from week 2 onward. The rules:

- Transcript starts **before** any work (`script lab.log` first)
- Every **Checkpoint** question answered *inline* in the transcript
- End states alone cap below full marks — the method must be visible
- Destructive commands appear only with their safety choreography
  (ls-first, dry-run-first, printed-path teardown)

This trains the professional habit that makes the capstone's incident
reports and the practical exam's transcripts feel like *normal*, not
new.

## 4. Safe-dangerous pedagogy

The course teaches genuinely dangerous operations (mkfs, rm -rf, --delete,
chmod -R, ufw default-deny) — that is the point of an administration
course. The pattern that keeps this safe *and* honest:

| Element | Implementation |
|---|---|
| Purpose | stated before the command ("mkfs is how filesystems are born") |
| Risk | stated plainly, with the real-world failure story |
| Safe environment | loopback disks, snapshots, user units, `~/` scratch — named explicitly ("safe because loopback") |
| Reversal | snapshot restore, backup dir, second-session insurance — or the honest admission that there is none |

Never teach a dangerous command *without all four*; the student-facing
[lab rules](../lab-workbook/student-lab-rules.md) mirror this table.

## 5. Spaced reinforcement map

Nothing is taught once. The deliberate reappearances:

| Skill | Introduced | Rehearsed | Assessed | Demonstrated |
|---|---|---|---|---|
| evidence-reading | M03 | M08–M24 labs | midterm, final B | capstone incident report |
| scripting skeleton | M10 | M19, M23 labs | A1, A2 | capstone health.sh |
| permissions | M12 | M13, M22, M27 | LA-3, midterm | capstone matrix |
| verification (hashes) | M19 | M23, M24 | A2 | capstone restore drill |
| 8-step method | M24 | M32 drills | practical exam | capstone Operate |

When a student asks "why again?", the map is the answer.

## 6. Questioning technique for terminals

- Ask for the **evidence**, never the flag: "what did `ss` say?" not
  "which flag lists listeners?"
- Ask for **prediction** before demonstration (loop rule 1)
- Ask **"how would you check?"** — the diagnostic instinct outranks the
  remembered fact
- Silence after a question is the sound of thinking; count to seven

## 7. Feedback patterns that scale to 60 students

- **Rubric-referenced one-liners**: "step 2 skipped — evidence not
  quoted" beats "see me"
- **Transcript hot-marks**: ✓ at correct choreography, ▲ at method
  gaps — fast to apply, precise to read
- **Public debrief of anonymized common errors** (never names): the
  misconception bank grows from these
- **Exemplar releases**: one anonymized full-credit transcript per
  circuit, released *after* grading

## 8. What this methodology is *not*

- Not tool-of-the-week: tools are the vocabulary; method is the grammar
- Not speed-running: sessions that finish content slowly beat sessions
  that cover it fast (the plan's compression notes respect this)
- Not perfection theater: instructors demo recovery from their own
  failures deliberately — the fix-the-bug labs exist because broken is
  the normal state of learning
