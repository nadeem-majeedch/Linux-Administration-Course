# Lesson 2 — systemctl: Operating Services (and Your Own)

> Module 20 · Unit 6 · Difficulty: Advanced
> Reading time: ~35 min · Lab: [Lab 1](../labs/lab-01-service-circuit.md), [Lab 2](../labs/lab-02-break-and-fix.md)
> Prerequisites: [Lesson 1](01-systemd-units-concepts.md)

> 🟡 **Safety tier:** inspection everywhere; `start/stop/restart` on
> **your own VM**; on shared systems, `systemctl --user` manages *your*
> units without touching anyone else's — that's exactly what this
> lesson builds.

---

## 1. The verb vocabulary

systemctl's verbs map to real operations — learn them as *actions on a
process tree*, not magic words:

```console
$ systemctl status ssh        # 1. LOOK — always first (below)
$ systemctl start ssh         # spawn it now
$ systemctl stop ssh          # SIGTERM the process tree (M18's ladder, automated)
$ systemctl restart ssh       # stop+start in one go (drops connections!)
$ systemctl reload ssh        # re-read config WITHOUT dropping (if supported)
$ systemctl reload-or-restart ssh   # reload if possible, else restart
```

`reload` vs `restart` is an operational distinction that matters: for
nginx/ssh-style daemons, reload applies config changes while keeping
every established connection. When you're remote *through* the service
you're fixing, reload is how you avoid locking yourself out (Lab 1
drills this with ssh deliberately).

The question verbs:

```console
$ systemctl is-active ssh     # running?        → active/inactive/failed
$ systemctl is-enabled ssh    # at boot?        → enabled/disabled/…
$ systemctl is-failed ssh     # crashed state?
```

And the inventory verbs:

```console
$ systemctl list-units --type=service --state=running   # what's up now
$ systemctl list-unit-files --type=service              # what exists + enabled state
$ systemctl list-units --failed                          # THE morning command: anything broken?
```

`list-units --failed` on any server you inherit — it's the fastest
"what's wrong here" signal in the entire toolset.

---

## 2. Reading status output (the diagnostic core)

`systemctl status <unit>` is a diagnosis in five zones — learn to read
it like a chart:

```console
$ systemctl status cron
● cron.service - Regular background program processing daemons
     Loaded: loaded (/lib/systemd/system/cron.service; enabled; preset: enabled)
     Active: active (running) since Mon 2026-03-10 09:00:03 UTC; 2h 4min ago
   Main PID: 812 (cron)
      Tasks: 1 (limit: 4632)
     Memory: 2.5M
        CPU: 180ms
     CGroup: /system.slice/cron.service
             └─812 /usr/sbin/cron -f -P
Mar 10 09:00:03 labvm systemd[1]: Started cron.service...
```

Zone by zone:

1. **The dot** — green ● active, white ○ inactive, red ● failed. Color
   first, then confirm with text (accessibility: `--no-pager` keeps
   color decisions predictable in scripts).
2. **Loaded line** — where the unit file lives + enabled state + the
   `preset` default. A unit "not found" here means a typo in the name.
