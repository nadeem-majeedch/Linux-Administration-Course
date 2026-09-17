# Capstone Project Specification — Student Edition

**Theme: "Deploy and Administer a Linux-Based Data Science Server"**

> M30 · Unit 8 · Difficulty: Advanced · Suggested timeline: 5 weeks
> Prerequisites: the full course chain (M26–M29 and both clinics strongly recommended)
> Companion reading: [M31 — The Data Science Server](../../../modules/M31-data-science-server/README.md)

---

## 1. Project statement

You will design, deploy, secure, operate, and **defend** a small but complete
Linux-based data-science server: data arrives on a schedule, is validated and
processed, lands in storage, feeds a trained model, and is served by an API —
with users, permissions, a firewall, SSH, logs, monitoring, backups, and a
runbook around it all.

The difficulty is deliberately **operational completeness, not model
sophistication**: one small dataset, one CPU-sized model (< 2 minutes), one
API. A pipeline that reliably runs, logs, restores, and *explains itself*
outscores a deep-learning showpiece that cannot say why it failed.

This is a miniature of a production DS system — and the final assessment is
not the artifact alone but your ability to **operate and defend it live**.

## 2. Learning outcomes

On completion you can:

- **LO1 — Deploy:** produce a working Linux server environment (VM/WSL2/Docker
  track) with a documented, repeatable setup (M04/M27/M28/M29-ext).
- **LO2 — Administer identity & access:** configure users/groups, least-
  privilege permissions, and key-only SSH with tested rollback (M12–M14, M22, M25).
- **LO3 — Engineer data on Linux:** run a scheduled, idempotent, logged
  pipeline that validates and quarantines data into designed storage (M06–M11, M17, M19).
- **LO4 — Train & serve:** train a pinned-environment model and serve it behind
  nginx with health checks (M20, M27–M29).
- **LO5 — Secure:** apply the hardening checklist, manage secrets correctly,
  and justify every open port (M25 + M29-ext security layers).
- **LO6 — Observe:** make the system explain itself — structured logs,
  monitoring report, and answers to "what happened at 02:00?" from evidence
  (M18, M24, clinics).
- **LO7 — Recover:** back up and *prove* restore; diagnose an injected incident
  via the eight-step method (M32-clinic, M24 §5).
- **LO8 — Automate & package:** deliver Bash automation passing shellcheck and
  a reproducibility story (pinned venv and/or Docker) (M10/M11, M26–M28).
- **LO9 — Document & present:** write operator-grade documentation and defend
  design choices in a live demo and viva (M26, M29, Extension A).

## 3. Architecture (the reference shape)

Adapt to your approved scenario; the *roles* are fixed, the implementations
are yours.

```text
                         ┌──────────────────────────── VM / WSL2 / Docker host ────────────────────────────┐
                         │                                                                                  │
  dataset/         ┌─────▼──────┐   validate/process   ┌──────────┐   train/score   ┌────────────┐         │
  feed (script ───►│  inbox/    │─────────────────────►│ Postgres │◄───────────────►│ model job  │         │
  or provided CSV) │ (M19 sched)│   (M08–M11 scripts)  │ (M17/M29)│   (M27, pinned) │ CPU <2 min │         │
                   └────────────┘                      └────┬─────┘                 └────────────┘         │
                                                             │                                              │
                   ┌────────────┐   reverse proxy   ┌───────▼──────┐                                       │
  you ◄──SSH/tunnel│   nginx    │──────────────────►│ API (FastAPI)│── health endpoint ──► health.sh ──────┤
  (M22/M27)        │ (M29)      │                   │ user unit    │            (M24 kit)                  │
                   └────────────┘                   └──────────────┘                                       │
                         │                                                                                  │
                         │  ufw (M25) · systemd user units (M20) · logs→journald/files (M24)                │
                         │  backups: data + config + pg_dump → second location (M24/M23)                    │
                         └──────────────────────────────────────────────────────────────────────────────────┘
```

## 4. Required tasks (the component checklist)

Every item cites its module; each must be *evidenced*, not claimed.

1. **Environment setup** (M04/M27/M29-ext): the host (VM snapshot, WSL2 distro,
   or Docker track) provisioned; setup documented to the "fresh rebuild"
   standard. *[Track details: §10.]*
2. **Users & groups** (M12–M13): at minimum your user + a limited `svc`
   account (or user-unit separation); group-owned shared data directory with
   SGID; a permission matrix in the docs.
3. **Permissions** (M13/M27): data read-only where it should be; secrets'
   files `600` outside the repo; the accidental-overwrite guard *demonstrated*
   (a failed write, quoted).
4. **SSH** (M22/M25): key-only access to the host; the tunnel as the access
   path for any UI; host-key handling documented.
5. **Packages & environment** (M16/M27): apt baseline documented; pinned
   `requirements.txt` (or `environment.yml`/image) that rebuilds cleanly.
6. **Git** (M26): the project repo with small, described commits; no secrets,
   no bulk data, no generated junk.
