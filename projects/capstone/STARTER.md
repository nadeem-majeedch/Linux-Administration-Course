# Capstone Starter — Suggested Layout and First Steps

## Suggested repository layout

Adapt freely; the rubric cares about evidence, not folder names. This layout
mirrors the conventions taught across the course.

```
capstone/
├── README.md                  # overview, architecture summary, quickstart
├── docs/
│   ├── proposal.md            # phase-1 deliverable
│   ├── runbook.md             # operator documentation (phase 4)
│   ├── incident-report.md     # from the injected incident (phase 3)
│   └── restore-test.md        # restore evidence (phase 3)
├── assets/
│   └── architecture.png       # per assets/ conventions
├── pipeline/
│   ├── ingest.sh              # scheduled ingestion (idempotent, lockfile)
│   ├── validate.sh            # + validate report outputs
│   ├── process.py             # or .sh — cleaning/aggregation
│   └── train.py               # model job (CPU, < 2 min)
├── service/
│   ├── app.py                 # FastAPI/Flask API
│   ├── app.service            # systemd **user** unit template
│   ├── requirements.txt       # pinned
│   └── env.example            # env file template (never real secrets)
├── ops/
│   ├── health.sh              # adapted from Mini-Project E
│   ├── backup.sh              # + restore mode
│   └── nginx.conf             # site config with backup copy
├── etc/                       # cron/timer unit files, sql/ for schema + \copy seeds
└── logs/, artifacts/, backups/   # gitignored; evidence lives here at runtime
```

## First-week checklist (phase 1)

1. [ ] Pick the scenario (Pattern 1, Pattern 2, or approved own proposal).
2. [ ] Write `docs/proposal.md`: data source, pipeline sketch, component choices
      (cron vs timer, venv vs Docker), and the health/backup plan.
3. [ ] Snapshot the VM (`pre-capstone`).
4. [ ] Create the repo; commit the proposal and this skeleton.
5. [ ] Set up `~/data`, volume, and inbox directories (M06/M17 conventions).
6. [ ] Dry-run the M19 scheduling pattern with a trivial "hello pipeline" —
      prove the schedule fires and logs *before* building the real pipeline.

## Standing rules during the capstone

- Snapshot before every risky operation; record snapshots in `lab-log.md`.
- Every script passes `shellcheck`; strict mode everywhere (M10/M11 standards).
- No secrets in Git — `env.example` only; real env files live outside the repo
  with `600` permissions.
- Commit small and often; the history is graded (M26 standards).
- When stuck 30+ minutes on an unfamiliar failure: capture the evidence
  (commands + outputs), form a hypothesis, and bring *that* to office hours —
  exactly the M24 incident workflow.
