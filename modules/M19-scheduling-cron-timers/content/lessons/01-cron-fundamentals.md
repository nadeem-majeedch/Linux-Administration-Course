# Lesson 1 — cron Fundamentals and crontab Fluency

> Module 19 · Unit 5 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Lab 1 — schedule the pipeline](../labs/lab-01-schedule-the-pipeline.md)
> Up next: [Lesson 2 — the cron environment & logging](02-cron-environment-logging.md)

---

## 1. Why scheduling is the payoff of everything before it

Every script you've hardened — strict mode, logging, idempotency,
dry-runs — has waited for this module. **Scheduling** is what turns
"a script I run" into "a pipeline that runs itself": the nightly
dataset refresh, the weekly report, the hourly cleanup. The course
order is deliberate: [M11](../../../M11-advanced-shell-automation/content/README.md)
made scripts *safe to automate*; this module automates them. A
fragile script on a schedule is just a recurring failure.

## 2. cron — the daemon and the two crontabs

**cron** is a background daemon ([M20](../../../M20-systemd-services/content/README.md)
vocabulary: a service) that wakes every minute, checks every
registered schedule, and runs what's due. Schedules live in
**crontabs** (cron tables), of which there are two kinds:

| Kind | Location | Managed by | Who can edit |
|---|---|---|---|
| **User crontab** | `/var/spool/cron/crontabs/<user>` | the `crontab` command | you, for yours |
| **System crontabs** | `/etc/crontab`, `/etc/cron.d/*` | admin via files | root only |

Course scope: **user crontabs only** — `crontab -e` is your
interface, and it's the only blessed one (see the rule in §4).

## 3. The five fields — reading and writing

Each crontab line: five time fields, then the command:

```text
┌───────── minute        (0–59)
│ ┌─────── hour          (0–23)
│ │ ┌───── day of month  (1–31)
│ │ │ ┌─── month         (1–12, or JAN–DEC)
│ │ │ │ ┌─ day of week   (0–7, 0 and 7 = Sunday, or SUN–SAT)
│ │ │ │ │
* * * * *  command to execute
```

Grammar per field — numbers, lists, ranges, steps, wildcards:

| Expression | Meaning |
|---|---|
| `30 2 * * *` | 02:30 every day |
| `0 9 * * 1-5` | 09:00 on weekdays |
| `*/15 * * * *` | every 15 minutes |
| `0 4 1 * *` | 04:00 on the 1st of each month |
| `0 0 1 1 *` | midnight, January 1st (yearly) |
| `0 */6 * * *` | every 6 hours (00:00, 06:00, 12:00, 18:00) |

The pitfall that owns its own name: **day-of-month + day-of-week
are OR'd** when both are restricted. `0 0 13 * FRI` runs on the
13th *and* every Friday — not "Friday the 13th" (that classic
requires one restricted field + a test in the command). When in
doubt: restrict one field, verify with the validator below.

**The @shortcuts** — the common schedules, pre-written:

```text
@hourly     = 0 * * * *
@daily      = 0 0 * * *     (also @midnight)
@weekly     = 0 0 * * 0
@monthly    = 0 0 1 * *
@yearly     = 0 0 1 1 *
@reboot     = once, at startup   (great for "start my session watcher")
```

## 4. Managing your crontab — the three verbs and one ban

```console
$ crontab -l               # list — always the first command
$ crontab -e               # edit in $EDITOR; syntax-checked-ish on save
$ crontab -r               # REMOVE YOUR ENTIRE CRONTAB — no prompt, no undo
```

**Course rule: `crontab -r` is banned without a preceding `crontab
-l > ~/crontab-backup.txt` in the same session.** `-r` destroys all
scheduled jobs instantly and silently — the one command in this
module that can ruin your week by itself. (`crontab -ir` prompts
first on modern systems, but the backup habit is the real
protection.)

The editing loop that builds fluency:

