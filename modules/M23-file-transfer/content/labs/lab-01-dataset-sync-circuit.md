# Lab 1 — The Dataset Sync Circuit

> Module 23 · Unit 6 · Difficulty: Intermediate
> Time: ~50 min · Environment: **your own VM, loopback only** — this
> lab talks to `localhost` over SSH, so it is safe, repeatable, and
> impossible to aim at the wrong machine by accident.
> Prerequisites: [M22 Lab 1](../../../M22-ssh-remote-admin/content/labs/lab-01-key-workflow.md)
> (key-based login must work), [Lesson 1](../lessons/01-transfer-toolbox.md),
> [Lesson 2](../lessons/02-rsync-fundamentals.md)
> Start an evidence transcript: `script m23-lab1.log`

## Why loopback

"Remote" practice normally needs a second machine. Your VM already
*is* one: `ssh localhost` exercises the full sshd → scp/rsync stack
with zero risk of touching anyone else's system. Everything here
lives under `~/m23lab/` — created by you, deletable at the end
(safely, M08-style).

## Setup (5 min) — generate a realistic dataset

```console
$ sudo apt-get install -y rsync          # Ubuntu: may say "already newest"
$ mkdir -p ~/m23lab && cd ~/m23lab
$ python3 - <<'PY'
import os, random, csv
random.seed(42)
os.makedirs("raw", exist_ok=True)
for d in range(3):
    with open(f"raw/sensor_2026-09-{10+d:02d}.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["ts","sensor","value"])
        for r in range(5000):
            w.writerow([f"2026-09-{10+d:02d}T{r//3600:02d}:{r//60%60:02d}:{r%60:02d}",
                        f"S{r%12:02d}", round(random.gauss(20,3),2)])
print("created:", sorted(os.listdir("raw")))
PY
$ du -sh raw/ && find raw -type f | wc -l
```

Record the byte total — it is your baseline for Part C.

## Part A — scp precision drill (10 min)

1. `mkdir -p stage && scp raw/sensor_2026-09-10.csv stage/`
2. Add the port flag variant: `scp -P 22 raw/sensor_2026-09-11.csv localhost:stage/`
   — confirm it succeeds; then run `scp -p 22 ...` and **read the
   error carefully** before rerunning with the right case.
3. Recursive: `scp -r raw localhost:~/m23lab/scp-copy/`
4. Verify identity independently:
   `diff -r raw scp-copy && echo "IDENTICAL"` — then delete nothing
   yet; note `scp -r`'s behavior if `scp-copy/` already existed
   (run step 3 again and `diff` once more).

**Checkpoint:** explain in one comment line in your transcript why
`-p 22` failed (exact flag semantics).

## Part B — sftp session (10 min)

1. `sftp localhost`, then, in one session: `pwd`, `lpwd`, `cd m23lab`,
   `lcd ~/m23lab`, `get raw/sensor_2026-09-12.csv pulled.csv`,
   `put pulled.csv uploaded-via-sftp.csv`, `ls -l`, `bye`.
2. `sha256sum raw/sensor_2026-09-12.csv uploaded-via-sftp.csv` —
   hashes must match.

**Checkpoint:** which two `sftp` commands mapped to which `scp`
invocations from Part A?

## Part C — rsync: measure, then believe (15 min)

1. First sync: `rsync -avh --progress raw/ localhost:~/m23lab/rsync-copy/`
   — record the **total size is / speedup** line.
2. Immediate re-run — record the *new* stats line. It should report
   **0 transferred bytes**; write down why (size+mtime comparison).
3. Now touch one file (`touch raw/sensor_2026-09-10.csv`) and re-sync:
   only that file moves. Explain in one line what changed that
   rsync noticed (hint: `stat` from M06).
4. **The slash experiment** (dry-run first, always):
   ```console
   $ rsync -avhn raw  localhost:~/m23lab/slash-test/    # no trailing slash
   $ rsync -avhn raw/ localhost:~/m23lab/slash-test/    # with slash
   ```
   Compare the two destination paths in the output. Write the rule
   in your own words in the transcript.

**Checkpoint:** paste both speedup lines next to each other and one
sentence: what does `speedup is` mean when it's absent entirely?

## Part D — interrupt and resume (10 min)

1. Generate a big file: `head -c 200M /dev/urandom > raw/big.parquet`
2. Start `rsync -avh --partial --progress raw/ localhost:~/m23lab/rsync-copy/`
   and **press Ctrl-C after ~5 seconds**.
3. Confirm the partial file exists remotely (via `ssh localhost du -sh
   ~/m23lab/rsync-copy/big.parquet`) and is smaller than the original.
4. Re-run the identical command to completion. Total bytes moved in
   run 2 ≪ 200M — that is resumption, not a full retry.

**Checkpoint:** record both the interrupted and completed transfer
lines. What would `scp` have done instead?

## Part E — the `--delete` demonstration (sacrificial directory)

Roadmap contract: see `--delete` do its real work on a directory
that exists to be sacrificed — with dry-run evidence first.

```console
$ mkdir -p sacrificial && cp raw/sensor_2026-09-10.csv sacrificial/
$ touch sacrificial/obsolete.txt
$ rsync -avh --delete --dry-run raw/ sacrificial/   # READ this output
```

The dry-run lists `obsolete.txt` under *deleting*. Confirm the file
still exists (`ls sacrificial/obsolete.txt`), then run the identical
command without `--dry-run` and confirm the deletion. Nothing of
value was at risk — but you just executed the full discipline:
**rehearse → read → verify intent → apply**.

**Checkpoint:** paste the dry-run's deleting line and the pre- and
post-`ls` evidence.

## Teardown (2 min, deliberate and scoped)

```console
$ cd ~ && rm -rf ~/m23lab        # you created every byte under this path
$ ls ~/m23lab 2>&1               # confirm: "No such file or directory"
```

Only ever `rm -rf` on a path you created this session and just
printed. Exit the transcript (`exit`), keep `m23-lab1.log`.

## Deliverables

1. `m23-lab1.log` with the five checkpoints answered inline
2. Both stats lines (fresh sync vs no-op sync)
3. The slash rule, in your own words
4. Resume evidence: interrupted vs completed totals
