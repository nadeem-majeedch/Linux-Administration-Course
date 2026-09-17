# Module 03 Labs

| # | Lab | Focus | Est. time |
|---|-----|-------|-----------|
| 1 | [lab-01-anatomy-tour.md](lab-01-anatomy-tour.md) | The layer-cake evidence tour: procfs/sysfs/`ldd`/`strace -c` on your own VM | 40 min |
| 2 | [lab-02-grub-intervention.md](lab-02-grub-intervention.md) | Interrupt the boot on purpose, read the kernel command line, boot once with an override | 25 min |

**Environment:** your own Ubuntu VM (Lab 2 needs a real GRUB menu;
WSL2 students do the read-only parts and observe `wsl.exe --status`
instead). All commands are read-only except the explicitly fenced
one-boot GRUB edit. No root required for Lab 1.
