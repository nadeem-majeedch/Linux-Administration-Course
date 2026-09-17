# Lesson 4 — The Incident Methodology

> Module 24 · Unit 6 · Difficulty: Advanced
> Reading time: ~25 min · Lab: [Labs 1 & 3](../labs/lab-01-log-forensics.md)
> Up next: [Mini-Project E — health & backup kit](../mini-project-health-backup-kit.md)

---

## 1. Why a methodology at all

Under pressure, untrained people do three things: run random commands
("have you tried restarting?"), form theories before facts ("it's
definitely DNS"), and fix symptoms while the cause keeps working
(reboot the server, never learn why it died). This lesson installs the
opposite habit — a fixed order of questions that *produces* evidence
before verdicts. It fuses everything the course has built: M08's
text pipelines, M18's process inspection, M20's service status +
journal, M21's layered ladder, and this module's monitoring toolkit.

## 2. The six steps

**1. Stabilize the scene — before touching anything.**
What changed *recently*? New package (`/var/log/dpkg.log` or apt
history), config edit, new data volume, new cron job? Time-box this:
five minutes of "what changed" beats an hour of "what's broken".

**2. Define the symptom precisely.**
Not "the server is slow" but: *which* command, *since when*,
*compared to what baseline*, error message **verbatim**. A symptom
you can't re-run is a symptom you can't diagnose. If a user reports
it, get the exact command and timestamp.

**3. Gather evidence, broadly then narrowly.**
Start wide (the 60-second health check from Lesson 3 §8), then narrow
along the strongest signal. Logs first if something *said* something;
monitoring first if something *behaves* wrong. Never interpret while
collecting — collect first, then read. The discipline matters because
the first plausible story anchors you; three more minutes of evidence
usually breaks the anchor.

**4. Form ONE hypothesis, and design its killer test.**
The best test is the one that *falsifies* the hypothesis cheaply.
"OOM killed it" → `journalctl -k -g oom -b -1` (ten seconds, binary
answer). "Disk full" → `df -h` (two seconds). If the test passes,
proceed to fix; if not, back to step 3 with the new evidence. One
hypothesis at a time — shotgun theories produce shotgun fixes.

**5. Fix, then VERIFY the fix.**
The smallest reversible change that addresses the *cause* — and then
the step everyone skips: re-run the failing command / re-check the
metric, and *watch it hold* for a sensible interval. A fix without a
verified before/after is a coin toss you'll pay for again.

**6. Write the postmortem — five lines, no heroics.**
Symptom (verbatim) → root cause → the command that revealed it → the
fix → the prevention. This is exactly the report format M14's sudo
incidents and M21's clinic used; here it becomes permanent habit.
The prevention line is where skill compounds: each incident should
delete a whole *class* of future incidents (a check added, a
rotation policy, a health-kit alert).

> The sequence is also the grading rubric for
> [Lab 1](../labs/lab-01-log-forensics.md) and
> [Mini-Project E's](../mini-project-health-backup-kit.md) incident
> report: evidence at every step, verdicts only at step 4, prevention
> always.

## 3. Five incidents you will actually have

Each maps to a lab rehearsal. Read the shape now; the labs make your
hands do it.

### Incident 1 — "The service won't start"

Symptom: `systemctl --user start sync.service` fails, or starts and
dies. Method in action:

```console
$ systemctl --user status sync.service     # → "failed (Result: exit-code)"
$ journalctl --user -u sync.service -b --no-pager | tail -20
Sep 15 21:04:11 ds-lab sync.service[4312]: FileNotFoundError: '/home/ds/cron/sync.py'
```

The journal line *is* the diagnosis: wrong path in `ExecStart=`.
Fix: correct the unit, `systemctl --user daemon-reload`, start,
verify status + one log line. Prevention: `systemd-analyze verify`
before installing units (M20). Rehearsed in
[Lab 1, part A](../labs/lab-01-log-forensics.md).

### Incident 2 — "Training died overnight"

Symptom: SSH in at 08:00; the job that was at epoch 9 is gone; the
terminal says "Killed" — or nothing at all.

```console
$ journalctl -b -1 -k -g oom --no-pager | tail -8   # previous boot's kernel view
$ journalctl --user -u train.service -b -1 --no-pager | tail -15
Sep 15 02:14:09 ds-lab kernel: Out of memory: Killed process 5521 (python3)...
```

`-b -1` (previous boot) is the step people forget — if the machine
*rebooted*, last night's evidence is in the *previous* journal. Root
cause: RSS growth met RAM limit; kernel chose the fattest process.
Fix: cap the job (`ulimit`/batch size/`--memory` limits), schedule
within resources. Prevention: memory-trend the first run (`watch -n30
free -h`) and set a unit memory cap so *your* job dies first, not the
server's other tenants. Rehearsed in
[Lab 1, part B](../labs/lab-01-log-forensics.md).

### Incident 3 — "Disk full"

Symptom: writes fail — checkpoints abort, logs stop, sometimes
services crash in confusing secondary ways (databases refuse writes,
SSH sessions misbehave).

```console
$ df -h /home                     # which filesystem? (i-node check: df -i)
$ du -h --max-depth=1 ~ | sort -rh | head -5
4.1G    ~/data/exports
2.8G    ~/.cache
1.9G    ~/logs
```

Root cause candidates: experiment logs never rotated (Lesson 2 §5),
checkpoint accumulation, dataset duplication. Fix: clean *own* files
(cache first — it's regenerable), add rotation, add a `df` check to
the job. Prevention: the health check's `df -h` line + a rotation
policy. Rehearsed in [Lab 3's](../labs/lab-03-monitoring-under-load.md)
disk segment — safely, on files you create for the purpose.

### Incident 4 — "High CPU — is something wrong?"

Symptom: a teammate says "the server is hot"; `top` shows python3 at
700% (8 cores). Method's discipline: high utilization is *not yet* a
problem — check saturation and identity:

```console
$ uptime                          # load vs nproc: saturated or just busy?
$ ps -eo pid,ppid,user,%cpu,%mem,etime,cmd --sort=-%cpu | head -6
 5521  4310 ds    690 12.3 03:12 python3 train.py --epochs 50
```

Root cause: *someone's legitimate job*. The admin question is
coordination (nice it? reschedule? M18's renice), not termination.
The incident: if it *is* yours and unexpected — verify what it's
running (the full command line) before killing anything. Prevention:
announce long jobs on shared servers; keep a baseline of "normal" so
anomalies are visible. Rehearsed in
[Lab 3](../labs/lab-03-monitoring-under-load.md).

### Incident 5 — "Application error at 3 AM"

Symptom: cron/timer-driven pipeline; morning report empty; job's log
shows `ERROR` at 03:14.

```console
$ journalctl --user -u etl.timer -b -1 --no-pager | grep -E "ERROR|fail"
Sep 15 03:14:02 ds-lab etl.sh[8812]: ERROR fetch: HTTPSConnectionPool(host='api.example.com'): Max retries exceeded
```

Root cause: upstream API unreachable at 03:14 (network blip or
rate-limit window). Two-layer fix: make the job resilient (retry with
backoff) *and* observable (the greppable log from Lesson 2 §6, so the
next 3 AM answers itself). Prevention: schedule check + alert on
absence ("no SUCCESS line by 06:00" is itself a monitorable event —
a cron job that greps *for* the success line). This is the
"application error" rehearsal in
[Lab 2](../labs/lab-02-live-tail-circuit.md) and the failed-network-
service pattern in this module's
[Troubleshooting](../troubleshooting.md).

## 4. Evidence discipline — the rules that make method work

1. **Verbatim over paraphrase.** Copy error text exactly; a paraphrased
   error can't be grepped or googled honestly.
2. **Timestamps anchor everything.** "It broke" → "it broke at
   03:14:02" → every log becomes cross-referencable.
3. **Binary tests before narrative theories.** `df -h` answers
   disk-full in 2s; no theory should outlive a cheap binary test.
4. **Change one thing at a time.** Shotgun fixes destroy the causal
   signal — you'll never know what worked.
5. **The transcript is the deliverable.** Commands + outputs,
   annotated — the same artifact in labs, tickets, and postmortems.

## 5. Try it now (10 minutes, harmless)

Run the method on your *own* machine's history as practice data:

1. **Symptom:** "boot took long once." **Evidence:**
   `systemd-analyze blame | head -5` and
   `journalctl -b -p warning.. --no-pager | tail -10`.
2. **Symptom:** "an upgrade happened last week." **Evidence:**
   `sudo grep " upgrade " /var/log/dpkg.log | tail -5`.
3. Write the five-line postmortem for either — yes, for trivia. The
   *format* is the skill; trivia is where you practice it.

## 6. Common mistakes

- Skipping step 1 ("what changed") — the answer is usually there and
  five minutes long.
- Diagnosing from `top` alone — utilization without saturation and
  identity is a vibe, not evidence.
- Fixing without verifying — the re-run IS the fix's second half.
- Postmortems that blame a person ("Dave restarted it") — root causes
  are *conditions* (no memory cap, no rotation, no alert), and
  conditions are fixable.
- Treating the method as ceremony. Under a real outage, the six steps
  compress to minutes of habit — that's the point of rehearsing them.

> **Next:** [Mini-Project E — server health & backup
> kit](../mini-project-health-backup-kit.md) packages this module
> (health.sh, backup.sh + test-restore, one incident report) into
> your first real admin toolkit.
