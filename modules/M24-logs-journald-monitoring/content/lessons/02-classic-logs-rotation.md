# Lesson 2 — Classic Logs, Levels and Rotation

> Module 24 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 2](../labs/lab-02-live-tail-circuit.md)
> Up next: [Lesson 3 — the monitoring toolkit](03-monitoring-toolkit.md)

---

## 1. The two logging worlds

Lesson 1's journal is modern; the text files under `/var/log` are the
classical world that predates it — and both live on every Ubuntu
machine *simultaneously*. Many daemons write to the journal; some
also (or only) write classic text files; the kernel has its own ring
buffer. An administrator reads **both worlds** without blinking. The
mapping to memorize:

| Question | Journal answer | Classic answer |
|---|---|---|
| What did service X say? | `journalctl -u X` | grep `/var/log/syslog` |
| Who logged in / sudo'd? | `journalctl -u ssh`, `_COMM=sudo` | `/var/log/auth.log` |
| What did the kernel complain about? | `journalctl -k` | `dmesg` (live ring buffer) |
| What did a *package* install log? | `journalctl -t apt` | `/var/log/apt/history.log` |

This lesson tours the classic half; the querying skills (grep, cut,
sort, uniq, tail -f) come straight from
[M08](../../../M08-text-processing/content/README.md) — logs are the
killer app for text-processing fluency.

## 2. The /var/log tour

Read-only reconnaissance — most need sudo to read:

```console
$ ls -la /var/log/            # the lay of the land
$ sudo tail -20 /var/log/syslog          # general system log (rsyslog)
$ sudo tail -40 /var/log/auth.log        # logins, sudo, ssh auth events
$ sudo tail -20 /var/log/dpkg.log        # package installs/removals, with timestamps
$ sudo tail -20 /var/log/apt/history.log # apt transactions, human-formatted
$ sudo dmesg | tail -20                  # kernel ring buffer (no sudo on Ubuntu desktop defaults)
```

What each is *for*:

