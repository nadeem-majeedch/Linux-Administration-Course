# Lab 4 — Backups and the Test-Restore

> Module 24 · Unit 6 · Difficulty: Advanced
> Time: ~50 min · Environment: your own VM
> Prerequisites: [Lesson 4](../lessons/04-incident-methodology.md) (the
> 3-2-1 rule), M17's loopback/virtual-disk skills, M23's rsync basics
> ⚠️ Backs up **only `~/lab24/precious/`** — files created in this
> lab. No system files, no whole-disk images, no `rm -rf` beyond the
> lab's own scratch directory.

The lesson this lab teaches the hard way: **a backup that has never
been restored is a hope, not a backup.** You will make two kinds of
backup (archive + mirror), damage the original, and recover —
*proving* the recovery with checksums.

## Setup — the "irreplaceable" data (5 min)

```console
$ mkdir -p ~/lab24/precious/{datasets,results}
$ head -c 5M /dev/urandom > ~/lab24/precious/datasets/panel.bin
$ printf 'epoch,loss\n1,0.69\n2,0.58\n3,0.51\n' > ~/lab24/precious/results/run1.csv
$ echo "lab notebook v1" > ~/lab24/precious/NOTES.md
$ find ~/lab24/precious -type f | wc -l          # remember: 3 files
$ du -sh ~/lab24/precious
```

The 3-2-1 rule (Lesson 4): **3** copies, **2** different media, **1**
offsite. Your lab can't do real offsite, so: original (copy 1, home
fs), archive on a second *virtual* disk (copy 2, different medium),
and the "offsite" role played by a directory on the *other* filesystem
— with the mapping to real 3-2-1 written into the lab log.

## Part A — the archive: tar + checksum (10 min)

```console
$ mkdir -p ~/lab24/backups
$ tar -czf ~/lab24/backups/precious-$(date +%F).tar.gz -C ~/lab24 precious
$ tar -tzf ~/lab24/backups/precious-*.tar.gz          # LIST before trusting
$ sha256sum ~/lab24/backups/precious-*.tar.gz | tee ~/lab24/backups/precious.sha256
```

`tar -t` (test-list) before trust, `sha256sum` as the integrity
receipt — this pair is muscle memory for every archive you'll ever
ship to a collaborator. Record the checksum in `lab-log.md`.

## Part B — the mirror: rsync to a second virtual disk (15 min)

The M17 skill returns: a loopback file, formatted, mounted *in user
space terms* via sudo, used as "different medium".

```console
$ dd if=/dev/zero of=~/lab24/disk2.img bs=1M count=256 status=none
$ sudo mkfs.ext4 -F ~/lab24/disk2.img                 # -F: it's a file, we're sure
$ mkdir -p ~/lab24/mnt && sudo mount -o loop ~/lab24/disk2.img ~/lab24/mnt
$ sudo chown $USER: ~/lab24/mnt                       # your user owns the mount root
$ df -h ~/lab24/mnt | tail -1                          # new filesystem, 251M
```

The mirror — with the flags that make rsync a *backup* tool:

```console
$ rsync -av --delete ~/lab24/precious/ ~/lab24/mnt/mirror/
$ ls -laR ~/lab24/mnt/mirror | head -20
```

Why each flag: `-a` = archive (recursive, perms, times), `-v` =
narrated (transcript goes to the lab log), `--delete` = the mirror is
*exact* — deletions propagate. **The --delete warning from M23 bears
repeating:** it makes the destination match the source *including
removals* — correct for backups, catastrophic as a "copy" habit. The
trailing-slash semantics (`precious/` vs `precious`) decide
copy-into vs copy-as; note which you used.

## Part C — the disaster (5 min)

A realistic one — not `rm -rf ~`, but the *wrong file overwritten*:

```console
$ printf 'CORRUPTED\n' > ~/lab24/precious/results/run1.csv
$ rm ~/lab24/precious/datasets/panel.bin
$ find ~/lab24/precious -type f | wc -l              # now 2 files
```

Verify the mirror's `--delete` behavior — an important truth about
mirrors:

```console
$ rsync -av --delete ~/lab24/precious/ ~/lab24/mnt/mirror/ | tail -5
$ ls ~/lab24/mnt/mirror/datasets/                    # panel.bin gone there too!
```

**Write before fixing:** one sentence on why a mirror with `--delete`
is *not* version history — and what that implies (archives! Part A's
tar is the history; the mirror is the live second copy).

## Part D — the test-restore (10 min)

**From the mirror** (fast path, last state):

```console
$ rsync -av ~/lab24/mnt/mirror/ ~/lab24/restore-mirror/
```

Hmm — `run1.csv` restores corrupted, `panel.bin` stays gone. That's
the mirror's honest limitation. **From the archive** (point-in-time):

```console
$ mkdir -p ~/lab24/restore-archive
$ tar -xzf ~/lab24/backups/precious-*.tar.gz -C ~/lab24/restore-archive
$ sha256sum -c ~/lab24/backups/precious.sha256       # fails? why: path differs — see below
```

The checksum file references the *original backup path*. Verify
content instead, then reconcile:

```console
$ diff -r ~/lab24/precious ~/lab24/restore-archive/precious && echo "IDENTICAL"
$ find ~/lab24/restore-archive/precious -type f | wc -l    # 3 again
```

**Fix the original from the restore**, then re-mirror:

```console
$ rm -rf ~/lab24/precious && cp -a ~/lab24/restore-archive/precious ~/lab24/
$ rsync -av --delete ~/lab24/precious/ ~/lab24/mnt/mirror/ | tail -3
$ diff -r ~/lab24/precious ~/lab24/mnt/mirror && echo "MIRROR OK"
```

## Part E — teardown and the rule (5 min)

```console
$ sudo umount ~/lab24/mnt
$ rm ~/lab24/disk2.img
$ df -h ~ | tail -1                                  # disk space back
```

Keep `~/lab24/backups/` (the tar + checksum) — the next lab's
mini-project builds on the pattern. Then answer in `lab-log.md`:

1. Which copy saved `panel.bin`, and why couldn't the other?
2. Your lab's 3-2-1 mapping: what played "offsite", and what would
   the real version be? (Think: M23's rsync over SSH to another host.)
3. The restore you just did took 30 seconds for 5 MB. Write the
   scheduling reality: when would you *rehearse* this for a 500 GB
   dataset, and how often?

## Done when

- [ ] Part A checksum recorded; Part B rsync transcript in log
- [ ] Part C's one-sentence --delete insight written *before* Part D
- [ ] Both restores verified (diff exit 0 lines in transcript)
- [ ] Part E's three questions answered
- [ ] Virtual disk unmounted and removed; `df -h ~` back to baseline
