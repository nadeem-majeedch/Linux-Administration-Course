# Unit 8 Lecture Slides — Capstone (M30–M32)

> **Delivery:** Sessions 29–30 · Speaker notes:
> [../speaker-notes/unit-08-capstone-notes.md](../speaker-notes/unit-08-capstone-notes.md)

---

# Slide 1 — Title

## Slide Content
**Unit 8 — Capstone: Deploy & Administer a Linux-Based DS Server**
The whole course, operating as one system (M30–M32)

## Instructor Delivery Notes
Tone-setting: "Nothing on these two slides is new. That's the point —
watch the course assemble itself."

## Visual or Demonstration Suggestion
The capstone architecture diagram as a jigsaw, pieces flying in from
unit numbers.

## Student Question
"Which course verb do you think you'll use most during Operate week?"

---

# Slide 2 — The capstone at a glance

## Slide Content
- **Theme:** deploy & administer a Linux-based Data Science server
- Five phases: Proposal (5%) → Build (25%) → **Operate (30%)** → Document (20%) → Demo+viva (20%)
- Environment: your VM · WSL2 where appropriate · Docker — cloud/GPU optional
- Non-negotiables: restore-tested backup; key-only SSH; secrets `600` outside repo; peer-tested runbook
- Environment choice + team roles due with Proposal

## Instructor Delivery Notes
Operate is the heaviest phase *on purpose* — running is the point.
Read one non-negotiable aloud as a story (the rumor backup scores zero)
so the rules land as wisdom, not bureaucracy.

## Visual or Demonstration Suggestion
Phase-timeline bar with the rubric weights as widths.

## Student Question
"What does 'operating' include that 'building' doesn't? (Answer: time passing.)"

---

# Slide 3 — The ten rubric areas

## Slide Content
| Area | Pts | The one-line test |
|---|---|---|
| Pipeline correctness | 15 | 3 logged runs, dirty rows quarantined, idempotent |
| Storage design | 8 | dedicated volume, nofail, justified |
| Model job | 8 | pinned env, provenance sidecar |
| Serving stack | 12 | user unit + nginx, survives restart |
| Security | 12 | checklist *evidenced*, key-only, minimal ufw |
| Observability | 10 | health.sh + "what happened at 02:00?" |
| Backup & restore | 10 | restore performed, diff-verified, RTO timed |
| Reproducibility | 8 | classmate rebuilds from your doc |
| Documentation | 12 | peer-tested runbook, 8-step incident report |
| Git hygiene | 5 | small commits, no secrets/data |

## Instructor Delivery Notes
Have students circle their two weakest areas *now* and write one
mitigation each — the rubric as a self-checklist from day one.

## Visual or Demonstration Suggestion
The rubric table with phase-color coding.

## Student Question
"Which area does *no* amount of week-5 cramming fix?" (backup/restore — it needs real time passing)

---

# Slide 4 — M31: the DS server day-in-the-life

## Slide Content
- The 13-scenario narrative: access → SSH → project → env → deps →
  clone → dataset → Jupyter → experiment → monitor → results → backup → cleanup
- Server etiquette is *mechanized*: tmux durability, pre-flight checks, monitoring circuit
- The `/data` commons: checksum provenance, run directories, shared permissions
- Everything CPU-only — every GPU concept has an administrative twin

