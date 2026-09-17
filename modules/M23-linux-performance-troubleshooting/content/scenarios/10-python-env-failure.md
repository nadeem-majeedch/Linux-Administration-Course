# Drill Card 10 — "Python Environment Failure"

> Scenario family: Environment · Difficulty: ●●●
> Source modules: [M27](../../../M27-python-jupyter-data/README.md), [M27 troubleshooting](../../../M27-python-jupyter-data/content/troubleshooting.md)

## Symptom

`ModuleNotFoundError`, "works in my notebook, fails in the scheduled
job", pip installs succeeding into the void, an import working
yesterday and not today. The family trait: *the code is fine — the
interpreter isn't who you think it is.*

## Decision tree

```text
IN THE FAILING CONTEXT (same shell, same cron, same kernel):
python -c "import sys; print(sys.executable, sys.prefix)"
├─ not your .venv        → wrong interpreter (activation missing, cron PATH)
├─ your .venv, import fails → pip never landed there / version conflict → pip list
└─ inside notebook failing → which KERNEL? sys.executable in the cell (card 12 crossover)
```

## Evidence

The golden rule from M27: **diagnose in the failing context** — the
same terminal, the same crontab environment, the same notebook kernel.
The five-command sweep:

```console
$ python -c "import sys; print(sys.executable, sys.prefix)"
$ which -a python python3 pip           # every candidate on PATH
$ python -m pip --version               # pip belongs to WHICH interpreter?
$ python -m pip list | grep -i pandas   # is it actually THERE?
$ pip check                             # dependency conflicts, silent until now
```

For the scheduled-job flavor, the `env -i` rehearsal is the evidence
(M19/M27 Lab 3): `env -i HOME=$HOME PATH=/usr/bin:/bin /abs/path/script.sh`
— if it fails here and works interactively, the environment delta
*is* the bug.

## Fix pattern

- **Wrong interpreter** → activate properly, or better: call the venv
  python by absolute path (`~/proj/.venv/bin/python`) — the scheduled
  job's permanent cure.
- **Wrong pip** → `python -m pip install …` always; the `pip` on PATH
  belongs to someone else.
- **Version conflict** (`pip check` noisy) → recreate from the pin:
  `rm -rf .venv && python3 -m venv .venv && pip install -r
  requirements.txt` — venvs are disposable by design (M27); if
  requirements.txt doesn't reproduce it, the pin was the bug.
- **Kernel/venv mismatch** → re-register:
  `.venv/bin/python -m ipykernel install --user --name proj` (card 12
  takes the Jupyter side).

## Verify

The failing command succeeds **in its original context** — cron's
environment (via the `env -i` rehearsal), the notebook's kernel (a
fresh cell), the script's shebang path. "Works in my terminal" is the
diagnosis being ignored, not a verification.

## Document

Quote `sys.executable` before and after the fix. Vocabulary: *"cron
PATH resolution hit system python (no absolute path)"*, *"pip installed
to user site while venv active"*, *"requirements unpinned, resolver
drift"*. The prevention is nearly always the same sentence: absolute
interpreter paths and pinned files, everywhere.

**Done when:** you can stage the split-brain (install into system,
import from venv), discriminate it in ≤ 4 commands, and write the
one-line prevention.