3. **Active line** — state since *when* (crashes show as "since 30s
   ago" repeatedly — the restart-loop tell) + the restart count.
4. **Main PID / CGroup** — which process (M18 tools apply directly:
   `ps -p 812`, `/proc/812/…`) and its supervision group.
5. **The log tail** — the last journal lines for this unit. Usually the
   answer is already here.

**The failed-service drill** (Lab 2 breaks services so you can do this
for real): status → Active line says `failed` with exit code → log
tail shows the reason → `journalctl -u <unit> -n 50` for the full
story → fix → `systemctl restart` → re-status. Five moves, every time.

---

## 3. journalctl per unit (the 20% you need today)

M24 owns logging deeply; services need the per-unit slice now:

```console
$ journalctl -u ssh --no-pager -n 20        # last 20 lines for one unit
$ journalctl -u cron -f                     # follow live (tail -f, systemd edition)
$ journalctl -u ssh --since "1 hour ago" --no-pager
$ journalctl -u myunit -p err --no-pager    # errors only (priority filter)
```

Everything a service writes to stdout/stderr lands here automatically —
no logger configuration, no "where does my daemon's output go" mystery.
That single fact is why unit files stay so clean (Lesson 3).

---

## 4. User services: systemd without root

`systemctl --user` manages a *per-user* manager — same machinery, your
own unit namespace, zero sudo. This is the data scientist's sweet spot:

```console
$ systemctl --user list-units --type=service      # your private services
$ systemctl --user start my-job.service
$ journalctl --user -u my-job.service             # your private journal slice
```

**The one catch — lingering.** User services normally die with your
last session (same SIGHUP problem as M18's nohup, one level up).
Lingering keeps *your* manager alive after logout:

```console
$ loginctl show-user $USER -p Linger     # no → services die at logout
$ sudo loginctl enable-linger $USER      # yes → they survive (own VM)
```

With lingering on, `systemctl --user enable --now my-long-job.service`
survives reboots *and* your logout — the durable answer to M18's
"overnight SSH job" question, without cron and without root. The trade:
it consumes your resource quota whether you're logged in or not —
enable it deliberately.

**Limits without root:** user units can cap themselves:

```ini
[Service]
MemoryMax=2G
CPUQuota=50%
```

Recall M18's memory-hog experiment — `MemoryMax=2G` is the systemd
expression of "cap this job before it caps the server," available to
you as a plain user. (Resource control specifics: `man
systemd.resource-control`.)

---

## 5. The maintenance workflow (assembling the verbs)

The rhythm you'll actually use on any service, anywhere:

```console
$ systemctl status myapp                    # 1. look
$ systemctl is-enabled myapp                # 2. boot question
$ journalctl -u myapp -n 50 --no-pager      # 3. recent story
$ sudo systemctl restart myapp              # 4. the change (own VM / authorized)
$ systemctl status myapp                    # 5. verify — never skip
$ journalctl -u myapp --since "-2 min"      # 6. did it *stay* healthy?
```

Step 6 is the professional tell: a restart that "worked" means active
*and* still active after minutes, logs clean after the restart lines.
Lab 2's break-and-fix circuits force all six steps until they're
reflexes.

---

## Exercises (lab-log.md)

1. Run `systemctl list-units --failed` right now. Empty? Paste it
   anyway — "all green" is a finding, and now you know where to look.
2. Pick a running service, record its status output, and annotate all
   five zones in the margin. Include Main PID and cross-check it with
   `ps -p <pid> -o pid,ppid,cmd` — one tree, two views.
3. reload vs restart: `systemctl show ssh -p ExecReload` — does ssh
   support reload? What does its ExecReload actually run? (One
   sentence on why reload support is a per-service choice.)
4. User manager: `systemctl --user list-units --type=service` — what's
   there before you create anything? (ubuntu's default user units.)
   Check your Linger status and explain what it would take to change.
5. Write the six-step maintenance workflow as a shell function
   `svc <name>` (echo each step's command for now — automation comes
   in M10/M19).
6. (Stretch) `journalctl --user -u <any unit> --since today` vs
   `journalctl -u ssh --since today` — one works, one errors. Why the
   user/system split in journal access? (Hint: privacy + permission
   model, M12 echo.)

## Check yourself before Lesson 3

- [ ] I read status in five zones and know the restart-loop tell.
- [ ] reload vs restart is a decision, not a synonym.
- [ ] I can create and keep alive a *user* service with lingering.
- [ ] My maintenance rhythm ends with "still healthy minutes later."

## Further reading (official sources)

- `man systemctl`, `man systemd.special`, `man loginctl`
- freedesktop docs: https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
- Ubuntu Server Docs — service management: https://ubuntu.com/server/docs
