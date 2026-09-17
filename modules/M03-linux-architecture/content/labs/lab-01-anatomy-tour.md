# Lab 1 — The Anatomy Tour

> Module 03 · Unit 1 · Difficulty: Beginner → Intermediate · Est. time: 40 min
> Environment: your own VM/WSL2. **Every command is read-only.**
> Goal: produce an evidence sheet of your machine's architecture —
> one command per layer, one sentence of interpretation each.

## Setup

```console
$ mkdir -p ~/lab03 && cd ~/lab03
$ script anatomy.txt        # record the session; exit with Ctrl-d
```

## Station 1 — Firmware/bootloader traces (5 min)

```console
$ ls /sys/firmware/efi 2>/dev/null && echo "UEFI boot" || echo "legacy/BIOS or container"
$ [ -d /sys/firmware/efi/efivars ] && ls /sys/firmware/efi/efivars | head -3
```

Write: did this machine boot UEFI or legacy? (In WSL2 you'll see the
"or" branch — note why: the kernel runs against a synthetic
firmware-less platform.)

## Station 2 — Kernel identity (5 min)

```console
$ uname -r && uname -v
$ cat /proc/cmdline               # Act 3's stage directions
$ cat /proc/version               # compiler + build info
```

Write: which act wrote `/proc/cmdline`, and who read it?

## Station 3 — The kernel's ledger: procfs (10 min)

```console
$ head -3 /proc/meminfo           # memory manager speaks
$ cat /proc/loadavg               # scheduler speaks (M24 decodes this)
$ head -3 /proc/cpuinfo | grep -E 'model name|processor'
$ cat /proc/sys/kernel/hostname
```

Write: which *subsystem* of the kernel owns each file? (Map each to
the Lesson 2 table.) Note that `sysctl` settings live under
`/proc/sys` — read-only today.

## Station 4 — Hardware census: sysfs (5 min)

```console
$ ls /sys/class/net/              # NICs the kernel found
$ ls /sys/block/                  # block devices (M08 revisits)
$ ls /sys/class/ | head           # the device-class index
```

Write: how many NICs, and what are they named? (`lo` counts — say
what it is, M21 will prove it.)

## Station 5 — User-space anatomy (10 min)

```console
$ type -a python3; readlink -f "$(command -v python3)"
$ file "$(command -v bash)"
$ ldd "$(command -v bash)" | head -5
$ strace -c bash -c 'ls / >/dev/null' 2>&1 | tail -8
```

Write: (a) the full symlink chain behind `python3`; (b) the three
libraries bash always maps; (c) the top three syscalls in the census
and which lesson-4 actor issued them.

## Station 6 — PID 1 and the service layer (5 min)

```console
$ cat /proc/1/comm
$ systemctl is-system-running
$ systemctl --no-pager --failed
```

Write: what is PID 1, and is Act 4 healthy right now?

## Deliverable

`anatomy-report.md`: for each station, the command(s), their one-line
interpretation, and — the graded part — **a drawn diagram** (ASCII
fine) of *your* machine's stack with the evidence file annotated at
the layer it proves. End with the boundary count: how many
user↔kernel crossings did Station 5's `ls` make, roughly?

## Troubleshooting

- `strace: command not found` — `sudo apt install strace` (pure
  read-only tracer, safe: it only *watches*).
- `/sys/firmware/efi` missing in a container — expected; containers
  boot nothing, they reuse the host kernel. Say so in the report.
- `systemctl` errors in WSL2 — systemd may be disabled; check
  `/etc/wsl.conf` `[boot] systemd=true` (SETUP.md covers this) and
  note the state instead of forcing it.
