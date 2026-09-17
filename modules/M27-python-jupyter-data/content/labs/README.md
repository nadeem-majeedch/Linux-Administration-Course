# Module 27 Labs — Python, Jupyter & Data Workloads

> Three labs under `~/projects/` (the course's project-home
> convention starts here). Environments are project-local
> (`.venv`), installs respect PEP 668, Jupyter binds loopback with
> token auth, batch jobs run capped and logged.

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-environments.md](lab-01-environments.md) | Build a pinned env, freeze `requirements.txt`, **recreate on a second account**, verify imports match | ~50 min |
| 2 | [lab-02-jupyter-remote.md](lab-02-jupyter-remote.md) | Headless Jupyter on the VM → M22 tunnel → host browser → analysis notebook over `datasets/` → clean shutdown | ~55 min |
| 3 | [lab-03-batch-scheduling.md](lab-03-batch-scheduling.md) | Training-style script via tmux + nohup with progress logs, polite stop (M18), checkpoint verification | ~50 min |

Standing rules (recap):

- `python3 -m venv .venv` per project; `python -m pip` inside it.
- `pip freeze > requirements.txt` at milestones; recreate-to-verify.
- Jupyter: `--no-browser --port=8888 --ip=127.0.0.1`; reach it by
  tunnel only.
- Background jobs: nohup/tmux, log contract, nice, caps, PID
  recorded.
- `data/raw/` is read-only by convention; `.venv`, `outputs/`,
  `.ipynb_checkpoints/` are git-ignored.
