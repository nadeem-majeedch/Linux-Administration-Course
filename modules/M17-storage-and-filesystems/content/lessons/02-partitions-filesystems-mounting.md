# Lesson 2 — Partitions, Filesystems & Mounting (on a Loopback Disk)

> Module 17 · Unit 5 · Difficulty: Intermediate → Advanced
> Reading time: ~40 min · Lab: [Lab 1 — the loopback disk lab](../labs/lab-01-loopback-disk-lab.md)
> Prerequisites: [Lesson 1](01-block-devices-topology.md)

> 🔴 **Safety tier for this lesson:** the *concepts* are free; the
> *commands* (`parted`, `mkfs`, `mount`) are **own-VM + sudo + a
> disposable target only**. The disposable target here is a **loopback
> image** — a plain file (say, `disk.img`) that Linux treats as a real
> block device. You can `mkfs` it, mount it, destroy it, and delete it
> with `rm` — the perfect classroom. **Never in this course will you
> repartition your real disk as an exercise.**

---

## 1. Partitions: carving one disk into many

A **partition** is a declared slice of a disk with its own boundaries,
recorded in a **partition table** at the disk's start. Two table formats
exist:

| | MBR (msdos) | GPT |
|---|---|---|
| Max size | 2 TiB | 9.4 ZB (effectively unlimited) |
| Max primary partitions | 4 (extended/logical hack) | 128 standard |
| Redundancy | none | primary + backup table |
| Modern default | legacy/BIOS only | **yes** — UEFI systems |

Modern Ubuntu installs are GPT + UEFI. `lsblk` doesn't show the table
type; `sudo parted /dev/sdX print` does (own VM, read-only subcommand):

```console
$ sudo parted /dev/sda print
Model: ATA VBOX HARDDISK (scsi)
Disk /dev/sda: 26.8GB
Partition Table: gpt
Number  Start   End     Size    File system  Name     Flags
 1      1049kB  538MB   537MB   fat32        EFI      boot, esp
 2      538MB   1075MB  537MB   ext4
 3      1075MB  26.8GB  25.8GB  ext4
```

`parted` is interactive-capable and scriptable; `print` (read-only) is
safe everywhere; its modifying subcommands (`mklabel`, `mkpart`,
`rm`) are Lab-1-loopback-only in this course. One wrong `mklabel` on a
real disk erases the partition table — **the course will never ask you
to run it on anything but a loopback file.**

---

## 2. Filesystems: what a partition becomes

A partition is raw space until a **filesystem** organizes it into
files, directories, and metadata. Creating one is **formatting**
(`mkfs.*` — "make filesystem"). Ubuntu's default is **ext4**; you should
recognize the others:

| FS | Character | Where you meet it |
|---|---|---|
| **ext4** | journaling, mature, default | Ubuntu's root, /boot, data disks |
| xfs | high-performance, RHEL default | big-file workloads, RHEL family |
| btrfs | copy-on-write, snapshots | openSUSE, some NAS |
| vfat/FAT32 | universal, no permissions | EFI partition, USB sticks |
| exfat | modern FAT, big files | cross-platform external drives |
| tmpfs | RAM-backed, volatile | /run, /dev/shm (Lesson 1) |

