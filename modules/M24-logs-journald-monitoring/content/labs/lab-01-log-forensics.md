# Lab 1 — Log Forensics: Two Prepared Incidents

> Module 24 · Unit 6 · Difficulty: Advanced
> Time: ~45 min · Environment: your own VM (user-scope units only)
> Prerequisites: [Lesson 1](../lessons/01-journald-journalctl.md),
> [Lesson 4](../lessons/04-incident-methodology.md), M20's user services
> ⚠️ Both incidents are created by *you*, on *your* units, from
> scripts in this lab. Nothing outside `~/.config/systemd/user/` and
> your home directory is touched.

Two incidents, symptoms first, journal only as witness. For each, run
the six-step method from Lesson 4 and write the five-line postmortem.
The grading question is *what evidence led to the verdict* — a right
answer without the command that proved it is half credit.

## Setup — the lab's victim service (5 min)

A tiny "sync" service that pretends to mirror a dataset directory:

```console
$ mkdir -p ~/lab24/{data,logs} && cd ~/lab24
$ cat > sync.sh <<'EOF'
#!/usr/bin/env bash
# fake sync: touch a marker, log an ISO line, sleep
echo "$(date -Iseconds) INFO  sync run start"
touch ~/lab24/data/.synced
echo "$(date -Iseconds) INFO  sync run ok"
EOF
$ chmod +x sync.sh
$ mkdir -p ~/.config/systemd/user
$ cp sync.service.below . 2>/dev/null || true
```

Create `~/.config/systemd/user/sync.service` with **exactly** this
(note the `ExecStart` path — you'll break it later):

```ini
[Unit]
Description=Lab24 fake sync service

[Service]
ExecStart=%h/lab24/sync.sh
Type=oneshot
```

(If you changed the unit file: `systemctl --user daemon-reload`.)

```console
$ systemctl --user daemon-reload
$ systemctl --user start sync.service
$ systemctl --user status sync.service    # expect: active (exited) — oneshot semantics
$ journalctl --user -u sync.service --no-pager | tail -3
```

Record this baseline in `lab-log.md`: **this is what healthy looks
like** — status, and two INFO lines.

## Incident A — "the sync service won't start" (15 min)

**The break** (a TA applied it; you get only the symptom):

```console
$ mv ~/lab24/sync.sh ~/lab24/sync.sh.bak
```

**Reported symptom:** `systemctl --user start sync.service` fails;
`status` says `failed (Result: exit-code)`.

**Your job — method, not guessing:**

1. *Stabilize/what changed:* you know the setup; in real life this
   step = `ls -la ~/lab24/`, check recent edits. What would you look
   at first, and why?
2. *Precise symptom:* capture the full `status` output verbatim.
3. *Evidence:* `journalctl --user -u sync.service -b --no-pager |
   tail -10` — the journal names the missing file **and** the
   exit code. Record the exact line.
4. *Hypothesis + test:* "ExecStart path no longer exists" → verify
   with `systemctl --user cat sync.service | grep ExecStart` and
   `ls` the target.
5. *Fix:* `mv sync.sh.bak sync.sh`, restart, **verify** (status +
   journal line).
6. *Postmortem:* five lines. Prevention: what pre-flight check would
   have caught a moved script? (Hint: `systemd-analyze verify
   ~/.config/systemd/user/sync.service`.)

## Incident B — "the training job died overnight" (20 min)

A "train" service that actually does leak memory until the kernel
kills it. Create `~/lab24/leak.py`:

```python
#!/usr/bin/env python3
"""Lab24 'training' job: grows until the OOM killer notices it."""
import logging, time

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S")
log = logging.getLogger("train")
buf = []
epoch = 0
while True:
    epoch += 1
    buf.append(bytearray(24 * 1024 * 1024))   # 24 MB per epoch
    log.info("INFO  train epoch=%d rss_mb=%d", epoch, epoch * 24)
    time.sleep(2)
```

And `~/.config/systemd/user/train.service`:

```ini
[Unit]
Description=Lab24 fake training job

[Service]
ExecStart=%h/lab24/leak.py
MemoryMax=300M
```

`MemoryMax=300M` is the safety harness: it makes *systemd* kill this
unit at 300 MB instead of pressuring your whole VM. That's a feature
to observe, not an obstacle — and it mirrors exactly what you'd set
for real jobs (Lesson 4's prevention).

```console
$ systemctl --user daemon-reload
$ chmod +x ~/lab24/leak.py
$ systemctl --user start train.service
$ watch -n5 'systemctl --user status train.service | head -3; free -h | head -2'
```

Watch memory climb (Ctrl-C the `watch` after ~1 minute), then:

```console
$ systemctl --user status train.service
```

**Reported symptom (the 8 AM view):** the service is dead. Journal:

```console
$ journalctl --user -u train.service -b --no-pager | tail -8
```

Expect: your INFO lines (note the growing `rss_mb` — evidence of the
trend *before* death), then the kill notice. The OOM *source* line
usually surfaces in the system view — compare both namespaces:

```console
$ journalctl -k -g oom --no-pager | tail -4     # kernel's version (sudo if empty)
$ journalctl --user -u train.service -o short-precise --no-pager | tail -3
```

**Your job:** postmortem with the evidence chain: growth trend →
death time → killer (systemd's MemoryMax, functionally identical to
an OOM kill from the admin's chair) → fix (cap batch size in `leak.py`
— halve the bytearray — or raise MemoryMax *deliberately*) →
prevention (memory caps on all long jobs + watching the RSS trend
line in logs, which just saved you from guessing).

## Wrap-up — the meta-question

Both incidents were *fully* diagnosable from logs with zero guessing.
Write two sentences: which journal query gave the fastest verdict in
each incident, and what that says about where to spend learning time
(`-u` by unit? `-k` kernel? `-b -1` previous boot?).

## Done when

- [ ] Baseline + both postmortems in `lab-log.md` (five lines each,
      evidence commands quoted)
- [ ] `train.service` fixed and stopped cleanly
      (`systemctl --user stop train.service`)
- [ ] `systemd-analyze verify` run on both units, output recorded
- [ ] The meta-question answered
