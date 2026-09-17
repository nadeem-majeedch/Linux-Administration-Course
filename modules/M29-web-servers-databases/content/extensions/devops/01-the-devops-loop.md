# Lesson 1 — The DevOps Loop: Linux's Role and Git as Truth

> Extension C · DevOps on Linux · Difficulty: Advanced
> Reading time: ~25 min · Up next: [CI/CD concepts](02-ci-cd-concepts.md)

---

## 1. The wall, and the loop

Traditional delivery had a wall: *developers* produce code, *operators*
run it — and the handoff is where velocity and reliability die (the
famous "works on my machine" is a wall artifact). **DevOps** merges
the two roles and automates the path between them:

```text
  write ──► commit ──► [pipeline: test, lint, build] ──► deploy ──► operate
    ▲                                                                    │
    └────────────────── feedback: logs, metrics, incidents ◄──────────────┘
```

Linux's role is not a footnote — it is the substrate. Every stage of
that loop is Linux work you already own: commits are Git (M26), tests
and builds run in shells (M10/M11) inside containers (M28), deployment
is systemd units and config discipline (M20/M29), operation is logs
and monitoring (M24) and the incident method (M23-clinic). The pipeline
itself is a Linux process (a runner) executing your checklist with
robotic patience.

**The cultural core, stated as the course has taught it:** automate
the repeatable (M11), make evidence the deliverable (M24/M23-clinic),
and treat every artifact — code, environment, config, infrastructure —
as versioned text.

## 2. Git as the single source of truth

In a DevOps shop, the repository is the *species* of everything that
runs — not just code:

```text
repo/
├── analysis/            # code (M26/M27)
├── requirements.txt     # environment contract (M27)
├── Dockerfile           # environment as artifact (M28)
├── compose.yaml         # the stack (M28)
├── .github/workflows/   # the pipeline definition (this extension)
├── infra/               # IaC manifests (this extension, lesson 3)
├── runbook.md           # operations truth (Extension A)
└── .gitignore           # the hygiene line (M26 lesson 3)
```

Two properties make Git *the* substrate:

- **The commit is the unit of change** — and by extension, the unit of
  deployment and (when needed) the unit of *rollback*: revert the
  commit, redeploy. M26's "commit early, commit small" becomes an
  operational property, not just tidy history.
- **Review happens at the diff** — the M26 feature-branch workflow is
  where a second pair of eyes meets every change *before* it runs:
  policy (Extension A lesson 2) enforced by the merge, not by memory.

The discipline that follows: **if it isn't in the repo, it doesn't
exist** — hand-edited server configs are Extension A's *drift*, and
the pipeline is the scheduled convergence that absorbs them.

## 3. Environments and secrets in the loop

The pipeline multiplies the environments your code meets — dev, test,
staging, prod — and the course's reproducibility rule becomes an
architectural requirement:

- **The environment is built, not found.** Every run starts from the
  pinned contract: `pip install -r requirements.txt` (M27) or the
  Docker image (M28). "It worked on the runner last week" is drift
  (Extension A lesson 2) — the fix is the same: pin, rebuild,
  converge.
- **Configuration flows in; secrets are injected.** The M25 §5/M28
  rules, pipeline edition: config via environment variables *declared*
  per environment; secrets via the pipeline's secret store injected as
  env/files at runtime — *never* in the repo, never in logs. A secret
  that reached a log line is burned (rotate), exactly as in M26's
  clinic patient.
- **Parity**: dev, test, and prod differ by configuration, not by
  construction — same image, different env. The "works in dev" bug
  class dies when construction is identical (M28's pinned base made
  this possible).

## 4. Operate feeds back: the loop closes

The right half of the loop — operate, feed back — is where DS work
lives: logs tell you the job ran (M24's three-element evidence),
monitoring tells you it *should* run differently, and the incident
method (M23-clinic) converts failures into prevention. Two DevOps
habits institutionalize that feedback:

- **Every deploy is observable** — health endpoints (M29), structured
  logs, the health kit (M24): the pipeline's last stage is a
  *verification* (smoke test), not a shrug.
- **Every incident changes the repo** — the drill-card postmortem ends
  with a prevention *committed*: a test, a canary, a threshold. The
  loop's feedback is a pull request, not a lesson learned in someone's
  head.

---

## Key takeaways

- DevOps = merged roles + **automated path from commit to operate**;
  Linux is the substrate at every stage, and you've already practiced
  each stage's skills.
- **The repo is the species of everything that runs** — code,
  environment, pipeline definition, infrastructure, runbook — and the
  commit is the unit of change, deploy, and rollback.
- Environments are *built from pinned contracts* per run; **secrets
  are injected, never stored, never logged** — M25's rules at
  pipeline speed.
- The loop closes when operations feed back as *commits* —
  prevention becomes a pull request.

## Check yourself

1. Name the wall DevOps removes, and the two cultural rules that
   replace it.
2. Why does "commit early, commit small" (M26) become an *operational*
   property in DevOps, not just a history preference?
3. A pipeline run succeeds on Monday and fails on Tuesday with no code
   change. Name the most likely mechanism and its fix — in this
   course's vocabulary.
4. Where do pipeline secrets live, and what is the procedure when one
   appears in a log line?

*Answers:* (1) The dev/ops handoff wall; replaced by merged
responsibility and *automation of the path between them* —
everything-as-versioned-text, executed by the pipeline. (2) Because
the commit becomes the unit of deployment and rollback — small commits
make reverts surgical and bisectable failures; big commits make
rollback a redesign. (3) Drift — an unpinned dependency resolved
differently (or a base image moved); fix: pin to exact versions/digests
and rebuild (M27's freeze + M28's digest pinning, lesson 1 §4). (4) In
the pipeline's secret store, injected as env/files at runtime; when
one reaches a log: treat as burned — rotate/revoke first (M26 Lab 2
patient 2), then fix the leak's mechanism.

Up next: [CI/CD concepts](02-ci-cd-concepts.md) — the robot that runs
the checklist.
