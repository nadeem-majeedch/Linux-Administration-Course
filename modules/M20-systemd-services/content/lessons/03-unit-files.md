# Lesson 3 — Unit Files: Reading & Writing Service Definitions

> Module 20 · Unit 6 · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Lab 1](../labs/lab-01-service-circuit.md), [Lab 2](../labs/lab-02-break-and-fix.md)
> Prerequisites: [Lesson 2](02-systemctl-operations.md)

> 🟡 **Safety tier:** you'll write a **user** unit (no root, no system
> impact). System-unit authoring is shown instructor-side; the
> mechanical skills transfer 1:1 when you have your own server.

---

## 1. Anatomy: reading a real unit file

The fastest way to learn the format is reading a stock one:

```console
$ systemctl cat cron
# /usr/lib/systemd/system/cron.service
[Unit]
Description=Regular background program processing daemons
Documentation=man:cron(8)
After=mail.target

[Service]
EnvironmentFile=-/etc/default/cron
ExecStart=/usr/sbin/cron -f -P
IgnoreSIGPIPE=false
KillMode=process
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

`systemctl cat` (not `cat /lib/...`) — it shows the file *plus any
drop-in overrides*, which is the full effective truth. Three sections:

| Section | Purpose | You'll touch it |
|---|---|---|
| `[Unit]` | metadata + relationships | Description, After, Wants, Requires |
| `[Service]` | how to run/stop/restart | ExecStart, Restart, User, Type |
| `[Install]` | what `enable` wires up | WantedBy |

Key directives decoded (the 80/20 set):

| Directive | Meaning | In cron's file |
|---|---|---|
| `After=` | ordering constraint | start after mail stack, if present |
| `EnvironmentFile=-…` | read KEY=VALUE pairs; `-` = optional | /etc/default/cron, if it exists |
| `ExecStart=` | **the one required command** | `/usr/sbin/cron -f -P` |
| `Restart=on-failure` | supervisor behavior | re-spawn if it dies abnormally |
| `KillMode=process` | what stop() signals (process vs cgroup) | narrowly: only the main PID |
| `WantedBy=multi-user.target` | what enable() symlinks into | boot at multi-user |

**Why `-f` in ExecStart?** cron must *not* daemonize (fork to
background) — systemd wants the process it supervises to stay in the
foreground. `-f` = foreground. This is the `Type=` question (below).

---

## 2. Type=: how systemd knows you're ready

The subtlest directive: when does systemd consider the service
"started"?

| Type | "Started" means | Use for |
|---|---|---|
| `simple` (default) | ExecStart forked | most modern daemons; safe default |
| `exec` | forked **and** exec() succeeded | when binary may fail to exec |
| `forking` | the process daemonized (parent exited) | old-school daemons (sshd pre-socket) |
| `oneshot` | the process *exited* successfully | one-shot scripts, setup tasks |
| `notify` | the daemon called sd_notify("READY=1") | well-behaved modern daemons |

Beginner guidance: **`simple` for anything that runs in the
foreground; `oneshot` for scripts that do a thing and exit.** The
classic bug: a script that backgrounds itself, paired with `Type=
simple` — systemd thinks it died, `Restart=on-failure` loops it forever
(Lab 2 breaks exactly this, on purpose).

---

## 3. Writing your first unit (the lab's spine)

A user service that runs a long job with supervision and a memory cap —
the M18 watchdog, productionized:

```ini
# ~/.config/systemd/user/hello.service
[Unit]
Description=Hello — my first user service
After=network-online.target

[Service]
Type=simple
ExecStart=%h/bin/hello-loop.sh
Restart=on-failure
RestartSec=5
MemoryMax=200M

