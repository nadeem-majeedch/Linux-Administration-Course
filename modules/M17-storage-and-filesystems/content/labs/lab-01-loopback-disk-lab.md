# Lab 1 — The Loopback Disk Lab: a Disk Lifecycle Without a Disk

> Module 17 · Unit 5 · Difficulty: Intermediate → Advanced
> Time: ~60 min · Environment: **your own VM, snapshot taken first**
> Prerequisites: [Lessons 1–3](../lessons/01-block-devices-topology.md)
>
> You will build, use, persist, and cleanly remove an entire disk —
> partition table, filesystem, fstab entry and all — on a **loopback
> image**: a 100-MB file that Linux treats as a real block device.
> Every command is one you'd run on a real data disk; every mistake
> costs a deleted file.

## 0. Pre-flight (5 min — do not skip)

```console
$ echo "=== LAB17 $(date +%F) ===" >> ~/lab-log.md
$ sudo losetup -a                # existing loop devices? (expect few/none)
$ lsblk                          # baseline topology — paste into lab-log
```

**Snapshot the VM now** (VirtualBox: Machine → Take Snapshot; Multipass:
`multipass stop <vm>` then snapshot via the hypervisor; WSL2: your data
is safe — loop devices work fine — but note `wsl --export` as your
escape hatch). *The snapshot is the lab's undo button.*

## Part A — create and attach the disk (10 min)

```console
$ truncate -s 100M ~/lab17-disk.img        # a sparse 100-MB "disk"
$ sudo losetup --find --show ~/lab17-disk.img
/dev/loop0
$ losetup -a | grep lab17                  # PROOF: which loop holds your file?
$ lsblk /dev/loop0                         # your disk exists
NAME    MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
loop0     7:0    0  100M  0 loop
```

**Record:** the loop device name. **From here on, every command in this
lab uses `/dev/loopN` — substitute your N. Verify with `losetup -a`
before anything destructive. The rule is absolute: if a command's
target isn't your loop device, stop.**

## Part B — partition and format (15 min)

```console
$ sudo parted /dev/loop0 mklabel gpt                 # NEW partition table
$ sudo parted /dev/loop0 mkpart datasets ext4 1MiB 100%
$ sudo parted /dev/loop0 print                       # verify: 1 partition, gpt
$ sudo mkfs.ext4 -L labdata /dev/loop0p1             # FORMAT (loopback-safe!)
$ lsblk -f /dev/loop0                                # FSTYPE + UUID now present
```

**Record:** the FS-UUID from `lsblk -f` (you'll need it in Part D), and
one sentence: what did `mkfs` put on the partition that wasn't there
before?

## Part C — mount and use (10 min)

```console
$ sudo mkdir -p /mnt/labdata
$ sudo mount /dev/loop0p1 /mnt/labdata
$ df -h /mnt/labdata                       # ~97M usable — where did 3M go? (fs metadata)
$ echo "dataset manifest v1" | sudo tee /mnt/labdata/MANIFEST.txt
$ sudo mkdir /mnt/labdata/raw && echo "a,b,c" | sudo tee /mnt/labdata/raw/sample.csv
$ findmnt /mnt/labdata                     # mounted, ext4, rw — evidence pasted
```

## Part D — persistence, the safe way (15 min)

Follow Lesson 3's workflow exactly:

```console
$ sudo cp /etc/fstab /etc/fstab.bak-$(date +%F)      # backup — non-negotiable
$ sudo nano /etc/fstab
```

Append (your UUID):

```text
UUID=<your-loop-fs-uuid>  /mnt/labdata  ext4  defaults,nofail,noatime  0  2
```

```console
$ sudo findmnt --verify --verbose          # VERDICT must be clean
$ sudo umount /mnt/labdata
$ sudo mount -a                            # fstab-only mount — the real test
$ findmnt /mnt/labdata && cat /mnt/labdata/MANIFEST.txt
```

**Record:** the `findmnt --verify` output. If it flags anything, fix
the line before continuing — this is the skill, not the mount.

## Part E — prove persistence (the honest way, 5 min)

```console
$ sudo reboot
# ... log back in ...
$ findmnt /mnt/labdata                     # there without you touching it
$ cat /mnt/labdata/MANIFEST.txt            # data intact
```

(WSL2: a full reboot is `wsl --shutdown` from PowerShell then relaunch —
loop attachments don't survive it, so *document that caveat* instead:
in real VMs the fstab line persists; in WSL2 you'd re-attach and
mount manually. Write the two-sentence comparison.)

## Part F — clean removal (10 min — the half everyone skips)

Reverse the whole stack, in order, verifying at each step:

```console
$ sudo nano /etc/fstab              # delete your line (or: sed -i '/labdata/d')
$ sudo findmnt --verify             # clean again
$ sudo umount /mnt/labdata
$ sudo losetup -d /dev/loop0        # detach the loop
$ losetup -a | grep lab17 || echo "detached"
$ rm ~/lab17-disk.img               # the disk ceases to exist
$ lsblk | grep loop0 || echo "gone" # topology back to baseline
```

**Record:** the removal transcript next to the Part-A baseline — the
pair *is* the lab's deliverable: a full lifecycle with no residue.

## Wrap-up — the operator's reflection

1. Which single command in this lab would have been catastrophic on
   your real disk, and what three habits kept it safe here?
2. Order matters in Part F — what breaks if you `losetup -d` before
   `umount`? (Try it on a *fresh* tiny loopback if curious.)
3. Your cloud team attaches a real 500-GB volume tomorrow. List the
   Part B–D commands with the device name swapped — that's your
   runbook. Save it as `lab-log.md`'s last entry.

## Done when

- [ ] Snapshot taken (before Part A) and noted in lab-log
- [ ] Baseline + final `lsblk` pasted; loop device verified before every
      destructive step
- [ ] fstab line verified with findmnt --verify; mount -a proven
- [ ] Persistence proven by reboot (or WSL2 caveat documented)
- [ ] Full clean removal — zero residue
- [ ] Reflection + the real-disk runbook written
