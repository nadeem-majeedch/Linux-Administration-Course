# M04 — Installing Linux & Virtual Machines

> Unit 1 · Foundations of Linux · Difficulty: Beginner
> Prerequisites: [M02](../M02-linux-distributions/README.md) (verify
> skills), [M03](../M03-linux-architecture/README.md) (boot theory)
> Est. time: ~5 h (lessons ~80 min, labs ~2 h incl. install,
> practice ~80 min)

**Status: content complete.**

## Learning objectives

By the end of this module you can:

1. **Justify** the VM-first laboratory approach and select between
   VirtualBox, virt-manager/KVM, Hyper-V and WSL2 for given hardware,
   stating each option's limits.
2. **Provision** an Ubuntu Server LTS VM with defensible sizing
   (2 vCPU / 4 GiB / 25 GiB, NAT), completing the installer's key
   decisions deliberately (normal user, SSH at install, entire
   *virtual* disk only).
3. **Verify** an ISO's integrity (SHA-256 manifest) and authenticity
   (signature over the manifest), and respond correctly to each
   verification outcome — before installing.
4. **Read** a first boot's evidence (`systemd-analyze`, `blame`,
   `journalctl -b -p err`) and record day-one identity evidence.
5. **Operate** snapshots as a reset system: milestone naming policy,
   controlled revert with before/after evidence, and the snapshot-
   is-not-a-backup distinction that M26 builds on.

## What's inside

| Path | Contents |
|------|----------|
| [content/README.md](content/README.md) | Module guide + prerequisite map |
| [content/lessons/](content/lessons/) | 4 lessons: why a lab · provisioning · verification & first boot · snapshots & reset discipline |
| [content/labs/](content/labs/) | Lab 1: provision with four evidence gates · Lab 2: the WSL2 track |
| [content/practice/](content/practice/) | Quiz (+ key) · challenges C1–C5 |
| [content/troubleshooting.md](content/troubleshooting.md) | Seven provisioning-failure patterns |

## Definition of done

- [ ] VM provisioned through Lab 1's four gates, all evidence logged
- [ ] Controlled revert performed and *proven* with the evidence pair
- [ ] `lab-environment.md` written (host, specs, snapshots, reset
      procedure) and peer-checked via C5
- [ ] Quiz ≥ 14/18; WSL2 students additionally complete Lab 2

## Module links

- Roadmap: [COURSE-ROADMAP.md](../../COURSE-ROADMAP.md#unit-1--foundations-of-linux-m01m04)
- Next: [M05](../M05-terminal-and-shell/README.md) — Unit 2 begins ·
  Cheatsheets: [resources/cheatsheets/](../../resources/cheatsheets/)
