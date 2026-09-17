# Lesson 2 — CI/CD Concepts, and GitHub Actions as the Exemplar

> Extension C · DevOps on Linux · Difficulty: Advanced
> Reading time: ~30 min · Lab: [Local CI](lab-01-local-ci.md)
> Teaching mode: GitHub Actions as the *pattern* — the workflow you write here
> runs locally in a container runner, and unchanged on GitHub if you later use it.

---

## 1. CI, CD, and the robot's job description

**Continuous Integration (CI)**: every push to the repo triggers an
automated *build-and-verify* — code compiles, tests pass, lint is
clean. The value is mathematical: integration problems surface in
minutes on a robot instead of weeks in a human's debugging session.

**Continuous Delivery/Deployment (CD)**: the verified artifact proceeds
*automatically* to deployment — delivery = packaged and ready (a human
presses the button), deployment = the button presses itself. The
spectrum is a risk dial; the discipline is the same.

What the robot actually buys you, in course vocabulary:

| Robot behavior | The course habit it automates |
|---|---|
| Runs tests on every commit | M10/M11's shellcheck + self-testing scripts |
| Builds from pinned contracts | M27 freeze / M28 Dockerfile |
| Fails loudly, logs everything | M24's evidence contract |
| Verifies before reporting success | M32-clinic's verify-the-original-symptom |
| Refuses to deploy unverified change | the blast-radius sentence, made mechanical |

The mental model to keep: **the pipeline is your runbook's
verification section, executed by software, on every commit.**

## 2. Anatomy of a pipeline

Pipelines are trees of work with two structural concepts:

```text
  push/PR event
       │
  ┌────▼─────┐
  │ workflow │  (the file in your repo: .github/workflows/ci.yaml)
  └────┬─────┘
   ┌───┴────┐
   │  jobs  │  (units of work; each runs on a fresh runner)
   └───┬────┘
   ┌───┴────────────┐
   │ steps (shared  │  (commands/actions within a job, run in order)
   │ run env)       │
   └────────────────┘
```

