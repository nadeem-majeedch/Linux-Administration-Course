# Lesson 2 — Jupyter on Linux: Headless, Tunnels and Data Directories

> Module 27 · Unit 7 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 2 — Jupyter remote](../labs/lab-02-jupyter-remote.md)
> Up next: [Lesson 3 — background workloads](03-background-workloads.md)

---

## 1. What Jupyter actually is — three moving parts

"Running a notebook" involves a *server* (the web app you see), one
or more *kernels* (the processes that actually execute your code —
one Python process per running notebook), and a *browser* (just a
client). On Linux the server is a process you start, configure,
authenticate, and — critically — bind to an interface deliberately
(M21's bind-scope discipline applies to Jupyter more than anywhere
else in DS life).

```console
$ python3 -m venv .venv && source .venv/bin/activate
(.venv) $ pip install jupyterlab pandas matplotlib
(.venv) $ jupyter lab --version
```

JupyterLab is the modern interface (Notebook 7 shares its
foundation); both run identically as servers — the course uses
`jupyter lab` throughout.

## 2. Headless launch — the server without a desktop

On a server there's no browser to open; the flag pair that makes
Jupyter a *Linux service* rather than a desktop app:

```console
(.venv) $ jupyter lab --no-browser --port=8888 --ip=127.0.0.1
[I 21:04:11.042 LabApp] Jupyter Server 2.14.1 is running at:
[I 21:04:11.042 LabApp]     http://127.0.0.1:8888/lab?token=9f3b7c1d...
```

The three flags and their reasons: `--no-browser` (no GUI
attempt), `--port` (chosen, not random — your tunnel depends on
it), and `--ip=127.0.0.1` — **the default and the correct default**:
the server listens on loopback only, unreachable from any network.
The startup line's **token** is the auth: every browser/client
must present it (the URL includes it; you paste it once per
browser).

The professional variant — persistent, configured once in
`~/.jupyter/jupyter_lab_config.py`:

```python
c.ServerApp.ip = "127.0.0.1"
c.ServerApp.port = 8888
c.ServerApp.open_browser = False
c.ServerApp.root_dir = "/home/ds/projects"   # the visible filesystem root
```

`c.ServerApp.root_dir` scopes what notebooks can touch — the
Jupyter-flavored version of least privilege: the server's file
browser starts *at your project*, not at `$HOME` or `/`.

## 3. Remote access — the tunnel, never the exposure

