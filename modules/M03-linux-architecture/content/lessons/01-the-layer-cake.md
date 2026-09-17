# Lesson 1 — The Layer Cake

> Module 03 · Unit 1 · Difficulty: Beginner → Intermediate
> Reading time: ~20 min · Lab: [Lab 1](../labs/lab-01-anatomy-tour.md)
> Up next: [Lesson 2 — kernel space and user space](02-kernel-space-user-space.md)

---

## 1. Why draw the stack at all

Every skill in this course is a question to one layer of a stack:

- "Why can't I write to this file?" — a **permissions** question (M13)
- "Why is my training slow?" — a **hardware/kernel** question (M08, M24)
- "Why did my service die on reboot?" — an **init** question (M20)
- "Why is this Python different from that Python?" — a **user space**
  question (M27)

You cannot diagnose what you cannot locate. This module gives you the
map; every later module annotates a region.

## 2. The stack, top to bottom

```
┌─────────────────────────────────────────────┐
│  Applications        python, jupyter, git   │  user space
├─────────────────────────────────────────────┤
│  Shells & utilities  bash, ls, grep, ssh    │
├─────────────────────────────────────────────┤
│  Libraries           glibc, OpenSSL,        │
│                      libpython              │
├────────────────────── ▲ syscalls ───────────┤
│  KERNEL              process/memory/net/    │  kernel space
│                      fs/driver subsystems   │
├─────────────────────────────────────────────┤
│  Bootloader          GRUB2                  │  pre-kernel
├─────────────────────────────────────────────┤
│  Firmware            UEFI (or BIOS)         │  pre-boot
├─────────────────────────────────────────────┤
│  HARDWARE            CPU · RAM · disk · NIC │
└─────────────────────────────────────────────┘
```

Two truths to carry for the rest of the course:

1. **Each layer only talks to its neighbors.** Python never touches
   your disk; it asks glibc/`libcurl`, which asks the kernel, which
   asks the driver. When something breaks, you walk the boundary
   between two layers, not the whole stack.
2. **Everything above the kernel can be swapped without touching it**
   — that's the lesson of M02. The kernel + bootloader + firmware are
   shared by every distro on the machine; user space is what
   distributions *are*.

## 3. Walking the cake with one command

Follow one command down the stack — `ls`:

- `bash` parses your typing (user space, shell layer)
- `bash` asks the kernel to *fork + exec* `/bin/ls` (syscall
  boundary)
- `ls` links against `libc`, calls `opendir`/`read` (library layer)
- each becomes a **syscall** (`getdents64`) crossing into the kernel
- the kernel's VFS consults the ext4 driver and the block driver
- the driver programs the (virtual) disk controller — hardware

Now run it and see the layers leave fingerprints:

```console
$ type -a ls                 # shell layer: which ls does bash run?
$ ldd /usr/bin/ls | head     # library layer: what does it link?
$ strace -c ls >/dev/null    # kernel boundary: which syscalls? (safe)
```

`strace` is safe here because `ls` only reads. You'll see `openat`,
`getdents64`, `close` — the boundary crossing in act 3.

## 4. Where the course's modules live on the cake

| Layer | Owner modules |
|-------|---------------|
| Firmware/bootloader | M03 (this one); touched in M04 installs |
| Kernel (processes, memory, fs, net) | M10, M18, M21, M24; tuned in M16 |
| Libraries | M27 (Python envs are library layer), M16 (packages install here) |
| Shells & utilities | M05–M12, M19, M20, M22 |
| Applications | M27–M29, M30 capstone |

Keep this table. Half of "where do I even start?" is answering
*which layer* — and this is the map that answers it.

## 5. The Data Science connection

Your stack has one more annotation: **CUDA**. When M31 discusses GPU
work, the question "why won't PyTorch see the GPU?" is a *layer*
question: framework → toolkit → driver → hardware. Diagnosing it is
walking this cake downward, one boundary at a time — the same skill
as `strace`-ing `ls`.

---

**Key takeaways**

- The stack: hardware ← firmware ← bootloader ← kernel ← libraries ←
  shell/utilities ← applications.
- Layers talk only to neighbors; bugs and slowness are located by
  walking boundaries.
- User space is swappable (M02); the kernel boundary is fixed per
  boot (Lesson 2).

**Check yourself:** in the `ls` walkthrough, name the layer where
each of these lives: `getdents64` · glibc · bash's parsing · the
ext4 driver.

**Next:** [Lesson 2 — kernel space and user space](02-kernel-space-user-space.md)
