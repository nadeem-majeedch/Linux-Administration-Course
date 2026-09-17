# Fresh-Environment Verification Checklist

> **Status: NOT EXECUTED.** This checklist consolidates every environment
> check the course assumes, so a single pass on a fresh VM/WSL2 image
> verifies them all. It was **prepared by inspection** from SETUP.md and
> the module labs; no check below has been executed in a provisioned VM
> during its preparation. Each row has a pass/fail + notes field for the
> person who runs it. Companion documents: [student setup](student-environment-setup.md) ·
> [instructor setup](instructor-environment-setup.md) · [lab infrastructure](lab-infrastructure.md).

## How to use

1. Provision the target environment (Path A VM / Path B WSL2 / instructor image).
2. Run checks in order; each lists prerequisites — skip nothing silently.
3. Record pass/fail + notes per row. Any FAIL = fix before the course week
   that depends on it (the "Week" column says which).
4. Re-run after any snapshot restore that predates a check.

## A. Base system (Ubuntu LTS — Path A VM or lab image)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| A1 | OS release correct | booted VM | `grep PRETTY /etc/os-release` | Ubuntu 24.04 LTS (or newer LTS) | newer LTS ok | read-only | 1 | ☐ | |
| A2 | Kernel sane | booted VM | `uname -r` | generic Ubuntu kernel | minor suffixes | read-only | 1 | ☐ | |
| A3 | Non-root user | booted VM | `whoami && id` | your user, uid ≥ 1000 | — | read-only | 1 | ☐ | |
| A4 | sudo works | A3 | `sudo -v` | password prompt, exit 0 | — | user's own password | 1 | ☐ | |
| A5 | Package lists fresh | A4 | `sudo apt update` | no errors; lists fetched | slow mirror ok | network, no changes | 1 | ☐ | |
| A6 | Toolchain present | A5 | `command -v tree shellcheck htop jq tmux git; python3 --version` | all found; Python 3.10+ | versions vary | read-only | 2 | ☐ | |
| A7 | Directory convention | A6 | `ls -d ~/data ~/projects ~/archive` | all exist | — | none | 2 | ☐ | |
| A8 | Time sync | booted VM | `timedatectl \| head -3` | NTP active, clock correct | — | read-only | 2 | ☐ | |

## B. VirtualBox / VM layer (Path A)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| B1 | 64-bit capable | host | new-VM dialog lists 64-bit Ubuntu | yes | VMware/virt-manager equivalent | none | 1 | ☐ | |
| B2 | VM specs per course | VM powered off | settings: 2 vCPU · 4 GiB · 25 GiB dynamic · NAT | as stated | — | none | 1 | ☐ | |
| B3 | Snapshot machinery | installed VM | take snapshot `clean-install-<date>`; revert; boot | revert returns state | — | VM-only | 2 | ☐ | |
| B4 | Guest additions/dkms | A6 | `sudo apt install -y build-essential dkms linux-headers-$(uname -r)` | installs clean | — | apt | 1 | ☐ | |

## C. WSL2 (Path B)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| C1 | WSL2 present | Windows 10/11 | `wsl.exe --status` | version 2 listed | — | none | 1 | ☐ | |
| C2 | Ubuntu LTS distro | C1 | `wsl.exe --list --verbose` | Ubuntu-24.04, VERSION 2 | newer LTS | none | 1 | ☐ | |
| C3 | systemd enabled | C2 | `cat /proc/1/comm` after `wsl.conf` + `wsl --shutdown` | `systemd` | — | restarts WSL | 2 | ☐ | |
| C4 | System running | C3 | `systemctl is-system-running` | running/degraded | degraded = diagnose | read-only | 2 | ☐ | |
| C5 | Snapshot-equivalent honest | C4 | try `checkpoint`/restore options | none full-machine | — | read-only | 2 | ☐ | record what your reset button actually is |

## D. Identity & permissions (M12–M14 path)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| D1 | umask sane | shell | `umask` | 0002/0022 | other=unusual | read-only | 6 | ☐ | |
| D2 | Group mechanics | A3 | `sudo groupadd -f dsdata && sudo usermod -aG dsdata "$USER"` then re-login | `id` shows dsdata | — | VM-only | 6 | ☐ | |
| D3 | Shared tree | D2 | `/srv/datasets` staged per [lab-infrastructure](lab-infrastructure.md) | 2775 root:dsdata | — | sudo, VM-only | 6 | ☐ | |
| D4 | sudo policy | A4 | `sudo -l` | scoped grants visible | (CMN) ALL for lab user | read-only | 6 | ☐ | |

