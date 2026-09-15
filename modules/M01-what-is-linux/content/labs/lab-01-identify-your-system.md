# Lab 1 — Identify Your System

> Lesson 4 · Time: ~30 min · Risk level: zero (all read-only)
> Environment: any Ubuntu system — your VM (Lab 4), a lab machine, or WSL2

## Goal

Interrogate a Linux system about itself using read-only commands, and learn the
outputs well enough to answer "what am I running on?" in under a minute — the
first question of every incident, forum post, and bug report you will ever file.

## Before you start

- [ ] A terminal is open (Ctrl+Alt+T on desktop Ubuntu; Start menu → Ubuntu on WSL2)
- [ ] Your `lab-log.md` exists (any file is fine until Lab 4 creates the real one)
- [ ] You remember: `$` is the prompt — you never type it

## Part 1 — The identity block

Run each command; **predict first**, then compare with reality:

| # | Command | What to look for |
|---|---|---|
| 1 | `whoami` | Your username |
| 2 | `hostname` | The machine's name |
| 3 | `uname -srm` | Kernel name, release, architecture |
| 4 | `cat /etc/os-release` | Distribution, version, codename, family |
| 5 | `id` | Your uid, gid, and groups |

Checkpoint: in `lab-log.md`, write your machine's identity block (all five outputs,
trimmed) under the heading `Lab 1 — Part 1`. Underline (bold) one field you did
*not* expect — e.g., `ID_LIKE=debian` or your `sudo` group membership.

## Part 2 — Hardware, through the /proc window

```console
$ lscpu | head -8
```

Record: architecture, CPU count, model name. If you are in a VM, also run
`lscpu | grep -i hypervisor` — what does it say?

```console
$ free -h
```

Record total and available memory. On WSL2, note how much of the *host* RAM the
VM shows — where do you think the limit comes from?

```console
$ lsblk
```

Your first look at storage topology: disks and their partitions as a tree. VMs
typically show `sda` (the virtual disk) with partitions; WSL2 shows a smaller,
odd-looking root. Do not act on anything here — Module 17 will make this command
essential; today it is vocabulary.

## Part 3 — Reading outputs like data

You are a data scientist: treat outputs as datasets.

1. From `cat /etc/os-release`, extract *just* the version number field. (Manual
   reading is fine — but notice the `KEY=value` shape; Modules 8–9 will extract
   such fields mechanically.)
2. From `lscpu`, find the CPU's model name. Quote it exactly.
3. From `free -h`: is your *available* memory larger or smaller than *free*?
   One sentence: why do you think both numbers exist?

## Part 4 — Comparison drill (pairs, or solo with two systems)

If a classmate's machine (or a lab server) is reachable, run the identity block
there too and tabulate:

| Field | Machine A | Machine B |
|---|---|---|
| OS release | | |
| Kernel | | |
| Architecture | | |
| CPU count | | |
| Total RAM | | |

Solo alternative: compare your VM against the numbers quoted in Lesson 4 and note
every difference. Then answer: which of these differences would change *which
package manager* the machine uses? (Hint: Lesson 3.)

## Wrap-up checklist

- [ ] Identity block recorded with date and machine name
- [ ] You can answer, from memory: which kernel? which distro? which family (deb/rpm)?
- [ ] `lab-log.md` has entries for Parts 1–3
- [ ] You used Tab completion at least once while typing these commands (habit!)

## What you can now do

Walk up to any Linux machine — lab, cluster login node, cloud instance — and in
under a minute produce its identity card. Every "help, my thing is broken" request
you file for the rest of your career should start with exactly these outputs.
