# Lab — Run a Real CI Pipeline Locally (Container Runner, No Cloud)

> Extension C · DevOps on Linux · Time: ~75 min · Environment: your own VM (Docker from M28)
> ⚠️ The pipeline runs in a local container runner (`act`-class, executing
> GitHub Actions workflows via Docker). No GitHub account, no cloud, no paid
> services. The workflow file is *unchanged* from what GitHub Actions would run.

## Part A — the repository, DevOps-shaped (15 min)

Assemble the pipeline's subject — a repo that holds *everything the
service needs* (lesson 1 §2):

```console
$ mkdir -p ~/devops-lab/{scripts,tests,.github/workflows} && cd ~/devops-lab
$ printf 'pandas==2.2.3\npytest==8.3.3\n' > requirements.txt
$ cat > analysis.py <<'EOF'
"""Regional revenue summary — the smallest real analysis."""
import pandas as pd

def summarize(csv_path: str):
    df = pd.read_csv(csv_path)
    return df.groupby("region")["revenue"].sum().sort_values(ascending=False)
EOF
$ printf 'region,revenue\nnorth,1200\nsouth,850\nnorth,300\n' > data.csv
$ cat > tests/test_analysis.py <<'EOF'
from analysis import summarize

def test_north_leads():
    s = summarize("data.csv")
    assert s.idxmax() == "north"
    assert s["north"] == 1500
EOF
$ cat > scripts/smoke.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail                       # M11 strict mode
python -c "from analysis import summarize; summarize('data.csv'); print('smoke ok')"
EOF
$ chmod +x scripts/smoke.sh
$ git init && git add -A && git commit -m "Analysis, tests, and the pipeline's subject"   # M26
```

## Part B — the workflow file (20 min)

`.github/workflows/ci.yaml` — lesson 2's, tuned to this repo:

```yaml
name: ds-analysis CI
on: [push, workflow_dispatch]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip                     # M27's cache lesson, CI edition

      - run: pip install -r requirements.txt

      - name: shellcheck the scripts     # M10's bar
        run: shellcheck scripts/*.sh

      - name: run tests
        run: pytest -v

      - name: smoke test
        run: ./scripts/smoke.sh
```

Install the local runner (container-based — M28's engine running the
robot):

```console
$ curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash
$ act --version
```

(If your distribution packages `act` or an equivalent local Actions
runner, prefer that — the lesson is the workflow, not the installer.)

## Part C — run the robot (20 min)

```console
$ act workflow_dispatch -P ubuntu-latest=catthehacker/ubuntu:act-latest
[Test ds-analysis CI/test   ] ⭐ Run tests
  …
  ✅  Success - Main run tests
[Test ds-analysis CI/smoke  ] ⭐ Smoke test
  smoke ok
```

Read the output as the course's history replayed by a robot: checkout
(the repo *is* the subject), pinned Python + `requirements.txt` (M27),
shellcheck (M10's bar enforced), pytest (the tests you wrote *as*
tests), smoke (M23-clinic's verify, mini).

**The drift-proof demonstration** — the lab's core lesson:

```console
$ pip3 install --user flask==3.0.3        # pollute YOUR environment deliberately
$ python3 -c "import flask; print('host has flask')"      # it does
$ act workflow_dispatch -P …              # the runner: same result as before
```

The pipeline's verdict didn't move: the fresh container has no flask,
no leftovers, no memory — *only the manifest*. Write the two-sentence
observation in `lab-log.md` (lesson 2 §2's point, witnessed).

Then the failure drill: break `test_analysis.py`'s assertion, commit
("break the gate"), run `act` — red pipeline, and the *build you'd
never ship* never ran. Fix, commit ("green again"), re-run. The gate
is real because it's mechanical.

## Part D — the deploy job, rehearsed (15 min)

Add the deploy job from lesson 2 §4 — pointed at *your* VM's user unit
(the M29 core service):

```yaml
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: smoke via runner               # the verify-before-deploy
        run: |
          pip install -r requirements.txt
          ./scripts/smoke.sh
      - name: "Deploy (rehearsal: prints the commands it WOULD run)"
        run: |
          echo "ssh ds@vm 'cd ~/projects/ds-capstone && git pull'"
          echo "ssh ds@vm 'systemctl --user restart myapi'"
          echo "ssh ds@vm 'curl -fsS http://127.0.0.1:8000/health'"
```

Run it with `act -j deploy workflow_dispatch …`. The rehearsal-print
form (M11's dry-run discipline) makes the deployment *reviewable
text* — when you wire a real host, the echo-strip is the only change.
Write the CD three questions (lesson 2 §4) answered for this exact
pipeline in your journal.

## Done when

- [ ] Workflow file versioned in the repo; all three jobs' logs in
      `lab-log.md`
- [ ] Drift-proof demonstration recorded (polluted host, unchanged
      pipeline verdict)
- [ ] Failure drill: red gate blocked the nonexistent build; green
      restored
- [ ] Deploy job rehearsed in echo-form; the three CD questions
      answered
- [ ] One paragraph: what this pipeline automates *from your own
      course habits* — name four modules it robotizes

**Stretch:** add a `schedule:` trigger (M19's cron, repo edition) that
runs the smoke test nightly — and one `if:` guard that skips deploy on
non-main branches. Two lines of YAML; the concepts are the lesson.
