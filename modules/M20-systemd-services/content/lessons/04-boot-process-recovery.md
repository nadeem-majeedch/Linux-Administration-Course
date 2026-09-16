# Lesson 4 — Boot, Recovery & the System Identity Routine

> Module 20 · Unit 6 · Difficulty: Advanced
> Reading time: ~40 min · Lab: [Lab 2 — break & fix](../labs/lab-02-break-and-fix.md)
> Prerequisites: Lessons 1–3, [M17 storage](../../../M17-storage-and-filesystems/content/lessons/03-fstab-uuids-persistence.md)

> 🟡 **Safety tier:** boot *analysis* (`systemd-analyze`, `journalctl
> -b`) is safe everywhere. Recovery-mode practice happens in **your own
> VM** — that's also where you learn GRUB without fear, because VMs
> snapshot.

---

## 1. From power button to login prompt

The full chain, with the stage names you'll see in logs:

```text
1. Firmware (UEFI/BIOS)     — POST, picks the boot device
2. Bootloader (GRUB2)       — loads the kernel + initramfs, passes parameters
3. Kernel + initramfs       — drivers, mounts / (fstab pass-1!), starts PID 1
4. systemd                  — default target's unit graph, in dependency order
5. Getty / display manager  — the login you actually see
```

Two observations that connect earlier modules:

- **Step 3 mounts `/` using fstab** — M17's `pass 1` field, and why an
  fstab typo halts boot *before* systemd even runs (emergency shell,
  root read-only: `mount -o remount,rw /` then fix).
- **Step 4 is everything M20 has taught** — targets, wants, ordering.
  `systemd-analyze` makes the graph measurable:

```console
$ systemd-analyze                     # total boot time
Startup finished in 2.341s (firmware) + 1.802s (loader) + 3.117s (kernel) + 8.944s (userspace) = 16.204s
$ systemd-analyze blame | head -5     # slowest units (parallel boot ≠ sum!)
$ systemd-analyze critical-chain      # the dependency path that gated everything
```

`critical-chain` answers "why does boot *wait* on X" — always an
After=/Requires= from Lesson 1.

---

## 2. GRUB: the two-second intervention window

At boot, hold `Shift` (BIOS) or tap `Esc` (UEFI) in a VM console to get
the GRUB menu. The entries that matter:

- **Advanced options → recovery mode** — boots to a menu: `root` shell
  (as root, no password — *you* hold the machine, physically), fsck,
  dpkg repair.
- **Edit an entry (`e`)** — one-off kernel parameter changes: add
  `systemd.unit=rescue.target` to boot to rescue instead; `fsck.mode=
  force` to force a check; `nomodeset` for graphics trouble. `Ctrl-X`
  boots with your edits — **one boot only, nothing persists.**

The classic recovery combo (VM-only practice, once, deliberately):
boot → edit → `systemd.unit=rescue.target` → root shell → fix what
broke → reboot. Ten minutes of rehearsal turns the scariest failure
mode of a Linux box into a checklist. (Cloud VMs can't show you GRUB —
they offer *serial console* or "rescue mode" in the provider panel;
same ideas, different door.)

---

## 3. Boot journal: post-mortems without a Ouija board

Everything from firmware to login lives in the journal, tagged by boot:

```console
$ journalctl --list-boots             # every boot this machine remembers
  0 … current
-1 … previous boot
$ journalctl -b -1 -p err --no-pager  # last boot's errors (post-mortem!)
$ journalctl -b 0 -u ssh              # this boot, one unit
$ journalctl -k -b -1 | grep -iE "error|fail"   # kernel lines, last boot
```

`-b -1` is the workhorse: "the machine rebooted overnight, what
happened?" is one command, and it works even for the seconds *before*
userspace logging existed (kernel ring buffer is swept into the
journal).

---

## 4. The system identity & hardware routine

New box, first hour — the commands every admin runs, now assembled.
Think of it as the machine's passport control:

```console
$ hostnamectl                          # identity: hostname, OS, kernel, arch
 Static hostname: labvm
 Operating System: Ubuntu 24.04.2 LTS
 Kernel: Linux 6.8.0-52-generic
 Architecture: x86-64
$ sudo hostnamectl set-hostname ds-lab-01   # rename (own VM; see note)
$ hostnamectl status --transient hostname? no — just verify with `hostnamectl` again
$ uptime                               # load + how long since reboot
 10:42:07 up 2 days,  3:12,  2 users,  load average: 0.52, 0.48, 0.44
$ uptime -p                            # pretty: up 2 days, 3 hours
$ uname -r                             # kernel release alone
$ uname -a                             # everything, one line
```

