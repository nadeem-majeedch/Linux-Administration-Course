# SETUP.md — Build Your Course Environment

> Goal: by the end of this guide you have a working **Ubuntu LTS** environment where
> you can safely practice every lab in the course — even if you start with nothing
> installed and no administrator rights on your main computer.

---

## 0. Choose Your Path

| Path | Who it's for | Needs admin rights? | Notes |
|---|---|---|---|
| **A. VirtualBox VM (recommended)** | Almost everyone; the course's primary environment | Yes, to install VirtualBox | Full Ubuntu experience; snapshots make practice safe |
| **B. WSL2** | Windows 10/11 users on machines where VirtualBox is impractical | Yes (Windows-side) | Real Linux kernel; some GUI/networking differences noted below |
| **C. Native install** | Confident users with a spare machine or partition | Yes | Optional; most "real" but least forgiving |
| **D. Lab machines / cloud** | University-provided VMs, remote desktops, or temporary cloud instances | Varies | Follow instructor guidance; everything in this course works under a normal user account |

> **If you cannot install anything** (locked-down lab computer): ask your instructor
> for a prebuilt VM image or a cloud/lab instance. Every module's labs are designed
> to run inside a normal user account — root access is never assumed.

**Minimum specs for the VM:** 2 CPU cores, 4 GB RAM (8 GB host RAM recommended),
30 GB virtual disk, virtualization enabled in the BIOS/UEFI.

---

## Path A — Ubuntu LTS in VirtualBox (Recommended)

### A1. Download

1. **VirtualBox:** get the current platform package for your host OS from the official
   site: <https://www.virtualbox.org/wiki/Downloads>. Install it with default options.
   (Windows may ask for permission to install network drivers — accept; this is normal.)
2. **Ubuntu ISO:** download the current **Ubuntu 24.04 LTS Desktop** ISO from the
   official site: <https://ubuntu.com/download/desktop>.
