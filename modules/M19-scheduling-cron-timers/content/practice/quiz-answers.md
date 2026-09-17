# Module 19 Quiz — Answer Key

> Reasoning graded; cron lines on "would cron accept and fire them".

## Section A — crontab

**A1.** minute (0–59), hour (0–23), day-of-month (1–31), month
(1–12 or JAN–DEC), day-of-week (0–7, 0/7 = Sunday).

**A2.** `15 7 * * 1-5 /path/to/job`

**A3.** The 13th of every month **and** every Friday — when both
day fields are restricted, cron ORs them. "Friday the 13th" needs
one day field restricted (`* * * * FRI`) plus a `[ "$(date +%d)"
= 13 ]` test in the command.

**A4.** `@daily` = `0 0 * * *` (exactly 00:00); `@reboot` = once at
startup. Problem: midnight is when every `@daily` job on every
server fires — load spikes and contention; stagger deliberately
(`0 2 * * *`, `30 2 * * *`, ...).

**A5.** It removes the *entire* crontab instantly, with no prompt
and no undo. Habit: `crontab -l > backup` before any destructive
crontab operation; `crontab -e` for edits, never `-r` reflexively.

**A6.** `crontab -e` goes through cron's machinery — it installs
atomically, signals cron to re-read, and syntax-checks lightly.
Direct spool edits may be silently ignored (permissions/format)
and leave cron serving the *old* table while you debug the new
one.

## Section B — the cron environment

**B7.** `/usr/bin:/bin`. Canonical failure: `python3` resolves to
the system interpreter without your venv/conda packages — or
user-local tools (`pip`, `~/.local/bin` scripts) aren't found at
all.

**B8.** Any four: cwd is `$HOME`; no rc files (`/bin/sh -c`);
bare environment (no exports, no conda, no `SSH_AUTH_SOCK`); no
tty (prompts hang); no `DISPLAY`.

**B9.** Runs the script with an *empty* environment through
`/bin/sh` — cron's poverty simulated in one command. If it
survives `env -i`, it doesn't depend on your shell — the property
cron-readiness actually is.

**B10.** `>> log 2>&1`: stdout appended to log, *then* stderr
duplicated to stdout's current destination (the log) — both land
in the file. `2>&1 > log`: stderr duplicated to stdout *first*
(the terminal — for cron: nowhere), then stdout redirected —
stderr is lost.

**B11.** cron mails it to the local user (the mail spool). Read:
`tail /var/mail/$USER` (or `mail` where installed). On minimal
VMs, no reader exists — but the spool file is plain text.

**B12.** cron's cwd is `$HOME`, so `./data/input.csv` resolves to
`~/data/input.csv` — possibly a different file, possibly none.
Fix: derive paths from the script location
(`BASH_SOURCE`/`SCRIPT_DIR`) or use absolutes; habit: never rely
on the caller's cwd (M11's cron-proofing).

## Section C — timers & production

**C13.** Advantages: `Persistent=true` (missed runs fire after
downtime); journal integration (output recorded without plumbing);
unit directives (ordering, timeouts, memory caps); `systemctl
list-timers` introspection. Cron wins for: one-line jobs (no unit
ceremony), universal environments (containers, BSD, macOS).

**C14.** The timer records its last trigger; if the machine was
down/asleep at trigger time, the job fires **once** at next
startup — not once per missed slot. Three missed nightlies = one
catch-up run.

**C15.**
```ini
# dq.service
[Service]
Type=oneshot
ExecStart=/home/ds/lab19/dq.sh /home/ds/lab19/sales.csv

# dq.timer
[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
```
(Plus `[Install] WantedBy=timers.target` on the timer for
`enable`.)

**C16.** The *timer* is the schedule; enabling the service just
runs the job once immediately (and never schedules anything) —
you armed the work, not the recurrence.

**C17.** The next several dates that expression will fire, parsed
by systemd itself. It validates *before* scheduling — the five
fields' or OnCalendar's meaning confirmed by the same engine that
will execute them (and it exposes the cron OR trap).

**C18.** `mkdir` is a single atomic syscall — create-or-fail with
no gap between check and act; a `touch`+`[ -f ]` pair races (two
jobs pass the check, both proceed). Released by the `trap ... EXIT`
cleanup, so failure paths don't strand it.

**C19.** The script's own log; the journal (`journalctl -u`);
`systemctl list-timers` (LAST column); the mail spool for cron's
unredirected output. Only the **absence alarm** catches the job
that *never ran* — every other source is silent when there's
nothing to log.

**C20.** (1) explicit `PATH` — carries its own environment;
(2) absolute/derived paths — no cwd dependence; (3) timestamped,
leveled logs on success *and* failure — silence is a bug;
(4) mkdir-lock + EXIT trap — no overlapping runs, no stranded
locks; (5) `set -euo pipefail` + idempotent steps — safe to
retry.

## Bonus (Q21) — model answer

1. `tail -20 /var/mail/$USER` — cron's unredirected errors
   (the job "stopped" often means "started failing"; the spool
   confesses).
2. `systemctl list-timers | grep <name>` (or `grep <name>
   /var/log/syslog`) — did it *fire* at all? Fires-with-errors vs
   never-fired are different diseases.
3. `journalctl --user -u <unit> --since "4 days ago" | tail` —
   the last good run vs the first bad one; diff the dates.
4. `crontab -l` + `ls -l /path/to/script` — the two silent
   saboteurs: the *other* admin's crontab edit, or the script/
   data moved out from under a working schedule.

(The order is the M24 method: evidence, timeline, then the
"what changed" pass — verdicts after, not before.)

## Score guide

| Score | Meaning |
|---|---|
| 18–21 | Scheduling fluency achieved — the capstone pipeline awaits |
| 14–17 | Re-read flagged sections; redo the matching lab phase |
| < 14 | Repeat lessons 1–2; the environment trap is non-negotiable |
