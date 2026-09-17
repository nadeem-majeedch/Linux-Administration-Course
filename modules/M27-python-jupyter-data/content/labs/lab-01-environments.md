# Lab 1 — Environments: Build, Freeze, Recreate, Verify

> Module 27 · Unit 7 · Difficulty: Intermediate
> Time: ~50 min · Environment: your own VM
> Prerequisites: [Lesson 1](../lessons/01-python-on-linux.md)
> ⚠️ Project-local `.venv` only; no system installs; the lab's
> proof is a *recreated* environment, not a remembered one.

The reproducibility contract, enforced: build an environment,
freeze it, destroy it, rebuild it **as another user**, and prove
the two environments agree. This is "requirements.txt works" made
demonstrable — the environment twin of M24's test-restore.

## Part A — build (15 min)

```console
$ mkdir -p ~/projects/sales-analysis && cd ~/projects/sales-analysis
$ python3 -m venv .venv && source .venv/bin/activate
(.venv) $ python -m pip install "pandas==2.2.3" "numpy==2.1.3" "matplotlib==3.9.2" "scikit-learn==1.5.2"
(.venv) $ pip check                     # dependency sanity — must be silent
```

Record: total install size (`du -sh .venv`) and the wheel-vs-build
behavior in the pip output (wheels download; nothing compiles —
Lesson 1 §3's point, witnessed).

## Part B — prove isolation (10 min)

```console
(.venv) $ pip show pandas | grep Location     # inside the venv tree
(.venv) $ python -c "import pandas; print(pandas.__file__)"
(.venv) $ deactivate
$ python3 -c "import pandas"                   # ModuleNotFoundError — system has none
$ echo $?                                      # 1 — the honest exit
```

The pair of transcripts *is* the isolation proof. Then the PATH
witness: `which python` before/after activation, and the
no-activation invocation
(`~/projects/sales-analysis/.venv/bin/python -c "import pandas;
print('ok')"`) — the scheduled-job trick, working.

## Part C — freeze (5 min)

```console
$ source .venv/bin/activate
(.venv) $ pip freeze > requirements.txt
(.venv) $ wc -l requirements.txt               # note: far more than the 4 you named
```

Read five lines of the freeze: transitive dependencies, exact
pins. That's the reproducibility cost — and the reason
`requirements.txt` is committed while `.venv` is ignored
([M26](../../../M26-git-dev-workflows/README.md) previews this
`.gitignore`).

## Part D — recreate as a second user (15 min)

The verification that earns the contract:

```console
$ sudo useradd -m -s /bin/bash qa && sudo -u qa bash
qa@vm:~$ python3 -m venv .venv && source .venv/bin/activate
qa@vm:~$ pip install -r /home/ds/projects/sales-analysis/requirements.txt   # (or scp it)
qa@vm:~$ python -c "import pandas, numpy, matplotlib, sklearn as sk; print(pandas.__version__, numpy.__version__, sk.__version__)"
```

The version string must match your Part A versions **exactly**
(compare against `pip freeze`'s four). Then the negative test —
recreate *without* the file (`pip install pandas` unpinned) on a
third venv and compare `pip freeze` outputs: the drift is why
pinning exists.

## Part E — the migration preview (5 min)

Create `~/projects/sales-analysis/data/{raw,processed}/`, drop a
CSV into `raw/`, `chmod -R a-w data/raw/`, then try `echo "x" >
data/raw/test.csv` — read-only by convention, enforced. Write the
three-line project `.gitignore` preview (`.venv/`, `outputs/`,
`.ipynb_checkpoints/`) — [Lab 2](lab-02-jupyter-remote.md) uses
this project as its home.

## Done when

- [ ] Part B's isolation pair recorded; Part C's freeze line
      count noted
- [ ] Part D: second-user import versions **match** the freeze —
      the unpinned-drift comparison pasted
- [ ] Part E: read-only raw enforced (the failed write quoted)
- [ ] One paragraph: what would break in a teammate's hands if
      `requirements.txt` were missing — or unpinned