3. **Verify the ISO checksum** (teaches M02's skill early):
   - Get the official SHA256SUMS from Ubuntu's release pages.
   - Windows (PowerShell): `Get-FileHash <iso-file> -Algorithm SHA256`
   - macOS/Linux: `sha256sum <iso-file>`
   - Compare with the published value. **If it differs, delete and re-download.**

### A2. Create the VM

1. VirtualBox → **New** → Name: `Ubuntu-DS-Lab`, Type: Linux, Version: Ubuntu (64-bit).
2. Memory: **4096 MB** (more if the host has ≥16 GB). Processors: **2** (more if available).
3. Disk: **Create a virtual hard disk now** → VDI → **Dynamically allocated** → **30 GB**.
4. Settings → System → Processor: 2 CPUs. Display → Video Memory: 128 MB.
5. Settings → Storage → click the empty optical drive → choose the Ubuntu ISO.
6. (Optional but recommended) Settings → General → Advanced → enable **Shared
   Clipboard: Bidirectional** and **Drag'n'Drop: Host To Guest**.

### A3. Install Ubuntu

1. Start the VM → choose **Try or Install Ubuntu**.
2. Follow the installer with these course-recommended choices:
   - Language/keyboard: your preference.
   - Installation type: **Erase disk and install Ubuntu** — *this is safe here*: it
     erases the **virtual** disk, not your real computer. (Read the dialog; it names
     the virtual disk, e.g. `VBOX HARDDISK`.)
   - Your name / computer name: e.g. `ds-student` / `ubuntu-ds-lab`.
   - Username: lowercase, no spaces (e.g. `dsstudent`).
   - Password: choose one you will remember — you'll type it often for `sudo`.
   - Log in automatically: **off** (password logins are part of the practice).
3. When the installer finishes → **Restart Now** → when prompted, remove the ISO
   (VirtualBox usually does this automatically; if asked: Devices → Optical Drives →
   Remove disk from virtual drive) → press Enter to reboot.

### A4. First boot: update and snapshot

Open a terminal inside Ubuntu (`Ctrl+Alt+T`) and run:

```bash
sudo apt update
sudo apt upgrade -y
```

Then shut down cleanly and take the course's first snapshot:

- Machine → **Take Snapshot** → name it `M04-clean-install`, description:
  "Fresh install, updated. Rollback point for risky labs."

> **Snapshots are rollbacks, not backups.** They live inside the VM file and vanish
> with it. Real backups arrive in M24.

### A5. Guest Additions (comfort features)

Devices → **Insert Guest Additions CD Image** → inside Ubuntu:

```bash
sudo apt update
sudo apt install -y build-essential dkms linux-headers-$(uname -r)
cd /media/$USER/VBox_GAs_*    # name varies by version; use tab completion
sudo ./VBoxLinuxAdditions.run
```

Reboot the VM. You now get auto-resizing display and bidirectional clipboard.
If the mount path differs, run `ls /media/$USER/` to find the actual directory name.

---

## Path B — WSL2 (Windows 10/11)

WSL2 runs a **real Linux kernel** in a lightweight VM managed by Windows. It is an
excellent environment for most of this course. Install from **PowerShell (Admin)**:

```powershell
wsl --install
```

This installs WSL2 with Ubuntu by default. Reboot when asked, then set your Linux
username and password on first launch. Useful commands (PowerShell):

```powershell
wsl --list --online        # see available distributions
wsl --install -d Ubuntu-24.04
wsl --list --verbose       # confirm VERSION is 2
wsl --set-default-version 2
wsl --update               # keep the WSL components current
```

Inside WSL Ubuntu, everything in the course works with two categories of exceptions:

| Topic | Difference in WSL2 |
|---|---|
| systemd | Modern WSL2 supports systemd (default in new installs; enable `systemd=true` in `/etc/wsl.conf` if needed, then `wsl --shutdown` from PowerShell and restart). Older setups lack it — M20/M29 labs then need the Path A VM. |
| Storage lab (M17) | You cannot add a raw virtual disk the VirtualBox way; the module's WSL alternative uses a loopback disk image, documented in the module. |
| Firewall lab (M25) | ufw is not the host firewall in WSL2; the module explains the WSL2 reality and demonstrates ufw concepts in the VM instead. |
| GUI apps | Supported on Windows 11 via WSLg; not needed by the course. |

Run `wsl --version` and `cat /etc/os-release` to record your exact setup in your
`lab-log.md` before M05.

---

## Path C — Native Ubuntu Install (Optional)

Only on a machine you may dedicate or repartition. Follow the official guide:
<https://ubuntu.com/tutorials/install-ubuntu-desktop> — then:

1. Complete **A4** (updates + first notes in `lab-log.md`).
2. **No snapshots here** — without virtualization there is no rollback. Adjust lab
   instructions: the course marks every risky step; skip or simulate destructive steps
   per module notes, or do those modules in a VM instead.
3. Keep `~/data` and `~/projects` (created in M06) on a separate home partition if
   you repartition — it makes reinstalls painless.

---

## Path D — Lab Machines, Cloud & No-Install Options

- **Instructor-provided VM image:** import into VirtualBox, skip A1–A3, resume at A4.
- **University remote desktop / VDI:** usually already Ubuntu — check with
  `cat /etc/os-release`; you may have sudo on the VM (ask).
- **Cloud instance (own account):** a small Ubuntu LTS instance (t3.small-class or
  free-tier equivalent) works for Units 1–6; GPU instances are never required by the
  course. Cost warning: stop instances when not in use. SSH setup arrives in M22 —
  for early modules use the provider's web console or browser SSH.
- **Restricted accounts:** the entire course works without root *except* explicitly
  marked sudo steps (M13/M14/M16/M17/M25/M28/M29 labs), which include a documented
  alternative ("observe + instructor demo" or "user-space equivalent").

---

## Post-Install Checklist (All Paths)

Run inside Ubuntu and confirm each line works:

```bash
cat /etc/os-release              # shows 24.04 LTS (or newer LTS)
uname -r                          # kernel version — note it in lab-log.md
whoami && id                      # your user, your groups
sudo -v                           # asks for YOUR password; proves sudo works
sudo apt update                   # package lists refresh without errors
python3 --version                 # Python is present
git --version                     # git is present (install: sudo apt install git)
```

Install the **course toolchain** now (this is M16 practice — typing it early is fine):

```bash
sudo apt install -y tree shellcheck htop jq tmux build-essential \
  python3-venv python3-pip curl wget git
```

Then create your course directory convention (M06 will formalize it):

```bash
mkdir -p ~/data ~/projects ~/archive
```

Open `lab-log.md` in your home directory and record: date, path chosen (A/B/C/D),
Ubuntu version, kernel version, and anything that surprised you. **You will keep this
file for the whole course** — labs and the capstone grade it as evidence of practice.

### Docker (needed from Week 14 — install anytime before then)

M28 (containers) and the capstone's Docker track need Docker Engine. On the
lab VM (Ubuntu), install from Ubuntu's own repository — sufficient for this
course:

```bash
sudo apt install -y docker.io
sudo usermod -aG docker "$USER"   # run containers without sudo; log out & back in
docker run hello-world             # verify — see M28 lab 0 for the full walkthrough
```

- **WSL2 (Path B):** Docker Desktop with the WSL2 backend, or `docker.io`
  inside the distro — both work; M28 [lab 0](modules/M28-docker-containers/content/labs/lab-00-install.md)
  covers both and what differs.
- The `docker` group is root-equivalent on the VM — fine for a disposable
  lab machine, and a good M25 discussion point.
- Fall behind? `lab-00-install.md` is the authoritative, tested path;
  this section is the heads-up, not the replacement.

---

## Troubleshooting

| Symptom | Likely cause & fix |
|---|---|
| VM won't start: "VT-x/AMD-V is disabled" | Enable virtualization (Intel VT-x / AMD-V) in the BIOS/UEFI: reboot into firmware settings, find *Virtualization Technology*/*SVM Mode*, enable, save. |
| Ubuntu is slow in the VM | Give the VM ≥2 CPUs and 4 GB RAM; install Guest Additions; ensure the host has free RAM. |
| `wsl --install` says "virtualization not enabled" | Same firmware fix as above; on Windows also verify "Virtual Machine Platform" is on (Windows Features). |
| Shared clipboard doesn't work | Guest Additions not installed/running — redo A5 inside the VM. |
| `sudo: command not found` | Unusual; check `which sudo`. On WSL minimal images: `apt install sudo` (as root via `su -` if needed — ask the instructor first). |
| Screen resolution tiny in VM | Guest Additions (A5), or View → Virtual Screen → resize. |
| Disk space warnings during labs | See M17; meanwhile close other VMs and grow the virtual disk (VirtualBox: `VBoxManage modifymedium disk <file> --resize 46080` then resize the partition from a live ISO — instructor-assisted). |
| Internet not working in VM | Set the VM's network adapter to **NAT** (default). For bridged-mode labs (M21), switch to Bridged with instructor guidance. |

---

## Verify You're Ready

You are ready for M05 when:

- [ ] Ubuntu boots and you can open a terminal.
- [ ] `cat /etc/os-release` shows an Ubuntu LTS release.
- [ ] `sudo apt update` succeeds.
- [ ] Snapshot `M04-clean-install` exists (Path A) or your setup is documented in `lab-log.md` (Paths B/C/D).
- [ ] Course toolchain installed; `~/data`, `~/projects`, `~/archive` exist.
- [ ] You know your password and have typed it for `sudo` at least once.

Bring that `lab-log.md` everywhere — it's the first artifact of the course.
