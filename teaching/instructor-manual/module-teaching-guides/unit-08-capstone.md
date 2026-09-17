# Unit 8 Teaching Guide — Capstone (M30–M32)

> Sessions S29–S30 + defense window · companions: [speaker notes](../../speaker-notes/unit-08-capstone-notes.md) · [deck](../../lecture-slides/unit-08-capstone-slides.md)

## M30 Capstone Project (S29 launch + fortnight)

**Teaching objectives.** Launch the five phases with the rubric as a
*self-checklist*; set Operate expectations (time passing is graded);
assign mentoring priorities from the rubric self-assessment.

**Sequence.** Phase overview + weights → the ten areas as a checklist →
environment/team decisions → non-negotiables as stories → Proposal
requirements.

**Difficult concepts.** *Operate ≠ build with time passing* — health
checks, incident response, delta reports, restore drills are the graded
work. *Evidence discipline at capstone scale* — every rubric line starts
with "evidenced".

**Common mistakes.** Build-heavy schedules (4 weeks build, 1 operate);
runbooks written from memory in week 5; "temporary" firewall holes;
secrets committed early then "cleaned" (history remembers); backups
never restored.

**Demo plan.** A past-style morning-after report skeleton (timestamps +
quoted lines); the peer-test definition read verbatim.

**Activity.** Rubric circling (two weak areas + one mitigation each,
collected).

**Assessment hook.** The [capstone pack](../../../projects/capstone/instructor/RUBRIC.md):
phase weights, area rubric, non-negotiables, live-demo protocol. The
*viva bank* is instructor-held — student prep is the [revision viva
page](../../revision/viva-questions.md).

**Extension.** Cloud/GPU optional tracks are documented in the capstone
brief — CPU-only is fully graded; nothing requires spend.

**Troubleshooting.** Proposal-stage scope inflation: the brief's
minimum-viable system is deliberately small; approve *small and
operated* over *large and assembled*. Team-formaton conflicts: pairs
with defined roles (admin/analyst) split cleanly.

## M31 The Data Science Server (S29)

**Objectives.** The 13-scenario day as *rehearsal of the capstone's
operate phase*; tmux durability; pre-flight checks; the /data commons
contract (permissions + checksum provenance + run directories); cleanup
census discipline.

**Difficult concepts.** *The commons contract*: shared data is
immutable-snapshot + provenance sidecar; personal scratch is disposable.
The two live under different permission designs (M13 returns).

**Common mistakes.** Working directly in /data (the commons) instead of
run dirs; leaving tmux sessions with 12 dead shells; no pre-flight
check before long jobs (disk, quota, env).

**Demo plan.** One full scenario pass (access → dataset → Jupyter →
monitor → cleanup) narrated with the *etiquette* moves mechanized.

**Assessment hook.** Feeds LA-5 and the capstone's operate phase
directly; the DS Server lab's phases are graded evidence patterns.

**Extension.** GPU-server concepts (`nvidia-smi` literacy) at
administrative level — CPU-only labs required, GPU reading encouraged.

**Troubleshooting.** Two-actor lab needs a colleague account — the lab
documents the staging; if pairs are odd, the instructor plays the
second actor (it works well).

## M32 Performance & Troubleshooting Clinic (S29)

**Objectives.** The 8-step method *under pressure*; drill-book incident
practice with method-fidelity scoring; the drill as the practical
exam's dress rehearsal.

**Difficult concepts.** Ranked hypotheses (unranked testing = guessing);
read-only evidence before mutation; verification as a *step* (7), not a
vibe.

**Common mistakes.** Skipping step 2 (evidence quoting); fixing while
diagnosing; not re-testing the *original* symptom after the fix.

**Demo plan.** Instructor runs one drill incident, scoring themselves
aloud against the method rubric — self-grading models the standard.

**Activity.** Teams run the phantom-hang drill (25 min) with the rubric.

**Assessment hook.** The Drill Book is the practical exam's closest
analogue; method-fidelity is scored, not just outcomes.

**Extension.** The blind-diagnosis swap challenge (M32 practice).

---

## Unit-level notes (defense window)

- **Viva preparation:** students get the [revision viva page](../../revision/viva-questions.md);
  the *protected* bank stays in the instructor pack. Run one mock viva
  round in S30's close (2 students, 3 minutes each) to normalize format.
- **Scheduling the defenses:** the [RUBRIC](../../../projects/capstone/instructor/RUBRIC.md)
  defines the 10-minute demo + 10-minute viva protocol and grade bands;
  book the S32 window per cohort size.
- **The grading triage:** Operate phase incidents cap grades — read the
  cap rule before students ask; the rubric's language is the policy.
- **After the defense:** incident reports and runbooks archive into the
  course file — they are the accreditation binder's performance
  evidence ([accreditation/](../../../accreditation/ACCREDITATION-ONE-PAGER.md)).
