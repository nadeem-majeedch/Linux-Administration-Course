# Module 19 Quiz — Scheduling

> 20 questions. Answer first, then check [quiz-answers.md](quiz-answers.md).
> Scope: lessons 1–3.

## Section A — crontab (Q1–6)

**Q1.** Name the five cron time fields in order, with their ranges.

**Q2.** Write the cron line: every weekday at 07:15.

**Q3.** What does `0 0 13 * FRI` actually schedule — and why is it
not "Friday the 13th"?

**Q4.** What do `@daily` and `@reboot` expand to/do? When is
`@daily`'s exact meaning a problem in practice?

**Q5.** Why is `crontab -r` treated as dangerous, and what is the
course's mandatory habit around it?

**Q6.** `crontab -e` vs editing `/var/spool/cron/crontabs/ds`
directly — why does the course forbid the second?

## Section B — the cron environment (Q7–12)

**Q7.** What is cron's default `PATH`, and what's the canonical
failure it causes for DS scripts?

**Q8.** List four environment differences between your interactive
shell and a cron job (beyond PATH).

**Q9.** What does `env -i /bin/sh -c 'script'` do, and why is it
the cron-readiness test?

**Q10.** In `>> log 2>&1`, why does the *order* matter? What does
`2>&1 > log` do instead?

**Q11.** Where does a cron job's output go if you don't redirect
it — and how do you read it on a minimal Ubuntu VM?

**Q12.** A script uses `./data/input.csv` and "always worked".
State the cron cwd, and the two-layer fix (script and habit).

## Section C — timers & production (Q13–20)

**Q13.** Name three advantages systemd timers have over cron, and
two reasons cron remains the right choice sometimes.

**Q14.** What does `Persistent=true` do — precisely, including
what happens after three missed slots?

**Q15.** Write the two unit files' *key* lines for a nightly 02:00
user timer running `/home/ds/lab19/dq.sh` (service: type, exec;
timer: schedule, persistence).

**Q16.** Why `systemctl --user enable --now dq.timer` and not
`... dq.service`? What does the wrong command do?

**Q17.** What does `systemd-analyze calendar "*-*-01 04:00:00"`
print, and why is it the module's validator of choice?

**Q18.** The mkdir-lock overlap guard: why `mkdir` (atomic) instead
of `touch`/file-existence checks? What releases the lock?

**Q19.** "Verify-it-ran": name the four evidence sources this
module taught, and the one class of failure only the *absence
alarm* catches.

**Q20.** The production script shape has five properties (env,
paths, logging, lock, idempotency). State each in one line as you'd
put it in a team wiki.

## Bonus (Q21) — the 2 AM ticket

A teammate's 02:00 cron job "stopped running" three days ago — no
one changed the crontab. Draft the first four commands you'd run,
in order, and what each would tell you.