**What formatting actually does** (ext4): writes the superblock
(the FS's own metadata header), inode tables, block-allocation maps,
and the journal. Formatting does not (necessarily) overwrite data
blocks — but it destroys the *index*, which for practical purposes
destroys the data. Treat `mkfs` as a data-destruction command, always.

### The inode (the FS's real unit of accounting)

Every file is an **inode**: a fixed-size record holding metadata
(permissions, owner, timestamps, size) and pointers to data blocks.
Directory entries map *names → inode numbers*; `ls -i` shows them.

Consequences worth knowing:

- **Inode limits are set at format time** (`mkfs.ext4` chooses bytes-per-
  inode) — a filesystem can run out of inodes while having free space
  (Lesson 1's `df -i`).
- **Hard links** (M07) are directory entries sharing one inode — same
  number, two names.
- **A file's name lives in the directory; its identity lives in the
  inode** — renaming changes nothing about the inode. Deleting releases
  the inode when its link count hits zero *and* no process holds it
  open (Lesson 1's df/du puzzle).

---

## 3. Mounting: grafting a filesystem onto the tree

Linux has no "D:" drive — every filesystem is **mounted** at a
directory (its **mount point**), making its contents appear *inside*
the tree. The kernel's mount table:

```console
$ findmnt /            # the tree view of one mount
TARGET SOURCE    FSTYPE OPTIONS
/      /dev/sda3 ext4   rw,relatime,errors=remount-ro
$ findmnt | head -6    # the whole tree, indented by graft point
```

The mount/umount pair (sudo required — mounting is a system-wide
operation):

```console
$ sudo mkdir -p /mnt/data
$ sudo mount /dev/sdb1 /mnt/data       # device → directory
$ ls /mnt/data                          # contents appear
$ sudo umount /mnt/data                 # detach (by MOUNT POINT or device)
```

**The two umount errors everyone meets:**

```console
$ sudo umount /mnt/data
umount: /mnt/data: target is busy.
```

Something holds it: a shell with cwd inside, an open file, a running
copy. Find the holder, stop it, then unmount:

```console
$ lsof +f -- /mnt/data                  # who's holding? (or: fuser -vm /mnt/data)
$ cd /                                  # your own shell is a frequent culprit
$ sudo umount /mnt/data
```

Never use `umount -l` (lazy) as a routine fix — it detaches the *name*
while I/O continues underneath, which is how "unmounted" disks get
corrupted. Diagnose first; `-l` is the escalation, not the habit.

**The mount-point occlusion trap:** mounting over a non-empty directory
*hides* what was there (the files aren't gone — they're under the new
filesystem). `findmnt` first, always: "is anything already mounted
here?"

### The loopback trick: a file as a disk

A loopback image is a regular file attached to a loop device, making it
a full citizen of block-device land:

```console
$ truncate -s 100M ~/lab17-disk.img          # sparse 100-MB file
$ sudo losetup --find --show ~/lab17-disk.img
/dev/loop0
$ lsblk /dev/loop0                           # it's a "disk" now
NAME    SIZE TYPE
loop0   100M disk
```

Now every Lesson-2 command — `parted`, `mkfs`, `mount` — works on
`/dev/loop0` *exactly* as it would on a real disk. Delete the file at
the end and the whole exercise evaporates. Lab 1 runs this end to end;
**that lab is the only sanctioned place to practice `mkfs`/`parted` in
this course.**

---

## 4. Filesystem checks: fsck, with its danger framing

`fsck` (filesystem check) repairs inconsistencies — after unclean
shutdowns, or on filesystems that report errors. The rules that keep it
from being a data-destruction command:

1. **Never fsck a mounted filesystem.** Live repair of a mounted FS
   corrupts it. (ext4 self-checks on mount and refuses fsck anyway —
   the refusal is your friend.)
2. **Check, don't assume:** `fsck -N /dev/sdb1` shows what *would* run;
   `fsck -n` does a read-only check.
3. **Repair interactively or with explicit flags** (`fsck -y` answers
   yes to everything — powerful, last resort).

```console
$ sudo fsck -N /dev/sdb1        # what would run? (safe)
$ sudo fsck -n /dev/sdb1        # read-only check (safe on unmounted)
$ sudo fsck /dev/sdb1           # real repair: unmounted, sudo, careful
```

In normal life ext4 journals make fsck rare — you'll mostly meet it via
systemd's boot-time checks or `fsck.mode=force` kernel parameters. Know
it, fear it appropriately, use it only unmounted.

---

## 5. Worked example: the loopback lifecycle (the whole lesson in 12 lines)

Preview of Lab 1's spine — read it, then *do it* in the lab with the
checklist:

```console
$ truncate -s 100M ~/lab17-disk.img
$ sudo losetup --find --show ~/lab17-disk.img        # /dev/loop0
$ sudo parted /dev/loop0 mklabel gpt                 # NEW table (loopback-safe!)
$ sudo parted /dev/loop0 mkpart data ext4 1MiB 100%
$ sudo mkfs.ext4 /dev/loop0p1                        # format the partition
$ sudo mkdir -p /mnt/labdata
$ sudo mount /dev/loop0p1 /mnt/labdata
$ echo "hello from a file-disk" | sudo tee /mnt/labdata/note.txt
$ cat /mnt/labdata/note.txt
$ sudo umount /mnt/labdata
$ sudo losetup -d /dev/loop0                         # detach
$ rm ~/lab17-disk.img                                # everything gone, nothing harmed
```

Every line there has a real-disk analog — which is exactly why it's
practiced on a file first.

---

## Exercises (lab-log.md)

1. MBR vs GPT: name two limits that make MBR a poor choice for a 4-TB
   dataset disk. Which table does your VM's disk use? (`parted print`,
   read-only.)
2. Why does the course call `mkfs` a data-destruction command even
   though "formatting doesn't overwrite data"? One precise sentence.
3. `df -i /` — what's your inode use%? Compute how many files you could
   still create (`IFree`). When would a data pipeline care?
4. Explain the mount-occlusion trap: you mount a new disk at /srv/data
   which already has 500 GB of files. Where are they? What does
   `findmnt` tell you *before* the mount?
5. A teammate proposes `umount -l` as their standard unmount. Write the
   two-sentence reply with the correct alternative.
6. Run the §5 lifecycle *with* the lab checklist. Paste your transcript
   — this is the deliverable that Lesson 3 and Lab 1 build on.

## Check yourself before Lesson 3

- [ ] I can read a parted printout (table type, flags, FS).
- [ ] I know what mkfs really does and why it's always "destructive."
- [ ] I can mount, hit "target is busy," diagnose with lsof, and fix it.
- [ ] I have run the full loopback lifecycle once.

## Further reading (official sources)

- `man parted`, `man mkfs.ext4` (e2fsprogs: https://e2fsprogs.sourceforge.net/)
- `man mount`, `man umount`, `man findmnt`, `man losetup` (util-linux)
- kernel docs — filesystems: https://docs.kernel.org/filesystems/
- Ubuntu Server Docs — storage: https://ubuntu.com/server/docs
