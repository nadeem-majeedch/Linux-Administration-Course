# Lesson 3 — Data, Experiments, and Reproducibility

> M31 · Unit 8 companion · Difficulty: Advanced
> Reading time: ~30 min · Up next: [The 13 scenarios](04-scenario-walkthrough.md)
> Prerequisites: M13 (shared access), M24 lesson 5 (backups), M26 (Git), M28 (Docker)

---

## 1. Datasets: the read-only commons

The lesson-1 directory contract's most rule-bound corner is `/data` —
and its rules are all M13/M27 permissions grown into research policy:

- **Shared datasets are read-only by permission, not by convention** —
  group-owned with SGID (`chgrp lab /data/projects/x; chmod 2750`),
  mode bits enforcing what the README asks nicely (M27 Q18). The 2
  a.m. `to_csv("data/raw/…")` fails, exactly as designed.
- **Raw is immutable; derived is per-project** — the provenance
  pattern from M26 Lab 3: `data/raw/` never changes (a checksum
  manifest — `sha256sum … > SHA256SUMS` — is the immutability
  *proof*), while `data/processed/` is rebuilt by scripts from raw.
  If processed can't be regenerated from raw + code, the pipeline
  has a bug, not a data problem.
- **You don't copy shared data into `$HOME`** — you *reference* it (a
  symlink or an absolute path in config). Duplication on a shared box
  is quota debt plus divergence risk: two "copies" of the dataset that
  silently differ. The config points at the commons; the commons
  guarantees the version (that's what the checksum manifest is *for*).
- **Large transfers land with integrity** — M23-file-transfer's
  `rsync -av --checksum` discipline (or `wget -c` + checksum verify)
  for anything bigger than a notebook; the download isn't done until
  `sha256sum -c SHA256SUMS` passes.

## 2. The experiment directory: your project's second tree

Code lives in `$HOME/proj/`; the *work* the code produces lives in a
deliberate experiment tree — M27's project layout, promoted to the
server with run-awareness:

```text
~/proj/                      the CODE (git — small, text, versioned)
├── src/, notebooks/, requirements.txt, README.md
~/proj-runs/                 the WORK (never git — large, regenerable)
└── 2026-09-20_lr0.001/      one directory per run: date + the knob you turned
    ├── config.yaml          the EXACT configuration of this run (copied at launch)
    ├── logs/                train.log (tee'd), journal excerpts
    ├── checkpoints/         resume-able states (truncate-then-rename)
    ├── metrics.csv          epoch rows — the quantitative heartbeat
    └── model/               the artifact(s): model.pt, feature spec, metadata
```

Two rules make the tree trustworthy:

1. **The run directory is written by the run** — the launcher script
   creates it (timestamp + key hyperparameters in the name), stamps
   `config.yaml` (resolved config, git SHA of the code, dataset
   checksum), and everything else lands inside. A results directory
   assembled by hand is a results directory you can't trust.
2. **`metrics.csv` is the contract** — append-only epoch rows; it is
   what you *plot* to decide things, and its existence (with the
   config) is what makes a run *comparable* to the next one. This is
   MLflow/W&B's idea in raw filesystem form — and recognizing that is
   the point: the tools automate the tree, the tree is the discipline.

Model files get their own hygiene (M24's artifact thinking): name with
the run directory they came from, store the *metadata next to the
weights* (architecture, dataset checksum, git SHA, training-window),
and treat them like M26 treats binaries — too big for git, small
enough for backups, documented well enough to be loadable six months
later.

## 3. Logs: your experiments are production systems

Everything M24 taught about services applies to your runs, scaled down
to one process: the job logs unconditionally (`tee`), the log has a
**structure** (epoch, loss, lr, timestamp — parseable lines, not
prose), and the **three-element evidence bundle** (M27 Q20) is the
minimum claim that a run *happened*: the log line, the output
artifact (metrics.csv / checkpoint), and the resource trace (the
pre-flight + monitoring snapshot). The end-of-run line is written
*by the job* (`[2026-09-20T17:12] DONE best_epoch=7 val_loss=0.214`)
— the fail-loudly contract (M27 Lab 3 §D) means a run without a DONE
line is a run that didn't finish, whatever the notebooks claim.

## 4. Backups: what gets saved, what doesn't, and the proof

The M24 Lesson 5 rules, applied to the DS server's shapes:

| Content | Backup? | Why |
|---|---|---|
| `$HOME` code (git-pushed) | the *push* is the backup | off-site by definition (M26 remotes) |
| run directories — configs, metrics, logs | yes — small, irreplaceable context | the *story* of the work |
| checkpoints | latest only (working state) | resumability, not history |
| model artifacts | yes (they're the deliverable) | weeks of compute live here |
| `/scratch` intermediates | **no** | ephemeral by design — that's why they live there |
| shared `/data` | the *admins'* job (verify it exists) | commons, not yours |

The runbook (Extension A lesson 3) carries the schedule; the
**untested-restore rule** closes it: a backup of run directories that
has never been restored is a rumor — the drill (restore into a
scratch tree, checksum, run the eval script against the restored
model) is scheduled, timed, and logged like any other backup.

## 5. Reproducibility: the chain that proves the work

The module's culminating claim — reproducibility is not a tool, it's
a **chain of pinned artifacts**, each link from this course:

```text
  code        = git commit SHA            (M26 — the hash IS the version)
  environment = requirements.txt pins     (M27 — or conda env / Docker image SHA)
  data        = raw dataset checksum      (SHA256SUMS — the immutable commons)
  config      = config.yaml in the run dir (resolved, stamped)
  run         = the directory itself      (logs + metrics + checkpoints + model)
  proof       = fresh clone + fresh env + checksummed data → same numbers
```

**Docker as the strong form** (M28): the image pins code *and*
environment *and* system libraries into one digest — `FROM
python:3.12-slim` + `requirements.txt` + code, tagged by SHA, becomes
the runnable citation of the work. When a result must survive a
reviewer's "I can't reproduce this," the image is the answer; the
run-directory chain is the answer when containers aren't in play.

The chain's test is the one M27 Lab 1 made famous, scaled up: a
**fresh clone on a fresh environment** re-runs the analysis and
reaches the same numbers. The capstone's whole grading philosophy —
*reliable and reproducible beats impressive and mysterious* — is this
chain, held end to end.

---

## Key takeaways

- `/data` is a **permissioned commons**: read-only raw with checksum
  provenance, referenced (not copied) by projects, transferred with
  verified integrity.
- The **experiment directory** is written by the run — config stamped
  at launch, `metrics.csv` the contract, checkpoints resumable, models
  documented beside their weights.
- Logs make runs *provable* (the three-element bundle; a run without
  a DONE line didn't finish); backups split by content class, with
  the untested-restore rule applied to run directories.
- **Reproducibility is a chain of pins** — code SHA, env pins, data
  checksum, stamped config — tested by fresh-clone-plus-fresh-env;
  Docker is its strongest form.

## Check yourself

1. Why reference shared data rather than copying it into `$HOME`?
   Name the two costs of copying.
2. What makes a run directory trustworthy, compared to a folder of
   results assembled by hand?
3. Your best model is `model_final_REALLY.pt` in `$HOME`. In this
   module's terms, list the four things missing before it's a
   citable artifact.
4. The reviewer asks for a rerun. Compose the reproducibility chain
   for one of your runs — the six links, each naming its artifact.

*Answers:* (1) Quota debt (`$HOME` is quota'd and backed up — a
duplicated 50 GB dataset wrecks both) and divergence risk (two copies
silently differ; the checksummed commons guarantees one version).
(2) It was written by the run: the launcher created it, stamped
resolved config + git SHA + dataset checksum, and the artifacts
(metrics, checkpoints) are append-only outputs — provenance by
construction, not by memory. (3) The stamped config (what produced
it), the code SHA (which code), the dataset checksum (which data),
the metrics/log trail (that it *did*), and a name that means
something — `model_final_REALLY` is none of those things. (4) Code:
`git show <sha>`; environment: `requirements.txt` (or image SHA);
data: `SHA256SUMS` verification; config: the run dir's stamped
`config.yaml`; run: the directory (logs, metrics, checkpoints);
proof: fresh clone + fresh env re-run reaching the same `metrics.csv`
conclusion.

Up next: [The 13 scenarios](04-scenario-walkthrough.md) — the whole
course as one first week.
