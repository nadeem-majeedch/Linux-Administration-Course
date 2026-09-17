# Lesson 1 — Why a Lab, Not a Laptop

> Module 04 · Unit 1 · Difficulty: Beginner
> Reading time: ~15 min · Lab: [Lab 1](../labs/lab-01-provision-the-vm.md)
> Up next: [Lesson 2 — provision the VM](02-provision-the-vm.md)

---

## 1. The license to break things

Every skill in this course was learned by someone breaking a system:
a wrong `chown`, a full disk, a broken fstab, a firewall that locked
them out. On your daily-drive laptop, that tuition is unaffordable.
On a **virtual machine**, it's free: the damage is contained to a
sandbox, and a *snapshot* returns you to the pre-disaster state in
seconds.

Three properties make a VM the right laboratory:

| Property | What it buys you |
|---|---|
| **Isolation** | mistakes can't touch your host files, host network, or other people |
| **Reset** | snapshots restore known-good states in seconds (Lesson 4) |
| **Fidelity** | it's a *real* Linux — real kernel, real systemd, real root — unlike a web terminal |

A web terminal teaches typing; a VM teaches *administration* — the
difference is consequences, and the VM gives you consequences you can
undo.

## 2. WSL2: when it fits, when it doesn't

**WSL2** runs a real Linux kernel alongside Windows — excellent for
the command-line modules (M05–M12, M19, M27), and it integrates with
Windows files and your editor beautifully.

Where it is *not* the same as a VM:

- No firmware/bootloader theatrics (M03's Lab 2 needs a real VM).
- Some labs want a **second machine or second user account** — M22's
  SSH labs and M31's two-actor staging are cleaner in a VM.
- Kernel-level experiments (M17's loopback devices work; M03's boot
  acts don't exist).
- systemd must be *enabled* in `/etc/wsl.conf` (SETUP.md covers it).

**Course policy:** WSL2 is a first-class *tool* and a supported
track; a VM is the *primary* environment because the capstone and the
advanced labs assume a full machine. If your hardware allows only
WSL2, you can finish the course — with the noted substitutions.

## 3. Choosing your hypervisor

| Option | Best for | Notes |
|---|---|---|
| **VirtualBox** | any host, zero cost, simplest UI | the course's default; snapshots built in |
| **virt-manager (KVM/QEMU)** | Linux hosts; better performance | your VM *is* another Linux admin skill (libvirt) |
| **Hyper-V** | Windows Pro hosts | solid; snapshots via checkpoints |
| **VMware Workstation Player** | hosts already using it | fine; menus differ |

Performance rule of thumb for this course: **2 vCPU, 4 GiB RAM,
25 GiB disk** is comfortable for Ubuntu Server + everything through
the capstone. Hosts with 8 GiB total can run one VM at a time — plan
modules sequentially, not simultaneously.

## 4. Ubuntu Server vs Desktop in the VM

The course installs **Ubuntu Server LTS** (no GUI):

- Every lesson teaches the terminal anyway; a GUI costs ~1 GiB RAM
  and teaches point-and-click habits this course exists to replace.
- Servers are where data science actually runs (M31); practicing on
  Server from day one is honest rehearsal.
- If you want a desktop later, it's one package group away — a good
  exercise in itself (M16).

Pick the **latest LTS** (24.04 at time of writing), not interim
releases — M02 explained the support-window reasoning.

## 5. What "installed" will mean by the end of this module

You will have, and be able to *prove*:

1. a verified ISO (M02's Lab 2, applied to a real install)
2. a VM that boots to a login prompt (M03's four acts, observed)
3. a **clean-state snapshot** taken *before* you touch anything
4. a one-page `lab-environment.md` in your notes: host tool, VM
   specs, snapshot names, reset procedure

Item 4 matters more than it looks: the capstone and M31 ask you to
*document your environment* — starting now, with the first machine
you own, is the habit forming early.

---

**Key takeaways**

- A VM is a laboratory with an undo button; a web terminal is not.
- WSL2 is a supported track with named substitutions.
- Ubuntu Server LTS, 2 vCPU / 4 GiB / 25 GiB, snapshot immediately
  after first boot.

**Check yourself:** name one lab in M03 that *requires* a real VM and
why. Name one place where WSL2 is actually *more* convenient.

**Next:** [Lesson 2 — provision the VM](02-provision-the-vm.md)
