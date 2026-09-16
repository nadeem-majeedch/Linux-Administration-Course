# Lesson 3 — Persistence: /etc/fstab, UUIDs & the Safe Mount Workflow

> Module 17 · Unit 5 · Difficulty: Advanced
> Reading time: ~35 min · Lab: continues [Lab 1](../labs/lab-01-loopback-disk-lab.md)
> Prerequisites: [Lesson 2](02-partitions-filesystems-mounting.md)

> 🔴 **Safety tier:** `/etc/fstab` edits are own-VM + sudo + backup.
> A wrong fstab line can make the next boot stop and wait (or drop to an
> emergency shell). This lesson's workflow — backup, `nofail`, `findmnt
> --verify`, test-boot — exists so a typo costs minutes, not an
> unbootable machine.

---

## 1. The problem fstab solves

`mount` lives until reboot. A data disk that must exist *every* boot
needs a declaration the kernel's userspace (systemd) reads at startup:
`/etc/fstab` — the **f**ile **s**ystem **tab**le. One line per
persistent mount:

```text
UUID=8c7d...-1e...  /mnt/data  ext4  defaults,nofail  0  2
```

Six fields, left to right — memorize the pattern, then the details:

| # | Field | Example | Meaning |
|---|---|---|---|
| 1 | **what** | `UUID=…` | the device/identity to mount |
| 2 | **where** | `/mnt/data` | mount point (must exist) |
| 3 | **type** | `ext4` | filesystem type (`auto` allowed) |
| 4 | **options** | `defaults,nofail` | comma-separated, no spaces! |
| 5 | **dump** | `0` | legacy backup flag — always 0 today |
| 6 | **pass** | `2` | fsck order at boot: 0 = never, 1 = root only, 2 = rest |

Reading stock Ubuntu's own entries is the best drill:

```console
$ grep -v "^#" /etc/fstab
UUID=8c7d...  /         ext4  errors=remount-ro  0  1
UUID=B2A1-9C0F  /boot/efi  vfat  umask=0077  0  1
/swapfile      none       swap  sw          0  0
```

Root has pass 1 (checked first); EFI is vfat with a locked-down umask;
the swapfile declares type `swap` at mount point `none` — all three are
patterns you'll reproduce in variations forever.

---

## 2. What to put in field 1: UUID, not /dev/sdX

Lesson 1 warned: `/dev/sdb` can become `/dev/sdc` across boots.
Filesystem **UUIDs** (set at format time, stable for the FS's life) are
the fix:

```console
$ sudo blkid                    # every block device's identity (sudo to see all)
/dev/sda3: UUID="8c7d...-1e..." TYPE="ext4" PARTUUID="a1b2..."
/dev/sdb1: UUID="f00d...-ba5e" TYPE="ext4" PARTLABEL="data"
$ lsblk -f                      # same info, tree view (no sudo)
```

For the *what* field, the convention ladder:

1. **`UUID=…`** — default choice; stable across reboots and port changes.
2. `PARTUUID=…` — identifies the *partition* (survives reformatting the
   FS — niche use).
3. `LABEL=data` — human-readable labels (`mkfs.ext4 -L data`); fine on
   small setups.
4. `/dev/sdX` — **never in fstab.** Discovery-order roulette.

Two UUIDs exist per partition (FS-UUID and PARTUUID) and both look
similar in `blkid` output — `lsblk -f`'s UUID column is the FS-UUID
fstab wants by default.

---

## 3. Field 4: the options that matter

`defaults` = `rw,suid,dev,exec,auto,nouser,async` — a reasonable bundle.
Beyond it, the options with real operational meaning:

| Option | Effect | When |
|---|---|---|
| **`nofail`** | boot continues if the device is missing | **external/data disks — always** |
| `noatime` | don't record access times | datasets, SSDs (fewer writes) |
| `ro` | mount read-only | archives, immutable raw data |
| `errors=remount-ro` | on error, go read-only (ext4 default) | integrity over availability |
| `auto`/`noauto` | mount at boot / only on demand | removable media |
| `user`/`nouser` | mortals may mount / only root | desktop convenience |
| `umask=0077` | restrictive perms (vfat) | shared USB sticks |

**`nofail` deserves its own paragraph.** Without it, a missing device at
boot (unplugged USB, a cloud volume not yet attached) leaves systemd
waiting and can drop the machine to an emergency shell — a headless
server now needs console access. With `nofail`, the machine boots and
your data directory is simply empty. Rule: **every non-root mount in
fstab gets `nofail`.** (Root cannot have it — without root there is no
system; that's what pass 1 and rescue mode are for.)

---

## 4. The safe persistence workflow (course standard)

Six steps between "mounted manually" and "will survive reboot":

```console
# 1. Get the identity
$ sudo blkid /dev/sdb1
# 2. Ensure the mount point exists (empty!)
$ ls -A /mnt/data && sudo mkdir -p /mnt/data
# 3. BACKUP the file you're about to edit
$ sudo cp /etc/fstab /etc/fstab.bak-$(date +%F)
# 4. Edit — append the line (visudo-style caution: no editor war here,
#    but the backup IS the safety net)
$ sudo nano /etc/fstab
#    UUID=f00d...-ba5e  /mnt/data  ext4  defaults,nofail,noatime  0  2
# 5. VERIFY WITHOUT REBOOTING
$ sudo findmnt --verify --verbose
# 6. Prove it: unmount, then mount *from fstab alone*
$ sudo umount /mnt/data
$ sudo mount -a          # mounts everything fstab declares
$ findmnt /mnt/data      # it's back → the entry works
```

`findmnt --verify` parses your fstab, checks that devices/types/mount
points are consistent, and reports problems *before* boot does. It has
caught more student unbootable-VMs than any other command in this
module. `mount -a` (mount-all) is the functional test: if it succeeds,
the boot-time mount will too.

**If you break fstab anyway:** boot may drop to an emergency shell with
`/` mounted read-only. The repair sequence: `mount -o remount,rw /` →
fix or comment out the bad line (`nano /etc/fstab`) → `mount -a` →
reboot. In a VM you also have snapshots — which is why the lab says
*snapshot first*.

---

## 5. systemd's view (a one-paragraph preview)

systemd reads fstab at boot and generates `.mount` unit files behind
the scenes — you can see them:

```console
$ systemctl list-units --type=mount | head -5
```

This is why `findmnt --verify` matters even in a systemd world: fstab
*is* still the configuration interface; systemd is the engine that
executes it. Native systemd mount/automount units (and what they add)
are M20's territory — for persistence, fstab remains the common
denominator every admin speaks.

---

## 6. DS framing: the dataset volume pattern

The realistic end-state of this lesson — a lab server's second disk,
dedicated to datasets, declared safely:

```text
UUID=f00d...-ba5e  /srv/datasets  ext4  defaults,nofail,noatime  0  2
```

Then the group-permission layer from M13 (`chgrp labteam; chmod 2770
with setgid`) lives *inside* that mount — storage (this module) and
access control (M13) compose. When the cloud team attaches a 2-TB
volume, your fstab line is ready before the disk is. "Datasets live at
/srv/datasets, declared by UUID, nofail, noatime" is a sentence you
will either write or read in every data team you join.

---

## Exercises (lab-log.md)

1. Decode your VM's stock fstab line by line (all six fields each).
   Which entries have `nofail`? Why is its absence on `/` correct?
2. `findmnt --verify` on the *unmodified* stock fstab — what does it
   report? (Some warnings are normal; name them.)
3. Why `noatime` for a dataset volume? What do you trade away? (Think:
   forensic timelines vs write amplification.)
4. Write (don't apply) the fstab line for a USB archive disk mounted
   read-only at /mnt/archive. Justify each field including dump/pass.
5. Simulate the failure mode *safely*: add a fstab line for a
   nonexistent device **without** nofail, run `findmnt --verify`, read
   the verdict, then delete the line. What would boot have done?
6. (Stretch, after Lab 1) Take your loopback mount through the full §4
   workflow, then prove persistence the honest way: `sudo reboot`, log
   back in, and `findmnt /mnt/labdata` without touching anything.

## Check yourself before Lesson 4

- [ ] I can write all six fstab fields from memory with nofail, and
      explain dump/pass.
- [ ] I verify with findmnt --verify and test with mount -a — never
      "reboot and pray."
- [ ] I know the emergency-shell repair sequence before I need it.
- [ ] I can state the dataset-volume fstab pattern as one sentence.

## Further reading (official sources)

- `man 5 fstab`, `man findmnt`, `man mount` (util-linux)
- Ubuntu Server Docs — mounting/fstab: https://ubuntu.com/server/docs
- systemd.mount documentation (how fstab becomes units):
  https://www.freedesktop.org/software/systemd/man/latest/systemd.mount.html
