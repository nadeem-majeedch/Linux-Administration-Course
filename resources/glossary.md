# Glossary

Plain-language definitions of terms used in the course. Each entry says what it is
and why a data scientist cares. Terms are introduced formally in the module shown.

## A

**ACL (Access Control List)** — Fine-grained permissions beyond user/group/other;
grant a specific user access to a specific file. *M13.*

**apt** — Ubuntu's package tool; installs software from signed repositories. *M16.*

**Architecture (Linux)** — The layering: hardware → kernel → libraries → tools →
shell → GUI. *M01, M03.*

**awk** — A field-aware text-processing language; the classic tool for "take column
3 and sum it." *M09.*

## B

**Background job** — A process running without holding your terminal (`&`, `bg`);
how long training runs coexist with your typing. *M18.*

**Bash** — The Bourne Again Shell; the course's shell and scripting language. *M05, M10.*

**Binding (port)** — Claiming a port on an interface; a service "bound to localhost"
is unreachable from other machines. *M21, M29.*

**Boot process** — Firmware → bootloader → kernel → systemd → services. *M20.*

## C

**Capstone** — The final project: a complete pipeline + service + ops evidence. *M30.*

**chmod / chown** — Change permissions / change ownership. *M12, M13.*

**Container** — An isolated process view using the host kernel; lighter than a VM. *M28.*

**cron** — The classic time-based job scheduler; five fields: minute hour day month
weekday. *M19.*

**cgroups** — Kernel feature limiting a group's resource use; the mechanism under
container limits. *M18, M28 (awareness).*

## D

**Daemon** — A background service process (sshd, nginx, journald). *M03, M20.*

**Dataset volume** — A dedicated mounted disk for data; keeps a full data disk from
taking down the system disk. *M17.*

**Deployment** — Putting a working service into operation: artifact, config, health
check, logs, rollback. *M29, M30.*

**Directory** — A file that contains other files' names. Execute permission on it
means "may pass through." *M06, M12.*

**DNS (Domain Name System)** — Turns names into IP addresses. When "the network is
down," it is often DNS. *M21.*

**Dry run** — Executing a command in report-only mode to preview damage (`rsync
--dry-run`, your own `--dry-run` flags). *M11, M23.*

## E

**Environment variable** — A value a process inherits (`PATH`, `HOME`,
`CUDA_VISIBLE_DEVICES`); the standard way to configure programs without editing them. *M15.*

**Exit code** — A command's numeric status; `0` = success. Scripts that check exit
codes fail loudly instead of silently. *M05, M10.*

## F

**Filesystem** — The structure that organizes files on a partition (ext4, xfs). *M17.*

**Filter** — A command that reads stdin and writes stdout (`grep`, `sort`, `awk`). *M09.*

**FHS (Filesystem Hierarchy Standard)** — The convention for what lives in `/etc`,
`/var`, `/home`, and friends. *M06.*

**Firewall** — Rules deciding which network traffic is allowed (ufw on Ubuntu). *M25.*

**Fork** — To create a new process by copying the current one; how the shell runs
your commands. *M18 (concept).*

## G

**Git** — Distributed version control; snapshots of your project with history. *M26.*

**Group** — A named set of users; permissions can be granted per group — the basis
of shared dataset access. *M12, M13.*

## H

**Hard link / soft link** — Another name for the same file / a pointer to a path.
Course covers recognition; `ln` appears in M07 labs (optional).

**Hash (checksum)** — A fingerprint of a file's bytes (`sha256sum`); proves a
download or transfer is intact. *M02, M23, M24.*

## I–J

**Idempotent** — Safe to run again with the same result; the property that makes
scripts schedulable. *M11, M19.*

**IP address** — A machine's network address (IPv4 like `192.168.1.20`); private
ranges (`10.x`, `172.16–31.x`, `192.168.x`) are not routable from the internet. *M21.*

**journald** — systemd's binary, structured logging service; queried with
`journalctl`. *M24.*

**Jupyter** — Notebook server for interactive data work; on Linux it runs headless
and is reached through SSH tunnels. *M27.*

## K–L

**Kernel** — The core of the OS: processes, memory, devices, filesystems, network.
What "Linux" strictly means. *M01, M03.*

**Load average** — Runnable + uninterruptible processes over 1/5/15 min; read it
against core count, not against 1.0. *M18, M24.*

**LTS (Long Term Support)** — Ubuntu releases with 5 years of fixes; the course's
platform. *M02.*

## M–N

**Mount** — Attaching a filesystem to a directory tree at a mount point. *M17.*

**NAT** — Network address translation; lets a VM share the host's IP. *M21 (VM networking).*

**nice / renice** — Set / change a process's scheduling priority. *M18.*

## O–P

**Ownership** — Every file has one owning user and one owning group. *M12, M13.*

**Package / repository** — Bundled software with metadata / a signed catalog of
packages. *M16.*

**Partition** — A subdivision of a disk holding a filesystem. *M17.*

**PATH** — The ordered list of directories the shell searches for commands; the
answer to "command not found." *M15.*

**Permission (rwx)** — Read, write, execute, per user/group/other. *M12.*

**PID** — Process ID; how you target a process with signals. *M18.*

**Pipe** — Connect one command's stdout to the next's stdin (`|`); the core of
shell data processing. *M09.*

**Port** — A numbered door on a machine for network services (22 SSH, 80/443 web,
5432 PostgreSQL). *M21.*

**Process** — A running program with its own memory and PID. *M18.*

## R–S

**Redirection** — Sending streams to/from files (`>`, `>>`, `<`, `2>`). *M09.*

**Repository (apt)** — See *Package*. Distro repos are signed; third-party repos
are trust decisions. *M16.*

**rsync** — Delta-synchronizing copy tool; the dataset-transfer workhorse. *M23.*

**Shell** — The program that reads your commands and runs them; also a programming
language. *M05.*

**Signal** — A message to a process (SIGTERM = please stop, SIGKILL = stop now,
SIGINT = your Ctrl+C). *M18.*

**Snapshot (VM)** — A saved point-in-time state of a VM; instant rollback —
*not* a backup. *M04, M24.*

**Socket** — An endpoint of a network connection; `ss` lists who is listening. *M21.*

**SSH** — Encrypted remote shell; keys, config, tunnels, and tmux make it the
remote-workstation workflow. *M22.*

**stdin / stdout / stderr** — The three standard streams: input, output, errors. *M09.*

**sudo** — Run a command as another user (usually root) with policy control. *M14.*

**systemd** — The init system and service manager (PID 1); units, targets,
`systemctl`. *M20.*

## T–U

**Terminal emulator** — The window that hosts your shell session. *M05.*

**tmux** — Terminal multiplexer: sessions that survive disconnects; the SSH
companion. *M22.*

**udev** — Device manager; why device names can change between boots (hence UUIDs
in fstab). *M17 (recognition).*

**umask** — The permission bits *removed* from new files by default. *M12.*

**UUID** — A filesystem's unique ID; the stable way to mount in fstab. *M17.*

## V–Z

**venv** — A Python virtual environment: an isolated interpreter + packages tree. *M27.*

**Volume** — See *Dataset volume*; in LVM, a logical volume. *M17.*

**WSL2** — Windows Subsystem for Linux 2: a real Linux kernel in a lightweight VM
on Windows. *M04, SETUP.md.*

**Xargs** — Builds command lines from stdin; the bridge from `find` to actions. *M09.*

**Zombie** — A dead process not yet reaped by its parent; usually harmless, always
worth recognizing. *M18.*
