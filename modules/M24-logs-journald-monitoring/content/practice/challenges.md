# Module 24 Challenges — Logs & Monitoring

> Eight challenges, all on your own VM, all evidence-first: every
> answer ships with the command that proved it, recorded in
> `lab-log.md`. C5–C8 lean on the labs' lab24 units and data — set up
> [Lab 1](../labs/lab-01-log-forensics.md) first if you haven't.

## C1 — The boot biography

Using only `journalctl`: produce a 10-line summary of your VM's most
recent boot — first message timestamp, time to `Reached target
Multi-User System` (hint: `journalctl -b | grep "Reached target"`),
any err+ entries, and the last message before this moment. No system
changes; pure archaeology.

## C2 — The two-minute disk detective

Create a hidden space hog in your home dir (`dd if=/dev/zero
of=~/lab24/hog bs=1M count=300`), then — using only df/du/sort/head —
*find* it as if someone else had made it. Present the exact command
sequence and the one-line rule you'd put in a team wiki for "disk
full on a shared server, first three moves".

## C3 — Priority triage

One command that answers: "which units produced error-severity (or
worse) messages this boot, ranked by count?" (You'll need `journalctl
-b -p err..` + M08 pipelines — short-pretty output's unit column is
extractable; `awk` earns its keep.) Then the same for your *user*
journal. Note in one sentence where your own services rank against
system noise.

## C4 — The rotation inspector

Explain, with evidence, exactly how `/var/log/syslog` rotates on your
machine: read `/etc/logrotate.d/rsyslog` and report schedule, keep
count, compression; then `ls -la /var/log/syslog*` to show the actual
resulting generations. Finally, `zgrep -h "session opened"
/var/log/syslog*.gz | wc -l` — proving compressed history is still
queryable. (Counts may be small/zero on a young system; the *method*
is the answer.)

## C5 — The leak forensics

Re-run [Lab 1's](../labs/lab-01-log-forensics.md) `train.service`
incident, but this time *before* it dies, capture the growth curve:
`journalctl --user -u train.service -f -o short-precise | grep
rss_mb` into a file while it runs. Then, with M08 tools, produce the
growth table (epoch → rss_mb) and compute the MB/epoch slope. One
sentence: at what epoch would an *alarm* have fired if the budget
were 250 MB — i.e., when should monitoring have paged you, given
death comes at 300 MB?

## C6 — The latency story

Run [Lab 3's](../labs/lab-03-monitoring-under-load.md) `churn.sh` in
one terminal and, in another, time a trivial read of a 200 MB file
(`time cat churnfile > /dev/null`) *during* the churn vs after it.
Correlate: quote the `iostat -x` `await`/`%util` during your timed
run. Deliverable: three sentences — measured slowdown, device
evidence, and what this predicts for "my data load is slow" tickets
on shared servers.

## C7 — Design the retention policy

A fictional service writes 40 MB/day of INFO logs; compliance needs
90 days of ERROR+; the disk partition for logs is 2 GB, shared with
nothing. Write the policy as a 10-line logrotate-style config sketch
(two stanzas: full logs, errors-only extract) plus a `journalctl
--vacuum-*` equivalent for the service's journald stream. Then the
honesty line: how would you *verify* the policy works before the day
it matters?

## C8 — The absence alarm

The scariest failures are silent: the 3 AM job that *never ran*.
Write a 12-line bash check, `expected-runner.sh`: given a tag (e.g.
`-t demo` from Lab 2) and a max-age, it exits 0 if
`journalctl -t "$TAG" --since "@$(( $(date +%s) - MAXAGE ))"` found a
line and 1 with a clear message if not. Demonstrate both exits
against Lab 2's demo logger. One sentence on where you'd schedule it
(cron? timer? — and which module's tools run it).

## Stretch — C9, the observability one-pager

Condense the module into a single reference page: the six-rung
monitoring ladder (uptime→free→df→vmstat→journal→postmortem) with one
command + one "healthy looks like" fragment per rung, and the five
incidents from Lesson 4 as a symptom→first-command table. Compare
against [resources/cheatsheets/](../../../../resources/cheatsheets/)
and reconcile differences — disagreements between your summary and
the cheatsheet are *discussion topics*, not errors.
