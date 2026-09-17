# Assignments — Framework & New Instruments

## The canonical assignments (repository-shipped)

| Assignment | Covers | Weight | Paper |
|---|---|---|---|
| A1 — The Organized Analyst | M05–M13 | 5% | [assignment-1](../../../assessments/assignments/assignment-1-organized-analyst.md) |
| A2 — Automated Pipeline | M09–M10, M16–M19 | 5% | [assignment-2](../../../assessments/assignments/assignment-2-automated-pipeline.md) |
| A3 — Remote Operator | M20–M25, M27–M28 | 5% | [assignment-3](../../../assessments/assignments/assignment-3-remote-operator.md) |

Each ships with its own brief, deliverables, hard rules, and point
table. Keys/marking guidance for A1–A3 are instructor-held
([answer-keys inventory](../../instructor-resources/README.md)).

## New instruments (A4–A6) — optional replacements or enrichment

Three additional assignments cover topics the canonical trio doesn't
reach. **Adoption policy:** substitute one-for-one against an existing
5% assignment weight (or run as ungraded enrichment) — *do not* add
load on top of the documented scheme.

| Instrument | Topic | Replaces (optionally) | Student paper | Key |
|---|---|---|---|---|
| **A4 — The Survivor Script** | Shell automation under hostile conditions (M10–M11, M19) | A2 alternative | [assignment-4-shell-automation.md](new/assignment-4-shell-automation.md) | [key](new/assignment-4-shell-automation-key.md) *(instructor)* |
| **A5 — The Network Doctor** | Networking + services diagnosis with evidence (M20–M23) | A3 alternative | [assignment-5-network-and-services.md](new/assignment-5-network-and-services.md) | [key](new/assignment-5-network-and-services-key.md) *(instructor)* |
| **A6 — Harden the Science Server** | Security hardening + incident report (M25, M31–M32) | enrichment / A3 extension | [assignment-6-ds-server-hardening.md](new/assignment-6-ds-server-hardening.md) | [key](new/assignment-6-ds-server-hardening-key.md) *(instructor)* |

Keys are **instructor-only** — no site navigation links them.

## Evidence & submission standard (all assignments)

1. `script` transcript(s) started before any work
2. Checkpoint/justification answers **inline**
3. A short `README.md` in the submission describing what a grader will
   find and where
4. Commands that would destroy anything run only in the sanctioned
   environments (own VM, loopback, staged users) — unsafe sequences are
   deductions regardless of outcome
5. Git-hygiene bonus where the assignment uses a repo (small commits,
   no datasets, no secrets)

## Academic integrity guidance

- Transcripts make work **comparable**: identical command histories
  across submissions are examined at the *checkpoint answers* level,
  which diverge under real understanding
- Predict-before-run lines are personal — copying them is as visible as
  copying code
- AI assistants: follow institutional policy; the course's position is
  that transcripts of *your* machine doing *your* diagnosis cannot be
  delegated, and viva follow-ups test exactly that
- Detection process and evidence bundles: [troubleshooting-teaching §5](../../instructor-manual/troubleshooting-teaching.md#5-academic-integrity-incidents-in-transcripts)
