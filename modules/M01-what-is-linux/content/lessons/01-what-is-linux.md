# Lesson 1 — What Is Linux?

> Module 01 · Unit 1 · Difficulty: Beginner
> Reading time: ~20 min · Lab: none · Up next: [Lesson 2](02-linux-vs-unix-and-open-source.md)

---

## 1. What is an operating system?

Every computer — laptop, phone, server, supercomputer — runs an **operating system**
(OS). The OS is the layer of software that sits between the hardware (the physical
machine: CPU, memory, disks, network card) and the applications you actually use
(a browser, Python, Jupyter).

The OS has four core jobs:

1. **Run programs.** Decide which program gets the CPU, and for how long
   (this is *scheduling* — you will meet it hands-on in Module 18).
2. **Manage memory.** Give each program its own memory and keep them from
   trampling each other.
3. **Manage files.** Present disks as files and folders so programs can read and
   write data without knowing disk electronics.
4. **Talk to hardware.** Translate "save this file" into electrical reality on a
   specific disk.

You have already used several operating systems, possibly without thinking about it:

| Device | Typical OS |
|---|---|
| Windows laptop | Microsoft Windows |
| Mac | macOS |
| Android phone | Android (which is built on the Linux kernel!) |
| iPhone | iOS |
| Most web servers, supercomputers, cloud VMs | **Linux** |

> **Data Science connection:** your future working life involves machines that run
> Linux: training servers, cloud notebooks, databases, Docker containers. Learning
> Linux is learning the operating system your profession actually runs on.

## 2. What exactly is "Linux"?

Here is the first surprise: **strictly speaking, Linux is not a whole operating
system.** The word "Linux" names one part of it:

> **The Linux kernel** — the core program that starts when the machine boots and
> manages the hardware forever after: CPU time, memory, disks, network cards,
> USB devices.

By itself, a kernel does nothing useful for a human. You cannot browse the web with
a kernel. A usable operating system = **kernel + a large collection of surrounding
software**: shells, command-line tools, libraries, compilers, a desktop environment,
an installer, a package manager.

In practice, "Linux" is used for both meanings:

- **Narrow (technical):** Linux = the kernel, started in 1991 by Linus Torvalds.
- **Broad (everyday):** Linux = the kernel **plus** all the system software bundled
  around it. The broad meaning is what people mean when they say "Linux server."

You will see both uses in this course; context tells you which is meant.

## 3. GNU: the other half of the name

The surrounding software — the shell, the file utilities, the compiler — mostly comes
from a project called **GNU** (GNU's Not Unix — a recursive acronym), started in 1983
by Richard Stallman. GNU set out to build a complete free operating system; by the
early 1990s it had all the parts *except* a working kernel. Linux supplied the missing
kernel, and the two fit together.

That is why the Free Software Foundation asks people to write **"GNU/Linux"** when
naming the complete OS: it credits both halves. You will hear "Linux" far more often —
it is the standard everyday term — but knowing the name "GNU" matters, because the
command-line tools you will use every day of this course (`bash`, `ls`, `cp`, `grep`,
`awk`, `tar`) are GNU software.

| Term | Refers to | Example usage |
|---|---|---|
| Linux (narrow) | The kernel | "The Linux kernel 6.8 was released…" |
| GNU/Linux (complete OS) | Kernel + GNU userland | "This server runs GNU/Linux" |
| Linux (everyday) | The whole system, any distro | "We run Linux on our GPU cluster" |
| Distribution | Kernel + userland + installer + repos + support, packaged | "Ubuntu 24.04 LTS" |

## 4. Where Linux runs

Linux's quiet dominance is the reason it is on your timetable:

- **Supercomputers:** 100% of the TOP500 supercomputers run Linux.
- **Cloud computing:** the majority of cloud virtual machines run Linux; Amazon,
  Google, and Microsoft all offer Linux as their default (often cheapest) images.
- **Servers:** most web servers, database servers, and DNS servers on the internet.
- **Containers:** Docker and Kubernetes images are overwhelmingly Linux-based.
- **Android:** billions of phones run the Linux kernel.
- **Embedded devices:** routers, TVs, cars, satellites.

**Why servers and clouds chose Linux** (each point becomes a lesson later):

| Reason | What it means | Course module |
|---|---|---|
| Free of license fees | Run 1,000 VMs without 1,000 license purchases | M02, M16 |
| Stable for years | Servers stay up for months between reboots | M20 |
| Small footprint | A server needs no desktop, so all RAM/CPU goes to the workload | M04, M27 |
| Scriptable everything | Every admin action can be automated — no clicking | M10–M11, M19 |
| Security model | Real multi-user permissions from the ground up | M12–M14 |
| Remote-first design | Administer 500 machines from one terminal over SSH | M22 |

## 5. The players: a 60-second history

- **1969 — Unix** is born at Bell Labs. Powerful, influential, expensive; runs on
  costly minicomputers. (Next lesson.)
- **1983 — GNU project** starts: build a free Unix-like OS. Delivers everything but
  the kernel.
- **1991 — Linus Torvalds**, a Finnish student, posts a hobby kernel to a Usenet
  group. People download it, fix it, extend it. The kernel + GNU = a complete,
  freely usable OS.
- **1993 — Debian** founded: a community distribution. Ubuntu will later grow from it.
- **2004 — Ubuntu** released by Canonical: Debian made easy, with a predictable
  release schedule. It is the course's platform.

The lesson of this history for you: Linux grew by **sharing**. Thousands of people
improved the kernel because the license allowed anyone to read, fix, and redistribute
the code. That licensing idea is the subject of Lesson 2.

## 6. What "free" means here (preview)

"Free" in free software means **freedom**, not price: the freedom to run, study,
modify, and share software. Free software can cost money; the point is that the
*source code* is open for inspection. For a data scientist this is not ideology —
it is practical: you can read how your tools work, fix them, pin exact versions for
reproducibility, and run the same stack anywhere without licensing friction.

## Exercises (answer in your lab-log.md)

1. In one sentence each, what are the four jobs of an operating system?
2. Strictly speaking, what is "Linux"? What is the broader everyday meaning?
3. What was the GNU project missing in 1991, and what filled the gap?
4. Name three places Linux runs and one reason it dominates each.
5. Your phone very likely runs the Linux kernel. Explain how that can be true even
   if it has no "Linux" branding anywhere.
6. Which of the six "why servers chose Linux" reasons do you think matters most for
   a university GPU cluster? Justify in two sentences.

## Check yourself before Lesson 2

- I can define *operating system*, *kernel*, *userland*, *distribution*, *GNU*.
- I can explain "Linux" (narrow) vs "GNU/Linux" (complete) vs "Ubuntu" (distribution).
- I can name two reasons Linux dominates cloud computing.

If any of these wobble, re-read Section 2–4 — these terms are used every single
week of the course.

## Further reading (official sources)

- The Linux Kernel documentation — <https://docs.kernel.org/>
- gnu.org: what is GNU? — <https://www.gnu.org/gnu/linux-and-gnu.en.html>
- Ubuntu: what is Ubuntu — <https://ubuntu.com/desktop>

Next: [Lesson 2 — Linux vs Unix & Open Source](02-linux-vs-unix-and-open-source.md)
