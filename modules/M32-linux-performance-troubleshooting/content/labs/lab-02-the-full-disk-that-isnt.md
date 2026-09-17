# Drill Book — Incident 2: The Full Disk That Isn't

> Setup time: 8 min · Solve time: ~25 min
> Cards: [2 — Disk full](../scenarios/02-disk-full.md)
> Safety: this incident uses a **loopback virtual disk you create**
> (M17's safe playground). No system filesystem is touched.

## Setup

```bash
#!/usr/bin/env bash
# setup-incident-2.sh — a 60 MB loopback FS with a hidden space thief
set -euo pipefail
mkdir -p ~/drill2 && cd ~/drill2

# the virtual disk (M17 Lab pattern)
dd if=/dev/zero of=disk.img bs=1M count=60 status=none
mkfs.ext4 -q disk.img
mkdir -p mnt
sudo mount -o loop disk.img mnt
sudo chown $USER: mnt

# 20 MB of legitimate data (the du-visible part)
head -c 20M /dev/urandom > mnt/dataset.bin

# THE BREAK: 35 MB written, then "deleted" — while a holder keeps it open
head -c 35M /dev/urandom > mnt/big.log
tail -f mnt/big.log > /dev/null 2>&1 &      # the holder
echo $! > holder.pid
rm mnt/big.log                               # deleted... from the namespace only

df -h mnt | tail -1                          # the "full" disk
echo "Incident 2 staged. Mount: ~/drill2/mnt"
```

## The symptom

```console
$ cp ~/projects/ds-capstone/data/raw/sales.csv ~/drill2/mnt/
cp: cannot create … : No space left on device
```

**Your incident brief:** "The analysis disk refuses writes. Someone
said it's full; the cleanup team says it's half-empty. It's blocking
tonight's batch."

## Solving notes (for the grader in you)

- `du` vs `df` disagreeing *is* the fingerprint — card 2's third fork.
  The teaching point: `df` counts the block device; `du` walks names.
  A deleted-but-open file has the former's blocks and none of the
  latter's names.
- The read-only evidence path: `df -h ~/drill2/mnt`, `du -sh
  ~/drill2/mnt`, then the discriminator — `lsof +L1 ~/drill2/mnt`
  (awareness level; may need sudo on some systems) or the
  `/proc/*/fd` hunt for links marked `(deleted)`.
- The safe test that *confirms* before any kill: `echo x >
  ~/drill2/mnt/probe` fails (reproduces); after stopping the holder,
  the same probe succeeds (establishes causality — C15's logic).
- The undo is structural: `kill $(cat holder.pid)`, verify `df` recovers,
  and the fix conversation is about *log rotation* (M24 lesson 2) — the
  prevention sentence writes itself: "apps that append forever need
  rotate+truncate, not delete".
- Cleanup when done: `kill` the holder, `sudo umount ~/drill2/mnt`,
  `rm -rf ~/drill2` — it's your loopback toy, and saying so in the
  journal is part of the blast-radius discipline.

**Done when:** `df` shows recovery, the original `cp` succeeds, and
the eight-step block explains the deleted-open mechanism with the
before/after `df` pair.

Next: [Incident 3 — the unresolvable host](lab-03-the-unresolvable-host.md)
