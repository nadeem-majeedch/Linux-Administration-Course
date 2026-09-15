# Lesson 4 — Linux Architecture

> Module 01 · Unit 1 · Difficulty: Beginner
> Reading time: ~25 min · Lab: [Lab 1 — Identify your system](../labs/lab-01-identify-your-system.md)
> Up next: [Lesson 5](05-shell-and-terminal.md)

---

## 1. The layers

Every GNU/Linux system, from a router to a GPU server, is a stack of layers. Draw
this once in your notes; you will refer to it all course:

```
┌──────────────────────────────────────────────┐
│  Applications        Jupyter, Python, Chrome │   user space
├──────────────────────────────────────────────┤
│  Shell & utilities   bash, ls, grep, awk     │
├──────────────────────────────────────────────┤
│  Libraries           glibc, OpenSSL          │
├══════════ system call interface ═════════════┤   ← the boundary
│  KERNEL              Linux: processes,       │   kernel space
│                      memory, devices, files, │
│                      networking, drivers     │
├──────────────────────────────────────────────┤
│  HARDWARE            CPU, RAM, disk, GPU, NIC│
└──────────────────────────────────────────────┘
```

- **Hardware:** the physical machine.
- **Kernel:** the supervisor that owns the hardware (Lesson 1). Decides which
  program runs, mediates every disk and network access, isolates programs from
  each other.
- **System call interface:** the narrow, well-defined door between the two worlds.
  Programs cannot touch hardware directly; they *ask* the kernel.
- **Libraries:** shared code (e.g., **glibc**, the GNU C library) that programs
  load instead of each reimplementing "open a file".
- **Shell and utilities:** the tools and the shell that runs them — your working
  environment for the whole course.
- **Applications:** the programs the user actually wanted: Python, Jupyter, a
  database, a browser.

## 2. User space vs kernel space

This is the architecture's central idea, and it exists to **protect**.

The CPU runs in (at least) two modes:

- **Kernel mode:** everything is allowed — real hardware access, any memory.
- **User mode:** the hardware itself forbids dangerous operations; attempts trigger
  a fault the kernel handles.

**User space** = everything running in user mode: your shell, Python, Jupyter, every
app. **Kernel space** = the kernel and its drivers, in kernel mode.

When a program needs something only the kernel may do — read a file, send a network
packet, allocate memory — it makes a **system call** (syscall): it hands the request
across the boundary and waits. The kernel performs the work *for* it, and returns the
result.

**Why the wall exists — three everyday payoffs:**

1. **Crash isolation.** A buggy Python script *cannot* crash the machine. Worst
   case, the script dies; the kernel shrugs and reclaims its memory. (Contrast with
   DOS-era home computers, where any program could hang the whole box.)
2. **Security.** A process can only touch what the kernel permits it to touch —
   your files, not other users'; your memory, not the password database. The entire
   permission system of Module 12 leans on this wall.
3. **Uniformity.** Every program reads disks through the same syscalls, so the
   kernel can present a USB stick, a cloud volume, and an NVMe drive the same way.

> **Mental model for DS people:** the kernel is the database server of the operating
> system, syscalls are its query API, user programs are clients. Clients never edit
> the database files directly; everyone benefits from one enforced, audited API.

**Rings.** You may read that x86 CPUs have more than two privilege levels ("rings"):
ring 0 = kernel, ring 3 = user; rings 1–2 are essentially unused on mainstream OSes.
Two rings is the level of detail you need.

## 3. "Everything is a file" — Unix's best trick

In Linux, almost anything worth reading or controlling appears in the filesystem as
a file — even when there is no disk involved:

| Path | What it really is | Course module |
|---|---|---|
| `/etc/hostname` | Plain-text config: the machine's name | M06–M07 |
| `/proc/cpuinfo` | A *window into the kernel's view* of your CPU — generated on read | M03 (now) |
| `/proc/meminfo` | Same for memory | M03, M18, M24 |
| `/dev/sda` | The first disk, as a file (careful!) | M17 |
| `/dev/null` | The bottomless pit: writing discards, reading gives nothing | M09 |

There is no special mechanism behind `/proc/cpuinfo`: a program simply *reads the
file*, and the kernel generates the content at that moment. One tool (`cat`) therefore
works on documents, device information, and kernel state alike — because to the
kernel, they are all files. This uniformity is why command-line text tools (Module 8–9)
can process *the system itself*.

## 4. Daemons: the always-running programs

A **daemon** is a program that runs in the background, usually started at boot,
with no window and no terminal — doing quiet continuous work. You benefit from
dozens right now:

| Daemon | Its quiet job | Module |
|---|---|---|
| `systemd` | PID 1 — starts and supervises every other daemon | M20 |
| `journald` | Collects all their logs | M24 |
| `sshd` | Waits for incoming SSH logins | M22 |
| `cron` / timers | Wakes jobs at scheduled times | M19 |
| `resolved` | Answers DNS lookups | M21 |

