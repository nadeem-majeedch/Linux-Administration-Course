# The Six Backup Exercises — Scheduled Cleanup to Disaster Rehearsal

> Module 24 · Unit 6 · Companion to
> [Lesson 5 — backups & recovery deep dive](../lessons/05-backups-recovery-deep-dive.md)
> and [Lab 4](lab-04-backup-test-restore.md)
> ⚠️ **Everything targets `~/lab24/` test directories.** No real
> system directories, no destructive operations outside the lab's
> own scratch — every deletion is narrated, guarded, and reversible
> by re-creating the test data.

Six exercises, one per capability. Each ends with evidence in
`lab-log.md`; together they discharge the course's central
admission: **a backup that has never been restored/tested is not
assumed reliable** — these make yours tested.

## Setup — the lab estate (5 min)

```console
$ mkdir -p ~/lab24/{estate/{datasets,experiments,configs},backups/{daily,weekly},scratch}
$ head -c 2M /dev/urandom > ~/lab24/estate/datasets/panel_v1.bin
$ printf 'epoch,loss\n1,0.69\n2,0.58\n' > ~/lab24/estate/experiments/run42.csv
$ printf 'PATH=/usr/local/bin:/usr/bin:/bin\n' > ~/lab24/estate/configs/pipeline.conf
```

Three asset classes (data, results, config) — the inventory of
[Lesson 5 §2.1](../lessons/05-backups-recovery-deep-dive.md),
concrete.

## Exercise 1 — scheduled data cleanup (the retention side)

Extend M19 C3's `cleanup.sh` to the estate: `@daily` (crontab)
removal of `~/lab24/estate/scratch/**` files older than 7 days —
dry-run first, allowlist-guarded, narrated. Prove: create
`touch -d '9 days ago' ~/lab24/estate/scratch/old.tmp`, force the
run (`systemctl --user start` or cron two-minute rule), confirm
the narrated removal *and* that nothing outside scratch was
touched (checksum the estate before/after).

**Why this is a backup exercise:** retention and rotation are
backup's mirror — the same `find -mtime`/age logic, the same
deletion risks, the same need for guards.

## Exercise 2 — the dataset backup (incremental-shaped snapshots)

Implement [Lesson 5 §3's](../lessons/05-backups-recovery-deep-dive.md)
`--link-dest` snapshotter as `snapshot.sh` (strict mode, log
contract, `--dry-run`):

```bash
rsync -a --delete --link-dest="$BACKUPS/latest" \
      "$HOME/lab24/estate/" "$BACKUPS/$(date +%F)/"
```

Run it three times, mutating one file between runs; verify with
`ls -li` that unchanged files share inodes across snapshots and
`du -sh backups/*` shows the incremental *storage* cost of a
full-*looking* snapshot. Then `tar -czf` the latest snapshot —
the archive for offsite (Exercise 4).

## Exercise 3 — the experiment backup (the work product)

Experiments are small, precious, and change *constantly* — the
high-frequency, high-value case. Write `exp-sync.sh`: `rsync -avP
~/lab24/estate/experiments/ → ~/lab24/backups/experiments/`
**plus** an append-only log (`run42.csv` → checksummed entries:
timestamp, file, sha256). Schedule it hourly (two-minute rule
first). The deliverable: an evidence trail — "at 14:00, run42.csv
had sha X" — which is *provenance*, the DS-grade upgrade of
backup.

## Exercise 4 — the configuration backup + offsite simulation

Configs are tiny and utterly load-bearing. Back up
`~/lab24/estate/configs/` **plus** the admin's real dotfiles
(`~/.bashrc`, `~/.ssh/config` — *public* halves only, the
[M25](../../../M25-security-firewall/content/README.md) secrets rule
enforced: grep the tarball's listing for anything key-shaped
before shipping). Then the offsite simulation: `rsync` the
resulting tarballs to a *second* directory simulating a remote
host (`~/lab24/offsite/`), record the command that would do it
for real (`rsync -avP ... remote-host:backups/` — M23), and note
the 3-2-1 mapping in one line per copy.

## Exercise 5 — restore the deleted dataset (the drill that matters)

The central rehearsal, performed honestly:

1. **Delete:** `rm ~/lab24/estate/datasets/panel_v1.bin` — gone.
2. **Panic protocol** (written before acting): do not touch
   anything; restore to scratch per
   [Lesson 5 §7](../lessons/05-backups-recovery-deep-dive.md)'s
   runbook.
3. **Restore:** locate the latest snapshot (Exercise 2's dated
   dirs), `rsync -av backups/$(latest)/datasets/ ~/lab24/scratch/restore/`
   — *to scratch, never over*.
4. **Verify:** `sha256sum` the restored file against Exercise 3's
   evidence log (or Lab 4's checksum habit).
5. **Promote:** move the restored file into the estate; log the
   incident M24-style (five lines: symptom, cause, the command
   that saved it, fix, prevention).

**The grading question:** how long did the restore take, end to
end? That number is your RTO — write it down; it's now a metric
you own.

## Exercise 6 — verify backup integrity (the scheduled habit)

Automate the verification grade: `verify-backup.sh` re-computes
checksums of the latest archive against its `.sha256`, tar-lists
it (`-tzf | wc -l` — file-count sanity), and writes a PASS/FAIL
line to a verification log. Schedule it *weekly* (two-minute rule
first). Then the corruption drill: flip one byte in a copy of an
archive (`printf 'x' | dd of=copy.tar.gz bs=1 seek=100 conv=notrunc`),
run the verifier against the copy — the FAIL line is the control
working. Delete the corrupt copy; the real archive passes.

**The close:** your `lab-log.md` now holds the chain — backups
made (E2–4), restore drilled (E5), verification scheduled (E6),
retention guarded (E1). The untested-backup rule is discharged
*by schedule*, not by this one afternoon.

## Done when

- [ ] E1: cleanup scheduled, narrated removal proven, estate
      untouched (checksums match)
- [ ] E2: inode-sharing witnessed (`ls -li`), storage cost recorded
- [ ] E3: provenance log shows hourly entries with sha256
- [ ] E4: offsite mapping written (3 copies / 2 media / 1 simulated
      offsite)
- [ ] E5: the deleted dataset restored to scratch, verified,
      promoted — **RTO timed and recorded**
- [ ] E6: verifier scheduled; corrupt-copy FAIL witnessed
- [ ] One paragraph: which exercise changed how much you *trust*
      your backups, and why