7. **Dataset management** (M07/M08/M23): dataset ingested on schedule,
   checksum-verified, validated (dirty rows **quarantined with a report**, not
   silently dropped).
8. **Storage** (M17/M29): designed layout (dedicated volume or justified
   alternative; Postgres via `\copy` if Pattern 2); usage visible in docs.
9. **Networking & firewall** (M21/M25): ports documented with a *reason each*;
   ufw default-deny with explicit allows; loopback/tunnel posture for anything
   sensitive.
10. **Jupyter** (M27/M31): reachable via tunnel from the host; kernel = project
    env; shut-down discipline shown.
11. **Process management** (M18/M20): API as systemd **user** unit with
    `Restart=`; the model job launched per the pre-flight (nice, logged,
    checkpointed if resumable); tmux habit evidenced.
12. **Logging & monitoring** (M24 + clinics): structured logs per component;
    `health.sh` (Mini-Project E adapted) one-page report; watchdog/resource
    evidence for the model run.
13. **Backup & restore** (M24/M23): snapshots of data + config + DB dump to a
    second location, retention policy stated — and a **performed,
    diff-verified restore test**.
14. **Bash automation** (M10/M11): `ingest.sh`, `backup.sh`, `health.sh`,
    setup script — all shellcheck-clean, strict-mode, idempotent where they
    re-run.
15. **Docker** (M28 — track-dependent): at least one containerized component
    (the API, or the whole stack in the Docker track), image built from a
    pinned base, tagged by commit SHA.
16. **Security hardening** (M25): checklist applied and *documented with
    evidence*; secrets management per §7.
17. **Troubleshooting** (M32-clinic): one **instructor-injected incident**
    diagnosed from evidence and written up (see §9); your own incident notes
    from the build weeks.
18. **Documentation** (§8): runbook, architecture diagram, README, incident
    report, restore-test evidence.

## 5. Milestones & checkpoints

| Phase | Week | Checkpoint deliverable | Graded at |
|---|---|---|---|
| 1. Proposal | 1 | 1-page `docs/proposal.md`: scenario, data, pipeline sketch, component choices (cron vs timer; venv vs Docker), health/backup plan — **instructor sign-off** | 5% |
| 2. Build | 2–3 | Working pipeline + storage + model; repo with clean history; first scheduled runs logged | 25% (rubric areas 1–4) |
| 3. Operate | 4 | Hardening checklist evidenced; monitoring + backup + **restore test**; **injected incident** diagnosed and reported | 30% (areas 5–7, 9) |
| 4. Document | 5 | Runbook (peer-tested), architecture diagram, reproducibility statement | 20% (areas 8–10) |
| 5. Present | 5 | Live demo (10 min) + **viva** (10 min) | 20% (demo protocol + viva) |

Checkpoint artifacts are committed to the repo by the phase deadline; late
evidence is worth evidence-with-penalty, so commit *as you go*.

## 6. Week-by-week instructions

**Week 1 — Proposal (Phase 1).** Choose Pattern 1 (sensor telemetry), Pattern
2 (sales reporting — see `datasets/`), or propose your own equivalent. Write
the proposal: data source and shape, pipeline sketch (boxes and arrows you can
defend), component choices *with one-sentence justifications*, and the
health/backup plan. Snapshot the VM (`pre-capstone`). Create the repo from
[STARTER.md](STARTER.md). Prove scheduling works with a trivial "hello
pipeline" before building the real one.

**Weeks 2–3 — Build (Phase 2).** Stand up storage; write the pipeline scripts
(idempotent, lockfile, validation report, quarantine); train the model from
the pipeline (pinned env, logged); deploy the API behind nginx as a user unit;
get three scheduled runs logged end-to-end. Commit small, commit often.

**Week 4 — Operate (Phase 3).** Walk the M25 hardening checklist against this
system and document with evidence; stand up `health.sh` and the watchdog;
build `backup.sh` with restore mode and **perform the restore test**; then
survive the injected incident: diagnose from evidence only, write
`incident-report.md` (eight-step method, M32-clinic template).

**Week 5 — Document & present (Phases 4–5).** Peer-test the runbook (a
classmate performs two operations using *only* your document — their friction
list goes in your appendix); finalize the architecture diagram; rehearse the
demo per the rubric's four beats. The viva follows the demo.

## 7. Security requirements (non-negotiable)

