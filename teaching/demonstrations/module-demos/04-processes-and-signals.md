# Demo 4 — Processes & Signals: TERM vs KILL

> **Session:** S17 · **Duration:** ~10 min · **Risk:** low (VM, demo
> processes only) · **Objective:** install the signal ladder — TERM
> politely, KILL as the fire axe — by *showing* what KILL skips.

## Prerequisites

- Demo VM terminal (projected)
- The trap script below (typed live — it's 8 lines; students see it
  built, which demystifies `trap`)

## Setup (typed live, narrated)

```console
$ mkdir -p ~/demolab && cd ~/demolab
$ cat > worker.sh <<'EOF'
#!/usr/bin/env bash
tmp=$(mktemp -d)                      # create a "resource"
cleanup() { echo "cleaning up $tmp"; rm -r "$tmp"; }
trap cleanup EXIT                      # runs on normal exit AND on TERM
echo "worker running (pid $$), temp at $tmp"
while true; do echo tick >> "$tmp/log"; sleep 2; done
EOF
$ chmod +x worker.sh
```

## Procedure

**Step 1 — start it; find the PID.**

```console
$ ./worker.sh &
[1] 4321
$ jobs
[1]+  Running                 ./worker.sh &
```

**Step 2 — SIGTERM: the polite knock.**

```console
$ kill -TERM 4321
[1]+  Terminated              ./worker.sh
cleaning up /tmp/tmp.XXXX            # ← the trap ran
```

*Narration:* "TERM says 'please finish'. The script caught it, cleaned
its temp directory, exited. Let the machine be polite and it will be."

**Step 3 — restart; SIGKILL: the fire axe.**

```console
$ ./worker.sh &
[1] 4444
$ kill -9 4444
[1]+  Killed                  ./worker.sh
                                      # ← NO "cleaning up" line
$ ls /tmp/tmp.*                       # ← the temp dir is ORPHANED
/tmp/tmp.XXXX
```

*Narration:* "KILL cannot be caught — that's its *job*. The trap never
ran; the temp directory leaks. On a server, leaked resources are how
2 a.m. incidents are born."

**Step 4 — read the evidence.**

```console
$ ps aux | grep -c 'worker.sh'      # 0 (plus the grep itself — discuss)
$ free -h                            # one orphaned tmpdir is small; a thousand is a disk-full
```

*Narration:* connect to the M17 df/du mystery — deleted-but-open and
orphaned-temp are cousins.

## Expected output

As shown; PIDs and tmp dirs vary (say so). The *absence* of the
cleanup line after KILL is the demo's payload — point at it in
silence for a beat.

## Questions to ask

1. Before step 3: "predict what you will and won't see."
2. "Why can't KILL be caught?" (kernel-level; the signal isn't
   delivered to the process at all — it's the removal)
3. "Your backup script hangs. Order your kills." (TERM, wait, inspect,
   KILL last)

## Common errors & recovery

- `kill 4321` in the wrong terminal session (backgrounded jobs die with
  their shell — the `&` job belongs to *this* terminal; if the shell
  exits, SIGHUP arrives — that's the tmux teaser for M22)
- Killing by name with `pkill worker` when two copies run — the
  two-python3s story lands here; `ps aux | grep` first, then choose
- If the trap doesn't fire on TERM: the script wasn't `chmod +x`'d and
  they're running `bash worker.sh &` — check the PID they killed was
  bash's, and re-narrate `$$`

## Recovery

No state at risk: orphaned tmpdirs get cleaned in the demo's own
cleanup, and the VM snapshot is the backstop.

## Cleanup (census)

```console
$ ls /tmp/tmp.*        # show the orphans (evidence!)
$ rm -r /tmp/tmp.XXXX  # by exact name; or note that /tmp cleans on reboot
$ rm -r ~/demolab      # after the census
```

## Optional extension

`kill -HUP` on a process that reloads config (nginx later in the course
does this) — SIGHUP's "reread yourself" meaning; one sentence here,
demonstrated properly in M20/M29.
