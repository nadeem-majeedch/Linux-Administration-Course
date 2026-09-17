# Module 04 Troubleshooting — When Provisioning Goes Sideways

> Seven patterns from real install/VM sessions. Each: symptom →
> likely cause → diagnosis → fix → prevention. The VM makes all of
> these *safe to meet* — that's the point of having a lab.

## 1. VT-x/AMD-V not enabled ("virtualization support is missing")

**Symptom:** hypervisor refuses to start any VM; error mentions
VT-x/AMD-V/SVM.
**Cause:** virtualization disabled in firmware, or (Windows)
Hyper-V/VBS conflicts with VirtualBox.
**Diagnosis:** host-side — Task Manager → Performance → CPU →
"Virtualization: Enabled"; or `systeminfo`'s Hyper-V requirements.
**Fix:** enable SVM/VT-x in UEFI settings; on Windows hosts choose
*one* virtualization stack (WSL2 path uses Hyper-V; VirtualBox path
wants it off or recent VirtualBox using its Hyper-V API).
**Prevention:** check before the module, per SETUP.md.

## 2. Installer can't see the virtual disk

**Symptom:** "no disk detected" / empty partitioning list.
**Cause:** virtual disk not attached to a storage controller, or
wrong controller type for the ISO's kernel.
**Diagnosis:** VM settings → Storage — is the disk actually attached
(SATA/NVMe)? 
**Fix:** attach it, reboot installer.
**Prevention:** Part B gate — record settings *before* boot.

## 3. Boots to `grub>` after successful install

**Symptom:** after "reboot", you land at a `grub>` prompt.
**Cause:** the install ISO is still attached and outranks the VM's
disk; or disk boot order wrong.
**Diagnosis:** M03 knowledge — check VM boot order; is the ISO still
"inserted"?
**Fix:** remove ISO from the virtual drive (or uncheck boot-from-
optical), reboot.
**Prevention:** unmount the ISO at the end of install, every time.

## 4. No IP address / "network unreachable" on first login

**Symptom:** `ip -brief address` shows the NIC with no address.
**Cause:** NAT service hiccup, or cable "disconnected" in VM
settings, or Netplan config typo if you hand-edited.
**Diagnosis:** `ip -brief link` (is the NIC UP?); VM settings →
network adapter connected?; `journalctl -b -u systemd-networkd`.
**Fix:** reconnect the adapter; `sudo netplan apply` only if you
changed config (M21 teaches it properly).
**Prevention:** leave networking at defaults until M21.

## 5. `sudo: unable to resolve host` warnings

**Symptom:** every `sudo` prints a resolve warning, then works.
**Cause:** hostname was changed (Lab or curiosity) but `/etc/hosts`
still has the old name.
**Diagnosis:** `hostname` vs `grep $(hostname) /etc/hosts`.
**Fix:** add the current hostname to `/etc/hosts`' 127.0.1.1 line
(M21 explains why resolution touches this file first).
**Prevention:** when renaming a host, rename it in both places —
M29-ext A's provisioning script does exactly this, in one logged
transaction.

## 6. Verification failures on the ISO

**Symptom:** `FAILED` in `sha256sum -c`, or signature *bad*.
**Cause:** truncated download (most common), wrong manifest for that
ISO, or an untrustworthy source.
**Diagnosis:** compare your ISO's computed hash to the manifest line
*by hand* once — see the actual difference; check file size against
the official page.
**Fix:** delete, re-download from a different official source,
re-verify. Signature *bad* (not just uncertified): stop, treat the
source as suspect, report it.
**Prevention:** download ISO + manifest + signature together, from
the same official directory.

## 7. Snapshot revert leaves the VM unbootable

**Symptom:** after revert, boot fails or behaves oddly.
**Cause:** typically a delta-chain inconsistency (snapshot deleted
while VM running/suspended) — or you reverted to a snapshot taken
*mid-write* during a suspended state.
**Diagnosis:** hypervisor's log for the VM; does the last snapshot
predate the suspend?
**Fix:** revert to the older `clean-install-…` (this is exactly why
the two-snapshot policy exists), re-apply from your notes — the reset
procedure you wrote is now earning its keep.
**Prevention:** snapshot only while powered off; keep `clean-install`
forever.
