# Module 03 Quiz — Answer Key

> Grade the *reasoning*, not exact wording. A correct command with a
> wrong reason scores half; the reverse — wrong command, right
> mechanism — scores a discussion.

## Section A

**Q1.** Hardware → firmware → bootloader → kernel → libraries →
shell/utilities → applications. Sample placements: firmware–`lsblk`?
No — accept: kernel (`uname`, `free`, `ip`), libraries (`ldd` reads
them; `python3` maps them), shell (`bash`, `ls`, `grep`),
applications (`jupyter`, `git`, `docker`), bootloader/firmware
(boot-time only; no run-time command lives there — a good answer says
so).

**Q2.** Python (user space) → stdlib/`io` → libc wrapper → **syscall
`write`** (the wall) → kernel VFS → ext4 driver → block/disk driver →
disk (virtual, in a VM). Final toucher: the **block device driver**
acting on the kernel's behalf. Partial credit for stopping at "the
kernel" — the point is naming *which part* of it.

**Q3.** Layers talk only to neighbors, and the kernel's *contract* to
user space (syscalls + libc ABI) is stable — so any user space that
speaks it runs on it. The reverse fails because user space has no
stable hook into the privileged world; replacing the kernel swaps the
CPU's privileged tenant mid-flight, impossible without restarting the
machine.

**Q4.** Provided by the kernel (VFS: one file interface over
regular files, procfs, sysfs); consumed by user space. `/proc/cpuinfo`
is the kernel *generating* file content on read — no bytes exist on
any disk; `/home`'s file is the ext4 driver answering from a real
medium. Both present the same `read()` face.

**Q5.** Framework (PyTorch) → CUDA toolkit (runtime libraries) →
driver (kernel module + user-space driver) → hardware (GPU). The
driver layer straddles the wall — part kernel module. That's why
mismatches bite: framework and toolkit negotiate in user space, then
must both speak to *one* kernel driver.

## Section B

**Q6.** The **kernel** — mode bits are checked inside `open()`'s
implementation, in privileged space. It must be the kernel because
user space is untrusted by design: any check a buggy program performs
it could also skip. Security policy enforced at the wall can't be
opted out of.

**Q7.** Notebook: that process dies, others continue, system healthy —
evidence: shell message/`journalctl` user-scope. Kernel bug: **panic**
— everything stops; evidence: `journalctl -k -b` from the *previous*
boot, console scrollback, crash dump. The asymmetry (isolation) is
the design win.

**Q8.** Syscall: the controlled entry point where user code asks the
kernel for a service. libc: the shared library wrapping raw syscalls
into portable C functions. Alpine speaks a *different dialect*
(musl vs glibc) on the user side of the same wall — binaries linked
against one won't load on the other.

**Q9.** Before `main` runs: the dynamic loader must map the
interpreter and its libraries — each `open`/`mmap`/`read`/`close` of
an `.so` is a boundary crossing; symbol resolution; locale/stdio
setup. Python also imports its startup modules. Traffic scales with
*how much machinery loads*, not with your one line.

**Q10.** It's blocked *inside* a kernel syscall it cannot abort —
typically uninterruptible storage I/O (`D` = waiting on the kernel/
hardware side). `SIGKILL` is delivered by the kernel but can't be
acted on by a task that isn't scheduled; killing is only possible
once the syscall returns. Fix the I/O, not the process.

## Section C

**Q11.** Firmware: self-test, finds a boot device, runs the loader.
Bootloader: loads kernel + initramfs into memory, passes the command
line. Kernel+initramfs: gains the CPU, loads storage drivers, mounts
the real root, execs its init. Init (systemd): starts units in
dependency order, brings up targets, spawns logins.

**Q12.** Act 3 fails to mount the real root: the initramfs carries the
storage drivers and the mount-then-switch-root logic; without it the
kernel may lack the disk driver entirely and has no root to exec init
from → panic or initramfs shell. It exists to bridge "kernel knows
nothing yet" → "root filesystem available".

**Q13.** It lives in RAM — GRUB handed the kernel a *memory-resident
argument list* this boot only. The mechanism restoring normality:
the bootloader re-reads its on-disk configuration next boot; nothing
was written to disk.

**Q14.** Userspace (22s of 27s) — Act 4. `systemd-analyze blame`
ranks units by activation time; cross-check `journalctl -b -p err`
for the slow ones that *also* erred.

**Q15.** `-b` fences this boot's evidence from history — without it
you read last week's errors too. `-p err` lifts the signal from the
noise. Together: "what did *this* boot fail at", which is the actual
question; bare `journalctl` answers "what has ever failed", which
invites theory before evidence.

## Section D

**Q16.** Shell (parse) → `$PATH` lookup (shell/kernel? — shell asks
the kernel to exec) → dynamic loader → shared libraries → the
program's `main`. `command not found` is the **shell's** verdict
after the PATH search fails.

**Q17.** Economically: one read-only copy mapped into many processes —
RAM is paid once. Risk: it's a single point of update — replacing the
file changes behavior for every tenant at once; running processes
keep old mappings, so versions diverge until restart. M16's rule:
update as one consistent set.

**Q18.** The old mapping: the kernel holds the inode open; deletion/
replacement creates a new file, but running processes keep paging
from the old one until restart. Evidence: `ls -l` shows the new file;
`/proc/<pid>/maps` still resolves the old path's inode (or a
`(deleted)` suffix).

**Q19.** No loader, no `.so` lookups — the binary carries its
libc/toolkit; library security updates do **not** reach it until it's
rebuilt. You want it for tiny rescue tools, containers' `busybox`
style utilities, or hostile/unknown environments — and you accept the
rebuild-for-CVE cost.

**Q20.** Still `python3.12` — bare `python3` was resolved by the
**shell** (PATH + symlink chain) at invocation, and the chain points
at 3.12. Installing 3.13 adds files but edits no symlink. The actor:
the shell's PATH lookup + the symlink the distro maintains. Changing
the answer requires changing PATH or the symlink — M27's territory,
now explained mechanically.
