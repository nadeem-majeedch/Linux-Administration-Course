# Lab 1 — Schedule the Pipeline: cron and Timers, Both Proven

> Module 19 · Unit 5 · Difficulty: Advanced
> Time: ~55 min · Environment: your own VM, `~/lab19/`
> Prerequisites: M11's hardened `dq.sh`; [Lessons 1–3](../README.md)
> ⚠️ User crontab + user timer only. Scratch data only. Every
> schedule verified by the two-minute rule or a forced run.

One job, three schedules. You'll wire M11's hardened `dq.sh` into
cron, then into a systemd timer, then let the timer fire naturally —
and the deliverable for each is *evidence it ran*, not the wiring.

## Setup — make the job cron-proof first (10 min)

Copy your hardened `dq.sh` into `~/lab19/` and apply Lesson 2's
five rules: absolute `PATH` line, `SCRIPT_DIR` derivation, no
prompts, log via the `log()` pair to `~/lab19/logs/pipeline.log`.
Then the gate test:

```console
$ env -i /bin/sh -c '/home/ds/lab19/dq.sh /home/ds/lab19/sales.csv' && echo CRON-PROOF
```

Fix until `CRON-PROOF` prints. (If it already passes: excellent —
M11 paid off. Record the pass.)

## Part A — the cron schedule (15 min)

```console
$ crontab -l > ~/lab19/crontab.backup         # the backup-first rule, always
$ crontab -e
# add — with redirect, per Lesson 2 Layer 1:
# */2 * * * * /home/ds/lab19/dq.sh /home/ds/lab19/sales.csv >> /home/ds/lab19/logs/cron.log 2>&1
```

The **two-minute rule**: wait for two firings (the log gets two
entries), and verify *both* records — `cron.log` (your redirect)
*and* the mail spool if anything went wrong. Then re-schedule to
the realistic form (`0 2 * * *`) and remove the test line. The
two-minute loop is the whole craft: fail fast, learn fast, then
commit to the real schedule.

## Part B — the systemd timer (15 min)

Build the pair from Lesson 3 §2 (`dq.service` + `dq.timer`,
`OnCalendar` at a **testable** time — or `OnCalendar=*-*-* *:00/15:00`
for the first proof), then:

```console
$ systemctl --user daemon-reload
$ systemctl --user enable --now dq.timer
$ systemctl list-timers --user | grep dq           # NEXT / LAST visible
$ systemctl --user start dq.service                # force one run NOW — no waiting
$ journalctl --user -u dq.service --no-pager | tail -8
```

The forced run is the timer's version of the two-minute rule. Then
wait for (or simulate) one *scheduled* firing and capture the
journal delta — scheduled-run evidence, not just forced-run.

## Part C — the proof sheet (10 min)

`~/lab19/lab-log.md` closes with the verification matrix:

| Schedule | Proof of run | Timestamp | Exit status |
|---|---|---|---|
| cron `*/2` (test) | cron.log line | … | 0 |
| cron `0 2` (real) | crontab -l line + (next morning) | … | — |
| timer, forced | journal line | … | 0 |
| timer, scheduled | journal line | … | 0 |

Three of four cells filled today; the fourth is tomorrow's
homework, checked by the absence-alarm pattern if you add it
(M24 C8, scheduled *by* cron — cron watching cron).

## Part D — disable what you don't keep (5 min)

Course hygiene: schedules you stop trusting are *removed*, not
left running silently.

```console
$ systemctl --user disable --now dq.timer        # decide: keep or stop
$ crontab -e                                      # keep only the real 02:00 line, or none
$ crontab -l                                      # final state, transcribed
```

If you keep one schedule (recommended: the timer), say in one line
which and why — the cron-vs-timer decision table applied to your
own case.

## Done when

- [ ] `CRON-PROOF` gate passed (or the fixes that got there logged)
- [ ] crontab backup file exists and predates every crontab change
- [ ] Verification matrix ≥ 3 rows with real timestamps
- [ ] Final schedule state transcribed (crontab -l + list-timers)
- [ ] One-paragraph decision note: cron or timer for this job, and
      which table row decided it
