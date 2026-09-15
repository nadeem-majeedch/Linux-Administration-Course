# Lesson 8 — Setup: VMs, WSL2 & Ubuntu

> Module 01 · Unit 1 · Difficulty: Beginner (hands-on)
> Reading time: ~30 min · Lab: [Lab 4 — Ubuntu setup & first login](../labs/lab-04-ubuntu-setup.md)
> Companion: [SETUP.md](../../../../SETUP.md) (the repo's full setup guide)

---

## 1. Three ways to run Linux, and who should pick which

| Way | What it is | Pick it if… | Course verdict |
|---|---|---|---|
| **Virtual machine (VM)** | A full computer *simulated in software* on your host OS, running a complete Ubuntu | You want the real, complete Linux experience, safely isolated | **Recommended** — the course's primary environment |
| **WSL2** (Windows only) | A real Linux kernel running in a lightweight utility VM, integrated into Windows | You're on Windows and can't or don't want to run VirtualBox | Fine for most of the course; differences listed below |
| **Native install** | Ubuntu replaces/beside your OS on real hardware | You have a spare machine | Optional; works, but no snapshots to rescue you |

Why a **VM** is the right classroom: mistakes are the curriculum. A VM gives you
**snapshots** — saved, point-in-time states you can roll back to in seconds. You can
deliberately break things (later modules will ask you to!) with a guaranteed undo.
Snapshots are *not* backups (they live inside the VM's disk file) — a distinction
Module 24 formalizes — but for learning they are the safety net.

A bonus: your future cloud instances (Module 22 and beyond) are *also* virtual
machines. The skills — create, start, stop, snapshot, connect — transfer directly.

## 2. Virtual machines: the 5-minute theory

A **hypervisor** (VirtualBox, VMware, or the KVM already inside Linux) is software
that carves your real computer into several virtual ones:

- **Host** = your real machine (Windows/macOS/Linux) with its real OS.
- **Guest** = the VM — Ubuntu here — which believes it owns real hardware. It
  doesn't: the hypervisor translates its every hardware request to the host.
- The guest gets a slice of **CPU cores**, **RAM**, and a **virtual disk**, which is
  just a big file on the host (e.g., `Ubuntu-DS-Lab.vdi`).

One hardware requirement: **virtualization must be enabled in your BIOS/UEFI**
(Intel calls it VT-x, AMD calls it AMD-V/SVM). Most machines ship enabled; if
VirtualBox complains "VT-x is disabled", it's a firmware settings visit — exact steps
in the module [troubleshooting guide](../troubleshooting.md).

Recommended VM size for this course (fits in 8 GB-RAM laptops):

| Resource | Setting |
|---|---|
| RAM | 4096 MB |
| CPUs | 2 |
| Disk | 30 GB, **dynamically allocated** (grows as used — takes what it needs, not all 30 GB at once) |

## 3. Building the VM (VirtualBox path)

Full detail lives in [SETUP.md](../../../../SETUP.md) Path A; the short form:

1. Install **VirtualBox** from <https://www.virtualbox.org/wiki/Downloads>.
2. Download the **Ubuntu 24.04 LTS Desktop** ISO from <https://ubuntu.com/download/desktop>.
3. **Verify the ISO checksum** (`sha256sum ubuntu-24.04…iso` on any system, or
   PowerShell's `Get-FileHash … -Algorithm SHA256` on Windows) against the value
   Ubuntu publishes. A mismatch means a corrupted or tampered download: delete,
   re-download. (Lesson 2's "open source is verifiable" made practical.)
4. New VM: name `Ubuntu-DS-Lab`, Type Linux / Ubuntu (64-bit), 4 GB RAM, 2 CPUs,
   30 GB dynamic VDI; attach the ISO as the optical drive.
5. Start → "Try or Install Ubuntu" → walk the installer (next section).

## 4. The installer: safe choices explained

The Ubuntu installer asks real questions. The course-recommended answers, with the
*why*:

| Question | Choose | Why |
|---|---|---|
| Try or install | **Install** | You want the permanent system |
| Keyboard layout | Yours (test the typing box) | Wrong layout = mangled passwords later |
| Installation type | **Erase disk and install Ubuntu** | Terrifying name, safe reality: it erases the **virtual** disk, not your host. Read the dialog: it names the virtual disk (e.g. `VBOX HARDDISK`) |
| Your name | e.g. `DS Student` | Cosmetic |
| Computer name | `ubuntu-ds-lab` | Appears in your prompt (Lesson 5!) and on the network |
| Username | lowercase, no spaces, e.g. `dsstudent` | Conventions matter; commands are case-sensitive |
| Password | Memorable one; you'll type it for `sudo` often | You *will* use it weekly |
| Log in automatically | **Off** | Typing your password at login is itself practice — and better hygiene |

First boot: updates run (`sudo apt update && sudo apt upgrade -y` — Module 16 will
formalize this), then **Machine → Take Snapshot**, name it `M01-clean-install`.
This snapshot is your undo button for the whole course.

Optional comfort: Guest Additions (SETUP.md §A5) for resizable windows and shared
clipboard. (Host-level detail: [SETUP.md](../../../../SETUP.md).)

## 5. WSL2: the honest alternative

**WSL2** (Windows Subsystem for Linux, version 2) runs a *real Linux kernel* in a
lightweight VM managed by Windows, deeply integrated with the host: your Windows
files appear under `/mnt/c/…` inside Linux, Linux files are reachable from Windows
Explorer, and both share the network. One PowerShell (Admin) command installs it:

```powershell
wsl --install
```

Reboot, choose a username and password, and you're inside Ubuntu. Verify:

```console
$ cat /etc/os-release     # confirm Ubuntu 24.04 LTS
$ uname -r                # note: kernel names include "microsoft-standard"
```

That `microsoft-standard` kernel string is your first clue that WSL2 is *real Linux,
with seams*. The honest list of seams for this course:

| Area | WSL2 reality | Course impact |
|---|---|---|
| systemd | Supported on current WSL2 (enable `systemd=true` in `/etc/wsl.conf` if needed) | Mostly none; older setups need the VM for M20/M29 labs |
| Disks/partitions (M17) | Can't add raw virtual disks the VirtualBox way | Module provides a loopback-image alternative |
| ufw/firewall (M25) | Not the host's firewall; ufw is demonstrable but not protective | Module explains the difference; VM used for the real lab |
| GUI apps | Work via WSLg on Windows 11 | None for this course |
| Snapshots | No VirtualBox-style rollback | Keep backups instead; VM recommended for risky labs |

**Recommendation:** WSL2 is a fine primary environment for Lessons 4–7's read-only
work and most of the course; the VM remains the course's reference where M17/M25-type
labs need true hardware emulation. If you have 8 GB+ RAM, run both; if one, prefer
the VM.

## 6. First login & terminal orientation

Boot the VM, log in with your user (this is *why* auto-login is off: the ritual
matters), then open a terminal — the exact moment this module's theory becomes your
daily tool:

1. **Desktop Ubuntu:** press **Ctrl+Alt+T**, or Activities → type "Terminal".
2. **WSL2:** open "Ubuntu" from the Start menu.

Then orient yourself (each command is from Lessons 5–7 — notice you can already read
them):

```console
$ whoami
dsstudent
$ hostname
ubuntu-ds-lab
$ uname -srm
Linux 6.8.0-45-generic x86_64
$ cat /etc/os-release | head -2
PRETTY_NAME="Ubuntu 24.04.1 LTS"
NAME="Ubuntu"
```

Record all four outputs in `lab-log.md` — this is the "identity" entry of your
machine, and the first row of your professional habit: *when debugging anything,
first establish who and where you are*.

Finish Lab 4's checklist (create `lab-log.md`, take the snapshot) and this module —
and your whole environment for the rest of the course — is complete.

## 7. Which lessons to revisit when

| Symptom in later modules | Come back to |
|---|---|
| "What's a distro again?" on a RHEL cluster | Lesson 3 |
| Confusion about where a tool "runs" (container confusion, M28) | Lesson 4 (layers, user/kernel) |
| GUI temptation during automation | Lesson 5 (§2) |
| Forgetting an option's exact spelling | Lesson 6 — *that's the lesson that keeps paying* |
| Mysterious script failures with options-as-filenames | Lesson 7 (quoting, `--`) |

## Exercises (lab-log.md)

1. Explain snapshots vs backups in two sentences, and why the course still wants both
   (the second half arrives in Module 24).
2. Your VM's disk file is 6 GB on the host although you allocated 30 GB. Explain,
   using the word *dynamically*.
3. Record your machine's identity block: `whoami`, `hostname`, `uname -srm`,
   `cat /etc/os-release | head -2`.
4. WSL2 users: run `uname -r` and explain the `microsoft-standard` string. VM users:
   run `lscpu | grep -i hypervisor` and report what it says about your machine.
5. Take the `M01-clean-install` snapshot now (VM users). WSL2 users: write the
   backup plan you'll use instead, and why snapshots can't be your answer.
6. Predict-then-verify: before opening the terminal, write down what each of the
   four commands in §6 will print. Compare. Any surprises?

## Check yourself (module complete)

- I can define VM, host, guest, hypervisor, snapshot — and say why the VM is the
  right classroom.
- I can describe WSL2's architecture and name two honest seams.
- My Ubuntu environment exists, is updated, and is snapshotted.
- My `lab-log.md` has the identity block and dates.

## Further reading (official sources)

- Ubuntu Desktop install tutorial — <https://ubuntu.com/tutorials/install-ubuntu-desktop>
- VirtualBox manual — <https://www.virtualbox.org/manual/>
- WSL documentation — <https://learn.microsoft.com/windows/wsl/>
- This repo's [SETUP.md](../../../../SETUP.md) and
  [troubleshooting guide](../troubleshooting.md)

You have finished Module 01. Next module in the curriculum:
[M02 — Linux Distributions](../../../M02-linux-distributions/README.md)
(you are ahead of the game: Lesson 3 already covered half of it).
