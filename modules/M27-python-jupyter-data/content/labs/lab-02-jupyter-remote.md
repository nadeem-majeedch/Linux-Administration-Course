# Lab 2 — Jupyter on Your Linux Server, Tunnels Included

> Module 27 · Unit 7 · Difficulty: Intermediate
> Time: ~55 min · Environment: your own VM
> Prerequisites: [Lesson 2](../lessons/02-jupyter-on-linux.md), [M22](../../../M22-ssh-remote-admin/README.md)
> ⚠️ Jupyter binds `127.0.0.1` — *always* in this course. The
> host stays firewalled; access is by tunnel, never exposure.

From a clean, logged-out state to a *working* remote notebook,
built the way the university servers demand: headless on the VM,
tunneled from your physical machine, with config as evidence.

## Part A — server-side config (15 min)

```console
$ mkdir -p ~/projects/sales-analysis/notebooks
$ cd ~/projects/sales-analysis && source .venv/bin/activate
(.venv) $ python -m pip install jupyterlab
(.venv) $ jupyter lab --generate-config
```

Edit `~/.jupyter/jupyter_lab_config.py` (two lines matter):

```python
c.ServerApp.ip = "127.0.0.1"            # loopback, non-negotiable
c.ServerApp.root_dir = str(__import__("pathlib").Path("~/projects/sales-analysis").expanduser())
```

(Take the `root_dir` line verbatim; it pins the notebook root to
the project so the file browser can't wander.) Then note your
token:

```console
(.venv) $ jupyter lab list   # shows the URL with ?token=... (pre-start, harmless)
```

## Part B — first headless run, foreground (10 min)

```console
(.venv) $ cd ~/projects/sales-analysis && jupyter lab
```

Watch the startup banner: it advertises
`http://127.0.0.1:8888/lab?token=...`. Verify the bind from a
second VM terminal: `ss -tlnp | grep 8888` — `127.0.0.1:8888`,
not `0.0.0.0:8888`. Screenshot or transcript both, then
Ctrl-C the foreground run.

## Part C — the tunnel (15 min)

From your **physical machine** (SSH client role, M22 §1):

```console
$ ssh -L 9999:127.0.0.1:8888 ds@<vm-ip> -N &     # -N: no shell, forward only
$ curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9999/   # 302 — alive
```

Open `http://127.0.0.1:9999` in the physical machine's browser,
paste the token from Part B's banner. Inside Jupyter: new
notebook, `import pandas, sklearn` (no ModuleNotFoundError —
the *kernel's* venv, Lesson 2 §3), then cell 1:

```python
import pandas as pd
df = pd.read_csv("../data/raw/sales.csv")
df.groupby("region")["revenue"].sum().sort_values(ascending=False)
```

Save the notebook. Evidence pair: the browser URL (`127.0.0.1:9999`
— local-looking, working) and the `ss` line on the VM.

## Part D — server-side verification (10 min)

```console
$ ps aux | grep -i jupyter | grep -v grep     # user, PID, the 8888 listener
$ ls -la ~/projects/sales-analysis/notebooks/  # your .ipynb saved server-side
$ ls -la ~/.ipynb_checkpoints/ 2>/dev/null || echo "no checkpoints dir yet"
```

Then the negative test — from the physical machine, try
`curl -s http://<vm-ip>:8888` (browser too). It **fails** —
loopback only, nothing listening on the VM's LAN address. That
refusal is the security posture working. Kill the tunnel:
`kill %1` (or `pkill -f "ssh -L 9999"`).

## Part E — background run with evidence (5 min)

```console
(.venv) $ nohup jupyter lab > outputs/jupyter.log 2>&1 &
(.venv) $ echo $! > outputs/jupyter.pid && sleep 3
(.venv) $ tail -5 outputs/jupyter.log; ss -tlnp | grep 8888
```

Shut down *politely* — `kill $(cat outputs/jupyter.pid)` (SIGTERM,
jupyter checkpoints and exits cleanly; verify with
`ss -tlnp | grep 8888` again). Background discipline carries from
[M18](../../../M18-processes-jobs-signals/README.md); [Lesson 3](../lessons/03-background-workloads.md)
covers the long jobs this becomes.

## Done when

- [ ] Part B: `ss` proof of `127.0.0.1:8888` binding
- [ ] Part C: token-gated notebook working **through the tunnel**;
      the DS cell runs
- [ ] Part D: the LAN-address curl **fails** — posture proven
- [ ] Part E: log + PID evidence; clean SIGTERM shutdown recorded
- [ ] One paragraph: why a tunnel beats opening 8888 in the VM's
      firewall ([M25](../../../M25-security-firewall/README.md) echo)
