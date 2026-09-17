# Drill Card 11 — "Package Installation Failure"

> Scenario family: Environment · Difficulty: ●●○
> Source modules: [M16](../../../M16-package-management/README.md), [M27 lesson 1](../../../M27-python-jupyter-data/content/lessons/01-python-on-linux.md)

## Symptom

`apt install` or `pip install` refuses: lock errors, unmet
dependencies, 404s, "externally managed environment", build failures
on native wheels. Two package worlds, two decision trees — same
method.

## Decision tree — apt

```text
sudo apt install X fails:
├─ 'Unable to locate package'   → apt update? universe repo? name right?
├─ 'broken packages' / unmet deps → apt --fix-broken / check held pins
├─ dpkg lock / 'is another process using it' → is an apt REALLY running?
└─ 404 / hash sum mismatch     → stale index → apt update first
```

## Decision tree — pip

```text
pip install X fails:
├─ 'externally-managed-environment' → you're in SYSTEM python (M27's guard) → venv!
├─ 'No matching distribution'      → wrong index/typo/python version (X.Y support?)
├─ build fails (gcc, headers)      → native wheel missing → slim base needs build-essential (M28 §5)
└─ resolution conflict             → pip check; pin deliberately, don't fight blindly
```

## Evidence

```console
# apt family
$ sudo apt update && sudo apt install -y <pkg>   # refresh FIRST — 404s are usually this
$ apt-cache policy <pkg>                          # which version, from WHERE, candidates
$ sudo apt --fix-broken install                   # the dependency repair path

# pip family (in the venv!)
$ python -m pip install -v <pkg> 2>&1 | tail -20  # -v: the actual failing step
$ python -m pip check                             # what conflicts, named
$ python --version && python -m pip show <pkg>    # interpreter version vs package needs
```

The discipline that matters most: **read the last 20 lines, not the
first error** — both tools bury the real cause under a preamble
("Solving environment…" noise, apt's "try --fix-mce"). The `-v` on pip
and the untruncated apt output are the evidence; a screenshot of the
first red line is not.

## Fix pattern

- **Stale index/metadata** → `apt update` (or pip `--upgrade pip`
  within the venv) — the boring cause that wins most races.
- **Externally-managed** → *the system working as designed* (PEP 668):
  the fix is the venv, not `--break-system-packages`. That flag
  appears in this course's materials exactly zero times, on purpose.
- **Native build failure** → the slim-base lesson (M28): system libs
  (`build-essential`, `libpq-dev`) via apt, *then* pip; or prefer the
  prebuilt wheel by matching the Python version.
- **Broken deps (apt)** → `apt --fix-broken install`, then
  `apt-cache policy` to see what *held* the old version; document the
  held package if one exists.

## Verify

`apt-cache policy <pkg>` / `pip show <pkg>` — installed, from the
expected source, at the expected version — then **the consumer works**:
the tool runs, the import lands (card 10's sweep), the service starts.
"Install succeeded" is one layer short of verified.

## Document

Quote the discriminating line from the verbose output. Vocabulary:
*"system-python install attempted (PEP 668)"*, *"native wheel absent
for Python 3.13, built from source without libpq-dev"*, *"stale apt
index after image snapshot"*. Preventions: always-venv, base-image
deps in the Dockerfile, refresh before install.

**Done when:** you've reproduced one apt-class and one pip-class
failure deliberately, and can name the discriminating command for
each from memory.