## E. Storage (M17 path)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| E1 | Block devices visible | booted VM | `lsblk` | vda/sda tree | naming varies | read-only | 8 | ☐ | |
| E2 | Loopback capability | A6 | create 100 MB file, `losetup` per M17 lab | loop device attaches | — | VM-only, loopback | 8 | ☐ | |
| E3 | mkfs on loopback ONLY | E2 | M17 lab lifecycle | fs mounts, survives remount | — | **destructive on loopback file only** | 8 | ☐ | never on real block devices |

## F. Networking & services (M20–M25 path)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| F1 | Loopback reachable | booted VM | `ping -c1 127.0.0.1` | 0% loss | — | none | 10 | ☐ | |
| F2 | DNS works | F1 | `dig example.com +short` | an A record | campus resolver fine | network | 10 | ☐ | |
| F3 | systemd user units | C4 | `systemctl --user status` | manager running | lingering off (fine) | read-only | 10 | ☐ | |
| F4 | Ephemeral listener | F3 | `python3 -m http.server 8000 &` then `ss -tlnp \| grep 8000`; kill it | line appears/disappears | — | loopback | 10 | ☐ | |
| F5 | SSH server | A6 | `systemctl is-active ssh` | active (installed at M04) | — | none | 11 | ☐ | |
| F6 | Key auth loopback | F5 | M22 lab 1 procedure | key login succeeds | — | loopback, lab keys | 11 | ☐ | |
| F7 | UFW available | A4 | `sudo ufw status` | inactive (default) | — | read-only | 12 | ☐ | |
| F8 | journald persistent | A4 | `ls /var/log/journal` | dir exists | volatile = documented | read-only | 12 | ☐ | |

## G. Python / Jupyter / Git (M26–M27 path)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| G1 | venv creation | A6 | `python3 -m venv .venv && . .venv/bin/activate && which python3` | venv path wins | — | none | 13 | ☐ | |
| G2 | pip explicit form | G1 | `python3 -m pip --version` | points into venv | — | none | 13 | ☐ | |
| G3 | Pinned install | G2 | `python3 -m pip install pandas==<pin>` (course pin) | installs into venv | version per semester | network | 13 | ☐ | |
| G4 | Jupyter serves | G3 | `jupyter lab --no-browser` + `ss -tlnp \| grep 8888` | listener on 8888 | port may vary | loopback | 13 | ☐ | |
| G5 | Git identity | A6 | `git config --global user.name/user.email` | set | — | none | 13 | ☐ | |
| G6 | SSH remote auth | F6 | `ssh -T git@` course server or localhost probe | key offered | — | loopback | 13 | ☐ | |

## H. Docker (M28 path — optional track)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| H1 | Docker installed | A5 | `docker --version` | present (SETUP.md section) | Desktop on WSL2 | none | 14 | ☐ | |
| H2 | Group membership | H1 | `docker run hello-world` | runs without sudo | sudo acceptable | container sandbox | 14 | ☐ | |
| H3 | Volume persistence | H2 | M28 build lab volume check | data survives `docker rm` | — | VM-only | 14 | ☐ | |
| H4 | Port mapping | H2 | `-p 8888:8888` container + `ss` | host-side listener | — | loopback | 14 | ☐ | |

## I. Datasets & lab data (M07+ path)

| ID | Purpose | Prereq | Command / action | Expected | Acceptable variation | Safety | Week | Pass? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| I1 | Course data present | A6 | files from [M08 data dir](../../modules/M08-text-processing/content/data/) or lab share | server.log, access.log, transactions.csv, students.csv, sensor-telemetry.tsv, experiment.log | generated fresh | read-only | 4 | ☐ | |
| I2 | Checksums match | I1 | `sha256sum -c` per dataset README | OK lines | — | read-only | 4 | ☐ | |
| I3 | Two pending known | I1 | check [datasets/STATUS.md](../../datasets/STATUS.md) | syslog-sample pending noted | — | read-only | — | ☐ | instructor decision: deliver or substitute |

## Sign-off

| Field | Value |
|---|---|
| Environment (path/spec) | |
| Date | |
| Run by | |
| Checks passed | / total |
| Failures & dispositions | |
| Follow-ups | |
