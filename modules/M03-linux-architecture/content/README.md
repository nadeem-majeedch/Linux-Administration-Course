# M03 — Linux Architecture: from firmware to user space

> The x-ray of the machine you've been using. By the end you can draw
> the whole stack and name what each layer owns.

**Lessons**

| # | Lesson | You will be able to |
|---|--------|---------------------|
| 1 | [01-the-layer-cake.md](lessons/01-the-layer-cake.md) | Draw the full Linux stack and explain which layer a given problem lives in |
| 2 | [02-kernel-space-user-space.md](lessons/02-kernel-space-user-space.md) | Explain kernel vs user space, syscalls, the C library, and why the boundary is a *security* boundary |
| 3 | [03-boot-to-shell.md](lessons/03-boot-to-shell.md) | Trace boot from firmware → bootloader → kernel → init → login, and interrupt/recover the menu on your VM |
| 4 | [04-userspace-anatomy.md](lessons/04-userspace-anatomy.md) | Name the runtime components behind every command you type: shell, libc, loaders, services |

**Labs** — [labs/README.md](labs/README.md): the anatomy tour on
your own VM (procfs/sysfs evidence), plus a GRUB menu intervention.

**Practice** — [practice/quiz.md](practice/quiz.md) (20 Q),
[challenges.md](practice/challenges.md) (C1–C6).

**Prerequisite map:** M01 gave you the vocabulary; M02 told you which
distribution flavor of each layer you have. This module shows where
every later module *lives*: M10 in the kernel's process table, M16 in
the package manager's userspace, M20 in PID 1, M24 in the kernel's
ring buffers.
