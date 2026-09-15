# Capstone Brief — End-to-End Data System on Linux

> Module: M30 · Unit 8 · Difficulty: Advanced
> Prerequisites: the full course chain; M26–M29 strongly recommended

## The task

Build and operate a small but complete data-science system on your Ubuntu VM:
data arrives on a schedule, gets validated and processed, lands in storage,
feeds a trained model, and is served behind an API — with logs, monitoring,
backups, and documentation proving it all works.

You choose the scenario. Two approved patterns (or propose your own):

- **Pattern 1 — Sensor pipeline:** `datasets/sensor-telemetry.tsv`-style readings
  arrive via a simulated feed script; your pipeline validates, aggregates, and
  loads them; a small model scores anomalies; an API exposes recent scores.
- **Pattern 2 — Sales reporting:** `datasets/sales-2019-q1.csv` exports drop into
  an inbox directory on a schedule; your pipeline cleans, validates, and loads
  them into PostgreSQL; an API/dashboard serves summaries and a forecast.

## Required components

Every item traces to a module; the mapping is deliberate.

1. **Scheduled ingestion** (M19, M11): a systemd user timer or cron job runs a
   scripted ingestion with idempotency and lockfile protection.
2. **Validation and processing** (M08–M10): pipeline scripts (shell and/or Python)
   produce a validation report; dirty rows are quarantined, not silently dropped.
3. **Storage** (M17, M29): processed data lands on a dedicated mounted volume
   and/or a PostgreSQL database (psql/`\copy` loading).
4. **Model** (M27): a small scikit-learn job (CPU, < 2 min) trained/scored by the
   pipeline; artifact versioned and logged.
5. **Serving** (M20, M29): a small API (FastAPI/Flask) running as a systemd user
   unit, fronted by nginx as reverse proxy; a health endpoint.
6. **Security** (M25, M22): the M25 checklist applied and documented; secrets in
   env files with correct permissions, never in Git; SSH key-only access on the VM.
7. **Observability** (M24, M18): all components write logs the operator can query
   (`journalctl`, structured script logs); `health.sh` (Mini-Project E, adapted)
   gives a one-page status; watchdog CSVs exist for the training run.
8. **Backups** (M24, M23): `backup.sh`-style snapshots of data + config + DB dump
   (`pg_dump`), with a **performed and evidenced restore test**.
9. **Reproducibility** (M26, M27, M28 — your choice): pinned venv with locked
   requirements, *or* a Dockerized component. Either way, a fresh environment
   rebuild must be documented.
10. **Documentation** (M26, M29): repository README, architecture diagram, and a
    runbook (start/stop, health, logs, restore, rollback, common failures).

## Phases and checkpoints

| Phase | Week | Checkpoint deliverable |
|---|---|---|
| 1. Proposal | 1 | 1-page proposal: scenario, data, pipeline sketch, component choices; instructor sign-off |
| 2. Build | 2–3 | Working pipeline + storage + model on the VM; repo with clean history |
| 3. Operate | 4 | Hardening checklist done; monitoring + backup + restore test evidenced; one injected incident diagnosed from logs |
| 4. Document | 5 | Runbook, architecture diagram, reproducibility statement |
| 5. Present | 5 | Live demo (10 min): show it running, break something benign, recover, show logs |

The **injected incident** in phase 3 is chosen by the instructor (e.g., disk fills,
a dependency is broken, the API dies): you must find and fix it from evidence.

## Deliverables checklist

- [ ] Git repository with the full project and clean history
- [ ] Proposal (approved), runbook, incident report, restore-test evidence
- [ ] All scripts pass `shellcheck`; all Python runs in the pinned environment
- [ ] Logs demonstrating at least three scheduled runs of the pipeline
- [ ] Monitoring report + watchdog CSV from the model run
- [ ] Backup snapshots + successful restore test (diff-verified)
- [ ] Architecture diagram (`assets/` conventions) and live demo

## Scope guidance

This is a *senior* project, not a startup: one small dataset, one model, one API.
The difficulty is in **operational completeness**, not model sophistication. A
pipeline that reliably runs, logs, restores, and recovers beats a deep-learning
showpiece that cannot explain its last failure.
