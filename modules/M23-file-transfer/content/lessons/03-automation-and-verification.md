# Lesson 3 — Automation & Verification: The DS Transfer Kit

> Module 23 · Unit 6 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 2 — transfer automation](../labs/lab-02-transfer-automation.md)
> Up next: [Quiz](../practice/quiz.md) · [Challenges](../practice/challenges.md)

---

## 1. From command to workflow

A one-off `rsync` is a command. A *transfer workflow* is a script
that is safe to run tired, at 2 a.m., after a failed experiment: it
verifies its inputs, fails loudly instead of silently half-copying,
keeps a log, and never deletes anything without a gate. Every piece
of that sentence is a skill you already own — [M10's
`set -euo pipefail`](../../../M10-bash-scripting/content/lessons/02-control-flow.md)
discipline, [M08's](../../../M08-text-processing/content/README.md)
log parsing, [M19's](../../../M19-scheduling-cron-timers/content/README.md)
"unverified backup is no backup" rule — now applied to bytes in
motion.

## 2. The skeleton: a sync script that won't betray you

```bash
#!/usr/bin/env bash
# sync-results.sh — push experiment results to the shared server, safely.
# Usage: sync-results.sh <results-dir> <user@host:dest>
set -euo pipefail          # M10 rules: fail loudly, no undefined variables

SRC="${1:?usage: sync-results.sh <results-dir> <user@host:dest>}"
DEST="${2:?usage: sync-results.sh <results-dir> <user@host:dest>}"
EXCLUDE=(--exclude='.venv/' --exclude='__pycache__/' --exclude='*.pyc')
LOG="$PWD/sync-$(date +%Y%m%d-%H%M%S).log"

log() { printf '[%s] %s\n' "$(date -Is)" "$*" | tee -a "$LOG"; }

log "REHEARSAL: $SRC -> $DEST"
rsync -avhn "${EXCLUDE[@]}" "$SRC/" "$DEST/" | tee -a "$LOG"

read -r -p "Apply the changes above? [y/N] " answer
[[ $answer == y ]] || { log "aborted by operator"; exit 1; }

log "APPLY"
rsync -avh "${EXCLUDE[@]}" "$SRC/" "$DEST/" | tee -a "$LOG"
log "done"
```

Three design decisions to internalize:

1. **Rehearse, then ask.** The dry-run (`-n`) output is shown to the
   human *before* anything moves; `read -r` makes "apply" an
   explicit act. Deleting the prompt is exactly what you'd do for a
   cron job (M17) — and then the excludes and the tested dry-run
   history become your safety net instead.
2. **Every run leaves a timestamped log.** `tee -a` gives you both
   live output and evidence. Three weeks later, "what exactly did
   the Friday sync change?" is a `grep` away.
3. **Fail loudly.** With `set -e`, a failed rsync (network drop,
   permission error) aborts the script with a nonzero exit instead
   of continuing on incomplete data — the failure you *see* at 2
   a.m. is the one you can fix.

## 3. Verification: did the bytes actually arrive?

rsync's default comparison is *size + modification time* — fast,
and right for syncing. But "synced" and "verified identical" are
different claims. Two escalation levels:

**Checksum-driven sync** — make rsync itself compare content
(slower: reads every byte on both sides):

```console
$ rsync -avhc --dry-run clean/ vm:~/data/clean/   # lists content differences only
```

**Manifest verification** — an independent, auditable check. Run
the same fingerprint command on both sides and diff:

```console
$ (cd clean && find . -type f -exec sha256sum {} +) | sort > local.sha256
$ ssh vm 'cd ~/data/clean && find . -type f -exec sha256sum {} +' | sort > remote.sha256
$ diff local.sha256 remote.sha256 && echo "VERIFIED IDENTICAL"
```

Keep `local.sha256` with your project: it is a *provenance record*
(M29's reproducibility chain) — proof of which exact bytes an
analysis consumed. For a 5 GB dataset the hash pass costs a minute;
for a publication it's worth an afternoon.

## 4. Reading the transfer log like data

A sync log is just another dataset — apply [M08](../../../M08-text-processing/content/README.md):

```console
$ grep -c '^sent' sync-*.log                 # how many completed syncs
$ grep -o 'speedup is [0-9.]*' sync-*.log    # efficiency over time
$ awk '/total size is/ {print $NF}' sync-*.log   # hmm — see below
```

The **stats line** is the headline number: `sent 12.35M bytes ...
total size is 36.83M speedup is 2.98`. A speedup that *drops* over
time means the source is churning (logs being rewritten, timestamps
touched) — the signal that your excludes need attention.

## 5. Large datasets: the practical playbook

| Situation | Tool choice | Why |
|---|---|---|
| One 5 GB file, flaky link | `rsync --partial --progress` | Resumes; `scp` restarts from zero. |
| Millions of small files | `tar` the tree, transfer one archive, untar on the far side | Per-file negotiation dominates; one stream wins. |
| Already-compressed data (`.gz`, Parquet, images) | drop `-z` | Compression passes are pure CPU waste on incompressible bytes. |
| Shared uplink, daytime | `--bwlimit=5m` (≈5 MiB/s) | Be a good citizen — your labmates' meetings matter. |
| Live-written log files | copy whole, never `--append-verify` | Appending during resume corrupts the file. |
| Massive tree, repeat syncs | `--exclude` aggressively (`.venv/`, `__pycache__/`, checkpoints) | Excluded noise is the #1 speedup killer. |

And the meta-rule from [M22](../../../M22-ssh-remote-admin/content/README.md):
automation runs on **keys, not passwords**. A scripted transfer
with no key auth either hangs forever waiting for a password prompt
that never comes, or — worse — tempts someone to embed a password
in the script. Batch mode makes the failure loud instead:

```console
$ rsync -e "ssh -o BatchMode=yes" -avh results/ vm:~/results/
```

If keys aren't set up, this errors immediately — exactly what you
want from unattended automation.

## 6. DS connection: the weekly loop

Pull the raw feed (`rsync` pull) → clean locally → push results
(`sync-results.sh`) → verify with a manifest → keep the log. That
loop, repeated, *is* data engineering on a Linux box — and every
stage maps to a course module: transfer (M23), cleaning (M08),
automation (M10), verification (M19), provenance (M29). The lab
asks you to run it end-to-end and produce the evidence.

## Self-check

- Why does the script dry-run *and* prompt, when `set -e` already
  guards failures? (What does `set -e` *not* protect against?)
- Your manifest `diff` reports one file differing but rsync said
  "up to date" — what comparison level did each use?
- Which is wrong for a log file being actively written: `--partial`,
  `--append-verify`, or `-z`? Why?
- What breaks first if a cron-driven rsync has no SSH key: the
  transfer, or the *trustworthiness* of the automation?

Up next: [Quiz](../practice/quiz.md) · [Challenges](../practice/challenges.md).
