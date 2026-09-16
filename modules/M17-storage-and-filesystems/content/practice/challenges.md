# Challenge Problems — Module 17

After the quiz; own VM only, snapshot for anything in Part ≥ B of the
safety contract. Record pipelines + outputs in `lab-log.md`.

- [ ] **C1 — the topology interview.** Write `storage-report.sh`: a
  script (bash, M10-preview level) that prints lsblk -f, df -h (no
  tmpfs), df -i (top 3 by IUse%), and the top-5 du offenders of `/var`
  — one command a sysadmin would actually run on a new box.
- [ ] **C2 — the inode experiment.** On a fresh 50-M loopback ext4:
  `df -i` before; generate 50,000 empty files (`mkdir
  /mnt/lab/x; cd /mnt/lab/x; for i in $(seq 1 50000); do : > $i; done`
  — then measure how many *actually* landed before `No space left on
  device`); `df -h` vs `df -i` at exhaustion. Which filled first?
  Clean up. (This is the inode cliff, experienced.)
- [ ] **C3 — the held-open hunt.** Reproduce Lab 2 Part C's mystery,
  then solve it *without killing the process*: `: > /proc/PID/fd/N`
  truncates the held-open file. Verify df drops while tail still runs.
  (This trick saves servers at 3 a.m.)
- [ ] **C4 — the fstab gauntlet.** On loopback mounts only: create
  three fstab entries — one correct, one with a wrong UUID, one
  missing nofail pointing at a device you then detach. `findmnt
  --verify` each; document every verdict; then simulate the boot
  behavior of #3 with `mount -a` (what mounts? what's skipped?). Clean
  up all three.
- [ ] **C5 — swap A/B.** With `vmstat 2` running: (a) run a memory
  hog (`python3 -c "a='x'*10**10"` — watch it die or swap), (b) note
  si/so, (c) after killing it, `swapoff -a && swapon -a` and re-check.
  Write 3 sentences on what swap did for the system here.
- [ ] **C6 — the LVM field trip.** On any LVM-equipped system (or a
  fresh Ubuntu Server VM): map PV→VG→LV→mountpoint completely from
  `pvs/vgs/lvs/lsblk`. Then read `man lvextend` and write the exact
  command to grow the largest LV by 5G *if* the VG had free space (do
  you? say why not).
- [ ] **C7 — the tiering plan.** Design (document, don't execute) the
  storage for a 4-person DS lab: 1 TB SSD, 4 TB HDD, budget for one
  more disk. Deliverable: mount points, fstab lines, what lives where
  (raw/intermediate/results/venvs), backup statement, and the M13
  permission layer per tree.
- [ ] **C8 — the disaster post-mortems.** For each, write the
  symptom→diagnosis→fix→prevention in the course's incident format:
  (a) fstab typo, no nofail, headless server won't boot;
  (b) `df` 95% but `du` finds half the space — name two candidate
  causes and the command for each;
  (c) "I unplugged the USB and now the files are gone" — what actually
  happened, and the two-step rule that prevents it.

C2 and C3 are the two most transferable skills in this module — both
show up in real ops interviews.
