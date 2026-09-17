# Module 27 — Python, Jupyter & Data Workloads · Content Index

> **Status:** Content complete — 4 lessons, 3 labs, quiz + key, 8
> challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate.

> 🟡 **Module safety contract:** environments live *inside* project
> directories (`project/.venv`), never in `$HOME` root; installs
> respect PEP 668 (never `sudo pip`); Jupyter binds loopback with
> token auth; training-style jobs run under resource caps with logs.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-python-on-linux.md](lessons/01-python-on-linux.md) | system Python & the distro's relationship to it, PEP 668, interpreters on PATH, `python3 -m venv`, activation as env mutation, pip idioms, requirements pinning, apt-vs-pip rule |
| 2 | [02-jupyter-on-linux.md](lessons/02-jupyter-on-linux.md) | Jupyter architecture (server/kernel/browser), headless launch, token auth, SSH-tunnel remote access (M22), kernels, nbconvert to scripts, data-directory conventions & permissions |
| 3 | [03-background-workloads.md](lessons/03-background-workloads.md) | the training-run pattern: nohup/tmux/systemd-user options, logs with progress lines, resource caps (M18/M24), GPU vocabulary (nvidia-smi/CUDA), long-dataset CLI habits |
| 4 | [04-cli-python.md](lessons/04-cli-python.md) | command-line Python: `python -c` one-liners, `-m` module idioms, json.tool/csv/sort pipelines, script shebangs, exit codes — Python joining the M08/M11 pipeline world |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-environments.md](labs/lab-01-environments.md) | Create a pinned env (pandas/numpy/matplotlib/scikit-learn), freeze to `requirements.txt`, recreate on a second account, verify imports match |
| 2 | [lab-02-jupyter-remote.md](labs/lab-02-jupyter-remote.md) | Launch headless Jupyter on the VM, tunnel from host (M22), run an analysis notebook over `datasets/`, shut down cleanly |
| 3 | [lab-03-batch-scheduling.md](labs/lab-03-batch-scheduling.md) | Run a small training-style script via tmux + nohup, watch logs, stop politely (M18 signals), verify outputs survived |

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M15 env vars](../../M15-environment-variables/README.md) —
  activation *is* environment mutation; PATH mechanics.
- [M16 packages](../../M16-package-management/content/README.md) —
  apt vs pip, PEP 668, the five-beat install.
- [M22 SSH](../../M22-ssh-remote-admin/content/README.md) — the
  tunnel to remote Jupyter; keys for the whole remote workflow.
- [M18/M24](../../M24-logs-journald-monitoring/content/README.md) —
  background jobs, caps, logs, OOM post-mortems.
- [M26 Git](../../M26-git-dev-workflows/README.md) — venvs and
  data are *ignored*; code and `requirements.txt` are committed.
- [M29 deployment](../../M29-web-servers-databases/content/README.md) —
  the app's venv + uvicorn unit is this module's pattern, deployed.
