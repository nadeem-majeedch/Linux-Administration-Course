# Lab 1 — The Service Circuit: Inspect, Operate, Create

> Module 20 · Unit 6 · Difficulty: Advanced
> Time: ~50 min · Environment: **your own VM** (system ops) + user units
> Prerequisites: [Lessons 1–3](../lessons/01-systemd-units-concepts.md)

Four stations, building from reading to operating to authoring. Every
command's output goes in `lab-log.md` — the transcript is the
deliverable.

## Station 1 — read the landscape (10 min, safe everywhere)

```console
$ systemctl get-default
$ systemctl list-units --type=service --state=running | head -10
$ systemctl list-unit-files --type=service --state=enabled | head -10
$ systemctl --failed                       # the morning command
```

**Record:** how many running services, how many enabled, and one
sentence on the difference between those two numbers (Lesson 1's
four-state table, in the wild).

## Station 2 — operate a real service (15 min, own VM)

We exercise ssh — deliberately, because *locking yourself out is the
real risk you should rehearse safely*:

```console
$ systemctl status ssh                     # 1. look (running? enabled?)
$ systemctl cat ssh                        # 2. read its definition: Type, Restart, User
$ sudo systemctl restart ssh               # 3. the operation
$ systemctl status ssh                     # 4. verify — "since" line updated?
$ sudo systemctl reload ssh || echo "no reload support"   # 5. does it support reload?
```

**Record:** the before/after Active lines, whether reload worked, and
the ExecReload command if it exists. Then the enabled-state experiment:

```console
$ sudo systemctl disable --now cron        # stop AND un-enable
$ systemctl is-active cron; systemctl is-enabled cron     # both inactive — evidence
$ sudo systemctl enable --now cron         # restore both
$ systemctl is-active cron; systemctl is-enabled cron
```

**Record:** the four answers (2×2) — you just visited one quadrant of
the table live.

## Station 3 — author a user service (15 min, no root)

```console
$ mkdir -p ~/bin ~/.config/systemd/user
$ cat > ~/bin/hello-loop.sh <<'EOF'
#!/bin/bash
# hello-loop.sh — a well-behaved foreground service (simple Type)
while true; do
  echo "$(date +%T) hello from systemd"
  sleep 5
done
EOF
$ chmod +x ~/bin/hello-loop.sh
$ ~/bin/hello-loop.sh & sleep 2; pkill -f hello-loop   # test it raw first
```

Then the unit (Lesson 3 §3's file — write it exactly):

```console
$ cat > ~/.config/systemd/user/hello.service <<'EOF'
[Unit]
Description=Hello — my first user service

[Service]
Type=simple
ExecStart=%h/bin/hello-loop.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
$ systemctl --user daemon-reload
$ systemctl --user enable --now hello.service
$ systemctl --user status hello.service    # the five zones, on YOUR unit
$ journalctl --user -u hello.service -n 6  # its logs, flowing
```

**Record:** status + journal excerpts. Then prove supervision (the
point of systemd):

```console
$ pkill -f hello-loop.sh                   # kill the process UNDER systemd
$ sleep 6; systemctl --user status hello.service   # ...and it's back (Restart=)
```

**Record:** the kill → respawn evidence. That pair of lines is the
entire pitch for services over cron-and-hope.

## Station 4 — lingering (10 min)

```console
$ loginctl show-user $USER -p Linger       # current state
$ sudo loginctl enable-linger $USER        # keep my user manager alive
$ loginctl show-user $USER -p Linger       # Linger=yes
```

**Record:** what changed, and one sentence each: (a) what would happen
to hello.service at logout *without* linger; (b) the resource cost of
keeping it.

## Wrap-up

1. Which verbs did you use with sudo and which with --user — and could
   Station 3 have been done on a shared server? (Yes — say why.)
2. Paste your `systemctl --user status hello.service` and annotate the
   five zones.
3. Skill transfer: write the Station-3 unit you'd write for M18's
   priority-clinic latency logger (`jupyter_sim.sh`). Don't run it —
   just the file.

## Done when

- [ ] All four stations' evidence in lab-log.md
- [ ] The 2×2 enable/active quadrants visited live
- [ ] Kill → respawn supervision proof captured
- [ ] Linger before/after + the two sentences
- [ ] The transfer unit file written
