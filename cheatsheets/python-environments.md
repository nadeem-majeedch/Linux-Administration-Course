# 16 — Python Environments

> Learn it: [M27 — Python, Jupyter & Data on Linux](../modules/M27-python-jupyter-data/content/README.md) ·
> [M15 — Environment Variables](../modules/M15-environment-variables/content/README.md) ·
> Lookup, not understanding.

## venv — the default tool

| Command | Purpose | Notes |
|---|---|---|
| `python3 -m venv .venv` | create environment in-project | name `.venv` = visible convention, gitignored |
| `source .venv/bin/activate` | activate this shell | prompt shows `(.venv)` |
| `deactivate` | leave | — |
| `which python3` | **prove which interpreter is live** | first diagnostic, always |

⚠️ Activation only edits this shell's `PATH` — cron, systemd units
and other terminals don't inherit it. There, call the venv's
interpreter by **absolute path**:
`/home/ana/proj/.venv/bin/python script.py`.

## pip — inside the venv only

| Command | Purpose | Notes |
|---|---|---|
| `python3 -m pip install PKG` | install | **explicit `python3 -m pip` beats bare `pip`** — guarantees the interpreter you're looking at |
| `pip install 'pandas>=2.0,<3'` | constrain version | reproducibility lives in constraints |
| `pip install -r requirements.txt` | install pinned set | the project contract |
| `pip list` | what's installed here | — |
| `pip show PKG` | version, location, deps | — |
| `pip freeze > requirements.txt` | pin the environment | ideally after `pip uninstall -y pip-tools`-style cleanup; freeze pins transitively |
| `pip check` | broken dependency audit | cheap, catches the weird |
| `pip install --upgrade PKG` | update one | ⚠️ can drag transitive upgrades — check `pip check` |

⚠️ On Ubuntu 24.04, `pip install` into **system** Python fails with
`externally-managed-environment` (PEP 668) — apt owns that
interpreter. The fix is a venv, **not** `--break-system-packages`
as a habit.

## The interpreter maze (why "it works" lies)

| Symptom | Actual cause | Diagnosis |
|---|---|---|
| `ModuleNotFoundError: pandas` | running interpreter ≠ install target | `which python3` in shell; in the notebook, `import sys; sys.executable` |
| `pip install` "succeeds", import fails | pip belonged to another Python | `pip -V` — it names its Python and path |
| works in shell, fails in cron/systemd | activation didn't follow the job | absolute venv path in the unit/cron line |
| `ERROR: Can not perform a '--user' install` | venv active + `--user` flag | `--user` is only for system installs; drop it |

## PATH & the environment (15-minute refresher set)

| Command | Purpose |
|---|---|
| `echo $PATH` | where shells look for executables, in order |
| `echo $VAR` / `printenv` | inspect |
| `export VAR=value` | export to children of this shell |
| `VAR=value CMD` | per-command env (no export needed) |
| `env \| grep -i token` | ⚠️ audit what secrets you're exporting |

Shell startup reads `~/.profile` (logins) / `~/.bashrc`
(interactive shells) — environment quirks differ by context, which
is the whole M15 lesson.

## Secrets — the environment contract

```bash
# .env  (gitignored)          # load: set -a; source .env; set +a
DATABASE_URL=postgres://…     # apps read config from env, never argv
API_KEY=…                     # argv shows up in ps; env does not
```
Secrets: live in gitignored files or a secrets manager, referenced
by units via `EnvironmentFile=`; never in shell history, never in
`git log`, never echoed to logs.

## Reproducibility chain (pin everything)

```text
code  → git SHA
env   → requirements.txt (or conda env export / lock file)
data  → checksums (sha256sum) recorded, not rewritten
run   → timestamped directory + saved config
```

## conda / micromamba (translation table)

| Task | venv+pip | conda |
|---|---|---|
| create | `python3 -m venv .venv` | `conda create -n ds python=3.12` |
| activate | `source .venv/bin/activate` | `conda activate ds` |
| install | `pip install pandas` | `conda install pandas` (or pip inside) |
| export | `pip freeze > req.txt` | `conda env export > env.yml` |
| delete | delete the directory | `conda env remove -n ds` |

Course default: venv+pip. Conda earns its keep for compiled/ML
stacks (CUDA wheels, MKL) — and `micromamba` brings that without
needing root.
