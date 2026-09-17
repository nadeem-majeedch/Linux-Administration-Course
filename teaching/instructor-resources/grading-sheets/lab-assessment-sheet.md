# Lab Assessment — Generic Grading Sheet

> 🔒 INSTRUCTOR-ONLY. One reusable scorer for the five staged lab
> assessments (`assessments/lab-assessments/lab-assessment-01…05.md`).
> Fill the header from the specific LA, then score with the
> **evidence-quote discipline**: every point awarded or withheld cites
> a line from the student's `script` transcript or an end-state check
> you ran yourself.

**LA #:** ____ **Student:** ________________ **Date:** ______
**Transcript:** ________________ **Staged faults present (verified before handout):** [ ]

## Dimension scores (10 pts each, unless the LA specifies otherwise)

| Dimension | What earns marks | Score | Evidence quoted |
|---|---|---|---|
| **Diagnosis** | The fault was located from *evidence* (log line, ls -l, ss, df output), not trial-and-error | /10 | |
| **Fix correctness** | End state matches the LA's specified state exactly | /10 | |
| **Root cause, not symptom** | The underlying cause was named and addressed; no masking (restart-as-fix, chmod 777, `|| true`) | /10 | |
| **Safety discipline** | No destructive command outside its guarded context; blast radius stated | /10 | |
| **Verification** | The fix was *verified* with an independent check, quoted | /10 | |
| **Communication** | Notes answer: what broke, how you knew, how you fixed, how you'd prevent | /10 | |
| | **TOTAL** | **/60** | |

## Rubric anchors (per dimension)

- **10** — evidence quoted + correct + prevention noted
- **7–8** — correct, evidence partial or prevention missing
- **5–6** — correct end state but diagnosis was guesswork
- **2–4** — partial fix or symptom suppressed
- **0** — not attempted, or state achieved by breaking the check itself

## Common deductions (quote the transcript line, don't just tick)

| Flag | Typical transcript evidence | Deduction |
|---|---|---|
| Symptom masking | `systemctl restart` *before* any status/journal read | −4 on Root cause |
| Blast-radius blindness | `chmod -R 777` where a group write sufficed | −4 on Safety |
| Unverified success | fix applied, no `is-active`/`curl`/`ls` follow-up | −4 on Verification |
| Check-gaming | created the exact file the checker greps for, nothing else | 0 for that dimension + flag |
| Transcript missing | no `script` started | cap total at 30/60 |

## Second-mark triggers

[ ] ≥ 54/60  [ ] any "check-gaming" flag  [ ] student disputes score
**Second marker:** ______________ **Agreed final:** ____/60
