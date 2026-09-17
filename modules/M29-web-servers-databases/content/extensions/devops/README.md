# Extension C — DevOps on Linux

> M29 extensions · Difficulty: Advanced · Time: ~4 hours
> Environment: your own VM + a container-based local CI runner (no cloud, no paid services)
> Prerequisites: M26 (Git), M27 (Python envs), M28 (Docker), Extension A (config management)

**DevOps is not a job title — it is the removal of a wall.** When the
people who write analysis code are not the people who run it, changes
travel by email and hope. DevOps merges the work: the same Git repo
that holds the analysis also holds its environment, its tests, its
provisioning, and its runbook — and a pipeline carries changes from
commit to running service without human copying. This extension names
the practices you have *already been doing* in this course (seriously:
you have) and adds the automation layer that makes them continuous.

## Files

| # | File | Topic |
|---|------|-------|
| 1 | [01-the-devops-loop.md](01-the-devops-loop.md) | Linux's role in DevOps; Git as the source of truth; environments & secrets in the pipeline |
| 2 | [02-ci-cd-concepts.md](02-ci-cd-concepts.md) | CI/CD concepts: build/test/deploy stages, pipelines, runners; GitHub Actions as the exemplar (conceptual + local) |
| 3 | [03-iac-and-deployment.md](03-iac-and-deployment.md) | Containers in the pipeline; deployment patterns (reload, blue-green, rollback); Terraform conceptually; Ansible ↔ CI |
| 4 | [lab-01-local-ci.md](lab-01-local-ci.md) | **Local lab:** run a real GitHub Actions workflow in a container runner (`act`-class) — test → lint → build → smoke-test, no cloud |
| — | [practice.md](practice.md) | 10 questions + key, 4 challenges |

## The course-as-DevOps claim (take it seriously)

Everything DevOps prescribes, you have done:

| DevOps practice | You did it in |
|---|---|
| Version control everything | M26 — history as evidence |
| Pinned, reproducible environments | M27 — `requirements.txt` as contract |
| Containers as deploy artifacts | M28 — image = environment as object |
| Config via env vars, secrets as files | M25 §5 / M27 / M28 |
| Automated tests before deploy | M10/M11 — shellcheck, self-testing scripts |
| Logs, health checks, monitoring | M24 / M29 — health.sh, drill cards |
| Runbooks and postmortems | M23-clinic / Extension A |
| Infrastructure as code | Extension A — the provisioning manifest |

What's genuinely new here is only the **automation of the carry** —
the robot that runs your checklist on every commit. One honest
pipeline beats a hundred DevOps slideware decks.

## The extension contract

- CI runs **locally in a container** (an `act`-class runner) — no
  GitHub account required, though the workflow file you write is
  *exactly* what would run there.
- No deploy targets beyond your own VM/user units; "production" is a
  locally-started service with a health endpoint.
- Secrets in the pipeline are demonstrated with throwaway values in
  env-file form — the M25 §5 rules quoted verbatim.

Start: [Lesson 1 — the DevOps loop](01-the-devops-loop.md)