[Install]
WantedBy=default.target
```

Read the differences from system units: `%h` is the specifier for your
home dir (no absolute paths that break if you move); `WantedBy=
default.target` is the *user* manager's default target (its
multi-user equivalent). The specifiers worth knowing: `%h` home,
`%u` username, `%i` instance name (for templated units —
`@`-suffixed, recognition level).

Then the lifecycle (all user-mode, no sudo):

```console
$ mkdir -p ~/.config/systemd/user && nano hello.service   # write it
$ systemctl --user daemon-reload                          # re-read definitions
$ systemctl --user enable --now hello.service             # start + persist
$ systemctl --user status hello.service                   # five zones, your unit
$ journalctl --user -u hello.service -n 20                # its logs, already flowing
```

`daemon-reload` after *every* unit-file edit — systemd caches
definitions; without the reload, you're editing a file it isn't
reading (the #1 beginner unit-file bug, and Lab 2 reproduces it).

---

## 4. Hardening directives (the least-privilege echo)

Units can run *tightly* — M13/M14's least-privilege, expressed to the
process supervisor:

```ini
[Service]
User=svc-notebooks            # run as this user, not root
DynamicUser=yes               # or: ephemeral UID per start
NoNewPrivileges=true          # block privilege escalation from inside
ProtectSystem=strict          # /usr,/boot,/etc read-only
ProtectHome=read-only         # home invisible for writing
PrivateTmp=true               # private /tmp (no cross-service snooping)
ReadOnlyPaths=/srv/datasets   # explicit read-only carve-outs
```

You'll *meet* these in shipped units (open `systemctl cat ssh` on
newer Ubuntu and read its hardening block) long before you write them.
The skill for now: read a hardened unit and say *what it's protecting*.
The DS server translation: the inference daemon runs as its own user,
read-only on datasets, private /tmp, memory-capped — every line maps to
a policy a security reviewer asks for (M25's echo).

---

## 5. Editing shipped units the supported way

Never hand-edit `/lib/systemd/system/*` (M16: package updates own it).
The supported patterns:

```console
$ sudo systemctl edit ssh            # drop-in override: /etc/systemd/system/ssh.service.d/override.conf
$ sudo systemctl edit --full ssh     # full copy to /etc, replaces vendor file
$ systemctl cat ssh                  # shows vendor file + your drop-in merged
```

`systemctl edit` opens a nearly-empty override file — you write only
the changed directives under a section header:

```ini
[Service]
MemoryMax=1G
```

Save → daemon-reload happens automatically → restart to apply. The
override survives package upgrades; `systemctl revert ssh` undoes it.
That's the whole maintenance story for services you didn't author.

---

## Exercises (lab-log.md)

1. `systemctl cat cron`, `systemctl cat ssh`: for each, list
   Type= (or infer), Restart=, User= (or note its absence → root), and
   one hardening directive. Two columns, two units.
2. Why does cron use `KillMode=process` while most services use the
   default (control-group-wide)? (Think: what does cron fork that
   should *survive* a stop — check `man 8 cron` if stuck.)
3. Write hello.service from §3, start it, paste status. Then change
   something via a *user drop-in* (`systemctl --user edit hello`,
   add `CPUQuota=10%`), daemon-reload, restart — and show `systemctl
   cat hello` displaying the merge.
4. The oneshot drill: write `backup.service` (Type=oneshot) whose
   ExecStart tars your lab-log into ~/backups. Run it with `systemctl
   --user start backup.service` — then explain why *enabling* it would
   be pointless without a timer (M19's cliffhanger).
5. Specifiers: in hello.service, replace `%h` with your literal home
   path. Does it still work? When would `%h` be the better choice?
6. (Stretch) Read `systemctl cat systemd-journald` and name three
   hardening directives you now understand. One sentence each.

## Check yourself before Lesson 4

- [ ] I can read any unit file's three sections and 10 key directives.
- [ ] I know my Type= decision tree (simple vs oneshot first).
- [ ] daemon-reload after edits is muscle memory.
- [ ] I can harden-read a unit and state what each directive protects.

## Further reading (official sources)

- `man systemd.service`, `man systemd.unit`, `man systemd.exec` (the
  hardening directive catalog), `man systemd.resource-control`
- freedesktop docs: https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
- Ubuntu Server Docs — systemd: https://ubuntu.com/server/docs