(`hostnamectl set-hostname` edits `/etc/hostname` + notifies running
services — the modern replacement for hand-editing; also fix
`/etc/hosts` so sudo doesn't complain — M14 §6's resolution warning,
met again.)

**Hardware discovery** — the read-only inventory kit:

```console
$ lscpu                     # CPU: cores, threads, model, cache
$ lsblk                     # storage topology (M17 lesson 1 — your old friend)
$ free -h                   # RAM + swap
$ lspci | head              # PCI devices: GPU lines appear here! (VGA/NVIDIA)
$ lsusb                     # USB tree
$ sudo dmidecode -t system | head -12   # SMBIOS: vendor, model, serial (safest read)
$ cat /proc/cpuinfo | grep "model name" | head -1   # the /proc route (M18 echo)
```

For a DS student, `lspci | grep -i nvidia` is the first command on any
GPU server (does the box *have* the GPU before you debug CUDA?),
`lscpu` tells you whether your DataLoader's 16 workers make sense, and
`free -h` decides whether the 40-GB dataset loads or OOMs (M18 §5, one
more echo).

**The morning routine, distilled** (save this — it's Lab 2's opener):

```console
$ uptime && systemctl list-units --failed && df -h | grep -vE 'tmpfs|loop' && free -h
```

Four commands: is it up and sane, anything broken, disks OK, memory OK.
Every inherited server, every Monday morning, every incident triage —
this line goes first.

---

## 5. Time, timezone & clock sanity

```console
$ timedatectl                       # everything clock-related, one view
               Local time: Mon 2026-03-10 10:42:07 UTC
           Time zone: Etc/UTC (UTC, +0000)
       System clock synchronized: yes
               NTP service: active
$ sudo timedatectl set-timezone Europe/Berlin    # own VM
$ timedatectl set-ntp true          # ensure NTP sync (default on)
```

Time sanity is an operational prerequisite: TLS, cron windows, log
correlation across machines, Kerberos on university clusters — all
require coherent clocks. `timedatectl` showing "not synchronized" is a
real incident on real systems; knowing it exists is half the fix.

DS echo: experiment logs with *local* timestamps vs a server on UTC is
the classic "why do these intervals look wrong" puzzle — the course
datasets fake it deliberately (declare your timezone in every
timestamp, or use UTC everywhere).

---

## Exercises (lab-log.md)

1. Run the four-command morning routine. Paste output. Annotate one
   number you'd watch over time (load? disk%?) and why.
2. `systemd-analyze blame | head -8`: which unit costs the most, and
   is it actually *on the critical path*? (Compare with
   `critical-chain` — blame ≠ critical, and that's the lesson.)
3. `journalctl -b -1 -p err` on your VM. If this boot is your first
   (-1 doesn't exist), reboot once deliberately and then run it —
   what did the previous boot log that this one didn't?
4. In a VM console: interrupt GRUB, edit an entry to add
   `systemd.unit=rescue.target`, boot to rescue, log the experience,
   then `reboot` normally. What could you fix from there that you
   couldn't from a running system?
5. `lscpu | grep -E "^CPU\(s\)|Thread|Core"` — parse your CPU's
   socket/core/thread layout in one line. Would your next training
   script's `n_jobs` be set differently?
6. Identity: rename your VM (`hostnamectl set-hostname ds-lab-01`),
   fix `/etc/hosts`, verify a sudo command no longer warns, then
   rename it back. Two sentences: what did the rename touch?

## Check yourself before Lab 2

- [ ] I can narrate the five boot stages and say where fstab and
      systemd each act.
- [ ] I know GRUB's edit-a-boot trick and that it's one-shot.
- [ ] `journalctl -b -1` is my post-mortem reflex.
- [ ] The morning routine is written down and I've run it twice.

## Further reading (official sources)

- `man systemd-analyze`, `man journalctl`, `man hostnamectl`,
  `man timedatectl`, `man bootup` (systemd's boot sequence doc —
  excellent)
- freedesktop: https://www.freedesktop.org/software/systemd/man/latest/bootup.html
- GNU GRUB manual: https://www.gnu.org/software/grub/manual/
- Ubuntu Server Docs — console & boot: https://ubuntu.com/server/docs
