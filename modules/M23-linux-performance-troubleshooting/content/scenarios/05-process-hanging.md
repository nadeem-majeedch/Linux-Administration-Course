# Drill Card 5 — "Process Hanging"

> Scenario family: System · Difficulty: ●●●
> Source modules: [M18](../../../M18-processes-jobs-signals/README.md), [M24 Clinic lesson 1](../../../M24-logs-journald-monitoring/content/performance/01-cpu-performance.md)

## Symptom

A process *exists* but does nothing: a notebook cell spins forever, a
`git pull` never returns, a training script sits at the same log line.
The subtle diagnostic point: **"hanging" has two very different
species** — runnable-but-starved vs blocked-on-something-forever — and
they take different fixes.

## Decision tree

```text
ps -o pid,stat,wchan:30,etime -p PID
├─ STAT R, churning CPU          → not hung: computing (or spinning) — card 4
├─ STAT S, wchan in poll/select  → waiting on input/socket — WHO was it talking to?
├─ STAT D, uninterruptible       → blocked in kernel I/O — signals WON'T help
└─ STAT T, stopped               → SIGSTOP'd (Ctrl-Z, job control) — fg/kill -CONT
```

## Evidence

```console
$ ps -o pid,ppid,stat,wchan:30,etime,cmd -p 5432    # the state fingerprint
$ ls -l /proc/5432/fd | head                        # open files/sockets — what is it holding?
$ cat /proc/5432/wchan; echo                        # kernel wait channel
$ pidstat -d -p 5432 2 3                            # any I/O at all? (0 = truly stuck)
$ pgrep -af PARENT                                  # the family tree: orphans?
```

## Fix pattern

- **S-state on a socket** → the *peer* died: find what it was talking
  to (`ss -tnp | grep <pid>` — M21), fix or bypass the peer, restart
  the process. The hang was a symptom of the connection, not the code.
- **D-state** → signals are useless by design (the process can't run
  signal handlers). Diagnose the *I/O*: which mount is wedged (stale
  NFS is the classic), is the disk saturated (card 2/3)? If the device
  is unhealthy, the process frees when the *device* does — often
  meaning a reboot is the honest fix, escalated with evidence.
- **T-state** → it was SIGSTOPped (a stray Ctrl-Z, a job-control
  accident): `kill -CONT 5432` or bring it to the foreground. The
  cheapest "fix" in this deck — and the most common on shared
  terminals.
- **Orphaned children** (parent died, kids spin) → kill the process
  group or the children by PID; check what was supposed to reap them.

## Verify

The process's *output* moves: log line advances, file grows
(`ls -l` twice), CPU/I-O counters change (`pidstat`). "Still alive"
was never the symptom; *progress* is the verification.

## Document

Record the state (`S`/`D`/`T`) and the wait channel — they're the
diagnosis. Root-cause vocabulary: *"peer died mid-request (S, poll)"*,
*"wedged FUSE mount (D, nfs_wait)"*, *"SIGSTOP'd by stray Ctrl-Z (T)"*.

**Done when:** you can stage all three species (a stopped job, a
socket-waiter via `nc` to a dead port, a D-state observation) and
write the three-line discrimination in your journal.

> ⚠️ **Never** `kill -9` as a first move — it forecloses cleanup and
> corrupts mid-write state (M18's handshake lesson). D-state processes
> ignore even that, which is the lesson's point.
