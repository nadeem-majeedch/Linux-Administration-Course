# Capstone Starter — Layout, Setup, and the First Week

> Companion to [SPEC.md](SPEC.md). The rubric grades evidence, not folder
> names — adapt the layout freely; keep the conventions.

## Repository layout (suggested)

```text
capstone/
├── README.md                  # overview, architecture summary, quickstart that works
├── docs/
│   ├── proposal.md            # phase-1 deliverable (sign-off)
│   ├── runbook.md             # six-section operator doc (phase 4; peer-tested)
│   ├── incident-report.md     # injected incident, eight-step method (phase 3)
│   ├── restore-test.md        # performed restore: checksums, RTO, model-loads
│   ├── reproducibility.md     # fresh-clone statement + classmate rebuild citation
│   └── extensions.md          # optional extension evidence (E1–E5)
├── assets/
│   └── architecture.png       # every component, data directions, trust boundaries
├── pipeline/
│   ├── ingest.sh              # scheduled ingestion (idempotent, lockfile, strict mode)
│   ├── validate.sh            # validation report + quarantine
│   ├── process.py             # cleaning/aggregation (or .sh)
│   └── train.py               # model job — CPU, < 2 min, checkpoint-aware
├── service/
│   ├── app.py                 # FastAPI/Flask API
│   ├── app.service            # systemd **user** unit template (VM/WSL2 tracks)
│   ├── requirements.txt       # pinned (M27 freeze)
│   └── env.example            # template only — real env files live outside the repo
├── ops/
│   ├── health.sh              # one-page report (Mini-Project E, adapted)
│   ├── backup.sh              # snapshots + restore mode (M24 lesson 5 pattern)
│   └── nginx.conf             # site config, with its backup copy
├── docker/                    # Docker track: compose.yaml, Dockerfile(s)
├── etc/                       # timer/cron units, sql/ (schema + \copy seeds)
└── logs/ artifacts/ backups/  # gitignored; runtime evidence lives here
```

## Environment tracks — first-hour setup

**Ubuntu VM (primary).** Snapshot now (`pre-capstone`) and before every risky
operation (record snapshots in `lab-log.md`). Everything from the course works
as taught: user units, ufw, volumes in fstab with `nofail`.

**WSL2.** Ubuntu distro; enable systemd (`[boot]\nsystemd=true` in
`/etc/wsl.conf`, then `wsl --shutdown`) — user units work after this. ufw is
available, but the **Windows firewall is the real edge**: document the
difference in your runbook and keep sensitive services loopback-bound. Disk is
a virtual disk inside your `%USERPROFILE%` — check `df -h` before big data.

**Docker all-in-one.** The stack is `docker/compose.yaml`: `db`, `api`,
`pipeline` services with healthchecks, named volumes, pinned image tags by
commit SHA. "User unit" translates to a restart policy + healthcheck; "ufw"
translates to loopback-only published ports; state lives in volumes — your
restore test targets *volumes*, not tars. The translation is part of the
engineering; say it out loud in the runbook.

## First-week checklist (phase 1)

1. [ ] Pick the scenario (Pattern 1, Pattern 2, or approved own proposal).
2. [ ] Write `docs/proposal.md`: data source, pipeline sketch, component
       choices **with one-sentence justifications**, health/backup plan.
3. [ ] Snapshot the VM (`pre-capstone`) / init the WSL2 distro / scaffold the
       compose file — and record it in `lab-log.md`.
4. [ ] Create the repo; commit the proposal and this skeleton (M26 standards
       start now: small, described commits).
5. [ ] Set up the directory contract: `~/data`, inbox, run trees (M06/M17/M31
       conventions); write your permission matrix into the proposal.
6. [ ] **Prove the schedule fires** — a trivial "hello pipeline" timer/cron
       that logs one line, *before* building the real pipeline (M19 Lab 1's
       forward-trigger).

## Standing rules during the capstone

- Snapshot before risky operations; record them.
- Every script passes `shellcheck`; strict mode everywhere (M10/M11).
- No secrets in Git — `env.example` only; real env files outside the repo,
  `600`.
- Commit small and often; the history is graded.
- Stuck 30+ minutes: capture evidence, form a hypothesis, bring *that* to
  office hours — the M32-clinic discipline, in office-hours form.
- The runbook is written *as you go* (every operation you perform, you
  document) — not reconstructed in week 5. Future-you is its first reader.
