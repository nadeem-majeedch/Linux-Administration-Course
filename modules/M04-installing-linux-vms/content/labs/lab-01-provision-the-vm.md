# Lab 1 — Provision the Lab VM, with Evidence

> Module 04 · Unit 1 · Difficulty: Beginner · Est. time: ~90 min
> Environment: your host machine (hypervisor of choice) + the new VM.
> ⚠️ The only destructive act is the installer erasing the **VM's
> virtual disk** — double-check every dialog names the *virtual*
> disk, never a host drive. On a host with one disk this is easy; on
> a dual-boot machine, be paranoid about the disk selection screen.

## Objective

Build the course's laboratory with recorded evidence at every gate —
and prove the snapshot/restore cycle works before you ever need it
under pressure.

## Part A — Download & verify (15 min + download)

1. From the official Ubuntu release server, fetch: the latest **LTS
   Server** ISO for your architecture, plus `SHA256SUMS` and
   `SHA256SUMS.gpg` from the same directory.
   > **Desktop-ISO students (SETUP.md Path B):** everything in this lab
   > works with the Desktop ISO too — the same `SHA256SUMS`/
   > `SHA256SUMS.gpg` files sit beside the Desktop download on
   > releases.ubuntu.com, and the installer differs only in looks.
   > The verify step itself is identical.
2. Verify integrity, then authenticity (M02 Lab 2 procedure):

```console
$ sha256sum -c SHA256SUMS 2>&1 | grep -iE '\.iso|FAILED'
$ gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys <KEYID-from-ubuntu.com>
$ gpg --verify SHA256SUMS.gpg SHA256SUMS
```

**Gate 1:** paste the `OK` line and the `Good signature` + warning
lines into your lab log. Resolve the trust warning via the official
fingerprint, note that you did.

## Part B — Provision (10 min)

Create the VM per Lesson 2's table: 2 vCPU · 4 GiB · 25 GiB
dynamically-allocated disk · NAT · Ubuntu 64-bit profile. Attach the
ISO to the virtual optical drive. **Gate 2:** record the VM's exact
settings in your log before first boot.

## Part C — Install (30–45 min)

Run the installer with Lesson 2's annotated answers. Non-negotiables:

- **entire virtual disk** (read the confirmation screen twice)
- profile: username `ds` (or your choice), strong password
- **Install OpenSSH server: YES**
- no snaps

First login, then the day-one circuit:

```console
$ sudo -v && whoami
$ ip -brief address
$ systemctl --no-pager --failed
$ df -h /
$ hostnamectl
```

**Gate 3:** all five outputs in your log. Zero failed units expected;
investigate anything else now.

## Part D — Snapshot & the controlled revert (15 min)

1. Shut down cleanly; take snapshot `clean-install-<date>`.
2. Boot, then make the mess:

```console
$ sudo apt-get update && sudo apt-get install -y sl
$ touch ~/mess.txt
$ ls ~/mess.txt && command -v sl        # both exist
```

3. Power off; **revert** to `clean-install-<date>`; boot.
4. Prove the restore: `ls ~/mess.txt` (gone) and `command -v sl`
   (absent).

**Gate 4:** the before/after evidence pair, and the snapshot name +
timestamp, in your log.

## Part E — Document (10 min)

Write `lab-environment.md` (Lesson 4 §5 template): host, VM specs,
user, snapshot inventory, reset procedure. This file follows you to
the capstone — start it properly.

## Troubleshooting

- **Installer can't see the disk:** 25 GiB is below some defaults'
  comfort; confirm the virtual disk was actually created and attached
  (SATA), not just configured.
- **No IP address:** NAT is default — check the VM's network setting
  is NAT/`enp0s3`-class NIC present via `ip -brief address`.
- **ISO boots to grub prompt after install:** the installer medium is
  still attached and outranks the disk — unmount the ISO, reboot.
- **`gpg` can't reach the keyserver:** campus proxy? Use
  `gpg --keyserver hkps://keyserver.ubuntu.com` explicitly or fetch
  the key from ubuntu.com's page and import from file.
