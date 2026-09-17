# 13 — cron & Scheduling

> Learn it: [M19 — Scheduling: cron & timers](../modules/M19-scheduling-cron-timers/content/README.md) ·
> Lookup, not understanding.

## crontab basics

| Command | Purpose | Notes |
|---|---|---|
| `crontab -e` | edit **your** crontab (the only edit path) | — |
| `crontab -l` | list | verify after editing |
| `crontab -l > ~/crontab.backup` | **back it up after every edit** | the undo for the next line |
| `crontab -r` | ⚠️ delete your whole crontab — no prompt, no undo | type `-e` by reflex, never `-r` |
| `sudo crontab -u bob -l` | view another user's | admin view |
| `ls /etc/cron.d/` | system job files | packager-managed too |

## The five fields

```text
┌──────── minute      0–59
│ ┌────── hour        0–23
│ │ ┌──── day-month   1–31
│ │ │ ┌── month       1–12 (jan-dec)
│ │ │ │ ┌ day-week    0–7  (0 and 7 = sunday)
* * * * * command-to-execute
```

| Expression | Fires |
|---|---|
| `0 3 * * *` | daily 03:00 |
| `*/10 * * * *` | every 10 minutes |
| `0 9 * * 1-5` | weekdays at 09:00 |
| `0 0 1 * *` | first of the month |
| `30 2 15 * *` | 02:30 on the 15th |

## The cron environment traps (works-in-my-shell, fails-in-cron)

| Difference | Consequence | Defense |
|---|---|---|
| minimal `PATH` (`/usr/bin:/bin`) | venvs, `~/.local/bin` invisible | **absolute paths** for the script *and* inside it |
| cwd = `$HOME` | relative paths land elsewhere | `cd "$(dirname "$0")"` or absolute everywhere |
| no shell rc files | aliases, conda init, exports absent | set what you need in the script itself |
| no tty | some tools behave differently | log everything (next row) |
| output mailed, not seen | silent failures for weeks | redirect on every line: `>> log 2>&1` |

```cron
0 3 * * * /home/ana/bin/nightly.sh >> /home/ana/logs/nightly.log 2>&1
```
The script must still exit non-zero on failure and the log line must
end with the status — **"it ran" is not "it worked."**

## Test-first schedule (the discipline)

```cron
*/10 * * * * /home/ana/bin/nightly.sh >> …log 2>&1   # week 1: observe
```
Then promote to the real `0 3 * * *`. A schedule that has never
fired under observation is a hope, not a schedule.

## systemd timers (the modern alternative)

```ini
# /etc/systemd/system/backup.timer        (or ~/.config/systemd/user/)
[Unit]
Description=Nightly backup

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true               # catches up if the machine was off

[Install]
WantedBy=timers.target
```
paired with `backup.service` running the actual job.

| Command | Purpose |
|---|---|
| `systemctl list-timers` | what fires when — next + last run |
| `systemctl start UNIT.timer` | activate |
| `journalctl -u UNIT.service` | the job's output |

**cron vs timer:** cron = simpler, universal, five fields everyone
reads; timers = `Persistent` catch-up, calendar flexibility,
per-job units in the journal. One-sentence justification is the
expected answer in reviews (Level 4).

## `at` — one-shot scheduling

```console
$ echo "/usr/local/bin/report.sh" | at 22:00
$ atq                       # queue
$ atrm 3                    # remove job 3
```

## Alternatives summary

| Need | Reach for |
|---|---|
| daily/weekly jobs | cron or timer |
| survives machine-off periods | **timer with `Persistent=true`** |
| one-shot later today | `at` |
| long-running, not scheduled | tmux / user unit |
| job must run as specific service identity | system unit, not cron |