- **No secrets in Git, ever.** Secrets live in env files outside the repo,
  mode `600`; the repo carries `env.example` only. A committed secret is a
  −15 deduction plus a mandatory history-remediation exercise (M26 Lab 2,
  patient 2's lesson: rotate first).
- **SSH key-only**; password auth off; the *rollback* (how you'd recover if
  the key is lost) documented and plausible.
- **Firewall**: default deny; every allow rule has a one-line justification;
  loopback/tunnel posture for Jupyter and anything administrative. "Open it
  temporarily" is not a rule; it's a finding.
- **Least privilege**: services run as the least-privileged identity that
  works (user units; no root-owned services); the permission matrix matches
  reality (`namei -l` evidence for one deep path).
- **Destructive commands** in shipped scripts carry safeguards: dry-run
  modes, explicit paths, no `rm -rf` with variables unquoted. `curl | sudo
  bash`-style patterns: −10.
- **Secrets never in logs** — a leaked-to-log secret is *burned*: rotate, then
  fix the mechanism (M26 patient 2's order).

## 8. Documentation requirements

| Document | Standard |
|---|---|
| `README.md` | Overview, architecture summary, quickstart that *actually works* from fresh clone |
| `docs/proposal.md` | Phase-1 artifact, signed off |
| `docs/runbook.md` | Six sections (M29 standard): start/stop, health, logs, restore, rollback, common failures — commands exact, expected outputs stated; **peer-tested** |
| `docs/incident-report.md` | Eight-step method template; evidence-quoted; prevention concrete |
| `docs/restore-test.md` | Performed restore: checksums, timed RTO, model-loads proof |
| `assets/architecture.png` (or `.svg`) | Every component from §3, data directions, and the trust boundaries |
| Reproducibility statement | "Fresh clone → working system" in ≤ N documented steps; a classmate's successful rebuild cited |

## 9. Troubleshooting requirements

- **The injected incident** (Phase 3): the instructor introduces one failure
  from the [incident bank](../instructor/INCIDENTS.md) — disk fills, a
  dependency breaks, the API dies, DNS poisons, permissions drift. You get
  the *symptom only*. Deliverable: `incident-report.md` using the eight-step
  method (define → evidence → component → hypotheses → safe test → fix →
  verify → document), evidence quoted, prevention concrete.
- **Your own incident notes**: during build weeks, failures you solved go into
  `lab-log.md` as mini-reports (M32-clinic's journal discipline). Two good
  self-reported incidents ≈ one injected one in viva currency.
- The demo includes **breaking something benign live** and recovering using
  your own runbook — the runbook's accuracy is thereby tested in public.

## 10. Environment tracks (choose one, justify in the proposal)

| Track | Setup | Notes |
|---|---|---|
| **Ubuntu VM** (primary) | M04 VM; snapshots as rollback; full systemd incl. user units; full ufw | Most faithful to the course; recommended |
| **WSL2** (supported) | Ubuntu distro; systemd enabled (`/etc/wsl.conf`); user units work; ufw available but the *Windows* firewall is the real edge — document the difference | Acceptable where VMs are impractical; note the network model honestly |
| **Docker all-in-one** | The whole stack in compose (M28): services instead of user units; healthchecks replace `systemctl is-active`; "firewall" = published ports on loopback | Valid engineering; the runbook must translate the M20/M25 concepts to container equivalents — the translation itself is graded |

Cloud/GPU is **optional and uncredited** — every requirement is satisfiable
locally; a cloud-deployed project earns no extra points and assumes all
cloud-risk itself.

## 11. Deliverables checklist (committed to the repo)

- [ ] Approved `docs/proposal.md`
- [ ] Working pipeline: three scheduled runs logged end-to-end
- [ ] Validation report + quarantine evidence
- [ ] Storage layout + (Pattern 2) loaded DB
- [ ] Model artifact + training log + watchdog CSV
- [ ] API as user unit behind nginx; health endpoint; restart-survival proof
- [ ] Hardening checklist, applied and evidenced
- [ ] `health.sh` report + backup snapshots + **restore test** (diff-verified, model-loads)
- [ ] `incident-report.md` (injected incident, eight-step method)
- [ ] `runbook.md` (peer-tested) + architecture diagram + README
- [ ] Reproducibility statement + classmate rebuild citation
- [ ] Clean Git history (small commits, no secrets/junk)

## 12. Extension challenges (optional; viva currency, not rubric points)

- **E1 — Blue-green deploy**: run v2 beside v1, flip nginx, keep v1 for
  rollback (M29-ext lesson 3). Demonstrate the flip and the rollback.
- **E2 — Ansible the setup**: encode your provisioning as a playbook
  (M29-ext A lesson 4); demonstrate convergence on a broken second node.
- **E3 — CI the pipeline**: a GitHub Actions workflow (run via a local
  `act`-class runner) that tests + shellchecks + smoke-tests on every push
  (M29-ext C).
- **E4 — IaC the host**: a Terraform manifest (reading + plan output against
  a local provider, e.g. docker) that declares the stack (M29-ext B/C).
- **E5 — Canary metrics**: metrics-based promotion — the pipeline scores two
  models and promotes the better by a configurable margin, with the decision
  logged (M27/M31 lesson 3).

Each extension: one page of evidence in `docs/extensions.md` + a live
demonstration on request.

---

*The rubric your instructors grade against: [../instructor/RUBRIC.md](../instructor/RUBRIC.md).
The viva question bank: [../instructor/VIVA.md](../instructor/VIVA.md) — read it
as a study guide; every question traces to a course module.*
