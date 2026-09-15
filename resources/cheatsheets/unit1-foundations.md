# Cheatsheet — Unit 1: Foundations

## Know your system

```bash
cat /etc/os-release      # distribution + version (works everywhere)
lsb_release -a           # distributor, codename, release
uname -r                 # kernel version
uname -a                 # kernel + architecture + hostname + date
lscpu                    # CPU model, cores, architecture
free -h                  # memory and swap
lsblk                    # block devices (disks, partitions)
```

## Distribution families (M02)

| Family | Examples | Packages | Release style |
|---|---|---|---|
| Debian | Debian, Ubuntu, Mint | `apt` / `dpkg` (.deb) | stable / LTS + interim |
| Red Hat | RHEL, Fedora, CentOS/Alma | `dnf` / `rpm` (.rpm) | enterprise / fast |
| SUSE | SLES, openSUSE | `zypper` / rpm | enterprise / rolling option |
| Arch | Arch, Manjaro | `pacman` | rolling |

- **LTS (Ubuntu):** every 2 years, 5 years of standard support.
- Verify an ISO: `sha256sum <file>` and compare with the publisher's checksum.

## Architecture layers (M03)

```
hardware -> kernel (Linux) -> system libs -> userland tools -> shell -> GUI
```

- Kernel manages: processes, memory, devices, filesystems, networking.
- `everything is a file`: devices, kernel state (`/proc`, `/sys`).
- Daemons: background services (sshd, journald, cron).

## Virtual machines (M04)

- VM = full computer emulated on your host; **snapshot** = saved point-in-time state.
- Snapshot == instant rollback. Snapshot != backup (it dies with the VM file).
- WSL2 = real Linux kernel in a lightweight VM on Windows; most (not all) labs work.

## First-aid facts

```bash
whoami; id               # who am I; what groups
hostname                 # machine name
sudo apt update          # refresh package lists (first admin command)
```