- **`/var/log/syslog`** — the general firehose (rsyslog's output).
  Anything syslog-aware lands here, including much of what journald
  forwards. First stop for "when did X happen, system-wide?"
- **`/var/log/auth.log`** — authentication and privilege events:
  logins, sudo usage, SSH accepted/failed attempts, user
  additions. The forensic log for "who did what, when?" — and the
  log you'll check on shared DS servers before trusting a mysterious
  file's provenance.
- **`/var/log/kern.log`** — kernel messages, duplicated from
  `dmesg`'s ring buffer. OOM kills and I/O errors surface here.
- **`/var/log/dpkg.log` & `apt/history.log`** — the machine's
  *change history*: what was installed or upgraded, and exactly when.
  "It broke after Tuesday" becomes "it broke after the Tuesday
  upgrade of X" — that's a root-cause lead, not a coincidence.
- **`/var/log/cron.log` / journal** — cron job execution (Ubuntu
  logs cron to syslog by default; jobs' own output is emailed to the
  local user or redirected — [M19](../../../M19-scheduling-cron-timers/README.md)).

```console
$ sudo grep "sudo" /var/log/auth.log | tail -5      # recent privilege use
$ sudo grep "CUDA\|oom\|segfault" /var/log/kern.log # kernel-side drama
$ sudo grep " install " /var/log/dpkg.log | tail -10  # recent installs
```

## 3. dmesg — the kernel's diary

`dmesg` prints the **kernel ring buffer**: hardware detection at boot,
device errors, OOM kills, filesystem complaints. It's a *ring* — old
entries fall off as new ones arrive — and it starts at boot, so it's
the log of record for "what did the kernel think happened?"

```console
$ dmesg | tail -20                 # latest kernel messages
$ dmesg --level=err,warn           # filter by level (newer util-linux)
$ sudo dmesg -T | grep -i "out of memory"    # -T = human timestamps
```

OOM kills deserve special attention for DS work: when the kernel
kills your training process for hogging RAM, the evidence — process
name, PID, memory totals — appears here and in the journal
(`journalctl -k -g oom`). Lesson 4's incident #2 rehearses reading it.

## 4. Log levels — one vocabulary, three implementations

Lesson 1's priority table (emerg→debug) is the shared standard. You'll
meet it in three costumes:

1. **journald**: numeric `PRIORITY` field, filtered with `-p`.
2. **rsyslog text files**: levels embedded per-line via syslog
   facility/severity (`authpriv`, `kern`, `daemon`...).
3. **Your applications**: whatever the developer prints — which is
   where *you* come in (§6).

The professional habit: **one level per line, every line.** A log you
can filter by severity is a tool; a wall of undifferentiated print()
output is archaeology.

## 5. Rotation and retention — why logs don't grow forever

Logs must grow forever, or be deleted forever — so systems
**rotate**: rename the active file, start a fresh one, compress and
expire the old.

```console
$ ls -la /var/log/ | grep syslog
-rw-r----- 1 syslog adm  412K Sep 15 21:00 syslog
-rw-r----- 1 syslog adm  2.1M Sep 14 23:59 syslog.1        # previous period, rotated
-rw-r----- 1 syslog adm  180K Sep 07 23:59 syslog.2.gz      # older, compressed
```

The machinery is **logrotate**, configured per-log-file under
`/etc/logrotate.d/`:

```console
$ cat /etc/logrotate.d/rsyslog
/var/log/syslog
{
        rotate 7
        daily
        missingok
        notifempty
        delaycompress
        compress
        postrotate
                ...
        endscript
}
```

Reading it: `daily` rotate, keep `7`, compress old ones, skip empty
files. Same pattern for journald's size/time caps from Lesson 1.
**Retention is a policy decision** ("keep 30 days of auth logs for
audit") implemented by config — and on shared servers, a *quota*
question: logs share the disk with datasets.

**DS connection:** your experiment logs follow the same physics.
A training script appending to `train.log` for a month without
rotation will eventually fill a disk (Lesson 4, incident #3).
Rotate by size or date — or log to the journal with `systemd-cat`
and inherit journald's caps for free:

```console
$ ./train.py 2>&1 | systemd-cat -t train -p info   # → journalctl -t train
```

## 6. Application logs — writing logs worth reading

Whether output goes to journald (services), a file (batch jobs), or a
terminal (quick scripts), the *content* rules are identical. The
greppable log contract, adapted from M08's pipeline thinking:

```text
2026-09-15T21:04:11+00:00 INFO  train epoch=3 loss=0.241 lr=1e-4
2026-09-15T21:04:41+00:00 ERROR train epoch=3 cuda_oom=True free_gb=0.4
```

- **ISO-8601 timestamp** — sorts lexically, unambiguous, timezone-stamped.
- **UPPERCASE level** — `grep -E " ERROR|CRIT "` works forever.
- **key=value pairs** — machine-extractable with grep -o or awk
  without regex gymnastics.
- **One event per line** — multiline tracebacks get folded (or
  tagged `trace_begin`/`trace_end`).

Python's `logging` module does all of this in three lines, and
Jupyter's server logs already follow the pattern — read them in
[Lab 2](../labs/lab-02-live-tail-circuit.md) and notice how findable
one request is among thousands.

## 7. Try it now (5 minutes, read-only)

1. `sudo tail -5 /var/log/auth.log` — your last sudo events. (The
   one that says `COMMAND=...` for *this session* is you, now.)
2. `sudo grep -c "session opened" /var/log/auth.log` — count a thing
   across the whole file: text tools on real logs.
3. `ls /var/log/*.gz | head -3` — find three rotated files; you've
   now *seen* rotation.
4. `dmesg --level=err,warn | tail -5` — any kernel complaints this
   boot? (Laptops: expect battery/ACPI chatter — read *patterns*, not
   single lines.)

## 8. Common mistakes

- Editing or deleting files in `/var/log` — they're system records;
  diagnose, never tidy. (Disk-full from logs → Lesson 4, incident #3
  shows the *policy* fix.)
- Reading `syslog` when you mean `auth.log` (or vice versa) — pick by
  *question*: system events vs human/privilege events.
- Ignoring rotated files — yesterday's crash is in `syslog.1` or
  `syslog.2.gz` (`zgrep` searches compressed files directly).
- Treating timestamps as decoration. The first diagnostic question is
  always "when?", and every correlation — deploy ↔ error, mount ↔
  failure — is a timestamp join.

> **Up next:** [Lesson 3 — the monitoring toolkit](03-monitoring-toolkit.md):
> uptime, free, vmstat, iostat, sar — reading what the system is
> *doing*, not just what it *said*.
