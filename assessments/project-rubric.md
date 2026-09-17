# Project Rubric — Pointer Pack

> The capstone is assessed with the evidence rubric in
> [`projects/capstone/instructor/RUBRIC.md`](../projects/capstone/instructor/RUBRIC.md):
> 100 points, ten evidence-based areas, phase weighting
> (proposal 5% → build 25% → operate 30% → document 20% →
> present+viva 20%), non-negotiable deductions, and the 4-beat
> live-demo protocol.

## What the rubric grades (the ten areas)

1. Deployment & environment track (VM/WSL2/Docker) — with track
   translations graded where claimed.
2. Identity & access — users, groups, sudo scoping, least privilege.
3. Data engineering on Linux — dataset permissions, ingest, storage.
4. The workload — training/serving with resource honesty.
5. Security posture — key-only SSH, default-deny firewall, secrets.
6. Observability — units, journals, healthcheck, monitoring circuit.
7. Recovery — tested backup/restore (untested claims score zero).
8. Automation — scripts, schedules, idempotency.
9. Packaging — containers/reproducibility (requirements/Dockerfile).
10. Documentation & defense — runbook, incident notes, viva.

## Cross-references

- Student-facing specification: [`projects/capstone/student/SPEC.md`](../projects/capstone/student/SPEC.md)
- Oral examination: [`viva-questions.md`](viva-questions.md) and the
  full bank in [`projects/capstone/instructor/VIVA.md`](../projects/capstone/instructor/VIVA.md)
- Injectable incidents with answer keys:
  [`projects/capstone/instructor/INCIDENTS.md`](../projects/capstone/instructor/INCIDENTS.md)

## Non-negotiables (echoed here because they end arguments)

- A committed secret: −15 **plus** history remediation before
  resubmission.
- An untested restore claim: the recovery area scores **zero**.
- Destructive-command misuse anywhere in evidence: area zero and a
  safety referral.
