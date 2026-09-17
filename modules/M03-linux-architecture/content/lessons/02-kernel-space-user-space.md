# Lesson 2 — Kernel Space and User Space

> Module 03 · Unit 1 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 1](../labs/lab-01-anatomy-tour.md)
> Up next: [Lesson 3 — boot to shell](03-boot-to-shell.md)

---

## 1. The most important wall in the operating system

Modern CPUs run code in (at least) two privilege modes. Linux puts:

- **the kernel** in the privileged mode — *kernel space*
- **everything else** — every process you run, including your
  Jupyter notebook — in the unprivileged mode — *user space*

The point is protection: user code **cannot** touch hardware, other
processes' memory, or the raw disk. It must *ask* the kernel, through
a narrow doorway: the **system call** interface.

```
 user space:   python ── bash ── jupyter ── nginx     (unprivileged)
                  │         │         │        │
                  └────┬────┴────┬────┴────────┘
                       ▼    syscalls (open, read, fork, …)
 kernel space:  process scheduler · memory manager · VFS ·
                network stack · device drivers         (privileged)
```

## 2. What each side owns

| | Kernel space | User space |
|---|---|---|
| **Runs** | scheduler, memory manager, VFS, network stack, drivers | shells, utils, libraries, applications |
| **Crash effect** | kernel panic — machine stops | one process dies; system fine |
| **Memory** | sees all physical memory | sees only its own virtual address space |
| **Upgrade** | reboot (new kernel loaded) | replace a file, restart the process |
| **Debug tools** | dmesg, journalctl -k, crash dumps | strace, ltrace, gdb, logs |

That last row is the practical half of this lesson: when you
`journalctl -k` (M24), you're reading *kernel-space* speech. When you
`strace` a program, you're recording its *user-space → kernel-space*
requests.

## 3. The syscall, demonstrated

```console
$ strace -c python3 -c 'print(open("/etc/os-release").readline())'
```

Expect a tail like:

```
% time     seconds  usecs/call     calls    errors syscall
------ ----------- ----------- --------- --------- ----------------
 23.31    0.000445           4       112           mmap
 13.21    0.000252           3        87           read
  ...
  0.00    0.000000           0         3         1 openat
```

- Hundreds of syscalls **before** your line of code runs: loading the
  interpreter itself is boundary traffic.
- `openat` with `errors=1`: that's the loader probing for a library
  that isn't there — *failed* probes are normal.

**Read the trace like an admin:** each line is one request from user
space. `read` = "kernel, give me bytes." `mmap` = "kernel, map memory."
The wall is busy.

## 4. libc — the user's side of the doorway

Programs rarely issue raw syscalls; they call the **C library**
(glibc on Ubuntu), which wraps them (`fopen` → `openat`). That's why
`ldd /usr/bin/ls` shows `libc.so.6`: almost every user-space program
speaks to the kernel *through* it.

Consequence you already know from M02: Alpine's musl vs Ubuntu's
glibc changes *which prebuilt binaries run* — because the doorway's
user-side dialect differs.

**Safe demo (all read-only):**

```console
$ ldd /usr/bin/ls | head -3
$ ls -l /lib/x86_64-linux-gnu/libc.so.6   # note the version symlink
```

## 5. Why the wall is a *security* wall

- **Permissions live at the boundary.** `open()` is checked against
  the file's mode bits (M13) by the kernel, not by the program — a
  buggy program can't "forget" to check.
- **Isolation lives at the boundary.** Your process cannot read
  another user's memory. (Containers, M28, are this same idea productized:
  namespaces isolate *views*, cgroups cap *resources* — all enforced
  by the kernel on behalf of everyone.)
- **Privilege escalation** is the art of tricking the privileged side
  — why setuid binaries (M13) are audited, and why the daemon socket
  (M28's security lesson) is guarded like a root shell.

## 6. Kernel vs user space at a glance (DS scenarios)

| Symptom | Which side? | First evidence tool |
|---|---|---|
| Process segfaults | user space | `journalctl` shows the trap; rerun under `gdb`/`ulimit -c` |
| I/O hangs, `wa` high | boundary (syscall waiting) | `ps -o stat` shows `D` state |
| OOM kill | kernel decision, user-space victim | `journalctl -k -g oom` (M24) |
| Python imports wrong lib | user space | `strace -e openat`, `which python3` (M27) |

Rule of thumb: **if a *message* explains it, it's user space; if
only *behavior* shows it, suspect the kernel side** — then go get the
kernel's own words with `journalctl -k`.

---

**Key takeaways**

- Kernel space = privileged, shared, crashes are fatal; user space =
  sandboxed, per-process, crashes are local.
- Syscalls are the doorway; libc is the doorman; `strace -c` is the
  traffic census.
- Permissions and isolation are enforced *by the kernel* — programs
  cannot opt out, bugs cannot skip the check.

**Check yourself:** your notebook calls `pandas.read_csv` on a file it
can't read. Which side denies the request — pandas or the kernel? What
evidence would prove it?

**Next:** [Lesson 3 — boot to shell](03-boot-to-shell.md)
