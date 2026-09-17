# Lesson 2 — rsync Fundamentals: The Sync Engine

> Module 23 · Unit 6 · Difficulty: Intermediate
> Reading time: ~30 min · Lab: [Lab 1, Part C](../labs/lab-01-dataset-sync-circuit.md)
> Up next: [Lesson 3 — automation & the DS transfer kit](03-automation-and-verification.md)

---

## 1. What "sync" actually means

`scp` answers: *how do I move this?* `rsync` answers: *what must
change so that destination matches source?* — a fundamentally
smarter question. rsync compares the two sides (size + mtime by
default, checksums on request), then transfers only the difference.

```console
$ rsync -avh --progress raw/ vm:~/data/raw/
sending incremental file list
sensor_2026-08-31.csv
         12.34M 100%   28.41MB/s    0:00:00 (xfr#1, to-chk=1/3)
sent 12.35M bytes  received 35 bytes  4.94M bytes/sec
total size is 36.83M  speedup is 2.98
```

Read that last line like a DS result: `speedup is 2.98` means rsync
moved roughly a third of the naive copy. On a week-long experiment
folder, that's the difference between minutes and hours.

## 2. The flag grammar: `-avh --progress` decoded

| Flag | Meaning | DS consequence |
|---|---|---|
| `-a` | **archive**: recursive + preserves permissions, timestamps, symlinks (equivalent to `-rlptgoD`) | The default for real work — a synced experiment tree stays a faithful copy. |
| `-v` | verbose: name what transferred | Your evidence trail. |
| `-h` | human-readable sizes (12.34M not 12939431) | Readable logs. |
| `--progress` | per-file progress | Tames the 5 GB transfer. |
| `-z` | compress in flight | Big win for text (CSV/logs); waste for already-compressed data (`.gz`, images, Parquet). |
| `-n` | **dry run: report, transfer nothing** | Non-negotiable before any consequential sync. |
| `--exclude=...` | skip patterns (`--exclude='*.tmp'`) | Keeps virtualenvs/checkpoints out of the sync. |

`-a` preserves *permissions and ownership attributes*, but note:
remote ownership can only be preserved by root (`-o`/`-g` are
root-only). Normal-user syncs preserve modes and times — exactly
what M13 taught you to expect.

## 3. The trailing slash: rsync's famous trap

With a source ending in **`/`** rsync copies the *contents*. Without
it, rsync copies the *directory itself*:

```console
$ rsync -a raw/ vm:~/data/raw/       # contents land IN data/raw/
$ rsync -a raw  vm:~/data/raw/       # creates data/raw/raw/ ← almost never wanted
```

Same trap locally: `rsync -a src/ dst/` (merge) vs `rsync -a src
dst/` (nest). This course's rule: **decide the destination shape
first, then choose the slash deliberately** — and rehearse with
`--dry-run`, which prints exactly where files would land.

## 4. `--delete`: the sharpest tool in the kit

```console
$ rsync -avh --delete clean/ vm:~/data/clean/   # mirror semantics
```

`--delete` removes destination files that no longer exist at the
source — true mirroring, and the single most dangerous flag in the
transfer toolbox. Its dangers compound when combined with `--exclude`:
deleted-and-excluded is ambiguous without `--delete-excluded`, and
"deleted at source" can mean "I deleted my work". So the course rule:

> **`--delete` only ever follows a clean `--dry-run` you actually
> read.** Belt-and-braces: keep the output, or use
> `--backup --backup-dir=...` so removals land in a holding folder
> instead of oblivion (M19 recovery thinking, applied at transfer).

Also know the direction discipline: `--delete` makes **source the
authority** — pushing with `--delete` enforces your laptop's view on
the server; *pulling* with `--delete` enforces the server's view on
your laptop. Both are legitimate; only one matches your intent.
Decide which side is the master *before* typing the command.

## 5. Interrupted transfers: resume, don't restart

Kill a 5 GB `scp` at 90% and you restart from zero. rsync is built
for bad connections: interrupted files restart where they left off
(the temp file survives), and `--partial` keeps the incomplete piece
to resume from next run.

```console
$ rsync -avh --partial --progress big.parquet vm:~/data/
```

`--append-verify` can resume even mid-file on stable data; it is
**not** safe on files being written concurrently — a live log
appended while you sync will corrupt. Rule: *resume completed data
(snapshots, exports); copy live files whole.*

## 6. The three questions before every real transfer

1. **Direction & authority** — push or pull? Who is the master copy?
2. **Scope** — full tree or subset? (`--exclude` everything you
   don't need: `.venv/`, `__pycache__/`, `checkpoints/`)
3. **Deletion semantics** — should destination deletions happen at
   all? If yes: dry-run, read it, then execute.

A DS team that answers these three consistently stops experiencing
"sync accidents". The lab makes you answer them in writing, every
time — that habit is the assessed skill.

## Self-check

- What exactly does `-a` expand to, and which parts need root on the
  far side?
- `rsync -a src dst/` vs `rsync -a src/ dst/` — where do files land?
- Why is `--delete` + `--exclude` a dangerous combination, and what
  two safeguards tame it?
- Why is `--append-verify` wrong for a log file being written?

Up next: [Lesson 3 — automation & the DS transfer kit](03-automation-and-verification.md).
