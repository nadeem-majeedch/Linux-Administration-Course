# Answer Key — Module 17 Quiz

Each answer cites the lesson to revisit.

1. A device addressable in fixed-size blocks, exposed as a file under
   `/dev` (mode `b`). (L1 §1)
2. `sd` SATA/USB, `nvme` PCIe SSDs, `vd` virtio VM disks, `loop`
   files-as-devices. (L1 §1)
3. Discovery order can swap between boots; FS **UUIDs** are stable.
   (L1 §1, L3 §2)
4. e.g. `sda3  ext4  8c7d…  /` = third partition of sda, formatted
   ext4, FS-UUID 8c7d…, currently mounted at /. (L1 §2)
5. df = per-*filesystem* fullness; du = per-*directory* usage.
   Disagreement: deleted-but-held-open files (lsof +L1), or files
   hidden under a mount point. (L1 §4)
6. Inodes exhausted (`df -i` IUse% 100) — metadata capacity is fixed
   at format time. (L1 §3)
7. `du -h --max-depth=1 ~ | sort -rh | head -5`. (L1 §4)
8. MBR caps at 2 TiB and 4 primary partitions; GPT does neither. (L2 §1)
9. Superblock, inode tables, allocation maps, journal — the *index*
   that maps names to data; without it the data is unreachable.
   (L2 §2)
10. `sudo mkdir -p /mnt/data; sudo mount /dev/sdb1 /mnt/data`;
    on "busy": `lsof +f -- /mnt/data` (or fuser -vm), fix holder
    (cd away, stop process), `sudo umount /mnt/data`. (L2 §3)
11. A regular file attached to a loop device (`losetup`), behaving as a
    real block device — full parted/mkfs/mount practice where mistakes
    cost `rm`. (L2 §3, Lab 1)
12. Live repair corrupts a mounted FS; ext4 journals replay at mount
    and fsck refuses mounted targets anyway. (L2 §4)
13. `UUID=f00d-ba5e  /srv/datasets  ext4  defaults,nofail,noatime  0  2`
    (L3 §1, §4)
14. what/where/type/options/dump/pass; dump is a legacy backup flag
    nothing uses (dump(8) is dead). (L3 §1)
15. Without nofail, a missing device stalls boot (or emergency shell);
    with it, boot proceeds and the point is empty. `/` can't nofail —
    no root, no system. (L3 §3)
16. `findmnt --verify` (parses/validates) and `mount -a` (functional
    test, then `findmnt` to confirm). (L3 §4)
17. A swapfile is a file — resize/relocate without repartitioning;
    chmod 600 because swap contents are memory images (keys, tokens).
    (L4 §1)
18. PVs (plots) → VG (land bank) → LV (building parcel);
    `sudo lvextend --resizefs /dev/vg/data -L +10G`. (L4 §2)
19. Survives one disk failure via parity; doesn't survive deletion,
    ransomware, controller death, or double faults — a mirror
    replicates `rm -rf` instantly, so backups remain mandatory. (L4 §3)
20. TRIM (`fstrim.timer`) keeps writes fast; cells wear (TBW); place
    hot random-I/O on SSD, cold sequential on HDD. (L4 §4)
21. Buffered writes may not have reached the device; umount flushes
    them and closes cleanly — "eject" is umount. (L4 §5)
22. Hot/active experiments + indexes on SSD; raw archive on HDD;
    implemented with partitions/LV per tier, each in fstab (UUID,
    nofail, noatime) per tier. (L4 §4, §6)
23. A *tree* of mounts with source/type/options — occlusion is visible
    before you hide someone's files under a new mount. (L2 §3)
