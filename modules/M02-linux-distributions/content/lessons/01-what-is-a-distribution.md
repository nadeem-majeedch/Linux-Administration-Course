# Lesson 1 — What Is a Distribution?

> Module 02 · Unit 1 · Difficulty: Beginner
> Reading time: ~20 min · Up next: [Identify your distro](02-identify-your-distro.md)

---

## 1. Linux the kernel vs Linux the operating system

From [M01](../../../M01-what-is-linux/README.md): **Linux** is a kernel —
the program that owns the hardware and grants processes their
resources. A kernel alone can't edit a file or fetch a page. An
**operating system** needs hundreds of pieces around it: a shell, core
utilities (`ls`, `cp`), libraries (glibc), a package manager, boot
tooling, documentation.

A **distribution** ("distro") is a curated, tested, *shipped-together*
bundle of all of it: one vendor's selection of kernel version, libc,
core utilities, package manager, installer, defaults, and support
promise. The analogy this course uses: the kernel is an engine; a
distribution is the whole car — chassis, controls, warranty, and the
dealer network that keeps it fueled.

Why hundreds of distros exist: different audiences optimize differently
— a server distro optimizes stability and decade-long support; a
hobbyist distro optimizes freshness; a container base image optimizes
size. Same kernel, different promises.

## 2. The three ingredients that define a family

Distros cluster into families by three choices:

1. **Package manager & format** — the tool that installs software.
   Debian-family: `apt`/`.deb`. Red Hat-family: `dnf`/`.rpm`. Arch:
   `pacman`. Alpine: `apk`. This is the most visible daily difference.
2. **Release model** — *point releases* (fixed versions with long
   support: Ubuntu LTS, RHEL) vs *rolling* (continuous updates: Arch,
   openSUSE Tumbleweed). Servers favor point + LTS: predictability
   beats novelty when colleagues depend on the machine.
3. **Defaults & provenance** — which libc (glibc vs musl), which
   init (systemd nearly everywhere now), which defaults and support
   organization (community vs commercial).

## 3. The family map (the five you'll actually meet)

| Family | Flagship examples | Package manager | Release model | Where you'll meet it |
|---|---|---|---|---|
| **Debian** | Debian, **Ubuntu**, Linux Mint | `apt` (.deb) | point + LTS (Ubuntu: 5-yr support on LTS) | This course; most cloud & DS images |
| **Red Hat** | RHEL, Fedora, CentOS Stream, Rocky/Alma | `dnf` (.rpm) | RHEL: enterprise-long; Fedora: fast point | HPC clusters, enterprise servers, many university grids |
| **SUSE** | SLES, openSUSE | `zypper` (.rpm) | enterprise + rolling variant | European enterprise, some HPC |
| **Arch** | Arch, Manjaro | `pacman` | rolling | hobbyist boxes, "latest everything" |
| **Alpine** | Alpine Linux | `apk` | point, small | **containers** — the most common tiny base image |

Two lines of context worth knowing: **Ubuntu LTS** (Long Term Support)
releases every two years with five years of free updates — the reason
this course pins to it (colleagues' scripts and vendor images assume
it); and **RHEL rebuilds** (Rocky, Alma) exist because RHEL is
commercial — the RPM ecosystem without the contract.

## 4. Which distro for data science, and why it rarely matters

Most DS tooling (Python, conda, Docker images, CUDA drivers) targets
the *big two* families first: Debian-family and RHEL-family. Your
skills from this course transfer because the **layer under the package
manager is the same**: same kernel interfaces, same systemd, same
bash, same OpenSSH. What changes between families is the *package
manager's accent* (`apt install` vs `dnf install`) and some file
locations — a two-hour translation, once you know where to look
(next lesson: looking).

The course teaches Ubuntu because: LTS predictability, the widest
documentation, default availability in clouds and teaching labs, and
the Debian-family dominance of container bases (`python:3.12-slim` is
Debian underneath — M28's bases, named at last).

---

## Key takeaways

- Distribution = kernel + userland + package manager + defaults +
  **support promise**, shipped as one tested unit.
- Families differ by **package manager, release model, defaults**;
  Debian/Ubuntu and Red Hat families cover most of the DS world.
- Point/LTS releases trade freshness for predictability — the server
  trade.
- The tooling you learned (systemd, bash, SSH, permissions) is
  family-portable; the package manager is the accent.

## Check yourself

1. What three ingredients cluster distros into families?
2. Why do servers prefer point/LTS releases while hobbyists often
   choose rolling?
3. You meet a machine running `dnf`. Which family, and what's the
   Debian equivalent command?
4. Why does this course pin Ubuntu LTS rather than the latest
   release?

*Answers:* (1) package manager/format, release model, defaults &
provenance. (2) Predictability and long support windows vs freshness —
colleagues and vendor tooling depend on the floor not moving. (3) Red
Hat family; `apt install`. (4) Five years of support, widest
documentation/vendor compatibility, Debian-family dominance of DS
container bases — predictability for a 30-module course.

Up next: [Identify your distro](02-identify-your-distro.md) — reading a
system's identity from files.
