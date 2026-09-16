# Lesson 4 — Swap, LVM, RAID, SSDs & Removable Media

> Module 17 · Unit 5 · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Lab 2 — the space audit](../labs/lab-02-space-audit.md)
> Prerequisites: Lessons 1–3

> 🟡 **Safety tier:** this lesson is *mostly concepts* — swap creation and
> LVM are own-VM, sudo, snapshot-first operations; RAID is concept-only
> in this course (real RAID belongs to dedicated storage training). Every
> command that writes is labeled inline.

---

## 1. Swap: the overflow valve

**Swap** is disk space the kernel uses when RAM runs low — either a
dedicated partition or a swapfile. Pages of memory that haven't been
touched get written to disk, freeing RAM for active work.

```console
$ free -h                     # the summary (M18's reading, swap line now)
$ cat /proc/swaps             # device-level detail: partition or file?
Filename     Type       Size  Used  Priority
/swapfile    file       4194300 0    -2
$ swapon --show               # same, human units
```

**What swap is for (and against):**

- ✅ Absorbs rare spikes; lets the OOM killer (M18 §5) be a last resort
  instead of the *first* symptom; hibernation needs it.
- ❌ Disk is ~1000× slower than RAM. A *swapping* server is effectively
  down — si/so in `vmstat` (M18) nonzero while load is high means the
  box is thrashing.

Ubuntu defaults to a swapfile sized ~1×RAM up to 4 GB. The
resize operation (own VM, sudo, safe — swapfile, not partition):

```console
$ sudo fallocate -l 2G /swapfile2          # 1. create
$ sudo chmod 600 /swapfile2                # 2. root-only (security!)
$ sudo mkswap /swapfile2                   # 3. format as swap
$ sudo swapon /swapfile2                   # 4. enable
$ echo '/swapfile2 none swap sw 0 0' | sudo tee -a /etc/fstab   # 5. persist
$ swapon --show                            # verify both active
```

(Symmetric removal: `swapoff`, fstab line out, `rm`. The `chmod 600`
isn't cosmetic — world-readable swap leaks whatever memory held:
keys, tokens, your data.)

**DS servers and swap:** GPU boxes typically run *minimal* swap — the
right response to memory pressure is killing the runaway job (M18), not
thrashing. But know both policies and the reason for each.

---

## 2. LVM: the flexible volume layer

**Logical Volume Manager** inserts a layer between disks and mounts:
physical devices feed **volume groups**, from which **logical volumes**
are carved and mounted. The translation table:

| LVM object | Made of | Think of it as |
|---|---|---|
| **PV** (physical volume) | a disk/partition initialized for LVM | a plot of land |
| **VG** (volume group) | pooled PVs | the land bank |
| **LV** (logical volume) | carved from a VG | the parcel you actually build on |

```console
$ sudo pvs; sudo vgs; sudo lvs        # read-only inventories (recognize, don't run yet)
$ lsblk                               # LVM shows as type 'lvm' under an 'sd' disk
```

**Why it exists — the elasticity story:** your `/home` LV is full, but
`/tmp`'s LV has 80 GB spare. Without LVM: buy a disk, migrate, edit
fstab. With LVM: `lvextend --size +50G --resizefs /dev/vg0/home` — the
filesystem grows *online*, no unmount. That single command is why LVM
is the default on Ubuntu Server and every cloud image:

- grow volumes live (`lvextend` + `resize2fs`, or `--resizefs` in one)
- add disks to the pool whenever (`vgextend`)
- snapshots: freeze a consistent view for backup (`lvcreate --snapshot`)
  — the backup feature M26's backup lesson builds on

**Course depth:** recognize the three-layer stack in `lsblk` output,
read `pvs/vgs/lvs` inventories, and know `lvextend --resizefs` by name.
Creating PVs/VGs/LVs is an own-VM exercise you can do once from the
official guides — this course stops at fluency, not mastery.

### DS framing

Cluster scratch volumes, cloud data disks, and anything "we might need
bigger later" is an LVM story. The phrase to recognize in onboarding
docs: "*the data VG is thin-provisioned*" — pooled, elastic, expandable
on demand (thin provisioning = allocate blocks as written, not upfront).

---

## 3. RAID: redundancy concepts (recognition level)

**RAID** (Redundant Array of Independent Disks) combines disks for
capacity, speed, and/or survival. The levels you must recognize on
sight:

| Level | Layout | Buys you | Costs you |
|---|---|---|---|
| **0** | stripes across disks | speed + capacity | **no redundancy** — one disk dies, all data gone |
| **1** | mirror (two copies) | survival of one disk | 50% capacity |
| **5** | stripe + parity (3+ disks) | survives one disk | parity overhead, write penalty |
| **6** | double parity (4+ disks) | survives two disks | more overhead |
| **10** | mirror+stripe (4+) | speed + survival | 50% capacity |

Two sentences that summarize twenty years of storage arguments: **RAID
is not backup** (it survives disk failure, not deletion, ransomware, or
controller death — a mirror replicates your `rm -rf` instantly). And
**parity rebuild on huge disks is where arrays die** — modern practice
prefers RAID-1/10 or nothing-plus-backups for most workloads.

