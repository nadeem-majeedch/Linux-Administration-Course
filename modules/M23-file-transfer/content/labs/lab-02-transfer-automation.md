# Lab 2 — Transfer Automation: The Weekly Loop, Scripted

> Module 23 · Unit 6 · Difficulty: Intermediate
> Time: ~45 min · Environment: **your own VM, loopback only**
> Prerequisites: [Lab 1](lab-01-dataset-sync-circuit.md) complete,
> [Lesson 3](../lessons/03-automation-and-verification.md),
> [M10](../../../M10-bash-scripting/content/README.md) (functions,
> `set -euo pipefail`), [M19](../../../M19-scheduling-cron-timers/content/README.md)
> (verification mindset)
> Evidence transcript: `script m23-lab2.log`

## The mission

Turn Lesson 3's skeleton into a working, logged, verifying transfer
tool — then use it as a real DS weekly loop: **pull → clean → push →
verify → log**. Every run must leave evidence a teammate could audit.

## Setup (3 min)

```console
$ mkdir -p ~/m23lab2/{server,project/{raw,clean}} && cd ~/m23lab2/project
$ python3 - <<'PY'
import csv, random
random.seed(7)
with open("raw/feed.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["ts","sensor","value"])
    for r in range(20000):
        v=random.gauss(20,3)
        w.writerow([f"2026-09-16T{r//3600:02d}:{r//60%60:02d}:{r%60:02d}",
                    f"S{r%10}", "ERR" if r%997==0 else round(v,2)])
PY
```

We will treat `~/m23lab2/server/` as the *shared server* (via
`localhost`) and `project/` as your workstation.

## Part A — build `sync-results.sh` (15 min)

Write `~/m23lab2/project/sync-results.sh` from Lesson 3's skeleton,
then make it executable and run it against the fake server:

```console
$ chmod u+x sync-results.sh
$ ./sync-results.sh clean/ localhost:~/m23lab2/server/results/
```

Required behavior (each is a checkpoint when demonstrated):

1. **Guards:** missing argument → usage message, exit 1 (test with
   `./sync-results.sh` alone). `set -euo pipefail` at the top.
2. **Rehearsal first:** a `--dry-run` whose output is shown before
   the apply prompt; answering anything but `y` aborts cleanly with
   exit 1.
3. **Excludes:** `--exclude` for `.venv/` and `__pycache__/`; prove
   it works by creating `clean/__pycache__/junk.pyc` and confirming
   the dry-run does *not* list it.
4. **Timestamped log:** every run appends to a `sync-YYYYmmdd-HHMMSS.log`
   via `tee -a`; the log contains both the rehearsal and the apply.

## Part B — the weekly loop, end to end (15 min)

```console
# 1. PULL the raw feed from the "server"
$ rsync -avh localhost:~/m23lab2/server/feeds/ raw/ 2>/dev/null || \
  echo "no feeds dir yet — create one first (see below)"
```

Create the server side (`mkdir -p ~/m23lab2/server/feeds` and copy
`raw/feed.csv` there), then pull properly. Continue:

```console
# 2. CLEAN locally (M08 pipeline — errors out of scope, in scope here)
$ grep -v ',ERR$' raw/feed.csv | awk -F, 'NR==1 || $3+0==0 || $3+0' \
    | awk -F, 'NR==1{print;next} {print}' > clean/feed_cleaned.csv
$ wc -l raw/feed.csv clean/feed_cleaned.csv   # record both counts

# 3. PUSH via your script
$ ./sync-results.sh clean/ localhost:~/m23lab2/server/results/

# 4. VERIFY with an independent manifest (Lesson 3 §3)
$ (cd clean && find . -type f -not -path '*/__pycache__/*' \
     -exec sha256sum {} +) | sort > local.sha256
$ ssh localhost 'cd ~/m23lab2/server/results && find . -type f \
     -exec sha256sum {} +' | sort > remote.sha256
$ diff local.sha256 remote.sha256 && echo "VERIFIED IDENTICAL"
```

**Checkpoint:** paste the "VERIFIED IDENTICAL" line and both line
counts into the transcript. One sentence: why is the sha256 diff a
*stronger* claim than rsync's "up to date"?

## Part C — break it, observe it, explain it (12 min)

1. **Change on the server side only.** Append one line to the
   remote copy: `echo "2026-09-16T23:59:59,S99,19.5" | ssh localhost
   'cat >> ~/m23lab2/server/results/feed_cleaned.csv'`. Re-verify:
   the manifest diff now *fails* — read the exact diff line. Then
   re-push and re-verify to green.
2. **Speedup drift.** Touch every file in `clean/`
   (`touch clean/*.csv`), push, and read the stats line: speedup
   collapses toward 1.0. One sentence: what does this predict about
   a project whose build rewrites timestamps nightly?
3. **Batch mode honesty check.** Temporarily rename your localhost
   key? — **No.** Instead simulate a headless failure safely:
   `rsync -e "ssh -o BatchMode=yes" -avh clean/ localhost:~/tmp-batch/`
   should succeed (key auth active). Now point it at a host that
   requires a password (if none available, skip) and note that
   BatchMode fails *immediately and loudly* instead of hanging.

**Checkpoint:** three transcript lines, one per observation, each
with the "why" in your own words.

## Teardown (2 min, scoped)

```console
$ cd ~ && rm -rf ~/m23lab2 && ls ~/m23lab2 2>&1   # confirm gone
```

## Deliverables

1. `sync-results.sh` (working, guarded, logged)
2. `m23-lab2.log` with all checkpoints answered inline
3. The successful `VERIFIED IDENTICAL` manifest diff
4. One sample `sync-*.log` with rehearsal + apply sections
