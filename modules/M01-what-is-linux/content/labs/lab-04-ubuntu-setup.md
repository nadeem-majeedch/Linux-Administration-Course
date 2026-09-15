# Lab 4 — Ubuntu Setup & First Login

> Lesson 8 · Time: 60–90 min · Risk level: **contains the module's only state-changing
> steps** (creating a VM, installing updates) — all inside your own VM/WSL2, all
> reversible or harmless
> Environment: your host machine + VirtualBox, or WSL2

## Goal

Build the machine the entire course runs on, take its safety snapshot, and log in
to a terminal you operate by choice, not by guesswork. Done carefully, this lab is
the highest-leverage hour of the whole program.

## Before you start

- [ ] Read Lesson 8 (this lab implements it)
- [ ] Host requirements: ~25 GB free disk, 8 GB RAM recommended
- [ ] Choose your track: **A — VirtualBox VM (recommended)** or **B — WSL2**

---

## Track A — VirtualBox VM (recommended)

### A1. Download and verify (15 min)

1. VirtualBox from <https://www.virtualbox.org/wiki/Downloads>; install with
   defaults.
2. **Ubuntu 24.04 LTS Desktop** ISO from <https://ubuntu.com/download/desktop>.
3. Verify the ISO (integrity is a professional habit, not paranoia):
   - Linux/macOS: `sha256sum <iso-file>`
   - Windows PowerShell: `Get-FileHash <iso-file> -Algorithm SHA256`
   - Compare against the SHA256SUMS Ubuntu publishes with the release.
     **Mismatch → delete and re-download.** Record the checksum in `lab-log.md`.

### A2. Create the VM (10 min)

| Step | Setting |
|---|---|
| New → Name | `Ubuntu-DS-Lab`, Type: Linux, Version: Ubuntu (64-bit) |
| Memory | 4096 MB |
| CPUs | 2 (Settings → System → Processor) |
| Disk | Create now → VDI → **Dynamically allocated** → 30 GB |
| Storage | Attach the ISO to the empty optical drive |
| Display | Video memory 128 MB (smoother) |

### A3. Install Ubuntu (20 min)

Start the VM → "Try or Install Ubuntu" → follow the installer with the choices from
[Lesson 8 §4](../lessons/08-setup-vms-wsl2-ubuntu.md#4-the-installer-safe-choices-explained)
(keyboard test included; username lowercase; auto-login OFF). When it reboots into
the desktop, log in with your password — first ritual of many.

> **Why "Erase disk" is safe here:** it erases the *virtual* disk inside the VM's
> disk file — your host machine is untouched. Read the dialog; it says
> `VBOX HARDDISK`. If it ever names your real disk, you are in the wrong installer —
> abort (that cannot happen inside a VM, but the reading habit is the point).

### A4. Update and snapshot (10 min)

Open a terminal (**Ctrl+Alt+T**):

```console
$ sudo apt update
$ sudo apt upgrade -y
```

Both commands need your password (the one you chose at install; typing is invisible
— normal). `apt` is Module 16's subject; today it means "refresh the catalog, then
apply updates". This is the course's *only* planned `sudo` in Module 01, and its
purpose is explained: package updates require admin rights, this VM is yours, and
the `-y` auto-confirms the routine list.

Then the safety net:

- Shut down cleanly (`sudo shutdown now` or the desktop menu — reading Lesson 8:
  why do we prefer clean shutdowns?), start VirtualBox again,
  **Machine → Take Snapshot** → name: `M01-clean-install`.

Verify the snapshot exists in the Snapshots pane. Done: every future "what if I
break it?" now has an answer — *restore snapshot*.

---

## Track B — WSL2 (Windows 10/11)

### B1. Install (15 min)

PowerShell (Admin):

```powershell
wsl --install
```

Reboot when prompted. Ubuntu launches; choose username (lowercase) and password.
Confirm versions:

```powershell
wsl --version
wsl --list --verbose
```

`VERSION` must read `2` for your Ubuntu. Inside Ubuntu:

```console
$ cat /etc/os-release     # expect Ubuntu 24.04 LTS
$ uname -r                # expect: …-microsoft-standard-WSL2
```

### B2. Update and configure (10 min)

```console
$ sudo apt update
$ sudo apt upgrade -y
```

WSL2 has no VirtualBox-style snapshot: your safety net is documentation + backups.
In `lab-log.md`, write your recovery plan (three lines minimum): what you would
reinstall, in what order, and which files you would back up first. (Modules 24 and
beyond turn this into scripted backups.)

Optional but recommended: enable systemd if your WSL2 needs it later — check
`systemctl --version` works; if not, SETUP.md §B shows the `/etc/wsl.conf` setting.

---

## Common to both tracks: first login & orientation (10 min)

### C1. Create your lab log

```console
$ cd
$ nano lab-log.md
```

(`cd` alone = go home — Module 6's subject; `nano` is the beginner editor; save with
**Ctrl+O, Enter**, exit with **Ctrl+X**.) Start the file with:

```
# Lab log — <your name>
Machine: <hostname> · Track: A/B · Started: <date>

## M01 — Lab 4
- Ubuntu 24.04.1 LTS, kernel <from uname -r>
- Snapshot taken: M01-clean-install (track A) / recovery plan written (track B)
```

### C2. The orientation circuit

Run and record (all read-only — you met every one of these):

```console
$ whoami
$ hostname
$ uname -srm
$ cat /etc/os-release | head -2
$ free -h | head -2
```

Then three *movements* that keep you out of trouble forever:

1. **Prompt check:** read your prompt aloud to yourself — username `@` hostname,
   `~`, and `$`. You are a normal user on your own machine.
2. **Ctrl+C:** run `ping localhost`, then **Ctrl+C**. The prompt returned. This is
   your emergency exit for the rest of the course.
3. **Terminal discipline:** close the terminal (Ctrl+D or `exit`), reopen it, and
   press **↑** — history survived. (Why? Discuss in one log line.)

### C3. Housekeeping (2 min)

- Desktop Ubuntu users: consider Guest Additions (SETUP.md §A5) for resizable windows.
- Bookmark — in a text file, not a browser — this module's troubleshooting guide
  ([../troubleshooting.md](../troubleshooting.md)).

## Wrap-up checklist

- [ ] Ubuntu 24.04 LTS boots; identity block recorded in `lab-log.md`
- [ ] ISO checksum verified before install (track A)
- [ ] `M01-clean-install` snapshot exists (track A) / recovery plan written (track B)
- [ ] Updates applied via `apt` — and you can say in one sentence why sudo was needed
- [ ] Ctrl+C tested; history tested; prompt read
- [ ] `lab-log.md` lives in your home directory and has today's date

## What you have now

A real Ubuntu environment you built, verified, updated, and snapshotted — plus the
log-keeping habit the course grades. Every module from here on assumes this machine
exists. When something goes wrong later (something will — that's the curriculum),
you restore a snapshot or follow a recovery plan *like a professional*, not by
re-installing from scratch.
