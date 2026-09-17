# Demo 9 — Storage & Backups: The Loopback Lifecycle

> **Session:** S16 · **Duration:** ~15 min · **Risk: MEDIUM — contains
> real `mkfs`; safe *only* because the device is a loopback file. A
> recording fallback exists; use it if the room's state is wrong.** ·
> **Objective:** the complete block-device lifecycle — create, format,
> mount, use, persist via fstab, verify a restore — with the four-line
> rule recited at the dangerous moment.

## The four-line rule, recited on stage

| Line | This demo |
|---|---|
| **Purpose** | `mkfs` creates filesystems — how every disk becomes usable |
| **Risk** | it formats the *named device*, destroying its contents, permanently |
| **Safe environment** | the device today is a **100 MB loopback file** — a file pretending to be a disk; your real disks are untouched |
| **Recovery** | delete the loopback file and start over — the *real-disk* version has no recovery, which is the lesson |

## Prerequisites

- Demo VM, snapshot `pre-loopback` taken
- Root-capable sudo (staged drop-in or password)
- **Recording fallback ready** (see [demo index](../demo-index.md))

## Setup (before class)

```console
$ truncate -s 100M ~/demolab-disk.img
$ sudo losetup -f --show ~/demolab-disk.img        # → /dev/loop0 (name varies)
$ sudo apt-get install -y parted >/dev/null        # if absent
```

## Procedure

**Step 1 — the device exists.**

```console
$ losetup -l
$ sudo parted /dev/loop0 --script mklabel msdos mkpart primary ext4 1MiB 100%
$ lsblk /dev/loop0
```

*Narration:* "`lsblk` now shows a partition *inside a file*. From here
down, every command believes it's talking to a disk."

**Step 2 — the dangerous moment (recite the rule, then run).**

```console
$ sudo mkfs.ext4 /dev/loop0p1
```

*Narration:* "Read the output: inodes, block groups, UUID. A
filesystem was born — on 100 megabytes of *file*. On a real disk, this
command is the catastrophe; the object defines the risk."

**Step 3 — mount and use.**

```console
$ sudo mkdir -p /mnt/demo-data
$ sudo mount /dev/loop0p1 /mnt/demo-data
$ echo "demo dataset" | sudo tee /mnt/demo-data/readme.txt
$ df -h /mnt/demo-data | tail -1
```

**Step 4 — persistence: the fstab entry.**

```console
$ sudo blkid /dev/loop0p1        # get the UUID
$ echo 'UUID=<the-uuid> /mnt/demo-data ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab
$ sudo umount /mnt/demo-data && sudo mount -a && ls /mnt/demo-data
```

*Narration:* field by field — device, mountpoint, type, options
(`nofail`: a missing disk must not block boot), dump (legacy, 0), pass
(2: fsck order, root is 1).

**Step 5 — the backup-and-restore proof (M19's rule, planted).**

```console
$ sudo cp /mnt/demo-data/readme.txt ~/readme.backup
$ echo "changed while in use" | sudo tee /mnt/demo-data/readme.txt
$ sudo cp ~/readme.backup /mnt/demo-data/readme.txt && cat /mnt/demo-data/readme.txt
demo dataset
```

*Narration:* "A copy that was *restored and verified* — that's a
backup. The nightly dump nobody has ever restored is a rumor. The
capstone grades the restore, not the copy."

**Step 6 — clean teardown.**

```console
$ sudo umount /mnt/demo-data
$ sudo sed -i '/demo-data/d' /etc/fstab && sudo mount -a   # fstab back to pristine
$ sudo losetup -d /dev/loop0 && rm ~/demolab-disk.img
$ lsblk                                     # the device is gone — it was a file all along
```

*Narration:* "The disk never existed. Every *command* was real; the
*object* made it safe. That distinction is this course's whole safety
architecture."

## Questions to ask

1. Before step 2: "what am I about to destroy?" (the loopback's
   contents — nothing else)
2. After step 4: "which field would I change for a USB backup disk,
   and why?" (nofail)
3. After step 5: "your snapshot vs this backup — why does the capstone
   accept only the second?" (restore-tested, separate location)

## Common errors & recovery

- Loop device name differs (`loop1`, `p16` partition naming) — use
  `losetup -f --show`'s output and `lsblk` to read the real partition
  name; never hard-code
- `mount: /mnt/demo-data: wrong fs type` — mkfs was skipped or ran on
  the wrong node; `lsblk -f` shows who has a filesystem
- fstab typo (space vs tab is fine, wrong UUID isn't) → `mount -a`
  fails: fix with `sudo mount -o remount /mnt/demo-data` diagnostics,
  or restore the snapshot — never leave a broken fstab
- `losetup -d` refused (still busy) → an unmount was missed; `mount |
  grep demo` finds it

## Recovery

Snapshot `pre-loopback` restores any mid-demo disaster (including a
broken fstab). On stage, *narrate* the restore if you use it — that's
the method.

## Cleanup (census)

Step 6 is the cleanup — verify with:

```console
$ grep -c demo-data /etc/fstab        # 0
$ losetup -l | wc -l                  # no demo loops
$ ls ~/demolab-disk.img 2>&1          # No such file
```

## Optional extension

`losetup` a *second* file, make an ext4 on it, and `mount -o loop` —
students articulate why the two "disks" are independent. LVM/RAID
reading pointer closes the session.
