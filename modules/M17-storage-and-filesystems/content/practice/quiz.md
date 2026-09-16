# Module 17 Quiz — 22 Questions

Answer in `lab-log.md`; key: [quiz-answers.md](quiz-answers.md).

1. **R** What is a block device, and where do block device files live?
2. **R** Name the four device-naming families (sd/nvme/vd/loop) and one
   place you'd meet each.
3. **U** Why is `/dev/sdX` naming unsafe for fstab, and what replaces it?
4. **P** Decode one `lsblk -f` line completely: NAME, FSTYPE, UUID,
   MOUNTPOINT.
5. **R** `df` vs `du` — what does each measure, and what does their
   disagreement usually mean? (Two causes.)
6. **U** Why can `df` show free space while the filesystem refuses new
   files? (The inode cliff.)
7. **P** The pipeline that lists the five biggest subdirectories of
   your home, human-sorted.
8. **R** MBR vs GPT: two limits that disqualify MBR for a 4-TB data
   disk.
9. **U** What does `mkfs` actually write, and why is it a
   data-destruction command despite "not overwriting data"?
10. **P** Mount /dev/sdb1 at /mnt/data, then unmount it — including the
    diagnosis when umount says "target is busy."
11. **R** What is a loopback image, and why is it this course's
    sanctioned practice ground?
12. **U** Why must fsck never run on a mounted filesystem? What does
    ext4 do instead at mount time?
13. **P** Write the fstab line: FS-UUID f00d-ba5e, ext4, mounted at
    /srv/datasets, defaults + nofail + noatime, standard fsck pass.
14. **U** Explain the six fstab fields in one phrase each — and why
    dump is always 0 today.
15. **R** What does `nofail` change about boot behavior, and why does
    `/` never get it?
16. **P** The two commands that verify fstab *without* rebooting.
17. **U** Swap: partition vs swapfile — one operational difference, and
    why the swapfile needs chmod 600.
18. **R** LVM: PV/VG/LV in one metaphor sentence — and the command that
    grows a mounted ext4 LV.
19. **DS** RAID-5 on four disks: what it survives, what it doesn't, and
    why "RAID is not backup."
20. **U** Two SSD-specific operational facts (TRIM, wear) and one
    placement heuristic vs HDD.
21. **R** Why must removable drives be unmounted before unplugging?
    What does umount do that matters?
22. **DS** Your 40-TB raw dataset + 2-TB SSD + 8-TB HDD: propose the
    tiering and name the Lesson-2/3 mechanics that implement it.

## Bonus

23. What does `findmnt` show that `mount`'s raw output doesn't — and
    why does that matter before mounting over a directory?
