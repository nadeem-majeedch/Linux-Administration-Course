# Lesson 2 — The cron Environment and Logging Scheduled Jobs

> Module 19 · Unit 5 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 2 — cron debugging](../labs/lab-02-cron-debugging.md)
> Up next: [Lesson 3 — systemd timers & the production pattern](03-systemd-timers-production.md)

---

## 1. The most common cron bug in existence

> *"It works in my terminal but fails in cron."*

This is the single most frequent scheduling complaint in Linux —
and it's not a cron bug at all. Your interactive shell and cron run
commands in **wildly different environments**, and the script that
depended on your environment was fragile in a way only cron
reveals. This lesson names every difference, then builds the
logging pattern that turns "fails silently at 2 AM" into "fails
loudly, with a log."

## 2. The environment differences, inventoried

| Variable/condition | Interactive shell | cron |
|---|---|---|
| `PATH` | your full `~/.local/bin`, conda, nvm... | **`/usr/bin:/bin`** (that's all) |
| `HOME` | yours | yours (this one matches) |
| Working directory | wherever you are | **`$HOME`** |
| Shell | your login shell, rc files sourced | `/bin/sh -c`, **no rc files** |
| Environment variables | everything you export, conda activations, `SSH_AUTH_SOCK` | **only a handful** (`SHELL`, `LOGNAME`, `HOME`, `PATH`) |
| TTY | yes | **none** |
| $DISPLAY | set on desktop | unset |

Each row is a classic failure:

- **PATH** — `python3` resolves to your conda's Python interactively;
  in cron it's `/usr/bin/python3` (the M16-era system one, missing
  your packages) — or `pip` isn't found at all. *The* canonical
  cron failure.
- **cwd** — the script that reads `data/input.csv` (relative) breaks
  when cron runs it from `$HOME`.
- **tty** — anything interactive (`read -p`, a confirmation prompt)
  hangs forever: M10's "script that prompts and hangs the pipeline",
  now on a timer.
- **rc files** — aliases, `rbenv init`, conda hooks: all absent. The
  script can't *assume* any of them.
- **agent** — `SSH_AUTH_SOCK` unset: your key is in the agent, but
  cron can't reach it (rsync-over-ssh jobs fail auth). Fix:
  `IdentityFile` in ssh config (M22) — the config file *is* the
  agent-independent path.

## 3. The cron-proof script — five rules

A script is cron-ready when it *doesn't care* where it's run from:

1. **Absolute paths everywhere** — `/home/ds/lab19/dq.sh`, not
   `./dq.sh`; better: derive from the script itself:
   `readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"`.
2. **Full paths for critical binaries**, or set PATH *at the top*:
   `PATH=/usr/local/bin:/usr/bin:/bin` — explicit beats inherited.
