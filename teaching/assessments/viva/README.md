# Viva — Student Preparation Guide

> The capstone ends with a 10-minute oral defense. This page tells you
> how to prepare; the actual question bank is instructor-held — the
> point of an oral exam is that answers can't be pre-canned.

## Format

- **10 minutes**, two pillars drawn from the bank's spine:
  1. **Evidence** — defend one claim from *your* system: "show me why
     your pipeline is idempotent" / "how do you know the restore
     worked?"
  2. **Trade-offs** — justify a design decision against its
     alternative: "why user units and not system units?" / "why this
     backup schedule?"
- Follow-up probes are the norm: every answer can be drilled one level
  deeper — expect "why?" twice

## What graders reward

| Signal | What it sounds like |
|---|---|
| Quoted evidence | "the journal line at 02:14 says the exec failed" |
| Mechanism, not ritual | "SGID because new files must inherit the team group — otherwise bob's edits land in *his* group" |
| Honest blast radius | "that fix touched one unit; my API stayed up — here's how I know" |
| Trade-off ownership | "I chose X despite its cost Y because Z mattered more here" |

## How to practice (the week before)

1. **Re-run your own demo** and narrate every command's *purpose*
   aloud — the viva is your runbook spoken
2. **The three-whys drill**: take five commands from your transcript;
   for each, answer "why this?" three times
3. **Red-team your own system**: find your weakest rubric area and
   prepare its defense *before* the panel finds it
4. **Practice with the [revision viva bank](../../revision/viva-questions.md)** —
   general questions in the same style; your instructor may run mock
   rounds from it
5. **Sleep.** The method-under-pressure skill you trained all semester
   is exactly what the viva samples.

## What to have open (per the protocol)

- Your system, live (the demo protocol precedes the viva)
- Your OPERATIONS notes and incident report
- Nothing else — prepared sheets read aloud score as reading, not
  knowing

## If you don't know

Say the honest version: "I didn't verify that — here's how I *would*
check: …" Evidence-first thinking applied to your own ignorance scores
better than confabulation, in this course and in the profession.
