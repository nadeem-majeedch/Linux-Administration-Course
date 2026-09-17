# M03 — Linux Architecture

> Unit 1 · Foundations of Linux · Difficulty: Beginner → Intermediate
> Prerequisites: [M01](../M01-what-is-linux/README.md),
> [M02](../M02-linux-distributions/README.md)
> Est. time: ~5 h (lessons ~100 min, labs ~65 min, practice ~100 min)

**Status: content complete.**

## Learning objectives

By the end of this module you can:

1. **Draw and annotate** the seven layers of the Linux stack, and
   locate any problem or command on that map.
2. **Explain** the kernel-space/user-space boundary: syscalls, libc's
   role, why it is a security boundary, and the crash/isolation
   asymmetry between the two sides.
3. **Trace** the four acts of boot (firmware → bootloader →
   kernel+initramfs → init), read a boot's evidence with
   `systemd-analyze` and `journalctl -b`, and perform a safe one-boot
   GRUB intervention.
4. **Identify** the user-space actors behind a typed command — shell,
   PATH resolution, dynamic loader, shared libraries — and the
   evidence command for each.
5. **Connect** each of the above to the course's later modules
   (processes, systemd, containers, environments) as locations on one
   map.

## What's inside

| Path | Contents |
|------|----------|
| [content/README.md](content/README.md) | Module guide + prerequisite map |
| [content/lessons/](content/lessons/) | 4 lessons: layer cake · kernel/user space · boot to shell · user-space anatomy |
| [content/labs/](content/labs/) | 2 labs: anatomy tour (evidence sheet) · GRUB intervention |
| [content/practice/](content/practice/) | Quiz (+ key) · challenges C1–C6 |
| [content/troubleshooting.md](content/troubleshooting.md) | Six architecture-level symptom patterns |

## Definition of done

- [ ] Anatomy tour report with per-layer evidence lines
- [ ] One-boot GRUB override performed and reverted, evidence logged
- [ ] Quiz ≥ 16/20; C2 (the evidence diagram) completed
- [ ] You can say *which layer* — and name the one evidence command —
      for: command not found · missing `.so` · `D`-state process ·
      wrong Python

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-1--foundations-of-linux-m01m04)
- Next: [M04](../M04-installing-linux-vms/README.md) ·
  Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