- **Events** trigger workflows: `push`, `pull_request`, `schedule`
  (M19's cron, repo edition), `workflow_dispatch` (manual button).
- **Jobs** run in parallel by default on fresh environments (isolation:
  no "it worked because of last week's leftovers" — drift is
  structurally impossible on a fresh runner).
- **Steps** are shell (your M10 skills) or *actions* (reusable
  packaged steps). `needs:` builds dependencies between jobs — the
  test job gates the build job gates the deploy job.
- **Artifacts & caching** — jobs are ephemeral; anything one job
  produces for another must be *declared* (an artifact), and slow
  steps (dependency installs — M27/M28's cache lessons) get cache
  declarations. Same lessons, CI vocabulary.

The runner itself: a Linux machine (often a container) that checks out
your repo and executes the steps — Extension A's "server", Extension
B's "instance", rented per job and destroyed after. Ephemeral
infrastructure is the CI superpower: **every run starts from the
manifest, so drift can't accumulate.**

## 3. GitHub Actions: reading and writing a workflow

GitHub Actions is the de-facto pattern; its file format is worth
learning precisely because it *is* the pattern (GitLab CI, CircleCI,
Jenkins differ in syntax, not in concepts). A workflow that runs this
course's actual checks:

```yaml
# .github/workflows/ci.yaml
name: ds-analysis CI

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:          # the manual button (for the lab)

jobs:
  test:
    runs-on: ubuntu-latest    # the runner: Linux, fresh, ephemeral
    steps:
      - uses: actions/checkout@v4          # action: check out the repo

      - name: Set up pinned Python         # M27, automated
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install pinned environment   # the requirements contract
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Shellcheck the scripts       # M10's bar, enforced
        run: shellcheck scripts/*.sh

      - name: Run tests                    # the checklist
        run: pytest tests/ -v

      - name: Smoke-import the analysis    # M32-clinic verify, mini
        run: python -c "import analysis; print('import ok')"

  build:
    needs: test                             # the gate: no test, no build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build image from pinned base  # M28, digest-pinnable
        run: docker build -t ds-analysis:${{ github.sha }} .
      # (no push in this course — the image tag proves the build)
```

Read the file against the course: `runs-on` is the ephemeral runner
(§2), `uses` pulls reusable actions, `run:` is M10's shell, `needs:`
is the gating that makes CD safe, and `${{ github.sha }}` tags the
image by *commit* — the traceability rule: **every artifact points
back to the exact code that built it** (M26's hash discipline, at
deploy scale).

Secrets appear as `${{ secrets.NAME }}` — stored in the platform's
vault, injected as env at runtime, masked in logs. The M25 §5 rules
with a mechanical enforcement: the platform *refuses* to print them.

## 4. CD: from green build to running service

The deploy job is Extension A's provisioning, triggered by a green
build. The minimal honest pattern for this course:

```yaml
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to my VM over SSH          # M22, scripted
        run: |
          ssh ds@vm "cd ~/projects/ds-capstone && git pull"
          ssh ds@vm "systemctl --user restart myapi"
          ssh ds@vm "curl -fsS http://127.0.0.1:8000/health"   # the verify step
```

Every CD discussion is a variation on three questions — keep them and
any tool becomes learnable:

1. **How does the artifact travel?** (git pull on the host = rebuild
   from source; image push/pull = M28's registry; both are fine at
   this scale.)
2. **How is the swap made safe?** (restart with `--user` scope; the
   zero-downtime pattern is M29's reload-vs-restart; blue-green =
   run the new one beside the old, flip, keep the old for rollback.)
3. **Who verifies?** (the pipeline's final smoke test — health
   endpoint or nothing; "it deployed" is not "it works", the M29 core
   lesson.)

**Rollback is a first-class stage**, not an apology: deploy N+1 with
the knowledge that N is one `git revert` + redeploy away (lesson 1 §2).
A pipeline that can't roll back hasn't finished being written.

---

## Key takeaways

- CI = every push verified by a fresh, ephemeral runner; CD = the
  verified artifact flows to deploy with a *human or automatic* gate —
  the risk dial is yours to set.
- Workflow anatomy: **events → jobs (parallel, ephemeral) → steps
  (shell/actions)**, with `needs:` gating and artifacts bridging jobs.
- The runner is drift-proof *by construction* — every run from the
  manifest, nothing inherited.
- CD = artifact travel + safe swap + **verification**, and rollback is
  a designed stage; `${{ secrets.* }}` is M25 §5, mechanically
  enforced.

## Check yourself

1. Why does a fresh runner per job eliminate the "worked because of
   last week" bug class — and what replaces the machine state a
   long-lived server would have had?
2. In the workflow, what makes the build job *gated* — and what would
   you add before a real deploy job?
3. Why tag the image with `github.sha` rather than `latest`?
4. Name the three CD questions and answer them for "restart a user
   unit on my VM".
5. A deploy succeeded but the health endpoint 503s. Which pipeline
   stage *should* have caught it, and what does its absence mean
   about the pipeline's design?

*Answers:* (1) Ephemeral runners share nothing between runs, so
nothing can be "left over"; the manifest (pinned deps, image) *is* the
machine state — M27/M28's reproducibility as architecture. (2) `needs:
test` gates it; before a real deploy: the smoke test step (health
endpoint), and rollback tooling (the revert-and-redeploy path
documented in the runbook). (3) The SHA ties the artifact to the exact
commit that built it — traceability/rollback anchoring; `latest` is
the mutable-tag sin (M28 lesson 1 §4) at deploy scale. (4) Travel =
git pull on the host (rebuild from source); swap = `systemctl --user
restart` (M29's restart, with reload as the zero-downtime variant);
verify = the health endpoint curl as a pipeline step. (5) The deploy
job's smoke-test step; its absence means the pipeline verifies
*deployment mechanics* but not *service correctness* — it is CI with
a delivery habit, not CD.

Up next: [IaC and deployment patterns](03-iac-and-deployment.md) —
Terraform, and where the containers fit.