## Instructor Delivery Notes
Narrate the 13 steps as a *day* with times ("08:40, you get the
email…"). Students should recognize every verb — pause and let them name
the unit each came from.

## Visual or Demonstration Suggestion
A run-directory tree annotated with what each file proves.

## Student Question
"Step 13 is 'clean up'. What does a professional *actually* delete?" (their own scratch — census first)

---

# Slide 5 — M32: the 8-step incident method

## Slide Content
1. Define the problem (symptom ≠ cause)
2. Gather evidence (read-only first!)
3. Identify the affected component
4. Form hypotheses — *ranked*
5. Test safely (smallest blast radius)
6. Fix
7. Verify (the original symptom, gone)
8. Document (timeline, evidence, prevention)

## Instructor Delivery Notes
Drill one incident live using *only* the method, narrating which step
you're in. The rules that grade: read-only before mutating; one change
at a time; evidence quoted, not paraphrased.

## Visual or Demonstration Suggestion
A real journal + top output on screen; walk steps 1–5 with the class voting on each move.

## Student Question
"Which step do untrained admins skip — and what does it cost?" (2: random fixes, destroyed evidence)

---

# Slide 6 — Knowledge check

## Slide Content
1. Your pipeline ran 3 times but twice silently dropped rows. Which area bleeds, and why?
2. Rank two hypotheses before testing — why does ranking matter?
3. The Drill Book's phantom-hang: which *first* command distinguishes D-state from deadlock?

## Instructor Delivery Notes
Q2 is method-fidelity: unranked testing is guessing with extra steps —
the drill rubric deducts for it. Q3 previews S29's live drill.

## Visual or Demonstration Suggestion
—

## Student Question
(Q2 is the check)

---

# Slide 7 — Operate week: what "running" demands

## Slide Content
- Overnight unattended run: it *will* hit something you didn't plan
- Morning-after delta report: logs alone answer "what happened?"
- health.sh runs *before* you trust the dashboard
- The watchdog CSV is evidence, not decoration
- Operate-caps: an incident disaster caps the grade even with perfect polish — *operating is the point*

## Instructor Delivery Notes
Tell the truth about the deliberate container-kill in the Level-5 lab:
the course *will* break something on purpose while they sleep — that's
the pedagogy of Operate.

## Visual or Demonstration Suggestion
A real morning-after report skeleton (timestamps + quoted log lines).

## Student Question
"What's the first thing you'll do when the morning report looks wrong?"

---

# Slide 8 — Revision strategy: the final two weeks

## Slide Content
- [final-revision-checklist](../revision/final-revision-checklist.md) — triage, don't re-read
- Practice questions + rapid troubleshooting scenarios — evidence-first formats
- The practical exam = the method under a clock: 6 faults, 12 tasks, transcripts graded
- Final exam Sections A–D: reasoning, evidence, design, live terminal
- **Sleep is a graded strategy** — tired admins cause the incidents

## Instructor Delivery Notes
Show the practical exam's zero-score triggers verbatim (dangerous
commands, no transcript) — the rules are published precisely so nobody
meets them by surprise.

## Visual or Demonstration Suggestion
The practical exam rubric beside the 8-step method — same shape, on purpose.

## Student Question
"What's your personal weakest evidence-reading habit?"

---

# Slide 9 — Common mistakes (capstone season)

## Slide Content
- Building for 4 weeks, operating for 1 — phase weights say otherwise
- Runbook written from memory in week 5 (fails the peer test)
- "Temporary" firewall holes and 777s found by the grader
- Secrets committed in week 2, "cleaned" in week 5 — history remembers
- Demo rehearsed on the *good* machine only

## Instructor Delivery Notes
Every one of these is a real deduction pattern from past-semester
equivalents — frame as "how not to lose points you already earned."

## Visual or Demonstration Suggestion
The peer-test definition: "a classmate performs 2 ops using only your doc."

## Student Question
"Which mistake is invisible until exactly the wrong moment?"

---

# Slide 10 — Summary & exit ticket

## Slide Content
**Summary:** rubric as self-checklist · 13-scenario day · 8-step method ·
Operate is the point · revision = triage
**Exit ticket:** your two weakest rubric areas + one mitigation each;
the method's step you most often skip
**HW:** Proposal due (if not in) · Operate prep · revision checklist triage

## Instructor Delivery Notes
Collect rubric self-assessments — they seed your mentoring priorities
for the final fortnight.

## Visual or Demonstration Suggestion
—

## Student Question
(exit ticket is the question)

---

## Deck references
- Modules: [M30](../../modules/M30-capstone-project/README.md) · [M31](../../modules/M31-data-science-server/README.md) · [M32](../../modules/M32-linux-performance-troubleshooting/README.md)
- Assessment pack: [capstone rubric](../../projects/capstone/instructor/RUBRIC.md) · [practical exam](../../assessments/practical/practical-exam.md) · [final](../../assessments/exams/final.md)
