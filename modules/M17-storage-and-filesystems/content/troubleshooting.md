# Troubleshooting — Module 17

Symptom → cause → check → fix → prevention. Destructive operations are
marked; when in doubt, snapshot first.

## 1. `mount: /mnt/data: unknown filesystem type 'ext4'` on a valid device

- **Cause:** wrong device (that's the *disk*, not a partition —
  `/dev/sdb` vs `/dev/sdb1`), or no filesystem on it.
- **Check:** `lsblk -f /dev/sdb` — FSTYPE column: empty = never
  formatted; FS on whole disk = you're pointing at the parent.
- **Fix:** the correct partition (`/dev/sdb1`), or format if truly
  empty (**destructive — loopback/own-VM only, verify target twice**).
- **Prevention:** `lsblk -f` before every mount; the habit answers
  this before mount fails.

## 2. `umount: target is busy`

- **Cause:** a process holds a file open or has cwd inside.
- **Check:** `lsof +f -- /mnt/data` or `fuser -vm /mnt/data`; your own
  shell's cwd is the most common holder.
- **Fix:** `cd /` out of it, stop the process, retry umount.
- **Prevention:** never leave terminals sitting inside mounts; umount
  before closing work.

## 3. Boot drops to emergency shell after an fstab edit

- **Cause:** bad fstab line (wrong UUID, missing mount point, syntax).
- **Check (in the emergency shell):** the console names the failed
  unit; `journalctl -xb` shows the mount attempt.
- **Fix:** `mount -o remount,rw /` → correct or comment the line in
  `/etc/fstab` → `mount -a` → reboot. (VM snapshot restore is the
  other path — take it if the shell feels unfamiliar.)
- **Prevention:** Lesson 3's workflow — backup, `nofail` on data
  disks, `findmnt --verify`, `mount -a` test — makes this near-
  impossible to cause.

## 4. `df` says full; `du` finds half the space

- **Cause (ranked):** deleted-but-open files; files under a mount
  point; (ext4) root-reserved blocks.
- **Check:** `lsof +L1` (open+deleted); `findmnt` on the path; `df -h`
  vs `du -xh --max-depth=1 /` sums.
- **Fix:** restart/`trunc` the holder (`: > /proc/PID/fd/N`); unmount
  and audit the underlying dir; reserved blocks are ext4 policy
  (`tune2fs -m` — sysadmin territory).
- **Prevention:** log rotation + the weekly audit habit (Lab 2).

## 5. `No space left on device` but `df -h` shows plenty free

- **Cause:** **inodes exhausted** — millions of tiny files.
- **Check:** `df -i <path>` — IUse% at or near 100.
- **Fix:** find and archive/delete the file flood
  (`du --inodes -s /* 2>/dev/null | sort -rn | head`), or reformat
  with more inodes (destructive; replan bytes-per-inode).
- **Prevention:** `df -i` in monitoring; batch pipelines write
  containers (tar/parquet), not one-file-per-event.

## 6. Data disk vanished after reboot

- **Cause:** fstab entry missing/wrong, device renamed (no UUID), or
  the disk simply wasn't attached (cloud volume).
- **Check:** `lsblk -f` (is it there but unmounted?); `systemctl
  status mnt-data.mount`; `journalctl -b | grep -i mount`.
- **Fix:** mount manually, then repair the fstab line via Lesson 3's
  workflow (UUID + nofail + verify).
- **Prevention:** `nofail` everywhere except `/`; verify before
  rebooting (always).

## 7. `mount: /mnt/x: can't find in /etc/fstab` (when mounting as user)

- **Cause:** non-root users may only mount fstab-declared entries with
  the `user` option.
- **Check:** `grep /mnt/x /etc/fstab` — is `user`/`users` in options?
- **Fix:** sudo mount (one-off), or add `user,noauto` for a personal
  removable-media entry.
- **Prevention:** removable media gets a proper fstab line too.

## 8. USB stick writes silently lost / "files disappeared"

- **Cause:** unplugged without unmount — buffered writes never
  flushed; or FAT/exfat has no permission model and something else
  (a sync tool) overwrote.
- **Check:** dmesg tail (`I/O error` lines tell the story).
- **Fix:** usually nothing to fix — the data never landed. Re-copy,
  then **umount before unplugging**, always.
- **Prevention:** the two-command reflex: `sync && sudo umount /media/...`
  (sync forces buffers; umount confirms clean close).

## 9. SSD "getting slower over months"

- **Cause:** TRIM not running — deleted blocks aren't reclaimed by the
  drive.
- **Check:** `systemctl status fstrim.timer` (enabled? last run?);
  `lsblk --discard` (does the device support it?).
- **Fix:** `sudo fstrim -av` once, then ensure the weekly timer is
  enabled (`systemctl enable fstrim.timer`).
- **Prevention:** it's a timer — just check it exists on new machines
  (especially non-Ubuntu installs).

## 10. Swap "used" but system not slow (or: swap at 0% but OOM killed)

- **Cause:** swap holding *old, cold* pages is normal and healthy;
  swap at 0% during a spike means allocation outpaced swap-in.
- **Check:** `vmstat 2 5` (si/so rates, not totals); `free -h`
  available; the OOM evidence from M18 (`journalctl -k | grep -i oom`).
- **Fix:** none needed for case 1 (swap used ≠ thrashing); case 2 is
  the M18 playbook (limit the job, chunk the data), not a swap fix.
- **Prevention:** read si/so *rates*, never the swap-used column
  alone; capacity-plan memory like disk.