3. **No interactivity, ever** — arguments/flags (M10's rule), never
   prompts; a scheduled script must succeed unattended or fail
   loudly, never wait.
4. **`cd` to a known directory** — or make every path absolute;
   relative paths are terminal-luxury.
5. **Strict mode + idempotency** — `set -euo pipefail`, safe to
   re-run (M11): cron retries happen; overlapping runs happen
   (locks, Lesson 3).

The test that proves cron-readiness *without* waiting for cron:

```console
$ env -i /bin/sh -c '/home/ds/lab19/dq.sh sales.csv'
```

`env -i` empties the environment — a one-command simulation of
cron's poverty. If the script survives `env -i`, it survives cron.

## 4. Logging — the record that replaces hope

[Lesson 1](01-cron-fundamentals.md) §6 left output in the mail
spool; the professional pattern takes ownership of it. Two layers:

**Layer 1 — redirect at the crontab line** (quick, per-job):

```text
0 2 * * * /home/ds/lab19/dq.sh /home/ds/lab19/sales.csv >> /home/ds/lab19/logs/dq.log 2>&1
```

`>> file 2>&1` — append stdout *and* stderr (the order matters:
`2>&1` after the redirect means "stderr to the same place").
Timetamped lines inside the script (M10's `log()` with
`date -Iseconds`) make the file greppable — M24's contract,
fulfilled by every scheduled job.

**Layer 2 — the script logs itself** (better, survives being run
from anywhere): the `log()`/`fail()` pair from M10 writing to a
fixed path (`$SCRIPT_DIR/logs/`). Then the crontab line stays
clean, and the script is honest when run by hand too.

**Quiet when successful** — the course's log etiquette: a healthy
run appends one timestamped INFO line; failures append ERROR lines
*and* exit non-zero. A log that grows a line an hour forever is
noise; a log that's silent all day then screams at 02:00 is
signal. (The `>/dev/null 2>&1` *discard* is the anti-pattern —
unless you're certain the script logs internally; silent
success + silent failure = an outage nobody noticed.)

## 5. Fail-loudly — the exit code and the notification

The [M11](../../../M11-advanced-shell-automation/content/README.md)
exit-code contract now has teeth: cron *records* the exit status,
and a non-zero status means the failure is discoverable:

- **mail spool** — failed jobs land there with their output (§2).
- **the absence alarm** — the strongest pattern: a *second* cron job
  that greps for today's expected success line and complains if
  absent ([M24 C8](../../../M24-logs-journald-monitoring/content/README.md)):
  `"no dq OK line by 03:00"` is an observable event — silence made
  monitorable.
- **systemd timers** (next lesson) — `journalctl -u` and
  `systemctl list-timers` give the same answers *without* you
  building the mail/log plumbing.

The design rule: every scheduled job ends one of two ways — a
success line in the log, or a non-zero exit with an ERROR line.
Anything else is unfalsifiable.

## 6. Diagnosing "works for me, fails in cron" — the procedure

The evidence procedure [Lab 2](../labs/lab-02-cron-debugging.md)
drills:

1. **Read the record** — your log (Layer 1/2), then the mail spool
   (`tail /var/mail/$USER`). The error is usually verbatim there.
2. **Reproduce the poverty** — `env -i /bin/sh -c '...'` (§3): if it
   fails here too, it's an environment bug, not a cron mystery.
3. **Compare environments** — `env | sort > /tmp/mine` from your
   shell; a `* * * * * env | sort >> /tmp/crons` job for one
   minute; `diff` them. The missing variable names itself.
4. **Fix at the script** — PATH at the top, absolute paths (§3's
   five rules). Fixing it in the *crontab* (sourcing files there)
   works but hides the dependence — scripts should carry their own
   environment.

## 7. Try it now (15 minutes)

1. PATH witness: schedule `* * * * * echo $PATH >> ~/lab19/env.log`
   for one minute; compare to `echo $PATH` in your terminal. The
   two lines *are* the lesson.
2. The env-i rehearsal: run your M11-hardened `dq.sh` under
   `env -i` — does it survive? If not, apply §3's five rules and
   re-test. (This is Lab 2's setup, done gently.)
3. Logging upgrade: add `>> logs 2>&1` to the heartbeat from
   Lesson 1, watch the log format, then replace raw `date` output
   with a proper ISO+level line from a tiny script.
4. Mail archaeology: `tail -30 /var/mail/$USER 2>/dev/null` — any
   past unlogged jobs confessing their output?

## 8. Common mistakes

- Assuming cron sources `.bashrc` — it doesn't (and `/bin/sh` isn't
  bash; bashisms break too).
- `2>&1 > file` instead of `>> file 2>&1` — order matters; the
  former sends stderr to the *terminal* (cron: nowhere) and stdout
  to the file.
- Relative paths that worked "because I always run it from ~/lab19"
  — cron runs from `$HOME`, and so will every other scheduler you
  ever use.
- Discarding output (`>/dev/null 2>&1`) on a script that doesn't
  log internally — a scheduled silent failure is the worst artifact
  this module can produce.
- Debugging by adding `echo` debug lines *to the crontab* instead
  of the script — fix the script; the crontab is a schedule, not a
  program.

> **Up next:** [Lesson 3 — systemd timers & the production
> pattern](03-systemd-timers-production.md): the modern scheduler,
> `Persistent=true` (catching up after downtime), and the
> lock-verified pipeline.
