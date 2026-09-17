# Lab 2 — Live Tail Circuit: Watching While It Happens

> Module 24 · Unit 6 · Difficulty: Intermediate
> Time: ~40 min · Environment: your own VM
> Prerequisites: [Lesson 1](../lessons/01-journald-journalctl.md),
> [Lesson 2](../lessons/02-classic-logs-rotation.md), M20 user services
> ⚠️ All traffic is your own units' output. No system logs are
> modified; nothing is installed.

Three drills: *watch* events live, *write* a greppable logger, and
*follow* a file like a tailor-made `tail -f`. The skill being built:
when something happens, your first reflex is a terminal that is
already watching.

## Drill 1 — the two-terminal reflex (10 min)

**Terminal 1** — the watcher:

```console
$ journalctl -f -p info.. --no-pager
```

**Terminal 2** — the actor. One at a time, and after each, find the
event in Terminal 1 (the newest lines land at the bottom):

```console
$ systemctl --user restart sync.service        # from Lab 1's setup
$ touch ~/lab24/data/.synced                   # no log... (why not? think)
$ python3 -c "print('hello journal')" | systemd-cat -t lab24cat
$ logger -p user.warning "lab24: this is a warning test"
```

Questions for `lab-log.md`: which actions appeared in the journal and
which didn't — and what does that tell you about *what the journal
collects* (stdout of services vs arbitrary file writes)? Which
`journalctl` field would let you find *only* the `lab24cat` lines?

Now the reverse — filter the flood *before* it hits your screen:

```console
# Terminal 1, restart the watcher with a tighter filter:
$ journalctl -f -t lab24cat -t train
# Terminal 2:
$ python3 -c "print('second entry')" | systemd-cat -t lab24cat
$ logger -p user.warning "lab24: this should NOT appear"
```

The `logger` line is warning-level but wrong `-t` tag: the watcher
misses it. **Tag + priority = your two filter dimensions.** Record
which you'd use for "only my training job's errors".

## Drill 2 — write a logger worth grepping (15 min)

Create `~/lab24/logger_demo.py` — a compliant version of the
[Lesson 2 §6](../lessons/02-classic-logs-rotation.md) contract:

```python
#!/usr/bin/env python3
"""Lab24: emits greppable, ISO-8601, key=value log lines."""
import logging, sys, time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z",
    stream=sys.stdout,
)
log = logging.getLogger("demo")

for run in range(1, 6):
    log.info("run id=exp42 n=%d stage=fetch status=ok", run)
    log.info("run id=exp42 n=%d stage=transform status=ok rows=%d", run, run * 100)
    if run == 3:
        log.error("run id=exp42 n=%d stage=load status=failed reason=timeout", run)
    time.sleep(0.5)
```

Run it into the journal and interrogate it like an incident:

```console
$ python3 logger_demo.py | systemd-cat -t demo
$ journalctl -t demo --no-pager --since "-2 min"
$ journalctl -t demo -p err.. --no-pager --since "-2 min"     # just the failure
$ journalctl -t demo -o json-pretty --no-pager | head -20     # the field view
```

Then prove the contract with M08 pipelines against the text output:

```console
$ journalctl -t demo --no-pager --since "-2 min" | grep -c "status=ok"
$ journalctl -t demo --no-pager --since "-2 min" | grep ERROR
$ journalctl -t demo --no-pager --since "-2 min" \
  | grep -o "rows=[0-9]*" | cut -d= -f2 | paste -sd+ | bc     # sum of rows
```

Record in `lab-log.md`: the one-line answer to *"why does ISO-8601
`--since "-2 min"` filtering work without you parsing dates?"* — that
is the whole payoff of the format.

## Drill 3 — tail a file like an operator (10 min)

Not everything logs to the journal; batch jobs often write files.
Create a job that appends ISO lines, then follow it live:

```console
$ (while true; do echo "$(date -Iseconds) INFO  heartbeat ok" >> ~/lab24/logs/beat.log; sleep 3; done) &
$ tail -f ~/lab24/logs/beat.log
```

Watch two or three heartbeats land (Ctrl-C to stop watching — the
*writer* keeps going for now). Then the operator's addendum:

```console
$ tail -f ~/lab24/logs/beat.log | grep --line-buffered ERROR
```

No errors yet — good, you're watching a healthy file. Kill the
background writer **by PID, the M18 way**:

```console
$ pgrep -af "beat.log"          # find the loop's PID (scope it: it's the 'while' shell)
$ kill <PID>                    # TERM, wait, verify gone with pgrep again
```

## Wrap-up — the reflex inventory

Three commands now in your reflex set: `journalctl -f` (filtered by
tag/priority), `tail -f` (+grep), and `systemd-cat` (making your own
tools journal-native). Write one sentence each on when you'd reach
for which — service output vs file-based batch job vs "I want fields
and retention for free".

## Cleanup

```console
$ pkill -f "beat.log" 2>/dev/null; pgrep -af "beat.log" || echo "writer stopped"
```

## Done when

- [ ] All three drills' answers recorded in `lab-log.md`
- [ ] The bc pipeline summed rows correctly (show the number)
- [ ] Background writer confirmed dead
- [ ] Reflex inventory written (one sentence × 3)
