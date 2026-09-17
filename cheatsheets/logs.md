# 10 — Logs

> Learn it: [M24 — Logs, journald & Monitoring](../modules/M24-logs-journald-monitoring/content/README.md) ·
> Lookup, not understanding.

## journald — the modern store

| Command | Purpose | Key options / examples |
|---|---|---|
| `journalctl` | everything, oldest first | `-e` jump to end · `-f` follow (tail -f) · `-r` reverse |
| `journalctl -u UNIT` | one service | `-u nginx -u php-fpm` (repeated = OR) |
| `journalctl -u UNIT --since -1h` | time-windowed | `--since today` · `--since "2026-03-01" --until "2026-03-02"` |
| `journalctl -p err` | priority filter | `emerg alert crit err warning notice info debug` |
| `journalctl -k` | kernel ring | `-k -g oom` post-mortem on OOM kills |
| `journalctl _UID=$(id -u)` | by identity | `_PID=` · `_COMM=` (command name) |
| `journalctl --disk-usage` | journal size | pair with `--vacuum-*` below |
| `journalctl -b` | this boot | `-b -1` previous boot — rebooted-after-crash forensics |
| `journalctl -g PATTERN` | grep inside the journal | `-g 'segfault\|oom'` |

⚠️ Never `grep` inside `/var/log/journal/` — entries are binary,
compressed, and split across files. `journalctl` gives structured
fields and boot/time slicing that raw grep cannot.

Volatile vs persistent: without `Storage=persistent` (or
`/var/log/journal` existing), the journal lives in
`/run/log/journal` and **dies at reboot**. Ubuntu Server keeps it
persistent by default.

## Classic `/var/log`

| File | Holds |
|---|---|
| `/var/log/syslog` | the general feed (non-journal daemons) |
| `/var/log/auth.log` | logins, sudo uses, sshd decisions |
| `/var/log/kern.log` | kernel messages |
| `/var/log/nginx/`, `/var/log/postgresql/` | per-app dirs (access/error logs) |
| `/var/log/unattended-upgrades/` | what auto-patching did |

| Command | Purpose | Example |
|---|---|---|
| `tail -f FILE` | follow | `tail -f /var/log/syslog` |
| `grep PATTERN FILE` | filter | `grep 'Failed password' /var/log/auth.log` |
| `zgrep` / `zless` | rotated `.gz` files | `zgrep CRON /var/log/syslog.2.gz` |

## Log levels (what severity *means*)

Use them when your app logs, not just when reading:

| Level | Meaning | Operational response |
|---|---|---|
| emerg/alert/crit | system-level damage | page someone |
| err | failed operation | investigate today |
| warning | degraded, still working | watch |
| notice/info | normal significant events | context |
| debug | developer detail | off in production (noise is a cost) |

## Rotation

`logrotate` handles `/var/log` files (config:
`/etc/logrotate.conf` + `logrotate.d/`): rotate → compress →
delete-after-N. For the journal:

```console
$ sudo journalctl --vacuum-time=7d     # keep a week
$ sudo journalctl --vacuum-size=500M   # or cap by size
```
Permanent caps: `MaxRetentionSec=` / `SystemMaxUse=` in
`/etc/systemd/journald.conf` (or a drop-in). ⚠️ Never `rm` journal
files directly — vacuum is the tool.

## Monitoring in the same breath

| Command | Read |
|---|---|
| `free -h` | `available` column is the honest memory number |
| `df -h` | filesystem fullness — pair with `du -xsh /* \| sort -h` to find the eater |
| `uptime` | load vs cores |
| `vmstat 1` | `wa` column = disk wait; `si/so` = swap churn |
| `systemctl --failed` | what broke at a glance |

The daily glance: `systemctl --failed` + `df -h` + `journalctl -p
err --since today`.

## Method rules that outlive this sheet

1. **Journal first, unit file second** — read what happened before
   reading what was configured.
2. Quote the decisive line in your incident note; a fix without its
   evidence line can't be reviewed.
3. Logs are evidence: never `rm` them to "clean up" — vacuum,
   rotate, or leave them.
