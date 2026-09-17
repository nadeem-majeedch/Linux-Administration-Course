# M04 — Installing Linux & Virtual Machines

## Objectives & navigation

The module's formal **learning objectives, concepts, command-line skills,
laboratory, exercises, and Data Science connection** are specified in the
roadmap: [COURSE-ROADMAP.md — Unit 1 · Foundations of Linux](../../../COURSE-ROADMAP.md#unit-1--foundations-of-linux-m01m04).
This page indexes the material; the lessons deliver it.

| Layer | Where |
|---|---|
| Objectives & module contract | [Roadmap](../../../COURSE-ROADMAP.md#unit-1--foundations-of-linux-m01m04) + [module README](../README.md) |
| Lessons | below, in order — do the end-of-lesson self-checks |
| Labs | [labs/README.md](labs/README.md) |
| Practice | [practice/](practice/) — quiz (+ instructor key), challenges |
| Troubleshooting | [troubleshooting.md](troubleshooting.md) |

> From "I have a laptop" to "I have a lab": provision an Ubuntu VM you
> can break fearlessly, verify the download like an administrator,
> and keep a reset button for the whole course.

**Lessons**

| # | Lesson | You will be able to |
|---|--------|---------------------|
| 1 | [01-why-a-lab-not-a-laptop.md](lessons/01-why-a-lab-not-a-laptop.md) | Argue the VM-first approach and choose between VirtualBox, virt-manager and WSL2 for your hardware |
| 2 | [02-provision-the-vm.md](lessons/02-provision-the-vm.md) | Create a VM with sane disk/CPU/memory sizing, install Ubuntu Server, and snapshot the clean state |
| 3 | [03-verify-and-first-boot.md](lessons/03-verify-and-first-boot.md) | Verify the ISO (M02's skill, applied), complete first login, and read a fresh boot's evidence |
| 4 | [04-snapshots-and-reset-discipline.md](lessons/04-snapshots-and-reset-discipline.md) | Use snapshots as the course's safety net — and know what they are *not* (backups, M26) |

**Labs** — [labs/README.md](labs/README.md): the full provisioning
lab (download → verify → install → snapshot → break → restore) plus
the WSL2 alternate track.

**Practice** — [practice/quiz.md](practice/quiz.md) (18 Q),
[challenges.md](practice/challenges.md) (C1–C5).

**Prerequisite map:** consumes M02 (checksums/signatures) and M03
(what you'll watch boot). Feeds every later module: this VM *is* the
course's laboratory.
