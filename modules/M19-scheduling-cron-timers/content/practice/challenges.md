# Module 19 Challenges — Scheduling

> Eight challenges under `~/lab19/`, user-level scheduling only.
> Every challenge ends in log-file evidence; every new schedule
> passes through the two-minute rule first. C5–C8 build the
> artifacts other modules will schedule (M24's health kit, M25's
> patch report, the capstone pipeline).

## C1 — The translation drill

Convert, both directions, with `systemd-analyze calendar`
verification for each: "every 20 minutes", "weekdays at 08:45",
"first Monday of the month at 06:00" (harder — one cron line + a
date test), "quarterly (Jan/Apr/Jul/Oct 1st)", "nightly at 23:30
but only Sundays". Ten total (five each way) into `lab-log.md`.

## C2 — The stagger plan

A teammate schedules five `@daily` jobs. Redesign them to spread
load: write the five cron lines (backup, cleanup, report, sync,
rotation) with staggered times, and one sentence each justifying
its slot (backup before sync; cleanup after both; report after
data lands...). The deliverable is *the reasoning*, not the
syntax.

## C3 — The scheduled cleanup, hardened

Write `cleanup.sh` (M11-grade: strict, logged, dry-run flag,
idempotent): removes files older than N days from
`~/lab19/scratch/` using `find -mtime` — with the safety triad:
absolute paths only (never `/`-rooted), a `--dry-run` default,
and an explicit allowlist root (refuse to run if the target
doesn't start with `$HOME/lab19/`). Schedule it `@daily`, prove
one run, then test the retention edge: create a 8-day-old file
(`touch -d '8 days ago'`), confirm the next run removes it and
logs the removal.

## C4 — The calendar validator drill

Find the trap before cron does: for each of these intended
schedules, state what the naive cron line *actually* does
(`systemd-analyze calendar` is your witness), then write the
corrected version: (a) "Friday the 13th, midnight" via
`0 0 13 * 5`; (b) "every 5 hours starting at 1am" via
`1 */5 * * *`; (c) "last day of the month" (no cron field for it —
date-test idiom required).

## C5 — The absence alarm, deployed

Take M24's `expected-runner.sh` concept (C8) and *schedule* it: a
cron job at 03:00 that checks `pipeline.log` for today's 02:00
success line, exits 66 with an ERROR log line if absent, 0 with an
INFO line if present. Prove both paths: one night with the 02:00
job killed (absence fires), one normal. You've built cron watching
cron — the health kit's core loop.

## C6 — The timer with teeth

Extend Lab 1's timer pair with production directives: `TimeoutStartSec=300`,
`MemoryMax=200M` (M20/M24's caps), `RandomizedDelaySec=10m` — then
prove each: a deliberately hung script (`sleep 600`) gets killed at
300s (journal shows the timeout), and a memory-hog gets killed by
MemoryMax. Restore the real script afterward. The deliverable: the
journal lines showing systemd *enforcing* the contract.

## C7 — The multi-job dependency chain

Schedule three jobs that must run in order (fetch → process →
report) using two approaches: (a) cron with staggered times
(02:00/02:10/02:20) — plus the *assumption risk* written out; (b)
one wrapper script (the M11 `runall.sh` pattern) with sequential
stages, scheduled once — with the *chaining benefit* written out.
Prove both with logs; one paragraph on which you'd ship.

## C8 — The @reboot session starter

Use `@reboot` (crontab) or a user timer with `OnBootSec` to start
a personal watcher at boot: a small script that appends a
timestamped "boot detected, watcher alive" line to a log, plus
(optional, M22-honoring) an autossh-style tunnel check. Prove by
rebooting the VM. One sentence on why `@reboot` jobs must also be
idempotent (hint: reboot cycles in clouds).

## Stretch — C9, the scheduling runbook

One page for the capstone's pipeline: every scheduled job (name,
schedule, script, log path, expected success line, absence alarm,
lock), the cron-vs-timer decision per job with the table row that
decided it, and the quarterly review date. You've written the
document that makes an automation farm auditable — Mini-Project D
taught the runbook form; this is its scheduling chapter.
