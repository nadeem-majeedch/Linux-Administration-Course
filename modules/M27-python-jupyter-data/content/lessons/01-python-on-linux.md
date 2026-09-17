# Lesson 1 — Python on Linux: Interpreters, venvs, pip and Pinning

> Module 27 · Unit 7 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 1 — environments](../labs/lab-01-environments.md)
> Up next: [Lesson 2 — Jupyter on Linux](02-jupyter-on-linux.md)

---

## 1. The interpreter — which Python is *the* Python?

On Ubuntu, Python is preinstalled — but *which* one answers
depends on `PATH` ([M15](../../../M15-environment-variables/README.md)):

```console
$ which -a python3
/usr/bin/python3
$ python3 --version
Python 3.12.3
$ ls /usr/bin/python3*         # the interpreter family the distro manages
```

Two concepts to separate:

- **System Python** — `/usr/bin/python3`, installed and *updated by
  the distro*. Ubuntu itself uses it: apt tools, cloud-init, system
  scripts. It belongs to the OS.
- **Your environments** — self-contained interpreter+packages
  trees, created per project. They borrow the system binary's
  *version* but own their *packages*.

The cardinal rule that follows — **never install packages into
system Python** — has two justifications. One is political: apt
manages `/usr/lib/python3/dist-packages`, and mixing pip-installed
versions on top breaks apt's assumptions (the "mixed apt/pip"
corruption, this module's classic troubleshooting patient). The
other is now *literal*: modern Debian/Ubuntu enforce **PEP 668** —
the system environment is marked "externally managed", and
`sudo pip install pandas` refuses with `error: externally-managed-environment`
([M16](../../../M16-package-management/content/README.md) §3 met the
message; here's its meaning: the OS is protecting itself). The
sanctioned paths: **venvs** (§2) or `pipx` for CLI tools — and the
`--break-system-packages` flag exists as the marked anti-pattern.

## 2. venv — the project's private Python

```console
$ mkdir -p ~/projects/sales-analysis && cd ~/projects/sales-analysis
$ python3 -m venv .venv                 # create the environment tree
$ source .venv/bin/activate             # enter it
(.venv) $ which python && which pip
/home/ds/projects/sales-analysis/.venv/bin/python
(.venv) $ python --version && pip list  # interpreter + packages, isolated
```

What `.venv` actually is, demystified: a directory tree containing
a `bin/` (symlinks to the system interpreter plus its own
pip/activation scripts), a `lib/python3.12/site-packages/` (where
pip installs *this project's* packages), and a `pyvenv.cfg`. It is
**not** a full Python copy — a few MB of plumbing over the system
interpreter.

**Activation is environment mutation**, exactly as
[M15](../../../M15-environment-variables/README.md) taught: the
`activate` script prepends `.venv/bin` to `PATH` and sets
`VIRTUAL_ENV` — so `python` and `pip` resolve *inside the tree*.
Deactivation (`deactivate`) restores the old `PATH`. The venv is
not "on" like a service; it's a PATH prefix that exists per-shell —
which is why every new terminal needs its own `source .venv/bin/activate`
(and why the [M19](../../../M19-scheduling-cron-timers/content/README.md)
lesson says scheduled jobs invoke `.venv/bin/python` *by absolute
path* — no activation, no PATH dependence).

Naming: `.venv` (dot-prefixed) is the de-facto standard — tools
look for it, and [M26's](../../../M26-git-dev-workflows/README.md)
`.gitignore` excludes it (environments are *rebuildable from
requirements*, never committed).

## 3. pip — the package workflow

```console
(.venv) $ python -m pip install pandas          # the recommended invocation
(.venv) $ pip list                              # what's installed here
(.venv) $ pip show pandas                       # version, location, deps
(.venv) $ pip install "pandas==2.2.3"           # exact version
(.venv) $ pip install "pandas>=2.1,<3"          # range
(.venv) $ pip install --upgrade pandas
(.venv) $ pip uninstall pandas
```

`python -m pip` beats bare `pip` for one reason: it guarantees the
pip bound to *that* interpreter — the cure for "pip installed into
the wrong place" (a PATH confusion this module's clinic
rehearses). Inside an activated venv the two are identical; the
idiom is armor.

**apt vs pip — the division of labor** from
[M16](../../../M16-package-management/content/README.md), now precise:

| Need | Source |
|---|---|
| Python interpreter itself | apt (`python3`, `python3-venv`, `python3-pip`) |
| System libraries with C deps | apt (`libpq-dev`, `python3-dev` when building) |
| Project Python packages | pip, *inside a venv* — always |
| CLI tools you want system-wide | `pipx` (its own venv per tool) |

The DS-specific wrinkle: heavy scientific wheels (`numpy`,
`pandas`, `scipy`) ship precompiled on PyPI — `pip install numpy`
downloads a binary wheel, no compiler needed. When pip *does* try
to build from source (sdist), the missing piece is usually an apt
library (`python3-dev`, `libpq-dev` for psycopg2) — read the error's
tail for the missing header, apt it, retry.

## 4. requirements.txt — the reproducibility contract

A DS result that can't be re-created is an anecdote. The
environment is part of the method, and `requirements.txt` is its
serializable form:

```console
(.venv) $ pip freeze > requirements.txt        # capture: exact versions
```

```text
# requirements.txt — the pinned contract
numpy==2.1.3
pandas==2.2.3
matplotlib==3.9.2
scikit-learn==1.5.2
```

```console
$ python3 -m venv .venv && source .venv/bin/activate
(.venv) $ pip install -r requirements.txt      # recreate: identical versions
(.venv) $ pip check                            # dependency sanity
```

Two disciplines around the contract: **freeze at milestones**
(working analysis → commit the freeze → [M26](../../../M26-git-dev-workflows/README.md)
commits it beside the code), and **recreate to verify** — Lab 1
builds the env a *second time* on a second account and imports
against both, because a `requirements.txt` that was never
reinstalled from is this module's version of the untested backup
([M24](../../../M24-logs-journald-monitoring/content/README.md)'s
rule, in environment form). `pip-tools`/`uv` and full lock files
are the professional next step — named for awareness; the freeze
pattern is the foundation they refine.

## 5. Python paths — where things resolve

The interpreter's search order, worth knowing when imports fail:

1. script's directory / current directory
2. `PYTHONPATH` entries (if set)
3. the venv's `site-packages` (when active)
4. system `dist-packages`

The practical corollaries: a file named `random.py` in your project
*shadows the stdlib* (a self-inflicted import bug); a stray
`PYTHONPATH` in `.bashrc` explains mysterious imports;
`python -c "import sys; print(sys.path)"` prints the actual order
when debugging. And `pip show <pkg>` prints its `Location:` —
system dist-packages appearing there is the mixed-install red
flag, caught early.

## 6. Try it now (20 minutes)

1. The refusal witness: `sudo pip3 install requests` → read the
   PEP 668 error verbatim. The system just taught Lesson 1 §1.
2. Build `.venv`, `pip install pandas`, then `pip show pandas` —
   the `Location:` proves isolation. `deactivate`, `pip list`
   again — system view, no pandas.
3. Freeze and inspect `requirements.txt` — note pip's *transitive*
   pins (every dependency, exact). That's what "reproducible" costs.
4. The PATH experiment: `deactivate`, then run
   `.venv/bin/python -c "import sys; print(sys.prefix)"` — the
   interpreter knows its venv without activation. This is the
   trick scheduled jobs and containers use.

## 7. Common mistakes

- `sudo pip install ...` — PEP 668 refusal at best, system
  breakage at worst; venv or pipx, always.
- Committing `.venv` to Git — thousands of files of rebuildable
  binary; commit `requirements.txt`, ignore the tree.
- Assuming activation persists — new shell, new SSH session,
  cron: none inherit it. Absolute venv paths for anything
  automated.
- Bare `pip` outside a venv with multiple Pythons — installs
  *somewhere else*; `python -m pip` pins the target.
- Editing `requirements.txt` by hand after installs drift — freeze
  regenerates it; hand edits lie.

> **Up next:** [Lesson 2 — Jupyter on
> Linux](02-jupyter-on-linux.md): the notebook server as a Linux
> service — headless, token-authenticated, reached through M22's
> tunnel.
