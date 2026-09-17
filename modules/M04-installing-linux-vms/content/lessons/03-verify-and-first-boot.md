# Lesson 3 — Verify the Download and Read the First Boot

> Module 04 · Unit 1 · Difficulty: Beginner
> Reading time: ~20 min · Lab: [Lab 1](../labs/lab-01-provision-the-vm.md)
> Up next: [Lesson 4 — snapshots and reset discipline](04-snapshots-and-reset-discipline.md)

---

## 1. Why verification is not optional ceremony

Every year, mirrors are compromised, uploads are truncated, and
torrents lie. The install ISO is the *root of trust for your entire
lab* — a tampered ISO gives you a perfectly working system that
answers to someone else. M02 gave you the theory (integrity vs
authenticity); this is its application with real stakes.

The Ubuntu project publishes, alongside each ISO:

- `SHA256SUMS` — the integrity manifest
- `SHA256SUMS.gpg` — a signature over that manifest (authenticity)

Both live on the official `cdimage`/`releases` servers. Download
**both plus the ISO** before provisioning.

## 2. The verification, end to end

```console
$ cd ~/downloads
$ sha256sum -c SHA256SUMS 2>&1 | grep -E 'ubuntu.*iso|FAILED'
ubuntu-24.04.2-live-server-amd64.iso: OK
$ gpg --keyserver hkps://keyserver.ubuntu.com --recv-keys 0x46181433FBB75451  # example ID
$ gpg --verify SHA256SUMS.gpg SHA256SUMS
gpg: Good signature from "Ubuntu CD Image Automatic Signing Key ..."
gpg: WARNING: This key is not certified with a trusted signature!
```

Reading the three outcomes honestly:

- `OK` — the ISO is byte-for-byte what the manifest listed.
- `Good signature` + the **warning** — the signature is mathematically
  valid, but you haven't yet told GPG you *trust that this key is
  Ubuntu's*. Resolve it the honest way: check the key fingerprint on
  ubuntu.com's own pages, then `--lsign-key` it. The warning is the
  web-of-trust step, not an error.
- `FAILED` — stop. Delete, re-download from a different official
  source, re-verify. Never install from a failed verification.

**Record all three outcomes in your lab log.** "I verified it" is a
claim; the three lines above are evidence — the distinction the whole
course runs on.

## 3. First boot as a M03 field trip

You watched the four acts in theory; now watch them on a machine you
built. On the first login, run the boot-reading trio:

```console
$ systemd-analyze
Startup finished in 2.341s (firmware) + 1.208s (loader) + 4.872s (kernel) + 11.003s (userspace) = 19.424s 
$ systemd-analyze blame | head -5
$ journalctl -b -p err --no-pager
```

Interpret like an administrator:

- **firmware/loader seconds** — the VM's BIOS-and-GRUB act; VMs are
  faster than physical firmware because there's no hardware inventory
  to walk.
- **kernel seconds** — Act 3; includes initramfs unpacking drivers.
- **userspace** — Act 4; `blame` ranks the suspects. On a fresh
  install, expect `systemd-journal-flush`, networking, sshd among the
  heavier units — all normal.
- **zero err lines** is the definition of a clean boot. (If you see
  some — read them now; day-one errors are the cheapest to fix and
  the best practice.)

## 4. Identity evidence for your notes

Three commands that answer "what machine is this, exactly?" — the
opening moves of every future incident:

```console
$ cat /etc/os-release | head -2      # distro + version (M02)
$ uname -r                            # kernel series (M03)
$ hostnamectl                         # hostname, chassis, virtualization: kvm
```

Note `Virtualization: kvm` (or `oracle` under VirtualBox): the system
*knows* it's a VM, and M31's remote-server work will lean on this
self-knowledge. Record all three outputs in `lab-environment.md` —
that file, started today, follows you to the capstone.

## 5. When verification fails (the real skill)

Two failure shapes, two responses:

- **Checksum `FAILED`:** byte-level mismatch — truncated download or
  a lying mirror. Response: delete, re-fetch from a *different*
  official source, re-verify. One re-download is normal; a second
  failure from the same source is a finding worth reporting.
- **Signature doesn't verify at all:** either you fetched the wrong
  signature file, the download corrupted it, or — rare and serious —
  the source isn't what it claims. Response: stop before installing;
  cross-check against the fingerprint published on ubuntu.com.

The discipline generalizes to everything you'll ever install: Python
packages (pip's hash-checking, M27), container base images (digest
pinning, M28), datasets from collaborators (M31). The ISO is just the
first, largest, most consequential artifact you'll verify.

---

**Key takeaways**

- ISO first, `SHA256SUMS` + signature with it; verify *before* the
  hour-long install.
- `Good signature` with a trust *warning* is normal on a fresh
  keyring — resolve it via the official fingerprint.
- First boot is a M03 field trip: `systemd-analyze`, `blame`,
  `journalctl -b -p err`; log the outputs as day-one evidence.

**Check yourself:** you verified the checksum but skipped the
signature. What attack does that leave open, and what does M02 call
the difference?

**Next:** [Lesson 4 — snapshots and reset discipline](04-snapshots-and-reset-discipline.md)