By convention, daemon names often end in `d`. They are normal user-space programs —
but long-lived ones. When a daemon misbehaves, you do not reinstall the OS; you ask
systemd what happened and read its logs (M20, M24). That is administration.

## 5. First contact: asking the machine about itself

Everything below is **read-only** — safe everywhere, including on shared machines.
Run these in your Ubuntu VM (set up in Lesson 8 / Lab 4). If you are reading before
installing, study the outputs; they are real examples you will reproduce.

**What kernel is running?**

```bash
uname -r
```

Expected output (yours may differ in version number):

```
6.8.0-45-generic
```

`-r` = *release*. Read it as: kernel version 6.8, patch 0, Ubuntu build 45, generic
flavor. `uname -a` adds architecture (`x86_64`), hostname, and build date.

**What distribution is this?**

```bash
cat /etc/os-release
```

Expected output (Ubuntu 24.04):

```
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.1 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
```

Read it like a data file, because it is one: `ID_LIKE=debian` tells you the family
(→ `apt`), `VERSION_ID` the release, `PRETTY_NAME` the human string. Scripts read
this file to behave distribution-aware — a pattern you will use yourself.

**What hardware am I on?**

```bash
lscpu | head -5
```

Expected output (trimmed — VM numbers vary):

```
Architecture:             x86_64
  CPU op-mode(s):         32-bit, 64-bit
  Address sizes:          39 bits physical, 48 bits virtual
  Byte Order:             Little Endian
CPU(s):                   2
```

```bash
free -h
```

Expected output (trimmed):

```
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       612Mi       2.1Gi        19Mi       1.1Gi       3.0Gi
Swap:          2.0Gi          0B       2.0Gi
```

`-h` = *human-readable* (GiB, not raw bytes) — a flag you will want on `df`, `du`,
`ls` too. `free` is your first monitoring command; in Module 18 it becomes diagnostic.

**Peeking through the /proc window:**

```bash
cat /proc/version
head -3 /proc/cpuinfo
```

Expected output (trimmed):

```
Linux version 6.8.0-45-generic (buildd@lcy02-amd64-…) (gcc …) #45-Ubuntu SMP …

processor	: 0
vendor_id	: GenuineIntel
cpu family	: 6
```

You just read *kernel-generated* files about a *virtual* CPU. Note what `cat` did
not do: it did not care that the file was not on a disk. That is "everything is a
file" working for you.

> **Where am I — VM or real?** `lscpu` on a VM often reveals the hypervisor
> (e.g., `Hypervisor vendor: KVM`). Try `lscpu | grep -i hypervisor` after Lab 4.

## 6. Why an architect's map pays a data scientist

- **Sizing machines** (cloud, cluster): the layers tell you what "2 vCPU, 4 GB RAM"
  means — hardware the kernel will apportion to user space, where your notebooks live.
- **Reading error messages:** "Kernel died" (Jupyter), "OOM killed" (M24), "killed
  by signal 9" (M18) are kernel-space events reaching your user-space eyes.
- **Debugging "works here, fails there":** different userlands (macOS `sed` vs GNU
  `sed`, M08) on the same ideas — the map tells you which layer to blame.
- **Containers in Module 28:** Docker containers *share the host kernel* and isolate
  user space. You cannot understand what a container is without this lesson.

## Exercises (lab-log.md)

1. Redraw the layer stack from memory. Mark where each lives: `bash`, Python,
   glibc, the kernel, Jupyter, `/etc/hostname`.
2. A classmate says: "My script crashed the whole computer." After Lesson 4, what
   is the most likely true explanation, and why can user-space code almost never
   do what they claim?
3. Explain a syscall to a non-programmer with a restaurant analogy (waiter? kitchen?).
4. `cat /etc/os-release` vs `cat /proc/cpuinfo` — one is a real file, one is
   generated. Why does the same command work on both?
5. In the `free -h` output above, what is the difference between *free* and
   *available* memory? (Take a guess now; verify in Module 18.)
6. Name three daemons that are running on your machine right now and what each is
   doing for you. (Hint: journald is definitely one.)
7. Why is "everything is a file" *convenient* for the text-processing work of
   Modules 8–9? Two sentences.

## Check yourself before Lesson 5

- I can draw the stack and place kernel, shell, libraries, applications.
- I can explain user space vs kernel space and name the boundary (syscalls).
- I can give two concrete protections the user/kernel wall buys me.
- I can run `uname -r`, `cat /etc/os-release`, `free -h` and read their outputs.

## Further reading (official sources)

- Linux Kernel documentation: overview — <https://docs.kernel.org/>
- man-pages: syscalls — <https://www.kernel.org/doc/man-pages/>
- proc(5) man page (`man 5 proc` in your VM) — the /proc filesystem documented

Next: [Lesson 5 — The Shell & The Terminal](05-shell-and-terminal.md)
