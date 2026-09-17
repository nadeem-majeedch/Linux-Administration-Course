# 14 — Storage & Filesystems

> Learn it: [M17 — Storage & Filesystems](../modules/M17-storage-and-filesystems/content/README.md) ·
> Lookup, not understanding.

## Looking (all safe, all read-only)

| Command | Purpose | Key options / examples |
|---|---|---|
| `lsblk` | disk & partition tree | `lsblk -f` adds filesystems/UUIDs |
| `df -h` | **filesystem** free/used space | `-h` human · `-i` inodes · `-x tmpfs` skip noise |
| `du -sh DIR` | **directory** sizes | `-h` human · `--max-depth=1` per-child |
| `blkid` | UUIDs & types | the fstab source of truth |
| `findmnt /mount` | what's mounted where, options | verification after remount |
| `free -h` | memory & swap | `available` is the honest column |

**`df` vs `du`:** df counts blocks on the filesystem; du counts
visible files. They disagree for two classic reasons —
*deleted-but-open* files (`lsof +L1` finds them) and `du` not
seeing what your user can't read (`sudo du -xsh /`).

## Mounting

```console
$ findmnt                        # everything currently mounted
$ sudo mount /dev/sdb1 /mnt/data # device → directory
$ sudo umount /mnt/data          # ⚠️ busy = something's using it: lsof +D /mnt/data
$ sudo mount -a                  # mount everything in fstab — run BEFORE rebooting
$ sudo mount -o remount,ro /mnt  # flip options live
```
Unmount before unplugging removable media — `umount` is what
flushes the write cache; skipping it is how files vanish.

## `/etc/fstab` — boot-time mounts

```text
# <device>            <mount>   <type>  <options>     <dump> <pass>
UUID=1a2b-…           /mnt/data ext4    defaults      0      2
```
| Rule | Why |
|---|---|
| Use `UUID=` (from `blkid`), never `/dev/sdX` | device letters change between boots |
| End with `nofail` on non-critical mounts | a missing disk shouldn't drop the machine to emergency shell |
| Always test with `sudo mount -a` before rebooting | a typo here can stop the boot |

## Making a filesystem — the lab-safe loopback way

```console
$ dd if=/dev/zero of=~/disk.img bs=1M count=100    # 100 MiB image FILE (not a device!)
$ mkfs.ext4 -F ~/disk.img                          # format it
$ sudo mount -o loop ~/disk.img /mnt/test          # mount via loop device
$ df -h /mnt/test; sudo umount /mnt/test
```
⚠️ **Never** `mkfs`/`dd of=` on a real device path in coursework —
the loopback image gives you a real filesystem with none of the
blast radius.

## Swap

| Check | Command |
|---|---|
| size/usage | `free -h` (swap row) · `swapon --show` |
| activity (is it *churning*?) | `vmstat 1` → `si/so` columns |
| which process got swapped | `grep VmSwap /proc/*/status \| sort -h -k2 \| tail` |

Size ≠ activity: a used swap page that's never touched is fine;
constant `si/so` is memory pressure.

## Concepts you administer around

| Concept | One-line working knowledge |
|---|---|
| ext4 | Ubuntu default journaling FS; the safe answer for local volumes |
| inodes | one per file; `df -i` exhaustion = millions of tiny files, **not** a space problem |
| journaling | crash recovery without full fsck; why ext4 survives power cuts |
| LVM | volume management layer: resize/grow logical volumes over partitions |
| RAID 1/5 | disk redundancy (mirroring/parity) — **not** a backup |
| SSD vs HDD | SSDs: no defrag, TRIM (`fstrim.timer`), put hot data here; HDDs: cheap depth for archives |
| quotas | per-user/group limits — concept on shared servers |

## Space triage (the full-disk drill)

```console
$ df -h                          # which filesystem?
$ sudo du -xsh /* 2>/dev/null | sort -h | tail    # drill down layer by layer
$ sudo lsof +L1 | sort -k7 -h | head              # deleted-but-open eaters
$ find /var/log -size +100M -exec ls -lh {} \;    # big logs
$ sudo journalctl --vacuum-size=200M             # safe journal reclaim
```
Fix order: reclaim tool-natively (logs, journal, caches) → move
data → *then* consider resizing. Never delete under `/home` or
`/srv` to "free space" on a shared machine — it's someone's data.