```console
$ crontab -l | head -5              # what's scheduled now?
$ crontab -e                        # add: */2 * * * * date >> ~/lab19/heartbeat.log
$ crontab -l                        # verify it took
$ sleep 130 && cat ~/lab19/heartbeat.log    # wait two minutes; prove it ran
$ crontab -e                        # remove the test line
```

That last `cat` — *proving the job ran* — is the module's core
discipline. A schedule you haven't watched fire is a hypothesis;
[Lab 1](../labs/lab-01-schedule-the-pipeline.md) makes "it ran,
here's the log" the deliverable.

## 5. Validating schedules — before cron judges you

Two validators, one human one mechanical:

- **`systemd-analyze calendar "Fri *-*-13"`** — Ubuntu's schedule
  expression parser prints exactly when the expression will next
  fire, several iterations deep. It understands cron fields and
  systemd's richer syntax — invaluable for the OR'd-fields trap:

  ```console
  $ systemd-analyze calendar "0 0 13 * FRI" 2>/dev/null | head -5
  # → shows the 13th of each month AND each Friday — the trap, made visible
  ```

- **The two-minute rule** — while learning, schedule new jobs
  `*/2 * * * *`, watch one run, then re-schedule properly. Cheap
  feedback beats 2 AM discovery.

## 6. Where job output goes — the mail spool preview

A cron job's stdout/stderr doesn't vanish — cron tries to **mail it
to the local user**. On a minimal Ubuntu VM there's no local mail
reader, so output silently accumulates in the spool:

```console
$ ls /var/mail/$USER 2>/dev/null      # exists? your jobs have been talking
$ cat /var/mail/$USER | tail -20      # cron's actual output, buffered
```

Reading your mail spool after a few scheduled runs is the honest
diagnostic for "did it work" — before [Lesson 2](02-cron-environment-logging.md)
teaches the professional pattern: *redirect everything yourself*
and let logging, not mail, be the record.

## 7. The mental model — cron as the DS pipeline engine

The DS scenarios this module enables, in the vocabulary of fields:

- **Nightly dataset refresh** — `0 2 * * *` → the [M22](../../../M22-ssh-remote-admin/content/README.md)
  rsync push, scheduled.
- **Weekly report** — `0 7 * * 1` → summary.sh generates Monday's
  PDF before the team stands-up.
- **Hourly cleanup** — `@hourly` → the M11 scratch cleaner.
- **The health kit's absence alarm** —
  [M24 C8's](../../../M24-logs-journald-monitoring/content/README.md)
  expected-runner script, itself cron-scheduled — cron watching
  cron, honestly.

Every one is the same act: a hardened script + five fields + a log
file.

## 8. Try it now (15 minutes)

1. Heartbeat: schedule `*/2 * * * * date >> ~/lab19/heartbeat.log`,
   verify with the two-minute rule, then remove it — full cycle,
   transcript recorded.
2. `crontab -l` on your machine — what already runs? (Ubuntu
   desktops: usually nothing at user level. Servers: much more.)
3. Validator drills: predict, then `systemd-analyze calendar` —
   `0 4 * * 1-5`, `*/10 9-17 * * *`, `0 0 13 * FRI` (the trap).
4. `ls /var/mail/$USER` — has any job mailed you? (If the M24
   heartbeat from a previous module ran unlogged, its output is
   sitting there — the mail spool caught what logging missed.)

## 9. Common mistakes

- Editing `/var/spool/cron/...` files directly — use `crontab -e`;
  direct edits can be silently ignored (spool perms) and skip
  cron's re-read signal.
- `crontab -r` reflexes — one keystroke from destroying every
  schedule you own.
- The 13th/Friday OR trap.
- Assuming `@daily` means "sometime reasonable" — it means exactly
  00:00, when every other `@daily` job on every server also fires.
  Stagger deliberately (`0 2 * * *` for yours).
- Waiting a day to learn a job never ran — the two-minute rule
  exists so you never do.

> **Up next:** [Lesson 2 — the cron environment &
> logging](02-cron-environment-logging.md): why jobs work in your
> terminal and fail in cron — PATH, HOME, cwd, tty — and the
> logging pattern that makes every run auditable.