Software RAID on Linux = `mdadm` (recognize the name; `/proc/mdstat`
shows arrays). Hardware RAID hides as one big "disk" in `lsblk` — the
topology lesson's "why is my 8-disk server showing one disk?" answer.

### DS framing

"Is the lab server RAID?" is a question you'll ask before trusting it
with the only copy of anything. The correct follow-up — "and where do
backups go?" — is M26's. RAID never excuses dataset backup discipline.

---

## 4. SSD vs HDD: the considerations that change decisions

| Concern | SSD (incl. NVMe) | HDD |
|---|---|---|
| Random I/O latency | ~100 µs | ~10 ms (100× slower) |
| Best for | databases, VMs, frequent small reads, boot | bulk sequential: archives, backups, cold datasets |
| Writes wear cells | yes (TBW rating) | no (mechanical wear instead) |
| Cost per TB | higher | lower |
| Over-provisioning/TRIM | needs periodic `fstrim` | n/a |

Operational takeaways:

- **`fstrim`**: SSDs need periodic trim (Ubuntu runs a weekly timer:
  `systemctl status fstrim.timer` — check yours). Without it, writes
  slow over months. This is a *why-did-the-SSD-get-slow* answer.
- **Placement heuristics:** hot data (active experiments, database
  files, venvs) on SSD; cold data (raw archive, completed runs) on HDD
  or object storage. The 80/20 of dataset access makes tiering cheap.
- **NVMe vs SATA SSD:** same semantics, NVMe is the PCIe-fast one —
  that's why the device names differ (Lesson 1).

---

## 5. Removable media & quotas (two short sections)

**USB/external drives** mount like any device — with two manners:

```console
$ lsblk                                    # find it (usually sdb/sdc)
$ sudo mkdir -p /media/usb && sudo mount /dev/sdb1 /media/usb
$ sudo umount /media/usb                   # BEFORE unplugging — always
```

The unmount-before-unplug rule isn't bureaucracy: buffered writes may
not have reached the device yet; `umount` flushes. "Eject" in desktops
= the same operation. FAT/exfat sticks carry no Unix permissions —
anything sensitive on one is readable by whoever holds it (and M13's
permission model doesn't travel with it).

**Quotas (concept only):** ext4/xfs support per-user/per-group **space
and inode quotas** — the sysadmin's answer to "one student filled the
shared volume." You'll recognize them in onboarding docs (`usrquota`,
`grpquota` mount options, `repquota` reports); the practical DS
equivalent you control is *cultural*: per-project directories with
agreed budgets, plus the `du` audit from Lab 2. Real quota administration
is a sysadmin task — know it exists, don't configure it on shared kit.

---

## 6. The storage decision card (the lesson in one box)

| Question | Answer |
|---|---|
| Need more space on an existing volume? | LVM: `lvextend --resizefs` |
| Is it safe if one disk dies? | RAID-1/5/10 — but backups are still mandatory |
| Is it fast for random small reads? | SSD/NVMe (and `fstrim` healthy) |
| Can it fill "silently"? | `df -h` + `df -i` monitoring; quotas for shared boxes |
| Will it survive reboot? | fstab line, UUID, **nofail**, verified |
| Is it the only copy? | **Then it doesn't exist yet.** Backups (M26). |

---

## Exercises (lab-log.md)

1. `cat /proc/swaps` + `swapon --show` on your VM: partition or file?
   Size? (Then compute: swap seconds-to-fill at the vmstat si/so rates
   you saw in M18's labs — one sentence.)
2. Resize drill (own VM, sudo, snapshot first): create a 512-M swapfile
   with the five-step §1 sequence, verify, then remove it cleanly. Paste
   the transcript. Why is the `chmod 600` step security-relevant?
3. LVM reading drill: on a default Ubuntu *server* install (or any VM
   image that has it), run `lsblk` and `sudo lvs; sudo vgs`. Name the
   VG, its LVs, and which mount each LV feeds. If your desktop VM has
   no LVM, say so and explain what that implies about its install
   choice.
4. RAID reasoning: your advisor proposes RAID-5 on four 12-TB disks for
   the lab's new server "so we never lose data." Write the 4-sentence
   reply: what RAID-5 buys, what it doesn't (two failure modes), and
   the question you ask next (backups).
5. `systemctl status fstrim.timer` — enabled? When did it last run?
   (Journal line.) One sentence on what would happen without it.
6. Design: 40-TB raw dataset arrives; 2 TB SSD + 8 TB HDD available.
   Propose the tiering (what lives where, moving what when) in five
   lines. Which Lesson-2/3 mechanics implement it?

## Check yourself before the labs

- [ ] I can create and remove a swapfile in five commands, safely.
- [ ] I can read a 3-layer LVM stack in lsblk and name PV/VG/LV.
- [ ] I can say what each RAID level buys/costs — and why RAID ≠ backup.
- [ ] I know why removable drives get unmounted before unplugging.

## Further reading (official sources)

- `man 8 swapon`, `man 8 mkswap`, `man 8 fallocate` (util-linux)
- LVM upstream docs: https://sourceware.org/lvm2/
- `man 8 mdadm` (software RAID: https://raid.wiki.kernel.org/)
- `man 8 fstrim`; kernel docs — SSD/NVMe:
  https://docs.kernel.org/admin-guide/
