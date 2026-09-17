# Drill Card 2 — "Disk Full"

> Scenario family: System · Difficulty: ●●○
> Source modules: [M17](../../../M17-storage-and-filesystems/README.md), [M24 Clinic lesson 3](../../../M24-logs-journald-monitoring/content/performance/03-disk-io.md)

## Symptom

Writes fail ("No space left on device"), or a monitoring threshold
cries, or — the sneaky version — jobs start failing *randomly* because
temporary files can't be created.

## Decision tree

```text
df -h  →  which filesystem, how full?
├─ Use% ~100, space really gone      → WHO ate it? → du walk
├─ Use% fine but writes still fail   → df -i: inodes?
└─ df full but du sums much less     → deleted-but-open files
```

## Evidence

```console
$ df -h                    # the patient filesystem
$ df -i                    # the resource df -h lies about
$ sudo du -xh --max-depth=1 / 2>/dev/null | sort -rh | head    # descend from the root
$ sudo du -xh --max-depth=1 /home/ds | sort -rh | head         # then into the culprit dir
$ journalctl --disk-usage  # journald's own appetite (M24 §2)
```

## Fix pattern (by cause)

- **Giant datasets/outputs**: archive-then-delete (M24 Lesson 5: tar or
  rsync to the backup target *before* deleting; never delete the only
  copy).
- **Runaway logs**: truncate properly — `journalctl --vacuum-size=500M`
  for journald; for app logs, rotate (M24 lesson 2), don't `rm` the
  open file (deleted-open trap below).
- **Inode exhaustion**: find the small-file nest
  (`du --inodes -xh --max-depth=1`, GNU du) — sessions/, caches,
  `.ipynb_checkpoints` forests — and clear by directory.
- **Deleted-but-open**: identify the holder (`lsof +L1`, awareness),
  stop/restart *that* process, then the space returns. Restart-first
  wastes the diagnosis; stop-writer-first is the order.

## Verify

`df -h` (and `df -i`) show recovery — then prove the *original failure*
is gone: re-run the write that failed (`touch`, or the job's own temp
write). If the fix was cleanup-only, the canary is the threshold:
logcheck the growth source (`du -sh` on the culprit dir, weekly).

## Document

Template per the [methodology](../lessons/01-methodology.md#8-document).
Classic root causes to name precisely: *"no retention policy on
outputs/"*, *"log grew unbounded because no rotation"*, *"100% inodes
from checkpoints"* — each implies a different prevention.

**Done when:** you've run the three-way fork (space/inodes/deleted-open)
once on your own VM and can cite the command that discriminated it.
