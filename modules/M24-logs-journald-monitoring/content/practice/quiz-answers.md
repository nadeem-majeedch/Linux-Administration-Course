# Module 24 Quiz — Answer Key

> A/B are factual; C/D graded on reasoning. Command answers graded on
> "would it work if typed".

## Section A — journald

**A1.** The journal is **binary, indexed** storage — grep on it
yields binary-matches noise at best. `journalctl` gives (1) field-
aware queries (`-u`, `-p`, `-g`, `--since`) over the index and (2)
proper rendering of structured entries (timestamps, unit, PID).

**A2.** Volatile: `/run/log/journal/` — a tmpfs wiped at reboot.
Persistent: `/var/log/journal/` — survives reboot, subject to size
(`SystemMaxUse`) and retention caps. Reboot in volatile mode =
history gone; persistent mode = `journalctl -b -1` has something to
show.

**A3.** `journalctl -u train.service -b -1 -p err..` (order of flags
irrelevant; `-p err..` = err and worse).

**A4.** 4 = warning. The trailing `..` means "and above" — the range
includes every level more severe than warning (err, crit, alert,
emerg).

**A5.** (1) Wrong namespace: is the unit actually a *user* unit? Try
`journalctl -u sync.service` (system) vs `--user`. (2) Boot scope:
without `-b`, an old-unit-noise flood can hide today's lines — or the
unit name may be misspelled (tab-complete `systemctl --user list-units`).

**A6.** It emits each entry as a JSON object with **all structured
fields** (`__MONOTONIC_TIMESTAMP`, `_PID`, `PRIORITY`, custom
fields). Pipelines prefer it because parsing JSON is reliable;
parsing rendered prose is not.

## Section B — classic logs & rotation

**B7.** sudo events: `/var/log/auth.log` (`sudo: ... COMMAND=...`).
Upgrades: `/var/log/dpkg.log` (or `/var/log/apt/history.log`).

**B8.** The kernel **ring buffer** — fixed-size memory. Old entries
are overwritten as new ones arrive (which is why kernel evidence also
lands in the journal/kern.log if you need history).

**B9.** Seven rotations are kept — with `daily`, seven days of
history; the 8th-oldest is deleted each cycle. `compress` means the
older ones sit as `.gz` (possibly delayed one cycle by
`delaycompress`).

**B10.** The rotated files: `syslog.1` (plain) and, for older spans,
`syslog.2.gz` etc. — searched with `grep` and **`zgrep`**
respectively (zcat | grep also fine).

**B11.** Any two of: ISO-8601 timestamp (sorts lexically; timezone-
explicit); UPPERCASE level (trivially grep-able severity filter);
key=value fields (machine-extractable without regex gymnastics); one
event per line (line-oriented tools — grep/cut/awk — keep working).
Each earns its place because it preserves the *pipeline* property.

**B12.** It pipes the script's stdout/stderr **into the journal**
under tag `myjob`, inheriting journald's storage, indexing, and
rotation for free. Filter later with `journalctl -t myjob`.

## Section C — monitoring

**C13.** `free` = truly unused pages. `available` = free + reclaimable
cache — what can be handed to a new process without swapping. Low
`free` is healthy because Linux deliberately puts idle RAM to work as
page cache; *available* is the honest number.

**C14.** The trend: compare the 1-min vs 15-min load numbers (and
re-sample). Falling 1-min (e.g. 6.2 → 15-min 4) = spike passing,
queue draining; rising = queue growing. A single snapshot can't tell
those apart.

**C15.** `si/so` (swap-in/out per second) — activity there signals
real memory pressure even with cache present. The iowait column is
**`wa`**.

**C16.** `%util` — fraction of time the device had work (→ saturated
near 100%); `await` — average wait per request in ms (climbing await
+ high %util = requests queueing). (Accept r/s, w/s read/write rates
as context.)

**C17.** **Historical replay**: sar records samples over time, so you
can query windows that already ended ("what was CPU at 14:20?").
Requirement: the sysstat collector service enabled (off by default on
Ubuntu) — otherwise no data exists.

**C18.** `df -h` → which *filesystem/mount* is filling; then
`du -h --max-depth=1 <mount-point-path> | sort -rh | head` → which
directory inside it. Iterate one level deeper as needed.

## Section D — methodology & safety

**D19.** Stabilize/what-changed → precise symptom → broad-then-narrow
evidence → one hypothesis + killer test → fix and **verify** →
postmortem with prevention.

**D20.** Binary tests are cheap and *falsifiable*: `df -h` settles
"disk full?" in two seconds with a yes/no. Narrative theories anchor
attention; a passed/failed binary test breaks the anchor with
evidence.

**D21.** 3 copies, 2 different media, 1 offsite. The lab demo: after
deleting `panel.bin`, re-running the `--delete` mirror propagated the
deletion — the mirror matched the disaster. Only the point-in-time
*tar archive* still held the file. History ≠ mirror.

**D22.** (1) **Verify** the fix against the original symptom — re-run
the failing check and watch it hold for a sensible interval; (2) the
**postmortem** including the prevention line. A verified fix without
a postmortem leaves the class of incident alive.

## Bonus (Q23) — model answer

Commands: `uptime` (load vs nproc — is it *saturated*?), `ps -eo
user,pid,%cpu,%mem,etime,cmd --sort=-%cpu | head` (whose process,
doing what?), `vmstat 2 3` (is it CPU-bound `us`, or iowait `wa` —
very different stories at "90%"). The question to the teammate:
**"since when, and compared to what baseline?"** — plus, on shared
servers, "is a long job of mine/ours expected right now?" (High CPU
alone is not an incident; saturation + identity + timeframe is the
beginning of one.)

## Score guide

| Score | Meaning |
|---|---|
| 20–23 | Incident-ready — build Mini-Project E |
| 15–19 | Re-read flagged sections; redo the matching lab drill |
| < 15 | Repeat lessons 1–3; the labs will cement what reading didn't |
