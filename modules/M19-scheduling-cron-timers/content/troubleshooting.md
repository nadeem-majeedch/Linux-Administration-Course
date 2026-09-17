# Module 19 Troubleshooting — Scheduling Symptoms → Fixes

> Ten patterns, ordered by field frequency. Each: **symptom →
> cause → diagnosis → fix → prevention**. The ladder from
> [Lab 2](labs/lab-02-cron-debugging.md) opens every case: job log →
> mail spool → `env -i` → env diff → fix at the script.

## 1. "Works in my terminal, fails in cron"

**Cause:** the environment chasm — PATH, cwd, rc files, tty
(Lesson 2's inventory).
**Diagnosis:** the ladder; usually the mail spool names it
verbatim.
**Fix:** explicit PATH, absolute paths, no prompts — at the script.
**Prevention:** the `env -i` gate before anything is scheduled.

## 2. "The job never runs at all" (no error anywhere)

**Cause hierarchy:** crontab line typo'd into commentary; the
schedule field never matches (`0 0 13 * FRI`'s OR trap); cron
daemon not running; wrong user's crontab; the job *is* running —
but dying before its first log line.
**Diagnosis:** `crontab -l` (is the line live?); `systemd-analyze
calendar` (does the field match when you think?); `systemctl
status cron`; `grep cron /var/log/syslog | tail` (cron logs every
firing attempt — ` syslog` is the meta-log).
**Fix:** field correction / daemon start / log-before-work in the
script.
**Prevention:** the two-minute rule — every schedule proven before
its real slot.

## 3. "The job runs twice" (or "runs while the last one's still going")

**Cause:** schedule faster than runtime; or `@reboot` + scheduled
double-fire; or a timer and a cron line for the same job (both
armed during migration).
**Diagnosis:** overlapping timestamps in the log; `ps -ef | grep
<script>` during the window; `crontab -l` *and* `systemctl
list-timers --user` checked together.
**Fix:** the mkdir-lock (Lesson 3 §3) — refuse overlaps; remove
the duplicate schedule.
**Prevention:** one scheduler of record per job; locks on
everything longer than its interval.

## 4. "Output vanishes / job hangs forever"

**Cause:** no redirect (output → mail spool you didn't check) and/
or an interactive prompt with no tty.
**Diagnosis:** `/var/mail/$USER`; `ps` shows the job alive with a
`read`/`sudo` wchan (M18's wchan).
**Fix:** redirect `>> log 2>&1`; de-prompt the script
(arguments/flags, `read -t` at worst); `sudo -n` for non-interactive
sudo.
**Prevention:** "a scheduled job never asks" — the M10 rule with
its enforcement here.

## 5. "It ran yesterday but not today" (nothing changed!)

**Cause:** something *did* change — data moved, a disk filled
(the job's write failed), a dependency updated (M16), daylight
shift for `TZ`-sensitive schedules, or the *machine* was off at
fire time (cron skips silently).
**Diagnosis:** M24's method: the job's log's last good line →
`diff` the environment → `df -h` (disk-full kills logging too) →
`uptime` vs the missed timestamps.
**Fix:** whichever the evidence names; consider `Persistent=true`
if off-at-fire-time is the story.
**Prevention:** the absence alarm (C5) — "nothing changed" claims
get audited by cron itself.

## 6. "Timer never fires" (systemd side)

**Cause:** unit edited without `daemon-reload`; `OnCalendar`
typo (accepted at load, never matches); timer `enabled` but the
service `Type=oneshot` marked failed from an earlier crash —
failed units don't re-trigger until reset; you enabled the
*service*, not the timer.
**Diagnosis:** `systemctl --user status dq.timer dq.service`;
`systemd-analyze calendar "<expr>"`; `systemctl list-timers --user`
(Next column: is it sane?); `journalctl --user -u dq.service`.
**Fix:** daemon-reload; fix the expression; `systemctl --user
reset-failed dq.service`; enable the timer.
**Prevention:** `systemd-analyze calendar` before every
daemon-reload; list-timers as the post-change glance.

## 7. "Timer fired but the service didn't do the work"

**Cause:** `ExecStart` path wrong *after a move* (unit files hold
absolutes that rot); `Type=oneshot` service left in failed state
from a previous run; `RemainAfterExit` confusion.
**Diagnosis:** `journalctl --user -u <svc> -b --no-pager` — systemd
quotes its exact complaint (command not found / exit code);
`systemd-analyze verify <unit>` for offline checking.
**Fix:** correct/derive paths; `reset-failed`; re-run.
**Prevention:** `systemd-analyze verify` in the edit loop (M20's
habit, M19's beneficiary).

## 8. "Timezone surprises — it ran at the wrong hour"

**Cause:** cron runs in the *system* timezone; servers are UTC,
laptops aren't; `TZ=` lines in crontabs are per-job overrides
people forget they set.
**Diagnosis:** `timedatectl` (system zone); `grep TZ /etc/crontab
/var/spool/cron/crontabs/$USER`; compare a firing's log timestamp
to intent.
**Fix:** schedule in the system zone, or make the intent explicit
(`CRON_TZ=Europe/Berlin` at the crontab top, documented); prefer
UTC on servers with converted expectations.
**Prevention:** log lines carry ISO-8601 *with offset*
(`date -Iseconds`) — ambiguous times announce themselves.

## 9. "The lock file is stuck — every run refuses"

**Cause:** a crashed run left the lock (the EXIT trap didn't fire —
`kill -9`, machine power-loss), and the guard now self-denies.
**Diagnosis:** the fail-fast line ("previous run still active");
`ls -ld` the lock (age vs schedule); no matching process (`pgrep
-af`).
**Fix:** verify no real run (pgrep), remove the lock, let the next
run proceed; consider a lock-age override (`[ lock newer than 24h
] || rm` with a warning line).
**Prevention:** the trap on every exit path (including `SIGKILL`
caveats — documented in the runbook); stale-lock policy written
down, not improvised.

## 10. "Cron spams me / my mail spool is enormous"

**Cause:** unredirected verbose jobs — every run mails its whole
output (the anti-pattern of Lesson 2 §4).
**Diagnosis:** `ls -lh /var/mail/$USER; grep -c Subject
/var/mail/$USER` — and the worst offenders' names are in the
headers.
**Fix:** add `>> log 2>&1` per job (keep failures loud by logging
inside the script); or `MAILTO=""` at the crontab top *only* for
jobs that verifiably self-log.
**Prevention:** quiet-when-successful scripts + redirected lines —
the mail spool should be an *emergency* record, not the archive.

## When to escalate

| Evidence | Escalate to |
|---|---|
| Cron daemon itself failing (`systemctl status cron` red) | Admin — system-level scheduler |
| System crontab (`/etc/cron.d/`) conflicts with yours | Admin — shared-machine scheduling policy |
| Scheduled jobs consuming shared resources unreasonably | Co-tenants — coordination before `nice`/reschedule (M18) |
| A job whose failure signals data loss | M24's incident method, then the data owner |

> Scheduling failures are *discoverable* failures — the whole
> module's point is that "it ran" is a queryable claim. When
> escalating, bring the ladder's evidence, not the mystery.
