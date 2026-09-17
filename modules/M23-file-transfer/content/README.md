# Module 23 Content — File Transfer & Synchronization

> Unit 6 · Difficulty: Intermediate · ~5 hours total
> Companion modules: [M22 — SSH](../../M22-ssh-remote-admin/content/README.md)
> (connectivity & keys) · [M19 — Backups](../../M19-scheduling-cron-timers/content/README.md)
> (verification discipline) · [M10 — Bash scripting](../../M10-bash-scripting/content/README.md)
> (the automation toolkit)

## Learning objectives

By the end of this module you can:

1. **Select** the right transfer tool — `scp`, `sftp`, or `rsync` —
   for a given workload, justifying the choice by file count,
   connection stability, and repetition.
2. **Execute** push and pull transfers in both directions with
   correct flags for ports, recursion, compression, and resume.
3. **Predict** rsync's behavior from its trailing-slash and
   comparison semantics (size+mtime vs `--checksum`) before running.
4. **Gate** any destructive sync (`--delete`) behind a read dry-run,
   archived rehearsal, and non-destructive backups.
5. **Automate** a transfer workflow: guarded script, timestamped
   logs, key-only authentication with `BatchMode=yes`.
6. **Verify** transfers with independent sha256 manifests and read
   sync logs (`speedup`, bytes sent) as data.
7. **Apply** the full transfer loop to a Data Science weekly cycle:
   pull raw → clean → push results → verify → keep provenance.

## Contents

### Lessons — read in order

| # | Lesson | Focus |
|---|--------|-------|
| 1 | [The Transfer Toolbox](lessons/01-transfer-toolbox.md) | scp/sftp/rsync selection; scp precision; sftp sessions; permissions on arrival |
| 2 | [rsync Fundamentals](lessons/02-rsync-fundamentals.md) | `-avh` grammar; the slash trap; `--delete` discipline; resume & `--partial` |
| 3 | [Automation & Verification](lessons/03-automation-and-verification.md) | the guarded sync script; sha256 manifests; large-dataset playbook; the DS weekly loop |

### Practice

| Resource | Purpose |
|---|---|
| [Lab 1 — Dataset Sync Circuit](labs/lab-01-dataset-sync-circuit.md) | loopback scp/sftp/rsync drills; measure, resume, explain |
| [Lab 2 — Transfer Automation](labs/lab-02-transfer-automation.md) | build the guarded script; run the weekly loop; break-and-observe |
| [Quiz](practice/quiz.md) | 20 scenario questions · [Answer key](practice/quiz-answers.md) (instructor) |
| [Challenges](practice/challenges.md) | ★★–★★★: delete-proof sync, speedup forensics, reproducibility pack |
| [Troubleshooting](troubleshooting.md) | 8 transfer symptoms → causes → fixes |

## Data Science connections

- **Datasets on the move:** pulling raw feeds, pushing cleaned
  outputs, syncing experiment folders to compute servers.
- **Reproducibility:** sha256 manifests = provable input provenance
  (M19 × M29).
- **Remote GPU servers:** resume-capable transfers for 5 GB+
  checkpoints; `--bwlimit` as lab citizenship.
- **Automation:** the same script pattern backs cron-driven dataset
  pipelines (M17) and Docker image/data staging (M28).

## Prerequisites

- [M22](../../M22-ssh-remote-admin/content/README.md) —
  working key-based SSH (Lab 1 depends on it)
- [M10](../../M10-bash-scripting/content/README.md) — script guards,
  `set -euo pipefail`
- [M19](../../M19-scheduling-cron-timers/content/README.md) — verification
  mindset (reciprocal: this module applies it to bytes in motion)

## Where this leads

The capstone (M30) requires a dataset ingest + results egress
pipeline with evidence; the DS server module (M31) assumes these
transfer skills as fluency, not novelty.
