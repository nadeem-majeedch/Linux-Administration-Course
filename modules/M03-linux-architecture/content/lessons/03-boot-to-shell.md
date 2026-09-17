# Lesson 3 — Boot to Shell: the Four-Act Play

> Module 03 · Unit 1 · Difficulty: Intermediate
> Reading time: ~25 min · Lab: [Lab 2](../labs/lab-02-grub-intervention.md)
> Up next: [Lesson 4 — user-space anatomy](04-userspace-anatomy.md)

---

## 1. The four acts

Every boot is the same play, whatever the distro:

```
FIRMWARE (UEFI/BIOS)  →  BOOTLOADER (GRUB2)  →  KERNEL + initramfs  →  INIT (systemd)
   self-test, picks        loads kernel from      unpacks drivers,      PID 1 starts
   a boot entry            disk into memory       mounts real root      units → login
```

- **Act 1 — Firmware.** Power-on self-test, detects disks, runs the
  boot entry (UEFI: reads the EFI System Partition; BIOS: reads the
  disk's first sectors). Knows nothing about Linux.
- **Act 2 — Bootloader (GRUB2 on Ubuntu).** Shows the menu (hold
  Shift, or tap Esc on UEFI), loads the kernel image and a small
  helper archive, the **initramfs**, into memory.
- **Act 3 — Kernel + initramfs.** The kernel takes the CPU, then runs
  the initramfs' init: load storage drivers, find the real root
  filesystem by UUID, mount it, hand over to its init.
- **Act 4 — Init = systemd, PID 1.** Starts units in dependency order
  (`systemd-analyze` shows the timings), spawns `getty`/display
  manager → login → your shell. Every later boot question is a
  systemd question (M20).

## 2. Reading the play after the curtain

The system remembers the boot in three places:

```console
$ systemd-analyze                    # total time, split by act
$ systemd-analyze blame | head       # which units ate Act 4
$ journalctl -b -p err               # this boot's errors, boot-scoped
$ journalctl -b -u systemd-modules-load.service   # one unit's side
```

`-b` ("this boot") is the boot-to-boot fence you'll use all course:
before it, only previous boots; after it, only this one.

**Kernel's own words:** `journalctl -k -b` shows only kernel messages
from this boot — driver probes, filesystem checks, the GPU handshake.
When a machine "boots but something's wrong", this is Act 3's script.

## 3. Interruptions: what "recovery" means at each act

| If this fails… | You see… | First moves |
|---|---|---|
| Firmware | no video/beeps | hardware layer — out of scope for the OS, note it and stop |
| GRUB | `grub>` prompt | you're at a mini-shell: `ls` lists GRUB's view of disks; a repair needs a live ISO (M04's rescue boot) |
| Kernel/initramfs | panic, or "dropped to initramfs shell" | often storage: wrong `root=`/UUID, missing driver. The initramfs shell *is* the recovery tool |
| systemd | boot stalls on jobs | the boot log names the unit; recovery is a unit fix (M20) + emergency.target |

The key administration habit: **locate the act** before acting. A
"server won't boot" ticket is four different playbooks depending on
where the curtain fell.

## 4. The one intervention every admin should do once

Deliberately interrupt GRUB (Lab 2 walks it on your VM):

- At the menu, press `e` — you see the kernel command line: `linux
  /boot/vmlinuz-… root=UUID=… ro quiet splash`. Those parameters are
  Act 3's stage directions. Boot once with them as-is (`Ctrl-x`) and
  confirm via `cat /proc/cmdline` that what you saw is what ran.
- The famous recovery use — appending `systemd.unit=rescue.target` —
  gives a single-user root shell for repairs (password resets, fsck).
  *Why it works:* you're overriding Act 4's first decision, before
  normal targets bring up networking or logins.

Understanding this beats memorizing it: the menu is a *text editor
for one boot*, and it resets at the next boot. Nothing you type there
persists — which is what makes it safe to learn.

## 5. DS connection: the machine that boots but isn't yours

On a shared ML server, "I rebooted it" is never trivial — Act 4 must
re-start *everyone's* services, and `systemd-analyze blame` plus
`journalctl -b -p err` is how a reviewer checks that a reboot was
clean. When your capstone server reboots, the grading question is
exactly this lesson: did every unit come back, and what does this
boot's log say it did?

---

**Key takeaways**

- Four acts: firmware → bootloader → kernel+initramfs → init.
- `systemd-analyze`, `journalctl -b`, `journalctl -k -b` are the
  post-curtain evidence tools; `-b` fences each boot.
- Recovery = locating the act. GRUB's `e`-editor changes one boot
  only — safe to practice.

**Check yourself:** a colleague's box shows `grub>` after a power
cut. Which act failed, and why is "just reinstall" the wrong first
move?

**Next:** [Lesson 4 — user-space anatomy](04-userspace-anatomy.md)
