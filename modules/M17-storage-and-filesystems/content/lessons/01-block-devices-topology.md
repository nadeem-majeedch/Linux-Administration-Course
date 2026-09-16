# Lesson 1 — Block Devices & Storage Topology: lsblk, df, du

> Module 17 · Unit 5 · Difficulty: Intermediate
> Reading time: ~35 min · Lab: [Lab 1 — the loopback disk lab](../labs/lab-01-loopback-disk-lab.md)
> Up next: [Lesson 2 — partitions, filesystems, mounting](02-partitions-filesystems-mounting.md)

> 🟢 **Safety level of this lesson: entirely read-only.** Every command
> here *observes* storage; nothing changes a single block. The
> write-capable tools start in Lesson 2 — inside a loopback image, not
> your disk.

---

## 1. Disks and block devices

A **disk** (SSD, HDD, NVMe drive, USB stick, SD card, virtual disk) is,
to Linux, a **block device**: a file in `/dev` that represents something
addressable in fixed-size **blocks** (usually 512 B or 4 KiB). Block
devices live up to their name:

```console
$ ls -l /dev/sda /dev/nvme0n1 2>/dev/null | head -3
brw-rw---- 1 root disk 8, 0 Mar 10 09:12 /dev/sda
brw-rw---- 1 root disk 259, 0 Mar 10 09:12 /dev/nvme0n1
```

The `b` at the start of the mode string = block device. Note the
permissions: `root:disk`, mode 660 — **ordinary users can't read raw
disks at all**, which is your first safety layer: accidental
`cp dataset /dev/sda` fails politely with Permission denied unless you
have sudo.

Naming conventions (memorize these four families):

| Pattern | Meaning | Example parts |
|---|---|---|
| `/dev/sdX` | SCSI/SATA/USB disks, letters in discovery order | `sda`, `sdb`; partitions `sda1`, `sda2` |
| `/dev/nvme0n1` | NVMe (PCIe SSDs) — controller 0, namespace 1 | partitions `nvme0n1p1`… |
| `/dev/vdX` | virtio disks (KVM/QEMU VMs) | `vda`, `vda1` |
| `/dev/loopN` | loopback — *files* mounted as block devices | `loop0`, `loop1p2` |

⚠️ **Why discovery-order naming matters:** `sda` and `sdb` can swap
between boots if drives enumerate differently — which is why Lesson 3
teaches fstab via **UUIDs**, never device names.

### DS framing

Every dataset you will ever wrangle lives on a block device — often one
you didn't choose (cloud VM data disk, cluster scratch volume). Reading
topology is step one of "can I fit this 800-GB intermediate file?" and
of "which disk died?" — both questions you'll face in year one of work.

---

## 2. lsblk: the family portrait

`lsblk` (list block devices) draws the whole tree — disks, partitions,
mount points — from sysfs:

```console
$ lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
loop0    7:0    0  74.3M  1 loop /snap/core22/1234
sda      8:0    0 25G    0 disk
├─sda1   8:1    0  1G    0 part /boot
├─sda2   8:2    0  513M  0 part /boot/efi
└─sda3   8:3    0 23.5G  0 part /
sr0     11:0    1 1024M  0 rom
```

Read it as a story: one 25-GB disk (`sda`), three partitions — a real
`/boot`, an EFI system partition, and the root filesystem holding
everything else. `RM 1` = removable; `RO 1` = write-protected; `sr0` =
the optical drive (VMs mount ISOs here).

The flag everyone should know:

```console
$ lsblk -f
NAME   FSTYPE FSVER LABEL    UUID                                 FSAVAIL ...
sda
├─sda1 ext4   1.0            3f2e...-4d...                          811M
├─sda2 vfat   FAT32          B2A1-9C0F
└─sda3 ext4   1.0   ubuntu-f 8c7d...-1e...                         18.7G   /
```

`-f` adds **FSTYPE** (what filesystem each partition holds) and
**UUID** — the immutable identity that fstab uses. A partition with no
FSTYPE is raw space: created but never formatted. That observation is
the entire setup of Lab 1.

```console
$ lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT,MODEL   # custom columns
$ lsblk /dev/sdb                                     # just one device (when you have one)
```

---

## 3. df: filesystems and their fullness

`lsblk` shows *hardware*; `df` (disk free) shows *mounted filesystems*
and how full they are:

```console
$ df -h
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           1.9G  1.2M  1.9G   1% /run
/dev/sda3        23G   4.3G   18G  20% /
tmpfs           9.4G     0  9.4G   0% /dev/shm
/dev/sda1       974M  163M  744M  17% /boot
```

`-h` = human units (G/M instead of blocks). The columns that matter:
`Avail` (can I fit the dataset?) and `Use%` (am I near the cliff?).

**Two readings beginners get wrong:**

1. **tmpfs lines are RAM**, not disk — `/run`, `/dev/shm` live in
   memory. They're big and "free" and irrelevant to disk space.
2. **One filesystem can appear many times** (bind mounts, overlays in
   containers, snaps). Deduplicate by the first column before summing.

