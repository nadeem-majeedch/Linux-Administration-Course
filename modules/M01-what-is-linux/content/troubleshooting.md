# Module 01 — Troubleshooting Guide

The ten failure points that actually happen at this stage, with causes and fixes.
Diagnosis order matters: **read the exact error text first** — most answers are in
the words you're about to scroll past.

---

## 1. "VT-x is disabled in the BIOS" (VirtualBox won't start the VM)

**Meaning:** your CPU's virtualization hardware assist is switched off in firmware.
VirtualBox needs it (on most hosts) to run 64-bit guests at usable speed.

**Fix:**
1. Reboot the host; enter BIOS/UEFI (usually Del, F2, or F12 at the vendor splash).
2. Find *Intel VT-x / Virtualization Technology* (Intel) or *SVM Mode* (AMD) —
   typically under Advanced / CPU Configuration / Security.
3. Enable → Save & Exit → boot host → retry the VM.

**If it still fails:** some hosts reserve VT-x for Hyper-V/WSL2 conflicts on Windows —
see SETUP.md's troubleshooting table (VirtualBox vs Hyper-V coexistence settings).

## 2. VM is unbearably slow

**Diagnose:** host RAM available? Other VMs running? 1 CPU allocated?

**Fix ladder:** close heavy host apps → give the VM 2 CPUs (never more than half
the host's cores) → 4 GB RAM → install Guest Additions (SETUP.md §A5) → check the
disk file is on an SSD, not a network drive. A course VM does not need more than
that; if it still crawls, the host is the bottleneck, not Linux.

## 3. ISO boots to a black screen or "no bootable device"

**Causes, in order of likelihood:** the ISO isn't attached to the optical drive;
the ISO download was corrupted (checksum!); the VM's EFI setting doesn't match
(leave EFI off for standard Ubuntu Desktop 24.04 unless the tutorial you followed
says otherwise).

**Fix:** VM Settings → Storage → confirm the ISO is in the drive; re-verify
checksum; retry. Last resort: re-download from ubuntu.com.

## 4. "This site can't be reached / apt update fails" inside the VM

**Meaning:** the VM has no working network path yet.

**Fix:** VM Settings → Network → Adapter 1 → **Attached to: NAT** (the default;
NAT lets the guest share the host's connection). Restart the VM, then in the guest:

```console
$ ping -c 2 ubuntu.com
```

Two replies = fixed, retry `sudo apt update`. Still failing on university networks?
Some campus networks require proxy settings — ask your instructor for the proxy
URL, apt honors it via `/etc/apt/apt.conf.d/` (M16 covers this properly).

## 5. Wrong keyboard layout (passwords "fail" at login)

**Meaning:** you typed the right password on the wrong layout — classic with
non-US layouts chosen incorrectly at install, or after switching host keyboard.

**Fix:** at the login screen, use the layout indicator (top-right) to switch
layouts, or type the password in the username box first to *see* what it becomes.
Permanent fix: Settings → Keyboard → add/remove layouts, set the default.

## 6. Terminal opens but commands print "command not found"

**Read the message exactly:** `bash: treee: command not found` — you mistyped the
command name. That is the *normal* response to unknown words.

**Fix ladder:** check spelling (`treee` vs `tree`) → Tab-complete instead of
typing full names → if the spelling is right, does the command exist on this
system? (`type tree` says "not found"; many tiny systems lack optional tools until
installed — M16's job.) Nothing in Module 01 requires installed extras; everything
you need is on a standard Ubuntu desktop.

## 7. `sudo` asks for a password and typing shows nothing

**Meaning:** nothing is broken. Linux hides password input entirely — no asterisks,
no movement, by design (the length would leak information).

**Fix:** type confidently, press Enter. If it genuinely fails three times, your
password differs from the install-time one (keyboard layout? Caps Lock? WSL2 has a
separate password from Windows — did you mix them?). WSL2 password reset procedure
is in SETUP.md's troubleshooting table.

## 8. `man: command not found` or "No manual entry for X"

**Cause A:** a minimal system (some WSL2 images, servers, containers) ships without
the man-page database. `sudo apt install man-db` fixes the tool; `sudo apt install
manpages-posix manpages` adds content sets.

**Cause B:** "No manual entry for X" for a *specific* X — the page genuinely isn't
installed for that tool (common for GUI apps) or the name is wrong. Try
`man -k <fragment>` to find what *is* documented; use `--help` meanwhile.

## 9. The terminal "froze" (prompt not coming back)

**Meaning:** a command is still running — not a crash. Did you start something
(ping without `-c`, a pager inside another)?

**Fix:** **Ctrl+C** first. If the screen looks garbled afterwards, run `reset`
(yes, a real command that redraws a sane terminal). If Ctrl+D accidentally logged
you out — that's Ctrl+D's job (end of input); log back in; nothing was lost.

## 10. WSL2-specific surprises

- **`systemctl` says "System has not been booted with systemd"** → your WSL2 is
  running without systemd: add to `/etc/wsl.conf` under `[boot]` the line
  `systemd=true`, then from *PowerShell*: `wsl --shutdown` and reopen Ubuntu.
  (Needed only for later modules; Lesson 8 explains the seams.)
- **Files "disappear" between sessions** → they don't; check `pwd`. WSL2 reopens
  in the directory you left (or in `~` after an update — behavior is configurable).
- **Windows files unreachable** → they live under `/mnt/c/...`; `ls /mnt/c` proves it.
- **Everything networking fails after Windows sleep** → from PowerShell:
  `wsl --shutdown`, then reopen; it rebuilds the virtual network.

---

## When nothing here helps

1. Write down the *exact* command and *exact* error text (you have the `lab-log.md`
   habit — this is why).
2. Re-run the identity block (`whoami`, `hostname`, `uname -srm`, `cat /etc/os-release`).
3. Bring both to the course forum/office hours — a question with evidence gets
   answered in minutes; "it doesn't work" takes days. That evidence habit *is*
   Module 24's incident discipline, started early.
