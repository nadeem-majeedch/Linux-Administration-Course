# Lesson 1 — journald and journalctl

> Module 24 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1](../labs/lab-01-log-forensics.md)
> Up next: [Lesson 2 — classic logs & rotation](02-classic-logs-rotation.md)

---

## 1. Where service output actually goes

Run a service, then ask: what did it *say*? On modern Ubuntu the answer
starts with **systemd-journald** — a daemon that collects every message
sent to the system log: stdout/stderr of every service systemd starts,
kernel messages (via kmsg), and anything apps send to `/dev/log` (syslog).

Two design choices distinguish journald from the classic `/var/log/syslog`
file you may know from older Unix:

- **Binary, indexed storage.** The journal is a set of structured,
  indexed files under `/var/log/journal/` (persistent) or
  `/run/log/journal/` (volatile). Not plain text — which is why you
  never `grep /var/log/journal/*` directly; you query with
  `journalctl`.
- **Structured metadata.** Every entry carries fields beyond the text:
  `_PID` (writer's process ID), `_SYSTEMD_UNIT` (which unit wrote it),
  `PRIORITY` (level), `_HOSTNAME`, timestamps with microsecond
  precision. The index over those fields is what makes
  "everything this service said since boot" a single command instead
  of a grep lottery.

Your own user services from [M20](../../../M20-systemd-services/content/README.md)
land here too: every line the hello service printed went to the journal,
tagged with `--user` scoping. That's the thread this module pulls.

## 2. Volatile vs persistent — a five-minute check

Whether the journal survives reboot depends on storage mode:

```console
$ ls /var/log/journal          # exists? → persistent
$ journalctl --disk-usage      # total size of archived journals
Archived and active journals take up 40.0M in the file system.
```

- **Volatile** (`/run/log/journal/`): lost at reboot. Default when
  `/var/log/journal/` doesn't exist.
- **Persistent**: survives reboot; capped by size (`SystemMaxUse=`,
  default ~10% of the filesystem) and time (`MaxRetentionSec=`,
  default: keep until size cap forces deletion).

Ubuntu Desktop ships persistent by default; minimal/WSL2 images often
start volatile. **DS relevance:** a training script that crashes
overnight is only diagnosable in the morning if the journal *kept* its
words. Check persistence before the first long job, not after the
first lost crash. (Making it persistent — `sudo mkdir -p
/var/log/journal && sudo systemctl restart systemd-journald` — is an
admin one-liner, noted for completeness; the labs work in either mode.)

## 3. The queries that matter

Learn these seven and journalctl pays rent forever. (All are read-only.)

```console
$ journalctl -u hello.service          # everything one unit said
$ journalctl -u hello.service -f       # ...and keep watching (-f = follow)
$ journalctl -b                        # this boot only (-b -1 = previous boot)
$ journalctl -p err..alert             # priority range: err, warning...
$ journalctl --since "2026-09-15 20:00" --until "2026-09-15 23:00"
$ journalctl -g "OOM|out of memory"    # regex on message text (grep-style)
$ journalctl -u jupyter.service -o json-pretty   # structured fields, machine-readable
```

Reading the output — one entry, annotated:

```
Sep 15 21:04:11 ds-lab hello.service[2341]: run #12 finished in 0.3s
└── date/time          └── host    └── unit + PID      └── message text
```

Combinations do the diagnosing: *which* unit, *when*, *how bad*:

```console
$ journalctl -u jupyter.service -b -p warning.. --no-pager | tail -20
```

`-p warning..` means "warning and worse" — the range syntax walks
*up* severity. `--no-pager` (or piping) when you're feeding another
command; the [M08](../../../M08-text-processing/content/README.md) tools
apply to journal output exactly as to any text stream.

### Priority levels — the shared vocabulary

| Level | Keyword | Meaning in practice |
|---|---|---|
| 0 | emerg | System unusable |
| 1 | alert | Act immediately |
| 2 | crit | Critical condition |
| 3 | err | Errors — failed actions |
| 4 | warning | Weird but continuing |
| 5 | notice | Normal but notable |
| 6 | info | Routine messages |
| 7 | debug | Developer detail |

Two habits: (1) `-p err..` first — most incidents live at err and
above; (2) debug spam is normal in healthy logs; *absence* of
info-level lines is often the real anomaly (is it even running?).

## 4. User journals — your services, no sudo

Everything so far works without root for **your own units** — a
deliberate systemd feature (user journal namespace). Two views:

```console
$ journalctl --user -u hello.service    # your user manager's units
$ journalctl _UID=$(id -u)              # everything your UID wrote, system-wide
```

The first answers "what did my service say"; the second answers "what
has my account been doing" — including your cron jobs
([M19](../../../M19-scheduling-cron-timers/README.md)) and plain
processes. On shared DS servers this is the difference between
self-service debugging and filing a ticket for every stray error.

## 5. Watching an event live

The reflex to build: when anything happens, start a follower *before*
reproducing the problem.

```console
# Terminal 1: watch everything warning-and-worse, live
$ journalctl -f -p warning..

# Terminal 2: trigger the event
$ systemctl --user restart hello.service

# Terminal 1 now shows the restart's messages as they land
```

This is the "evidence before verdict" rule from
[M21's diagnosis ladder](../../../M21-networking-fundamentals/content/README.md)
applied to services: run the command that *watches*, then the command
that *acts*, and the causal story writes itself in timestamp order.

## 6. Data-science connections

- **"Training died overnight."** `journalctl -b -1 -u train.service -p
  err.. --since "23:00"` — one command reconstructs the death: OOM
  kill, exception traceback, disk-full write error. Lesson 4's
  incident method is built on this.
- **Jupyter's own voice.** A Jupyter server (however you start it)
  logs every kernel start, every HTTP request, every auth attempt.
  Users who can read those lines stop guessing "is it the network or
  the notebook?"
- **Structured output for your own tools.** `-o json-pretty` shows
  the machine view. When your pipeline logs *fields* (level, job_id,
  stage) rather than prose, a week of runs becomes queryable:
  `journalctl -g "job_id=exp42" -p err..`. Lesson 2 turns this into a
  habit for your scripts.
- **Kernel events are service events.** OOM kills and I/O errors
  reach the journal from the kernel side; `-g OOM` finds the evidence
  across all units at once.

## 7. Try it now (3 minutes, read-only)

1. `journalctl --disk-usage` — how big is your journal?
2. `journalctl -b -p warning.. --no-pager | tail -15` — what has your
   machine warned about *this boot*?
3. `journalctl --user -u hello.service --no-pager | tail -5` — your
   M20 service's last words. (No such unit yet? That output —
   "no entries" — is itself information; Lab 1 fixes it.)

Answers to the incident question aren't in this lesson — they're in
your journal.

## 8. Common mistakes

- Grepping `/var/log/journal/` files directly — binary; use `journalctl`.
- Forgetting `-b`: unbounded queries drown you in last month's noise.
- Confusing `--user -u X` with `-u X`: the former is your user
  manager's unit, the latter the system one. Wrong namespace = "no
  entries" confusion.
- Reading `warning` as failure. Warnings *accumulate* before failures;
  they're your early-warning radar, not noise to ignore.

> **Up next:** [Lesson 2 — /var/log, syslog, auth and kernel logs,
> levels, rotation](02-classic-logs-rotation.md) — the text-file half
> of the logging world that journald coexists with.
