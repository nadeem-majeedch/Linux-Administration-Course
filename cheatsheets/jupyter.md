# 17 — Jupyter on Linux

> Learn it: [M27 — Jupyter on Linux](../modules/M27-python-jupyter-data/content/lessons/02-jupyter-on-linux.md) ·
> Lookup, not understanding.

## Install & launch

```console
$ python3 -m venv .venv && source .venv/bin/activate
$ python3 -m pip install jupyterlab pandas scikit-learn
$ jupyter lab                    # or: jupyter lab --no-browser
```

| Flag | Purpose | Example |
|---|---|---|
| `--port N` | fixed port (default 8888, auto-increments) | `jupyter lab --port 8889` |
| `--ip 127.0.0.1` | **loopback only** (the course rule on shared machines) | pair with an SSH tunnel |
| `--no-browser` | server without launching a GUI | headless/VM use |
| `--notebook-dir=DIR` | root directory | keep `$HOME` un-exposed |

**Security model:** on start, Jupyter prints a `token=…` URL — that
token *is* the login. `jupyter server list` re-shows running
servers. On shared machines: bind loopback + token + tunnel, or
configure a password (`jupyter server password`).

## Server vs kernel (the resource leak)

- **Server** = the web process (one per session you started).
- **Kernel** = the Python process per notebook, holding all its
  memory.

Closing the browser tab closes *neither*. Kernels keep training
runs, big DataFrames, and GPU memory alive invisibly.

```console
$ pgrep -af jupyter                 # census of servers
$ ps aux --sort=-%mem | head        # fat python processes = kernels
```
Shutdown properly: File → Shut Down (server), or Kernel → Shut Down
Kernel (per notebook) — the * civilized * cleanup; `pkill -f jupyter`
is the abridged version, after `pgrep -af` confirms the targets.

## Reaching a remote server (the daily pattern)

```console
# on the server:
$ jupyter lab --no-browser --ip 127.0.0.1 --port 8889

# on your laptop:
$ ssh -L 8889:localhost:8889 mlsrv
# then open http://localhost:8889 locally
```
The tunnel is authenticated by your SSH key; the service never
needs to face the network. ⚠️ Don't `--ip 0.0.0.0` a notebook
server on a shared machine to "make it easier" — that's everyone's
attack surface.

## Kernels & environments (the mismatch clinic)

A notebook runs in the kernel you *chose*, which may not be the
environment you *installed into*:

```console
$ python3 -m pip install ipykernel          # in the env you want
$ python3 -m ipykernel install --user --name ds-env --display-name "Python (ds-env)"
```
Then pick "Python (ds-env)" in the UI. The in-notebook proof:
```python
import sys; print(sys.executable)    # does it name YOUR venv?
```

## Working with notebooks from the shell

| Task | Command |
|---|---|
| run notebook headless | `jupyter nbconvert --to notebook --execute analysis.ipynb --inplace` |
| export to script | `jupyter nbconvert --to script analysis.ipynb` |
| clear outputs for committing | `jupyter nbconvert --clear-output --inplace analysis.ipynb` |
| batch & scheduling | plain `train.py` + cron/timer beats notebooks for unattended work |

Committing rule: notebooks carry outputs — clear them or
`nbstripout` them; a committed notebook with a 50 MB embedded
plot is a repo problem.

## Data-directory etiquette

| Rule | Why |
|---|---|
| notebooks reference data via paths relative to the notebook | makes `--notebook-dir` and teammates' clones work |
| read from `/data`, write results to your run directory | the shared-server contract (M31) |
| never write into the dataset directory | datasets are read-only commons |

## Troubleshooting quick table

| Symptom | Fix |
|---|---|
| `port already in use` | old server alive: `pgrep -af jupyter`, use it or kill it |
| kernel dies on import | wrong env: `sys.executable` check, re-register kernel |
| can't connect remotely | loopback bind + no tunnel — see the tunnel block above |
| token rejected | server restarted → new token; `jupyter server list` |
| notebook "hangs" | cell busy on a kernel you forgot; interrupt (⏹) then check `top` |
