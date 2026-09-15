# Capstone Rubric — 100 Points

Grading is evidence-based: if it isn't demonstrated (log, transcript, diff, live
demo), it doesn't score. Partial credit follows the tables below.

| # | Area | Points | What full credit looks like |
|---|---|---|---|
| 1 | **Pipeline correctness** | 15 | Scheduled runs complete end to end; validation report produced; dirty rows quarantined with evidence; three logged runs shown |
| 2 | **Storage design** | 8 | Dedicated volume mounted via fstab with `nofail` (or justified alternative); DB loaded via `\copy`; layout documented |
| 3 | **Model job** | 8 | Pinned env, scripted training, artifact versioned, run logged; runs < 2 min CPU |
| 4 | **Serving stack** | 12 | API as systemd user unit behind nginx; health endpoint; survives restart (`systemctl restart` → still healthy); 502 diagnosed live if induced |
| 5 | **Security hardening** | 12 | M25 checklist applied and documented; SSH key-only with tested rollback; secrets in env files, correct permissions, absent from Git; ufw rules minimal and justified |
| 6 | **Observability** | 10 | `health.sh`-style report accurate; logs queryable and structured; watchdog CSV present; operator can answer "what happened at 02:00?" from logs alone |
| 7 | **Backup and restore** | 10 | Snapshots + DB dump exist on second location; **restore test performed and diff-verified**; retention policy working |
| 8 | **Reproducibility** | 8 | Fresh-clone → working system via documented steps (pinned venv or Docker); missing steps count against |
| 9 | **Documentation** | 12 | Runbook usable by a peer (peer-tested in class); architecture diagram; README; incident report quality |
| 10 | **Git hygiene** | 5 | Small, described commits; sensible branches; no secrets, no bulk data, no generated junk committed |
| | **Total** | **100** | |

## Grade bands

| Band | Meaning |
|---|---|
| 90–100 | System is boringly reliable: it runs, logs, restores, and explains itself. Ready for a real team. |
| 75–89 | Solid system with gaps in one or two operational areas (commonly restore testing or runbook depth). |
| 60–74 | Core pipeline works but operations are thin: monitoring/backups/docs incomplete. |
| < 60 | Pipeline unstable or evidence missing. Retake with fixes; the rubric doubles as the improvement list. |

## Non-negotiables (automatic deductions)

- Any secret committed to Git: −15 and mandatory history remediation exercise.
- Any restore claim without a performed restore test: backup area scores 0.
- Destructive commands without documented safeguards (dry-run/snapshot): −10 first
  occurrence.
- `curl | sudo bash`-style patterns in shipped scripts: −10.

## Live demo requirements (10 minutes)

1. Show the system healthy (health report + service status).
2. Trigger a pipeline run live (or show the three most recent logged runs).
3. Break something benign on the spot (instructor picks): kill the API, fill a
   small partition, corrupt a config — then recover using your own runbook.
4. Show a log query answering a question about last night's run.
