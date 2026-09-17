# Drill Book — Incident 4: The Phantom Hang

> Setup time: 5 min · Solve time: ~30 min · The finale: two real faults, one red herring
> Cards: [5 — Process hanging](../scenarios/05-process-hanging.md) + [8 — Connectivity](../scenarios/08-connectivity-failure.md)

## Setup

```bash
#!/usr/bin/env bash
# setup-incident-4.sh — a "hung" data worker with a dead dependency
set -euo pipefail
mkdir -p ~/drill4 && cd ~/drill4

# the "remote dataset source": a local listener that will DIE mid-flight
nc -l -p 5060 > /dev/null 2>&1 &        # the peer
echo $! > peer.pid

# the worker: connects, requests, waits forever on a socket that's about to close
cat > worker.sh <<'EOF'
#!/usr/bin/env bash
echo "$(date -Is) worker: dialing dataset source"
exec 3<>/dev/tcp/127.0.0.1/5060 || exit 1
echo "$(date -Is) worker: connected, requesting" >&3
echo "$(date -Is) worker: awaiting data…"
timeout 900 cat <&3          # the hang: 15 minutes of patient nothing
EOF
chmod +x worker.sh
nohup ./worker.sh > worker.log 2>&1 &
echo $! > worker.pid

sleep 1
kill "$(cat peer.pid)"                 # THE BREAK: the peer dies after handshake
echo "Incident 4 staged."
```

## The symptom

```console
$ tail -2 ~/drill4/worker.log
2026-09-16T14:02:11 worker: connected, requesting
2026-09-16T14:02:11 worker: awaiting data…
# …and nothing. For 15 minutes, nothing.
```

**Your incident brief:** "The nightly dataset worker is hung again.
Third time this week. Someone already tried `kill -9`; they say it
*didn't even die*, which is 'impossible'."

## Solving notes (for the grader in you)

- **The red herring is in the brief**: "tried kill -9, didn't die." A
  process that ignores SIGKILL is in **D-state** (card 5) — *except*
  this one isn't: it's an **S-state socket-wait**, and the SIGKILL
  "failure" was likely misread (killed the wrong PID — the `nc` peer
  or the log tail — or signaled before checking). Teaching point: the
  brief lies by compression; the `ps` state column doesn't.
- The discrimination, in order: `ps -o pid,stat,wchan:30,etime -p
  $(cat worker.pid)` → `S`, `wchan` in poll/wait → *blocked on
  I/O-with-a-peer*, not CPU, not kernel I/O. Then
  `ls -l /proc/$(cat worker.pid)/fd` → the socket to port 5060 →
  `ss -tnp | grep 5060` → the peer is *gone* (card 8's rung 5 from the
  other side: this time *your* process was the client).
- The safe tests: `cat /proc/net/tcp` grep for the port's state
  (CLOSE-WAIT territory — the peer closed, your side hasn't), and the
  socket-count check (`ss -s`) for the leak vocabulary.
- The fix: the worker is a casualty — `kill $(cat worker.pid)` (SIGTERM;
  it's in S-state, it *will* die) — and the *root cause* is the peer's
  lifecycle: nothing restarts or monitors it. The prevention sentence
  is the M19/M24 pattern: the peer needs a supervised unit or a
  healthcheck, and the worker needs a timeout that *alerts* (its 900 s
  timeout silently exits — fail-loudly contract, M27 Lab 3 Part D).
- The verify: worker terminated (census), and the *original nightly
  workflow* re-run against a healthy peer (`nc -l -p 5060` by hand)
  completes its handshake.

**Done when:** the journal discriminates S vs D (killing the "kill -9
didn't work" myth with the state column), names the dead peer as root
cause with socket evidence, and the prevention names both the
supervision gap and the silent timeout.

---
*Drill Book complete. Log the four blocks, self-score against the
[rubric](README.md#per-incident-deliverable-the-rubrics-checklist),
then take the [quiz](../practice/quiz.md).*
