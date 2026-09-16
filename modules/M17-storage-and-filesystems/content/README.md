# Module 17 — Storage, Disks & Filesystems · Content Index

> **Status:** Content complete — 4 lessons, 2 labs (loopback disk lab +
> space audit), quiz + key, 8 challenges, troubleshooting guide.
> Module contract: [../README.md](../README.md) · Difficulty: Intermediate → Advanced.

> 🛑 **Module-wide safety contract** (stated in every lesson, enforced in
> every lab):
> - **Safe anywhere:** `lsblk`, `blkid` (read), `df`, `du`, `free`, `findmnt`, `cat /proc/swaps`
> - **Own VM only, with sudo + snapshot first:** `mount`/`umount`, `mkfs`,
>   `parted`, `swapon/off`, fstab edits, LVM commands
> - **Can destroy data, always named as such:** `mkfs`, `parted mklabel`,
>   `dd` to a device, `fsck` done wrong, fstab typos at boot
> - **Never a lab exercise:** repartitioning the real/boot disk. The disk
>   lab uses a **loopback image file** — a disk that is also just a file —
>   so mistakes cost a deleted file, not a laptop.

## Lessons

| # | File | Topic |
|---|------|-------|
| 1 | [01-block-devices-topology.md](lessons/01-block-devices-topology.md) | disks, block devices, lsblk, df, du, read-only topology mapping |
| 2 | [02-partitions-filesystems-mounting.md](lessons/02-partitions-filesystems-mounting.md) | partitions (MBR/GPT), filesystems (ext4), inodes, mounting, the loopback lab groundwork |
| 3 | [03-fstab-uuids-persistence.md](lessons/03-fstab-uuids-persistence.md) | /etc/fstab fields, UUIDs, nofail, findmnt --verify, safe persistence workflow |
| 4 | [04-swap-lvm-raid-ssd.md](lessons/04-swap-lvm-raid-ssd.md) | swap, LVM (PV/VG/LV), RAID levels, SSD/HDD considerations, removable media, quotas (concept) |

## Labs

| # | File | Task |
|---|------|------|
| 1 | [lab-01-loopback-disk-lab.md](labs/lab-01-loopback-disk-lab.md) | Full disk lifecycle on a loopback image: partition → format → mount → fstab → clean removal |
| 2 | [lab-02-space-audit.md](labs/lab-02-space-audit.md) | du/df space audit of your own VM + a written cleanup plan |

## Practice & Support

- [Quiz](practice/quiz.md) (22 Q) · [Answer key](practice/quiz-answers.md)
- [Challenges](practice/challenges.md) (C1–C8)
- [Troubleshooting](troubleshooting.md) — 10 symptom→cause→fix patterns

## Cross-references

- [M06 FHS tour](../../M06-filesystem-hierarchy/content/lessons/03-filesystem-hierarchy-tour.md)
  — where things live; this module explains *what they live on*.
- [M16 package management](../../M16-package-management/content/README.md)
  — apt filled your disk; this module audits it.
- [M20 systemd](../../M20-systemd-services/README.md) — mount units &
  automounts; systemd runs the show that fstab configures.
- [M27 datasets](../../M27-python-jupyter-data/README.md) — dataset
  storage planning is this module's DS payoff.