```console
$ df -hT                              # -T adds the filesystem TYPE column
$ df -h /home                         # just the filesystem holding /home
$ df -i /                             # INODES — Lesson 2's cliff, previewed
Filesystem     Inodes IUsed IFree IUse% Mounted on
/dev/sda3      2.9M   214K  2.7M    7% /
```

`df -i`: a filesystem can run out of *inodes* (file-count capacity) with
gigabytes "free" — the classic death of a mail server or a `node_modules`
collector. Data-science variant: a pipeline writing one file per
sensor reading per second.

---

## 4. du: who is using the space

`df` says *the filesystem* is full; `du` (disk usage) says *whose files*
did it. Per-directory sizes:

```console
$ du -h ~/datasets                     # human-readable total of one directory
3.2G    ~/datasets
$ du -h --max-depth=1 ~ | sort -rh | head -8     # the one-liner of self-knowledge
4.3G    /home/dsstudent
3.2G    /home/dsstudent/datasets
680M    /home/dsstudent/.cache
310M    /home/dsstudent/venvs
...
```

`--max-depth=1` (one level of subtotals) + `sort -rh` (human-numeric
descending) = the space audit in one pipeline. Other workhorse flags:

| Flag | Effect | Use |
|---|---|---|
| `-s` | summarize (total only) | quick size of one dir |
| `-a` | all files, not just dirs | find the single biggest file |
| `--apparent-size` | logical bytes vs disk blocks | sparse files, tarballs |
| `--exclude` | skip patterns | skip `.git`, datasets you know |

**df vs du disagreement** — the classic puzzle: `df` says 20 GB used,
`du` finds 12 GB. Explanations, in order of likelihood: (1) a deleted
file still held open by a process (its blocks aren't freed until the
process exits — `lsof +L1` finds the holder, M18-style); (2) files
beneath a *mount point* (du of `/mnt`'s underlying directory is
invisible when something's mounted on it — Lesson 2); (3) reserved
blocks for root (ext4 reserves ~5%). Lab 2 hunts these deliberately.

---

## 5. free & swap inventory (the RAM side)

```console
$ free -h
       total  used  free  shared  buff/cache  available
Mem:    15Gi  3.1Gi  6.8Gi  210Mi       5.4Gi       11Gi
Swap:  3.9Gi    0B  3.9Gi
```

M18 taught `available`; here add the swap line — Lesson 4 covers what
swap *is* and how to resize it. `cat /proc/swaps` shows device-level
detail (partition vs swapfile — a distinction that matters in Lesson 4).

---

## 6. Reading a real topology (worked example)

Put it together on your own VM and *narrate* it (this is Lab 2's opener):

1. `lsblk -f` — "one 25-G virtual disk, 3 partitions: EFI (vfat),
   /boot (ext4), root (ext4, mounted at /). No spare space, no data
   disk yet."
2. `df -h /` — "root is 20% used; 18 G available — the venv and
   datasets have room."
3. `df -i /` — "7% inodes — fine."
4. `du -h --max-depth=1 ~ | sort -rh | head` — "my home is 4.3 G; the
   cache directory is 680 M and first on the cleanup list."

That narration — topology → capacity → inode headroom → ownership — is
the standard "storage health check" you'll run on any new server,
usually within your first hour on it.

---

## Exercises (lab-log.md)

1. Run the §6 narration on your own machine, all four steps, with real
   output pasted. Identify: how many physical disks, how many
   filesystems, which is most full, what your biggest home directory is.
2. `lsblk -f`: which of your partitions have no FSTYPE? (Answer may be
   "none" — say so and explain what a partition with no FSTYPE would
   mean.)
3. `df -h /` vs `df -h /tmp` on a stock Ubuntu VM: same filesystem?
   Why does /tmp usually share root's? (M06 FHS + this lesson.)
4. Find one tmpfs line in `df -h` and explain in one sentence why its
   "Size" can exceed your disk's size.
5. Run `du -h --max-depth=1 ~ | sort -rh | head -5` and write your
   top-5 space consumers with one cleanup candidate circled.
6. (Stretch) Create the df/du disagreement *safely* in a terminal:
   `sleep 600 &` then `tail -f /var/log/syslog > /tmp/holder.log`,
   `rm /tmp/holder.log` (in another terminal), then `df -h /tmp; lsof
   +L1 | grep holder`. Explain the held-open blocks in two sentences,
   then Ctrl-C the sleep and re-check df.

## Check yourself before Lesson 2

- [ ] I can name every device family (sd/nvme/vd/loop) on sight.
- [ ] I read lsblk -f for FSTYPE and UUID without being told.
- [ ] I never mistake tmpfs for disk.
- [ ] I can run the four-step storage health check from memory.

## Further reading (official sources)

- `man lsblk`, `man df`, `man du`, `man free` (util-linux manual:
  https://github.com/util-linux/util-linux)
- kernel docs — /proc/sys and block devices:
  https://docs.kernel.org/admin-guide/
- Ubuntu Server Docs — storage: https://ubuntu.com/server/docs
