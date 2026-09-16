# Module 17 Labs — Storage & Filesystems

> Two labs. Both run **inside your own VM** — Lab 1 works on a
> **loopback image file** (a disk that is also just a file), Lab 2 is
> read-only plus your own cleanup actions. **No lab touches your real
> disk's partition table, ever.**

| # | Lab | Focus | Time |
|---|-----|-------|------|
| 1 | [lab-01-loopback-disk-lab.md](lab-01-loopback-disk-lab.md) | Full disk lifecycle on a loopback image: attach → partition → format → mount → fstab → clean removal | ~60 min |
| 2 | [lab-02-space-audit.md](lab-02-space-audit.md) | df/du space audit of your VM + a written, prioritized cleanup plan | ~40 min |

Standing safety rules (the module contract, in lab form):

- **Snapshot your VM before Lab 1** (VirtualBox: Machine → Take
  Snapshot; WSL2: note the `wsl --export` escape hatch). Restoring a
  snapshot is the undo for the whole lab.
- Every destructive command in the labs targets `/dev/loopN` — verify
  with `losetup -a` before each one. If you ever see your real disk
  (`sda`/`vda`/`nvme0n1`) in a lab command, **stop and re-read**.
- All state changes are sudo'd and reversible; the lab's final section
  removes every artifact it created.
- Record evidence in `lab-log.md` — the labs grade the transcript.
