# Module 24 Troubleshooting — Log & Monitoring Symptoms → Fixes

> Ten patterns, ordered by how often they hit real users. Each:
> **symptom → diagnosis → fix → prevention**. All diagnosis commands
> are safe (read-only) on any machine you admin; fixes stay in
> user/own-VM scope. The six-step method lives in
> [Lesson 4](lessons/04-incident-methodology.md); this page is its
> symptom index.

## 1. "The service won't start"

**Diagnosis:**
```console
$ systemctl --user status sync.service      # Result: exit-code? signal?
$ journalctl --user -u sync.service -b --no-pager | tail -15
```
The journal's last lines usually name the cause verbatim: missing
file, permission denied, Python traceback, port taken.
**Fix:** address the named cause (`daemon-reload` after unit edits).
**Prevention:** `systemd-analyze verify` units before installing;
a health-check line that watches `is-active`.

## 2. "My job died overnight with no explanation"

**Diagnosis:** the explanation is almost always in a log you haven't
read yet:
```console
$ journalctl --user -u train.service -b -1 --no-pager | tail -15   # previous boot!
$ journalctl -k -g "oom|out of memory" --no-pager | tail -5
```
`-b -1` if the machine rebooted; kernel view for OOM kills; the
service's own last lines for tracebacks.
**Fix:** resource caps (MemoryMax), smaller batches, reschedule.
**Prevention:** RSS-trend in logs (see C5) + caps so *your* job dies
first, on purpose, with a message.

## 3. "Disk full (or nearly)"

**Diagnosis:** filesystem → directory → decision:
```console
$ df -h; df -i                      # space AND inodes can be "full"
$ du -h --max-depth=1 ~ | sort -rh | head
```
Inode exhaustion (`df -i` at 100%) with free space is the sneaky
variant — millions of tiny files (unpacked datasets, old checkpoints).
**Fix:** own files only: caches, scratch, rotated-out logs. Never
"clean up" `/var/log` or others' data.
**Prevention:** health check's `df -h` line; rotation for anything
that appends; quota awareness on shared servers.

## 4. "CPU is high — something's wrong!"

**Diagnosis:** utilization is not yet a problem; get saturation and
identity:
```console
$ uptime                            # load vs nproc; 1/5/15 trend
$ ps -eo user,pid,%cpu,%mem,etime,cmd --sort=-%cpu | head -6
```
**Fix:** if it's your runaway: verify the command line, then M18's
ladder (preview → TERM → verify). If it's a teammate's legitimate
job: renice/coordinate — *not* kill.
**Prevention:** announce long jobs; baseline "normal" so anomalies
are visible; nice batch work by default.

## 5. "Memory pressure / the OOM killer visited"

**Diagnosis:**
```console
$ free -h                           # available shrinking? swap climbing?
$ vmstat 2 5                        # si/so activity
$ journalctl -k -g oom --no-pager | tail -5    # who was chosen, when
```
**Fix:** the killed process gets a cap or a smaller footprint; check
for leaks (restarting with a memory profile).
**Prevention:** MemoryMax/user-unit caps; `watch free -h` during
first runs; the growth-slope habit (C5).

## 6. "Logs stopped updating"

**Diagnosis:** is the *writer* dead, or the *reader* looking wrong?
```console
$ systemctl --user is-active sync.service
$ journalctl --user -u sync.service -n 5 --no-pager   # last words + when
$ df -h /var                          # full disk stops many writers
```
A service can also be alive-but-hung: last entry hours old + active
status = hang; pair with `ps` CPU state (M18).
**Fix:** restart after fixing the named cause (full disk: #3 first).
**Prevention:** heartbeats (Lab 2's beat.log pattern) + the absence
alarm (C8) — silence *is* a signal, monitor it.

## 7. "Journal is full of noise; I can't find my event"

**Diagnosis:** you're probably querying too wide. Narrow along three
axes: unit (`-u`/`-t`), time (`--since/--until`, `-b`), priority
(`-p`).
```console
$ journalctl --user -u sync.service --since "-2 hours" -p warning.. --no-pager
```
**Fix:** filters, not scrolling; `-o json-pretty` + jq for structured
hunts.
**Prevention:** write events with tags and levels (Lab 2's logger)
so *your* future queries have handles to grab.

## 8. "I/O is slow — the machine feels bogged down"

**Diagnosis:**
```console
$ vmstat 2 5                         # wa% high? b>0 sustained?
$ iostat -x 2 5                      # which device: %util, await
$ ps -eo pid,stat,wchan,cmd | grep -E " D "    # who's blocked on I/O
```
High `wa` with one pegged device = storage-bound, not CPU-bound —
different fix entirely (batch reads, faster disk, schedule heavy I/O
off-peak).
**Fix:** move/reshape the I/O; on shared servers, coordinate the
heavy loaders.
**Prevention:** baseline iostat numbers per server (C6's latency
story); sequential-read habits over random small reads.

## 9. "Authentication weirdness on a shared box" (read-only skill)

**Diagnosis (admin turf — know it, don't do it uninvited):**
```console
$ sudo grep "Failed password" /var/log/auth.log | tail -5
$ last | head -10                    # recent login sessions
```
Your part as a *user*: notice your own session oddities and report
with timestamps; never investigate others' accounts yourself.
**Fix/prevention:** keys over passwords (M22), report verbatim lines
+ timestamps to the admin. **The course rule stands:** on shared
machines, read *your* evidence and escalate the rest.

## 10. "It was slow at some point yesterday" (the history hunt)

**Diagnosis:** live-only tools can't help — you need recorded history:
```console
$ sar -u -s 13:50:00 -e 14:30:00     # CPU over the window
$ sar -r                             # memory, same idea
$ journalctl --since "2026-09-15 13:50" --until "2026-09-15 14:30" -p warning..
```
No sysstat history? The journal still has the *event* view — errors
and warnings carry timestamps too.
**Fix:** whatever the window shows (cron collision, backup job, cron
storm).
**Prevention:** enable sysstat on your own machines; schedule heavy
jobs apart; keep the health-kit baseline so "slow" has a reference.

## When to escalate

| Evidence in hand | Escalate to |
|---|---|
| Service failing at system level, journal quotes it | Admin, with `journalctl -u X` excerpt + timestamps |
| Disk ≥ 85% and it's not your files | Admin/quota owner — with `df -h` output, not adjectives |
| Recurring OOM on shared GPU server | Resource owner: the growth table (C5) is the exhibit |
| Auth anomalies | Admin immediately; timestamps and verbatim lines only |

> The escalation table is the method's last step wearing a different
> coat: evidence makes tickets short, and short tickets get fixed.
