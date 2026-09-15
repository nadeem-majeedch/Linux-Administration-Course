# projects/mini-projects/

Six mini-projects (A–F) punctuate the course. Each brief defines the deliverable,
constraints, and grading rubric. Suggested weights live in the main README.

| ID | Module | Title | Deliverable |
|---|---|---|---|
| [A](mini-project-A-dataset-qc-toolkit.md) | M10 | Dataset QC Toolkit | Script suite (`dq.sh`, `summary.sh`) over course datasets, shellcheck-clean, documented |
| [B](mini-project-B-shared-dataset-server.md) | M13 | Shared Dataset Server Design | Access-plan document + `setup_shared_tree.sh` demo for a 6-person research team |
| [C](mini-project-C-process-watchdog.md) | M18 | Process Watchdog | Monitor script logging CPU/MEM samples to CSV with overrun alerts |
| [D](mini-project-D-remote-workstation.md) | M22 | Remote Compute Workstation | SSH keys + config + tmux workflow + persistent service + operations runbook |
| [E](mini-project-E-health-backup-kit.md) | M24 | Server Health and Backup Kit | `health.sh` + `backup.sh` with tested restore + incident report |
| [F](mini-project-F-reproducible-mini-ml.md) | M27 | Reproducible Mini-ML | Pinned venv + `train.py` + `run.sh` + log + model artifact + README, clean Git history |

## Common rules for all mini-projects

1. Work happens in the student's own VM/lab environment; nothing is run against
   shared infrastructure.
2. Every script passes `shellcheck` (from M10 onward).
3. Every project ships a short `README.md` explaining what it does, how to run it,
   and what its logs mean.
4. Destructive operations require a dry-run mode or an explicit, documented safeguard.
5. Git history counts: small, described commits (from M26 onward, projects are
   submitted as repositories).
