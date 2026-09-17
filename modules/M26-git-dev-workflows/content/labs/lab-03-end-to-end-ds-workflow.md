# Lab 3 — The End-to-End Data Science Workflow on Linux

> Unit 7 capstone · Modules [M22](../../../M22-ssh-remote-admin/README.md) ·
> [M26](../../README.md) · [M27](../../../M27-python-jupyter-data/README.md) · Difficulty: Intermediate+
> Time: ~75 min · Environment: your own VM as the "server"
> ⚠️ All work on your own machine; nothing leaves it, nothing is committed
> anywhere but your practice repos.

One sitting, one pipeline — the daily loop of a professional data scientist,
staged on your own VM so every link in the chain is yours to inspect:

```text
Linux server → SSH → Git repository → Python venv → dataset
→ Jupyter (tunneled) → analysis → outputs → committed back to Git
```

Nothing here is new; that's the point. Each stage has a module behind it.
The lab's value is *sequencing* — doing them in order, cleanly, the way a
real session on a university GPU server goes.

## Stage 0 — inventory (5 min)

Confirm the four load-bearing pieces exist before chaining them:

```console
$ ssh ds@<vm-ip> 'echo connected'            # M22: key-based, no password prompt
$ which git && git --version                 # this module
$ ssh ds@<vm-ip> 'python3 --version'         # M27: system Python 3 present
$ ls ~/repos/ 2>/dev/null || echo "no bare repos yet"
```

Any failure: fix it *now* with the module that owns it — do not chain work
on top of a broken link.

## Stage 1 — repository on the server (10 min)

On the VM, create the remote (bare) and clone it into a project — the
Lesson 3 §1 pattern, now playing the role of "the department GitLab":

```console
$ git init --bare ~/repos/ds-capstone.git
$ git clone ~/repos/ds-capstone.git ~/projects/ds-capstone
$ cd ~/projects/ds-capstone
```

## Stage 2 — venv first, `.gitignore` first (10 min)

The M27 order — environment and exclusions *before* any code exists:

```console
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ python3 -m pip install pandas matplotlib jupyterlab ipykernel
(.venv) $ pip freeze > requirements.txt
$ printf '.venv/\noutputs/\ndata/raw/\ndata/processed/\n.ipynb_checkpoints/\n*.log\n' > .gitignore
$ git add .gitignore requirements.txt
$ git commit -m "Pin environment and exclude derived artifacts"
```

Two deliberate choices to notice: `requirements.txt` *is* committed
(environments are files — M27 Q3), while `.venv/` never is; and the
`.gitignore` predates the first dataset — Lesson 3 §2's "prevention" rule.

## Stage 3 — dataset with permissions hygiene (10 min)

```console
$ mkdir -p data/raw data/processed outputs
$ printf 'region,revenue\nnorth,1200\nsouth,850\nnorth,300\neast,410\n' > data/raw/sales.csv
$ chmod -R a-w data/raw/          # read-only raw: the accidental-overwrite guard (M27 Q18)
$ git add data/raw/README.md 2>/dev/null || {
    echo "Raw data comes from the CRM export of 2026-09-01; do not edit." > data/raw/README.md
    chmod a-w data/raw/README.md
    git add data/raw/README.md && git commit -m "Document raw data provenance"
  }
```

Raw data itself stays out of Git (ignored, Stage 2); its **provenance note**
goes in. That split — data out, metadata in — is the standard DS-repo
compromise.

## Stage 4 — Jupyter over a tunnel (15 min)

From your **physical machine** (M22 + M27 Lab 2 §C):

```console
$ ssh -L 9999:127.0.0.1:8888 ds@<vm-ip> -N &
```

On the VM, register the venv kernel and start headless:

```console
(.venv) $ python -m ipykernel install --user --name ds-capstone
(.venv) $ cd ~/projects/ds-capstone && jupyter lab        # binds 127.0.0.1 by default
```

Browse `http://127.0.0.1:9999` locally, token from the VM's banner. New
notebook → kernel **ds-capstone** (the Stage 2 venv — M27 Q9's rule in
action) → run the analysis:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/sales.csv")
summary = df.groupby("region")["revenue"].agg(["sum", "mean", "count"])
summary["sum"].plot(kind="bar", title="Revenue by region")
plt.tight_layout()
plt.savefig("outputs/revenue_by_region.png", dpi=150)
summary.to_csv("outputs/summary.csv")
summary
```

Save as `notebooks/analysis.ipynb`, then **clear outputs** before it's
committed (Lesson 3 §4) — commit the *code cell*, not the embedded plot.
Shut down Jupyter politely when done (M27 Q11) and kill the tunnel.

## Stage 5 — outputs back into history (15 min)

The last link: results committed with context. On the VM:

```console
$ git add notebooks/analysis.ipynb outputs/summary.csv
$ git commit -m "Add regional revenue analysis with grouped summary"
$ git log --oneline --stat -3      # history shows what each commit carried
$ git push origin main
```

`outputs/` was ignored in Stage 2 — but `summary.csv` staged *by explicit
name* overrides the ignore (Lesson 3 §2's deliberate-exception clause).
Decide consciously, per artifact: notebooks and key result tables belong
in history; regenerable PNGs and logs don't. Re-run the notebook cell and
confirm the PNG regenerates — the proof that ignoring it was safe.

Finally, the full-circle check from a *fresh* directory — the reproducibility
claim made physical:

```console
$ git clone ~/repos/ds-capstone.git ~/tmp-verify && cd ~/tmp-verify
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install -r requirements.txt -q
$ python -c "import pandas; df = pandas.read_csv('../projects/ds-capstone/data/raw/sales.csv'); print(df.groupby('region')['revenue'].sum())"
```

Fresh clone + pinned env + raw data = same numbers. That chain — Git,
requirements, provenance note — is what a supervisor re-runs in six months.

## Stage 6 — the debrief (5 min)

Answer in `lab-log.md`:

1. Which stage failed first for you, and which module's troubleshooting
   page solved it?
2. Where could this pipeline break for a *teammate* cloning it? (Three
   candidates: raw data path, kernel registration, tunnel config.)
3. Name the two artifacts you *deliberately* did not commit, and the rule
   behind each.

## Done when

- [ ] Stages 0–5 all evidenced in `lab-log.md` (one block each)
- [ ] Raw data read-only; provenance note committed; data itself ignored
- [ ] Notebook committed *with outputs cleared*; `summary.csv` staged by name
- [ ] Fresh-clone verification prints the same regional sums
- [ ] Debrief's three questions answered

**Where this leads:** the [capstone project](../../../../projects/capstone/student/SPEC.md)
does this loop for real, with Docker (M28) wrapping the environment and a
cloud target (M30) replacing your VM.
