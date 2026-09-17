# Lesson 3 — systemd Timers and the Production Schedule Pattern

> Module 19 · Unit 5 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1](../labs/lab-01-schedule-the-pipeline.md)
> Up next: [Unit 6 — Services, Networking & Security](../../../M20-systemd-services/README.md)

---

## 1. The second scheduler — and when it wins

cron is universal and simple; **systemd timers** are Ubuntu's modern
native scheduler — the same unit machinery as
[M20's](../../../M20-systemd-services/content/README.md) services, plus
time. Timers win on four grounds that matter in production:

1. **`Persistent=true`** — if the machine was *off* at the scheduled
   time (laptop asleep, VM suspended), the job fires at next boot.
   cron simply skips missed runs. For "the nightly backup must
   happen", persistence is the difference.
2. **Journal integration** — every run's output lands in
   `journalctl -u <service>`, timestamped, filterable — no log
   plumbing (Lesson 2's Layer 1 becomes optional).
3. **Dependencies and limits** — `Requires=`, `After=`, `TimeoutStartSec=`,
   `MemoryMax=` ([M20](../../../M20-systemd-services/content/README.md)'s
   directives): the job can be ordered *after* the network, capped
   in memory, auto-killed on hang.
4. **Introspection** — `systemctl list-timers` shows every timer's
   next/last run: the schedule dashboard cron never had.

cron keeps wins too: simpler one-liners, universal (containers,
macOS, BSD), no unit files for trivial jobs. The course rule of
thumb: **cron for one-line jobs; timers for anything with state,
dependencies, or persistence requirements.**

## 2. The timer + service pair

A timer *triggers* a service; the service holds the work. Two files,
user-level (`~/.config/systemd/user/` — M20's territory):

**`~/.config/systemd/user/dq.service`** — the work:

```ini
[Unit]
Description=Dataset quality check

[Service]
Type=oneshot
ExecStart=/home/ds/lab19/dq.sh /home/ds/lab19/sales.csv
# oneshot: a job that runs and exits (not a daemon)
```

**`~/.config/systemd/user/dq.timer`** — the schedule:

```ini
[Unit]
Description=Run dataset quality check nightly

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true
RandomizedDelaySec=10m

[Install]
WantedBy=timers.target
```

Activation (the M20 sequence, user-scoped):

```console
$ systemctl --user daemon-reload
$ systemctl --user enable --now dq.timer      # --now: armed immediately
$ systemctl list-timers --user | grep dq       # NEXT and LAST, visible
$ journalctl --user -u dq.service --no-pager | tail   # the run's output
```

**`OnCalendar` syntax** — richer than cron's five fields, validated
by the same tool from Lesson 1:

```text
*-*-* 02:00:00          daily 02:00           (same as cron's 0 2 * * *)
Mon *-*-* 07:00:00      Mondays 07:00
*-*-01 04:00:00         monthly, the 1st, 04:00
*-*-* *:00/15:00        every 15 minutes
```

`systemd-analyze calendar "Mon *-*-* 07:00:00"` — predict, verify,
schedule (the Lesson 1 validator, now the native dialect).

**`Persistent=true`'s fine print:** it records the last trigger in a
timestamp file; a missed run fires at next boot *once* — not once
per missed slot. A laptop asleep all weekend runs the missed nightly
job Monday morning, not four times.

## 3. The production pattern — every scheduled job, one shape

Assembling the whole course: the script that *deserves* scheduling
carries every property below ([M11's](../../../M11-advanced-shell-automation/content/README.md)
checklist plus this module):

```bash
#!/usr/bin/env bash
# nightly_pipeline.sh — cron/timer-proof by construction
set -euo pipefail

PATH=/usr/local/bin:/usr/bin:/bin            # cron-proof PATH (Lesson 2)
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOCK="$SCRIPT_DIR/.nightly.lock"

log() { printf '%s INFO  %s\n' "$(date -Iseconds)" "$*" >> "$SCRIPT_DIR/logs/pipeline.log"; }
fail() { printf '%s ERROR %s\n' "$(date -Iseconds)" "$*" >> "$SCRIPT_DIR/logs/pipeline.log"; exit 1; }

# overlap guard: cron at 02:00 + slow run + next 02:00 = two concurrent jobs
if ! mkdir "$LOCK" 2>/dev/null; then
    fail "previous run still active (lock present)"
fi
trap 'rmdir "$LOCK"' EXIT                     # M11: cleanup on every exit path

log "run started"
# ... the actual work — absolute paths, idempotent steps ...
log "run finished OK"
```

Three protections the shape adds:

- **The lock** (`mkdir`-atomic — M11's trick): overlapping runs are
  detected and *refused*, not doubled. The EXIT trap releases it
  even on failure.
- **Logging on every path** — including the fail-fast path.
- **Cron-proof env** — explicit PATH, derived directories (§3 of
  Lesson 2).

Whether triggered by cron or a timer, this script behaves
identically — which is the portability that makes the cron-vs-timer
choice a *scheduling* decision, not a rewrite.

## 4. Verify-it-ran — the discipline that closes the module

The course's repeated thesis, now the final habit: **a schedule is
not evidence**. The verification ladder:

```console
$ systemctl list-timers --user | grep dq      # when did it last run? when next?
$ journalctl --user -u dq.service --since today --no-pager | tail   # the run's story
$ tail -3 ~/lab19/logs/pipeline.log           # the script's own record
$ echo $?                                     # (after a manual run) the exit contract
```

And the cross-check that catches the silent class: the *absence
alarm* — a job scheduled to verify another job's log line exists
([M24 C8](../../../M24-logs-journald-monitoring/content/README.md)).
Cron watching cron; the health kit (M24's Mini-Project E) consumes
the same lines. On real servers, "the pipeline is green" means
"the success lines exist for every scheduled window" — a queryable
claim, not a feeling.

## 5. cron vs timers — the decision table

| Question | cron | systemd timer |
|---|---|---|
| One-line job, no state? | ✅ natural | unit files are ceremony |
| Must run even if the machine was off? | ❌ skips | ✅ `Persistent=true` |
| Needs ordering/caps/timeouts? | ❌ DIY | ✅ unit directives |
| Output handling? | redirect + mail spool | journal, built-in |
| On containers/BSD/macOS? | ✅ universal | ❌ systemd required |
| Introspection ("when did it last run?") | DIY (logs) | `systemctl list-timers` |

Both are legitimate; the *bad* choice is neither — an unlogged
cron job or a timer wrapping an unhardened script. The schedule is
the last mile of the pipeline, not a substitute for the first
mile's discipline.

## 6. Try it now (20 minutes)

1. Build the pair from §2 against your own `dq.sh` (adjust paths);
   `daemon-reload`, enable the timer, then **force one run now**:
   `systemctl --user start dq.service` — journal shows it without
   waiting for 02:00.
2. `systemctl list-timers --user` — find your timer's NEXT and
   LAST columns; that's the introspection cron never gave you.
3. Persist the proof: `sudo systemctl reboot`, log back in,
   `journalctl --user -u dq.service` — the *previous* run's output
   survives reboot (journal persistence — check M20's
   `/var/log/journal` note if it doesn't).
4. The overlap drill: `mkdir` the lock by hand, start the service —
   the fail-fast line fires ("previous run still active"). Remove
   the lock, re-run clean. You've rehearsed the overlap path
   without waiting for a real overlap.

## 7. Common mistakes

- `enable --now` on the **service** instead of the **timer** — the
  job runs once, immediately, and never again; you armed the work,
  not the schedule. (`systemctl --user enable --now dq.timer`.)
- Editing unit files without `daemon-reload` — systemd runs the old
  definition, faithfully and confusingly.
- `OnCalendar` typos — silently accepted at load, firing never.
  `systemd-analyze calendar` before `daemon-reload`, always.
- A timer wrapping a script that prompts — the hang returns
  (Lesson 2 §2), now invisible until `TimeoutStartSec` (which you
  should set) kills it.
- Forgetting that user timers need the user session — lingering
  (M20's `loginctl enable-linger`) is required for jobs that must
  run while you're logged out; note it in the runbook.

> **Next:** [Lab 1](../labs/lab-01-schedule-the-pipeline.md) —
> schedule the pipeline both ways, prove both ran; then
> [Lab 2](../labs/lab-02-cron-debugging.md) breaks the environment
> so you can diagnose it like an operator.
