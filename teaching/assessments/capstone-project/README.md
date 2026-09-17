# Capstone Project — Delivery Notes

> The capstone is fully specified in the repository's project pack;
> this page is the delivery wrapper for the 16-week calendar (phases
> land in weeks 11–16).

- **Brief & specification:** [projects/capstone/README.md](../../../projects/capstone/README.md)
- **Instructor pack:** [RUBRIC](../../../projects/capstone/instructor/RUBRIC.md) (100 pts, phase weights, non-negotiables) · [VIVA](../../../projects/capstone/instructor/VIVA.md) (29-question bank — instructor-held) · [INCIDENTS](../../../projects/capstone/instructor/INCIDENTS.md)
- **Assessment mapping:** [project-rubric pointer](../../../assessments/project-rubric.md) · [viva quick index](../../../assessments/viva-questions.md)
- Theme: **Deploy and Administer a Linux-Based Data Science Server** —
  local VM / WSL2 / Docker; cloud-GPU optional

## Phase calendar (mapped to the [plan](../../teaching-plan/16-week-course-plan.md))

| Phase | Weight | Weeks | What lands |
|---|---|---|---|
| 1. Proposal | 5% | W11 | environment choice (VM/WSL2/Docker), team roles, minimum-viable scope |
| 2. Build | 25% | W12–W14 | pipeline, storage volume, model job, serving stack, Git hygiene |
| 3. **Operate** | **30%** | W15 | scheduled runs, monitoring circuit, incident (staged), backup/restore drill |
| 4. Document | 20% | W15–W16 | runbook (peer-tested), architecture diagram, incident report |
| 5. Demo + viva | 20% | W16 | 10-min live demo + 10-min viva per the protocol |

The **Operate** phase is heaviest *by design* — the rubric's cap rule
(an Operate disaster caps the grade regardless of polish) is the
course's statement that administration is the graded skill.

## Milestone check-ins (instructor rhythm)

- **W12:** proposal feedback returned; storage/volume design sanity-check
- **W13:** pipeline dry-run observed (one scheduled run witnessed)
- **W14:** serving stack restart-survival spot-check; security checklist
  progress (evidence, not claims)
- **W15:** Operate checkpoint = the drill-book incident run live in
  S29's clinic; backup/restore drill verified (restore performed, or
  the area scores zero per non-negotiables)
- **W16:** defense slots booked; peer-test pairs assigned for runbooks

## Viva summary

- Format: 10 minutes; two pillars per student (drawn from the bank's
  spine: evidence, trade-offs, failure handling)
- Student preparation: [viva prep guide](../viva/README.md) — the
  protected bank stays instructor-held
- Grading: full-credit markers and follow-up probes are in VIVA.md

## Risk & safety considerations

- Everything runs on student-owned VMs/containers; no cloud spend is
  required (optional tracks documented, never graded higher)
- Secrets policy: `600` env files outside the repo; a committed secret
  is a non-negotiable deduction (rotate-first, then clean)
- The restore-drill non-negotiable exists because "the rumor backup"
  is the most common real-world failure — the rubric makes the point
  structural
