# Lesson 1 — systemd: PID 1, Units & Targets

> Module 20 · Unit 6 · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Lab 1 — the service circuit](../labs/lab-01-service-circuit.md)
> Prerequisites: [M18 processes](../../../M18-processes-jobs-signals/content/lessons/01-processes-inspection.md)

> 🟢 **Safety tier:** inspection commands are safe anywhere. Anything
> that *changes* service state (`start/stop/restart/enable`) is own-VM
> territory — on shared servers, services are managed by their admins,
> not their users.

---

## 1. PID 1 with a job description

M18 showed PID 1 is special: orphans get re-parented to it. On modern
Ubuntu, PID 1 is **systemd** — and its job description is enormous:

- **Start everything** at boot, in dependency order, in parallel where
  possible
- **Supervise** every service: restart what crashes, track what hangs
- **Log** everything services emit (the journal — M24)
- **Manage** more than services: mounts (M17's fstab!), timers (M19's
  cron rival), devices, sockets

The mental model: **systemd is a dependency-driven process supervisor
with a configuration format.** Everything else in this module is
vocabulary for that sentence.

### DS framing

JupyterHub, your training-queue daemon, the lab's database, the GPU
scheduler, every cloud VM's SSH server — all of them are systemd
services. "Is it up?" is `systemctl status`, and "make mine run at
boot" is a unit file. This module is the difference between *using*
infrastructure and *operating* it.

---

## 2. Units: the configuration atoms

A **unit** is a named configuration object with a type suffix. The
types you'll actually meet:

| Type | Suffix | Manages | Example |
|---|---|---|---|
| **service** | `.service` | daemons/long-runners | `ssh.service`, `cron.service` |
| **timer** | `.timer` | scheduled activation | `fstrim.timer` (M17!), `apt-daily.timer` |
| **mount** | `.mount` | filesystem mounts | generated from fstab (M17) |
| **socket** | `.socket` | activates services on connection | `ssh.socket` (newer Ubuntu) |
| **target** | `.target` | groups of units ("runlevels") | `multi-user.target`, `graphical.target` |
| **device/slice/scope** | … | kernel devices, resource groups | recognition level |

Units live in three directories, searched in this order (later wins):

```console
$ pkg-config systemd --variable=systemdsystemunitdir   # /lib/systemd/system — vendor ships here
$ ls /etc/systemd/system | head                        # ADMIN territory — your edits
$ ls ~/.config/systemd/user 2>/dev/null                # YOUR user units (no root!)
```

**The /etc rule:** never edit files in `/lib/systemd/system` (package
updates overwrite them). Override or create in `/etc/systemd/system`,
or use drop-in fragments (`systemctl edit`). This is the M16
"don't fight the package manager" principle, applied.

---

## 3. Targets: the boot groups

A **target** bundles units to reach a system state. The runlevel
descendants:

| Target | Meaning | Runlevel ancestor |
|---|---|---|
| `graphical.target` | multi-user + display manager | 5 |
| `multi-user.target` | full system, no GUI — **servers** | 3 |
| `rescue.target` | single-user repair shell | 1 |
| `emergency.target` | minimal shell, root FS read-only | (worse than 1) |

```console
$ systemctl get-default          # what this machine boots into
graphical.target
$ systemctl list-dependencies multi-user.target | head -8   # what it pulls in
```

Your VM boots to graphical; every server you'll ever SSH into is at
multi-user. When M17's mount units "run at boot," the precise statement
is: they're *wanted by* multi-user.target (or its dependencies).

---

## 4. Enable vs start: the distinction that runs this module

Two orthogonal questions, two different commands:

- **start** — run it *now* (until stopped or reboot)
- **enable** — arrange for it to run *at every boot* (by symlinking it
  into a target's `.wants/` directory)

```console
$ systemctl start ssh      # running now; gone after reboot
$ systemctl enable ssh     # will start at boot; not necessarily running now
$ systemctl enable --now ssh   # both — the idiom you'll type 90% of the time
```

The four states, and how to ask:

| | enabled | disabled |
|---|---|---|
| **active** | running + at boot | running *this* time only |
| **inactive** | will start at boot | fully off |

```console
$ systemctl is-active ssh; systemctl is-enabled ssh
```

The classic incident: "it works but vanishes after reboot" = started
but never enabled. "It's enabled but broken" = enabled but failing at
boot — `systemctl status` + journal tells the story (Lesson 2).

**Why enable is a symlink, not magic** — look under the hood:

```console
$ systemctl enable --now cron 2>/dev/null; ls -l /etc/systemd/system/multi-user.target.wants/ | head -5
cron.service -> /usr/lib/systemd/system/cron.service
```

Enabling = one symlink into `multi-user.target.wants/`. Disabling
removes it. That's all — demystify it once and it never confuses you
again.

---

## 5. Dependencies: why boot order works

Units declare relationships in their files (Lesson 3):

- `After=` — ordering: "start me after that" (no causal link)
- `Requires=` — hard dependency: if that fails, I fail
- `Wants=` — soft dependency: "pull it in too, but I survive its death"
  (this is what `enable` wires up!)

```console
$ systemctl show ssh -p After -p Wants | tr ' ' '\n' | head -8
```

Read the `systemd-analyze critical-chain` output in Lesson 4 with this
vocabulary — "why does boot wait on networkd?" is always an
After/Requires/Wants answer.

**DS framing — the supervision payoff:** `Restart=on-failure` in a unit
file is the systemd answer to M18's `while true; do myjob; done` shell
loops. Your training queue that dies at 3 a.m.? A unit file with
`Restart=` is what the ops team writes instead of cron-and-prayer.

---

## Exercises (lab-log.md)

1. `ps -p 1 -o comm=` on your VM. Now `systemctl --version` — what's
   actually running as PID 1, and which systemd?
2. List the unit types present on your machine:
   `systemctl list-units --type=service --state=running | head -8`.
   Pick three daemons and say what each does for you (man page or
   inference).
3. Find your default target, then count: how many units does
   `multi-user.target` want? (`list-dependencies | wc -l` — the
   machine's whole surface area in one number.)
4. The four-state table: find one unit of each quadrant on your VM
   (`is-active`/`is-enabled` pairs). Names + evidence.
5. Look at `ls -l /etc/systemd/system/multi-user.target.wants/` — how
   many symlinks? Which services did *someone* (you or the distro)
   decide must run at boot?
6. Explain to a hypothetical teammate (2 sentences): why "restart it
   and it'll be fine" is not a systemd strategy — what two systemd
   mechanisms already handle the restart problem?

## Check yourself before Lesson 2

- [ ] I can name six unit types and what each manages.
- [ ] enable vs start is reflexive — including enable --now.
- [ ] I know where units live and why /etc beats /lib.
- [ ] I can read After/Requires/Wants and say which one enable creates.

## Further reading (official sources)

- `man systemd`, `man systemd.unit`, `man systemctl`
- freedesktop systemd docs: https://www.freedesktop.org/wiki/Software/systemd/
- Ubuntu Server Docs — systemd introduction: https://ubuntu.com/server/docs