The university-GPU scenario: Jupyter runs on a server you SSH to;
your browser is on your laptop. The wrong move is
`--ip=0.0.0.0` (a token-protected but network-exposed notebook
server — and a target). The right move is
[M22's](../../../M22-ssh-remote-admin/content/README.md) local
forward:

```console
# on the server:
(.venv) $ jupyter lab --no-browser --port=8888 --ip=127.0.0.1
# on your laptop:
$ ssh -L 8888:localhost:8888 vm -N
# in the laptop's browser:
http://localhost:8888/lab?token=...
```

The browser talks to *your* loopback; the SSH tunnel carries it,
encrypted and authenticated by your key, to the *server's*
loopback — where Jupyter sits, exposed to nothing. The security
posture: two authentications (your key, the token), one exposed
port (22), zero web-facing Jupyter. When a teammate says "just
open the port to the campus network", this paragraph is the reply.
(TensorBoard, Spark UIs, every dev server — same tunnel pattern;
M29's nginx adds the reverse-proxy alternative for shared
services.)

## 4. Kernels — the processes behind the tabs

Each running notebook owns a **kernel** process (`python` from
*that* Jupyter's environment — the venv's interpreter). The
consequences worth knowing:

- **Kernel = environment.** A notebook uses the venv Jupyter was
  installed in — `import pandas` succeeds there because pandas is
  in *that* `site-packages`. "ModuleNotFoundError" in a notebook
  whose venv has the module is almost always a *different
  environment's* Jupyter running (Troubleshooting #3).
- **Kernels are processes** — restartable (Kernel → Restart — the
  honest fix for corrupted global state), interruptible (Kernel →
  Interrupt = SIGINT, M18), and *killable* when wedged
  (`pgrep -af jupyter`, then the M18 ladder).
- **Memory persists across cells** — deleted a 2 GB DataFrame?
  Restart the kernel; "it's still using RAM" is stale references,
  not a leak.

**From notebook to script** — the graduation path:

```console
(.venv) $ jupyter nbconvert --to script analysis.ipynb     # → analysis.py
(.venv) $ python analysis.py                                # the batch form (Lesson 3)
```

Notebooks are for *exploration*; the scheduled/production form is
the script — `nbconvert` is the bridge, and stripping outputs
(`--ClearOutputPreprocessor.enabled=True`) keeps secrets and
bloat out of [M26's](../../../M26-git-dev-workflows/README.md)
commits.

## 5. Data directories, permissions and big files

The Linux conventions that keep a DS project sane:

```text
project/
├── data/            # input data — read-only by convention (chmod -R a-w on shared)
│   ├── raw/         # untouched originals (never edited in place)
│   └── processed/   # derived — regenerable from raw + code
├── notebooks/       # exploration
├── src/             # scripts that earned their keep (nbconvert graduates)
├── outputs/         # results, figures — regenerable, git-ignored
└── requirements.txt # the environment contract (Lesson 1 §4)
```

- **Permissions**: on shared servers, `data/raw/` is setgid + group-
  writable-or-read-only per [M13](../../../M13-ownership-shared-access/content/README.md)
  — teammates read what they should, can't clobber originals. Your
  own project: `chmod -R a-w data/raw/` after the ingest is the
  "I promise I won't edit the raw file" trick.
- **Large datasets** — the [M10](../../../M10-bash-scripting/content/README.md)
  rule with GBs attached: **never commit data to Git** (M26 §remotes
  names Git LFS for the exceptions). Chunked reading is the Python
  habit (`pd.read_csv(..., chunksize=100_000)`), streaming instead
  of loading; and `du -h --max-depth=1 data/` (M24) before a
  backup decides whether "the dataset" needs archiving or just its
  checksum manifest.

## 6. Try it now (20 minutes)

1. Headless launch: start Jupyter per §2, read the token line,
   `curl -sI http://127.0.0.1:8888` (403 without token — auth
   working), then `ss -tlnp | grep 8888` (loopback only — the
   posture, witnessed).
2. The tunnel: from your host, `ssh -L 8888:localhost:8888 vm -N`,
   open the tokened URL in a real browser, run a cell printing
   `socket.gethostname()` — the *server's* name proves where code
   executes.
3. Kernel forensics: with the notebook running, `pgrep -af
   jupyter` and `ps --forest` (M18) — find the server, the kernel,
   and their tree. Restart the kernel from the UI; watch the PID
   change.
4. nbconvert: write a 3-cell notebook, convert to script, run the
   script — the exploration-to-production bridge, walked.

## 7. Common mistakes

- Binding `--ip=0.0.0.0` "so my teammate can reach it" — token
  auth is not a firewall; the tunnel or [M29's
  proxy](../../../M29-web-servers-databases/content/README.md) is the
  shared-access answer.
- Leaving servers running on shared machines — `pgrep -af jupyter`
  on a GPU box shows weeks of orphans; start deliberately, stop
  deliberately (`systemctl --user stop` or the M18 ladder).
- Running `jupyter lab` from `$HOME` with no `root_dir` — the file
  browser now exposes and edits everything; scope it (§2).
- Editing raw data in notebooks — the raw/processed split (§5)
  exists because notebooks *will* be rerun out of order.
- Committing `.ipynb_checkpoints/` and output-stuffed notebooks —
  gitignore both; nbconvert-with-clear-outputs for what ships.

> **Up next:** [Lesson 3 — background
> workloads](03-background-workloads.md): the training run as a
> first-class Linux job — nohup, tmux, caps, and logs that prove it
> worked.
